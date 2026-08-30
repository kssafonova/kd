from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
CSS = ROOT / "app" / "globals.css"

page = PAGE.read_text(encoding="utf-8")
original_page = page
css = CSS.read_text(encoding="utf-8")
original_css = css

helper_marker = "function isProductSizeAvailable(product:Product,primary:string|undefined,size:string,secondaryColor?:string){"
helper = 'const isUniversalSizeLabel=(value:unknown)=>String(cleanNulls(value)??"").trim().toLocaleLowerCase("ru-RU")==="единый размер";\n'
if helper not in page:
    if helper_marker not in page:
        raise SystemExit("PDP_SIZE_QUANTITY_V110: size helper insertion point not found")
    page = page.replace(helper_marker, helper + helper_marker, 1)

visible_line = "  const visibleSizes=sizes.filter(([name])=>!isUniversalSizeLabel(name));\n"
pdp_sizes_line = "  const sizes=getProductSizeOptions(product,color.name,secondaryColor||undefined);\n"
pdp_context = pdp_sizes_line + visible_line
if pdp_context not in page:
    if pdp_sizes_line not in page:
        raise SystemExit("PDP_SIZE_QUANTITY_V110: PDP sizes line not found")
    page = page.replace(pdp_sizes_line, pdp_context, 1)

plp_sizes_line = "  const sizes=getProductSizeOptions(product,selectedColor);\n"
plp_context = plp_sizes_line + visible_line
if plp_context not in page:
    if plp_sizes_line not in page:
        raise SystemExit("PDP_SIZE_QUANTITY_V110: PLP sizes line not found")
    page = page.replace(plp_sizes_line, plp_context, 1)

pdp_old = '''{sizes.length>1&&<><label className="pdp-size-head"><span>РАЗМЕР</span><button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button></label><ProductSizeRows sizes={sizes} selectedSize={effectiveSelectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}'''
pdp_new = '''{visibleSizes.length>0&&<><label className="pdp-size-head"><span>РАЗМЕР</span>{visibleSizes.length>1&&<button onClick={()=>alert(visibleSizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button>}</label><ProductSizeRows sizes={visibleSizes} selectedSize={effectiveSelectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}{sizes.length===1&&visibleSizes.length===0&&<div className="single-size-quantity"><span>КОЛИЧЕСТВО</span><QuantityControl quantity={quantity} setQuantity={setQuantity}/></div>}'''
if pdp_new not in page:
    if pdp_old not in page:
        raise SystemExit("PDP_SIZE_QUANTITY_V110: PDP size block not found")
    page = page.replace(pdp_old, pdp_new, 1)

plp_old = '''{sizes.length>1&&<><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}'''
plp_new = '''{visibleSizes.length>0&&<><div className="sheet-head"><span>РАЗМЕР</span>{visibleSizes.length>1&&<button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button>}</div><ProductSizeRows sizes={visibleSizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}{sizes.length===1&&visibleSizes.length===0&&<div className="single-size-quantity"><span>КОЛИЧЕСТВО</span><QuantityControl quantity={quantity} setQuantity={setQuantity}/></div>}'''
if plp_new not in page:
    if plp_old not in page:
        raise SystemExit("PDP_SIZE_QUANTITY_V110: PLP size block not found")
    page = page.replace(plp_old, plp_new, 1)

css_marker = "/* PDP_SIZE_QUANTITY_V110 */"
if css_marker not in css:
    css += '''\n\n/* PDP_SIZE_QUANTITY_V110 */\n.single-size-quantity{display:flex;align-items:center;justify-content:space-between;min-height:48px;padding:0 12px;margin-top:8px;border-top:1px solid #ddd;border-bottom:1px solid #ddd;font-size:10px;letter-spacing:.06em}\n.product-page .single-size-quantity{padding:0 10px}\n.plp-modal-info .single-size-quantity{min-height:61px;padding:0 14px;margin-top:8px}\n@media(max-width:900px){.single-size-quantity{min-height:46px;padding:0 8px}.plp-modal-info .single-size-quantity{min-height:46px;padding:0 10px}}\n'''

required = [
    "const isUniversalSizeLabel=",
    'visibleSizes.length>0&&<><label className="pdp-size-head"',
    'visibleSizes.length>0&&<><div className="sheet-head"',
    'className="single-size-quantity"',
    "fmt(unitPrice*quantity)",
]
for marker in required:
    if marker not in page:
        raise SystemExit(f"PDP_SIZE_QUANTITY_V110: required marker missing: {marker}")

if page.count(visible_line) < 2:
    raise SystemExit(f"PDP_SIZE_QUANTITY_V110: expected visibleSizes in PDP and PLP, got {page.count(visible_line)}")
if pdp_old in page or plp_old in page:
    raise SystemExit("PDP_SIZE_QUANTITY_V110: stale multi-size-only block remains")

PAGE.write_text(page, encoding="utf-8")
CSS.write_text(css, encoding="utf-8")
print(
    f"// PDP_SIZE_QUANTITY_V110: single real size is visible and auto-selected with quantity control; "
    f"universal size label hidden; total CTA remains unit price x quantity; "
    f"visibleScopes={page.count(visible_line)}; page_changed={page != original_page}; css_changed={css != original_css}"
)
