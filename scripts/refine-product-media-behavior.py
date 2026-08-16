from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()

start = text.find("function ScrollableProductMedia(")
end_marker = "\n}\n\nconst products: Product[] = ["
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("ScrollableProductMedia boundaries were not found")

helper = '''function ScrollableProductMedia({product,alt,className="",position}:{product:Product;alt:string;className?:string;position?:string}){
  const images=getProductImages(product);
  const vertical=className.includes("pdp-product-media");
  return <div className={`product-media-scroll ${images.length>1?"is-scrollable":""} ${vertical?"vertical-media":"horizontal-media"} ${className}`.trim()} role="group" aria-label={`${alt}: ${images.length} фото`} onWheel={event=>{
    if(images.length<=1)return;
    const node=event.currentTarget;
    if(vertical){
      const delta=event.deltaY||event.deltaX;
      const atStart=node.scrollTop<=0&&delta<0;
      const atEnd=node.scrollTop>=node.scrollHeight-node.clientHeight-1&&delta>0;
      if(!atStart&&!atEnd){node.scrollTop+=delta;event.preventDefault()}
      return;
    }
    if(Math.abs(event.deltaY)>Math.abs(event.deltaX)){
      const atStart=node.scrollLeft<=0&&event.deltaY<0;
      const atEnd=node.scrollLeft>=node.scrollWidth-node.clientWidth-1&&event.deltaY>0;
      if(!atStart&&!atEnd){node.scrollLeft+=event.deltaY;event.preventDefault()}
    }
  }}>{images.map((src,index)=><img key={`${src}-${index}`} src={assetUrl(src)} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>)}</div>;
}'''

text = text[:start] + helper + text[end + len("\n}"):]

for marker in ["product-media-hint", "фото · листайте"]:
    if marker in text:
        raise SystemExit(f"Visible media hint still present: {marker}")
if 'vertical?"vertical-media":"horizontal-media"' not in text:
    raise SystemExit("Media direction marker missing")

path.write_text(text)
print("Removed media hints and set vertical PDP / horizontal storefront media scrolling")
