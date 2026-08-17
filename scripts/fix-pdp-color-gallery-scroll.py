from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

# Ensure hooks used by the gallery are available.
text = text.replace(
    'import { useEffect, useMemo, useState } from "react";',
    'import { useEffect, useMemo, useRef, useState } from "react";',
    1,
)

find_sku = '''function findProductSku(product:Product,color?:string,size?:string){
  if(!product.skus?.length)return undefined;
  const selectedById=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
  if(selectedById&&(!color||selectedById.color===color)&&(!size||selectedById.size===size))return selectedById;
  return product.skus.find(item=>(!color||item.color===color)&&(!size||item.size===size))
    ??product.skus.find(item=>!color||item.color===color)
    ??product.skus[0];
}
'''
text, count = re.subn(
    r'function findProductSku\(product:Product,color\?:string,size\?:string\)\{.*?\n\}\n(?=\nfunction getProductSizeOptions)',
    find_sku.rstrip(),
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"findProductSku replacement failed: {count}")

get_images = '''function getProductImages(product:Product){
  if(product.skus?.length){
    const selectedById=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
    const mediaColor=product.selectedColor??selectedById?.color;
    const mediaSku=product.skus.find(item=>!mediaColor||item.color===mediaColor)??product.skus[0];
    return Array.from(new Set([mediaSku.image,...mediaSku.gallery].filter(Boolean)));
  }
  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;
  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];
  return Array.from(new Set(sources.filter(Boolean)));
}
'''
text, count = re.subn(
    r'function getProductImages\(product:Product\)\{.*?\n\}\n(?=\nfunction ScrollableProductMedia)',
    get_images.rstrip(),
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"getProductImages replacement failed: {count}")

scrollable = '''function ScrollableProductMedia({product,alt,className="",position,activeIndex,onActiveIndexChange}:{product:Product;alt:string;className?:string;position?:string;activeIndex?:number;onActiveIndexChange?:(index:number)=>void}){
  const images=getProductImages(product);
  const vertical=className.includes("pdp-product-media");
  const trackRef=useRef<HTMLDivElement>(null);
  const [mobile,setMobile]=useState(false);
  const imagesKey=images.join("|");

  useEffect(()=>{
    if(!vertical)return;
    const mediaQuery=window.matchMedia("(max-width: 900px)");
    const update=()=>setMobile(mediaQuery.matches);
    update();
    mediaQuery.addEventListener?.("change",update);
    return()=>mediaQuery.removeEventListener?.("change",update);
  },[vertical]);

  // Mobile PDP remains a horizontal native swipe gallery.
  useEffect(()=>{
    if(!vertical||!mobile||activeIndex===undefined)return;
    const node=trackRef.current;
    const target=node?.children[activeIndex] as HTMLElement|undefined;
    if(!node||!target)return;
    node.scrollTo({left:target.offsetLeft,top:0,behavior:"smooth"});
  },[activeIndex,mobile,vertical,imagesKey]);

  // Desktop PDP uses the page itself as the scroll container. Keep the active
  // thumbnail in sync with the large image currently visible in the viewport.
  useEffect(()=>{
    if(!vertical||mobile||!onActiveIndexChange)return;
    const node=trackRef.current;
    if(!node)return;
    const children=Array.from(node.children) as HTMLElement[];
    const observer=new IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting);
      if(!visible.length)return;
      visible.sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
      const next=Number((visible[0].target as HTMLElement).dataset.pdpImageIndex??0);
      if(Number.isFinite(next))onActiveIndexChange(next);
    },{root:null,rootMargin:"-110px 0px -38% 0px",threshold:[.15,.3,.5,.7,.85]});
    children.forEach(child=>observer.observe(child));
    return()=>observer.disconnect();
  },[vertical,mobile,onActiveIndexChange,imagesKey]);

  const syncMobileIndex=()=>{
    if(!vertical||!mobile||!onActiveIndexChange)return;
    const node=trackRef.current;
    if(!node||node.clientWidth<=0)return;
    const next=Math.max(0,Math.min(images.length-1,Math.round(node.scrollLeft/node.clientWidth)));
    if(next!==activeIndex)onActiveIndexChange(next);
  };

  return <div ref={trackRef} className={`product-media-scroll ${images.length>1?"is-scrollable":""} ${vertical?"vertical-media":"horizontal-media"} ${className}`.trim()} role="group" aria-label={`${alt}: ${images.length} фото`} onScroll={vertical&&mobile?syncMobileIndex:undefined}>{images.map((src,index)=><RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} data-pdp-image-index={vertical?index:undefined} style={{objectPosition:position||product.position||"center"}} draggable={false}/>)}</div>;
}
'''
text, count = re.subn(
    r'function ScrollableProductMedia\(.*?\n\}\n(?=\nfunction ProductRail)',
    scrollable.rstrip(),
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"ScrollableProductMedia replacement failed: {count}")

# Media belongs to the selected colour, not the selected size.
text = text.replace(
    '  const mediaSku=sku??findProductSku(product,color.name);',
    '  const mediaSku=findProductSku(product,color.name);',
    1,
)
text = text.replace(
    '  const image=gallery[activeImage]??mediaSku?.image??color.image;\n',
    '',
    1,
)
text = text.replace(
    '  const selectedProduct={...product,price:unitPrice,image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};',
    '  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};',
    1,
)
text = text.replace('  const displaySku=sku??mediaSku;\n','',1)

# Main gallery remounts only when product/colour changes, never when size changes.
text = re.sub(
    r'<ScrollableProductMedia key=\{`\$\{product\.id\}-\$\{color\.name\}(?:-\$\{image\})?`\} product=\{selectedProduct\} alt=\{`\$\{product\.name\}, \$\{color\.name\}`\} className="pdp-product-media"(?: activeIndex=\{activeImage\} onActiveIndexChange=\{setActiveImage\})?/>',
    '<ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/>',
    text,
    count=1,
)

# Thumbnail click scrolls the PAGE to the corresponding large image on desktop.
text = re.sub(
    r'onClick=\{\(\)=>setActiveImage\(n\)\} aria-label=\{`Фото товара \$\{n\+1\}`\}',
    'onClick={()=>{setActiveImage(n);if(typeof window!=="undefined"&&window.matchMedia("(min-width: 901px)").matches){document.querySelector(`[data-pdp-image-index="${n}"]`)?.scrollIntoView({behavior:"smooth",block:"start"})}}} aria-label={`Фото товара ${n+1}`}',
    text,
    count=1,
)

# SKU is internal: PDP displays only the article.
text, _ = re.subn(
    r'<small className="pdp-code">АРТИКУЛ: \{displaySku\?\.article\?\?product\.article\?\?`KD-PD-\$\{1020\+product\.id\}`\}\{displaySku&&<> · SKU: \{displaySku\.id\}</>\}</small>',
    '<small className="pdp-code">АРТИКУЛ: {product.article??`KD-PD-${1020+product.id}`}</small>',
    text,
    count=1,
)
if ' · SKU:' in text:
    raise SystemExit("SKU label removal failed")

path.write_text(text,encoding="utf-8")
print("PDP gallery matches editorial reference: sticky thumbnails, page-scroll desktop gallery, horizontal mobile swipe, colour-stable media")
