from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "public" / "images" / "imported-products"
SOURCE = IMAGE_DIR / "6a43757d69bf8_big.jpg"
TARGET = IMAGE_DIR / "6a43757dac52e_big.jpg"

if not TARGET.exists():
    if not SOURCE.exists():
        raise SystemExit(f"Missing same-product source image: {SOURCE}")
    shutil.copy2(SOURCE, TARGET)
    print(f"Copied same-product image to table filename: {TARGET.name}")
else:
    print(f"Table image already present: {TARGET.name}")
