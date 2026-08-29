from pathlib import Path
import csv
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts" / "product-source" / "all_site_products_grouped.csv"
RUNTIME = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
IMAGE_DIR = ROOT / "public" / "images" / "imported-products"
SOURCE_PHOTOS = ["Фото 1", "Фото 2", "Фото 3"]
RUNTIME_PHOTOS = ["Превью фотография товара", "Вторая фотография товара в скролле", "Третья фотография в стролле"]
LOCAL_PREFIX = "/images/imported-products/"


def clean(value):
    text = str(value or "").strip()
    return "" if not text or text.lower() == "null" else text


def expected_local(value):
    value = clean(value)
    if not value:
        return ""
    filename = Path(urlparse(value).path).name
    return f"{LOCAL_PREFIX}{filename}" if filename else ""

with SOURCE.open("r", encoding="utf-8-sig", newline="") as fh:
    source_rows = list(csv.DictReader(fh, delimiter=";"))
with RUNTIME.open("r", encoding="utf-8-sig", newline="") as fh:
    runtime_rows = list(csv.DictReader(fh))

if len(source_rows) != len(runtime_rows):
    raise SystemExit(f"RUNTIME_CATALOG_V102: row count mismatch source={len(source_rows)} runtime={len(runtime_rows)}")

errors = []
referenced = set()
for index, (source, runtime) in enumerate(zip(source_rows, runtime_rows), start=1):
    source_article = clean(source.get("Артикул"))
    runtime_article = clean(runtime.get("Артикул"))
    if source_article != runtime_article:
        errors.append(f"row {index}: article {source_article!r} != {runtime_article!r}")
    for source_field, runtime_field in zip(SOURCE_PHOTOS, RUNTIME_PHOTOS):
        expected = expected_local(source.get(source_field))
        actual = clean(runtime.get(runtime_field))
        if actual != expected:
            errors.append(f"{source_article} {source_field}: expected {expected!r}, got {actual!r}")
        if actual:
            if not actual.startswith(LOCAL_PREFIX):
                errors.append(f"{source_article} {runtime_field}: non-local path {actual!r}")
                continue
            filename = Path(actual).name
            referenced.add(filename)
            path = IMAGE_DIR / filename
            if not path.is_file() or path.stat().st_size <= 0:
                errors.append(f"{source_article} {runtime_field}: missing file {filename}")

if errors:
    print(f"RUNTIME_CATALOG_V102: {len(errors)} errors")
    for error in errors[:250]:
        print(error)
    raise SystemExit(1)

print(f"// RUNTIME_CATALOG_V102: {len(runtime_rows)} SKU rows verified; all {len(referenced)} runtime photo files match source and exist")
