from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text()

already_clean = all(marker not in text for marker in [
    "hasBundle?: boolean;",
    "buyBundle",
    "addBundle",
    "added-recommendations",
    '<p className="recommend-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</p>',
    "bundleSelecting",
])
if already_clean:
    print("Bundle purchase and cart upsell flows are already removed")
    raise SystemExit(0)

# Remove the bundle capability from the product model and product data.
text = text.replace("  hasBundle?: boolean;\n", "")
text = text.replace(", hasBundle: true", "")

# Remove the root-level add-many-to-cart handler.
text, count = re.subn(
    r'\n  const addBundle = \(items: Product\[\]\) => \{\n.*?\n  \};',
    "",
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit("addBundle handler was not found")

# Remove bundle props from root render calls.
text = text.replace(" buyBundle={addBundle}", "")

# Editorial pages remain shoppable item-by-item, without selection or buy-all flow.
editorial_start = text.find("function EditorialView(")
editorial_end = text.find("\n\nfunction QuantityControl", editorial_start)
if editorial_start < 0 or editorial_end < 0:
    raise SystemExit("EditorialView boundaries were not found")
editorial = '''function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  return <div className="editorial-page"><section className="editorial-cover"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><p>{editorial.kind}</p><h1>{editorial.name}</h1></div></section><section className="editorial-words"><p>{editorial.lead}</p><span>{editorial.description}</span></section><img className="editorial-detail" src={assetUrl(editorial.images[1])} alt={`Детали ${editorial.name}`}/><section className="editorial-words narrow"><p>{editorial.detail}</p></section><section className="editorial-split"><img src={assetUrl(editorial.images[2])} alt="Предметы коллекции"/><img src={assetUrl(editorial.images[3])} alt="Образ коллекции"/></section><section className="editorial-products"><div className="editorial-products-head"><div><p>В {editorial.kind==="КАПСУЛА"?"КАПСУЛЕ":"КОЛЛЕКЦИИ"}</p><h2>Предметы {editorial.kind==="КАПСУЛА"?"капсулы":"коллекции"}</h2></div></div><div className="product-grid">{items.map(item=><ProductCard product={item} key={`${editorial.id}-${item.id}`} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div></section></div>;
}'''
text = text[:editorial_start] + editorial + text[editorial_end:]

# ProductView: remove bundle prop and all bundle-only state/handlers.
text = text.replace(
    "function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct, recentlyViewed }:",
    "function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, recentlyViewed }:",
)
text = text.replace(
    "function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct }:",
    "function ProductView({ product, favorite, liked, chooseSize, add, selectProduct }:",
)
text = text.replace(" buyBundle:(items:Product[])=>void;", "")
text = text.replace("  const [bundleSelecting,setBundleSelecting]=useState(false);\n", "")
for pattern in [
    r'  const bundleExtras=.*?;\n',
    r'  const bundleItems=.*?;\n',
    r'  const \[bundleSelectedIds,setBundleSelectedIds\]=.*?;\n',
    r'  useEffect\(\(\)=>\{setBundleSelecting\(false\);setBundleSelectedIds\(bundleItems\.map\(item=>item\.id\)\)\},\[product\.id\]\);\n',
    r'  const selectedBundleItems=.*?;\n',
    r'  const bundleTotal=.*?;\n',
    r'  const toggleBundleItem=.*?;\n',
    r'  const handleBundle=.*?;\n',
]:
    text = re.sub(pattern, "", text, count=1)

bundle_start = text.find('{product.hasBundle&&<section className={`bundle')
if bundle_start < 0:
    raise SystemExit("PDP bundle block was not found")
bundle_end = text.find("</section>}", bundle_start)
if bundle_end < 0:
    raise SystemExit("PDP bundle block end was not found")
text = text[:bundle_start] + text[bundle_end + len("</section>}"):]

# Post-add drawer: keep confirmation and cart CTA, remove cross-sell recommendations.
added_start = text.find("function PLPAdded(")
added_end = text.find("\n\nfunction SizeSheet", added_start)
if added_start < 0 or added_end < 0:
    raise SystemExit("PLPAdded boundaries were not found")
added = '''function PLPAdded({product,close,openCart}:{product:CartItem;close:()=>void;openCart:()=>void}){
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><img src={assetUrl(product.image)} alt={product.name}/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div><aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}'''
text = text[:added_start] + added + text[added_end:]
text = re.sub(r' selectRecommendation=\{\(product\)=>\{setPlpAdded\(null\);setPlpSize\(product\)\}\}', "", text, count=1)

# Remove the cart cross-sell block shown for a non-empty cart.
text, count = re.subn(
    r'<p className="recommend-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</p><div className="cart-recs">.*?</div>',
    "",
    text,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit("Cart recommendation block was not found")

# Verify that all buy-all and post-add/cart upsell logic is gone.
for marker in [
    "hasBundle?: boolean;",
    "hasBundle: true",
    "buyBundle",
    "addBundle",
    "bundleSelecting",
    "bundleSelectedIds",
    "bundleTotal",
    "handleBundle",
    "ВЫКУПИТЬ ВЕСЬ КОМПЛЕКТ",
    "ВЫКУПИТЬ ВСЮ ",
    "СОБЕРИТЕ КОМПЛЕКТ",
    "added-recommendations",
    '<p className="recommend-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</p>',
]:
    if marker in text:
        raise SystemExit(f"Cleanup marker still present: {marker}")

path.write_text(text)
print("Removed bundle/collection/capsule buy-all flows and cart/post-add upsells")
