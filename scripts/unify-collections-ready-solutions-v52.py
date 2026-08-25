from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

# Remove retired editorial collections from the canonical collection list.
for retired_id in ("white-chapter", "home-in-bloom", "velvet-rhythm"):
    text = re.sub(rf"\n\s*\{{ id:\"{re.escape(retired_id)}\"[^\n]*\}},", "", text)

collections_start = text.find("function CollectionsView(")
editorial_start = text.find("function EditorialView(", collections_start)
lookbook_start = text.find("function LookbookViewer(", editorial_start)
if collections_start < 0 or editorial_start < 0 or lookbook_start < 0:
    raise SystemExit("V52: collection component anchors not found")

new_collections = r'''function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle,initialEditorial }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void; initialEditorial?:Editorial }) {
  // COLLECTIONS_UNIFIED_V52
  const [active,setActive]=useState<Editorial|null>(initialEditorial??null);
  const [purchaseMode,setPurchaseMode]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});

  useEffect(()=>{
    if(initialEditorial){
      setActive(initialEditorial);
      setPurchaseMode(false);
      setSelectedIds([]);
      setSizes({});
      setVariants({});
    }
  },[initialEditorial?.id]);

  useEffect(()=>{
    if(!active)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[active]);

  const collectionPrice=(editorial:Editorial)=>{
    const values=editorial.productIds.map(id=>products.find(item=>item.id===id)?.price||0).filter(Boolean);
    return values.length?Math.min(...values):0;
  };
  const items=useMemo(()=>active?active.productIds.map(id=>products.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)):[],[active]);
  const open=(editorial:Editorial)=>{setActive(editorial);setPurchaseMode(false);setSelectedIds([]);setSizes({});setVariants({})};
  const close=()=>{setActive(null);setPurchaseMode(false);setSelectedIds([]);setSizes({});setVariants({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const currentProduct=(item:Product)=>variants[item.id]??item;
  const colorOf=(item:Product)=>{const current=currentProduct(item);return current.selectedColor??current.colorVariants?.[0]?.name??current.skus?.[0]?.color??""};
  const sizeOptions=(item:Product)=>getProductSizeOptions(currentProduct(item),colorOf(item));
  const pending=selectedIds.filter(id=>{
    const item=items.find(product=>product.id===id);
    if(!item)return false;
    return sizeOptions(item).length>1&&!sizes[id];
  });
  const selectedProducts=selectedIds.map(id=>items.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)).map(item=>{
    const current=currentProduct(item);
    const color=colorOf(item);
    const options=sizeOptions(item);
    const selectedSize=sizes[item.id]??(options.length===1?options[0][0]:"");
    const sku=selectedSize?findProductSku(current,color,selectedSize):findProductSku(current,color);
    return {...current,selectedColor:color,selectedSize:selectedSize||sku?.size||"",selectedSkuId:sku?.id,price:sku?.price??current.price};
  });
  const total=selectedProducts.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;
  const startPurchase=()=>{setPurchaseMode(true);setSelectedIds([]);setSizes({})};
  const finishPurchase=()=>{setPurchaseMode(false);setSelectedIds([]);setSizes({})};
  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};

  return <main className="collections-v52">
    <header className="collections-v52-intro">
      <div><small>КУЛЬТУРА ДОМА · EDITORIAL</small><h1>Коллекции</h1></div>
      <p>Истории для дома, собранные вокруг цвета, орнамента и ритуала. Откройте коллекцию как журнал — и выбирайте предметы только тогда, когда они действительно нужны.</p>
    </header>
    <section className="collections-v52-index" aria-label="Коллекции Культура Дома">
      {editorials.map(editorial=><article className="collections-v52-card" key={editorial.id}>
        <button className="collections-v52-card-media" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v52-card-copy"><small>КОЛЛЕКЦИЯ</small><button type="button" onClick={()=>open(editorial)}><h2>{editorial.name}</h2></button><p>{editorial.lead}</p><div><span>{productCountLabel(editorial.productIds.length)}</span><strong>{collectionPrice(editorial)?`от ${fmt(collectionPrice(editorial))}`:""}</strong></div></div>
      </article>)}
    </section>

    {active&&<div className="v52-story-backdrop" role="presentation"><button className="v52-story-dismiss" type="button" onClick={close} aria-label="Закрыть коллекцию"/>
      <section className="v52-story-modal" role="dialog" aria-modal="true" aria-label={`Коллекция ${active.name}`}>
        <header className="v52-story-topbar"><button type="button" onClick={close}>← Коллекции</button><strong>КУЛЬТУРА ДОМА</strong><button type="button" onClick={close} aria-label="Закрыть">×</button></header>
        <div className="v52-story-columns">
          <aside className="v52-story-editorial" aria-label="История коллекции">
            <div className="v52-story-title"><small>КОЛЛЕКЦИЯ</small><h1>{active.name}</h1><p>{active.lead}</p><span>{productCountLabel(items.length)}</span></div>
            {active.images.map((image,index)=><figure key={`${active.id}-${image}`}><img src={assetUrl(image)} alt={`${active.name}, кадр ${index+1}`}/>{index===0&&<figcaption>{active.detail}</figcaption>}</figure>)}
            <div className="v52-story-note"><small>О КОЛЛЕКЦИИ</small><p>{active.description}</p></div>
          </aside>
          <section className="v52-story-commerce" aria-label="Товары коллекции">
            <header className="v52-commerce-head"><div><small>{purchaseMode?"СОБЕРИТЕ СВОЮ ИСТОРИЮ":"ТОВАРЫ КОЛЛЕКЦИИ"}</small><h2>{purchaseMode?"Выберите предметы":"Предметы истории"}</h2><p>{purchaseMode?"Отметьте нужные позиции. Для товаров с несколькими размерами размер можно выбрать после отметки.":"Каждый предмет можно добавить отдельно — привычной кнопкой корзины, как в каталоге."}</p></div>{purchaseMode?<div className="v52-commerce-actions"><button type="button" className="v52-secondary-action" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всё"}</button><button type="button" className="v52-text-action" onClick={finishPurchase}>Отменить</button></div>:<button type="button" className="v52-buy-story" onClick={startPurchase}>КУПИТЬ КОЛЛЕКЦИЮ</button>}</header>
            <div className={`product-grid v52-story-products ${purchaseMode?"is-selection-mode":""}`}>{items.map(item=>{const current=currentProduct(item);const selected=selectedIds.includes(item.id);const options=sizeOptions(item);const needsSize=selected&&options.length>1&&!sizes[item.id];return <div className={`v52-story-product ${selected?"selected":""}`} key={item.id}><ProductCard product={current} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={purchaseMode} selected={selected} pending={needsSize} onSelect={()=>toggle(item.id)} onVariantChange={product=>{setVariants(state=>({...state,[item.id]:product}));setSizes(state=>{const next={...state};delete next[item.id];return next})}}/>{purchaseMode&&selected&&options.length>1&&<label className="v52-inline-size"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(state=>({...state,[item.id]:event.target.value}))}><option value="">Выбрать</option>{options.map(([name])=><option key={name} value={name}>{name}</option>)}</select></label>}</div>})}</div>
            {purchaseMode&&<footer className="v52-purchase-bar"><div><span>{pending.length?`Выберите размер · ${pending.length}`:selectedProducts.length?`Выбрано ${selectedProducts.length} из ${items.length}`:"Выберите товары"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>ДОБАВИТЬ В КОРЗИНУ</button></footer>}
          </section>
        </div>
      </section>
    </div>}
  </main>;
}

'''

new_editorial = r'''function EditorialView({ editorial, selectProduct, onQuick, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // Direct/legacy editorial entry uses the same V52 collection experience.
  return <CollectionsView onProduct={selectProduct} onQuick={onQuick} favorite={favorite} favorites={favorites} buyBundle={buyBundle} initialEditorial={editorial}/>;
}

'''

text = text[:collections_start] + new_collections + new_editorial + text[lookbook_start:]

old_call = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}'
new_call = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}'
text = text.replace(old_call, new_call)

bridge_marker = "// UNIFIED_SITE_QUERY_BRIDGE_V52"
if bridge_marker not in text:
    anchor = '  const [slide, setSlide] = useState(0);'
    bridge = r'''
  // UNIFIED_SITE_QUERY_BRIDGE_V52
  useEffect(()=>{
    const params=new URLSearchParams(window.location.search);
    const section=params.get("section");
    const open=params.get("open");
    if(section==="collections")setView("collections");
    if(open==="cart")setCartOpen(true);
    if(open==="search")setSearch(true);
    if(open==="account")setAccount(true);
    if(open==="favorites")setFavoritesOpen(true);
    if(section||open)window.history.replaceState({},"",window.location.pathname);
  },[]);'''
    if anchor not in text:
        raise SystemExit("V52: state anchor not found")
    text = text.replace(anchor, anchor + bridge, 1)

page_path.write_text(text, encoding="utf-8")
print("V52 unified collections and site query bridge applied")
