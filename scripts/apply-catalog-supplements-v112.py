from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "public" / "data" / "catalog_master.csv"
SUPPLEMENTS_DIR = ROOT / "scripts" / "catalog-supplements"
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


def clean(value):
    return str(value or "").strip()


def key(row):
    return (
        clean(row.get("Артикул")),
        clean(row.get("Цвет")),
        clean(row.get("Аромат")),
        clean(row.get("Размер")),
    )


def read_rows(path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        headers = reader.fieldnames or []
        if headers != EXPECTED_HEADERS:
            raise SystemExit(f"CATALOG_SUPPLEMENTS_V112: unexpected headers in {path.relative_to(ROOT)}: {headers}")
        return list(reader)


if not MASTER.is_file():
    raise SystemExit("CATALOG_SUPPLEMENTS_V112: catalog_master.csv is missing")

master_rows = read_rows(MASTER)
supplement_files = sorted(SUPPLEMENTS_DIR.glob("*.csv")) if SUPPLEMENTS_DIR.is_dir() else []
if not supplement_files:
    print("// CATALOG_SUPPLEMENTS_V112: no supplements found; unchanged")
    raise SystemExit(0)

supplement_rows = []
for path in supplement_files:
    rows = read_rows(path)
    for row in rows:
        if not clean(row.get("Артикул")):
            raise SystemExit(f"CATALOG_SUPPLEMENTS_V112: blank article in {path.relative_to(ROOT)}")
        supplement_rows.append(row)

supplement_keys = [key(row) for row in supplement_rows]
if len(supplement_keys) != len(set(supplement_keys)):
    raise SystemExit("CATALOG_SUPPLEMENTS_V112: duplicate SKU keys across supplements")

supplement_key_set = set(supplement_keys)
kept_rows = [row for row in master_rows if key(row) not in supplement_key_set]
replaced = len(master_rows) - len(kept_rows)
merged_rows = kept_rows + supplement_rows

with MASTER.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=EXPECTED_HEADERS, delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(merged_rows)

articles_added = sorted({clean(row.get("Артикул")) for row in supplement_rows})
print(
    f"// CATALOG_SUPPLEMENTS_V112: supplements={len(supplement_files)}; "
    f"applied_rows={len(supplement_rows)}; replaced_existing_rows={replaced}; "
    f"master_rows={len(merged_rows)}; articles={','.join(articles_added)}"
)
