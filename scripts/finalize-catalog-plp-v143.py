from pathlib import Path

root = Path(__file__).resolve().parents[1]
storefront = root / "app" / "storefront-app.tsx"
text = storefront.read_text(encoding="utf-8")

# catalog_master.csv is the source of truth. Legacy merchandising removals must
# not delete products that are explicitly present in the current table.
old_retired = 'for(let index=products.length-1;index>=0;index-=1){if(isRetiredCatalogProduct(products[index].name))products.splice(index,1)}'
new_retired = 'if(!CATALOG_PRODUCTS_GENERATED.length){for(let index=products.length-1;index>=0;index-=1){if(isRetiredCatalogProduct(products[index].name))products.splice(index,1)}}'
text = text.replace(old_retired, new_retired, 1)

# Keep every Фото 1–3 available in PLP from the first interaction. Cards are
# mounted progressively, and every image uses native lazy loading, so this is
# reliable on touch devices without restoring the old all-catalog network burst.
old_media = '''function DeferredProductCardMedia({product,alt,position}:{product:Product;alt:string;position?:string}){
  const images=getProductImages(product);
  const [active,setActive]=useState(false);
  const activate=()=>{if(images.length>1&&!active)setActive(true)};
  return <div className={`product-media-scroll horizontal-media ${images.length>1?"is-scrollable":""}`} role="group" aria-label={`${alt}: ${images.length} фото`} onPointerEnter={activate} onPointerDown={activate} onFocus={activate} tabIndex={images.length>1?0:-1}>
    <RemoteImage src={images[0]??product.image} alt={alt} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>
    {active&&images.slice(1).map((src,index)=><RemoteImage key={`${src}-${index+1}`} src={src} alt={`${alt}, фото ${index+2}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>)}
  </div>;
}'''
new_media = '''function DeferredProductCardMedia({product,alt,position}:{product:Product;alt:string;position?:string}){
  const images=getProductImages(product);
  const sources=images.length?images:[product.image];
  return <div className={`product-media-scroll horizontal-media ${sources.length>1?"is-scrollable":""}`} role="group" aria-label={`${alt}: ${sources.length} фото`} tabIndex={sources.length>1?0:-1}>
    {sources.map((src,index)=><RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>)}
  </div>;
}'''
if old_media in text:
    text = text.replace(old_media, new_media, 1)

# Smaller initial PLP batch = faster first paint. IntersectionObserver appends
# subsequent groups before the user reaches the end of the mounted products.
text = text.replace('const [visibleCount,setVisibleCount]=useState(24);', 'const [visibleCount,setVisibleCount]=useState(18);', 1)
text = text.replace('useEffect(()=>{setVisibleCount(24)},[resultKey]);', 'useEffect(()=>{setVisibleCount(18)},[resultKey]);', 1)
text = text.replace('Math.min(current+24,list.length)', 'Math.min(current+18,list.length)', 1)

# PDP breadcrumb links use the same route contract as the standalone homepage.
old_pdp_crumbs = '<div className="crumbs">Главная / {product.category??"Каталог"} / {product.name}</div>'
new_pdp_crumbs = '<nav className="crumbs catalog-crumbs-v141" aria-label="Хлебные крошки"><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/`}}>Главная</button><span>/</span><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/catalog/?category=${encodeURIComponent(product.category??"Все товары")}`}}>{product.category??"Каталог"}</button><span>/</span><b>{product.name}</b></nav>'
text = text.replace(old_pdp_crumbs, new_pdp_crumbs, 1)

storefront.write_text(text, encoding="utf-8")
print("Catalog V143: CSV is authoritative, 139 articles retained, full lazy PLP galleries, 18-card progressive batches, linked PDP breadcrumbs")
