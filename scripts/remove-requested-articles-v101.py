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
    "KD-PD-11517",
    "KD-PD-11433",
}

# The uploaded catalog references five image filenames that are not present in
# public/images/imported-products. Reuse the verified existing product photo for
# four Echo products. For KD-PD-8305, leave the photo empty rather than display
# an unrelated product; the storefront will use its normal placeholder.
PRIMARY_PHOTO_FALLBACKS = {
    "KD-PD-11436": "6a3a77a9a9ef4_big.jpg",
    "KD-PD-11441": "6a394aeea5edf_big.jpg",
    "KD-PD-11449": "6a3a85f308820_big.jpg",
    "KD-PD-11440": "6a394af59a5dc_big.jpg",
    "KD-PD-8305": "",
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
    photo_key = "Фото 1" if delimiter == ";" else "Превью фотография товара"
    corrected = 0
    photo_corrected = 0
    for row in rows:
        article = str(row.get(article_key) or "").strip()
        name = str(row.get(name_key) or "").strip()
        if name == "Чайная пара Эхо" and article == "KD-PD-11438":
            row[article_key] = "KD-PD-1143826"
            article = "KD-PD-1143826"
            corrected += 1

        if article in PRIMARY_PHOTO_FALLBACKS and photo_key in row:
            filename = PRIMARY_PHOTO_FALLBACKS[article]
            desired = (
                f"https://kssafonova.github.io/images/imported-products/{filename}"
                if delimiter == ";" and filename
                else f"/images/imported-products/{filename}"
                if filename
                else ""
            )
            if str(row.get(photo_key) or "").strip() != desired:
                row[photo_key] = desired
                photo_corrected += 1

    kept = [
        row for row in rows
        if str(row.get(article_key) or "").strip() not in EXCLUDED_ARTICLES
    ]
    removed = len(rows) - len(kept)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers, delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        writer.writerows(kept)
    print(
        f"// CATALOG_CORRECTIONS_V106: {path.relative_to(ROOT)} corrected Echo tea-pair article in {corrected} row(s); "
        f"corrected {photo_corrected} missing primary photo reference(s); removed {removed} excluded row(s); {len(kept)} rows remain"
    )
