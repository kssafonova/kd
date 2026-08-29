from pathlib import Path

page_path = Path("app/page.tsx")
page = page_path.read_text(encoding="utf-8")

old = '''  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const chosenProduct = { ...product, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };
  const discount=discountOf(product);
  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);
  const knownPrice=priceKnown(product.price);'''
new = '''  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const primarySkus=(product.skus??[]).filter(item=>skuPrimaryMatches(product,item,chosen.name));
  const cardSkus=primarySkus.length?primarySkus:(product.skus??[]);
  const pricedCardSkus=cardSkus.filter(item=>priceKnown(item.price));
  const cardMinSku=pricedCardSkus.reduce<CatalogSku|undefined>((best,item)=>!best||item.price<best.price?item:best,undefined);
  const cardPrice=cardMinSku?.price??product.price;
  const cardOldPrice=Number(asVariantSku(cardMinSku)?.oldPrice)||0;
  const showFromPrice=new Set(cardSkus.map(item=>item.size)).size>1&&new Set(pricedCardSkus.map(item=>item.price)).size>1;
  const discount=cardOldPrice>cardPrice?Math.round((1-cardPrice/cardOldPrice)*100):0;
  const knownPrice=priceKnown(cardPrice);
  const chosenProduct = { ...product, price:cardPrice, oldPrice:cardOldPrice>cardPrice?cardOldPrice:undefined, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };'''
if old not in page:
    raise RuntimeError("ProductCard pricing block not found")
page = page.replace(old, new, 1)

old_price = '''<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span>'''
new_price = '''<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{showFromPrice?"от ":""}{fmt(cardPrice)} {cardOldPrice>cardPrice&&<><del>{showFromPrice?"от ":""}{fmt(cardOldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span>'''
if old_price not in page:
    raise RuntimeError("ProductCard price markup not found")
page = page.replace(old_price, new_price, 1)

# Remove obsolete hardcoded Echo media data. The new CSV is the only product-media source.
start_marker = "// ECHO_CSV_MEDIA_V81\n"
end_marker = "// READY_SOLUTIONS_MERCH_V75"
if start_marker in page:
    start = page.index(start_marker)
    end = page.index(end_marker, start)
    page = page[:start] + end_marker + page[end + len(end_marker):]

page_path.write_text(page, encoding="utf-8")
