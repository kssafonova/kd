from pathlib import Path

root=Path(__file__).resolve().parents[1]
storefront=root/"app"/"storefront-app.tsx"
layout=root/"app"/"catalog"/"layout.tsx"

text=storefront.read_text(encoding="utf-8")

marker='''function ProductRail({items,onProduct,onQuick,favorite,favorites,className=""}:{items:Product[];onProduct:(product:Product)=>void;onQuick:(product:Product)=>void;favorite:(id:number)=>void;favorites:number[];className?:string}){'''
if 'function DeferredProductCardMedia(' not in text and marker in text:
    component='''function DeferredProductCardMedia({product,alt,position}:{product:Product;alt:string;position?:string}){
  const images=getProductImages(product);
  const [active,setActive]=useState(false);
  const activate=()=>{if(images.length>1&&!active)setActive(true)};
  return <div className={`product-media-scroll horizontal-media ${images.length>1?"is-scrollable":""}`} role="group" aria-label={`${alt}: ${images.length} фото`} onPointerEnter={activate} onPointerDown={activate} onFocus={activate} tabIndex={images.length>1?0:-1}>
    <RemoteImage src={images[0]??product.image} alt={alt} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>
    {active&&images.slice(1).map((src,index)=><RemoteImage key={`${src}-${index+1}`} src={src} alt={`${alt}, фото ${index+2}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>)}
  </div>;
}

'''
    text=text.replace(marker,component+marker,1)

single='<RemoteImage src={chosenProduct.image} alt={`${product.name}, ${chosen.name}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:chosen.position||product.position||"center"}}/>'
full='<DeferredProductCardMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, ${chosen.name}`} position={chosen.position||product.position}/>'
text=text.replace(single,full,1)
storefront.write_text(text,encoding="utf-8")

if layout.exists():
    value=layout.read_text(encoding="utf-8")
    if 'import "../product-card-gallery.css";' not in value:
        value=value.replace('import "../product-media-scroll.css";\n','import "../product-media-scroll.css";\nimport "../product-card-gallery.css";\n',1)
    if 'import { ProductCardGalleryEnhancer } from "../product-card-gallery";' not in value:
        value=value.replace('import { CollectionPurchaseEnhancer } from "../collection-purchase-enhancer";\n','import { ProductCardGalleryEnhancer } from "../product-card-gallery";\nimport { CollectionPurchaseEnhancer } from "../collection-purchase-enhancer";\n',1)
    if '<ProductCardGalleryEnhancer />' not in value:
        value=value.replace('  return <>\n','  return <>\n    <ProductCardGalleryEnhancer />\n',1)
    layout.write_text(value,encoding="utf-8")

print("Restored full Фото 1–3 PLP gallery with deferred secondary image loading")
