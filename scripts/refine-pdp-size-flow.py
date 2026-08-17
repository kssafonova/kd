from pathlib import Path

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

# Characteristics are open by default.
page = page.replace('const [open,setOpen]=useState("");', 'const [open,setOpen]=useState("ХАРАКТЕРИСТИКИ");', 1)

# PDP starts without a selected size. First CTA click asks the user to select it.
page = page.replace(
    'const [selectedSize,setSelectedSize]=useState(product.skus?.[0]?.size??"Евро 200×220");\n  const [quantity,setQuantity]=useState(1);',
    'const [selectedSize,setSelectedSize]=useState("");\n  const [quantity,setQuantity]=useState(1);\n  const [sizePrompt,setSizePrompt]=useState(false);',
    1,
)

old_effect = 'useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);const nextIndex=initial>=0?initial:0;const nextColor=variants[nextIndex]?.name;setColorIndex(nextIndex);setActiveImage(0);setSelectedSize(findProductSku(product,nextColor)?.size??"Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);'
new_effect = 'useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);const nextIndex=initial>=0?initial:0;setColorIndex(nextIndex);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)},[product.id,product.selectedColor]);'
if old_effect in page:
    page = page.replace(old_effect, new_effect, 1)
elif new_effect not in page:
    raise SystemExit("PDP initialization effect not found")

old_logic = '''  const color=variants[colorIndex];
  const sizes=getProductSizeOptions(product,color.name);
  const sku=findProductSku(product,color.name,selectedSize);
  const gallery=sku?[sku.image,...sku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const image=gallery[activeImage]??sku?.image??color.image;
  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image,gallery:sku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};
  const specs=sku??product.skus?.[0];
  const handlePurchase=()=>product.skus?.length?add(selectedProduct):(window.matchMedia("(max-width: 900px)").matches?chooseSize():add(selectedProduct));'''
new_logic = '''  const color=variants[colorIndex];
  const sizes=getProductSizeOptions(product,color.name);
  const sku=selectedSize?findProductSku(product,color.name,selectedSize):undefined;
  const mediaSku=sku??findProductSku(product,color.name);
  const gallery=mediaSku?[mediaSku.image,...mediaSku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const image=gallery[activeImage]??mediaSku?.image??color.image;
  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??sizes[0]?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};
  const specs=sku??mediaSku??product.skus?.[0];
  const needsSize=Boolean(sizes.length&&!selectedSize);
  const handlePurchase=()=>{if(needsSize){setSizePrompt(true);return}add(selectedProduct)};'''
if old_logic in page:
    page = page.replace(old_logic, new_logic, 1)
elif new_logic not in page:
    raise SystemExit("PDP selection logic block not found")

old_color = '''<label>Цвет: {color.name}</label><div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize(findProductSku(product,variant.name)?.size??selectedSize);setQuantity(1)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>'''
new_color = '''<label className="pdp-color-label">Цвет: {color.name}</label>{variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}'''
if old_color in page:
    page = page.replace(old_color, new_color, 1)
elif new_color not in page:
    raise SystemExit("PDP color selector block not found")

old_sizes = '''<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>'''
new_sizes = '''<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>'''
if old_sizes in page:
    page = page.replace(old_sizes, new_sizes, 1)
elif new_sizes not in page:
    raise SystemExit("PDP size rows block not found")

old_cta = '''<button className="primary purchase-cta total-cta" onClick={handlePurchase}><span className="purchase-label desktop-label">ДОБАВИТЬ В КОРЗИНУ</span><span className="purchase-label mobile-label">ВЫБЕРИТЕ РАЗМЕР</span><b>{fmt(unitPrice*quantity)}</b></button>'''
new_cta = '''<button className={`primary purchase-cta total-cta ${needsSize?"needs-size":"ready-to-add"} ${sizePrompt&&needsSize?"choose-size-state":""}`} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{needsSize?(sizePrompt?"ВЫБЕРИТЕ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"):"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&<b>{fmt(unitPrice*quantity)}</b>}</button>'''
if old_cta in page:
    page = page.replace(old_cta, new_cta, 1)
elif new_cta not in page:
    raise SystemExit("PDP CTA block not found")

marker = "/* PDP SIZE-FIRST FLOW V2 */"
if marker not in css:
    css += '''\n\n/* PDP SIZE-FIRST FLOW V2 */
.product-page .pdp-grid{align-items:start}
.product-page .pdp-info{height:auto;align-self:start}
.product-page .purchase-cta{min-height:49px;transition:background .18s ease,color .18s ease,opacity .18s ease;display:flex;align-items:center;justify-content:center;gap:18px}
.product-page .purchase-cta.needs-size{background:#7d8b8d;color:rgba(255,255,255,.94)}
.product-page .purchase-cta.needs-size.choose-size-state{background:#687a7d}
.product-page .purchase-cta.ready-to-add{background:var(--dark);justify-content:space-between}
.product-page .purchase-cta .purchase-label{flex:1;text-align:center;white-space:nowrap}
.product-page .purchase-cta.ready-to-add .purchase-label{text-align:left}
.product-page .purchase-cta b{font-weight:400;white-space:nowrap}
.product-page .quantity-sizes .size-row{transition:background .18s ease,box-shadow .18s ease}
.product-page .quantity-sizes .size-row.active{background:#faf9f6}
.product-page .quantity-sizes .size-row.active>button>b{display:none}
.product-page .pdp-color-label{margin-bottom:8px}
@media(min-width:901px){
  .product-page .pdp-info{max-height:none!important;overflow:visible!important;padding:4px 26px 0 34px}
  .product-page .pdp-description{border-top:0!important;border-bottom:1px solid #d7d7d2!important;padding:0 0 16px!important;margin:16px 0!important;min-height:0}
  .product-page .product-swatches{gap:9px;margin-bottom:15px}
  .product-page .product-swatches button{width:30px!important;height:30px!important}
  .product-page .quantity-sizes{border-left:0;border-right:0}
  .product-page .quantity-sizes .size-row{padding:0 10px;min-height:45px}
  .product-page .quantity-sizes .size-row>button{font-size:10px}
  .product-page .quantity-control{border:0;background:transparent}
  .product-page .quantity-control button{width:28px!important;height:30px!important;padding:6px!important}
}
@media(max-width:900px){
  .product-page .pdp-info>.quantity-sizes{display:block!important}
  .product-page .pdp-info{height:auto;overflow:visible}
  .product-page .pdp-description{border-top:0;border-bottom:1px solid #ddd;padding:0 0 14px;margin:14px 0!important;min-height:0}
  .product-page .product-swatches{gap:9px;margin-bottom:13px}
  .product-page .product-swatches button{width:34px!important;height:34px!important}
  .product-page .purchase-cta{position:static!important;bottom:auto!important;margin-top:12px;min-height:48px}
  .product-page .quantity-sizes{border-left:0;border-right:0}
  .product-page .quantity-sizes .size-row{padding:0 8px}
  .product-page .quantity-sizes .size-row>button{font-size:10px}
  .product-page .quantity-control{border:0;background:transparent}
}
'''

page_path.write_text(page, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")
print("Refined PDP size-first flow, color swatches, open characteristics, and responsive content sizing")
