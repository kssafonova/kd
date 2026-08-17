from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

old = 'const currentProducts=currentScene?.productIds.map(itemById).filter((item):item is Product=>Boolean(item))??[];'
new = 'const currentProducts=(currentScene?.productIds.map(itemById).filter(Boolean)??[]) as Product[];'

if old in text:
    text = text.replace(old, new, 1)
elif new not in text:
    raise SystemExit("Luna currentProducts typecheck marker not found")

path.write_text(text, encoding="utf-8")
print("Fixed Luna editorial TypeScript narrowing")
