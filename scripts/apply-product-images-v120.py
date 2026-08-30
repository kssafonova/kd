from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_master.csv"
ASSETS = ROOT / "assets" / "images"

# PRODUCT_IMAGES_V120
DIRECT_IMAGE_MAP = {
    "KD-PD-2519": "KD-PD-2519.png",
    "KD-PD-10254": "KD-PD-10254.png",
    "KD-PD-10256": "KD-PD-10256.png",
    "KD-PD-10911": "KD-PD-10911.png",
    "KD-PD-10915": "KD-PD-10915.png",
    "KD-PD-10917": "KD-PD-10917.png",
    "KD-PD-10918": "KD-PD-10918.png",
    "KD-PD-10919": "KD-PD-10919.png",
    "KD-PD-10922": "KD-PD-10922.png",
    "KD-PD-10924": "KD-PD-10924.png",
    "KD-PD-10926": "KD-PD-10926.png",
    "KD-PD-10927": "KD-PD-10927.png",
    "KD-PD-10928": "KD-PD-10928.png",
}

COLOR_IMAGE_MAP = {
    ("KD-PD-1027", "молочный"): "KD-PD-1027МОЛОЧНЫИ\u0306.png",
    ("KD-PD-1027", "серо-синий"): "KD-PD-1027СЕРОСИНИИ\u0306.png",
    ("KD-PD-10786", "голубой"): "KD-PD-10786ГОЛУБОИ\u0306.png",
    ("KD-PD-10786", "экрю"): "KD-PD-10786ЭКРЮ.png",
    ("KD-PD-10841", "бежевый"): "KD-PD-10841БЕЖЕВЫИ\u0306.png",
    ("KD-PD-10841", "голубой"): "KD-PD-10841ГОЛУБОИ\u0306.png",
    ("KD-PD-10841", "экрю"): "KD-PD-10841ЭКРЮ.png",
}

# All 21 screenshots supplied by the user are kept in canonical assets. The beige
# KD-PD-10786 image is intentionally not linked: that color has no catalog row today.
ALL_ASSETS = {
    "KD-PD-1027МОЛОЧНЫИ\u0306.png",
    "KD-PD-1027СЕРОСИНИИ\u0306.png",
    "KD-PD-2519.png",
    "KD-PD-10254.png",
    "KD-PD-10256.png",
    "KD-PD-10786БЕЖЕВЫИ\u0306.png",
    "KD-PD-10786ГОЛУБОИ\u0306.png",
    "KD-PD-10786ЭКРЮ.png",
    "KD-PD-10841БЕЖЕВЫИ\u0306.png",
    "KD-PD-10841ГОЛУБОИ\u0306.png",
    "KD-PD-10841ЭКРЮ.png",
    "KD-PD-10911.png",
    "KD-PD-10915.png",
    "KD-PD-10917.png",
    "KD-PD-10918.png",
    "KD-PD-10919.png",
    "KD-PD-10922.png",
    "KD-PD-10924.png",
    "KD-PD-10926.png",
    "KD-PD-10927.png",
    "KD-PD-10928.png",
}

EXPECTED_DIRECT_COUNTS = {
    "KD-PD-2519": 2,
    "KD-PD-10254": 1,
    "KD-PD-10256": 1,
    "KD-PD-10911": 2,
    "KD-PD-10915": 1,
    "KD-PD-10917": 1,
    "KD-PD-10918": 1,
    "KD-PD-10919": 1,
    "KD-PD-10922": 1,
    "KD-PD-10924": 1,
    "KD-PD-10926": 1,
    "KD-PD-10927": 1,
    "KD-PD-10928": 1,
}
EXPECTED_COLOR_COUNTS = {
    ("KD-PD-1027", "молочный"): 2,
    ("KD-PD-1027", "серо-синий"): 2,
    ("KD-PD-10786", "голубой"): 1,
    ("KD-PD-10786", "экрю"): 1,
    ("KD-PD-10841", "бежевый"): 1,
    ("KD-PD-10841", "голубой"): 1,
    ("KD-PD-10841", "экрю"): 1,
}

for filename in ALL_ASSETS:
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"PRODUCT_IMAGES_V120: missing asset {filename}")

text = CATALOG.read_text(encoding="utf-8")
if not text:
    raise SystemExit("PRODUCT_IMAGES_V120: catalog_master.csv is empty")

# Records can contain line breaks inside text fields. Every catalog record itself starts
# with an article at the beginning of a physical line, so split only at those boundaries.
chunks = re.split(r"(?=^KD-PD-)", text, flags=re.MULTILINE)
if len(chunks) < 2:
    raise SystemExit("PRODUCT_IMAGES_V120: no product records found")

header_chunk = chunks[0]
header_line = header_chunk.rstrip("\r\n")
header = header_line.split(";")
required_columns = ["Артикул", "Цвет", "Фото 1", "Фото 2", "Фото 3"]
missing_columns = [name for name in required_columns if name not in header]
if missing_columns:
    raise SystemExit("PRODUCT_IMAGES_V120: missing columns " + ", ".join(missing_columns))

idx = {name: header.index(name) for name in required_columns}
direct_counts = {article: 0 for article in EXPECTED_DIRECT_COUNTS}
color_counts = {key: 0 for key in EXPECTED_COLOR_COUNTS}
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

    article = parts[idx["Артикул"]].strip()
    color = parts[idx["Цвет"]].strip().casefold()

    filename = DIRECT_IMAGE_MAP.get(article)
    if filename:
        direct_counts[article] += 1
    else:
        key = (article, color)
        filename = COLOR_IMAGE_MAP.get(key)
        if filename:
            color_counts[key] += 1

    if not filename:
        out.append(chunk)
        continue

    parts[idx["Фото 1"]] = f"/assets/images/{filename}"
    parts[idx["Фото 2"]] = "null"
    parts[idx["Фото 3"]] = "null"
    out.append(";".join(parts) + ending)

if direct_counts != EXPECTED_DIRECT_COUNTS:
    raise SystemExit(
        f"PRODUCT_IMAGES_V120: unexpected direct rows {direct_counts}; expected {EXPECTED_DIRECT_COUNTS}"
    )
if color_counts != EXPECTED_COLOR_COUNTS:
    raise SystemExit(
        f"PRODUCT_IMAGES_V120: unexpected color rows {color_counts}; expected {EXPECTED_COLOR_COUNTS}"
    )

CATALOG.write_text("".join(out), encoding="utf-8")
updated_rows = sum(direct_counts.values()) + sum(color_counts.values())
print(
    "PRODUCT_IMAGES_V120: replaced product photos with uploaded assets; "
    f"updated_rows={updated_rows}; linked_assets=20; staged_assets={len(ALL_ASSETS)}; "
    "old secondary photos cleared"
)
