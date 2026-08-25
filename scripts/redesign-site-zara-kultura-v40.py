from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

marker = "SITE_ZARA_KULTURA_V40"

old_main = '<main className={`view-${view}`}>'
new_main = '<main className={`view-${view} site-zara-kultura-v40`}>'
if new_main not in page:
    if old_main not in page:
        raise SystemExit("V40 root main anchor not found")
    page = page.replace(old_main, new_main, 1)

old_solutions = '''  const solutions=[
    {room:"ГОСТИНАЯ",title:"Тихая гостиная",image:"/images/beige-bedroom.png"},
    {room:"СПАЛЬНЯ",title:"Синий бархат ночи",image:"/images/blue-bedroom.png"},
    {room:"КАБИНЕТ",title:"Кабинетное ретро",image:"/images/time-collection.png"},
    {room:"КУХНЯ",title:"Утро в зимнем саду",image:"/images/buyan-editorial.png"},
  ];'''
new_solutions = '''  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/images/constructor/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/images/constructor/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/images/products/KD-PD-2000-WHITE01.png",href:`${constructorHref}table-7/`},
  ];'''
if new_solutions not in page:
    if old_solutions not in page:
        raise SystemExit("V40 home solutions anchor not found")
    page = page.replace(old_solutions, new_solutions, 1)

old_cards = '<div id="home-solution-rail" className="hv4-solution-rail">{solutions.map(item=><a className="hv4-solution-card" href={constructorHref} key={item.room}><img src={assetUrl(item.image)} alt={`${item.room}: ${item.title}`}/><span><small>{item.room}</small><strong>{item.title}</strong><em>СМОТРЕТЬ</em></span></a>)}</div>'
new_cards = '<div id="home-solution-rail" className="hv4-solution-rail">{solutions.map(item=><a className="hv4-solution-card" href={item.href} key={item.title}><img src={assetUrl(item.image)} alt={`${item.room}: ${item.title}`}/><span><small>{item.room}</small><strong>{item.title}</strong><em>СОБРАТЬ РЕШЕНИЕ</em></span></a>)}</div>'
if new_cards not in page:
    if old_cards not in page:
        raise SystemExit("V40 home solution cards anchor not found")
    page = page.replace(old_cards, new_cards, 1)

if marker not in page:
    page = page.replace('// CATALOG_SKU_MODEL_V1', '// CATALOG_SKU_MODEL_V1\n// ' + marker, 1)

page_path.write_text(page, encoding="utf-8")
print("Site Zara Kultura V40 migration applied")
