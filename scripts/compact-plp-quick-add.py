from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

new_flow = r'''function PLPSizeFlow({ product, close, add }: { product:Product; close:()=>void; add:(size:string,color:string,unitPrice:number)=>void }) {
  const variants=product.colorVariants?.length?product.colorVariants:[{name:product.selectedColor??"Молочный",hex:"#eee",image:product.image,gallery:product.gallery,position:product.position}];
  const initialColorIndex=Math.max(0,variants.findIndex(variant=>variant.name===product.selectedColor));
  const [colorIndex,setColorIndex]=useState(initialColorIndex);
  const [detailsOpen,setDetailsOpen]=useState(false);
  const color=variants[colorIndex]??variants[0];
  const sizes=getProductSizeOptions(product,color.name);
  const [chosenSize,setChosenSize]=useState(sizes.length===1?(sizes[0]?.[0]??""):"");

  useEffect(()=>{
    const next=getProductSizeOptions(product,color.name);
    setChosenSize(next.length===1?(next[0]?.[0]??""):"");
  },[product.id,color.name]);

  const mediaSku=findProductSku(product,color.name);
  const selectedSku=chosenSize?findProductSku(product,color.name,chosenSize):undefined;
  const unitPrice=selectedSku?.price??sizes.find(([name])=>name===chosenSize)?.[1]??product.price;
  const hasSingleSize=sizes.length===1;
  const requiresSizeChoice=sizes.length>1;
  const canAdd=hasSingleSize||Boolean(chosenSize);
  const mediaProduct:Product={...product,selectedColor:color.name,selectedSkuId:selectedSku?.id??mediaSku?.id,image:mediaSku?.image??color.image??product.image,gallery:mediaSku?.gallery??color.gallery??product.gallery};
  const salePercent=product.oldPrice&&product.oldPrice>product.price?Math.round((1-product.price/product.oldPrice)*100):0;

  return <div className="overlay plp-flow plp-compact-flow">
    <button className="overlay-bg" onClick={close} aria-label="Закрыть"/>
    <section className="plp-modal plp-compact-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}>
      <button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button>

      <div className="plp-reference-gallery">
        <ScrollableProductMedia product={mediaProduct} alt={product.name} className="plp-reference-media" position={color.position??product.position}/>
      </div>

      <div className="plp-reference-body">
        <h2>{product.name}</h2>
        <div className="plp-reference-price">
          <strong>{fmt(product.price)}</strong>
          {product.oldPrice&&product.oldPrice>product.price&&<del>{fmt(product.oldPrice)}</del>}
          {salePercent>0&&<span>−{salePercent}%</span>}
        </div>

        <div className="plp-reference-color">
          <p>Цвет: {color.name.toLowerCase()}</p>
          {variants.length>1?<div className="plp-compact-swatches" role="group" aria-label="Выберите цвет">{variants.map((variant,index)=><button key={variant.name} type="button" className={index===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(index)} aria-label={`Цвет ${variant.name}`} title={variant.name}/>)}</div>:<div className="plp-reference-one-swatch" style={{background:color.hex}} aria-hidden="true"/>}
        </div>

        {product.note&&<p className="plp-reference-note">{product.note}</p>}

        <button className="plp-reference-details" type="button" onClick={()=>setDetailsOpen(current=>!current)} aria-expanded={detailsOpen}>
          <span>ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ</span><Icon name="chevron"/>
        </button>
        {detailsOpen&&<div className="plp-reference-details-copy">Материалы, состав и рекомендации по уходу доступны в карточке товара.</div>}

        <div className="plp-compact-field size-field">
          <div className="plp-compact-size-head"><span>РАЗМЕР</span><button type="button" onClick={()=>alert("Руководство по размерам")}>Руководство по размерам</button></div>
          {requiresSizeChoice?<div className="plp-compact-sizes" role="group" aria-label="Выберите размер">{sizes.map(([name,price])=><button key={name} type="button" className={chosenSize===name?"active":""} aria-pressed={chosenSize===name} onClick={()=>setChosenSize(name)}><span>{name}</span><b>{fmt(price)}</b></button>)}</div>:<div className="plp-compact-static-size"><strong>{sizes[0]?.[0]??product.selectedSize??"Единый размер"}</strong><b>{fmt(sizes[0]?.[1]??product.price)}</b></div>}
        </div>

        <button className={`primary plp-compact-add ${canAdd?"is-ready":"is-disabled"}`} type="button" disabled={!canAdd} aria-disabled={!canAdd} onClick={()=>{if(!canAdd)return;add(chosenSize,color.name,unitPrice)}}>{canAdd?`Добавить в корзину · ${fmt(unitPrice)}`:"Выберите размер"}</button>

        <button className="plp-reference-availability" type="button" onClick={()=>alert("Показываем наличие выбранного товара в бутиках")}> <Icon name="pin"/><span>НАЛИЧИЕ В МАГАЗИНАХ</span></button>
      </div>
    </section>
  </div>;
}'''

pattern = r'function PLPSizeFlow\([\s\S]*?\n}\n\nfunction ProductInfoDrawer'
match = re.search(pattern, page)
if not match:
    raise SystemExit("PLPSizeFlow block not found")
page = re.sub(pattern, new_flow + '\n\nfunction ProductInfoDrawer', page, count=1)

old_mount = '{plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,quantity,unitPrice) => addFromPLP(plpSize, chosenSize, quantity, unitPrice)} />}'
new_mount = '{plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,color,unitPrice) => addFromPLP({...plpSize,selectedColor:color}, chosenSize, 1, unitPrice)} />}'
if old_mount in page:
    page = page.replace(old_mount, new_mount, 1)
elif new_mount not in page:
    raise SystemExit("PLPSizeFlow mount not found")

page_path.write_text(page, encoding="utf-8")

css = re.sub(r'\n?/\* COMPACT_PLP_QUICK_ADD_V1 \*/[\s\S]*?/\* END_COMPACT_PLP_QUICK_ADD_V1 \*/', '', css)
css += r'''

/* COMPACT_PLP_QUICK_ADD_V1 */
.plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0 4px!important}
.plp-flow.plp-compact-flow .overlay-bg{background:rgba(0,0,0,.28)!important}
.plp-flow .plp-compact-modal{
  position:relative!important;
  width:min(646px,calc(100vw - 8px))!important;
  height:auto!important;
  max-height:94vh!important;
  display:flex!important;
  flex-direction:column!important;
  overflow-y:auto!important;
  margin:0!important;
  background:#fff!important;
  border:1px solid #e7e2dc!important;
  border-radius:0!important;
  box-shadow:0 -10px 35px rgba(0,0,0,.10)!important;
  animation:none!important;
}
.plp-flow .plp-compact-modal>.close{
  position:absolute!important;
  top:12px!important;
  right:12px!important;
  width:32px!important;
  height:32px!important;
  display:grid!important;
  place-items:center!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-radius:50%!important;
  background:rgba(255,255,255,.94)!important;
  z-index:8!important;
}
.plp-flow .plp-compact-modal>.close svg{width:17px!important;height:17px!important}
.plp-reference-gallery{position:relative;width:100%;background:#f3f1ed;overflow:hidden}
.plp-reference-media{display:flex!important;width:100%!important;height:auto!important;overflow-x:auto!important;overflow-y:hidden!important;scroll-snap-type:x mandatory!important;scrollbar-width:none!important;overscroll-behavior-x:contain!important}
.plp-reference-media::-webkit-scrollbar{display:none!important}
.plp-reference-media>img{flex:0 0 100%!important;width:100%!important;height:auto!important;aspect-ratio:1.68/1!important;object-fit:cover!important;scroll-snap-align:start!important}
.plp-reference-body{display:flex;flex-direction:column;padding:38px 44px 34px;background:#fff}
.plp-reference-body h2{margin:0 0 12px;font-size:22px;line-height:1.15;font-weight:500;letter-spacing:.01em;text-transform:uppercase;color:#1d1d1f}
.plp-reference-price{display:flex;align-items:baseline;gap:14px;margin-bottom:14px}
.plp-reference-price strong{font-size:16px;font-weight:600;color:#1d1d1f}
.plp-reference-price del{font-size:13px;color:#9a9690}
.plp-reference-price span{font-size:12px;color:#9a6748;background:#f4e8df;padding:6px 9px}
.plp-reference-color{display:flex;flex-direction:column;align-items:flex-start;gap:10px;margin-bottom:26px}
.plp-reference-color p{margin:0;font-size:12px;color:#4b4b4b}
.plp-compact-swatches{display:flex;align-items:center;gap:10px;flex-wrap:wrap;min-height:30px}
.plp-compact-swatches button,.plp-reference-one-swatch{width:27px;height:27px;border:1px solid #dedede;border-radius:0;padding:0;box-shadow:0 0 0 2px #fff}
.plp-compact-swatches button{cursor:pointer}
.plp-compact-swatches button.active{outline:2px solid #1d1d1f;outline-offset:2px}
.plp-reference-note{margin:0 0 22px;font-size:12px;line-height:1.55;color:#666}
.plp-reference-details{width:100%;display:flex;align-items:center;justify-content:space-between;gap:18px;height:42px;border:0;border-bottom:1px solid #d8d6d1;background:#fff;padding:0;font:inherit;color:#262626;text-align:left;cursor:pointer}
.plp-reference-details span{font-size:10px;letter-spacing:.07em;text-decoration:underline;text-underline-offset:2px}
.plp-reference-details svg{width:16px;height:16px;transition:transform .16s ease}
.plp-reference-details[aria-expanded="true"] svg{transform:rotate(90deg)}
.plp-reference-details-copy{padding:13px 0 18px;font-size:11px;line-height:1.5;color:#6f6f6f;border-bottom:1px solid #e3e1dd}
.plp-compact-field{display:flex;flex-direction:column;align-items:flex-start;gap:0;min-width:0;width:100%;margin-top:26px}
.plp-compact-size-head{width:100%;display:flex;align-items:center;justify-content:space-between;gap:14px;padding:0 4px 9px}
.plp-compact-size-head span{font-size:10px;letter-spacing:.08em;color:#333}
.plp-compact-size-head button{border:0;background:transparent;padding:0;font:inherit;font-size:11px;color:#292929;text-decoration:underline;text-underline-offset:2px;cursor:pointer}
.plp-compact-sizes{width:100%;border-top:1px solid #1d1d1f}
.plp-compact-sizes button,.plp-compact-static-size{width:100%;min-height:54px;display:flex;align-items:center;justify-content:space-between;gap:16px;border:0;border-bottom:1px solid #dedede;background:#fff;padding:0 14px;font:inherit;color:#1d1d1f}
.plp-compact-sizes button{cursor:pointer;text-align:left}
.plp-compact-sizes button span,.plp-compact-static-size strong{font-size:14px;font-weight:400}
.plp-compact-sizes button b,.plp-compact-static-size b{font-size:13px;font-weight:500;white-space:nowrap;color:#2a2a2a}
.plp-compact-sizes button:hover{background:#faf9f7}
.plp-compact-sizes button.active{background:#f5f4f1;box-shadow:inset 2px 0 0 #1d1d1f}
.plp-compact-sizes button.active span{font-weight:500}
.plp-compact-add{width:100%;min-height:58px!important;height:58px!important;margin:14px 0 0!important;padding:0 14px!important;border:0!important;font-size:12px!important;letter-spacing:.06em!important;transition:background-color .16s ease,color .16s ease!important;text-transform:uppercase}
.plp-compact-add.is-ready:not(:disabled){background:#1d1d1f!important;color:#fff!important;cursor:pointer!important}
.plp-compact-add.is-disabled,.plp-compact-add:disabled{background:#aeb1b2!important;color:#fff!important;cursor:not-allowed!important;opacity:1!important}
.plp-reference-availability{display:flex;align-items:center;gap:10px;align-self:flex-start;margin:21px 0 0;border:0;background:transparent;padding:0;font:inherit;color:#2f2f2f;cursor:pointer}
.plp-reference-availability svg{width:18px;height:18px}
.plp-reference-availability span{font-size:11px;text-decoration:underline;text-underline-offset:2px}
@media(max-width:700px){
  .plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0 3px!important}
  .plp-flow .plp-compact-modal{width:calc(100vw - 6px)!important;max-height:92vh!important;border-bottom:0!important}
  .plp-reference-media>img{aspect-ratio:1.72/1!important}
  .plp-reference-body{padding:29px 30px calc(24px + env(safe-area-inset-bottom))!important}
  .plp-reference-body h2{font-size:18px!important;margin-bottom:10px!important}
  .plp-reference-price{gap:11px!important;margin-bottom:12px!important}
  .plp-reference-price strong{font-size:15px!important}
  .plp-reference-price del{font-size:12px!important}
  .plp-reference-price span{font-size:11px!important;padding:5px 8px!important}
  .plp-reference-color{margin-bottom:22px!important}
  .plp-reference-note{font-size:11px!important;margin-bottom:18px!important}
  .plp-compact-field{margin-top:23px!important}
  .plp-compact-size-head button{font-size:10px!important}
  .plp-compact-sizes button,.plp-compact-static-size{min-height:51px!important;padding:0 10px!important}
  .plp-compact-sizes button span,.plp-compact-static-size strong{font-size:13px!important}
  .plp-compact-sizes button b,.plp-compact-static-size b{font-size:12px!important}
  .plp-compact-add{height:56px!important;min-height:56px!important;font-size:11px!important}
}
@media(max-width:430px){
  .plp-reference-body{padding:24px 22px calc(20px + env(safe-area-inset-bottom))!important}
  .plp-reference-body h2{font-size:16px!important}
  .plp-reference-media>img{aspect-ratio:1.55/1!important}
  .plp-compact-swatches button,.plp-reference-one-swatch{width:24px!important;height:24px!important}
  .plp-compact-size-head{padding-left:1px!important;padding-right:1px!important}
}
/* END_COMPACT_PLP_QUICK_ADD_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Applied PLP quick-add drawer matching the provided reference with scrollable product photos")
