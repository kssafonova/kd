from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
MARKER = "// GROUPED_CATALOG_V98"
OLD = '.filter(row=>row["Артикул"]&&row["Название товара"]&&row["Категория"]&&row["Подкатегория"]);'
NEW = '.filter(row=>row["Артикул"]&&row["Название товара"]);'

text = PAGE.read_text(encoding="utf-8")
if MARKER in text:
    print(f"{MARKER}: already applied")
    raise SystemExit(0)
if OLD not in text:
    raise SystemExit("Required catalog row filter fragment not found")
text = text.replace("// GROUPED_CATALOG_V96", f"// GROUPED_CATALOG_V98\n// GROUPED_CATALOG_V96", 1)
text = text.replace(OLD, NEW, 1)
PAGE.write_text(text, encoding="utf-8")
print(f"{MARKER}: category/subcategory are optional; every article from grouped CSV remains in All products")
