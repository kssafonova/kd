from __future__ import annotations

from pathlib import Path
import csv
import posixpath
import shutil
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
PUBLIC_IMAGES = ROOT / "public" / "images"
BUILT_IMAGES = ROOT / "images"
IMAGE_DIR = PUBLIC_IMAGES / "imported-products"
PHOTO_FIELDS = [
    "Превью фотография товара",
    "Вторая фотография товара в скролле",
    "Третья фотография в стролле",
]
MARKER = "// IMPORTED_PRODUCT_IMAGES_V90"


def image_basename(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme else value
    return posixpath.basename(path.rstrip("/"))


def build_source_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for base in (PUBLIC_IMAGES, BUILT_IMAGES):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.parent != IMAGE_DIR:
                index.setdefault(path.name, path)
    return index


def main() -> None:
    if not CATALOG.exists():
        raise SystemExit(f"Missing generated catalog: {CATALOG}")
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = reader.fieldnames or []

    missing_columns = [field for field in PHOTO_FIELDS if field not in fields]
    if missing_columns:
        raise SystemExit("Missing photo columns: " + ", ".join(missing_columns))

    referenced: set[str] = set()
    for row in rows:
        for field in PHOTO_FIELDS:
            filename = image_basename(row.get(field, ""))
            if not filename:
                row[field] = ""
                continue
            referenced.add(filename)
            row[field] = f"/images/imported-products/{filename}"

    source_index = build_source_index()
    copied: list[str] = []
    missing_files: list[str] = []
    for filename in sorted(referenced):
        target = IMAGE_DIR / filename
        if target.is_file():
            continue
        source = source_index.get(filename)
        if source and source.is_file():
            shutil.copy2(source, target)
            copied.append(filename)
        else:
            missing_files.append(filename)

    if missing_files:
        sample = ", ".join(missing_files[:30])
        suffix = "" if len(missing_files) <= 30 else f" … +{len(missing_files)-30} more"
        raise SystemExit(
            f"{len(missing_files)} table image filenames do not exist anywhere under public/images or built images: {sample}{suffix}"
        )

    with CATALOG.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(
        f"{MARKER}: {len(rows)} SKU rows, {len(referenced)} unique table image filenames, "
        f"{len(copied)} copied into public/images/imported-products -> /images/imported-products/"
    )


if __name__ == "__main__":
    main()
