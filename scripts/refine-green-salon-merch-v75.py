from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
builder_path = root / "app" / "constructor" / "table-solution-builder.ts"
marker = "// READY_SOLUTIONS_MERCH_V75"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise RuntimeError(f"{label}: anchor not found")
    return text.replace(old, new, 1)


# 1) Remove Niti and Phoenix from the public Collections index/editorial routes.
page = page_path.read_text(encoding="utf-8")
if marker not in page:
    page, niti_count = re.subn(r'^\s*\{ id:"niti"[^\n]*\},\n', '', page, count=1, flags=re.M)
    page, phoenix_count = re.subn(r'^\s*\{ id:"phoenix"[^\n]*\},\n', '', page, count=1, flags=re.M)
    if niti_count != 1 or phoenix_count != 1:
        raise RuntimeError(f"collections removal failed: niti={niti_count}, phoenix={phoenix_count}")
    page = replace_once(page, 'type Editorial = {', marker + '\ntype Editorial = {', 'page marker')
    page_path.write_text(page, encoding="utf-8")


# 2) Green Salon: Rosy is a default collection; atmosphere becomes a Decor subcategory.
ready = ready_path.read_text(encoding="utf-8")
if marker not in ready:
    ready = replace_once(
        ready,
        '  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна"],',
        '  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна", "Росы"],',
        'Green Salon base collections',
    )

    # Phoenix is no longer exposed as an addable Ready Solutions collection.
    ready = ready.replace(
        '  "Зимняя сказка": ["Жар-птица", "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],',
        '  "Зимняя сказка": ["Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],',
        1,
    )
    ready = ready.replace(
        '  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России", "Жар-птица"],',
        '  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России"],',
        1,
    )

    ready = replace_once(
        ready,
        '  "Петербург", "Многоцвет", "Весна",\n] as const;',
        '  "Петербург", "Многоцвет", "Весна", "Росы",\n] as const;',
        'Rosy source hint',
    )

    ready = replace_once(
        ready,
        '  if (name.includes("придан")) return "Приданое";\n  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";',
        '  if (name.includes("придан")) return "Приданое";\n  if (name.includes("росы")) return "Росы";\n  // The eligible feed names this SKU “Весенний сад”; merchandise the requested teapot inside the live “Весна” Green Salon collection.\n  if (name.includes("чайник заварочный весенний сад")) return "Весна";\n  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";',
        'collection inference',
    )

    ready = replace_once(
        ready,
        '  decor:{title:"Декор для дома",categories:["throwsCoverlets","decorativePillows","vases","baskets","games","storage","other"]},\n  atmosphere:{title:"Свечи и диффузоры",categories:["atmosphere"]},',
        '  decor:{title:"Декор для дома",categories:["throwsCoverlets","decorativePillows","vases","baskets","games","storage","atmosphere","other"]},\n  atmosphere:{title:"Свечи и диффузоры",categories:["atmosphere"]},',
        'Decor atmosphere subcategory',
    )
    ready = replace_once(
        ready,
        'const GROUP_ORDER: GroupId[] = ["tableware","tableTextile","bedding","decor","atmosphere","bath"];',
        'const GROUP_ORDER: GroupId[] = ["tableware","tableTextile","bedding","decor","bath"];',
        'group order',
    )

    ready = replace_once(ready, 'const CART_KEY = "kultura-cart";', marker + '\nconst CART_KEY = "kultura-cart";', 'ready marker')
    ready_path.write_text(ready, encoding="utf-8")


# 3) Product taxonomy used by Ready Solutions.
builder = builder_path.read_text(encoding="utf-8")
if marker not in builder:
    builder = replace_once(
        builder,
        '  tableTextile: {\n    title: "Скатерти, плейсматы и тканевые салфетки",\n    description: "Скатерти, дорожки, плейсматы и тканевые салфетки собраны вместе — выбирайте нужные элементы сервировки.",\n  },',
        '  tableTextile: {\n    title: "Скатерти, плейсматы, салфетки и конверты",\n    description: "Скатерти, дорожки, плейсматы, тканевые салфетки и конверты для приборов собраны вместе — выбирайте нужные элементы сервировки.",\n  },',
        'table textile title',
    )

    builder = replace_once(
        builder,
        '  if (hasAny(name, ["скатерт", "плейсмат", "салфет", "дорожк", "раннер"]) || hasAny(type, ["tablecloth", "placemat", "napkin", "table_runner"])) {',
        '  if (hasAny(name, ["скатерт", "плейсмат", "салфет", "дорожк", "раннер", "конверт для столовых приборов"]) || hasAny(type, ["tablecloth", "placemat", "napkin", "table_runner"])) {',
        'table textile classification',
    )

    builder = replace_once(
        builder,
        '  if (name.includes("ваза") || type.includes("vase")) return { id: "vases", perPerson: false };',
        '  if (name.includes("ваза для фруктов")) return { id: "serving", perPerson: false };\n\n  if (name.includes("ваза") || type.includes("vase")) return { id: "vases", perPerson: false };',
        'fruit vase classification',
    )

    builder = replace_once(builder, 'import type { CatalogRow, ConstructorData } from "./types";', 'import type { CatalogRow, ConstructorData } from "./types";\n\n' + marker, 'builder marker')
    builder_path.write_text(builder, encoding="utf-8")

print("Ready Solutions V75 merchandising rules applied")
