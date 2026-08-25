from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")
original = text

# Route every storefront entry point (menu + home Ready Solutions block)
# to the new standalone progressive-form experience.
text = text.replace(
    'const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;',
    'const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;'
)

# Keep terminology aligned with the current standalone Collections section.
text = text.replace('<span>КАПСУЛЫ И КОЛЛЕКЦИИ</span>', '<span>КОЛЛЕКЦИИ</span>')

if text != original:
    page_path.write_text(text, encoding="utf-8")
    print("V55: storefront menu and home now point to /ready-solutions/")
else:
    print("V55: ready-solutions links already current")
