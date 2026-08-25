from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "app" / "ready-solutions" / "ready-solutions-client.tsx"
text = path.read_text(encoding="utf-8")
original = text

# next/link already applies next.config basePath. Keep a separate prefix only
# for imperative browser navigation (window.location.href).
text = text.replace(
    'const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";',
    'const basePath = "";\nconst browserBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";'
)
text = text.replace(
    'window.location.href = `${basePath}/?open=cart`;',
    'window.location.href = `${browserBasePath}/?open=cart`;'
)

if text != original:
    path.write_text(text, encoding="utf-8")
    print("V55: fixed double basePath in Ready Solutions links")
else:
    print("V55: Ready Solutions basePath already fixed")
