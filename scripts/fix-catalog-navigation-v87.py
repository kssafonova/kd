from pathlib import Path

PAGE = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
MARKER = "// DYNAMIC_CATALOG_NAV_V87"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: source fragment not found")
    return text.replace(old, new, 1)


text = PAGE.read_text(encoding="utf-8")
if MARKER in text:
    print("Catalog navigation v87 already applied")
    raise SystemExit(0)

text = replace_once(
    text,
    'export default function Home() {\n  const [view, setView] = useState<View>("home");',
    'export default function Home({initialView="home",initialCatalogCategory="Все товары"}:{initialView?:View;initialCatalogCategory?:string}={}) {\n  const [view, setView] = useState<View>(initialView);',
    "home initial view",
)
text = replace_once(
    text,
    '  const [catalogCategory,setCatalogCategory]=useState("Все товары");',
    '  const [catalogCategory,setCatalogCategory]=useState(initialCatalogCategory);',
    "initial catalog category",
)
text = replace_once(
    text,
    '  useEffect(()=>{loadXlsxCatalogIntoProducts().finally(()=>setCatalogRevision(value=>value+1))},[]);',
    '  useEffect(()=>{loadXlsxCatalogIntoProducts().finally(()=>setCatalogRevision(value=>value+1))},[]);\n  useEffect(()=>setCatalogCategory(initialCatalogCategory),[initialCatalogCategory]);',
    "sync catalog category prop",
)

old_catalog = '''  const categoryProductIds: Record<string, number[]> = {
    "Все товары": products.map(item=>item.id),
    "Посуда и сервировка": [5,10,2001,2002,2003,2004,2005,2006,2007,1590,1591,1592,1593,1594,1595,1596],
    "Постельное бельё":[2,4,8,11,12],
    "Пледы и подушки":[9,10,11],
    "Декор для дома": [5,7,1499],
    "Домашняя одежда":[6],
    "Свечи и диффузоры":[1499],
    "Для ванной":[6],
    "Столовый текстиль":[7,9],
  };
  const tabs=["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Декор для дома","Свечи и диффузоры","Для ванной","Столовый текстиль"];'''

new_catalog = '''  const catalogText=(product:Product)=>`${product.name} ${product.note}`.toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
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
  const tabs=["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Декор для дома","Домашняя одежда","Свечи и диффузоры","Для ванной","Столовый текстиль"];'''
text = replace_once(text, old_catalog, new_catalog, "dynamic catalog categories")

text = replace_once(
    text,
    '{navCategories.map(item=><button type="button" key={item.title} onClick={()=>openCatalog(item.category)}>{item.title}</button>)}',
    '{navCategories.map(item=><a key={item.title} href={`${readyBase}/catalog/?category=${encodeURIComponent(item.category)}`} onClick={(event)=>{event.preventDefault();openCatalog(item.category)}}>{item.title}</a>)}',
    "catalog top nav links",
)

PAGE.write_text(text, encoding="utf-8")
print("Catalog navigation v87 applied")
