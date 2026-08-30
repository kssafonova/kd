from pathlib import Path
import re

path = Path("app/catalog-data.ts")
text = path.read_text(encoding="utf-8")

# Canonical storefront media after the final product-specific corrections.
# Keep this mapping aligned with the actual media choices used on the site.
IMAGES = {
    ("KD-PD-1023", "Белый"): ("/kd/assets/images/KD-PD-1023-WHITE02.png", ["/kd/assets/images/KD-PD-1023-WHITE02.png"]),
    ("KD-PD-1023", "Молочный"): ("/kd/assets/images/KD-PD-1023-BEIGE01.png", ["/kd/assets/images/KD-PD-1023-BEIGE02.png"]),
    ("KD-PD-1023", "Синий"): ("/kd/assets/images/KD-PD-1023-BLUE02.png", ["/kd/assets/images/KD-PD-1023-BLUE02.png"]),
    ("KD-PD-1026", "Белый"): ("/kd/assets/images/KD-PD-1026-WHITE01.png", ["/kd/assets/images/KD-PD-1026-WHITE02.png"]),
    ("KD-PD-1026", "Молочный"): ("/kd/assets/images/KD-PD-1026-BEIGE01.png", ["/kd/assets/images/KD-PD-1026-BEIGE02.png"]),
    ("KD-PD-1026", "Синий"): ("/kd/assets/images/KD-PD-1026-BLUE01.png", ["/kd/assets/images/KD-PD-1026-BLUE02.png"]),
    ("KD-PD-1027", "Молочный"): ("/kd/assets/images/KD-PD-1027-MOL01.png", []),
    ("KD-PD-1027", "Серо-синий"): ("/kd/assets/images/KD-PD-1027-PES01.png", []),
    ("KD-PD-1030", "Ночной синий"): ("/kd/assets/images/time-tea-pair.png", []),
    ("KD-PD-1024", "Ночной синий"): ("/kd/assets/images/KD-PD-1024-DARK01.png", ["/kd/assets/images/KD-PD-1024-DARK02.png"]),
    ("KD-PD-1025", "Ночной синий"): ("https://kssafonova.github.io/kd/assets/images/moon-plate.png", []),
    ("KD-PD-1028", "Пудровый"): ("https://kssafonova.github.io/kd/assets/images/peach-sheet.jpg", ["/kd/assets/images/KD-PD-1028-PUDRA02.png", "/kd/assets/images/KD-PD-1028-PUDRA03.png"]),
    ("KD-PD-1028", "Белый"): ("/kd/assets/images/KD-PD-1028-WHITE01.png", ["/kd/assets/images/KD-PD-1028-WHITE03.png"]),
    ("KD-PD-1028", "Ночной синий"): ("/kd/assets/images/KD-PD-1028-DARK01.png", ["/kd/assets/images/KD-PD-1028-DARK02.png"]),
    ("KD-PD-1128", "Пудровый"): ("/kd/assets/images/KD-PD-1128-PUDRA01.png", ["/kd/assets/images/KD-PD-1128-PUDRA03.png"]),
    ("KD-PD-1128", "Белый"): ("/kd/assets/images/KD-PD-1128-WHITE01.png", ["/kd/assets/images/KD-PD-1128-WHITE02.png", "/kd/assets/images/KD-PD-1128-WHITE03.png"]),
    ("KD-PD-1128", "Ночной синий"): ("/kd/assets/images/KD-PD-1128-DARK01.png", ["/kd/assets/images/KD-PD-1128-DARK03.png"]),
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
print(f"Synced canonical image URLs across {len(seen)} article/color variants; changed {changed} SKU rows")
