from pathlib import Path

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
page = page_path.read_text(encoding="utf-8")
css = css_path.read_text(encoding="utf-8")

replacements = [
    (
        'function EditorialView({ editorial, selectProduct, quickAdd, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; quickAdd:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {',
        'function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {'
    ),
    (
        'function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, quickAdd, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; selectProduct:(p:Product)=>void; quickAdd:(p:Product)=>void; recentlyViewed:number[] }) {',
        'function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; selectProduct:(p:Product)=>void; recentlyViewed:number[] }) {'
    ),
    (
        '<ProductRecommendations product={product} selectProduct={selectProduct} quickAdd={quickAdd} favorite={favorite} recentlyViewed={recentlyViewed}/>',
        '<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>'
    ),
    (
        'function ProductRecommendations({product,selectProduct,quickAdd,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;quickAdd:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){',
        'function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){'
    ),
    (
        '<EditorialView editorial={editorial} selectProduct={openProduct} quickAdd={setPlpSize} favorite={favorite} favorites={favorites} />',
        '<EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />'
    ),
    (
        '<ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} quickAdd={setPlpSize} recentlyViewed={recentlyViewed} />',
        '<ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} recentlyViewed={recentlyViewed} />'
    ),
]

for old, new in replacements:
    if old in page:
        page = page.replace(old, new, 1)

# Restore the previous navigation behavior for product-card quick actions inside
# editorial and PDP recommendation rails. PLP/home keep the dedicated quick-add drawer.
page = page.replace('onQuick={quickAdd}', 'onQuick={selectProduct}')

marker = "/* QUICK ADD FLOW ROLLBACK V1 */"
if marker not in css:
    css += r'''

/* QUICK ADD FLOW ROLLBACK V1 */
@media(min-width:901px){
  .plp-flow{align-items:stretch!important;justify-content:flex-end!important;padding:0!important}
  .plp-flow .overlay-bg{background:rgba(0,0,0,.58)!important}
  .plp-flow .plp-modal{
    margin-left:auto!important;
    width:min(560px,43vw)!important;
    height:100%!important;
    max-height:none!important;
    display:flex!important;
    flex-direction:column!important;
    box-shadow:-12px 0 45px #0002!important;
    animation:slideLeft .25s ease!important;
    overflow:auto!important;
  }
  .plp-flow .plp-modal>.close{
    position:fixed!important;
    right:20px!important;
    top:17px!important;
    width:34px!important;
    height:34px!important;
    border-radius:50%!important;
    background:#fff!important;
    display:grid!important;
    place-items:center!important;
  }
  .plp-flow .plp-modal>.close svg{width:22px!important;height:22px!important}
  .plp-flow .plp-modal-media{
    min-height:0!important;
    height:52vh!important;
    flex:0 0 52vh!important;
    background:#f1efea!important;
  }
  .plp-flow .plp-modal-media .product-media-scroll{height:100%!important}
  .plp-flow .plp-modal-media .product-media-scroll img{height:100%!important;object-fit:cover!important;background:#f1efea!important}
  .plp-flow .plp-modal-info{padding:34px 48px 38px!important}
  .plp-flow .plp-modal-info h2{font-size:21px!important;line-height:1.15!important;margin:8px 0!important}
  .plp-flow .plp-modal-info .modal-note{font-size:11px!important}
  .plp-flow .plp-modal-info .modal-price{margin:12px 0 16px!important}
  .plp-flow .plp-modal-info .modal-price b{font-size:18px!important}
  .plp-flow .plp-modal-info>p.quick-color{font-size:10px!important;margin:0 0 16px!important}
  .plp-flow .plp-modal-info .quick-description{font-size:10px!important;line-height:1.6!important;margin:0 0 12px!important}
  .plp-flow .plp-modal-info .quick-info-link{font-size:9px!important}
  .plp-flow .plp-modal-info .sheet-head{margin:20px 0 8px!important}
  .plp-flow .plp-modal-info .sheet-head>span{font-size:10px!important}
  .plp-flow .plp-modal-info .quantity-sizes .size-row{min-height:45px!important;padding:0 12px!important}
  .plp-flow .plp-modal-info .quantity-sizes .size-row>button{font-size:10px!important;padding:14px 0!important}
  .plp-flow .plp-modal-info .primary{min-height:46px!important;padding:14px!important;margin-top:16px!important;font-size:10px!important}
  .plp-flow .plp-modal-info .stores{padding:14px 0 0!important;font-size:9px!important}
}
'''

page_path.write_text(page, encoding="utf-8")
css_path.write_text(css, encoding="utf-8")
print("Restored previous quick-add navigation flow and desktop drawer dimensions")
