from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")
CSS = Path("app/globals.css")

# ---------- catalog-data.ts ----------
catalog = CATALOG.read_text(encoding="utf-8")

if "available?:boolean;" not in catalog:
    catalog = catalog.replace("  gallery:string[];\n};", "  gallery:string[];\n  available?:boolean;\n};", 1)

if '"Льняной":"#d2c1aa"' not in catalog:
    catalog = catalog.replace('  "Пудровый":"#e6bca8",\n};', '  "Пудровый":"#e6bca8",\n  "Льняной":"#d2c1aa",\n  "Небесный":"#9fb2c6",\n};', 1)

if '"Льняной":"LINEN"' not in catalog:
    catalog = catalog.replace('  "Пудровый":"POWDER",\n};', '  "Пудровый":"POWDER",\n  "Льняной":"LINEN",\n  "Небесный":"SKY",\n};', 1)

if 'makeProduct(2,"KD-PD-1022"' not in catalog:
    product_1022 = r'''  makeProduct(2,"KD-PD-1022","Пододеяльник из сатина","сатин, 140×220 / 200×220 / 220×240 см",18990,[
    {color:"Белый",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-product-bed.png",gallery:["/kd/images/classic-bedroom.png"]},
    {color:"Белый",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-product-bed.png",gallery:["/kd/images/classic-bedroom.png"]},
    {color:"Белый",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-product-bed.png",gallery:["/kd/images/classic-bedroom.png"],available:false},
    {color:"Льняной",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/beige-bedroom.png",gallery:["/kd/images/classic-bedroom.png"]},
    {color:"Льняной",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/beige-bedroom.png",gallery:["/kd/images/classic-bedroom.png"]},
    {color:"Льняной",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/beige-bedroom.png",gallery:["/kd/images/classic-bedroom.png"],available:false},
    {color:"Небесный",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/blue-bedroom.png",gallery:["/kd/images/blue-bedding-vertical.png"]},
    {color:"Небесный",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/blue-bedroom.png",gallery:["/kd/images/blue-bedding-vertical.png"]},
    {color:"Небесный",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/blue-bedroom.png",gallery:["/kd/images/blue-bedding-vertical.png"],available:false},
    {color:"Пудровый",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png"]},
    {color:"Пудровый",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png"]},
    {color:"Пудровый",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png"],available:false},
    {color:"Ночной синий",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-collection-night.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-collection-night.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/kd/images/zip-collection-night.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"],available:false},
  ]),

'''
    anchor = "const productList:CatalogProductOverride[] = [\n"
    if anchor not in catalog:
        raise SystemExit("catalog productList anchor not found")
    catalog = catalog.replace(anchor, anchor + product_1022, 1)

CATALOG.write_text(catalog, encoding="utf-8")

# ---------- page.tsx ----------
page = PAGE.read_text(encoding="utf-8")

if "REMOVED_PRODUCT_IDS" not in page:
    page = page.replace(
        "const products: Product[] = baseProducts.map(base=>{",
        "const REMOVED_PRODUCT_IDS = new Set([1,9]);\nconst products: Product[] = baseProducts.map(base=>{",
        1,
    )

if ").filter(product=>!REMOVED_PRODUCT_IDS.has(product.id));" not in page:
    pattern = r'(const REMOVED_PRODUCT_IDS = new Set\(\[1,9\]\);\nconst products: Product\[\] = baseProducts\.map\(base=>\{[\s\S]*?\n\}\);)'
    match = re.search(pattern, page)
    if not match:
        raise SystemExit("products map block not found")
    block = match.group(1)
    block = block[:-3] + '}).filter(product=>!REMOVED_PRODUCT_IDS.has(product.id));'
    page = page[:match.start()] + block + page[match.end():]

if "function isProductSizeAvailable(" not in page:
    anchor = '''function getProductSizeOptions(product:Product,color?:string){
  if(product.skus?.length){
    const rows=product.skus.filter(item=>!color||item.color===color);
    return Array.from(new Map(rows.map(item=>[item.size,[item.size,item.price] as const])).values());
  }
  return [["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
}
'''
    helper = anchor + '''function isProductSizeAvailable(product:Product,color:string|undefined,size:string){
  const rows=product.skus?.filter(item=>(!color||item.color===color)&&item.size===size);
  if(!rows?.length)return true;
  return rows.some(item=>item.available!==false);
}
function getUnavailableProductSizes(product:Product,color:string|undefined,sizes:readonly (readonly [string,number])[]){
  return sizes.filter(([name])=>!isProductSizeAvailable(product,color,name)).map(([name])=>name);
}
'''
    if anchor not in page:
        raise SystemExit("getProductSizeOptions block not found")
    page = page.replace(anchor, helper, 1)

product_size_rows = r'''function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableLast=true,unavailableSizes=[],oldPrice}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableLast?:boolean;unavailableSizes?:string[];oldPrice?:number}){
  const [notifySize,setNotifySize]=useState("");
  const [notifyEmail,setNotifyEmail]=useState("");
  const submitNotify=(event:React.FormEvent<HTMLFormElement>,name:string)=>{
    event.preventDefault();
    if(!notifyEmail.trim())return;
    notify(name);
    setNotifySize("");
    setNotifyEmail("");
  };
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{
    const unavailable=unavailableSizes.includes(name)||(unavailableLast&&index===sizes.length-1);
    return <div key={name} className={`size-row ${selectedSize===name&&!unavailable?"active":""} ${unavailable?"unavailable":""}`}>
      <button disabled={unavailable} onClick={()=>{if(!unavailable){setSelectedSize(name);setQuantity(1)}}}><span>{name}</span>{selectedSize!==name&&!unavailable&&<b><span>{fmt(price)}</span>{oldPrice&&oldPrice>price&&<del>{fmt(oldPrice)}</del>}</b>}</button>
      {unavailable?<div className="stock-actions"><span>НЕТ В НАЛИЧИИ</span><button type="button" onClick={()=>setNotifySize(current=>current===name?"":name)} aria-label={`Сообщить о поступлении размера ${name}`}><Icon name="mail"/></button></div>:selectedSize===name?<QuantityControl quantity={quantity} setQuantity={setQuantity}/>:null}
      {unavailable&&notifySize===name&&<form className="stock-notify-form" onSubmit={(event)=>submitNotify(event,name)}><label htmlFor={`stock-email-${name}`}>Сообщить о поступлении</label><div><input id={`stock-email-${name}`} type="email" required placeholder="Ваш email" value={notifyEmail} onChange={event=>setNotifyEmail(event.target.value)}/><button type="submit">СООБЩИТЬ</button></div></form>}
    </div>;
  })}</div>;
}'''
page, count = re.subn(r'function ProductSizeRows\([\s\S]*?\n}\n\nfunction ProductView', product_size_rows + '\n\nfunction ProductView', page, count=1)
if count != 1:
    raise SystemExit("ProductSizeRows boundaries not found")

# PDP: use explicit SKU availability, auto-select only a single available size, disable CTA until a variant is chosen.
page = page.replace(
    '  const sizes=getProductSizeOptions(product,color.name);\n  const sku=selectedSize?findProductSku(product,color.name,selectedSize):undefined;',
    '  const sizes=getProductSizeOptions(product,color.name);\n  const unavailableSizes=getUnavailableProductSizes(product,color.name,sizes);\n  const autoSize=sizes.length===1&&isProductSizeAvailable(product,color.name,sizes[0][0])?sizes[0][0]:"";\n  const effectiveSelectedSize=selectedSize||autoSize;\n  const sku=effectiveSelectedSize?findProductSku(product,color.name,effectiveSelectedSize):undefined;',
    1,
)
page = page.replace(
    '  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};',
    '  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize:effectiveSelectedSize,selectedSkuId:sku?.id,quantity};',
    1,
)
page = page.replace(
    '  const needsSize=Boolean(sizes.length&&!selectedSize);\n  const handlePurchase=()=>{if(needsSize){setSizePrompt(true);return}add(selectedProduct)};',
    '  const needsSize=Boolean(sizes.length&&!effectiveSelectedSize);\n  const selectedUnavailable=Boolean(effectiveSelectedSize&&!isProductSizeAvailable(product,color.name,effectiveSelectedSize));\n  const handlePurchase=()=>{if(needsSize||selectedUnavailable)return;add(selectedProduct)};',
    1,
)
page = page.replace(
    '<ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
    '<ProductSizeRows sizes={sizes} selectedSize={effectiveSelectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/>',
    1,
)
page = page.replace(
    '<button className={`primary purchase-cta total-cta ${needsSize?"needs-size":"ready-to-add"} ${sizePrompt&&needsSize?"choose-size-state":""}`} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{needsSize?(sizePrompt?"ВЫБЕРИТЕ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"):"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&<b>{fmt(unitPrice*quantity)}</b>}</button>',
    '<button className={`primary purchase-cta total-cta ${needsSize||selectedUnavailable?"needs-size":"ready-to-add"}`} disabled={needsSize||selectedUnavailable} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{selectedUnavailable?"НЕТ В НАЛИЧИИ":needsSize?"ВЫБРАТЬ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&!selectedUnavailable&&<b>{fmt(unitPrice*quantity)}</b>}</button>',
    1,
)

plp_flow = r'''function PLPSizeFlow({ product, close, add }: { product:Product; close:()=>void; add:(size:string,quantity:number,unitPrice:number)=>void }) {
  const selectedColor=product.selectedColor??product.colorVariants?.[0]?.name;
  const sizes=getProductSizeOptions(product,selectedColor);
  const unavailableSizes=getUnavailableProductSizes(product,selectedColor,sizes);
  const initialSize=sizes.length===1&&isProductSizeAvailable(product,selectedColor,sizes[0][0])?sizes[0][0]:"";
  const [chosenSize,setChosenSize]=useState(initialSize);
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  useEffect(()=>{setChosenSize(initialSize);setQuantity(1)},[product.id,selectedColor,initialSize]);
  const selectedSku=chosenSize?findProductSku(product,selectedColor,chosenSize):undefined;
  const unitPrice=selectedSku?.price??sizes.find(([item])=>item===chosenSize)?.[1]??sizes[0]?.[1]??product.price;
  const discount=discountOf(product);
  const canAdd=Boolean(chosenSize)&&isProductSizeAvailable(product,selectedColor,chosenSize);
  return <div className="overlay plp-flow"><button className="overlay-bg" onClick={close} aria-label="Закрыть выбор размера"/><section className="plp-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}><div className="flow-handle"/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="plp-modal-media"><ScrollableProductMedia product={product} alt={product.name}/></div><div className="plp-modal-info"><small>{product.badge||"КУЛЬТУРА ДОМА"}</small><h2>{product.name}</h2><p className="modal-note">{product.note}</p><div className="modal-price"><b>{sizes.length>1&&!chosenSize?`от ${fmt(sizes[0]?.[1]??product.price)}`:fmt(unitPrice)}</b>{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</div><p className="quick-color">Цвет: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p><p className="quick-description">Предмет создан в русской декоративной традиции: ясная форма, благородный цвет и точная отделка.</p><button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/><button className={`primary total-cta ${canAdd?"ready-to-add":"choose-size-disabled"}`} disabled={!canAdd} onClick={()=>canAdd&&add(chosenSize,quantity,unitPrice)}><span>{canAdd?"ДОБАВИТЬ В КОРЗИНУ":"ВЫБРАТЬ РАЗМЕР"}</span>{canAdd&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>
}'''
page, count = re.subn(r'function PLPSizeFlow\([\s\S]*?\n}\n\nfunction ProductInfoDrawer', plp_flow + '\n\nfunction ProductInfoDrawer', page, count=1)
if count != 1:
    raise SystemExit("PLPSizeFlow boundaries not found")

for marker in [
    'const REMOVED_PRODUCT_IDS = new Set([1,9]);',
    'function isProductSizeAvailable(',
    'stock-notify-form',
    'ВЫБРАТЬ РАЗМЕР',
    'unavailableSizes={unavailableSizes}',
]:
    if marker not in page:
        raise SystemExit(f"page marker missing: {marker}")

PAGE.write_text(page, encoding="utf-8")

# ---------- globals.css ----------
css = CSS.read_text(encoding="utf-8")
marker = "/* PRODUCT_CATALOG_RULES_V1 */"
if marker not in css:
    css += r'''

/* PRODUCT_CATALOG_RULES_V1 */
.product-page .purchase-cta:disabled,
.plp-modal-info .total-cta:disabled{
  background:#d8d8d4!important;
  color:#888984!important;
  opacity:1!important;
  cursor:not-allowed!important;
}
.quantity-sizes .size-row>button>b{
  display:flex;
  align-items:baseline;
  gap:8px;
}
.quantity-sizes .size-row>button>b del{
  color:#aaa;
  font-size:.86em;
  font-weight:400;
}
.quantity-sizes .size-row.unavailable{
  position:relative;
  background:#f3f3f1!important;
  color:#9b9b96!important;
}
.quantity-sizes .size-row.unavailable>button{
  text-decoration:none!important;
  cursor:not-allowed!important;
}
.stock-actions{
  display:flex;
  align-items:center;
  gap:4px;
  margin-left:auto;
}
.stock-actions>span{
  font-size:8px;
  letter-spacing:.06em;
  color:#8e8e89;
  white-space:nowrap;
}
.stock-actions>button{
  width:36px!important;
  height:36px!important;
  padding:9px!important;
  border-left:1px solid #c9c9c5!important;
  display:grid!important;
  place-items:center!important;
}
.stock-actions>button svg{width:17px!important;height:17px!important}
.stock-notify-form{
  grid-column:1/-1;
  width:100%;
  padding:0 0 12px;
}
.stock-notify-form label{
  display:block;
  margin:2px 0 8px;
  font-size:8px;
  letter-spacing:.07em;
  color:#777;
  text-transform:uppercase;
}
.stock-notify-form>div{
  display:grid;
  grid-template-columns:minmax(0,1fr) auto;
  gap:8px;
}
.stock-notify-form input{
  min-width:0;
  height:40px;
  border:1px solid #c9c9c5;
  background:#fff;
  padding:0 11px;
  font-size:11px;
}
.stock-notify-form button{
  height:40px!important;
  width:auto!important;
  border:1px solid #2f4548!important;
  background:#2f4548!important;
  color:#fff!important;
  padding:0 14px!important;
  font-size:8px!important;
  letter-spacing:.07em;
}

/* Product media must always fill its allocated card area; no letterboxing / grey bands. */
.product-image .product-media-scroll{
  width:100%;
  aspect-ratio:1/1.08;
  overflow:hidden;
}
.product-image .product-media-scroll>img{
  width:100%!important;
  height:100%!important;
  flex:0 0 100%!important;
  object-fit:cover!important;
  background:transparent!important;
}
.plp-modal-media .product-media-scroll,
.plp-modal-media .product-media-scroll>img{
  width:100%!important;
  height:100%!important;
}
.plp-modal-media .product-media-scroll>img,
.search-item-media>img,
.favorite-item-media>img,
.added-product-media>img,
.cart-item-media>img,
.checkout-item-media>img,
.recent-item-media>img{
  object-fit:cover!important;
  background:transparent!important;
}
@media(max-width:900px){
  .stock-actions>span{font-size:7px}
  .stock-notify-form>div{grid-template-columns:1fr}
  .stock-notify-form button{width:100%!important}
}
'''
CSS.write_text(css, encoding="utf-8")

print("Applied product removals, KD-PD-1022 SKU model, unified size flow, stock notification and media cover rules")
