from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

retired_ids = ("time", "buyan", "poetry", "firebird")
retired_titles = ("Нити времени", "Тайна острова Буяна")

# Remove retired entities from the Editorial source array. The items are intentionally
# kept out of the storefront while their underlying products remain available.
for editorial_id in retired_ids:
    pattern = rf'^\s*\{{ id:"{re.escape(editorial_id)}"[^\n]*\}},\n'
    text = re.sub(pattern, "", text, flags=re.MULTILINE)

# Remove homepage/promotional slide entries that still advertise a retired capsule.
for title in retired_titles:
    pattern = rf'^\s*\{{[^\n]*title: "{re.escape(title)}"[^\n]*\}},\n'
    text = re.sub(pattern, "", text, flags=re.MULTILINE)

PAGE.write_text(text, encoding="utf-8")
print("Removed retired Editorial capsules/collections and their named promo slides")
