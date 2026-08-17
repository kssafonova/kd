from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text(encoding="utf-8")

catalog_path = Path("app/catalog-data.ts")
catalog = catalog_path.read_text(encoding="utf-8")

# KD-PD-1023 media rule:
# keep White and Blue color variants, but remove WHITE01/BLUE01 from product media.
match = re.search(
    r'makeProduct\(3,"KD-PD-1023","Подушка с кружевом".*?\n  \]\),',
    catalog,
    flags=re.S,
)
if not match:
    raise SystemExit("KD-PD-1023 catalog block not found")

block = match.group(0)
block = block.replace(
    'image:"/kd/images/products/KD-PD-1023-WHITE01.png",gallery:["/kd/images/products/KD-PD-1023-WHITE02.png"]',
    'image:"/kd/images/products/KD-PD-1023-WHITE02.png",gallery:[]',
)
block = block.replace(
    'image:"/kd/images/products/KD-PD-1023-BLUE01.png",gallery:["/kd/images/products/KD-PD-1023-BLUE02.png"]',
    'image:"/kd/images/products/KD-PD-1023-BLUE02.png",gallery:[]',
)
if "KD-PD-1023-WHITE01.png" in block or "KD-PD-1023-BLUE01.png" in block:
    raise SystemExit("KD-PD-1023 still references WHITE01 or BLUE01")
if "KD-PD-1023-WHITE02.png" not in block or "KD-PD-1023-BLUE02.png" not in block:
    raise SystemExit("KD-PD-1023 replacement media is missing")

catalog = catalog[:match.start()] + block + catalog[match.end():]
catalog_path.write_text(catalog, encoding="utf-8")

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
print("Applied product preview rules and removed WHITE01/BLUE01 from KD-PD-1023 media")
