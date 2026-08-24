from pathlib import Path

page_path = Path(__file__).resolve().parents[1] / "app" / "page.tsx"
text = page_path.read_text(encoding="utf-8")

marker = 'CART_CONTROLS_V18'
if marker in text:
    print("Cart controls V18 already applied")
    raise SystemExit(0)

old = '''<span>Цвет: {p.selectedColor}</span>{p.giftWrap&&<span className="cart-gift-options">Подарочная упаковка добавлена</span>}<label>Размер<select value={p.selectedSize} onChange={event=>{const nextSize=event.target.value;const nextSku=findProductSku(p,p.selectedColor,nextSize);update(i,{selectedSize:nextSize,selectedSkuId:nextSku?.id,price:nextSku?.price??p.price,image:nextSku?.image??p.image,gallery:nextSku?.gallery??p.gallery})}}>{getProductSizeOptions(p,p.selectedColor).map(([option])=><option key={option}>{option}</option>)}</select></label>'''

new = '''<span>Цвет: {p.selectedColor}</span><div className="cart-item-variant" data-cart-controls="CART_CONTROLS_V18"><span>Размер</span><b>{p.selectedSize}</b></div>{isGiftPackagingAvailable(p)&&<label className="cart-gift-toggle"><input type="checkbox" checked={Boolean(p.giftWrap)} onChange={event=>update(i,{giftWrap:event.target.checked})}/><span><b>Подарочная упаковка</b><small>{p.giftWrap?"Добавлена к заказу":"Добавить к товару"}</small></span><i aria-hidden="true"/></label>}'''

if old not in text:
    raise SystemExit("Cart size selector source fragment was not found")

page_path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Cart controls V18 applied: size locked, gift wrap toggle enabled")
