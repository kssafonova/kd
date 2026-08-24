from pathlib import Path

page_path = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = "COLLECTIONS_REDESIGN_V23"
if marker in text:
    print("Collections redesign V23 already applied")
    raise SystemExit(0)

start = text.find("function CollectionsView(")
mid = text.find("function EditorialView(", start)
end = text.find("function LookbookViewer(", mid)
if start < 0 or mid < 0 or end < 0:
    raise SystemExit("Collections/Editorial component boundaries not found")

collections = r'''function CollectionsView({ onProduct,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTIONS_REDESIGN_V23
  const [active,setActive]=useState<Editorial|null>(null);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});

  const items=(active?.productIds??[]).map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const sizeOptions=(product:Product)=>Array.from(new Set((product.skus??[]).map(item=>item.size).filter(Boolean)));
  const hasSizes=(product:Product)=>sizeOptions(product).length>1;
  const chosenColor=(product:Product)=>product.selectedColor??product.skus?.[0]?.color??product.colorVariants?.[0]?.name??"";
  const chosenSize=(product:Product)=>{
    const options=sizeOptions(product);
    if(options.length===1)return options[0];
    if(options.length>1)return sizes[product.id]??"";
    return product.selectedSize??product.skus?.[0]?.size??"Единый размер";
  };
  const prepare=(product:Product)=>{
    const color=chosenColor(product);
    const size=chosenSize(product);
    const sku=findProductSku(product,color,size||undefined);
    return {
      ...product,
      price:sku?.price??product.price,
      image:sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      selectedColor:color,
      selectedSize:size||sku?.size||"Единый размер",
      selectedSkuId:sku?.id,
      quantity:1,
    };
  };
  const selectedProducts=items.filter(item=>selectedIds.includes(item.id)).map(prepare);
  const pending=items.filter(item=>selectedIds.includes(item.id)&&hasSizes(item)&&!sizes[item.id]);
  const total=selectedProducts.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;

  const open=(editorial:Editorial)=>{
    setActive(editorial);
    setSelectedIds(editorial.productIds);
    setSizes({});
  };
  const close=()=>{setActive(null);setSelectedIds([]);setSizes({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const addSelected=()=>{
    if(!selectedProducts.length||pending.length)return;
    buyBundle(selectedProducts);
    close();
  };
  const collectionPrice=(editorial:Editorial)=>editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((p):p is Product=>Boolean(p)).reduce((sum,p)=>sum+p.price,0);

  return <main className="collections-v23">
    <header className="collections-v23-head">
      <small>EDITORIAL</small>
      <h1>Капсулы и коллекции</h1>
      <p>Готовые истории для дома. Откройте понравившуюся, выберите нужные предметы и добавьте их в корзину одним действием.</p>
    </header>

    <section className="collections-v23-grid" aria-label="Капсулы и коллекции">
      {editorials.map((editorial,index)=>{
        const count=editorial.productIds.length;
        const price=collectionPrice(editorial);
        return <article className="collections-v23-card" key={editorial.id}>
          <button className="collections-v23-cover" type="button" onClick={()=>open(editorial)} aria-label={`Открыть ${editorial.name}`}>
            <img src={assetUrl(editorial.images[0])} alt={editorial.name}/>
            <span className="collections-v23-index">{String(index+1).padStart(2,"0")}</span>
          </button>
          <div className="collections-v23-card-copy">
            <div><small>{editorial.kind}</small><h2>{editorial.name}</h2><p>{editorial.lead}</p></div>
            <div className="collections-v23-card-bottom"><span>{productCountLabel(count)} · от {fmt(price)}</span><button type="button" onClick={()=>open(editorial)}>СМОТРЕТЬ <Icon name="arrow"/></button></div>
          </div>
        </article>;
      })}
    </section>

    {active&&<section className="collection-v23-layer" role="dialog" aria-modal="true" aria-label={active.name}>
      <header className="collection-v23-topbar"><button type="button" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><span>{active.kind}</span><strong>{active.name}</strong></header>
      <div className="collection-v23-layout">
        <section className="collection-v23-story">
          <div className="collection-v23-hero"><img src={assetUrl(active.images[0])} alt={active.name}/></div>
          <div className="collection-v23-intro"><small>{active.kind} · КУЛЬТУРА ДОМА</small><h2>{active.name}</h2><p>{active.detail}</p></div>
          {active.images.slice(1,3).length>0&&<div className="collection-v23-gallery">{active.images.slice(1,3).map((image,index)=><img src={assetUrl(image)} alt={`${active.name}, деталь ${index+1}`} key={image}/>)}</div>}
        </section>

        <aside className="collection-v23-shop">
          <div className="collection-v23-shop-head"><div><small>СОСТАВ</small><h3>Выберите, что купить</h3><p>Все предметы выбраны по умолчанию. Уберите лишнее и укажите размер только там, где он нужен.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять всё":"Выбрать всё"}</button></div>
          <div className="collection-v23-products">
            {items.map(item=>{
              const prepared=prepare(item);
              const selected=selectedIds.includes(item.id);
              const options=sizeOptions(item);
              return <article className={`collection-v23-product ${selected?"selected":""}`} key={item.id}>
                <label className="collection-v23-check"><input type="checkbox" checked={selected} onChange={()=>toggle(item.id)}/><span>{selected?"✓":""}</span></label>
                <button className="collection-v23-product-image" type="button" onClick={()=>onProduct(prepared)}><ScrollableProductMedia product={prepared} alt={item.name}/></button>
                <div className="collection-v23-product-copy"><button type="button" onClick={()=>onProduct(prepared)}><strong>{item.name}</strong></button><span>Цвет: {prepared.selectedColor||"—"}</span>{options.length>1?<label><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))} disabled={!selected}><option value="">Выбрать размер</option>{options.map(option=><option key={option} value={option}>{option}</option>)}</select></label>:<span>Размер: {prepared.selectedSize}</span>}<b>{priceKnown(prepared.price)?fmt(prepared.price):"Цена уточняется"}</b></div>
              </article>;
            })}
          </div>
          <footer className="collection-v23-summary">
            <div><span>{pending.length?`Нужно выбрать размер · ${pending.length}`:`Выбрано: ${selectedProducts.length} из ${items.length}`}</span><strong>{fmt(total)}</strong></div>
            <button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>ДОБАВИТЬ В КОРЗИНУ</button>
          </footer>
        </aside>
      </div>
    </section>}
  </main>;
}

'''

editorial = r'''function EditorialView({ editorial, selectProduct, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTIONS_REDESIGN_V23_DETAIL
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  useEffect(()=>{setSelectedIds(editorial.productIds);setSizes({})},[editorial.id]);
  const sizeOptions=(product:Product)=>Array.from(new Set((product.skus??[]).map(item=>item.size).filter(Boolean)));
  const prepare=(product:Product)=>{
    const color=product.selectedColor??product.skus?.[0]?.color??product.colorVariants?.[0]?.name??"";
    const options=sizeOptions(product);
    const size=options.length===1?options[0]:options.length>1?(sizes[product.id]??""):(product.selectedSize??product.skus?.[0]?.size??"Единый размер");
    const sku=findProductSku(product,color,size||undefined);
    return {...product,price:sku?.price??product.price,image:sku?.image??product.image,gallery:sku?.gallery??product.gallery,selectedColor:color,selectedSize:size||sku?.size||"Единый размер",selectedSkuId:sku?.id,quantity:1};
  };
  const selected=items.filter(item=>selectedIds.includes(item.id)).map(prepare);
  const pending=items.filter(item=>selectedIds.includes(item.id)&&sizeOptions(item).length>1&&!sizes[item.id]);
  const total=selected.reduce((sum,item)=>sum+item.price,0);
  const allSelected=selectedIds.length===items.length;
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const add=()=>{if(selected.length&&pending.length===0)buyBundle(selected)};

  return <main className="editorial-v23">
    <section className="editorial-v23-hero"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><small>{editorial.kind}</small><h1>{editorial.name}</h1><p>{editorial.lead}</p></div></section>
    <section className="editorial-v23-story"><div><small>ОБ ИСТОРИИ</small><p>{editorial.detail}</p></div>{editorial.images.slice(1,3).map((image,index)=><img src={assetUrl(image)} alt={`${editorial.name}, деталь ${index+1}`} key={image}/>)}</section>
    <section className="editorial-v23-commerce">
      <header><div><small>СОСТАВ</small><h2>{editorial.kind==="КАПСУЛА"?"Купить капсулу":"Купить коллекцию"}</h2><p>Выберите нужные предметы. Размер запрашивается только для товаров с размерной сеткой.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять всё":"Выбрать всё"}</button></header>
      <div className="editorial-v23-products">{items.map(item=>{const prepared=prepare(item);const options=sizeOptions(item);const isSelected=selectedIds.includes(item.id);return <article className={isSelected?"selected":""} key={item.id}><label><input type="checkbox" checked={isSelected} onChange={()=>toggle(item.id)}/><span>{isSelected?"✓":""}</span></label><button className="editorial-v23-product-image" onClick={()=>selectProduct(prepared)}><ScrollableProductMedia product={prepared} alt={item.name}/></button><div><button onClick={()=>selectProduct(prepared)}><strong>{item.name}</strong></button><span>Цвет: {prepared.selectedColor||"—"}</span>{options.length>1?<select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))} disabled={!isSelected}><option value="">Выбрать размер</option>{options.map(option=><option value={option} key={option}>{option}</option>)}</select>:<span>Размер: {prepared.selectedSize}</span>}<b>{fmt(prepared.price)}</b></div></article>})}</div>
      <aside className="editorial-v23-summary"><div><span>{pending.length?`Выберите размер · ${pending.length}`:`${selected.length} из ${items.length} выбрано`}</span><strong>{fmt(total)}</strong></div><button type="button" onClick={add} disabled={!selected.length||pending.length>0}>ДОБАВИТЬ В КОРЗИНУ</button></aside>
    </section>
  </main>;
}

'''

text = text[:start] + collections + editorial + text[end:]
page_path.write_text(text, encoding="utf-8")
print("Applied collections redesign V23")
