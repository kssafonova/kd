from pathlib import Path
import re

path = Path("app/catalog-data.ts")
text = path.read_text(encoding="utf-8")

# Source of truth: товары2(1).xlsx uploaded 2026-08-17.
# URLs below are the production URLs from that workbook.
IMAGES = {
    ("KD-PD-1023", "Белый"): ("/kd/images/products/KD-PD-1023-WHITE01.png", ["/kd/images/products/KD-PD-1023-WHITE02.png"]),
    ("KD-PD-1023", "Молочный"): ("/kd/images/products/KD-PD-1023-BEIGE01.png", ["/kd/images/products/KD-PD-1023-BEIGE02.png"]),
    ("KD-PD-1023", "Синий"): ("/kd/images/products/KD-PD-1023-BLUE01.png", ["/kd/images/products/KD-PD-1023-BLUE02.png"]),
    ("KD-PD-1026", "Белый"): ("/kd/images/products/KD-PD-1026-WHITE01.png", ["/kd/images/products/KD-PD-1026-WHITE02.png"]),
    ("KD-PD-1026", "Молочный"): ("/kd/images/products/KD-PD-1026-BIEGE01.png", ["/kd/images/products/KD-PD-1026-BIEGE02.png"]),
    ("KD-PD-1026", "Синий"): ("/kd/images/products/KD-PD-1026-BLUE01.png", ["/kd/images/products/KD-PD-1026-BLUE02.png"]),
    ("KD-PD-1027", "Молочный"): ("/kd/images/products/KD-PD-1027-MOL01.png", ["/kd/images/products/KD-PD-1027-MOL02.png"]),
    ("KD-PD-1027", "Песочный"): ("/kd/images/products/KD-PD-1027-PES01.png", ["/kd/images/products/KD-PD-1027-PES02.png"]),
    ("KD-PD-1030", "Ночной синий"): ("/kd/images/time-tea-pair.png", []),
    ("KD-PD-1024", "Ночной синий"): ("/kd/images/products/KD-PD-1024-DARK01.png", ["/kd/images/products/KD-PD-1024-DARK02.png"]),
    ("KD-PD-1025", "Ночной синий"): ("https://kssafonova.github.io/kd/images/moon-plate.png", []),
    ("KD-PD-1028", "Пудровый"): ("https://kssafonova.github.io/kd/images/peach-sheet.jpg", ["/kd/images/products/KD-PD-1028-PUDRA02.png", "/kd/images/products/KD-PD-1028-PUDRA03.png"]),
    ("KD-PD-1028", "Белый"): ("/kd/images/products/KD-PD-1028-WHITE01.png", ["/kd/images/products/KD-PD-1028-WHITE03.png"]),
    ("KD-PD-1028", "Ночной синий"): ("/kd/images/products/KD-PD-1028-DARK01.png", ["/kd/images/products/KD-PD-1028-DARK02.png"]),
    ("KD-PD-1128", "Пудровый"): ("/kd/images/products/KD-PD-1128-PUDRA01.png", ["/kd/images/products/KD-PD-1128-PUDRA03.png"]),
    ("KD-PD-1128", "Белый"): ("/kd/images/products/KD-PD-1128-WHITE01.png", ["/kd/images/products/KD-PD-1128-WHITE02.png", "/kd/images/products/KD-PD-1128-WHITE03.png"]),
    ("KD-PD-1128", "Ночной синий"): ("/kd/images/products/KD-PD-1128-DARK01.png", ["/kd/images/products/KD-PD-1128-DARK02.png"]),
}

product_pattern = re.compile(
    r'(makeProduct\(\d+,"(?P<article>KD-PD-\d+)".*?,\[\n)(?P<body>.*?)(\n\s*\]\),)',
    re.S,
)

changed = 0
seen = set()

def patch_product(match: re.Match[str]) -> str:
    global changed
    article = match.group("article")
    body = match.group("body")
    lines = body.splitlines()
    patched = []
    for line in lines:
        color_match = re.search(r'color:"([^"]+)"', line)
        if not color_match:
            patched.append(line)
            continue
        color = color_match.group(1)
        key = (article, color)
        media = IMAGES.get(key)
        if not media:
            patched.append(line)
            continue
        image, gallery = media
        gallery_code = "[" + ",".join(f'"{item}"' for item in gallery) + "]"
        new_line = re.sub(r'image:"[^"]*"', f'image:"{image}"', line, count=1)
        new_line = re.sub(r'gallery:\[[^\]]*\]', f'gallery:{gallery_code}', new_line, count=1)
        if new_line != line:
            changed += 1
        seen.add(key)
        patched.append(new_line)
    return match.group(1) + "\n".join(patched) + match.group(4)

text = product_pattern.sub(patch_product, text)
missing = sorted(set(IMAGES) - seen)
if missing:
    raise SystemExit(f"Image mappings not found in catalog: {missing}")

path.write_text(text, encoding="utf-8")
print(f"Synced updated workbook image URLs across {len(seen)} article/color variants; changed {changed} SKU rows")
