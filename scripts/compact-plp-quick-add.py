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
  const needsSize=sizes.length>1&&!chosenSize;
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
          {sizes.length>1?<select value={chosenSize} onChange={event=>setChosenSize(event.target.value)} aria-label="Выберите размер"><option value="" disabled>Выберите размер</option>{sizes.map(([name])=><option key={name} value={name}>{name}</option>)}</select>:<strong>{sizes[0]?.[0]??product.selectedSize??"Единый размер"}</strong>}
        </div>
        <button className="primary plp-compact-add" type="button" disabled={needsSize} onClick={()=>add(chosenSize,color.name,unitPrice)}>{needsSize?"ВЫБЕРИТЕ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</button>
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
.plp-flow.plp-compact-flow{align-items:center!important;justify-content:center!important;padding:20px!important}
.plp-flow.plp-compact-flow .overlay-bg{background:rgba(0,0,0,.44)!important}
.plp-flow .plp-compact-modal{
  position:relative!important;
  width:min(420px,calc(100vw - 40px))!important;
  height:auto!important;
  max-height:none!important;
  display:grid!important;
  grid-template-columns:152px minmax(0,1fr)!important;
  overflow:hidden!important;
  margin:0!important;
  background:#fff!important;
  border-radius:2px!important;
  box-shadow:0 18px 55px rgba(0,0,0,.22)!important;
  animation:none!important;
}
.plp-flow .plp-compact-modal>.close{
  position:absolute!important;
  top:10px!important;
  right:10px!important;
  width:28px!important;
  height:28px!important;
  display:grid!important;
  place-items:center!important;
  margin:0!important;
  padding:0!important;
  border:0!important;
  border-radius:50%!important;
  background:rgba(255,255,255,.92)!important;
  z-index:3!important;
}
.plp-flow .plp-compact-modal>.close svg{width:16px!important;height:16px!important}
.plp-compact-media{min-height:230px;background:#f3f3f1;overflow:hidden}
.plp-compact-media img{width:100%;height:100%;min-height:230px;display:block;object-fit:cover}
.plp-compact-controls{display:flex;flex-direction:column;justify-content:center;gap:18px;padding:34px 24px 22px}
.plp-compact-field{display:flex;flex-direction:column;align-items:flex-start;gap:8px;min-width:0}
.plp-compact-field>span{font-size:9px;line-height:1;letter-spacing:.09em;text-transform:uppercase;color:#777}
.plp-compact-field>strong,.plp-compact-field>small{font-size:11px;line-height:1.35;font-weight:400;color:#1d1d1f}
.plp-compact-swatches{display:flex;align-items:center;gap:8px}
.plp-compact-swatches button{width:20px;height:20px;border:1px solid #d8d8d8;border-radius:50%;padding:0;cursor:pointer;box-shadow:0 0 0 2px #fff}
.plp-compact-swatches button.active{outline:1px solid #1d1d1f;outline-offset:2px}
.plp-compact-field select{width:100%;height:38px;border:1px solid #d9d9d9;border-radius:0;background:#fff;padding:0 30px 0 10px;font:inherit;font-size:10px;color:#1d1d1f;outline:none}
.plp-compact-field select:focus{border-color:#1d1d1f}
.plp-compact-add{width:100%;min-height:42px!important;height:42px!important;margin:2px 0 0!important;padding:0 12px!important;border:0!important;background:#1d1d1f!important;color:#fff!important;font-size:9px!important;letter-spacing:.08em!important}
.plp-compact-add:disabled{background:#c9ccd1!important;color:#fff!important;cursor:not-allowed!important}
@media(max-width:700px){
  .plp-flow.plp-compact-flow{align-items:flex-end!important;justify-content:center!important;padding:0!important}
  .plp-flow .plp-compact-modal{width:100%!important;grid-template-columns:126px minmax(0,1fr)!important;border-radius:12px 12px 0 0!important}
  .plp-compact-media,.plp-compact-media img{min-height:218px!important}
  .plp-compact-controls{gap:14px;padding:28px 18px 18px!important}
  .plp-compact-field select{height:36px!important;font-size:10px!important}
  .plp-compact-add{height:42px!important;min-height:42px!important}
}
/* END_COMPACT_PLP_QUICK_ADD_V1 */
'''
css_path.write_text(css, encoding="utf-8")
print("Applied compact PLP quick-add modal")
