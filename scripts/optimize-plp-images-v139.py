from pathlib import Path

root = Path(__file__).resolve().parents[1]
storefront = root / "app" / "storefront-app.tsx"
layout = root / "app" / "catalog" / "layout.tsx"

text = storefront.read_text(encoding="utf-8")

# Only local repository assets explicitly listed in Фото 1–3 are valid catalog media.
entity_marker = 'const entityId=(article:string,name:string)=>300000+Array.from(`${article}|${name}`).reduce((sum,char)=>((sum*31)+char.charCodeAt(0))%500000,0);\n'
if 'const tableAssetImage=' not in text and entity_marker in text:
    text = text.replace(
        entity_marker,
        entity_marker + 'const tableAssetImage=(value:unknown)=>{const image=cleanNulls(value);if(!image)return undefined;if(image.startsWith("/assets/"))return image;if(image.startsWith("assets/"))return `/${image}`;return undefined};\n',
        1,
    )

old_images = 'const images=[row["Фото 1"],row["Фото 2"],row["Фото 3"]].map(cleanNulls).filter((value):value is string=>Boolean(value));'
new_images = 'const images=[row["Фото 1"],row["Фото 2"],row["Фото 3"]].map(tableAssetImage).filter((value):value is string=>Boolean(value));'
text = text.replace(old_images, new_images)

# PLP renders only Фото 1. Фото 2–3 remain in sku.gallery and are rendered on PDP only.
old_media = '<ScrollableProductMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, цвет ${chosen.name}`} position={chosen.position||product.position}/>'
new_media = '<RemoteImage src={chosenProduct.image} alt={`${product.name}, ${chosen.name}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:chosen.position||product.position||"center"}}/>'
text = text.replace(old_media, new_media)

# Progressive PLP rendering: do not mount hundreds of product cards on the first frame.
state_marker = '  const [draft,setDraft]=useState<CatalogFiltersV123>(()=>emptyCatalogFiltersV123());\n'
if 'const [visibleCount,setVisibleCount]' not in text and state_marker in text:
    text = text.replace(
        state_marker,
        state_marker + '  const [visibleCount,setVisibleCount]=useState(24);\n  const loadMoreRef=useRef<HTMLDivElement>(null);\n',
        1,
    )

open_filters_marker = '\n  const openFilters=()=>'
if 'const visibleList=list.slice(0,visibleCount);' not in text and open_filters_marker in text:
    progressive = '''\n  const resultKey=[category,sort,applied.subcategories.join("~"),applied.collections.join("~"),applied.capsules.join("~"),applied.materials.join("~"),applied.sizes.join("~"),applied.colors.join("~"),applied.priceFrom,applied.priceTo].join("|");
  useEffect(()=>{setVisibleCount(24)},[resultKey]);
  useEffect(()=>{
    const node=loadMoreRef.current;
    if(!node||visibleCount>=list.length||typeof IntersectionObserver==="undefined")return;
    const observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting))setVisibleCount(current=>Math.min(current+24,list.length))},{rootMargin:"900px 0px"});
    observer.observe(node);
    return()=>observer.disconnect();
  },[visibleCount,list.length,resultKey]);
  const visibleList=list.slice(0,visibleCount);
'''
    text = text.replace(open_filters_marker, progressive + open_filters_marker, 1)

text = text.replace(
    '{list.length?<div className="product-grid">{list.map(product=><ProductCard',
    '{list.length?<><div className="product-grid">{visibleList.map(product=><ProductCard',
    1,
)
text = text.replace(
    ' favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>:<div className="catalog-empty catalog-empty-v123">',
    ' favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>{visibleCount<list.length&&<div ref={loadMoreRef} aria-hidden="true" style={{height:1}}/>}</>:<div className="catalog-empty catalog-empty-v123">',
    1,
)

storefront.write_text(text, encoding="utf-8")

# Card gallery enhancer is unnecessary on PLP after rendering only Фото 1.
if layout.exists():
    layout_text = layout.read_text(encoding="utf-8")
    layout_text = layout_text.replace('import "../product-card-gallery.css";\n', '')
    layout_text = layout_text.replace('import { ProductCardGalleryEnhancer } from "../product-card-gallery";\n', '')
    layout_text = layout_text.replace('    <ProductCardGalleryEnhancer />\n', '')
    layout.write_text(layout_text, encoding="utf-8")

print("PLP image loading optimized: Фото 1 only on cards, Фото 2–3 on PDP, local /assets only, progressive card mounting enabled")
