from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_master.csv"
ASSETS = ROOT / "assets" / "images"

# SPRING_PRODUCT_IMAGES_V118
IMAGE_MAP = {
    ("KD-PD-8982", "Белый"): "KD-PD-8982WHITE.png",
    ("KD-PD-8982", "Зеленый"): "KD-PD-8982GREEN.png",
    ("KD-PD-8984", None): "KD-PD-8984.png",
    ("KD-PD-8985", None): "KD-PD-8985.png",
    ("KD-PD-9415", None): "KD-PD-9415.png",
    ("KD-PD-9416", None): "KD-PD-9416.png",
    ("KD-PD-9417", None): "KD-PD-9417.png",
    ("KD-PD-9418", None): "KD-PD-9418.png",
}
EXPECTED_COUNTS = {
    ("KD-PD-8982", "Белый"): 2,
    ("KD-PD-8982", "Зеленый"): 2,
    ("KD-PD-8984", None): 1,
    ("KD-PD-8985", None): 2,
    ("KD-PD-9415", None): 1,
    ("KD-PD-9416", None): 1,
    ("KD-PD-9417", None): 1,
    ("KD-PD-9418", None): 1,
}

for filename in IMAGE_MAP.values():
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"SPRING_PRODUCT_IMAGES_V118: missing asset {filename}")

text = CATALOG.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
if not lines:
    raise SystemExit("SPRING_PRODUCT_IMAGES_V118: catalog_master.csv is empty")

header = lines[0].rstrip("\r\n").split(";")
required_columns = ["Артикул", "Цвет", "Коллекция", "Фото 1", "Фото 2", "Фото 3"]
missing_columns = [name for name in required_columns if name not in header]
if missing_columns:
    raise SystemExit("SPRING_PRODUCT_IMAGES_V118: missing columns " + ", ".join(missing_columns))

idx = {name: header.index(name) for name in required_columns}
counts = {key: 0 for key in EXPECTED_COUNTS}
out = [lines[0]]

for line in lines[1:]:
    ending = "\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
    raw = line[:-len(ending)] if ending else line
    parts = raw.split(";")
    if len(parts) != len(header):
        out.append(line)
        continue

    article = parts[idx["Артикул"]]
    color = parts[idx["Цвет"]]
    collection = parts[idx["Коллекция"]]
    if collection != "Весна":
        out.append(line)
        continue

    key = (article, color) if (article, color) in IMAGE_MAP else (article, None)
    filename = IMAGE_MAP.get(key)
    if not filename:
        out.append(line)
        continue

    parts[idx["Фото 1"]] = f"/assets/images/{filename}"
    parts[idx["Фото 2"]] = "null"
    parts[idx["Фото 3"]] = "null"
    counts[key] += 1
    out.append(";".join(parts) + ending)

if counts != EXPECTED_COUNTS:
    raise SystemExit(f"SPRING_PRODUCT_IMAGES_V118: unexpected updated rows {counts}; expected {EXPECTED_COUNTS}")

updated = "".join(out)
CATALOG.write_text(updated, encoding="utf-8")

print(
    "SPRING_PRODUCT_IMAGES_V118: replaced Spring collection product photos with uploaded assets; "
    f"updated_rows={sum(counts.values())}; assets={len(set(IMAGE_MAP.values()))}; old secondary photos cleared"
)
