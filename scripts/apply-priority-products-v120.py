from pathlib import Path
import csv
import io
import re

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "public" / "data" / "catalog_master.csv"
PRIORITY = ROOT / "scripts" / "catalog-priority" / "dop1-20260830.csv"
ASSETS = ROOT / "assets" / "images"

if not MASTER.is_file():
    raise SystemExit("CATALOG_PRIORITY_V120: catalog_master.csv is missing")
if not PRIORITY.is_file():
    raise SystemExit("CATALOG_PRIORITY_V120: priority product file is missing")

master_text = MASTER.read_text(encoding="utf-8")
header_line = master_text.splitlines()[0] if master_text else ""
headers = header_line.split(";")
if not headers or headers[0] != "Артикул":
    raise SystemExit("CATALOG_PRIORITY_V120: unexpected catalog header")

with PRIORITY.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    if (reader.fieldnames or []) != headers:
        raise SystemExit(
            "CATALOG_PRIORITY_V120: priority file headers do not match catalog_master.csv"
        )
    priority_rows = list(reader)

if not priority_rows:
    raise SystemExit("CATALOG_PRIORITY_V120: priority product file is empty")

articles = [str(row.get("Артикул") or "").strip() for row in priority_rows]
if any(not article for article in articles):
    raise SystemExit("CATALOG_PRIORITY_V120: blank article in priority product file")
priority_articles = set(articles)

for row in priority_rows:
    for column in ("Фото 1", "Фото 2", "Фото 3"):
        value = str(row.get(column) or "").strip()
        if not value or value.lower() == "null":
            continue
        if not value.startswith("/assets/images/"):
            raise SystemExit(
                f"CATALOG_PRIORITY_V120: {column} must use /assets/images/: {value}"
            )
        filename = value.removeprefix("/assets/images/")
        if not (ASSETS / filename).is_file():
            raise SystemExit(f"CATALOG_PRIORITY_V120: missing asset {filename}")

# Preserve all non-priority catalog records byte-for-byte, including records with
# embedded line breaks. Every catalog record begins with an article at line start.
chunks = re.split(r"(?=^KD-PD-)", master_text, flags=re.MULTILINE)
if len(chunks) < 2:
    raise SystemExit("CATALOG_PRIORITY_V120: no product records found")

header_chunk = chunks[0]
kept = []
removed = 0
for chunk in chunks[1:]:
    article = chunk.split(";", 1)[0].strip()
    if article in priority_articles:
        removed += 1
        continue
    kept.append(chunk)

buffer = io.StringIO()
writer = csv.DictWriter(
    buffer,
    fieldnames=headers,
    delimiter=";",
    lineterminator="\n",
    extrasaction="ignore",
)
for row in priority_rows:
    writer.writerow({name: str(row.get(name) or "").strip() for name in headers})
priority_text = buffer.getvalue()

MASTER.write_text(header_chunk + priority_text + "".join(kept), encoding="utf-8")
print(
    "// CATALOG_PRIORITY_V120: "
    f"priority_rows={len(priority_rows)}; priority_articles={len(priority_articles)}; "
    f"replaced_existing_rows={removed}; pinned_to_catalog_top=true"
)
