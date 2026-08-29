from __future__ import annotations

from pathlib import Path
import csv
import posixpath
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_xlsx_full.csv"
IMAGE_DIR = ROOT / "public" / "images" / "imported-products"
PHOTO_FIELDS = [
    "Превью фотография товара",
    "Вторая фотография товара в скролле",
    "Третья фотография в стролле",
]
MARKER = "// IMPORTED_PRODUCT_IMAGES_V90"


def image_basename(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme else value
    return posixpath.basename(path.rstrip("/"))


def main() -> None:
    if not CATALOG.exists():
        raise SystemExit(f"Missing generated catalog: {CATALOG}")
    if not IMAGE_DIR.exists():
        raise SystemExit(f"Missing image directory: {IMAGE_DIR}")

    with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        fields = reader.fieldnames or []

    missing_columns = [field for field in PHOTO_FIELDS if field not in fields]
    if missing_columns:
        raise SystemExit("Missing photo columns: " + ", ".join(missing_columns))

    referenced: set[str] = set()
    missing_files: set[str] = set()
    for row in rows:
        for field in PHOTO_FIELDS:
            filename = image_basename(row.get(field, ""))
            if not filename:
                row[field] = ""
                continue
            referenced.add(filename)
            row[field] = f"/images/imported-products/{filename}"
            if not (IMAGE_DIR / filename).is_file():
                missing_files.add(filename)

    if missing_files:
        sample = ", ".join(sorted(missing_files)[:20])
        suffix = "" if len(missing_files) <= 20 else f" … +{len(missing_files)-20} more"
        raise SystemExit(f"{len(missing_files)} table image files are missing from public/images/imported-products: {sample}{suffix}")

    with CATALOG.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"{MARKER}: {len(rows)} SKU rows, {len(referenced)} unique table image filenames -> /images/imported-products/")


if __name__ == "__main__":
    main()
