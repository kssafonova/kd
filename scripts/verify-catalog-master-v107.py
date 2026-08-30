from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "public" / "data" / "catalog_master.csv"
CANONICAL_IMAGES = ROOT / "assets" / "images"
EXPECTED_HEADERS = [
    "Артикул",
    "Название товара",
    "Цвет",
    "Аромат",
    "Размер",
    "Цена",
    "Старая цена",
    "Высота",
    "Ширина",
    "Объем",
    "Диаметр",
    "Комплектация / информация о размере",
    "Материал",
    "Состав",
    "Детали",
    "Коллекция",
    "Капсула",
    "Категория",
    "Подкатегория",
    "Товар входит в готовое решение",
    "Опционально входит в готовое решение",
    "Фото 1",
    "Фото 2",
    "Фото 3",
    "Описание готового решения",
]
EXPECTED_ROWS = 210
EXPECTED_ARTICLES = 137
PHOTO_COLUMNS = ["Фото 1", "Фото 2", "Фото 3"]
STALE_FILES = [
    ROOT / "public" / "data" / "all_site_products_grouped.csv",
    ROOT / "public" / "data" / "catalog_truth.json.gz.b64",
    ROOT / "public" / "data" / "catalog_xlsx_full.csv",
    *[ROOT / "public" / "data" / f"kultura_doma_product_entities_xlsx_{index}.csv" for index in range(1, 6)],
    ROOT / "public" / "data" / "kultura_doma_product_entities_xlsx_extra.b64",
]
STALE_IMAGE_DIRS = [ROOT / "public" / "images", ROOT / "images"]

def clean(value):
    text = str(value or "").strip()
    return "" if not text or text.lower() == "null" else text

errors = []
if not MASTER.exists():
    raise SystemExit(f"CATALOG_MASTER_V107: missing {MASTER.relative_to(ROOT)}")
if not CANONICAL_IMAGES.is_dir():
    errors.append("canonical assets/images folder is missing")

with MASTER.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    headers = reader.fieldnames or []
    rows = list(reader)

if headers != EXPECTED_HEADERS:
    errors.append(f"unexpected headers: {headers}")
if len(rows) != EXPECTED_ROWS:
    errors.append(f"expected {EXPECTED_ROWS} SKU rows, got {len(rows)}")

articles = {clean(row.get("Артикул")) for row in rows if clean(row.get("Артикул"))}
if len(articles) != EXPECTED_ARTICLES:
    errors.append(f"expected {EXPECTED_ARTICLES} articles, got {len(articles)}")

for index, row in enumerate(rows, start=2):
    article = clean(row.get("Артикул"))
    name = clean(row.get("Название товара"))
    if not article:
        errors.append(f"row {index}: blank article")
    if not name:
        errors.append(f"row {index}: blank product name")

photo_refs = []
for row in rows:
    article = clean(row.get("Артикул"))
    for column in PHOTO_COLUMNS:
        ref = clean(row.get(column))
        if not ref:
            continue
        photo_refs.append(ref)
        prefix = "/assets/images/"
        if not ref.startswith(prefix):
            errors.append(f"{article} {column}: non-canonical photo path {ref}")
            continue
        filename = ref[len(prefix):]
        target = CANONICAL_IMAGES / filename
        if not target.is_file():
            errors.append(f"{article} {column}: missing canonical repository image {filename}")

duplicates = len(rows) - len({tuple(row.get(header, "") for header in EXPECTED_HEADERS) for row in rows})
if duplicates:
    errors.append(f"{duplicates} duplicate rows")

for stale in STALE_FILES:
    if stale.exists():
        errors.append(f"stale catalog file still exists: {stale.relative_to(ROOT)}")
for stale_dir in STALE_IMAGE_DIRS:
    if stale_dir.exists():
        errors.append(f"stale image directory still exists: {stale_dir.relative_to(ROOT)}")

if errors:
    print(f"CATALOG_MASTER_V107: {len(errors)} errors")
    print("\n".join(errors))
    sys.exit(1)

categories = {clean(row.get("Категория")) for row in rows if clean(row.get("Категория"))}
subcategories = {clean(row.get("Подкатегория")) for row in rows if clean(row.get("Подкатегория"))}
canonical_count = sum(1 for path in CANONICAL_IMAGES.iterdir() if path.is_file())
print(
    f"// CATALOG_MASTER_V107: {len(rows)} SKU rows / {len(articles)} articles; "
    f"{len(categories)} categories / {len(subcategories)} subcategories; "
    f"{len(photo_refs)} photo references / {len(set(photo_refs))} unique catalog images verified; "
    f"{canonical_count} canonical image assets total"
)
