from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

marker = "// PRODUCT_PREVIEW_RULES_V1"

if marker not in text:
    old_products = '''const products: Product[] = baseProducts.map(base=>{
  const override=catalogProductOverrides[base.id];
  if(!override)return base;
  const first=override.skus[0];
  const colors=Array.from(new Map(override.skus.map(item=>[item.color,item])).values());
  return {'''

    new_products = '''// PRODUCT_PREVIEW_RULES_V1
const catalogPreviewColorByArticle:Record<string,string> = {
  "KD-PD-1028":"Белый",
  "KD-PD-1128":"Белый",
};
const products: Product[] = baseProducts.map(base=>{
  const override=catalogProductOverrides[base.id];
  if(!override)return base;
  const preferredColor=catalogPreviewColorByArticle[override.article];
  const first=(preferredColor?override.skus.find(item=>item.color===preferredColor):undefined)??override.skus[0];
  const colorRows=Array.from(new Map(override.skus.map(item=>[item.color,item])).values());
  const colors=preferredColor
    ? [...colorRows.filter(item=>item.color===preferredColor),...colorRows.filter(item=>item.color!==preferredColor)]
    : colorRows;
  return {'''

    if old_products not in text:
        raise SystemExit("products mapping anchor not found")
    text = text.replace(old_products, new_products, 1)

    old_items = '''  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);'''
    new_items = '''  const lunaPreviewRules:Record<string,{color:string;image:string}>={
    "KD-PD-1023":{color:"Синий",image:"/kd/images/products/KD-PD-1023-BLUE02.png"},
    "KD-PD-1026":{color:"Синий",image:"/kd/images/products/KD-PD-1026-BLUE01.png"},
  };
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean).map(product=>{
    if(editorial.id!=="luna")return product;
    const rule=lunaPreviewRules[product.article??""];
    if(!rule)return product;
    const skus=product.skus?.map(sku=>sku.color===rule.color?{
      ...sku,
      image:rule.image,
      gallery:Array.from(new Set([sku.image,...sku.gallery].filter(image=>image!==rule.image))),
    }:sku);
    const orderedSkus=skus
      ? [...skus.filter(sku=>sku.color===rule.color),...skus.filter(sku=>sku.color!==rule.color)]
      : skus;
    const variants=product.colorVariants?.map(variant=>variant.name===rule.color?{
      ...variant,
      image:rule.image,
      gallery:Array.from(new Set([variant.image,...(variant.gallery??[])].filter(image=>image!==rule.image))),
    }:variant);
    const orderedVariants=variants
      ? [...variants.filter(variant=>variant.name===rule.color),...variants.filter(variant=>variant.name!==rule.color)]
      : variants;
    return {
      ...product,
      image:rule.image,
      selectedColor:rule.color,
      skus:orderedSkus,
      colorVariants:orderedVariants,
    };
  });'''

    if old_items not in text:
        raise SystemExit("EditorialView items anchor not found")
    text = text.replace(old_items, new_items, 1)
else:
    required = [
        '"KD-PD-1028":"Белый"',
        '"KD-PD-1128":"Белый"',
        '"KD-PD-1023":{color:"Синий",image:"/kd/images/products/KD-PD-1023-BLUE02.png"}',
        '"KD-PD-1026":{color:"Синий",image:"/kd/images/products/KD-PD-1026-BLUE01.png"}',
    ]
    missing = [value for value in required if value not in text]
    if missing:
        raise SystemExit("Preview rules marker exists but required rules are missing: " + ", ".join(missing))

path.write_text(text, encoding="utf-8")
print("Applied catalog white previews for KD-PD-1028/KD-PD-1128 and Luna blue previews for KD-PD-1023/KD-PD-1026")
