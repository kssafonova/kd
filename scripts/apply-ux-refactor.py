from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()
changes = 0

def rep(old: str, new: str, required: bool = True):
    global text, changes
    if old in text:
        text = text.replace(old, new, 1)
        changes += 1
    elif required:
        raise SystemExit(f"Required marker not found: {old[:120]}")

# Shared product sizing, category relation and cart merge helpers.
marker = 'const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;\n'
helpers = '''const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

const BEDDING_PRODUCT_IDS = [1,2,4,8,12];
const CATEGORY_GROUPS = [[1,2,4,8,12],[3,6,7,11],[5,9,10]];
const sizeOptionsFor = (product: Product): readonly (readonly [string, number])[] => {
  const basePrice = products.find(item=>item.id===product.id)?.price ?? product.price;
  return BEDDING_PRODUCT_IDS.includes(product.id)
    ? [["Евро 200×220",basePrice],["Семейный 150×200",basePrice+2000],["Кинг Сайз 220×240",basePrice+2000]] as const
    : [["Один размер",basePrice]] as const;
};
const unavailableSizesFor = (product: Product) => BEDDING_PRODUCT_IDS.includes(product.id) ? ["Кинг Сайз 220×240"] : [];
const categoryIdsFor = (product: Product) => CATEGORY_GROUPS.find(group=>group.includes(product.id)) ?? products.map(item=>item.id);
const mergeCartItem = (current: CartItem[], incoming: CartItem) => {
  const index = current.findIndex(item=>item.id===incoming.id && item.selectedSize===incoming.selectedSize && item.selectedColor===incoming.selectedColor);
  if(index<0) return [...current,incoming];
  return current.map((item,itemIndex)=>itemIndex===index?{...item,quantity:item.quantity+incoming.quantity,price:incoming.price,image:incoming.image}:item);
};
const mergeCartItems = (current: CartItem[], incoming: CartItem[]) => incoming.reduce<CartItem[]>((result,item)=>mergeCartItem(result,item),current);
'''
rep(marker, helpers)

# Cart operations: merge identical SKU variants instead of duplicating lines.
rep('setCart((current) => [...current, item]);', 'setCart((current) => mergeCartItem(current,item));')
rep('setCart((current)=>[...current,item]); setPlpSize(null); setPlpAdded(item);', 'setCart((current)=>mergeCartItem(current,item)); setPlpSize(null); setPlpAdded(item);')
rep('const bundleItems: CartItem[] = items.map((product)=>({ ...product, selectedSize: product.selectedSize ?? "Евро 200×220", selectedColor: product.selectedColor ?? product.colorVariants?.[0]?.name ?? "Молочный", quantity: product.quantity ?? 1 }));\n    setCart((current)=>[...current,...bundleItems]); setCartOpen(true);', 'const bundleItems: CartItem[] = items.map((product)=>({ ...product, selectedSize: product.selectedSize ?? sizeOptionsFor(product)[0][0], selectedColor: product.selectedColor ?? product.colorVariants?.[0]?.name ?? "Молочный", quantity: product.quantity ?? 1 }));\n    setCart((current)=>mergeCartItems(current,bundleItems)); setCartOpen(true);')

# Root navigation consistency: every product open goes through openProduct, every quick add opens one sizing flow.
rep('{view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}', '{view === "home" && <HomeView go={go} openCatalog={openCatalog} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}')
rep('{view === "editorial" && <EditorialView editorial={editorial} buyBundle={addBundle} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}', '{view === "editorial" && <EditorialView editorial={editorial} buyBundle={addBundle} selectProduct={openProduct} quickAdd={setPlpSize} favorite={favorite} favorites={favorites} />}')
rep('{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} buyBundle={addBundle} selectProduct={openProduct} recentlyViewed={recentlyViewed} />}', '{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={(p)=>setPlpSize(p)} add={(p) => add(p,p.selectedSize,p.quantity)} buyBundle={addBundle} selectProduct={openProduct} quickAdd={setPlpSize} recentlyViewed={recentlyViewed} />}')
rep('{search && <Search close={() => setSearch(false)} choose={(p) => { setSelected(p); setSearch(false); go("product"); }} />}', '{search && <Search close={() => setSearch(false)} choose={(p) => { setSearch(false); openProduct(p); }} />}')
rep('{favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setSelected(product);setFavoritesOpen(false);go("product")}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}', '{favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setFavoritesOpen(false);openProduct(product)}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}')
rep('{cartOpen && <Cart cart={cart} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} />}', '{cartOpen && <Cart cart={cart} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} quickAdd={(product)=>{setCartOpen(false);setPlpSize(product)}} />}')

# Home categories navigate to the correct catalog tab.
rep('function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void }) {', 'function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void }) {')
rep('{categories.map(([name,image], i)=><button className={`category-card c${i}`} key={name} onClick={() => i===2 ? go("collections") : go("catalog")}>', '{categories.map(([name,image], i)=><button className={`category-card c${i}`} key={name} onClick={() => name==="Капсулы и коллекции" ? go("collections") : openCatalog(name==="Спальня"?"Постельное бельё":name==="Кухня и столовая"?"Посуда и сервировка":name==="Домашний текстиль"?"Пледы и подушки":"Все товары")}>')

# Catalog labels/counts reflect actual demo data rather than a hard-coded production count.
rep('return <div className="catalog page"><div className="crumbs">Главная / Каталог / Домашний текстиль</div><div className="title-line"><h1>Домашний текстиль</h1><span>345 товаров</span></div>', 'const catalogTitle=category==="Все товары"?"Каталог":category;\n  return <div className="catalog page"><div className="crumbs">Главная / Каталог{category!=="Все товары"?` / ${category}`:""}</div><div className="title-line"><h1>{catalogTitle}</h1><span>{list.length} {list.length===1?"товар":list.length>=2&&list.length<=4?"товара":"товаров"}</span></div>')

# Editorial quick add should add, not navigate.
rep('function EditorialView({ editorial, buyBundle, selectProduct, favorite, favorites }: { editorial:Editorial; buyBundle:(items:Product[])=>void; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {', 'function EditorialView({ editorial, buyBundle, selectProduct, quickAdd, favorite, favorites }: { editorial:Editorial; buyBundle:(items:Product[])=>void; selectProduct:(product:Product)=>void; quickAdd:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {')
# This replacement is intentionally global after both Editorial and ProductRecommendations receive quickAdd.

# Product size rows: only explicitly unavailable sizes are disabled.
rep('function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void}){', 'function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableSizes=[]}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableSizes?:readonly string[]}){')
rep('const unavailable=index===sizes.length-1;', 'const unavailable=unavailableSizes.includes(name);')

# PDP uses product-specific sizes, related bundle products and current configuration on mobile.
rep('function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; buyBundle:(items:Product[])=>void; selectProduct:(p:Product)=>void; recentlyViewed:number[] }) {', 'function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct, quickAdd, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:(product:Product)=>void; add:(p:Product)=>void; buyBundle:(items:Product[])=>void; selectProduct:(p:Product)=>void; quickAdd:(p:Product)=>void; recentlyViewed:number[] }) {')
rep('const [selectedSize,setSelectedSize]=useState("Евро 200×220");', 'const [selectedSize,setSelectedSize]=useState(sizeOptionsFor(product)[0][0]);')
rep('setColorIndex(initial>=0?initial:0);setActiveImage(0);setSelectedSize("Евро 200×220");setQuantity(1)', 'setColorIndex(initial>=0?initial:0);setActiveImage(0);setSelectedSize(sizeOptionsFor(product)[0][0]);setQuantity(1)')
rep('const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;', 'const sizes=sizeOptionsFor(product);')
rep('const bundleExtras=products.filter(item=>item.id!==product.id).slice(0,2);', 'const bundleExtras=products.filter(item=>item.id!==product.id&&categoryIdsFor(product).includes(item.id)).slice(0,2);')
rep('const [bundleSelectedIds,setBundleSelectedIds]=useState<number[]>(bundleItems.map(item=>item.id));', 'const [bundleSelectedIds,setBundleSelectedIds]=useState<number[]>(bundleItems.map(item=>item.id));\n  const [bundleSizes,setBundleSizes]=useState<Record<number,string>>({});\n  const [bundleQuantities,setBundleQuantities]=useState<Record<number,number>>({});')
rep('useEffect(()=>{setBundleSelecting(false);setBundleSelectedIds(bundleItems.map(item=>item.id))},[product.id]);\n  const selectedBundleItems=bundleItems.filter(item=>bundleSelectedIds.includes(item.id));', 'useEffect(()=>{setBundleSelecting(false);setBundleSelectedIds(bundleItems.map(item=>item.id));setBundleSizes({});setBundleQuantities({})},[product.id]);\n  const configuredBundleItems=bundleItems.map((item,index)=>{const bundleSize=index===0?selectedSize:(bundleSizes[item.id]??sizeOptionsFor(item)[0][0]);const bundleQuantity=index===0?quantity:(bundleQuantities[item.id]??1);const bundlePrice=sizeOptionsFor(item).find(([name])=>name===bundleSize)?.[1]??item.price;return {...item,selectedSize:bundleSize,quantity:bundleQuantity,price:bundlePrice}});\n  const selectedBundleItems=configuredBundleItems.filter(item=>bundleSelectedIds.includes(item.id));')
rep('const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize():add(selectedProduct);', 'const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize(selectedProduct):add(selectedProduct);')
rep('<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>', '<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)} unavailableSizes={unavailableSizesFor(product)}/>')
rep('{bundleItems.map((item,index)=><article className={bundleSelectedIds.includes(item.id)?"selected":""} key={`${item.id}-${index}`}><div><img src={assetUrl(item.image)} alt={item.name}/>{bundleSelecting?<label className="product-selector compact"><input type="checkbox" checked={bundleSelectedIds.includes(item.id)} onChange={()=>toggleBundleItem(item.id)}/><span><Icon name="plus"/></span></label>:<i>✓</i>}</div><span>{item.name}</span><small>{index===0?`${selectedSize} · ${color.name}`:item.note}</small><b>{fmt(item.price*(item.quantity??1))}</b></article>)}', '{configuredBundleItems.map((item,index)=><article className={bundleSelectedIds.includes(item.id)?"selected":""} key={`${item.id}-${index}`}><div><img src={assetUrl(item.image)} alt={item.name}/>{bundleSelecting?<label className="product-selector compact"><input type="checkbox" checked={bundleSelectedIds.includes(item.id)} onChange={()=>toggleBundleItem(item.id)}/><span><Icon name="plus"/></span></label>:<i>✓</i>}</div><span>{item.name}</span><small>{index===0?`${selectedSize} · ${color.name}`:`${item.selectedSize} · ${item.note}`}</small>{bundleSelecting&&index>0&&<div className="bundle-config"><select value={item.selectedSize} onChange={event=>setBundleSizes(current=>({...current,[item.id]:event.target.value}))}>{sizeOptionsFor(item).map(([name])=><option key={name}>{name}</option>)}</select><QuantityControl quantity={item.quantity??1} setQuantity={next=>setBundleQuantities(current=>({...current,[item.id]:next}))}/></div>}<b>{fmt(item.price*(item.quantity??1))}</b></article>)}')
rep('"ВЫКУПИТЬ ВЕСЬ КОМПЛЕКТ"', '"ДОБАВИТЬ ВЕСЬ КОМПЛЕКТ"')

# Product recommendations use the same quick-add flow as PLP.
rep('<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>', '<ProductRecommendations product={product} selectProduct={selectProduct} quickAdd={quickAdd} favorite={favorite} recentlyViewed={recentlyViewed}/>')
rep('function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){', 'function ProductRecommendations({product,selectProduct,quickAdd,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;quickAdd:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){')
text = text.replace('onQuick={selectProduct}', 'onQuick={quickAdd}')

# PLP sizing: product-specific sizes, explicit OOS, shared boutique map.
rep('const [infoOpen,setInfoOpen]=useState(false);\n  const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;', 'const [infoOpen,setInfoOpen]=useState(false);\n  const [storesOpen,setStoresOpen]=useState(false);\n  const sizes=sizeOptionsFor(product);')
rep('const [chosenSize,setChosenSize]=useState("Евро 200×220");', 'const [chosenSize,setChosenSize]=useState(sizeOptionsFor(product)[0][0]);')
rep('<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/>', '<ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)} unavailableSizes={unavailableSizesFor(product)}/>')
rep('<button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>', '<button className="stores" onClick={()=>setStoresOpen(true)}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>} {storesOpen&&<BoutiqueMap close={()=>setStoresOpen(false)}/>}</div>')

# Filters should not reload the entire storefront or claim a fake result count.
rep('<button className="primary" onClick={apply}>ПОКАЗАТЬ 24 ТОВАРА</button><button className="link" onClick={()=>location.reload()}>СБРОСИТЬ</button>', '<button className="primary" onClick={apply}>ПРИМЕНИТЬ ФИЛЬТРЫ</button><button className="link" onClick={close}>СБРОСИТЬ</button>')

# Cart: correct per-product sizes, actionable recommendations and quick add.
rep('function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {\n  const sizeOptions=["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];', 'function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {')
rep('<label>Размер<select value={p.selectedSize} onChange={event=>update(i,{selectedSize:event.target.value})}>{sizeOptions.map(option=><option key={option}>{option}</option>)}</select></label>', '<label>Размер<select value={p.selectedSize} onChange={event=>{const nextSize=event.target.value;const nextPrice=sizeOptionsFor(p).find(([name])=>name===nextSize)?.[1]??p.price;update(i,{selectedSize:nextSize,price:nextPrice})}}>{sizeOptionsFor(p).map(([option])=><option key={option}>{option}</option>)}</select></label>')
rep('<div>{recentlyViewed.map(product=><button key={product.id} onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/><strong>{product.name}</strong><small>{product.note}</small><b>{fmt(product.price)}</b></button>)}</div>', '<div>{recentlyViewed.map(product=><article className="recent-cart-card" key={product.id}><button className="recent-product-link" onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/><strong>{product.name}</strong><small>{product.note}</small><b>{fmt(product.price)}</b></button><button className="recent-quick" onClick={()=>quickAdd(product)} aria-label={`Добавить ${product.name} в корзину`}><Icon name="cart-add"/></button></article>)}</div>')
rep('<p className="recommend-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</p><div className="cart-recs">{products.slice(2,4).map(p=><article key={p.id}><img src={assetUrl(p.image)} alt=""/><span>{p.name}</span><b>{fmt(p.price)}</b></article>)}</div>', '<p className="recommend-title">ДОПОЛНИТЕ ЗАКАЗ</p><div className="cart-recs">{products.filter(product=>!cart.some(item=>item.id===product.id)).slice(0,2).map(p=><article key={p.id}><button className="cart-rec-link" onClick={()=>choose(p)}><img src={assetUrl(p.image)} alt={p.name}/><span>{p.name}</span><b>{fmt(p.price)}</b></button><button className="cart-rec-add" onClick={()=>quickAdd(p)} aria-label={`Добавить ${p.name} в корзину`}><Icon name="cart-add"/></button></article>)}</div>')

# Checkout consent is opt-in; pickup points stay coherent with the displayed Moscow map.
rep('const [agreed,setAgreed]=useState(true);', 'const [agreed,setAgreed]=useState(false);')
rep('const points=delivery==="pickup"?["Петровка, 12","Кутузовский проспект, 48","Большая Конюшенная, 12"]:["Петровка, 12","Арбат, 20","Большая Ордынка, 31"];', 'const points=delivery==="pickup"?["Петровка, 12","Кутузовский проспект, 48","Большая Ордынка, 31"]:["Петровка, 12","Арбат, 20","Большая Ордынка, 31"];')

# Copy consistency.
text = text.replace('ВЫКУПИТЬ ВСЮ ', 'ДОБАВИТЬ ВСЮ ')
text = text.replace('>ДОБАВИТЬ</button>', '>ДОБАВИТЬ В КОРЗИНУ</button>')

# Sanity markers.
required_markers = [
  'sizeOptionsFor(product)',
  'mergeCartItem(current,item)',
  'quickAdd={setPlpSize}',
  'ДОПОЛНИТЕ ЗАКАЗ',
  'bundle-config',
  'useState(false);',
  'Товары из этой категории',
  'Вы недавно смотрели',
]
for marker in required_markers:
    if marker not in text:
        raise SystemExit(f"Missing marker after UX refactor: {marker}")

path.write_text(text)
print(f"UX refactor applied: {changes} targeted replacements")
