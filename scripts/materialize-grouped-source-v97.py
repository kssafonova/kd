from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "scripts" / "product-source" / "all_site_products_grouped.csv"
EXPECTED_HEADERS = [
    "ID","Артикул","Название товара","Цвет","Аромат","Размер","Цена","Старая цена","Высота","Ширина","Объем","Диаметр",
    "Комплектация / информация о размере","Материал","Состав","Детали","Коллекция","Капсула","Категория","Подкатегория",
    "Товар входит в готовое решение","Опционально входит в готовое решение","Капсула.1","Фото 1","Фото 2","Фото 3"
]

with TARGET.open("r", encoding="utf-8-sig", newline="") as fh:
    reader = csv.DictReader(fh, delimiter=";")
    if reader.fieldnames != EXPECTED_HEADERS:
        raise SystemExit(f"Unexpected canonical source headers: {reader.fieldnames}")
    rows = list(reader)

articles = {
    str(row.get("Артикул") or "").strip()
    for row in rows
    if str(row.get("Артикул") or "").strip()
}
print(
    f"// GROUPED_SOURCE_V106: using committed canonical catalog source; "
    f"{len(rows)} rows / {len(articles)} articles -> {TARGET.relative_to(ROOT)}"
)
