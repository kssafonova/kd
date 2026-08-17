from pathlib import Path

# Global filename replacements are safe because these media files belong to one product only.
media_replacements = {
    "KD-PD-1023-WHITE01.png": "KD-PD-1023-WHITE02.png",
    "KD-PD-1023-BLUE01.png": "KD-PD-1023-BLUE02.png",
}

for filename in ("app/catalog-data.ts", "app/page.tsx"):
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in media_replacements.items():
        text = text.replace(old, new)
    if any(old in text for old in media_replacements):
        raise SystemExit(f"{filename} still references removed KD-PD-1023 media")
    path.write_text(text, encoding="utf-8")

# KD-PD-1027: remove secondary product photos and rename Sand to Grey-blue.
catalog_path = Path("app/catalog-data.ts")
catalog = catalog_path.read_text(encoding="utf-8")

# Ensure the new swatch and SKU code exist without changing the existing Sand mapping
# that may still be used by other products.
if '"Серо-синий":"#738699"' not in catalog:
    catalog = catalog.replace(
        '  "Песочный":"#c9ad88",',
        '  "Песочный":"#c9ad88",\n  "Серо-синий":"#738699",',
        1,
    )
if '"Серо-синий":"GREY-BLUE"' not in catalog:
    catalog = catalog.replace(
        '  "Песочный":"SAND",',
        '  "Песочный":"SAND",\n  "Серо-синий":"GREY-BLUE",',
        1,
    )

start_marker = 'makeProduct(7,"KD-PD-1027"'
start = catalog.find(start_marker)
if start == -1:
    raise SystemExit("KD-PD-1027 product block not found")
next_product = catalog.find("makeProduct(", start + len(start_marker))
if next_product == -1:
    next_product = len(catalog)
block = catalog[start:next_product]

block = block.replace('color:"Песочный"', 'color:"Серо-синий"')
block = block.replace('gallery:["/kd/images/products/KD-PD-1027-MOL02.png"]', 'gallery:[]')
block = block.replace('gallery:["/kd/images/products/KD-PD-1027-PES02.png"]', 'gallery:[]')
block = block.replace('gallery:["https://kssafonova.github.io/kd/images/products/KD-PD-1027-MOL02.png"]', 'gallery:[]')
block = block.replace('gallery:["https://kssafonova.github.io/kd/images/products/KD-PD-1027-PES02.png"]', 'gallery:[]')

if "KD-PD-1027-MOL02.png" in block or "KD-PD-1027-PES02.png" in block:
    raise SystemExit("KD-PD-1027 still references removed secondary media")
if 'color:"Песочный"' in block:
    raise SystemExit("KD-PD-1027 still uses Sand color")
if 'color:"Серо-синий"' not in block:
    raise SystemExit("KD-PD-1027 Grey-blue color was not applied")

catalog = catalog[:start] + block + catalog[next_product:]
catalog_path.write_text(catalog, encoding="utf-8")

print("Updated KD-PD-1023 media and KD-PD-1027 Grey-blue single-image variants")
