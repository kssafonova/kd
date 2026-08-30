from pathlib import Path

root = Path(__file__).resolve().parents[1]
app = root / "app"
storefront = app / "storefront-app.tsx"
text = storefront.read_text(encoding="utf-8")

# Runtime-safe project base path: build env first, GitHub Pages path as fallback.
count_marker = 'const productCountLabel=(count:number)=>`${count} ${count===1?"товар":count>=2&&count<=4?"товара":"товаров"}`;\n'
if 'const runtimeStorefrontBase=' not in text and count_marker in text:
    text = text.replace(
        count_marker,
        count_marker + '''const runtimeStorefrontBase=()=>{\n  const configured=(process.env.NEXT_PUBLIC_BASE_PATH??"").replace(/\\/$/,"");\n  if(configured)return configured;\n  if(typeof window==="undefined")return "";\n  const path=window.location.pathname;\n  if(path==="/kd"||path.startsWith("/kd/"))return "/kd";\n  if(window.location.hostname.endsWith("github.io")){const first=path.split("/").filter(Boolean)[0];return first?`/${first}`:""}\n  return "";\n};\n''',
        1,
    )

old_loader = '''async function loadCatalogMasterIntoProducts(){
  if(catalogMasterLoaded)return;
  catalogMasterLoaded=true;
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);
  const sourceRows=databaseRows;
  const rows=sourceRows.map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as CatalogMasterRow).filter(row=>row["Артикул"]&&row["Название товара"]);
  if(!rows.length)return;
'''
new_loader = '''async function loadCatalogMasterIntoProducts(){
  if(catalogMasterLoaded&&products.length)return;
  const base=runtimeStorefrontBase();
  let databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);
  if(!databaseRows.length&&typeof window!=="undefined"){
    try{
      const directUrl=new URL(`${base}/data/catalog_master.csv`,window.location.origin).toString();
      const response=await fetch(directUrl,{cache:"force-cache"});
      if(response.ok)databaseRows=parseEntityCsv(await response.text());
    }catch{}
  }
  const sourceRows=databaseRows;
  const rows=sourceRows.map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as CatalogMasterRow).filter(row=>row["Артикул"]&&row["Название товара"]);
  if(!rows.length){catalogMasterLoaded=false;return;}
  catalogMasterLoaded=true;
'''
if old_loader in text:
    text = text.replace(old_loader, new_loader, 1)
else:
    # Handle already partially modified variants from previous migrations.
    text = text.replace('  if(catalogMasterLoaded)return;\n  catalogMasterLoaded=true;\n  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";\n  const databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);\n  const sourceRows=databaseRows;\n', new_loader.split('async function loadCatalogMasterIntoProducts(){\n',1)[1].split('  const rows=',1)[0], 1)
    text = text.replace('  if(!rows.length)return;\n', '  if(!rows.length){catalogMasterLoaded=false;return;}\n  catalogMasterLoaded=true;\n', 1)

# Do not expose a false empty catalog before the CSV has loaded.
old_boot = '''  const [,setCatalogMasterRevision]=useState(0);
  useEffect(()=>{loadCatalogMasterIntoProducts().then(()=>setCatalogMasterRevision(value=>value+1))},[]);
'''
new_boot = '''  const [catalogDataReady,setCatalogDataReady]=useState(()=>catalogMasterLoaded&&products.length>0);
  const [catalogDataError,setCatalogDataError]=useState(false);
  const reloadCatalogData=()=>{catalogMasterLoaded=false;setCatalogDataReady(false);setCatalogDataError(false);void loadCatalogMasterIntoProducts().then(()=>{const ready=products.length>0;setCatalogDataReady(ready);setCatalogDataError(!ready)})};
  useEffect(()=>{let mounted=true;void loadCatalogMasterIntoProducts().then(()=>{if(!mounted)return;const ready=products.length>0;setCatalogDataReady(ready);setCatalogDataError(!ready)});return()=>{mounted=false}},[]);
'''
text = text.replace(old_boot, new_boot, 1)

# Deep-link actions from the standalone homepage to catalog drawers.
slide_marker = '  const [slide, setSlide] = useState(0);\n'
if 'params.get("cart")==="open"' not in text and slide_marker in text:
    text = text.replace(
        slide_marker,
        slide_marker + '''  useEffect(()=>{\n    if(typeof window==="undefined")return;\n    const params=new URLSearchParams(window.location.search);\n    if(params.get("cart")==="open")setCartOpen(true);\n    if(params.get("search")==="open")setSearch(true);\n    if(params.get("account")==="open")setAccount(true);\n    if(params.get("favorites")==="open")setFavoritesOpen(true);\n  },[]);\n''',
        1,
    )

old_go = '  const go = (next: View) => { if(next==="home"){const base=process.env.NEXT_PUBLIC_BASE_PATH??"";window.location.href=`${base}/`;return;} setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };\n  const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog");const base=process.env.NEXT_PUBLIC_BASE_PATH??"";window.history.pushState({},"",`${base}/catalog/?category=${encodeURIComponent(category)}`)};'
new_go = '  const go = (next: View) => { if(next==="home"){window.location.href=`${runtimeStorefrontBase()}/`;return;} setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };\n  const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog");window.history.pushState({},"",`${runtimeStorefrontBase()}/catalog/?category=${encodeURIComponent(category)}`)};'
text = text.replace(old_go, new_go, 1)

# Replace catalog render with a real loading state.
old_render = '      {view === "catalog" && <CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />}'
new_render = '      {view === "catalog" && (catalogDataReady?<CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />:<CatalogBootStateV141 error={catalogDataError} retry={reloadCatalogData}/>)}'
text = text.replace(old_render, new_render, 1)

boot_component = '''function CatalogBootStateV141({error,retry}:{error:boolean;retry:()=>void}){\n  return <section className="catalog-boot-v141" aria-live="polite"><p>КАТАЛОГ</p><h1>{error?"Не удалось загрузить каталог":"Загружаем каталог"}</h1>{error?<><p className="catalog-boot-v141-error">Проверьте соединение и попробуйте ещё раз.</p><button type="button" onClick={retry}>Повторить</button></>:<div className="catalog-boot-v141-grid" aria-hidden="true">{Array.from({length:6},(_,index)=><div className="catalog-boot-v141-card" key={index}><span/><i/><b/></div>)}</div>}</section>;\n}\n\n'''
if 'function CatalogBootStateV141' not in text:
    text = text.replace('function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, onBoutiques, count, favoriteCount, go }:', boot_component + 'function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, onBoutiques, count, favoriteCount, go }:', 1)

# Breadcrumbs become real navigation, not dead text.
text = text.replace(
    '<div className="crumbs">Главная / Каталог / {category}</div>',
    '<nav className="crumbs catalog-crumbs-v141" aria-label="Хлебные крошки"><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/`}}>Главная</button><span>/</span><button type="button" onClick={()=>changeCategory("Все товары")}>Каталог</button>{category!=="Все товары"&&<><span>/</span><b>{category}</b></>}</nav>',
    1,
)

# Semantic horizontally-scrollable category slider.
text = text.replace(
    '<div className="tabs">{["Все товары",...categoryNames].map(name=>',
    '<div className="tabs catalog-category-slider-v141" role="tablist" aria-label="Категории каталога">{["Все товары",...categoryNames].map(name=>',
    1,
)
text = text.replace(
    '<button key={name} className={category===name?"active":""} onClick={()=>changeCategory(name)}>{name}</button>',
    '<button key={name} role="tab" aria-selected={category===name} className={category===name?"active":""} onClick={()=>changeCategory(name)}>{name}</button>',
    1,
)

# Keep all Фото 1–3 swipeable in PLP. ProductCardGalleryEnhancer suppresses card open after a drag.
layout = app / "catalog" / "layout.tsx"
layout_text = layout.read_text(encoding="utf-8")
if 'import "../catalog-ux-v141.css";' not in layout_text:
    layout_text = layout_text.replace('import "../cart-checkout-human-eye-v136.css";\n', 'import "../cart-checkout-human-eye-v136.css";\nimport "../catalog-ux-v141.css";\n')
if 'import "../product-card-gallery.css";' not in layout_text:
    layout_text = layout_text.replace('import "../product-media-scroll.css";\n', 'import "../product-media-scroll.css";\nimport "../product-card-gallery.css";\n')
if 'ProductCardGalleryEnhancer' not in layout_text:
    layout_text = layout_text.replace('import { CollectionPurchaseEnhancer }', 'import { ProductCardGalleryEnhancer } from "../product-card-gallery";\nimport { CollectionPurchaseEnhancer }', 1)
    layout_text = layout_text.replace('  return <>\n', '  return <>\n    <ProductCardGalleryEnhancer />\n', 1)
layout.write_text(layout_text, encoding="utf-8")

# Sort/filter labels stay short and readable.
enhancer = app / "catalog-togas-v132-enhancer.tsx"
enhancer_text = enhancer.read_text(encoding="utf-8")
enhancer_text = enhancer_text.replace('if(filterLabel&&filterLabel.textContent!=="Все фильтры")filterLabel.textContent="Все фильтры";', 'if(filterLabel&&filterLabel.textContent!=="Фильтры")filterLabel.textContent="Фильтры";')
enhancer.write_text(enhancer_text, encoding="utf-8")

# Homepage header actions now open the corresponding catalog UI, not just the catalog root.
home = app / "home-standalone.tsx"
home_text = home.read_text(encoding="utf-8")
home_text = home_text.replace('<button onClick={()=>navigate("/catalog/")} aria-label="Поиск"><Icon name="search"/></button>', '<button onClick={()=>navigate("/catalog/?search=open")} aria-label="Поиск"><Icon name="search"/></button>')
home_text = home_text.replace('<button onClick={()=>navigate("/catalog/")} aria-label="Профиль"><Icon name="user"/></button>', '<button onClick={()=>navigate("/catalog/?account=open")} aria-label="Профиль"><Icon name="user"/></button>')
home_text = home_text.replace('<button className="favorite-header" onClick={()=>navigate("/catalog/")} aria-label={`Избранное: ${favoriteCount}`}>', '<button className="favorite-header" onClick={()=>navigate("/catalog/?favorites=open")} aria-label={`Избранное: ${favoriteCount}`}>')
home.write_text(home_text, encoding="utf-8")

storefront.write_text(text, encoding="utf-8")
print("Catalog V141: reliable CSV boot, left title, category slider, adapted toolbar, gallery and route actions applied")
