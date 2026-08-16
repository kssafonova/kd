from pathlib import Path

path = Path("app/page.tsx")
text = path.read_text()

root_old = '{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} buyBundle={addBundle} selectProduct={openProduct} />}'
root_new = '{view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} buyBundle={addBundle} selectProduct={openProduct} recentlyViewed={recentlyViewed} />}'
if root_old in text:
    text = text.replace(root_old, root_new, 1)

sig_old = 'function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; buyBundle:(items:Product[])=>void; selectProduct:(p:Product)=>void }) {'
sig_new = 'function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; buyBundle:(items:Product[])=>void; selectProduct:(p:Product)=>void; recentlyViewed:number[] }) {'
if sig_old in text:
    text = text.replace(sig_old, sig_new, 1)

call_old = '<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite}/>'
call_new = '<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>'
if call_old in text:
    text = text.replace(call_old, call_new, 1)

component_old = '''function ProductRecommendations({product,selectProduct,favorite}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void}){
  const recommendations=products.filter(item=>item.id!==product.id).slice(0,4);
  return <section className="post-rich-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Вам может понравиться</h2></div><div>{recommendations.map(item=><ProductCard key={`recommendation-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>;
}'''

component_new = '''function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  const categoryGroups=[
    [1,2,4,8,12],
    [3,6,7,11],
    [5,9,10]
  ];
  const categoryIds=categoryGroups.find(group=>group.includes(product.id))??products.map(item=>item.id);
  const categoryProducts=products.filter(item=>item.id!==product.id&&categoryIds.includes(item.id)).slice(0,4);
  const viewedProducts=recentlyViewed
    .filter(id=>id!==product.id)
    .map(id=>products.find(item=>item.id===id))
    .filter((item): item is Product=>Boolean(item))
    .slice(0,4);
  return <>
    <section className="post-rich-recommendations category-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Товары из этой категории</h2></div><div>{categoryProducts.map(item=><ProductCard key={`category-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>
    {viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><div>{viewedProducts.map(item=><ProductCard key={`recent-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>}
  </>;
}'''

if component_old in text:
    text = text.replace(component_old, component_new, 1)
elif 'Товары из этой категории' not in text:
    raise SystemExit('ProductRecommendations component marker not found')

required = [
    'recentlyViewed={recentlyViewed}',
    'Товары из этой категории',
    'Вы недавно смотрели',
]
for marker in required:
    if marker not in text:
        raise SystemExit(f'Missing marker after patch: {marker}')

path.write_text(text)
