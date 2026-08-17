from pathlib import Path

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global page
    if old in page:
        page = page.replace(old, new, 1)
    elif new not in page:
        raise SystemExit(f"{label} not found")


# PDP: show the first available SKU as the reference SKU until a size is selected,
# display 'от' only while a multi-size product has no selected size, and align copy.
replace_once(
    '  const specs=sku??mediaSku??product.skus?.[0];\n  const needsSize=Boolean(sizes.length&&!selectedSize);',
    '  const specs=sku??mediaSku??product.skus?.[0];\n  const displaySku=sku??mediaSku;\n  const needsSize=Boolean(sizes.length&&!selectedSize);',
    'PDP display SKU logic',
)

replace_once(
    '<div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{fmt(unitPrice)}</strong>',
    '<div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)}</strong>',
    'PDP price label',
)

replace_once(
    '<small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}{sku&&<> · SKU: {sku.id}</>}</small>',
    '<small className="pdp-code">АРТИКУЛ: {displaySku?.article??product.article??`KD-PD-${1020+product.id}`}{displaySku&&<> · SKU: {displaySku.id}</>}</small>',
    'PDP article and SKU line',
)

replace_once(
    '<label>Размер <button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Размерная сетка</button></label>',
    '<label className="pdp-size-head"><span>РАЗМЕР</span><button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button></label>',
    'PDP size heading',
)

# Quick add opened from PLP / product rails.
replace_once(
    '<div className="modal-price"><b>{fmt(product.price)}</b>',
    '<div className="modal-price"><b>{sizes.length>1?`от ${fmt(sizes[0]?.[1]??product.price)}`:fmt(sizes[0]?.[1]??product.price)}</b>',
    'Quick-add starting price',
)

replace_once(
    '<p>Цвет: <b>{product.selectedColor ?? product.colorVariants?.[0]?.name}</b></p>',
    '<p className="quick-color">Цвет: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>',
    'Quick-add color line',
)

replace_once(
    '<button className="quick-info-link" onClick={()=>setInfoOpen(true)}>ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ <Icon name="chevron"/></button>',
    '<button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button>',
    'Quick-add product info label',
)

replace_once(
    '<div className="sheet-head"><span>Размер и количество</span><button onClick={()=>setInfoOpen(true)}>Размерная сетка</button></div>',
    '<div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div>',
    'Quick-add size heading',
)

# Legacy mobile size sheet uses the same vocabulary as PDP/quick-add.
replace_once(
    '<div className="sheet-head"><span>Размер и количество</span><button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button></div>',
    '<div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Руководство по размерам</button></div>',
    'Mobile size-sheet heading',
)

# Any product card quick-add (home, catalog, editorial, PDP recommendations, recently viewed)
# should open the same add-to-cart modal instead of navigating to PDP.
replace_once(
    'function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {',
    'function EditorialView({ editorial, selectProduct, quickAdd, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; quickAdd:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {',
    'Editorial quick-add signature',
)

replace_once(
    'function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; selectProduct:(p:Product)=>void; recentlyViewed:number[] }) {',
    'function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, quickAdd, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; selectProduct:(p:Product)=>void; quickAdd:(p:Product)=>void; recentlyViewed:number[] }) {',
    'PDP quick-add signature',
)

replace_once(
    '<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>',
    '<ProductRecommendations product={product} selectProduct={selectProduct} quickAdd={quickAdd} favorite={favorite} recentlyViewed={recentlyViewed}/>',
    'PDP recommendation quick-add prop',
)

replace_once(
    'function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){',
    'function ProductRecommendations({product,selectProduct,quickAdd,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;quickAdd:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){',
    'Recommendations quick-add signature',
)

# There are three intentional ProductRail quick handlers that previously navigated to PDP:
# editorial products, category recommendations, and recently viewed.
page = page.replace('onQuick={selectProduct}', 'onQuick={quickAdd}')

replace_once(
    '<EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />',
    '<EditorialView editorial={editorial} selectProduct={openProduct} quickAdd={setPlpSize} favorite={favorite} favorites={favorites} />',
    'Root editorial quick-add prop',
)

replace_once(
    '<ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} recentlyViewed={recentlyViewed} />',
    '<ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} quickAdd={setPlpSize} recentlyViewed={recentlyViewed} />',
    'Root PDP quick-add prop',
)

marker = "/* PRODUCT UI REFERENCE ALIGNMENT V3 */"
if marker not in css:
    css += r'''

/* PRODUCT UI REFERENCE ALIGNMENT V3 */
.product-page .pdp-description{
  border:0!important;
  padding:0!important;
  margin:24px 0 27px!important;
  min-height:0!important;
  color:#555;
  line-height:1.58!important;
}
.product-page .pdp-size-head,
.plp-modal-info .sheet-head,
.size-sheet .sheet-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:18px;
}
.product-page .pdp-size-head>span,
.plp-modal-info .sheet-head>span,
.size-sheet .sheet-head>span{
  font-size:9px;
  letter-spacing:.04em;
}
.product-page .pdp-size-head button,
.plp-modal-info .sheet-head button,
.size-sheet .sheet-head button{
  text-transform:none!important;
  text-decoration:underline;
  text-underline-offset:3px;
  font-size:10px;
  letter-spacing:0;
}
.product-page .quantity-sizes,
.plp-modal-info .quantity-sizes,
.size-sheet .quantity-sizes{
  border:0!important;
  border-top:1px solid #c9c9c4!important;
  border-bottom:1px solid #c9c9c4!important;
}
.product-page .quantity-sizes .size-row,
.plp-modal-info .quantity-sizes .size-row,
.size-sheet .quantity-sizes .size-row{
  border-bottom:1px solid #e2e2dd!important;
  box-shadow:none!important;
  background:transparent!important;
}
.product-page .quantity-sizes .size-row:last-child,
.plp-modal-info .quantity-sizes .size-row:last-child,
.size-sheet .quantity-sizes .size-row:last-child{
  border-bottom:0!important;
}
.product-page .quantity-sizes .size-row.active,
.plp-modal-info .quantity-sizes .size-row.active,
.size-sheet .quantity-sizes .size-row.active{
  box-shadow:none!important;
  background:transparent!important;
}
.product-page .quantity-control,
.plp-modal-info .quantity-control,
.size-sheet .quantity-control{
  border:0!important;
  background:transparent!important;
}
.product-page .pdp-code{color:#8d8d88!important}
.product-page .pdp-price strong{color:#242625}
.product-page .pdp-color-label{margin-bottom:9px!important}
.product-page .purchase-cta{border:0!important}
.product-page .stores{border:0!important}

.quick-info-link{
  min-height:46px;
  padding:0!important;
  border-top:0!important;
  border-bottom:1px solid #d0d0cb!important;
  text-decoration:none!important;
}
.quick-info-link span{text-decoration:underline;text-underline-offset:3px}
.quick-color{font-weight:400!important;letter-spacing:.01em!important}
.plp-modal-info .sheet-head{margin:28px 0 8px!important}
.plp-modal-info .modal-note{text-transform:uppercase;letter-spacing:.02em}
.plp-modal-info .quantity-sizes .size-row>button{font-weight:400}
.plp-modal-info .quantity-control button,
.product-page .quantity-control button,
.size-sheet .quantity-control button{border:0!important}

@media(min-width:901px){
  .product-page .pdp-grid{
    grid-template-columns:74px minmax(610px,1.52fr) minmax(430px,.78fr)!important;
    max-width:1720px!important;
    gap:16px!important;
  }
  .product-page .pdp-grid.without-thumbs{
    grid-template-columns:minmax(680px,1.55fr) minmax(430px,.76fr)!important;
  }
  .product-page .pdp-info{
    padding:12px 24px 0 36px!important;
    max-height:none!important;
    overflow:visible!important;
  }
  .product-page .pdp-title{margin-top:0!important}
  .product-page .pdp-title h1{font-size:27px!important;line-height:1.06!important;max-width:380px!important}
  .product-page .pdp-price{margin:17px 0 9px!important}
  .product-page .pdp-price strong{font-size:21px!important}
  .product-page .pdp-code{margin-bottom:22px!important;font-size:8px!important}
  .product-page .product-swatches{gap:10px;margin-bottom:23px!important}
  .product-page .product-swatches button{width:30px!important;height:30px!important}
  .product-page .pdp-size-head{margin:0 0 9px!important}
  .product-page .quantity-sizes .size-row{min-height:48px!important;padding:0 12px!important}
  .product-page .quantity-sizes .size-row>button{font-size:12px!important;padding:14px 0!important}
  .product-page .purchase-cta{min-height:51px!important;margin-top:10px!important;font-size:11px!important}
  .product-page .stores{padding:19px 0!important;font-size:10px!important}
  .product-page .pdp-accordions{margin-top:4px!important}
  .product-page .pdp-accordion-trigger{min-height:51px!important;font-size:10px!important}
  .product-page .pdp-accordion-panel{font-size:11px!important;padding-bottom:17px!important}

  .plp-flow .plp-modal{
    width:min(900px,75vw)!important;
    height:100%!important;
    max-height:none!important;
    margin-left:auto!important;
    display:flex!important;
    flex-direction:column!important;
    overflow:auto!important;
  }
  .plp-flow .plp-modal>.close{
    position:fixed!important;
    right:28px!important;
    top:25px!important;
    width:50px!important;
    height:50px!important;
    border-radius:50%!important;
    background:#fff!important;
    display:grid!important;
    place-items:center!important;
  }
  .plp-flow .plp-modal>.close svg{width:25px!important;height:25px!important}
  .plp-modal-media{height:52vh!important;flex:0 0 52vh!important;min-height:430px!important;background:#f4f2ee!important}
  .plp-modal-media .product-media-scroll{height:100%!important}
  .plp-modal-media .product-media-scroll img{height:100%!important;object-fit:contain!important;background:#f4f2ee}
  .plp-modal-info{padding:48px clamp(48px,6vw,76px) 42px!important}
  .plp-modal-info h2{font-size:29px!important;line-height:1.1!important;margin:7px 0 9px!important}
  .plp-modal-info .modal-note{font-size:11px!important;margin-bottom:17px!important}
  .plp-modal-info .modal-price{margin:19px 0 22px!important}
  .plp-modal-info .modal-price b{font-size:24px!important;color:#202321!important}
  .plp-modal-info>p.quick-color{font-size:11px!important;margin:0 0 24px!important}
  .plp-modal-info .quick-description{font-size:12px!important;line-height:1.65!important;margin:0 0 25px!important;max-width:650px}
  .plp-modal-info .quick-info-link{font-size:11px!important;letter-spacing:.07em!important}
  .plp-modal-info .sheet-head>span{font-size:10px!important}
  .plp-modal-info .sheet-head button{font-size:10px!important}
  .plp-modal-info .quantity-sizes .size-row{min-height:61px!important;padding:0 14px!important}
  .plp-modal-info .quantity-sizes .size-row>button{font-size:15px!important;padding:17px 0!important}
  .plp-modal-info .quantity-sizes .size-row>button b{font-size:13px!important}
  .plp-modal-info .quantity-control span{font-size:14px!important;min-width:28px!important}
  .plp-modal-info .quantity-control button{width:33px!important;height:34px!important}
  .plp-modal-info .primary{min-height:61px!important;margin-top:21px!important;padding:16px 22px!important;font-size:13px!important}
  .plp-modal-info .stores{padding:23px 0 0!important;font-size:11px!important}
}

@media(max-width:900px){
  .product-page .pdp-description{margin:18px 0 22px!important}
  .product-page .pdp-size-head{margin:0 0 8px!important}
  .product-page .pdp-size-head button{font-size:9px!important}
  .product-page .quantity-sizes .size-row{min-height:49px!important;padding:0 8px!important}
  .product-page .quantity-sizes .size-row>button{font-size:10px!important}
  .product-page .purchase-cta{margin-top:10px!important}
  .plp-modal-info .quick-info-link{font-size:9px!important}
  .plp-modal-info .sheet-head>span{font-size:9px!important}
  .plp-modal-info .sheet-head button{font-size:9px!important}
  .plp-modal-info .quantity-sizes{border-left:0!important;border-right:0!important}
  .size-sheet .sheet-head>span{font-size:9px!important}
  .size-sheet .sheet-head button{font-size:9px!important}
}
'''

page_path.write_text(page, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")
print("Aligned PDP, quick-add modal, product rail quick actions, labels, spacing, and borders to the supplied reference screens")
