from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_master.csv"
ASSETS = ROOT / "assets" / "images"

# DIYAF_PRODUCT_IMAGES_V119
IMAGE_MAP = {
    "KD-PD-10459": "KD-PD-10459.png",
    "KD-PD-10591": "KD-PD-10591.png",
    "KD-PD-10946": "KD-PD-10946.png",
    "KD-PD-10947": "KD-PD-10947.png",
    "KD-PD-10948": "KD-PD-10948.png",
    "KD-PD-10949": "KD-PD-10949.png",
    "KD-PD-10950": "KD-PD-10950.png",
    "KD-PD-10951": "KD-PD-10951.png",
}
EXPECTED_COUNTS = {
    "KD-PD-10459": 2,
    "KD-PD-10591": 1,
    "KD-PD-10946": 1,
    "KD-PD-10947": 1,
    "KD-PD-10948": 1,
    "KD-PD-10949": 1,
    "KD-PD-10950": 1,
    "KD-PD-10951": 1,
}

for filename in IMAGE_MAP.values():
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"DIYAF_PRODUCT_IMAGES_V119: missing asset {filename}")

text = CATALOG.read_text(encoding="utf-8")
if not text:
    raise SystemExit("DIYAF_PRODUCT_IMAGES_V119: catalog_master.csv is empty")

# Records can contain line breaks inside text fields. Every catalog record itself starts
# with an article at the beginning of a physical line, so split only at those boundaries.
chunks = re.split(r"(?=^KD-PD-)", text, flags=re.MULTILINE)
if len(chunks) < 2:
    raise SystemExit("DIYAF_PRODUCT_IMAGES_V119: no product records found")

header_chunk = chunks[0]
header_line = header_chunk.rstrip("\r\n")
header = header_line.split(";")
required_columns = ["Артикул", "Коллекция", "Фото 1", "Фото 2", "Фото 3"]
missing_columns = [name for name in required_columns if name not in header]
if missing_columns:
    raise SystemExit("DIYAF_PRODUCT_IMAGES_V119: missing columns " + ", ".join(missing_columns))

idx = {name: header.index(name) for name in required_columns}
counts = {article: 0 for article in EXPECTED_COUNTS}
out = [header_chunk]

for chunk in chunks[1:]:
    if chunk.endswith("\r\n"):
        ending = "\r\n"
        raw = chunk[:-2]
    elif chunk.endswith("\n"):
        ending = "\n"
        raw = chunk[:-1]
    else:
        ending = ""
        raw = chunk

    parts = raw.split(";")
    if len(parts) != len(header):
        out.append(chunk)
        continue

    article = parts[idx["Артикул"]]
    collection = parts[idx["Коллекция"]]
    filename = IMAGE_MAP.get(article)
    if collection != "Дияф" or not filename:
        out.append(chunk)
        continue

    parts[idx["Фото 1"]] = f"/assets/images/{filename}"
    parts[idx["Фото 2"]] = "null"
    parts[idx["Фото 3"]] = "null"
    counts[article] += 1
    out.append(";".join(parts) + ending)

if counts != EXPECTED_COUNTS:
    raise SystemExit(
        f"DIYAF_PRODUCT_IMAGES_V119: unexpected updated rows {counts}; expected {EXPECTED_COUNTS}"
    )

CATALOG.write_text("".join(out), encoding="utf-8")
print(
    "DIYAF_PRODUCT_IMAGES_V119: replaced Diyaf product photos with uploaded assets; "
    f"updated_rows={sum(counts.values())}; assets={len(IMAGE_MAP)}; old secondary photos cleared"
)
