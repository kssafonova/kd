from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"app"/"page.tsx"
MARKER="// GROUPED_CATALOG_V96"

def main():
    text=PAGE.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"{MARKER}: already applied")
        return
    anchor='function ScrollableProductMedia({product,alt,className="",position,activeIndex,onActiveIndexChange}'
    if anchor not in text:
        raise SystemExit("ScrollableProductMedia anchor not found")
    helper='''// GROUPED_CATALOG_V96\nfunction getProductImages(product:Product){\n  if(product.skus?.length){\n    const selected=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;\n    const sku=selected??product.skus[0];\n    return Array.from(new Set([sku?.image,...(sku?.gallery??[])].map(cleanNulls).filter((value):value is string=>Boolean(value))));\n  }\n  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;\n  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];\n  return Array.from(new Set(sources.map(cleanNulls).filter((value):value is string=>Boolean(value))));\n}\n\n'''
    text=text.replace(anchor,helper+anchor,1)
    PAGE.write_text(text,encoding="utf-8")
    print(f"{MARKER}: restored selected-SKU image gallery with null filtering")

if __name__=="__main__": main()
