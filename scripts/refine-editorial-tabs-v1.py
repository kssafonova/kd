from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Newer fullscreen Editorial story overlay owns CollectionsView completely.
# In that state this legacy tab migration is already superseded and must not fail.
if "EDITORIAL_STORY_OVERLAY_V1" in text or "EDITORIAL_STORY_OVERLAY_V2" in text or "buyBundle:(items:Product[])=>void" in text:
    print("Skipped legacy Editorial tab refinement: fullscreen story overlay already owns CollectionsView")
    raise SystemExit(0)

replacement = '''function CollectionsView({ openEditorial,onProduct,onQuick,favorite,favorites }: { openEditorial:(editorial:Editorial)=>void; onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {
  const [kind,setKind]=useState<"Истории"|"Готовые решения">("Истории");
  const solutionProductIds=Array.from(new Set(editorials.flatMap(item=>item.productIds)));
  const solutionProducts=solutionProductIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  return <div className="collections page">
    <div className="section-head"><p>EDITORIAL</p><h1>Истории и готовые решения</h1></div>
    <div className="center-tabs">{(["Истории","Готовые решения"] as const).map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div>
    {kind==="Истории"?
      <div className="collection-grid">{editorials.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></span></div></button></article>)}</div>
      :solutionProducts.length?
        <div className="product-grid editorial-solutions-grid">{solutionProducts.map(product=><ProductCard key={`editorial-solution-${product.id}`} product={product} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>
        :<div className="catalog-empty"><p>В опубликованных историях пока нет товаров</p></div>}
  </div>;
}

function LunaEditorialView'''

pattern = r'function CollectionsView\(\{ openEditorial \}: \{ openEditorial:\(editorial:Editorial\)=>void \}\) \{[\s\S]*?\n\}\n\nfunction LunaEditorialView'
text, count = re.subn(pattern, replacement, text, count=1)
if count != 1:
    pattern = r'function CollectionsView\(\{ openEditorial,onProduct,onQuick,favorite,favorites \}[\s\S]*?\n\}\n\nfunction LunaEditorialView'
    text, count = re.subn(pattern, replacement, text, count=1)
if count != 1:
    raise SystemExit("Could not patch CollectionsView")

old_call = '{view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}'
new_call = '{view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} />}'
if old_call in text:
    text = text.replace(old_call,new_call,1)
elif new_call not in text:
    raise SystemExit("Could not patch CollectionsView usage")

PAGE.write_text(text, encoding="utf-8")
print("Refined Editorial: Stories + product-based Ready solutions")
