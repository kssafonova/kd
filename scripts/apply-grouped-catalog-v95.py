from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"app"/"page.tsx"
MARKER="// GROUPED_CATALOG_V95"

def main():
    text=PAGE.read_text(encoding="utf-8")
    quick='<p className="quick-color">{isAromaProduct(product)?"Аромат":"Цвет"}: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>'
    wrapped='{product.switchBy!=="none"&&'+quick+'}'
    nested='{product.switchBy!=="none"&&'+wrapped+'}'
    changed=False
    while nested in text:
        text=text.replace(nested,wrapped)
        changed=True

    small='<small>{chosen.name.toLowerCase()}, {product.note}</small>'
    small_wrapped='<small>{product.switchBy==="none"?product.note:<>{chosen.name.toLowerCase()}, {product.note}</>}</small>'
    nested_small='<small>{product.switchBy==="none"?product.note:<>{product.switchBy==="none"?product.note:<>{chosen.name.toLowerCase()}, {product.note}</>}</>}</small>'
    while nested_small in text:
        text=text.replace(nested_small,small_wrapped)
        changed=True

    if MARKER not in text:
        anchor="// GROUPED_CATALOG_V94"
        if anchor not in text:
            raise SystemExit("V94 marker not found")
        text=text.replace(anchor,MARKER+"\n"+anchor,1)
        changed=True

    PAGE.write_text(text,encoding="utf-8")
    print(f"{MARKER}: normalized repeated catalog-card conditional wrappers; changed={changed}")

if __name__=="__main__": main()
