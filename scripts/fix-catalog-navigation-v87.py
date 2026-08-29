from pathlib import Path
import re

PAGE = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
MARKER = "// DYNAMIC_CATALOG_NAV_V87"


def sub_once(text: str, pattern: str, replacement: str, label: str) -> str:
    next_text, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: source fragment not found")
    return next_text


text = PAGE.read_text(encoding="utf-8")
if MARKER in text:
    print("Catalog navigation v87 already applied")
    raise SystemExit(0)

text = sub_once(
    text,
    r'export default function Home\(\) \{',
    'export default function Home({initialView="home",initialCatalogCategory="Все товары"}:{initialView?:View;initialCatalogCategory?:string}={}) {',
    "home props",
)
text = sub_once(
    text,
    r'const \[view, setView\] = useState<View>\("home"\);',
    'const [view, setView] = useState<View>(initialView);',
    "initial view",
)
text = sub_once(
    text,
    r'const \[catalogCategory,setCatalogCategory\]=useState\("Все товары"\);',
    'const [catalogCategory,setCatalogCategory]=useState(initialCatalogCategory);',
    "initial catalog category",
)
text = sub_once(
    text,
    r'(useEffect\(\(\)=>\{loadXlsxCatalogIntoProducts\(\)\.then\(\(\)=>setXlsxCatalogRevision\(value=>value\+1\)\)\},\[\]\);)',
    r'\1\n  useEffect(()=>setCatalogCategory(initialCatalogCategory),[initialCatalogCategory]);',
    "catalog category synchronization",
)

catalog_replacement = '''const catalogText=(product:Product)=>`${product.name} ${product.note}`.toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
  const categoryMatchers:Record<string,RegExp>={
    "Посуда и сервировка":/(тарел|блюд|чаш|круж|бокал|стакан|графин|салатник|сервиз|чайная пара|кофейн|молочник|супниц|прибор)/,
    "Постельное бельё":/(постель|пододеяль|простын|наволоч)/,
    "Пледы и подушки":/(плед|подуш)/,
    "Декор для дома":/(ваза|декор|скульп|панно|подсвеч)/,
    "Домашняя одежда":/(халат|пижам|сороч|домашн.*одежд)/,
    "Свечи и диффузоры":/(свеч|диффуз|аромат)/,
    "Для ванной":/(полотен|ванн)/,
    "Столовый текстиль":/(скатерт|салфет|раннер|плейсмат|дорожк.*стол)/,
  };
  const categoryProductIds:Record<string,number[]>=Object.fromEntries([
    ["Все товары",products.map(item=>item.id)],
    ...Object.entries(categoryMatchers).map(([key,matcher])=>[key,products.filter(item=>matcher.test(catalogText(item))).map(item=>item.id)]),
  ]);
  // DYNAMIC_CATALOG_NAV_V87
  '''
text = sub_once(
    text,
    r'const categoryProductIds:Record<string,number\[]>\s*=\s*\{.*?\};\s*(?=const list\s*=)',
    catalog_replacement,
    "dynamic catalog categories",
)
text = sub_once(
    text,
    r'const openCatalog=\(category="Все товары"\)=>\{setCatalogCategory\(category\);go\("catalog"\)\};',
    'const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog");const base=process.env.NEXT_PUBLIC_BASE_PATH??"";window.history.pushState({},"",`${base}/catalog/?category=${encodeURIComponent(category)}`)};',
    "catalog URL navigation",
)

PAGE.write_text(text, encoding="utf-8")
print("Catalog navigation v87 applied")
