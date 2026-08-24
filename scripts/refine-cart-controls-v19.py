from pathlib import Path

page_path = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = 'CART_CONTROLS_V19'
if marker in text:
    print("Cart controls V19 already applied")
    raise SystemExit(0)

old_v18 = '''<span>Цвет: {p.selectedColor}</span><div className="cart-item-variant" data-cart-controls="CART_CONTROLS_V18"><span>Размер</span><b>{p.selectedSize}</b></div>{isGiftPackagingAvailable(p)&&<label className="cart-gift-toggle"><input type="checkbox" checked={Boolean(p.giftWrap)} onChange={event=>update(i,{giftWrap:event.target.checked})}/><span><b>Подарочная упаковка</b><small>{p.giftWrap?"Добавлена к заказу":"Добавить к товару"}</small></span><i aria-hidden="true"/></label>}'''

new_v19 = '''<span>Цвет: {p.selectedColor}</span><span data-cart-controls="CART_CONTROLS_V19">Размер: {p.selectedSize}</span>{isGiftPackagingAvailable(p)&&<label className="cart-gift-checkbox"><input type="checkbox" checked={Boolean(p.giftWrap)} onChange={event=>update(i,{giftWrap:event.target.checked})} aria-label={`Подарочная упаковка для ${p.name}`}/><span>Подарочная упаковка</span></label>}'''

if old_v18 not in text:
    raise SystemExit("Cart controls V18 fragment was not found")

page_path.write_text(text.replace(old_v18, new_v19, 1), encoding="utf-8")
print("Cart controls V19 applied: size matches color row, one per-item gift checkbox")
