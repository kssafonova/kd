from pathlib import Path

replacements = {
    "KD-PD-1023-WHITE01.png": "KD-PD-1023-WHITE02.png",
    "KD-PD-1023-BLUE01.png": "KD-PD-1023-BLUE02.png",
}

for filename in ("app/catalog-data.ts", "app/page.tsx"):
    path = Path(filename)
    text = path.read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    if any(old in text for old in replacements):
        raise SystemExit(f"{filename} still references removed KD-PD-1023 media")
    path.write_text(text, encoding="utf-8")

print("Removed KD-PD-1023 WHITE01 and BLUE01 from storefront media")
