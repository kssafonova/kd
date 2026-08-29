from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"app"/"page.tsx"
MARKER="// GROUPED_CATALOG_V94"

def main():
    text=PAGE.read_text(encoding="utf-8")
    if MARKER in text:
        print(f"{MARKER}: already applied")
        return
    old='function skuPrimaryMatches(product:Product,sku:CatalogSku,primary?:string){if(!primary)return true;const extra=asVariantSku(sku);return isAromaProduct(product)?extra?.scent===primary:(extra?.sourceColor??sku.color)===primary}'
    new='function skuPrimaryMatches(product:Product,sku:CatalogSku,primary?:string){if(!primary||product.switchBy==="none")return true;const extra=asVariantSku(sku);return isAromaProduct(product)?extra?.scent===primary:(extra?.sourceColor??sku.color)===primary}'
    if old not in text:
        raise SystemExit("skuPrimaryMatches fragment not found")
    text=text.replace(old,new,1)
    text=text.replace("// GROUPED_CATALOG_V93",MARKER+"\n// GROUPED_CATALOG_V93",1)
    PAGE.write_text(text,encoding="utf-8")
    print(f"{MARKER}: size-only and single-selector products keep all SKU rows")

if __name__=="__main__": main()
