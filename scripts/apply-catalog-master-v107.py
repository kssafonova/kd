from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
text = PAGE.read_text(encoding="utf-8")
original = text

replacements = [
    ("type XlsxProductEntityRow = Record<string,string>;", "type CatalogMasterRow = Record<string,string>;"),
    ("let xlsxCatalogLoaded = false;", "let catalogMasterLoaded = false;"),
    ('const XLSX_ENTITY_FILES:string[] = ["catalog_xlsx_full.csv"]; // FULL_CSV_CATALOG_V89',
     'const CATALOG_MASTER_FILES:string[] = ["catalog_master.csv"]; // CATALOG_MASTER_V107'),
    ("XlsxProductEntityRow", "CatalogMasterRow"),
    ("xlsxCatalogLoaded", "catalogMasterLoaded"),
    ("loadXlsxCatalogIntoProducts", "loadCatalogMasterIntoProducts"),
    ("setXlsxCatalogRevision", "setCatalogMasterRevision"),
    ("XLSX_ENTITY_FILES", "CATALOG_MASTER_FILES"),
    ("`xlsx-${id}-${index}`", "`master-${id}-${index}`"),
    ('row["Превью фотография товара"],row["Вторая фотография товара в скролле"],row["Третья фотография в стролле"]',
     'row["Фото 1"],row["Фото 2"],row["Фото 3"]'),
    ('row["Комплектация / Информация о размере"]', 'row["Комплектация / информация о размере"]'),
]
for old, new in replacements:
    text = text.replace(old, new)

needle = '  const text=source.replace(/^\\\\uFEFF/,"");\n'
if needle in text and 'const delimiter=headerLine.includes(";")?";":",";' not in text:
    text = text.replace(
        needle,
        needle + '  const headerLine=text.split(/\\\\r?\\\\n/,1)[0]??"";\n'
        '  const delimiter=headerLine.includes(";")?";":",";\n',
        1,
    )
text = text.replace('else if(char===","){row.push(cell);cell=""}', 'else if(char===delimiter){row.push(cell);cell=""}')

compressed_pattern = re.compile(
    r'const loadCompressedEntityCsv=async\(\)=>\{.*?\n\};\n(?=const entityColorHex=)',
    re.S,
)
text, removed = compressed_pattern.subn("", text, count=1)

for stale in [
    "catalog_xlsx_full.csv",
    "kultura_doma_product_entities_xlsx_extra.b64",
    "Превью фотография товара",
    "Вторая фотография товара в скролле",
    "Третья фотография в стролле",
    "Комплектация / Информация о размере",
]:
    if stale in text:
        raise SystemExit(f"CATALOG_MASTER_UI_V107: stale reference remains: {stale}")

required = [
    'const CATALOG_MASTER_FILES:string[] = ["catalog_master.csv"];',
    'row["Фото 1"],row["Фото 2"],row["Фото 3"]',
    'row["Комплектация / информация о размере"]',
    "char===delimiter",
    "loadCatalogMasterIntoProducts",
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"CATALOG_MASTER_UI_V107: required marker missing: {marker}")

PAGE.write_text(text, encoding="utf-8")
print(
    f"// CATALOG_MASTER_UI_V107: page loader uses catalog_master.csv semicolon schema; "
    f"compressed legacy loader removed={removed}; changed={text != original}"
)
