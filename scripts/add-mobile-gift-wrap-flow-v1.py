from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

# GIFT_WRAP_FLOW_V2 — one post-add flow for PLP/home/PDP.
if "giftPackagingAvailable?: boolean;" not in page:
    page = page.replace(
        "  selectedSkuId?: string;\n};",
        "  selectedSkuId?: string;\n  giftPackagingAvailable?: boolean;\n};",
        1,
    )

# Remove the retired ribbon state from cart items while keeping the migration idempotent.
page = re.sub(
    r'type CartItem = Product & \{ selectedSize: string; selectedColor: string; quantity: number;[^}]*\};',
    'type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number; giftWrap?: boolean };',
    page,
    count=1,
)

# Eligibility is data-driven: active capsule/collection membership, SKU merchandising tags,
# or a bedding-set product. An explicit true flag can also opt a product in.
gift_helper = r'''function isGiftPackagingAvailable(product:Product){
  const inEditorial=editorials.some(item=>item.productIds.includes(product.id));
  const merchandisingTagged=Boolean(product.skus?.some(sku=>Boolean(sku.collection?.trim()||sku.capsule?.trim())));
  const beddingSet=/^Комплект\b/i.test(product.name);
  return product.giftPackagingAvailable===true||inEditorial||merchandisingTagged||beddingSet;
}
'''
if "function isGiftPackagingAvailable(product:Product)" not in page:
    anchor = "function PLPAdded("
    if anchor not in page:
        raise SystemExit("PLPAdded anchor not found")
    page = page.replace(anchor, gift_helper + "\n" + anchor, 1)

# Older V2 builds emitted a double-escaped word boundary into TypeScript.
page = page.replace(
    r'const beddingSet=/^Комплект\\b/i.test(product.name);',
    r'const beddingSet=/^Комплект\b/i.test(product.name);',
)

new_plp_added = r'''function PLPAdded({product,close,openCart,updateGift}:{product:CartItem;close:()=>void;openCart:()=>void;updateGift:(giftWrap:boolean)=>void}){
  const giftAvailable=isGiftPackagingAvailable(product);
  const [giftWrap,setGiftWrap]=useState(Boolean(product.giftWrap));
  const toggleWrap=(checked:boolean)=>{setGiftWrap(checked);updateGift(checked)};
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><ScrollableProductMedia product={product} alt={product.name} className="added-product-media"/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div>{giftAvailable&&<section className="added-gift-flow" aria-label="Подарочное оформление"><div className="added-gift-head"><div><strong>Оформить как подарок</strong><small>Для этого товара доступна фирменная подарочная упаковка.</small></div></div><label className="added-gift-option"><input type="checkbox" checked={giftWrap} onChange={event=>toggleWrap(event.target.checked)}/><span><b>Добавить подарочную упаковку</b><small>Фирменная упаковка «Культура дома»</small></span></label></section>}<aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}'''

pattern = r'function PLPAdded\([\s\S]*?\n}\n\nfunction SizeSheet'
if not re.search(pattern, page):
    raise SystemExit("PLPAdded function not found")
page = re.sub(pattern, new_plp_added + "\n\nfunction SizeSheet", page, count=1)

# Use the post-add confirmation for PDP/size-sheet adds instead of opening Cart immediately.
page = re.sub(
    r'setPlpSize\(null\);\s*setSizeSheet\(false\);\s*if\(openDrawer\)setCartOpen\(true\);',
    'setPlpSize(null); setSizeSheet(false); if(openDrawer)setPlpAdded(item);',
    page,
    count=1,
)

# Normalize the PLPAdded render and persist gift wrapping on the exact cart line item.
render_pattern = r'\{plpAdded && <PLPAdded product=\{plpAdded\}[\s\S]*?/\>}'
new_render = '''{plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} updateGift={(giftWrap)=>{const target=plpAdded;setPlpAdded({...target,giftWrap});setCart(current=>{const next=[...current];for(let i=next.length-1;i>=0;i--){const item=next[i];if(item.id===target.id&&item.selectedSize===target.selectedSize&&item.selectedColor===target.selectedColor){next[i]={...item,giftWrap};break}}return next})}} />}'''
if not re.search(render_pattern, page):
    raise SystemExit("PLPAdded render not found")
page = re.sub(render_pattern, new_render, page, count=1)

# Replace any legacy gift/ribbon summary with the single supported option.
page = re.sub(
    r'\{\(p\.giftWrap\|\|p\.ribbon\)&&<span className="cart-gift-options">[\s\S]*?</span>\}',
    '{p.giftWrap&&<span className="cart-gift-options">Подарочная упаковка добавлена</span>}',
    page,
    count=1,
)
page = page.replace(
    '{p.giftWrap&&<span className="cart-gift-options">Подарок: упаковка</span>}',
    '{p.giftWrap&&<span className="cart-gift-options">Подарочная упаковка добавлена</span>}',
)

page_path.write_text(page, encoding="utf-8")
print("Applied unified responsive gift wrapping post-add flow")
