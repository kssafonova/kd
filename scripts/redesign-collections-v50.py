from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

if "COLLECTIONS_EDITORIAL_V50" in page:
    print("V50 collections redesign already applied")
    raise SystemExit(0)

start = page.find("function CollectionsView(")
editorial_start = page.find("function EditorialView(", start)
lookbook_start = page.find("function LookbookViewer(", editorial_start)
if min(start, editorial_start, lookbook_start) < 0:
    raise RuntimeError("Could not locate collections/editorial component boundaries")

collections = r'''function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTIONS_EDITORIAL_V50
  const [active,setActive]=useState<Editorial|null>(null);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});

  const featured=editorials.find(item=>item.id==="luna")??editorials[0];
  const rest=editorials.filter(item=>item.id!==featured.id);
  const items=(active?.productIds??[]).map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const baseProduct=(product:Product)=>variants[product.id]??product;
  const sizeOptions=(product:Product)=>{
    const base=baseProduct(product);
    const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name;
    return getProductSizeOptions(base,color).map(([name])=>name);
  };
  const prepare=(product:Product)=>{
    const base=baseProduct(product);
    const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name??"";
    const options=sizeOptions(product);
    const chosenSize=options.length===1?options[0]:options.length>1?(sizes[product.id]??""):(base.selectedSize??base.skus?.[0]?.size??"Единый размер");
    const sku=findProductSku(base,color,chosenSize||undefined);
    return {...base,price:sku?.price??base.price,image:sku?.image??base.image,gallery:sku?.gallery??base.gallery,selectedColor:color,selectedSize:chosenSize||sku?.size||"Единый размер",selectedSkuId:sku?.id,quantity:1};
  };
  const selectedProducts=items.filter(item=>selectedIds.includes(item.id)).map(prepare);
  const pending=items.filter(item=>selectedIds.includes(item.id)&&sizeOptions(item).length>1&&!sizes[item.id]);
  const total=selectedProducts.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;
  const collectionPrice=(editorial:Editorial)=>editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((p):p is Product=>Boolean(p)).reduce((sum,p)=>sum+p.price,0);
  const open=(editorial:Editorial)=>{setActive(editorial);setSelectedIds([]);setSizes({});setVariants({})};
  const close=()=>{setActive(null);setSelectedIds([]);setSizes({});setVariants({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};
  const scrollToProducts=()=>document.getElementById("collection-v50-products")?.scrollIntoView({behavior:"smooth",block:"start"});

  return <main className="collections-v50">
    <header className="collections-v50-intro">
      <div><small>КУЛЬТУРА ДОМА · EDITORIAL</small><h1>Коллекции</h1></div>
      <p>Истории для дома, в которых текстиль, посуда и декор собраны в единую палитру. Выберите настроение, а затем — только те предметы, которые нужны именно вам.</p>
    </header>

    <section className="collections-v50-featured" aria-label={`Главная коллекция ${featured.name}`}>
      <button type="button" className="collections-v50-featured-media" onClick={()=>open(featured)}><img src={assetUrl(featured.images[0])} alt={featured.name}/></button>
      <div className="collections-v50-featured-copy"><small>КОЛЛЕКЦИЯ · В ФОКУСЕ</small><h2>{featured.name}</h2><p>{featured.lead}</p><div className="collections-v50-featured-meta"><span>{productCountLabel(featured.productIds.length)} · от {fmt(collectionPrice(featured))}</span><button type="button" onClick={()=>open(featured)}>Смотреть коллекцию →</button></div></div>
    </section>

    <section className="collections-v50-index" aria-labelledby="collections-v50-title">
      <header className="collections-v50-section-head"><div><small>ВСЕ ИСТОРИИ</small><h2 id="collections-v50-title">Коллекции для дома</h2></div><span>{editorials.length} коллекций</span></header>
      <div className="collections-v50-grid">{rest.map(editorial=><article className="collections-v50-card" key={editorial.id}>
        <button className="collections-v50-card-media" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v50-card-copy"><small>КОЛЛЕКЦИЯ</small><button type="button" onClick={()=>open(editorial)}><h3>{editorial.name}</h3></button><p>{editorial.lead}</p><div className="collections-v50-card-meta"><span>{productCountLabel(editorial.productIds.length)}</span><strong>от {fmt(collectionPrice(editorial))}</strong></div></div>
      </article>)}</div>
    </section>

    {active&&<section className="collection-v50-layer" role="dialog" aria-modal="true" aria-label={active.name}>
      <header className="collection-v50-topbar"><button type="button" onClick={close}>← Коллекции</button><strong>КУЛЬТУРА ДОМА</strong><span>КОЛЛЕКЦИЯ</span></header>
      <section className="collection-v50-hero"><img src={assetUrl(active.images[0])} alt={active.name}/><div className="collection-v50-hero-copy"><small className="collection-v50-kicker">КОЛЛЕКЦИЯ</small><h1>{active.name}</h1><p>{active.lead}</p><div className="collection-v50-hero-actions"><button type="button" onClick={scrollToProducts}>Смотреть товары ↓</button><span>{productCountLabel(active.productIds.length)}</span></div></div></section>
      <section className="collection-v50-story"><div className="collection-v50-story-copy"><small>О КОЛЛЕКЦИИ</small><h2>История пространства</h2><p>{active.detail}</p></div>{active.images.slice(1,3).map((image,index)=><img src={assetUrl(image)} alt={`${active.name}, ${index+1}`} key={`${active.id}-${image}`}/>)}</section>
      <section className="collection-v50-products" id="collection-v50-products">
        <header className="collection-v50-products-head"><div><small className="collection-v50-kicker">КУПИТЬ ИСТОРИЮ</small><h2>Товары коллекции</h2><p>Можно выбрать отдельные предметы или собрать всю коллекцию.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всю коллекцию"}</button></header>
        <div className="product-grid collection-v50-grid-products">{items.map(item=>{const selected=selectedIds.includes(item.id);const options=sizeOptions(item);return <div className={`collection-v50-item ${selected?"selected":""}`} key={item.id}><ProductCard product={baseProduct(item)} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} onVariantChange={product=>{setVariants(current=>({...current,[item.id]:product}));setSizes(current=>{const next={...current};delete next[item.id];return next})}}/><label className="collection-v50-select" title={selected?"Убрать из выбора":"Добавить в выбор"}><input type="checkbox" checked={selected} onChange={()=>toggle(item.id)}/><span>{selected?"✓":""}</span></label>{selected&&options.length>1&&<label className="collection-v50-size"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))}><option value="">Выбрать размер</option>{options.map(option=><option value={option} key={option}>{option}</option>)}</select></label>}</div>})}</div>
      </section>
      <footer className="collection-v50-summary"><div className="collection-v50-summary-copy"><span>{pending.length?`Выберите размер · ${pending.length}`:selectedProducts.length?`Выбрано ${selectedProducts.length} из ${items.length}`:"Выберите товары"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>ДОБАВИТЬ В КОРЗИНУ</button></footer>
    </section>}
  </main>;
}'''

editorial = r'''function EditorialView({ editorial, selectProduct, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTION_DETAIL_EDITORIAL_V50
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});
  useEffect(()=>{setSelectedIds([]);setSizes({});setVariants({})},[editorial.id]);
  const baseProduct=(product:Product)=>variants[product.id]??product;
  const sizeOptions=(product:Product)=>{const base=baseProduct(product);const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name;return getProductSizeOptions(base,color).map(([name])=>name)};
  const prepare=(product:Product)=>{const base=baseProduct(product);const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name??"";const options=sizeOptions(product);const chosenSize=options.length===1?options[0]:options.length>1?(sizes[product.id]??""):(base.selectedSize??base.skus?.[0]?.size??"Единый размер");const sku=findProductSku(base,color,chosenSize||undefined);return {...base,price:sku?.price??base.price,image:sku?.image??base.image,gallery:sku?.gallery??base.gallery,selectedColor:color,selectedSize:chosenSize||sku?.size||"Единый размер",selectedSkuId:sku?.id,quantity:1}};
  const selected=items.filter(item=>selectedIds.includes(item.id)).map(prepare);
  const pending=items.filter(item=>selectedIds.includes(item.id)&&sizeOptions(item).length>1&&!sizes[item.id]);
  const total=selected.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const add=()=>{if(selected.length&&pending.length===0)buyBundle(selected)};
  const scrollToProducts=()=>document.getElementById("editorial-v50-products")?.scrollIntoView({behavior:"smooth",block:"start"});

  return <main className="editorial-v50">
    <section className="editorial-v50-hero"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div className="editorial-v50-hero-copy"><small className="collection-v50-kicker">КОЛЛЕКЦИЯ</small><h1>{editorial.name}</h1><p>{editorial.lead}</p><div className="collection-v50-hero-actions"><button type="button" onClick={scrollToProducts}>Смотреть товары ↓</button><span>{productCountLabel(editorial.productIds.length)}</span></div></div></section>
    <section className="collection-v50-story"><div className="collection-v50-story-copy"><small>О КОЛЛЕКЦИИ</small><h2>История пространства</h2><p>{editorial.detail}</p></div>{editorial.images.slice(1,3).map((image,index)=><img src={assetUrl(image)} alt={`${editorial.name}, ${index+1}`} key={`${editorial.id}-${image}`}/>)}</section>
    <section className="collection-v50-products" id="editorial-v50-products"><header className="collection-v50-products-head"><div><small className="collection-v50-kicker">КУПИТЬ ИСТОРИЮ</small><h2>Товары коллекции</h2><p>Можно выбрать отдельные предметы или собрать всю коллекцию.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всю коллекцию"}</button></header>
      <div className="product-grid collection-v50-grid-products">{items.map(item=>{const isSelected=selectedIds.includes(item.id);const options=sizeOptions(item);return <div className={`collection-v50-item ${isSelected?"selected":""}`} key={item.id}><ProductCard product={baseProduct(item)} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)} onVariantChange={product=>{setVariants(current=>({...current,[item.id]:product}));setSizes(current=>{const next={...current};delete next[item.id];return next})}}/><label className="collection-v50-select"><input type="checkbox" checked={isSelected} onChange={()=>toggle(item.id)}/><span>{isSelected?"✓":""}</span></label>{isSelected&&options.length>1&&<label className="collection-v50-size"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))}><option value="">Выбрать размер</option>{options.map(option=><option value={option} key={option}>{option}</option>)}</select></label>}</div>})}</div>
    </section>
    <aside className="collection-v50-summary"><div className="collection-v50-summary-copy"><span>{pending.length?`Выберите размер · ${pending.length}`:selected.length?`Выбрано ${selected.length} из ${items.length}`:"Выберите товары"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selected.length||pending.length>0} onClick={add}>ДОБАВИТЬ В КОРЗИНУ</button></aside>
  </main>;
}'''

page = page[:start] + collections + "\n\n" + editorial + "\n\n" + page[lookbook_start:]
page_path.write_text(page, encoding="utf-8")
print("Applied V50 collections landing and detail redesign")
