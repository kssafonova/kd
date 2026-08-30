from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "apply-table-driven-catalog-v135.py"
text = TARGET.read_text(encoding="utf-8")
old = 'generated, count = re.subn(loader_pattern, strict_loader, generated, count=1, flags=re.S)'
new = 'generated, count = re.subn(loader_pattern, lambda _match: strict_loader, generated, count=1, flags=re.S)'
if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("TABLE_DRIVEN_CATALOG_FIX_V136: replacement signature not found")
TARGET.write_text(text, encoding="utf-8")
print("// TABLE_DRIVEN_CATALOG_FIX_V136: preserve literal \\n escapes in generated TypeScript loader")
