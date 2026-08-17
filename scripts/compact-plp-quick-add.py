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

      <div className="plp-compact-top">
        <div className="plp-compact-media"><RemoteImage src={preview} alt={product.name}/></div>
        <div className="plp-compact-color-panel">
          <div className="plp-compact-field color-field">
            <span>Цвет: <b>{color.name}</b></span>
            {variants.length>1?<div className="plp-compact-swatches" role="group" aria-label="Выберите цвет">{variants.map((variant,index)=><button key={variant.name} type="button" className={index===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(index)} aria-label={`Цвет ${variant.name}`} title={variant.name}/>)}</div>:null}
          </div>
        </div>
      </div>

      <div className="plp-compact-bottom">
        <div className="plp-compact-field size-field">
          <div className="plp-compact-size-head"><span>Размер</span></div>
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
.plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0 4px!important}
.plp-flow.plp-compact-flow .overlay-bg{background:rgba(0,0,0,.28)!important}
.plp-flow .plp-compact-modal{
  position:relative!important;
  width:min(760px,calc(100vw - 8px))!important;
  height:auto!important;
  max-height:92vh!important;
  display:flex!important;
  flex-direction:column!important;
  overflow-y:auto!important;
  margin:0!important;
  background:#fff!important;
  border:1px solid #e6e0d8!important;
  border-radius:0!important;
  box-shadow:0 -10px 35px rgba(0,0,0,.10)!important;
  animation:none!important;
}
.plp-flow .plp-compact-modal>.close{
  position:absolute!important;
  top:12px!important;
  right:12px!important;
  width:30px!important;
  height:30px!important;
  display:grid!important;
  place-items:center!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-radius:50%!important;
  background:rgba(255,255,255,.94)!important;
  z-index:5!important;
}
.plp-flow .plp-compact-modal>.close svg{width:17px!important;height:17px!important}
.plp-compact-top{
  display:grid;
  grid-template-columns:minmax(0,56%) minmax(0,44%);
  align-items:stretch;
  min-height:0;
}
.plp-compact-media{min-height:0;aspect-ratio:1.12/1;background:#f3f1ed;overflow:hidden}
.plp-compact-media img{width:100%;height:100%;display:block;object-fit:cover}
.plp-compact-color-panel{display:flex;align-items:center;padding:44px 30px 30px;background:#fff}
.plp-compact-field{display:flex;flex-direction:column;align-items:flex-start;gap:12px;min-width:0;width:100%}
.plp-compact-field>span,.plp-compact-field .plp-compact-size-head span{font-size:11px;line-height:1.2;color:#353535}
.plp-compact-field>span b{font-weight:400;text-transform:lowercase}
.plp-compact-swatches{display:flex;align-items:center;gap:10px;flex-wrap:wrap;min-height:30px}
.plp-compact-swatches button{width:26px;height:26px;border:1px solid #dedede;border-radius:0;padding:0;cursor:pointer;box-shadow:0 0 0 2px #fff}
.plp-compact-swatches button.active{outline:2px solid #1d1d1f;outline-offset:2px}
.plp-compact-bottom{display:flex;flex-direction:column;gap:18px;padding:28px 42px 34px;background:#fff}
.plp-compact-size-head{width:100%;display:flex;align-items:center;justify-content:space-between;padding:0 10px 4px}
.plp-compact-sizes{width:100%;border-top:1px solid #1d1d1f}
.plp-compact-sizes button,.plp-compact-static-size{width:100%;min-height:46px;display:flex;align-items:center;justify-content:space-between;gap:16px;border:0;border-bottom:1px solid #dedede;background:#fff;padding:0 14px;font:inherit;color:#1d1d1f}
.plp-compact-sizes button{cursor:pointer;text-align:left}
.plp-compact-sizes button span,.plp-compact-static-size strong{font-size:13px;font-weight:400}
.plp-compact-sizes button b,.plp-compact-static-size b{font-size:12px;font-weight:400;white-space:nowrap;color:#555}
.plp-compact-sizes button:hover{background:#faf9f7}
.plp-compact-sizes button.active{background:#f5f4f1;box-shadow:inset 2px 0 0 #1d1d1f}
.plp-compact-sizes button.active span{font-weight:500}
.plp-compact-add{width:100%;min-height:50px!important;height:50px!important;margin:2px 0 0!important;padding:0 14px!important;border:0!important;font-size:11px!important;letter-spacing:.02em!important;transition:background-color .16s ease,color .16s ease!important}
.plp-compact-add.is-ready:not(:disabled){background:#1d1d1f!important;color:#fff!important;cursor:pointer!important}
.plp-compact-add.is-disabled,.plp-compact-add:disabled{background:#c9ccd1!important;color:#fff!important;cursor:not-allowed!important;opacity:1!important}
@media(max-width:700px){
  .plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0 3px!important}
  .plp-flow .plp-compact-modal{width:calc(100vw - 6px)!important;max-height:90vh!important;border-bottom:0!important}
  .plp-compact-top{grid-template-columns:minmax(0,56%) minmax(0,44%)!important}
  .plp-compact-media{aspect-ratio:1.08/1!important}
  .plp-compact-color-panel{padding:36px 20px 24px!important;align-items:flex-start!important;justify-content:center!important}
  .plp-compact-field{gap:10px!important}
  .plp-compact-field>span,.plp-compact-field .plp-compact-size-head span{font-size:10px!important}
  .plp-compact-swatches{gap:8px!important}
  .plp-compact-swatches button{width:23px!important;height:23px!important}
  .plp-compact-bottom{gap:14px!important;padding:22px 24px calc(20px + env(safe-area-inset-bottom))!important}
  .plp-compact-size-head{padding:0 8px 3px!important}
  .plp-compact-sizes button,.plp-compact-static-size{min-height:42px!important;padding:0 10px!important}
  .plp-compact-sizes button span,.plp-compact-static-size strong{font-size:12px!important}
  .plp-compact-sizes button b,.plp-compact-static-size b{font-size:11px!important}
  .plp-compact-add{height:48px!important;min-height:48px!important;font-size:10px!important}
}
@media(max-width:430px){
  .plp-compact-top{grid-template-columns:minmax(0,55%) minmax(0,45%)!important}
  .plp-compact-color-panel{padding:34px 14px 20px!important}
  .plp-compact-swatches button{width:21px!important;height:21px!important}
  .plp-compact-bottom{padding:19px 18px calc(18px + env(safe-area-inset-bottom))!important}
}
/* END_COMPACT_PLP_QUICK_ADD_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Applied adaptive reference-style PLP quick-add modal")
