from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    (ROOT / "scripts" / "product-source" / "all_site_products_grouped.csv", ";"),
    (ROOT / "public" / "data" / "catalog_xlsx_full.csv", ","),
]
EXCLUDED_ARTICLES = {
    "KD-PD-10842",
    "KD-PD-10787",
    "KD-PD-8983",
    "KD-PD-8124",
    "KD-PD-11448",
    "KD-PD-11439",
    "KD-PD-11435",
    "KD-PD-8986",
    "KD-PD-10451",
    "KD-PD-1143826",
}
EXCLUDED_PRODUCT_NAMES = {
    "Чайная пара Эхо",
}

for path, delimiter in TARGETS:
    if not path.exists():
        continue
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=delimiter)
        headers = reader.fieldnames or []
        rows = list(reader)
    article_key = "Артикул"
    name_key = "Название товара"
    kept = [
        row for row in rows
        if str(row.get(article_key) or "").strip() not in EXCLUDED_ARTICLES
        and str(row.get(name_key) or "").strip() not in EXCLUDED_PRODUCT_NAMES
    ]
    removed = len(rows) - len(kept)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    print(f"// REMOVE_REQUESTED_ARTICLES_V103: {path.relative_to(ROOT)} removed {removed} rows; {len(kept)} rows remain")
