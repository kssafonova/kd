from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "public" / "data" / "catalog_master.csv"
REMOVE = {"KD-PD-11516", "KD-PD-11442"}

text = CATALOG.read_text(encoding="utf-8")
if not text:
    raise SystemExit("CATALOG_REMOVE_V121: catalog_master.csv is empty")

# Catalog records may contain line breaks inside text fields, but every record starts
# with its article at the beginning of a physical line.
chunks = re.split(r"(?=^KD-PD-)", text, flags=re.MULTILINE)
if len(chunks) < 2:
    raise SystemExit("CATALOG_REMOVE_V121: no product records found")

counts = {article: 0 for article in REMOVE}
out = [chunks[0]]

for chunk in chunks[1:]:
    article = chunk.split(";", 1)[0].strip()
    if article in REMOVE:
        counts[article] += 1
        continue
    out.append(chunk)

CATALOG.write_text("".join(out), encoding="utf-8")
print(
    "CATALOG_REMOVE_V121: removed requested catalog products; "
    f"removed_rows={sum(counts.values())}; articles={','.join(sorted(REMOVE))}"
)
