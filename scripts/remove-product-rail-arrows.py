from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()

start = text.find("function ProductRail(")
end_marker = "\n\nconst products: Product[] = ["
end = text.find(end_marker, start)

if start == -1 or end == -1:
    raise SystemExit("ProductRail block not found")

replacement = r'''function ProductRail({items,onProduct,onQuick,favorite,favorites,className=""}:{items:Product[];onProduct:(product:Product)=>void;onQuick:(product:Product)=>void;favorite:(id:number)=>void;favorites:number[];className?:string}){
  return <div className={`product-rail-shell ${className}`.trim()}>
    <div className="product-rail">{items.map(item=><ProductCard key={`${className}-${item.id}`} product={item} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
  </div>;
}'''

text = text[:start] + replacement + text[end:]
text = text.replace('import { useEffect, useMemo, useRef, useState } from "react";', 'import { useEffect, useMemo, useState } from "react";', 1)

if "product-rail-arrow" in text:
    raise SystemExit("Product rail arrows are still present")

path.write_text(text)
print("Removed product rail arrows and retained swipe/scroll behavior")
