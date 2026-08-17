from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

text = text.replace(
    'import { useEffect, useMemo, useState } from "react";',
    'import { useEffect, useMemo, useRef, useState } from "react";',
    1,
)

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

  useEffect(()=>{
    if(!vertical||!mobile||activeIndex===undefined)return;
    const node=trackRef.current;
    const target=node?.children[activeIndex] as HTMLElement|undefined;
    if(!node||!target)return;
    node.scrollTo({left:target.offsetLeft,top:0,behavior:"smooth"});
  },[activeIndex,mobile,vertical,imagesKey]);

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
    r'function ScrollableProductMedia\(.*?\n\}(?=\nfunction ProductRail)',
    scrollable.rstrip(),
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit(f"ScrollableProductMedia replacement failed: {count}")

old_thumb = 'onClick={()=>setActiveImage(n)} aria-label={`Фото товара ${n+1}`}'
new_thumb = 'onClick={()=>{setActiveImage(n);if(typeof window!=="undefined"&&window.matchMedia("(min-width: 901px)").matches){document.querySelector(`[data-pdp-image-index="${n}"]`)?.scrollIntoView({behavior:"smooth",block:"start"})}}} aria-label={`Фото товара ${n+1}`}'
if old_thumb in text:
    text = text.replace(old_thumb,new_thumb,1)
elif new_thumb not in text:
    raise SystemExit("PDP thumbnail click handler not found")

# Keep gallery identity tied only to product + colour, never size/image.
text = re.sub(
    r'<ScrollableProductMedia key=\{`\$\{product\.id\}-\$\{color\.name\}(?:-\$\{[^}]+\})?`\} product=\{selectedProduct\} alt=\{`\$\{product\.name\}, \$\{color\.name\}`\} className="pdp-product-media"(?: activeIndex=\{activeImage\} onActiveIndexChange=\{setActiveImage\})?/>',
    '<ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/>',
    text,
    count=1,
)

path.write_text(text,encoding="utf-8")
print("Applied reference-style PDP gallery: page-scroll desktop, sticky thumbnails, mobile swipe")
