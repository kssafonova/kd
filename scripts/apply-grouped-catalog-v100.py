from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
MARKER = "// GROUPED_CATALOG_V100"

text = PAGE.read_text(encoding="utf-8")
if MARKER in text:
    print(f"{MARKER}: already applied")
    raise SystemExit(0)

# 1) One CSV row / one SKU: quick-add must not render a size selector.
old_quick = '<button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/>'
new_quick = '<button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button>{sizes.length>1&&<><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}'
if old_quick not in text:
    raise SystemExit("PLP single-variant size block anchor not found")
text = text.replace(old_quick, new_quick, 1)

# 2) Product info drawer: every null/empty field hides both label and value.
start = text.find('function ProductInfoDrawer({product,close}')
end = text.find('\n\nfunction isGiftPackagingAvailable', start)
if start < 0 or end < 0:
    raise SystemExit("ProductInfoDrawer block not found")
new_drawer = '''function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize)??product.skus?.[0];
  const extra=asVariantSku(sku);
  const sizeValue=cleanNulls(sku?.size)==="Единый размер"?undefined:cleanNulls(sku?.size);
  const rows:[string,string|undefined][]=[
    ["Размер",sizeValue],
    ["Высота",cleanNulls(sku?.height)],
    ["Ширина",cleanNulls(sku?.width)],
    ["Объём",cleanNulls(extra?.volume)],
    ["Диаметр",cleanNulls(sku?.diameter)],
    ["Комплектация",cleanNulls(sku?.packageInfo)],
    ["Детали",cleanNulls(sku?.details)],
    ["Коллекция",cleanNulls(sku?.collection)],
    ["Капсула",cleanNulls(sku?.capsule)],
  ];
  const visibleRows=rows.filter((row):row is [string,string]=>Boolean(row[1]));
  const material=cleanNulls(sku?.material);
  const composition=cleanNulls(sku?.composition);
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div>{visibleRows.length>0&&<section><h2>ХАРАКТЕРИСТИКИ</h2><dl>{visibleRows.map(([label,value])=><div key={label}><dt>{label}</dt><dd>{renderMultiline(value)}</dd></div>)}</dl></section>}{(material||composition)&&<section><h2>МАТЕРИАЛ И СОСТАВ</h2>{material&&<h3>{renderMultiline(material)}</h3>}{composition&&<div>{renderMultiline(composition)}</div>}</section>}<section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}'''
text = text[:start] + new_drawer + text[end:]
text = text.replace("// GROUPED_CATALOG_V98", f"{MARKER}\n// GROUPED_CATALOG_V98", 1)
PAGE.write_text(text, encoding="utf-8")
print(f"{MARKER}: single-SKU quick add hides size selector; product info hides null labels and preserves multiline values")
