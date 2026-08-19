from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

# GIFT_WRAP_FLOW_V1
if "giftPackagingAvailable?: boolean;" not in page:
    page = page.replace(
        "  selectedSkuId?: string;\n};",
        "  selectedSkuId?: string;\n  giftPackagingAvailable?: boolean;\n};",
        1,
    )

page = page.replace(
    'type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number };',
    'type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number; giftWrap?: boolean; ribbon?: boolean };',
    1,
)

new_plp_added = r'''function PLPAdded({product,close,openCart,updateGift}:{product:CartItem;close:()=>void;openCart:()=>void;updateGift:(giftWrap:boolean,ribbon:boolean)=>void}){
  const giftAvailable=product.giftPackagingAvailable!==false;
  const [giftWrap,setGiftWrap]=useState(Boolean(product.giftWrap));
  const [ribbon,setRibbon]=useState(Boolean(product.ribbon));
  const toggleWrap=(checked:boolean)=>{setGiftWrap(checked);updateGift(checked,ribbon)};
  const toggleRibbon=(checked:boolean)=>{setRibbon(checked);updateGift(giftWrap,checked)};
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><ScrollableProductMedia product={product} alt={product.name} className="added-product-media"/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div>{giftAvailable&&<section className="added-gift-flow" aria-label="Подарочное оформление"><div className="added-gift-head"><div><strong>Оформить как подарок</strong><small>Добавьте оформление к этому товару</small></div></div><label className="added-gift-option"><input type="checkbox" checked={giftWrap} onChange={event=>toggleWrap(event.target.checked)}/><span><b>Подарочная упаковка</b><small>Фирменная упаковка Культура дома</small></span></label><label className="added-gift-option"><input type="checkbox" checked={ribbon} onChange={event=>toggleRibbon(event.target.checked)}/><span><b>Ленточка</b><small>Добавить декоративную ленту к подарку</small></span></label></section>}<aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}'''

pattern = r'function PLPAdded\(\{product,close,openCart\}[\s\S]*?\n\}\n\nfunction SizeSheet'
if re.search(pattern, page):
    page = re.sub(pattern, new_plp_added + "\n\nfunction SizeSheet", page, count=1)
elif "updateGift:(giftWrap:boolean,ribbon:boolean)=>void" not in page:
    raise SystemExit("PLPAdded function not found")

old_render = '{plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} />}'
new_render = '''{plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} updateGift={(giftWrap,ribbon)=>{const target=plpAdded;setPlpAdded({...target,giftWrap,ribbon});setCart(current=>{const next=[...current];for(let i=next.length-1;i>=0;i--){const item=next[i];if(item.id===target.id&&item.selectedSize===target.selectedSize&&item.selectedColor===target.selectedColor){next[i]={...item,giftWrap,ribbon};break}}return next})}} />}'''
if old_render in page:
    page = page.replace(old_render, new_render, 1)
elif "updateGift={(giftWrap,ribbon)=>" not in page:
    raise SystemExit("PLPAdded render not found")

old_cart = '<span>Цвет: {p.selectedColor}</span><label>Размер'
new_cart = '<span>Цвет: {p.selectedColor}</span>{(p.giftWrap||p.ribbon)&&<span className="cart-gift-options">Подарок: {[p.giftWrap&&"упаковка",p.ribbon&&"ленточка"].filter(Boolean).join(" · ")}</span>}<label>Размер'
if old_cart in page:
    page = page.replace(old_cart, new_cart, 1)

page_path.write_text(page, encoding="utf-8")
print("Applied mobile gift wrapping post-add flow")
