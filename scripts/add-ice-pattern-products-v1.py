from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

catalog_block = '''
  // ICE_PATTERN_PRODUCTS_V1
  makeProduct(2000,"KD-PD-2000","KD-PD-2000","Коллекция «Ледяные узоры»",0,[
    {color:"Синий",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2001,"KD-PD-2001","KD-PD-2001","Коллекция «Ледяные узоры»",0,[
    {color:"Ночной синий",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-DARK01.png",gallery:[]},
    {color:"Белый",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2003,"KD-PD-2003","KD-PD-2003","Коллекция «Ледяные узоры»",0,[
    {color:"Синий",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ]),
  makeProduct(2004,"KD-PD-2004","KD-PD-2004","Коллекция «Ледяные узоры»",0,[
    {color:"Белый",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2004-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2010,"KD-PD-2010","KD-PD-2010","Коллекция «Ледяные узоры»",0,[
    {color:"Белый",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Ночной синий",size:"Стандарт",material:"Не указано",composition:"Не указано",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-DARK01.png",gallery:[]},
  ]),
'''

if "ICE_PATTERN_PRODUCTS_V1" not in catalog:
    anchor = "\n];\n\nexport const catalogProductOverrides"
    if anchor not in catalog:
        raise SystemExit("catalog productList anchor not found")
    catalog = catalog.replace(anchor, "\n" + catalog_block + "];\n\nexport const catalogProductOverrides", 1)

page_block = '''
  // ICE_PATTERN_PRODUCTS_V1
  { id:2000, name:"KD-PD-2000", note:"Коллекция «Ледяные узоры»", price:0, image:"/images/products/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Синий",hex:"#8ba7c0",image:"/images/products/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2000-WHITE01.png"},
  ]},
  { id:2001, name:"KD-PD-2001", note:"Коллекция «Ледяные узоры»", price:0, image:"/images/products/KD-PD-2001-DARK01.png", colorVariants:[
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2001-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2001-WHITE01.png"},
  ]},
  { id:2003, name:"KD-PD-2003", note:"Коллекция «Ледяные узоры»", price:0, image:"/images/products/KD-PD-2003-BLUE01.png", gallery:["/images/products/KD-PD-2003-BLUE02.png"], colorVariants:[
    {name:"Синий",hex:"#8ba7c0",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ]},
  { id:2004, name:"KD-PD-2004", note:"Коллекция «Ледяные узоры»", price:0, image:"/images/products/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2004-WHITE01.png"},
  ]},
  { id:2010, name:"KD-PD-2010", note:"Коллекция «Ледяные узоры»", price:0, image:"/images/products/KD-PD-2010-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2010-WHITE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2010-DARK01.png"},
  ]},
'''

if "ICE_PATTERN_PRODUCTS_V1" not in page:
    anchor = "\n];\n\nconst REMOVED_PRODUCT_IDS"
    if anchor not in page:
        raise SystemExit("baseProducts anchor not found")
    page = page.replace(anchor, "\n" + page_block + "];\n\nconst REMOVED_PRODUCT_IDS", 1)

# Replace the old Ice Patterns assortment completely.
page, changed = re.subn(
    r'(\{ id:"ice", name:"Ледяные узоры"[^\n]*?productIds:)\[[^\]]*\]( \},)',
    r'\1[2000,2001,2003,2004,2010]\2',
    page,
    count=1,
)
if changed != 1 and "productIds:[2000,2001,2003,2004,2010]" not in page:
    raise SystemExit("Ice Patterns editorial assortment not found")

# Unknown-price UI. 0 is used only as an internal sentinel and is never shown as 0 ₽.
if "PRICE_PENDING_UI_V1" not in page:
    page = page.replace(
        'const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;',
        'const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;\n// PRICE_PENDING_UI_V1\nconst priceKnown=(value:number)=>Number.isFinite(value)&&value>0;',
        1,
    )

    page = page.replace(
        '  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);',
        '  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);\n  const knownPrice=priceKnown(product.price);',
        1,
    )
    old_price = '<span className={`price ${discount?"sale-price":""}`}>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</span>'
    new_price = '<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span>'
    if old_price not in page:
        raise SystemExit("ProductCard price block not found")
    page = page.replace(old_price, new_price, 1)

    old_quick = '<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>'
    new_quick = '<button className="quick" disabled={!knownPrice} onClick={()=>knownPrice&&onQuick(chosenProduct)} aria-label={knownPrice?`Добавить в корзину ${product.name}`:`Цена товара ${product.name} уточняется`}><Icon name="cart-add"/></button>'
    if old_quick not in page:
        raise SystemExit("ProductCard quick-add block not found")
    page = page.replace(old_quick, new_quick, 1)

    page = page.replace(
        '<span>{fmt(price)}</span>{oldPrice&&oldPrice>price&&<del>{fmt(oldPrice)}</del>}',
        '<span>{priceKnown(price)?fmt(price):"Цена уточняется"}</span>{priceKnown(price)&&oldPrice&&oldPrice>price&&<del>{fmt(oldPrice)}</del>}',
        1,
    )

    page = page.replace(
        '  const selectedUnavailable=Boolean(effectiveSelectedSize&&!isProductSizeAvailable(product,color.name,effectiveSelectedSize));\n  const handlePurchase=()=>{if(needsSize||selectedUnavailable)return;add(selectedProduct)};',
        '  const selectedUnavailable=Boolean(effectiveSelectedSize&&!isProductSizeAvailable(product,color.name,effectiveSelectedSize));\n  const knownUnitPrice=priceKnown(unitPrice);\n  const handlePurchase=()=>{if(needsSize||selectedUnavailable||!knownUnitPrice)return;add(selectedProduct)};',
        1,
    )
    page = page.replace(
        '<div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)}</strong>{product.oldPrice&&<><del>{sizes.length>1&&!selectedSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div>',
        '<div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{knownUnitPrice?(sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)):"Цена уточняется"}</strong>{knownUnitPrice&&product.oldPrice&&<><del>{sizes.length>1&&!selectedSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div>',
        1,
    )
    page = page.replace(
        '<button className={`primary purchase-cta total-cta ${needsSize||selectedUnavailable?"needs-size":"ready-to-add"}`} disabled={needsSize||selectedUnavailable} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{selectedUnavailable?"НЕТ В НАЛИЧИИ":needsSize?"ВЫБРАТЬ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&!selectedUnavailable&&<b>{fmt(unitPrice*quantity)}</b>}</button>',
        '<button className={`primary purchase-cta total-cta ${needsSize||selectedUnavailable||!knownUnitPrice?"needs-size":"ready-to-add"}`} disabled={needsSize||selectedUnavailable||!knownUnitPrice} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{selectedUnavailable?"НЕТ В НАЛИЧИИ":!knownUnitPrice?"ЦЕНА УТОЧНЯЕТСЯ":needsSize?"ВЫБРАТЬ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&!selectedUnavailable&&knownUnitPrice&&<b>{fmt(unitPrice*quantity)}</b>}</button>',
        1,
    )

    page = page.replace(
        '  const total=selectedItems.reduce((sum,item)=>sum+item.price,0);',
        '  const total=selectedItems.reduce((sum,item)=>sum+(priceKnown(item.price)?item.price:0),0);\n  const hasUnknownPrice=selectedItems.some(item=>!priceKnown(item.price));',
        1,
    )
    page = page.replace(
        '  const handleBundle=()=>{if(!selecting){setSelecting(true);return}if(selectedItems.length)buyBundle(selectedItems)};',
        '  const handleBundle=()=>{if(!selecting){setSelecting(true);return}if(selectedItems.length&&!hasUnknownPrice)buyBundle(selectedItems)};',
        1,
    )
    page = page.replace(
        '<button className="primary total-cta" disabled={selecting&&!selectedItems.length} onClick={handleBundle}><span>{selecting?"ДОБАВИТЬ В КОРЗИНУ":"ВЫКУПИТЬ ВСЮ "+(editorial.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ")}</span><b>{fmt(total)}</b></button>',
        '<button className="primary total-cta" disabled={(selecting&&!selectedItems.length)||hasUnknownPrice} onClick={handleBundle}><span>{hasUnknownPrice?"ЦЕНА УТОЧНЯЕТСЯ":selecting?"ДОБАВИТЬ В КОРЗИНУ":"ВЫКУПИТЬ ВСЮ "+(editorial.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ")}</span><b>{hasUnknownPrice?"Цена уточняется":fmt(total)}</b></button>',
        1,
    )

    page = page.replace('<b>{fmt(item.price)}</b>', '<b>{priceKnown(item.price)?fmt(item.price):"Цена уточняется"}</b>', 1)
    page = page.replace('<b>{fmt(p.price)}</b>', '<b>{priceKnown(p.price)?fmt(p.price):"Цена уточняется"}</b>', 1)

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Added five Ice Patterns products and replaced the previous collection assortment")
