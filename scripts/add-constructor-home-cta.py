from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

if 'className="home-constructor-entry"' in text:
    print("Constructor homepage CTA already present")
    raise SystemExit(0)

marker = '''    </section>\n\n    <section className="home-reference-shelf">'''
replacement = '''    </section>\n\n    <section className="home-constructor-entry" aria-label="Конструктор сценариев">\n      <a href={`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`}>СОБРАТЬ СЦЕНАРИЙ →</a>\n    </section>\n\n    <section className="home-reference-shelf">'''

if marker not in text:
    raise SystemExit("Homepage hero/shelf marker not found")

text = text.replace(marker, replacement, 1)
path.write_text(text, encoding="utf-8")
print("Added constructor CTA to homepage")
