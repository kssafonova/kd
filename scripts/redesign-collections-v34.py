from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

# Keep the catalog ProductCard as the single visual source of truth, but expose
# the active color variant to collection bundle selection.
if "PRODUCT_CARD_VARIANT_CALLBACK_V34" not in page:
    old_decl = 'function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void }) {'
    new_decl = 'function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect, onVariantChange }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void; onVariantChange?:(product:Product)=>void }) { // PRODUCT_CARD_VARIANT_CALLBACK_V34'
    if old_decl not in page:
        raise SystemExit("ProductCard declaration not found")
    page = page.replace(old_decl, new_decl, 1)

    anchor = '  const knownPrice=priceKnown(product.price);\n'
    helper = '''  const knownPrice=priceKnown(product.price);\n  const chooseVariant=(index:number)=>{\n    setColorIndex(index);\n    const variant=variants[index];\n    const sku=findProductSku(product,variant.name);\n    onVariantChange?.({...product,image:sku?.image??variant.image,gallery:sku?.gallery??variant.gallery??product.gallery,position:variant.position??product.position,selectedColor:variant.name,selectedSize:sku?.size,selectedSkuId:sku?.id});\n  };\n'''
    if anchor not in page:
        raise SystemExit("ProductCard price anchor not found")
    page = page.replace(anchor, helper, 1)
    if 'onClick={()=>setColorIndex(i)}' not in page:
        raise SystemExit("ProductCard swatch handler not found")
    page = page.replace('onClick={()=>setColorIndex(i)}', 'onClick={()=>chooseVariant(i)}', 1)

collections_start = page.index("function CollectionsView(")
editorial_start = page.index("function EditorialView(", collections_start)
lookbook_start = page.index("function LookbookViewer(", editorial_start)

collections_code = r'''function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTIONS_CATALOG_PARITY_V34
  const [filter,setFilter]=useState<"all"|"capsule"|"collection">("all");
  const [active,setActive]=useState<Editorial|null>(null);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});

  const visible=editorials.filter(item=>filter==="all"||(filter==="capsule"?item.kind==="КАПСУЛА":item.kind==="КОЛЛЕКЦИЯ"));
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
  const open=(editorial:Editorial)=>{setActive(editorial);setSelectedIds(editorial.productIds);setSizes({});setVariants({})};
  const close=()=>{setActive(null);setSelectedIds([]);setSizes({});setVariants({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const collectionPrice=(editorial:Editorial)=>editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((p):p is Product=>Boolean(p)).reduce((sum,p)=>sum+p.price,0);
  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};

  return <main className="collections-v34">
    <header className="collections-v34-head">
      <h1>Капсулы и коллекции</h1>
      <p>Истории для дома, собранные из предметов Культура Дома.</p>
    </header>

    <nav className="collections-v34-tabs" aria-label="Капсулы и коллекции">
      <button type="button" className={filter==="all"?"active":""} onClick={()=>setFilter("all")}>Все</button>
      <button type="button" className={filter==="capsule"?"active":""} onClick={()=>setFilter("capsule")}>Капсулы</button>
      <button type="button" className={filter==="collection"?"active":""} onClick={()=>setFilter("collection")}>Коллекции</button>
    </nav>

    <section className="collections-v34-grid" aria-label="Список капсул и коллекций">
      {visible.map(editorial=><article className="collections-v34-card" key={editorial.id}>
        <button className="collections-v34-image" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v34-copy"><small>{editorial.kind}</small><button type="button" onClick={()=>open(editorial)}><h2>{editorial.name}</h2></button><p>{editorial.lead}</p><div><span>{productCountLabel(editorial.productIds.length)}</span><strong>от {fmt(collectionPrice(editorial))}</strong></div></div>
      </article>)}
    </section>

    {active&&<section className="collection-v34-layer" role="dialog" aria-modal="true" aria-label={active.name}>
      <header className="collection-v34-topbar"><button type="button" onClick={close} aria-label="Назад"><span>←</span> Назад</button><strong>КУЛЬТУРА ДОМА</strong><span>{active.kind}</span></header>
      <section className="collection-v34-hero"><img src={assetUrl(active.images[0])} alt={active.name}/><div><small>{active.kind}</small><h1>{active.name}</h1><p>{active.detail}</p></div></section>
      <section className="collection-v34-products">
        <header><div><h2>Товары коллекции</h2><p>Карточки и выбор цвета работают так же, как в каталоге.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять всё":"Выбрать всё"}</button></header>
        <div className="product-grid collection-catalog-grid-v34">
          {items.map(item=>{
            const selected=selectedIds.includes(item.id);
            const options=sizeOptions(item);
            return <div className={`collection-catalog-item-v34 ${selected?"selected":""}`} key={item.id}>
              <ProductCard product={baseProduct(item)} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} onVariantChange={product=>{setVariants(current=>({...current,[item.id]:product}));setSizes(current=>{const next={...current};delete next[item.id];return next})}}/>
              <label className="collection-catalog-select-v34"><input type="checkbox" checked={selected} onChange={()=>toggle(item.id)}/><span>{selected?"✓":""}</span></label>
              {selected&&options.length>1&&<label className="collection-catalog-size-v34"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))}><option value="">Выбрать размер</option>{options.map(option=><option value={option} key={option}>{option}</option>)}</select></label>}
            </div>;
          })}
        </div>
      </section>
      <footer className="collection-v34-summary"><div><span>{pending.length?`Выберите размер · ${pending.length}`:`Выбрано ${selectedProducts.length} из ${items.length}`}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>ДОБАВИТЬ В КОРЗИНУ</button></footer>
    </section>}
  </main>;
}

'''

editorial_code = r'''function EditorialView({ editorial, selectProduct, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // COLLECTION_EDITORIAL_CATALOG_PARITY_V34
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});
  useEffect(()=>{setSelectedIds(editorial.productIds);setSizes({});setVariants({})},[editorial.id]);
  const baseProduct=(product:Product)=>variants[product.id]??product;
  const sizeOptions=(product:Product)=>{const base=baseProduct(product);const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name;return getProductSizeOptions(base,color).map(([name])=>name)};
  const prepare=(product:Product)=>{const base=baseProduct(product);const color=base.selectedColor??base.skus?.[0]?.color??base.colorVariants?.[0]?.name??"";const options=sizeOptions(product);const chosenSize=options.length===1?options[0]:options.length>1?(sizes[product.id]??""):(base.selectedSize??base.skus?.[0]?.size??"Единый размер");const sku=findProductSku(base,color,chosenSize||undefined);return {...base,price:sku?.price??base.price,image:sku?.image??base.image,gallery:sku?.gallery??base.gallery,selectedColor:color,selectedSize:chosenSize||sku?.size||"Единый размер",selectedSkuId:sku?.id,quantity:1}};
  const selected=items.filter(item=>selectedIds.includes(item.id)).map(prepare);
  const pending=items.filter(item=>selectedIds.includes(item.id)&&sizeOptions(item).length>1&&!sizes[item.id]);
  const total=selected.reduce((sum,item)=>sum+item.price,0);
  const allSelected=selectedIds.length===items.length;
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const add=()=>{if(selected.length&&pending.length===0)buyBundle(selected)};

  return <main className="editorial-v34">
    <section className="editorial-v34-hero"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><small>{editorial.kind}</small><h1>{editorial.name}</h1><p>{editorial.lead}</p></div></section>
    {editorial.images.slice(1,3).length>0&&<section className="editorial-v34-story"><div><small>О КОЛЛЕКЦИИ</small><p>{editorial.detail}</p></div>{editorial.images.slice(1,3).map((image,index)=><img src={assetUrl(image)} alt={`${editorial.name}, ${index+1}`} key={image}/>)}</section>}
    <section className="editorial-v34-products"><header><div><h2>Товары коллекции</h2><p>Те же карточки, цены и варианты, что в каталоге.</p></div><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять всё":"Выбрать всё"}</button></header>
      <div className="product-grid collection-catalog-grid-v34">{items.map(item=>{const isSelected=selectedIds.includes(item.id);const options=sizeOptions(item);return <div className={`collection-catalog-item-v34 ${isSelected?"selected":""}`} key={item.id}><ProductCard product={baseProduct(item)} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)} onVariantChange={product=>{setVariants(current=>({...current,[item.id]:product}));setSizes(current=>{const next={...current};delete next[item.id];return next})}}/><label className="collection-catalog-select-v34"><input type="checkbox" checked={isSelected} onChange={()=>toggle(item.id)}/><span>{isSelected?"✓":""}</span></label>{isSelected&&options.length>1&&<label className="collection-catalog-size-v34"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(current=>({...current,[item.id]:event.target.value}))}><option value="">Выбрать размер</option>{options.map(option=><option value={option} key={option}>{option}</option>)}</select></label>}</div>})}</div>
    </section>
    <aside className="collection-v34-summary editorial-v34-summary"><div><span>{pending.length?`Выберите размер · ${pending.length}`:`Выбрано ${selected.length} из ${items.length}`}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selected.length||pending.length>0} onClick={add}>ДОБАВИТЬ В КОРЗИНУ</button></aside>
  </main>;
}

'''

page = page[:collections_start] + collections_code + editorial_code + page[lookbook_start:]
page_path.write_text(page, encoding="utf-8")
print("Collections V34 applied")
