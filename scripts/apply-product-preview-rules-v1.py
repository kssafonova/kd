from pathlib import Path
import re

page_path = Path("app/page.tsx")
page = page_path.read_text(encoding="utf-8")

required = [
    '"KD-PD-1028":"Белый"',
    '"KD-PD-1128":"Белый"',
    '"KD-PD-1023":{color:"Синий",image:"/kd/images/products/KD-PD-1023-BLUE02.png"}',
    '"KD-PD-1026":{color:"Синий",image:"/kd/images/products/KD-PD-1026-BLUE01.png"}',
]
missing = [value for value in required if value not in page]
if missing:
    raise SystemExit("Required product preview rules are missing: " + ", ".join(missing))

catalog_path = Path("app/catalog-data.ts")
catalog = catalog_path.read_text(encoding="utf-8")
match = re.search(r'makeProduct\(3,"KD-PD-1023","Подушка с кружевом".*?\n  \]\),', catalog, flags=re.S)
if not match:
    raise SystemExit("KD-PD-1023 catalog block not found")

block = match.group(0)
block = block.replace("KD-PD-1023-WHITE01.png", "KD-PD-1023-WHITE02.png")
block = block.replace("KD-PD-1023-BLUE01.png", "KD-PD-1023-BLUE02.png")
if "KD-PD-1023-WHITE01.png" in block or "KD-PD-1023-BLUE01.png" in block:
    raise SystemExit("KD-PD-1023 still references WHITE01 or BLUE01")

catalog = catalog[:match.start()] + block + catalog[match.end():]
catalog_path.write_text(catalog, encoding="utf-8")
print("Removed WHITE01 and BLUE01 from KD-PD-1023 media")
