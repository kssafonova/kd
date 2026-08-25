from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")
old = '.filter(word=>word.length>4&&!/[^(]/.test(word)).filter(word=>!["комплект","декоративная","постельного","культура","товара"].includes(word))'
new = '.filter(word=>word.length>4&&/^[а-яёa-z0-9]+$/i.test(word)).filter(word=>!["комплект","декоративная","постельного","культура","товара"].includes(word))'
if old in page:
    page = page.replace(old,new,1)
elif new not in page:
    raise SystemExit("V42 cross-sell matcher anchor not found")
page_path.write_text(page,encoding="utf-8")
print("Refined V42 cross-sell matcher")
