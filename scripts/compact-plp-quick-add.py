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
  const preview=mediaSku?.image??color.image??product.image;

  return <div className="overlay plp-flow plp-compact-flow">
    <button className="overlay-bg" onClick={close} aria-label="Закрыть"/>
    <section className="plp-modal plp-compact-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}>
      <button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button>
      <div className="plp-compact-media"><RemoteImage src={preview} alt={product.name}/></div>
      <div className="plp-compact-controls">
        <div className="plp-compact-field color-field">
          <span>Цвет</span>
          {variants.length>1?<><div className="plp-compact-swatches" role="group" aria-label="Выберите цвет">{variants.map((variant,index)=><button key={variant.name} type="button" className={index===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(index)} aria-label={`Цвет ${variant.name}`} title={variant.name}/>)}</div><small>{color.name}</small></>:<strong>{color.name}</strong>}
        </div>
        <div className="plp-compact-field size-field">
          <span>Размер</span>
          {requiresSizeChoice?<div className="plp-compact-sizes" role="group" aria-label="Выберите размер">{sizes.map(([name,price])=><button key={name} type="button" className={chosenSize===name?"active":""} aria-pressed={chosenSize===name} onClick={()=>setChosenSize(name)}><span>{name}</span><b>{fmt(price)}</b></button>)}</div>:<div className="plp-compact-static-size"><strong>{sizes[0]?.[0]??product.selectedSize??"Единый размер"}</strong><b>{fmt(sizes[0]?.[1]??product.price)}</b></div>}
        </div>
        <button className={`primary plp-compact-add ${canAdd?"is-ready":"is-disabled"}`} type="button" disabled={!canAdd} aria-disabled={!canAdd} onClick={()=>{if(!canAdd)return;add(chosenSize,color.name,unitPrice)}}>{canAdd?`Добавить в корзину · ${fmt(unitPrice)}`:"Выберите размер"}</button>
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
.plp-flow.plp-compact-flow{align-items:center!important;justify-content:center!important;padding:24px!important}
.plp-flow.plp-compact-flow .overlay-bg{background:rgba(0,0,0,.32)!important}
.plp-flow .plp-compact-modal{
  position:relative!important;
  width:min(660px,calc(100vw - 48px))!important;
  height:auto!important;
  max-height:none!important;
  display:grid!important;
  grid-template-columns:minmax(250px,46%) minmax(0,1fr)!important;
  overflow:hidden!important;
  margin:0!important;
  background:#fff!important;
  border:1px solid #e6e0d8!important;
  border-radius:0!important;
  box-shadow:0 18px 55px rgba(0,0,0,.14)!important;
  animation:none!important;
}
.plp-flow .plp-compact-modal>.close{
  position:absolute!important;
  top:13px!important;
  right:13px!important;
  width:30px!important;
  height:30px!important;
  display:grid!important;
  place-items:center!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-radius:50%!important;
  background:rgba(255,255,255,.94)!important;
  z-index:3!important;
}
.plp-flow .plp-compact-modal>.close svg{width:17px!important;height:17px!important}
.plp-compact-media{min-height:340px;background:#f3f1ed;overflow:hidden}
.plp-compact-media img{width:100%;height:100%;min-height:340px;display:block;object-fit:cover}
.plp-compact-controls{display:flex;flex-direction:column;justify-content:center;gap:24px;padding:42px 34px 28px}
.plp-compact-field{display:flex;flex-direction:column;align-items:flex-start;gap:10px;min-width:0}
.plp-compact-field>span{font-size:10px;line-height:1;letter-spacing:.04em;color:#5f5f5f}
.plp-compact-field>strong,.plp-compact-field>small{font-size:12px;line-height:1.35;font-weight:400;color:#1d1d1f}
.plp-compact-swatches{display:flex;align-items:center;gap:10px;min-height:28px}
.plp-compact-swatches button{width:24px;height:24px;border:1px solid #dedede;border-radius:0;padding:0;cursor:pointer;box-shadow:0 0 0 2px #fff}
.plp-compact-swatches button.active{outline:2px solid #1d1d1f;outline-offset:2px}
.plp-compact-sizes{width:100%;border-top:1px solid #dcdcdc}
.plp-compact-sizes button,.plp-compact-static-size{width:100%;min-height:43px;display:flex;align-items:center;justify-content:space-between;gap:16px;border:0;border-bottom:1px solid #dedede;background:#fff;padding:0 10px;font:inherit;color:#1d1d1f}
.plp-compact-sizes button{cursor:pointer;text-align:left}
.plp-compact-sizes button span,.plp-compact-static-size strong{font-size:12px;font-weight:400}
.plp-compact-sizes button b,.plp-compact-static-size b{font-size:11px;font-weight:400;white-space:nowrap;color:#555}
.plp-compact-sizes button:hover{background:#faf9f7}
.plp-compact-sizes button.active{background:#f5f4f1;box-shadow:inset 2px 0 0 #1d1d1f}
.plp-compact-sizes button.active span{font-weight:500}
.plp-compact-add{width:100%;min-height:48px!important;height:48px!important;margin:2px 0 0!important;padding:0 14px!important;border:0!important;font-size:10px!important;letter-spacing:.04em!important;transition:background-color .16s ease,color .16s ease!important}
.plp-compact-add.is-ready:not(:disabled){background:#1d1d1f!important;color:#fff!important;cursor:pointer!important}
.plp-compact-add.is-disabled,.plp-compact-add:disabled{background:#c9ccd1!important;color:#fff!important;cursor:not-allowed!important;opacity:1!important}
@media(max-width:700px){
  .plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0!important}
  .plp-flow .plp-compact-modal{width:100%!important;grid-template-columns:132px minmax(0,1fr)!important;border:0!important;border-top:1px solid #e6e0d8!important;border-radius:0!important}
  .plp-compact-media,.plp-compact-media img{min-height:270px!important}
  .plp-compact-controls{gap:17px;padding:28px 18px 18px!important}
  .plp-compact-swatches button{width:22px;height:22px}
  .plp-compact-sizes button,.plp-compact-static-size{min-height:38px;padding:0 7px}
  .plp-compact-sizes button span,.plp-compact-static-size strong{font-size:10px}
  .plp-compact-sizes button b,.plp-compact-static-size b{font-size:9px}
  .plp-compact-add{height:44px!important;min-height:44px!important;font-size:9px!important}
}
@media(max-width:430px){
  .plp-flow .plp-compact-modal{grid-template-columns:118px minmax(0,1fr)!important}
  .plp-compact-media,.plp-compact-media img{min-height:250px!important}
  .plp-compact-controls{padding:26px 14px 14px!important;gap:14px}
}
/* END_COMPACT_PLP_QUICK_ADD_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Applied reference-style compact PLP quick-add modal")
