from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

start_token = "function CollectionsView("
end_token = "\n\nfunction LunaEditorialView("

replacement = r'''// EDITORIAL_STORY_OVERLAY_V2
function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  const [kind,setKind]=useState<"Истории"|"Готовые решения">("Истории");
  const [storyPreview,setStoryPreview]=useState<Editorial|null>(null);
  const [selectingStory,setSelectingStory]=useState(false);
  const [selectedStoryIds,setSelectedStoryIds]=useState<number[]>([]);
  const [storySizes,setStorySizes]=useState<Record<number,string>>({});

  const solutionProductIds=Array.from(new Set(editorials.flatMap(item=>item.productIds)));
  const solutionProducts=solutionProductIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const storyItems=(storyPreview?.productIds??[]).map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));

  const sizeOptions=(product:Product)=>Array.from(new Set((product.skus??[]).map(item=>item.size).filter(Boolean)));
  const hasMultipleSizes=(product:Product)=>sizeOptions(product).length>1;
  const selectedColor=(product:Product)=>product.selectedColor??product.skus?.[0]?.color;
  const selectedSize=(product:Product)=>{
    const sizes=sizeOptions(product);
    if(sizes.length===1)return sizes[0];
    return storySizes[product.id]??"";
  };
  const prepareStoryProduct=(product:Product):Product=>{
    const size=selectedSize(product);
    const color=selectedColor(product);
    const sku=size?findProductSku(product,color,size):findProductSku(product,color);
    return {
      ...product,
      price:sku?.price??product.price,
      image:sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      selectedColor:sku?.color??color,
      selectedSize:size||sku?.size??product.selectedSize,
      selectedSkuId:sku?.id??product.selectedSkuId,
      quantity:1,
    };
  };

  const selectedStoryProducts=storyItems.filter(item=>selectedStoryIds.includes(item.id)).map(prepareStoryProduct);
  const pendingSizeIds=storyItems.filter(item=>selectedStoryIds.includes(item.id)&&hasMultipleSizes(item)&&!storySizes[item.id]).map(item=>item.id);
  const storyTotal=storyItems.reduce((sum,item)=>sum+item.price,0);
  const selectedStoryTotal=selectedStoryProducts.reduce((sum,item)=>sum+item.price,0);

  const openStory=(item:Editorial)=>{
    setStoryPreview(item);
    setSelectingStory(false);
    setSelectedStoryIds(item.productIds);
    setStorySizes({});
  };
  const closeStory=()=>{
    setStoryPreview(null);
    setSelectingStory(false);
    setSelectedStoryIds([]);
    setStorySizes({});
  };
  const toggleStoryProduct=(id:number)=>setSelectedStoryIds(current=>current.includes(id)?current.filter(itemId=>itemId!==id):[...current,id]);

  useEffect(()=>{
    if(!storyPreview)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")closeStory()};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  // closeStory intentionally stays local to this overlay lifecycle
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[storyPreview]);

  const handleStoryPurchase=()=>{
    if(!storyItems.length)return;
    if(!selectingStory){
      setSelectingStory(true);
      setSelectedStoryIds(storyItems.map(item=>item.id));
      return;
    }
    if(!selectedStoryProducts.length||pendingSizeIds.length)return;
    buyBundle(selectedStoryProducts);
    closeStory();
  };

  return <div className="collections page">
    <div className="section-head"><p>EDITORIAL</p><h1>Истории и готовые решения</h1></div>
    <div className="center-tabs">{(["Истории","Готовые решения"] as const).map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div>
    {kind==="Истории"?
      <div className="collection-grid">{editorials.map((item)=><article key={item.id}><button onClick={()=>openStory(item)}><img src={assetUrl(item.images[1]??item.images[0])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></span></div></button></article>)}</div>
      :solutionProducts.length?
        <div className="product-grid editorial-solutions-grid">{solutionProducts.map(product=><ProductCard key={`editorial-solution-${product.id}`} product={product} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>
        :<div className="catalog-empty"><p>В опубликованных историях пока нет товаров</p></div>}

    {storyPreview&&<section className={`editorial-story-overlay ${selectingStory?"story-selection-mode":""}`} role="dialog" aria-modal="true" aria-label={`История ${storyPreview.name}`}>
      <div className={`editorial-story-visual ${storyPreview.images.length<2?"single":""}`}>
        {storyPreview.images.map((image,index)=><figure key={`${storyPreview.id}-story-${image}`}><img src={assetUrl(image)} alt={`${storyPreview.name}, editorial ${index+1}`}/><figcaption>{String(index+1).padStart(2,"0")} / {String(storyPreview.images.length).padStart(2,"0")}</figcaption></figure>)}
      </div>
      <aside className="editorial-story-shop">
        <button className="editorial-story-close" type="button" onClick={closeStory} aria-label="Закрыть историю"><Icon name="close"/></button>
        <header className="editorial-story-shop-head">
          <small>{storyPreview.kind} · EDITORIAL</small>
          <h2>{storyPreview.name}</h2>
          <p>{selectingStory?"Выберите предметы истории и размеры там, где это необходимо.":storyPreview.lead}</p>
          {selectingStory&&<div className="editorial-story-selection-tools"><span>{selectedStoryIds.length} из {storyItems.length} выбрано</span><button type="button" onClick={()=>setSelectedStoryIds(selectedStoryIds.length===storyItems.length?[]:storyItems.map(item=>item.id))}>{selectedStoryIds.length===storyItems.length?"Снять выбор":"Выбрать всё"}</button></div>}
        </header>
        <div className="editorial-story-products" aria-label="Товары из истории">
          <div className="editorial-story-catalog-grid product-grid">
            {storyItems.map(item=>{
              const sizes=sizeOptions(item);
              const multiple=sizes.length>1;
              const selected=selectedStoryIds.includes(item.id);
              const pending=selectingStory&&selected&&multiple&&!storySizes[item.id];
              return <div className={`editorial-story-catalog-item ${selected?"selected":""} ${pending?"pending-size":""}`} key={`story-product-${storyPreview.id}-${item.id}`}>
                <ProductCard product={item} onClick={(product)=>{closeStory();onProduct(product)}} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={selectingStory} selected={selected} pending={pending} onSelect={()=>toggleStoryProduct(item.id)}/>
                {selectingStory&&selected&&multiple&&<label className={`editorial-story-size-select ${pending?"required":""}`}>
                  <span>РАЗМЕР</span>
                  <select value={storySizes[item.id]??""} onChange={event=>setStorySizes(current=>({...current,[item.id]:event.target.value}))}>
                    <option value="">Выбрать размер</option>
                    {sizes.map(size=>{
                      const sku=findProductSku(item,selectedColor(item),size);
                      const available=sku?.available!==false;
                      return <option key={`${item.id}-${size}`} value={size} disabled={!available}>{size}{sku?.price?` · ${fmt(sku.price)}`:""}{!available?" · нет в наличии":""}</option>;
                    })}
                  </select>
                </label>}
              </div>;
            })}
          </div>
        </div>
        <footer className="editorial-story-shop-footer">
          <div className="editorial-story-total">
            <span>{selectingStory?pendingSizeIds.length?`Выберите размер · ${pendingSizeIds.length}`:`${productCountLabel(selectedStoryProducts.length)} выбрано`:`${productCountLabel(storyItems.length)} в истории`}</span>
            <strong>{fmt(selectingStory?selectedStoryTotal:storyTotal)}</strong>
          </div>
          <button className="editorial-story-buy" type="button" disabled={!storyItems.length||(selectingStory&&(!selectedStoryProducts.length||pendingSizeIds.length>0))} onClick={handleStoryPurchase}><span>{selectingStory?"ДОБАВИТЬ В КОРЗИНУ":"КУПИТЬ ИСТОРИЮ"}</span><b>{fmt(selectingStory?selectedStoryTotal:storyTotal)}</b></button>
        </footer>
      </aside>
    </section>}
  </div>;
}'''

start = text.find(start_token)
end = text.find(end_token, start)
if start < 0 or end < 0:
    raise SystemExit("Could not locate CollectionsView block")
text = text[:start] + replacement + text[end:]

old_call = '{view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} />}'
new_call = '{view === "collections" && <CollectionsView onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}'
if old_call in text:
    text = text.replace(old_call,new_call,1)
elif new_call not in text:
    raise SystemExit("Could not locate CollectionsView invocation")

path.write_text(text,encoding="utf-8")
print("Editorial story catalog-grid overlay applied")
