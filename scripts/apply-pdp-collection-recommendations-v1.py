from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

catalog = CATALOG.read_text(encoding="utf-8")
if "capsule?:string;" not in catalog:
    catalog = catalog.replace("  collection?:string;\n", "  collection?:string;\n  capsule?:string;\n", 1)
CATALOG.write_text(catalog, encoding="utf-8")

page = PAGE.read_text(encoding="utf-8")

replacement = r'''function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  const merchGroupOf=(item:Product)=>{
    const preferred=findProductSku(item,item.selectedColor,item.selectedSize);
    const rows=preferred?[preferred,...(item.skus??[]).filter(sku=>sku.id!==preferred.id)]:(item.skus??[]);
    for(const row of rows){
      const value=(row.collection??row.capsule)?.trim();
      if(value)return value.toLocaleLowerCase("ru-RU");
    }
    return "";
  };
  const currentMerchGroup=merchGroupOf(product);
  const collectionProducts=currentMerchGroup
    ? products.filter(item=>item.id!==product.id&&merchGroupOf(item)===currentMerchGroup).slice(0,4)
    : [];
  const viewedProducts=recentlyViewed
    .filter(id=>id!==product.id)
    .map(id=>products.find(item=>item.id===id))
    .filter((item): item is Product=>Boolean(item))
    .slice(0,4);
  return <>
    {collectionProducts.length>0&&<section className="post-rich-recommendations collection-recommendations"><div className="section-head"><p>КОЛЛЕКЦИЯ / КАПСУЛА</p><h2>Товары из этой коллекции</h2></div><ProductRail className="recommendation-product-rail" items={collectionProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
    {viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><ProductRail className="recommendation-product-rail" items={viewedProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
  </>;
}

function Menu'''

pattern = r'function ProductRecommendations\(\{product,selectProduct,favorite,recentlyViewed\}[\s\S]*?\n\}\n\nfunction Menu'
page, count = re.subn(pattern, replacement, page, count=1)
if count != 1:
    raise SystemExit("Could not patch ProductRecommendations")

PAGE.write_text(page, encoding="utf-8")
print("Applied collection/capsule-aware PDP recommendations")
