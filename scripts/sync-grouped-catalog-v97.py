from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "product-source" / "all_site_products_grouped.csv"
OUT = ROOT / "public" / "data" / "catalog_xlsx_full.csv"

SOURCE_HEADERS = [
    "ID","Артикул","Название товара","Цвет","Аромат","Размер","Цена","Старая цена","Высота","Ширина","Объем","Диаметр",
    "Комплектация / информация о размере","Материал","Состав","Детали","Коллекция","Капсула","Категория","Подкатегория",
    "Товар входит в готовое решение","Опционально входит в готовое решение","Капсула.1","Фото 1","Фото 2","Фото 3"
]
OUT_HEADERS = [
    "Id","Артикул","Название товара","Цвет","Аромат","Размер","Цена","Старая цена","Высота","Ширина","Объем","Диаметр",
    "Комплектация / Информация о размере","Материал","Состав","Детали","Коллекция","Капсула","Категория","Подкатегория",
    "Товар входит в готовое решение","Опционально входит в готовое решение","Описание готового решения",
    "Превью фотография товара","Вторая фотография товара в скролле","Третья фотография в стролле"
]
MAP = dict(zip(SOURCE_HEADERS, OUT_HEADERS))
PHOTO_FIELDS = ["Фото 1","Фото 2","Фото 3"]
PHOTO_PREFIX = "https://kssafonova.github.io/images/imported-products/"

def clean(value):
    text = str(value or "").strip()
    return "" if not text or text.lower() == "null" else text

with SOURCE.open("r", encoding="utf-8-sig", newline="") as fh:
    reader = csv.DictReader(fh, delimiter=";")
    if reader.fieldnames != SOURCE_HEADERS:
        raise SystemExit(f"Unexpected grouped source headers: {reader.fieldnames}")
    rows = list(reader)

for row in rows:
    for field in PHOTO_FIELDS:
        value = clean(row.get(field))
        if value and not value.startswith(PHOTO_PREFIX):
            raise SystemExit(f"Invalid photo URL in {field} for {row.get('Артикул')}: {value}")

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=OUT_HEADERS, lineterminator="\n")
    writer.writeheader()
    for source in rows:
        target = {out: clean(source.get(src)) for src, out in MAP.items()}
        writer.writerow(target)

articles = {clean(row.get("Артикул")) for row in rows if clean(row.get("Артикул"))}
categories = {clean(row.get("Категория")) for row in rows if clean(row.get("Категория"))}
null_category_articles = {clean(row.get("Артикул")) for row in rows if clean(row.get("Артикул")) and not clean(row.get("Категория"))}
print(f"// GROUPED_CATALOG_V97: {len(rows)} rows / {len(articles)} article cards; {len(categories)} named categories; {len(null_category_articles)} uncategorized cards kept in All products -> {OUT.relative_to(ROOT)}")
