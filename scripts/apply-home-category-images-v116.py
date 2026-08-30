from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
ASSETS = ROOT / "assets" / "images"

category_assets = [
    "1spal.png",
    "2stol.png",
    "3stoltekstil.png",
    "4dekor.png",
    "5homeclothes.png",
    "6van.png",
    "7outlet.png",
]
for filename in category_assets:
    if not (ASSETS / filename).is_file():
        raise SystemExit(f"HOME_CATEGORY_DIRECT_IMAGES_V116: missing asset {filename}")

page_text = PAGE.read_text(encoding="utf-8")
page_original = page_text

categories_block = '''  const categories=[
    {title:"Спальня",note:"Постельное бельё",image:"/assets/images/1spal.png",action:()=>openCatalog("Постельное белье")},
    {title:"Посуда и сервировка",note:"Кухня и столовая",image:"/assets/images/2stol.png",action:()=>openCatalog("Посуда и сервировка")},
    {title:"Столовый текстиль",note:"Скатерти, салфетки, дорожки",image:"/assets/images/3stoltekstil.png",action:()=>openCatalog("Столовый текстиль")},
    {title:"Декор",note:"Предметы для дома",image:"/assets/images/4dekor.png",action:()=>openCatalog("Декор для дома")},
    {title:"Текстиль для дома",note:"Пледы и подушки",image:"/assets/images/5homeclothes.png",action:()=>openCatalog("Пледы и подушки")},
    {title:"Ванная",note:"Для ежедневных ритуалов",image:"/assets/images/6van.png",action:()=>openCatalog()},
    {title:"Outlet",note:"Особые предложения",image:"/assets/images/7outlet.png",action:()=>openCatalog()},
  ];
'''

categories_pattern = re.compile(r'  const categories=\[.*?\n  \];\n', re.S)
if not categories_pattern.search(page_text):
    raise SystemExit("HOME_CATEGORY_DIRECT_IMAGES_V116: categories block not found")
page_text = categories_pattern.sub(categories_block, page_text, count=1)

category_rail_pattern = re.compile(r'      <div className="home113-category-rail">\{categories\.map\(item=><button.*?</div>', re.S)
category_rail = '''      <div className="home113-category-rail">{categories.map(item=><button type="button" key={item.title} className="home113-category-card" onClick={item.action}><span className="home113-atlas-card home113-category-image" role="img" aria-label={item.title} style={{backgroundImage:`url("${assetUrl(item.image)}")`,backgroundSize:"cover",backgroundPosition:"center center",backgroundRepeat:"no-repeat"}}/><strong>{item.title}</strong><small>{item.note}</small></button>)}</div>'''
if not category_rail_pattern.search(page_text):
    raise SystemExit("HOME_CATEGORY_DIRECT_IMAGES_V116: category rail markup not found")
page_text = category_rail_pattern.sub(category_rail, page_text, count=1)

for marker in category_assets:
    if marker not in page_text:
        raise SystemExit(f"HOME_CATEGORY_DIRECT_IMAGES_V116: page missing {marker}")
if "style={atlasStyle(item.index)}" in page_text:
    raise SystemExit("HOME_CATEGORY_DIRECT_IMAGES_V116: stale category atlas style remains")

PAGE.write_text(page_text, encoding="utf-8")

print(
    "// HOME_CATEGORY_DIRECT_IMAGES_V116: 7 direct category PNGs enabled; "
    "1spal + 2stol + 3stoltekstil + 4dekor + 5homeclothes + 6van + 7outlet; "
    f"page_changed={page_text != page_original}"
)
