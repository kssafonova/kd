from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

old = '''  const categoryProductIds:Record<string,number[]>={
    "Все товары":products.map(product=>product.id),
    "Посуда и сервировка":[5,9,10,3,1],
    "Постельное бельё":[1,2,4,6,8,12],
    "Пледы и подушки":[3,4,6,7,11],
    "Домашняя одежда":[2,3,6,8],
    "Столовый текстиль":[1,3,5],
  };
  const list = products.filter(product=>(categoryProductIds[category]??[]).includes(product.id)).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);
  return <div className="catalog page"><div className="crumbs">Главная / Каталог / Домашний текстиль</div><div className="title-line"><h1>Домашний текстиль</h1><span>345 товаров</span></div>'''

new = '''  const categoryProductIds:Record<string,number[]>={
    "Все товары":products.map(product=>product.id),
    "Посуда и сервировка":[5,10],
    "Постельное бельё":[2,4,8,11,12],
    "Пледы и подушки":[3,6,7],
    "Домашняя одежда":[],
    "Столовый текстиль":[],
  };
  const list = products.filter(product=>(categoryProductIds[category]??[]).includes(product.id)).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);
  return <div className="catalog page"><div className="crumbs">Главная / Каталог / {category}</div><div className="title-line"><h1>{category}</h1><span>{list.length} {list.length===1?"товар":list.length>=2&&list.length<=4?"товара":"товаров"}</span></div>'''

if old in text:
    text = text.replace(old, new)
elif new not in text:
    raise SystemExit("Catalog category block not found; mapping was not changed")

empty_old = '''    <div className="product-grid">{list.map(p=><ProductCard key={`${category}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div>
'''
empty_new = '''    {list.length?<div className="product-grid">{list.map(p=><ProductCard key={`${category}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div>:<div className="catalog-empty"><p>В этой категории пока нет товаров</p></div>}
'''
if empty_old in text:
    text = text.replace(empty_old, empty_new)
elif empty_new not in text:
    raise SystemExit("Catalog product grid block not found")

path.write_text(text, encoding="utf-8")

css_path = Path("app/globals.css")
css = css_path.read_text(encoding="utf-8")
marker = "/* CATALOG_CATEGORY_MAPPING_V1 */"
if marker not in css:
    css += '''\n\n/* CATALOG_CATEGORY_MAPPING_V1 */\n.catalog-empty{min-height:280px;display:grid;place-items:center;border-top:1px solid var(--line);color:var(--muted);text-align:center}\n.catalog-empty p{margin:0;font-size:12px;letter-spacing:.05em}\n/* END_CATALOG_CATEGORY_MAPPING_V1 */\n'''
    css_path.write_text(css, encoding="utf-8")

print("Applied strict catalog category mapping")
