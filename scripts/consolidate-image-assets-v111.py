from pathlib import Path
import hashlib
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "assets" / "images"
PUBLIC_MIRROR = ROOT / "public" / "assets" / "images"
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".svg", ".ico"}
TEXT_EXTS = {".ts", ".tsx", ".js", ".jsx", ".json", ".csv", ".py", ".yml", ".yaml", ".md", ".css", ".html", ".txt"}
SOURCE_ROOTS = [ROOT / "app", ROOT / "scripts", ROOT / "public" / "data", ROOT / ".github"]

CANONICAL.mkdir(parents=True, exist_ok=True)
canonical_preexisting = any(path.is_file() and path.suffix.lower() in IMAGE_EXTS for path in CANONICAL.iterdir())

# Once the canonical library exists, root /images is only a legacy Pages copy.
# Remove it before scanning so repeated builds cannot remap canonical URLs through stale duplicates.
if canonical_preexisting and (ROOT / "images").exists():
    shutil.rmtree(ROOT / "images")


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_name(path: Path) -> str:
    parts = [re.sub(r"[^A-Za-z0-9._-]+", "-", p) for p in path.parts]
    return "__".join(parts)


def priority(path: Path):
    rel = path.relative_to(ROOT).parts
    if rel[:3] == ("public", "images", "imported-products"):
        return (0, path.as_posix())
    if rel[:2] == ("public", "images"):
        return (1, path.as_posix())
    if rel and rel[0] == "public":
        return (2, path.as_posix())
    if rel and rel[0] == "images":
        return (3, path.as_posix())
    return (4, path.as_posix())

existing_by_hash = {}
existing_names = {}
for path in CANONICAL.glob("*"):
    if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
        value = digest(path)
        existing_by_hash[value] = path
        existing_names[path.name.lower()] = value

candidates = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in IMAGE_EXTS:
        continue
    rel = path.relative_to(ROOT)
    if rel.parts[:2] == ("assets", "images"):
        continue
    if rel.parts and rel.parts[0] in {".git", "node_modules", ".next", "exports", "export", "_next"}:
        continue
    candidates.append(path)

mapping = {}
moved = 0
deduped = 0
for src in sorted(candidates, key=priority):
    rel = src.relative_to(ROOT)
    value = digest(src)
    if value in existing_by_hash:
        dest = existing_by_hash[value]
        deduped += 1
    else:
        name = src.name
        used_hash = existing_names.get(name.lower())
        if used_hash and used_hash != value:
            name = safe_name(rel)
        if name.lower() in existing_names and existing_names[name.lower()] != value:
            name = f"{Path(name).stem}__{value[:10]}{src.suffix.lower()}"
        dest = CANONICAL / name
        shutil.copy2(src, dest)
        existing_by_hash[value] = dest
        existing_names[dest.name.lower()] = value
        moved += 1

    new_url = f"/assets/images/{dest.name}"
    rel_posix = rel.as_posix()
    mapping[f"/{rel_posix}"] = new_url
    if rel.parts and rel.parts[0] == "public":
        public_rel = Path(*rel.parts[1:]).as_posix()
        mapping[f"/{public_rel}"] = new_url
    src.unlink()

for stale_dir in [ROOT / "public" / "images", ROOT / "images", ROOT / "public" / "assets" / "images"]:
    if stale_dir.exists():
        shutil.rmtree(stale_dir)

text_files = []
for base in SOURCE_ROOTS:
    if not base.exists():
        continue
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTS and path != Path(__file__):
            text_files.append(path)
for path in ROOT.iterdir():
    if path.is_file() and path.suffix.lower() in TEXT_EXTS:
        text_files.append(path)

exact_pattern = None
if mapping:
    exact_pattern = re.compile("|".join(re.escape(key) for key in sorted(mapping, key=len, reverse=True)))

local_prefix_patterns = [
    (re.compile(r"(^|[\"'`(=:\s])\/public\/images\/", re.M), r"\1/assets/images/"),
    (re.compile(r"(^|[\"'`(=:\s])\/images\/imported-products\/", re.M), r"\1/assets/images/"),
    (re.compile(r"(^|[\"'`(=:\s])images\/imported-products\/", re.M), r"\1assets/images/"),
    (re.compile(r"(^|[\"'`(=:\s])\/images\/", re.M), r"\1/assets/images/"),
]

changed_files = 0
for path in sorted(set(text_files)):
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    original = text
    if exact_pattern:
        text = exact_pattern.sub(lambda match: mapping[match.group(0)], text)
    for pattern, replacement in local_prefix_patterns:
        text = pattern.sub(replacement, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        changed_files += 1

PUBLIC_MIRROR.mkdir(parents=True, exist_ok=True)
for src in CANONICAL.glob("*"):
    if src.is_file() and src.suffix.lower() in IMAGE_EXTS:
        shutil.copy2(src, PUBLIC_MIRROR / src.name)

legacy_refs = []
for path in sorted(set(text_files)):
    if not path.exists():
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    if any(pattern.search(text) for pattern, _ in local_prefix_patterns):
        legacy_refs.append(str(path.relative_to(ROOT)))
if legacy_refs:
    raise SystemExit("IMAGE_ASSETS_V111: stale local image references remain:\n" + "\n".join(legacy_refs[:100]))

canonical_count = sum(1 for p in CANONICAL.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS)
print(
    f"// IMAGE_ASSETS_V111: canonical assets/images contains {canonical_count} image files; "
    f"moved={moved}; deduped={deduped}; rewritten_files={changed_files}; "
    f"legacy_root_removed={canonical_preexisting}; public mirror materialized"
)
