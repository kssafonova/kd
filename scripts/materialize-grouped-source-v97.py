from pathlib import Path
import csv, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "scripts" / "product-source"
TARGET = SOURCE_DIR / "all_site_products_grouped.csv"
PARTS = [SOURCE_DIR / f"products_part_{i:02d}.csv" for i in range(1, 7)]
EXPECTED_DIGEST = "3ad1aa78cff53734efc1dbf5a24e6f4f30e247ec3572c9c77cb0fb264db30ec9"

headers = None
rows = []
for part in PARTS:
    with part.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        if headers is None:
            headers = reader.fieldnames
        elif reader.fieldnames != headers:
            raise SystemExit(f"Header mismatch in {part.name}")
        rows.extend(reader)

if not headers:
    raise SystemExit("No source headers")

payload = json.dumps({"headers": headers, "rows": [[row.get(h, "") for h in headers] for row in rows]}, ensure_ascii=False, separators=(",", ":"))
digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
if digest != EXPECTED_DIGEST:
    raise SystemExit(f"Grouped source differs from uploaded file: {digest} != {EXPECTED_DIGEST}")

with TARGET.open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=headers, delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

articles = {str(row.get("Артикул") or "").strip() for row in rows if str(row.get("Артикул") or "").strip()}
print(f"// GROUPED_SOURCE_V97: verified uploaded dataset digest; {len(rows)} rows / {len(articles)} articles -> {TARGET.relative_to(ROOT)}")
