from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

# PDP_CROSS_SELL_V1
new_recommendations = r'''function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  void recentlyViewed;
  const merchGroupOf=(item:Product)=>{
    const preferred=findProductSku(item,item.selectedColor,item.selectedSize);
    const rows=preferred?[preferred,...(item.skus??[]).filter(sku=>sku.id!==preferred.id)]:(item.skus??[]);
    for(const row of rows){
      const value=(row.collection??row.capsule)?.trim();
      if(value)return value;
    }
    return "";
  };
  const currentMerchGroup=merchGroupOf(product);
  const editorialGroup=editorials.find(item=>item.productIds.includes(product.id));
  const collectionProducts=currentMerchGroup
    ? products.filter(item=>item.id!==product.id&&merchGroupOf(item)===currentMerchGroup).slice(0,4)
    : editorialGroup
      ? editorialGroup.productIds.filter(id=>id!==product.id).map(id=>products.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)).slice(0,4)
      : [];

  const familyOf=(item:Product)=>{
    const value=`${item.name} ${item.note}`.toLowerCase();
    if(/комплект|постель|пододеяль|простын|наволоч/.test(value))return "bedding";
    if(/подуш/.test(value))return "pillow";
    if(/плед|покрывал|одеял/.test(value))return "throw";
    if(/тарел|салатник|сервиз|чайная пара|чаш|бокал|стакан|графин|прибор/.test(value))return "table";
    if(/свеч|аромат|ваза|декор|плейсмат/.test(value))return "decor";
    if(/халат|пижам|сороч|домашн.*одежд/.test(value))return "homewear";
    return "other";
  };
  const preferences:Record<string,string[]>={
    bedding:["pillow","throw","decor"],
    pillow:["bedding","throw","decor"],
    throw:["pillow","bedding","decor"],
    table:["table","decor"],
    decor:["table","bedding","pillow"],
    homewear:["bedding","decor"],
    other:["decor","table","pillow","throw"],
  };
  const currentFamily=familyOf(product);
  const preferredFamilies=preferences[currentFamily]??preferences.other;
  const excludedIds=new Set([product.id,...collectionProducts.map(item=>item.id)]);
  const complementaryProducts=products
    .filter(item=>!excludedIds.has(item.id))
    .map(item=>({item,rank:preferredFamilies.indexOf(familyOf(item))}))
    .filter(entry=>entry.rank>=0)
    .sort((a,b)=>a.rank-b.rank||Number(Boolean(b.item.badge))-Number(Boolean(a.item.badge))||a.item.id-b.item.id)
    .map(entry=>entry.item)
    .slice(0,4);

  return <>
    {collectionProducts.length>0&&<section className="post-rich-recommendations collection-recommendations"><div className="section-head"><p>КОЛЛЕКЦИЯ / КАПСУЛА</p><h2>Товары из этой коллекции</h2></div><ProductRail className="recommendation-product-rail" items={collectionProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
    {complementaryProducts.length>0&&<section className="post-rich-recommendations complementary-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ПОДОБРАНО К ЭТОМУ ТОВАРУ</p><h2>Дополните образ</h2></div><ProductRail className="recommendation-product-rail" items={complementaryProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
  </>;
}'''

start = page.find("function ProductRecommendations(")
end = page.find("function QuantityControl", start)
if start < 0 or end < 0:
    raise SystemExit("ProductRecommendations function anchors not found")
page = page[:start] + new_recommendations + "\n\n" + page[end:]

page_path.write_text(page, encoding="utf-8")
print("Applied PDP complementary merchandising block and removed recently viewed from PDP")
