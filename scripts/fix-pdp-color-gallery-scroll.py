from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

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

  useEffect(()=>{
    if(activeIndex===undefined)return;
    const node=trackRef.current;
    const target=node?.children[activeIndex] as HTMLElement|undefined;
    if(!node||!target)return;
    const horizontal=node.scrollWidth>node.clientWidth+2;
    node.scrollTo({
      left:horizontal?target.offsetLeft:0,
      top:horizontal?0:target.offsetTop,
      behavior:"smooth",
    });
  },[activeIndex,images.join("|")]);

  const syncActiveIndex=()=>{
    if(!onActiveIndexChange)return;
    const node=trackRef.current;
    if(!node)return;
    const horizontal=node.scrollWidth>node.clientWidth+2;
    const extent=horizontal?node.clientWidth:node.clientHeight;
    if(extent<=0)return;
    const positionValue=horizontal?node.scrollLeft:node.scrollTop;
    const next=Math.max(0,Math.min(images.length-1,Math.round(positionValue/extent)));
    if(next!==activeIndex)onActiveIndexChange(next);
  };

  return <div ref={trackRef} className={`product-media-scroll ${images.length>1?"is-scrollable":""} ${vertical?"vertical-media":"horizontal-media"} ${className}`.trim()} role="group" aria-label={`${alt}: ${images.length} фото`} onScroll={syncActiveIndex}>{images.map((src,index)=><RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>)}</div>;
}
'''
text, count = re.subn(
    r'function ScrollableProductMedia\(\{product,alt,className="",position\}:\{product:Product;alt:string;className\?:string;position\?:string\}\)\{.*?\n\}\n(?=\nfunction ProductRail)',
    scrollable.rstrip(),
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    # Already patched form: replace any ScrollableProductMedia implementation.
    text, count = re.subn(
        r'function ScrollableProductMedia\(.*?\n\}\n(?=\nfunction ProductRail)',
        scrollable.rstrip(),
        text,
        count=1,
        flags=re.S,
    )
if count != 1:
    raise SystemExit(f"ScrollableProductMedia replacement failed: {count}")

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

old_media = '<ScrollableProductMedia key={`${product.id}-${color.name}-${image}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media"/>'
new_media = '<ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/>'
if old_media in text:
    text = text.replace(old_media,new_media,1)
elif new_media not in text:
    raise SystemExit("PDP media component not found")

text, count = re.subn(
    r'<small className="pdp-code">АРТИКУЛ: \{displaySku\?\.article\?\?product\.article\?\?`KD-PD-\$\{1020\+product\.id\}`\}\{displaySku&&<> · SKU: \{displaySku\.id\}</>\}</small>',
    '<small className="pdp-code">АРТИКУЛ: {product.article??`KD-PD-${1020+product.id}`}</small>',
    text,
    count=1,
)
if count != 1 and ' · SKU:' in text:
    raise SystemExit("SKU label removal failed")

path.write_text(text,encoding="utf-8")
print("PDP media now follows color only; size selection keeps gallery stable; native scrolling enabled; SKU label hidden")
