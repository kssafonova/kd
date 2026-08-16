from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()

if "function ProductRail(" not in text:
    text = text.replace(
        'import { useEffect, useMemo, useState } from "react";',
        'import { useEffect, useMemo, useRef, useState } from "react";',
        1,
    )

    marker = "\nconst products: Product[] = ["
    if marker not in text:
        raise SystemExit("Product data marker not found")

    rail = r'''
function ProductRail({items,onProduct,onQuick,favorite,favorites,className=""}:{items:Product[];onProduct:(product:Product)=>void;onQuick:(product:Product)=>void;favorite:(id:number)=>void;favorites:number[];className?:string}){
  const railRef=useRef<HTMLDivElement>(null);
  const [hasOverflow,setHasOverflow]=useState(false);
  const [atStart,setAtStart]=useState(true);
  const [atEnd,setAtEnd]=useState(false);

  useEffect(()=>{
    const node=railRef.current;
    if(!node)return;
    const sync=()=>{
      const max=node.scrollWidth-node.clientWidth;
      setHasOverflow(max>2);
      setAtStart(node.scrollLeft<=2);
      setAtEnd(node.scrollLeft>=max-2);
    };
    sync();
    const observer=new ResizeObserver(sync);
    observer.observe(node);
    node.addEventListener("scroll",sync,{passive:true});
    return ()=>{observer.disconnect();node.removeEventListener("scroll",sync)};
  },[items.length]);

  const move=(direction:number)=>{
    const node=railRef.current;
    if(!node)return;
    const card=node.querySelector<HTMLElement>(".product-card");
    const gap=parseFloat(getComputedStyle(node).columnGap||getComputedStyle(node).gap||"0")||0;
    const step=(card?.getBoundingClientRect().width??node.clientWidth)+gap;
    node.scrollBy({left:direction*step,behavior:"smooth"});
  };

  return <div className={`product-rail-shell ${className}`.trim()}>
    {hasOverflow&&<button className="product-rail-arrow prev" onClick={()=>move(-1)} disabled={atStart} aria-label="Предыдущие товары"><Icon name="chevron"/></button>}
    <div className="product-rail" ref={railRef}>{items.map(item=><ProductCard key={`${className}-${item.id}`} product={item} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
    {hasOverflow&&<button className="product-rail-arrow next" onClick={()=>move(1)} disabled={atEnd} aria-label="Следующие товары"><Icon name="chevron"/></button>}
  </div>;
}
'''
    text = text.replace(marker, rail + marker, 1)

home_old = '<div className="product-row" key={`featured-${slide}`}>{featuredProducts.map(p=><ProductCard key={`${slide}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div>'
home_new = '<ProductRail key={`featured-${slide}`} className="home-product-rail" items={featuredProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>'
if home_old in text:
    text = text.replace(home_old, home_new, 1)
elif 'className="home-product-rail"' not in text:
    raise SystemExit("Home product rail marker not found")

category_old = '<section className="post-rich-recommendations category-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Товары из этой категории</h2></div><div>{categoryProducts.map(item=><ProductCard key={`category-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>'
category_new = '<section className="post-rich-recommendations category-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Товары из этой категории</h2></div><ProductRail className="recommendation-product-rail" items={categoryProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>'
if category_old in text:
    text = text.replace(category_old, category_new, 1)
elif 'category-recommendations"><div className="section-head"' in text and 'className="recommendation-product-rail"' not in text:
    raise SystemExit("Category recommendation rail marker not found")

viewed_old = '{viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><div>{viewedProducts.map(item=><ProductCard key={`recent-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>}'
viewed_new = '{viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><ProductRail className="recommendation-product-rail" items={viewedProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}'
if viewed_old in text:
    text = text.replace(viewed_old, viewed_new, 1)

cart_marker = 'function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {\n  const sizeOptions=["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];'
cart_replacement = 'function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {\n  const sizeOptions=["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];\n  const recentItems=recentlyViewed.slice(0,6);'
if "const recentItems=recentlyViewed.slice(0,6);" not in text:
    if cart_marker not in text:
        raise SystemExit("Cart marker not found")
    text = text.replace(cart_marker, cart_replacement, 1)
    text = text.replace('recentlyViewed.length?<section className="recent-cart"', 'recentItems.length?<section className="recent-cart"', 1)
    text = text.replace('{recentlyViewed.map(product=><button key={product.id}', '{recentItems.map(product=><button key={product.id}', 1)

required = [
    "function ProductRail(",
    'className="home-product-rail"',
    'className="recommendation-product-rail"',
    "const recentItems=recentlyViewed.slice(0,6);",
    'recentItems.length?<section className="recent-cart"',
    '{recentItems.map(product=><button key={product.id}',
]
for item in required:
    if item not in text:
        raise SystemExit(f"Missing expected rail/cart marker: {item}")

path.write_text(text)
print("Added responsive product rails and capped cart recently viewed at six items")
