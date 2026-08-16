from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()

if "function ScrollableProductMedia(" in text:
    print("Scrollable product media is already installed")
    raise SystemExit(0)

helper = r'''
function getProductImages(product:Product){
  const sources=[product.image,...(product.gallery??[]),...(product.colorVariants??[]).map(variant=>variant.image)];
  return Array.from(new Set(sources.filter(Boolean)));
}

function ScrollableProductMedia({product,alt,className="",position}:{product:Product;alt:string;className?:string;position?:string}){
  const images=getProductImages(product);
  return <div className={`product-media-scroll ${images.length>1?"is-scrollable":""} ${className}`.trim()} role="group" aria-label={`${alt}: ${images.length} фото`} onWheel={event=>{const node=event.currentTarget;if(images.length>1&&Math.abs(event.deltaY)>Math.abs(event.deltaX)){node.scrollLeft+=event.deltaY;event.preventDefault()}}}>{images.map((src,index)=><img key={`${src}-${index}`} src={assetUrl(src)} alt={index===0?alt:`${alt}, фото ${index+1}`} style={{objectPosition:position||product.position||"center"}} draggable={false}/>)}{images.length>1&&<span className="product-media-hint">{images.length} фото · листайте</span>}</div>;
}
'''

marker = "\nconst products: Product[] = ["
if marker not in text:
    raise SystemExit("Product data marker not found")
text = text.replace(marker, helper + marker, 1)

replacements = [
    (
        '<img key={chosen.image} src={assetUrl(chosen.image)} alt={`${product.name}, цвет ${chosen.name}`} style={{objectPosition:chosen.position||product.position||"center"}}/>',
        '<ScrollableProductMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, цвет ${chosen.name}`} position={chosen.position||product.position}/>',
        "ProductCard media",
    ),
    (
        '<div className="plp-modal-media"><img src={assetUrl(product.image)} alt={product.name}/></div>',
        '<div className="plp-modal-media"><ScrollableProductMedia product={product} alt={product.name}/></div>',
        "PLP quick-add media",
    ),
    (
        '<div className="added-product"><img src={assetUrl(product.image)} alt={product.name}/><div>',
        '<div className="added-product"><ScrollableProductMedia product={product} alt={product.name} className="added-product-media"/><div>',
        "post-add media",
    ),
    (
        '<button key={product.id} onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/><strong>{product.name}</strong>',
        '<button key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><strong>{product.name}</strong>',
        "empty-cart recent media",
    ),
    (
        '<article key={`${p.id}-${i}`}><img src={assetUrl(p.image)} alt={`${p.name}, ${p.selectedColor}`}/><div className="cart-item-copy">',
        '<article key={`${p.id}-${i}`}><ScrollableProductMedia product={p} alt={`${p.name}, ${p.selectedColor}`} className="cart-item-media"/><div className="cart-item-copy">',
        "cart item media",
    ),
    (
        '<article key={`${item.id}-${index}`}><img src={assetUrl(item.image)} alt={item.name}/><div><strong>{item.name}</strong>',
        '<article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-item-media"/><div><strong>{item.name}</strong>',
        "checkout item media",
    ),
    (
        '<button key={p.id} onClick={()=>choose(p)}><img src={assetUrl(p.image)} alt=""/><span>{p.name}',
        '<button key={p.id} onClick={()=>choose(p)}><ScrollableProductMedia product={p} alt={p.name} className="search-item-media"/><span>{p.name}',
        "search result media",
    ),
    (
        '<button className="favorite-image" onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/></button>',
        '<button className="favorite-image" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="favorite-item-media"/></button>',
        "favorites media",
    ),
    (
        '<div className="pdp-main"><img key={image} src={assetUrl(image)} alt={`${product.name}, ${color.name}`}/></div>',
        '<div className="pdp-main"><ScrollableProductMedia key={`${product.id}-${color.name}-${image}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media"/></div>',
        "PDP main media",
    ),
]

for old, new, label in replacements:
    if old not in text:
        raise SystemExit(f"{label} marker not found")
    text = text.replace(old, new, 1)

required = [
    "function ScrollableProductMedia(",
    'className="pdp-product-media"',
    'className="cart-item-media"',
    'className="checkout-item-media"',
    'className="added-product-media"',
    'className="recent-item-media"',
    'className="search-item-media"',
    'className="favorite-item-media"',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f"Missing product media marker: {marker}")

path.write_text(text)
print("Enabled scrollable multi-image product media across storefront forms")
