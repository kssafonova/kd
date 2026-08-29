from pathlib import Path
import csv
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "product-source" / "all_site_products_grouped.csv"
IMAGE_DIR = ROOT / "public" / "images" / "imported-products"
PHOTO_FIELDS = ["Фото 1", "Фото 2", "Фото 3"]

def clean(value):
    text = str(value or "").strip()
    return "" if not text or text.lower() == "null" else text

referenced = set()
missing = []
with SOURCE.open("r", encoding="utf-8-sig", newline="") as fh:
    for row in csv.DictReader(fh, delimiter=";"):
        article = clean(row.get("Артикул"))
        for field in PHOTO_FIELDS:
            value = clean(row.get(field))
            if not value:
                continue
            name = Path(urlparse(value).path).name
            if not name:
                missing.append((article, field, value, "invalid filename"))
                continue
            referenced.add(name)
            path = IMAGE_DIR / name
            if not path.is_file() or path.stat().st_size <= 0:
                missing.append((article, field, name, "missing file"))

if missing:
    print(f"GROUPED_IMAGES_V99: {len(missing)} missing image references")
    for item in missing[:200]:
        print(" | ".join(item))
    raise SystemExit(1)

print(f"GROUPED_IMAGES_V99: all {len(referenced)} referenced image files exist in {IMAGE_DIR.relative_to(ROOT)}")
