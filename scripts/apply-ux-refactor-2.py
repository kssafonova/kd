from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()
changes = 0

def rep(old: str, new: str, count: int = 1, required: bool = True):
    global text, changes
    if old in text:
        text = text.replace(old, new, count)
        changes += 1
    elif required:
        raise SystemExit(f"Required marker not found: {old[:140]}")

# Filter model.
rep('type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };', 'type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };\ntype CatalogFilters = { saleOnly:boolean; bedding:boolean; tableware:boolean; textile:boolean };')
rep('  const [filters, setFilters] = useState(false);', '  const [filters, setFilters] = useState(false);\n  const [catalogFilters,setCatalogFilters]=useState<CatalogFilters>({saleOnly:false,bedding:false,tableware:false,textile:false});\n  const [boutiquesOpen,setBoutiquesOpen]=useState(false);')

# Body lock and Escape handling.
rep('document.body.style.overflow = menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen ? "hidden" : "";', 'document.body.style.overflow = menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen || boutiquesOpen ? "hidden" : "";')
rep('}, [menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen]);', '}, [menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen, boutiquesOpen]);')
escape_marker = '  useEffect(()=>{localStorage.setItem("kultura-viewed",JSON.stringify(recentlyViewed))},[recentlyViewed]);\n'
escape_code = '''  useEffect(()=>{localStorage.setItem("kultura-viewed",JSON.stringify(recentlyViewed))},[recentlyViewed]);
  useEffect(()=>{
    const handleEscape=(event:KeyboardEvent)=>{
      if(event.key!=="Escape") return;
      if(checkoutOpen)setCheckoutOpen(false);
      else if(cartOpen)setCartOpen(false);
      else if(plpAdded)setPlpAdded(null);
      else if(plpSize)setPlpSize(null);
      else if(sizeSheet)setSizeSheet(false);
      else if(boutiquesOpen)setBoutiquesOpen(false);
      else if(filters)setFilters(false);
      else if(favoritesOpen)setFavoritesOpen(false);
      else if(account)setAccount(false);
      else if(search)setSearch(false);
      else if(menu)setMenu(false);
    };
    window.addEventListener("keydown",handleEscape);
    return()=>window.removeEventListener("keydown",handleEscape);
  },[checkoutOpen,cartOpen,plpAdded,plpSize,sizeSheet,boutiquesOpen,filters,favoritesOpen,account,search,menu]);
'''
rep(escape_marker, escape_code)

# Root wiring.
rep('<Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />', '<Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} onBoutiques={()=>setBoutiquesOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />')
rep('{view === "catalog" && <CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />}', '{view === "catalog" && <CatalogView initialCategory={catalogCategory} filters={catalogFilters} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />}')
rep('<Footer go={go} notice={notice} />', '<Footer go={go} notice={notice} onBoutiques={()=>setBoutiquesOpen(true)} />')
rep('{menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} />}', '{menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} onBoutiques={()=>{setMenu(false);setBoutiquesOpen(true)}} />}')
rep('{filters && <Filters close={() => setFilters(false)} apply={() => { setFilters(false); notice("Фильтры применены"); }} />}', '{filters && <Filters value={catalogFilters} close={() => setFilters(false)} apply={(next)=>{setCatalogFilters(next);setFilters(false);notice("Фильтры применены")}} reset={()=>{setCatalogFilters({saleOnly:false,bedding:false,tableware:false,textile:false});setFilters(false);notice("Фильтры сброшены")}} />}')
rep('{toast && <div className="toast">{toast}</div>}', '{boutiquesOpen&&<BoutiqueMap close={()=>setBoutiquesOpen(false)}/>}\n      {toast && <div className="toast" role="status" aria-live="polite">{toast}</div>}')

# Header boutiques becomes a real action.
rep('function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {', 'function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, onBoutiques, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; onBoutiques:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {')
rep('<button className="boutiques" onClick={() => alert("Бутики: Москва · Санкт-Петербург · Казань")}><Icon name="pin"/> Бутики</button>', '<button className="boutiques" onClick={onBoutiques}><Icon name="pin"/> Бутики</button>')

# Hero destinations match the visible merchandising category.
hero_marker = '  const featuredProducts = slideProductIds[slide].map(id=>products.find(product=>product.id===id)!).filter(Boolean);\n'
hero_code = '''  const featuredProducts = slideProductIds[slide].map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const openCurrent=()=>{
    if(current.destination==="collections") { go("collections"); return; }
    if(current.category==="СПАЛЬНЯ") openCatalog("Постельное бельё");
    else if(current.category==="КУХНЯ И СТОЛОВАЯ") openCatalog("Посуда и сервировка");
    else if(current.category==="ДЕКОР ДЛЯ ДОМА") openCatalog("Пледы и подушки");
    else openCatalog("Все товары");
  };
'''
rep(hero_marker, hero_code)
rep('onClick={() => go(current.destination)}', 'onClick={openCurrent}', count=2)

# Functional catalog filters.
rep('function CatalogView({ initialCategory, onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {', 'function CatalogView({ initialCategory, filters, onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; filters:CatalogFilters; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {')
rep('  const list = products.filter(product=>(categoryProductIds[category]??[]).includes(product.id)).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);', '''  const categoryList=products.filter(product=>(categoryProductIds[category]??[]).includes(product.id));
  const typeIds=new Set<number>([
    ...(filters.bedding?[1,2,4,8,12]:[]),
    ...(filters.tableware?[5,9,10]:[]),
    ...(filters.textile?[3,6,7,11]:[]),
  ]);
  const hasTypeFilter=filters.bedding||filters.tableware||filters.textile;
  const list=categoryList.filter(product=>(!filters.saleOnly||Boolean(product.oldPrice))&&(!hasTypeFilter||typeIds.has(product.id))).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);''')
rep('<div className="catalog-tools"><select value={sort} onChange={e=>setSort(e.target.value)}>', '<div className="catalog-tools"><select aria-label="Сортировка товаров" value={sort} onChange={e=>setSort(e.target.value)}>')
rep('<button key={x} className={category===x?"active":""} onClick={()=>setCategory(x)}>{x}</button>', '<button key={x} className={category===x?"active":""} aria-pressed={category===x} onClick={()=>setCategory(x)}>{x}</button>')

# Product card semantics.
rep('<button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label="Добавить в избранное">', '<button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-pressed={liked} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}>')
rep('<button className="product-image" onClick={()=>onClick(chosenProduct)}>', '<button className="product-image" onClick={()=>onClick(chosenProduct)} aria-label={`Открыть ${product.name}`}>')
rep('onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`}', 'onClick={()=>setColorIndex(i)} aria-pressed={i===colorIndex} aria-label={`Выбрать цвет ${variant.name}`}')

# Collection tabs semantics.
rep('<button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>', '<button key={x} className={kind===x?"active":""} aria-pressed={kind===x} onClick={()=>setKind(x)}>{x}</button>')

# Menu boutiques is actionable.
rep('function Menu({ current, setCurrent, close, go, openCatalog }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void }) {', 'function Menu({ current, setCurrent, close, go, openCatalog, onBoutiques }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void; onBoutiques:()=>void }) {')
rep('<span><Icon name="pin"/> Бутики</span>', '<button className="menu-boutiques" onClick={onBoutiques}><Icon name="pin"/> Бутики</button>')

# Replace fake filter facets with actual supported filters.
start = text.find('function Filters(')
end = text.find('\n\nfunction PLPSizeFlow', start)
if start < 0 or end < 0:
    raise SystemExit('Filters function boundaries not found')
new_filters = '''function Filters({ value, close, apply, reset }: { value:CatalogFilters; close:()=>void; apply:(value:CatalogFilters)=>void; reset:()=>void }) {
  const [draft,setDraft]=useState<CatalogFilters>(value);
  const toggle=(key:keyof CatalogFilters)=>setDraft(current=>({...current,[key]:!current[key]}));
  return <div className="overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть фильтры"/><aside className="side-panel filters" role="dialog" aria-modal="true" aria-label="Фильтры каталога"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ФИЛЬТРЫ</p><details open><summary>Категория<Icon name="plus"/></summary><label><input type="checkbox" checked={draft.bedding} onChange={()=>toggle("bedding")}/> Постельное бельё</label><label><input type="checkbox" checked={draft.tableware} onChange={()=>toggle("tableware")}/> Посуда и сервировка</label><label><input type="checkbox" checked={draft.textile} onChange={()=>toggle("textile")}/> Пледы, подушки и декор</label></details><details open><summary>Предложения<Icon name="plus"/></summary><label><input type="checkbox" checked={draft.saleOnly} onChange={()=>toggle("saleOnly")}/> Только товары со скидкой</label></details><button className="primary" onClick={()=>apply(draft)}>ПРИМЕНИТЬ ФИЛЬТРЫ</button><button className="link" onClick={()=>{setDraft({saleOnly:false,bedding:false,tableware:false,textile:false});reset()}}>СБРОСИТЬ</button></aside></div>;
}'''
text = text[:start] + new_filters + text[end:]
changes += 1

# Share has visible feedback/fallback instead of silently copying.
share_marker = '  const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize(selectedProduct):add(selectedProduct);\n'
share_code = '''  const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize(selectedProduct):add(selectedProduct);
  const shareProduct=async()=>{
    try{
      if(navigator.share) await navigator.share({title:product.name,url:location.href});
      else { await navigator.clipboard?.writeText(location.href); alert("Ссылка на товар скопирована"); }
    }catch{}
  };
'''
rep(share_marker, share_code)
rep('<button onClick={()=>navigator.clipboard?.writeText(location.href)} aria-label="Поделиться">', '<button onClick={shareProduct} aria-label="Поделиться товаром">')

# Footer boutiques uses the shared map.
rep('function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) {', 'function Footer({ go, notice, onBoutiques }: { go:(v:View)=>void; notice:(s:string)=>void; onBoutiques:()=>void }) {')
rep('<button onClick={()=>alert("Москва · Санкт-Петербург · Казань")}>Бутики</button>', '<button onClick={onBoutiques}>Бутики</button>')

required = [
    'CatalogFilters',
    'catalogFilters',
    'typeIds=new Set<number>',
    'menu-boutiques',
    'aria-pressed={liked}',
    'shareProduct',
    'boutiquesOpen&&<BoutiqueMap',
    'Только товары со скидкой',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'Missing marker after interaction refactor: {marker}')

path.write_text(text)
print(f"Interaction refactor applied: {changes} targeted changes")
