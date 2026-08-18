from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

marker = "// EDITORIAL_STORY_OVERLAY_V1"
start_token = "function CollectionsView("
end_token = "\n\nfunction LunaEditorialView("

replacement = r'''// EDITORIAL_STORY_OVERLAY_V1
function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  const [kind,setKind]=useState<"Истории"|"Готовые решения">("Истории");
  const [storyPreview,setStoryPreview]=useState<Editorial|null>(null);
  const solutionProductIds=Array.from(new Set(editorials.flatMap(item=>item.productIds)));
  const solutionProducts=solutionProductIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const storyItems=(storyPreview?.productIds??[]).map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const storyTotal=storyItems.reduce((sum,item)=>sum+item.price,0);

  useEffect(()=>{
    if(!storyPreview)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")setStoryPreview(null)};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  },[storyPreview]);

  const buyStory=()=>{
    if(!storyItems.length)return;
    buyBundle(storyItems);
    setStoryPreview(null);
  };

  return <div className="collections page">
    <div className="section-head"><p>EDITORIAL</p><h1>Истории и готовые решения</h1></div>
    <div className="center-tabs">{(["Истории","Готовые решения"] as const).map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div>
    {kind==="Истории"?
      <div className="collection-grid">{editorials.map((item)=><article key={item.id}><button onClick={()=>setStoryPreview(item)}><img src={assetUrl(item.images[1]??item.images[0])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></span></div></button></article>)}</div>
      :solutionProducts.length?
        <div className="product-grid editorial-solutions-grid">{solutionProducts.map(product=><ProductCard key={`editorial-solution-${product.id}`} product={product} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>
        :<div className="catalog-empty"><p>В опубликованных историях пока нет товаров</p></div>}

    {storyPreview&&<section className="editorial-story-overlay" role="dialog" aria-modal="true" aria-label={`История ${storyPreview.name}`}>
      <div className={`editorial-story-visual ${storyPreview.images.length<2?"single":""}`}>
        {storyPreview.images.slice(0,3).map((image,index)=><figure key={`${storyPreview.id}-story-${image}`}><img src={assetUrl(image)} alt={`${storyPreview.name}, editorial ${index+1}`}/></figure>)}
      </div>
      <aside className="editorial-story-shop">
        <button className="editorial-story-close" type="button" onClick={()=>setStoryPreview(null)} aria-label="Закрыть историю"><Icon name="close"/></button>
        <header className="editorial-story-shop-head">
          <small>{storyPreview.kind} · EDITORIAL</small>
          <h2>{storyPreview.name}</h2>
          <p>{storyPreview.lead}</p>
        </header>
        <div className="editorial-story-products" aria-label="Товары из истории">
          {storyItems.map(item=><button className="editorial-story-product" type="button" key={`story-product-${storyPreview.id}-${item.id}`} onClick={()=>{setStoryPreview(null);onProduct(item)}}>
            <span className="editorial-story-product-image"><RemoteImage src={item.image} alt={item.name}/></span>
            <span className="editorial-story-product-copy"><strong>{item.name}</strong><span>{item.note}</span></span>
            <strong>{priceKnown(item.price)?fmt(item.price):"Цена уточняется"}</strong>
          </button>)}
        </div>
        <footer className="editorial-story-shop-footer">
          <div className="editorial-story-total"><span>{productCountLabel(storyItems.length)} в истории</span><strong>{fmt(storyTotal)}</strong></div>
          <button className="editorial-story-buy" type="button" disabled={!storyItems.length} onClick={buyStory}><span>КУПИТЬ ИСТОРИЮ</span><b>{fmt(storyTotal)}</b></button>
        </footer>
      </aside>
    </section>}
  </div>;
}'''

if marker not in text:
    start = text.find(start_token)
    end = text.find(end_token, start)
    if start < 0 or end < 0:
        raise SystemExit("Could not locate CollectionsView block")
    text = text[:start] + replacement + text[end:]
else:
    print("Editorial story overlay component already present")

old_call = '{view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} />}'
new_call = '{view === "collections" && <CollectionsView onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}'
if old_call in text:
    text = text.replace(old_call,new_call,1)
elif new_call not in text:
    raise SystemExit("Could not locate CollectionsView invocation")

path.write_text(text,encoding="utf-8")
print("Editorial story overlay applied")
