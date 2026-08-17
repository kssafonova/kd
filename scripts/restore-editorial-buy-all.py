from pathlib import Path
import re

path = Path("app/page.tsx")
text = path.read_text()
text = text.replace('import { EditorialScenarioLanding } from "./editorial-scenario-landing";\n', '')

collections = '''function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  const [kind,setKind]=useState("ВСЕ");
  const visible=editorials.filter(item=>kind==="ВСЕ"||(kind==="КАПСУЛЫ"&&item.kind==="КАПСУЛА")||(kind==="КОЛЛЕКЦИИ"&&item.kind==="КОЛЛЕКЦИЯ"));
  return <div className="collections page"><div className="section-head"><p>EDITORIAL</p><h1>Коллекции и капсулы</h1></div><div className="center-tabs">{["ВСЕ","КАПСУЛЫ","КОЛЛЕКЦИИ"].map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div><div className="collection-grid">{visible.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ {item.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ"} <Icon name="arrow"/></span></div></button></article>)}</div></div>;
}'''
text, count = re.subn(r'function CollectionsView\(.*?\n}\n\nfunction LunaEditorialView', collections+'\n\nfunction LunaEditorialView', text, count=1, flags=re.S)
if count != 1: raise SystemExit("CollectionsView boundaries were not found")

editorial = '''function EditorialView({ editorial, selectProduct, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const [selecting,setSelecting]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>(items.map(item=>item.id));
  useEffect(()=>{setSelecting(false);setSelectedIds(items.map(item=>item.id))},[editorial.id]);
  const selectedItems=items.filter(item=>selectedIds.includes(item.id));
  const total=selectedItems.reduce((sum,item)=>sum+item.price,0);
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(itemId=>itemId!==id):[...current,id]);
  const handleBundle=()=>{if(!selecting){setSelecting(true);return}if(selectedItems.length)buyBundle(selectedItems)};
  return <div className="editorial-page"><section className="editorial-cover"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><p>{editorial.kind}</p><h1>{editorial.name}</h1></div></section><section className="editorial-words"><p>{editorial.lead}</p><span>{editorial.description}</span></section><img className="editorial-detail" src={assetUrl(editorial.images[1])} alt={`Детали ${editorial.name}`}/><section className="editorial-words narrow"><p>{editorial.detail}</p></section><section className="editorial-split"><img src={assetUrl(editorial.images[2])} alt="Предметы коллекции"/><img src={assetUrl(editorial.images[3])} alt="Образ коллекции"/></section><section className={`editorial-products ${selecting?"selection-mode":""}`}><div className="editorial-products-head"><div><p>В {editorial.kind==="КАПСУЛА"?"КАПСУЛЕ":"КОЛЛЕКЦИИ"}</p><h2>Соберите весь образ</h2>{selecting&&<div className="selection-help"><span>Отметьте предметы, которые хотите купить</span><button onClick={()=>setSelectedIds(selectedIds.length===items.length?[]:items.map(item=>item.id))}>{selectedIds.length===items.length?"Снять выбор":"Выбрать всё"}</button></div>}</div><button className="primary total-cta" disabled={selecting&&!selectedItems.length} onClick={handleBundle}><span>{selecting?"ДОБАВИТЬ В КОРЗИНУ":"ВЫКУПИТЬ ВСЮ "+(editorial.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ")}</span><b>{fmt(total)}</b></button></div><div className="product-grid">{items.map(item=><div className={`selectable-product ${selectedIds.includes(item.id)?"selected":""}`} key={`${editorial.id}-${item.id}`}>{selecting&&<label className="product-selector"><input type="checkbox" checked={selectedIds.includes(item.id)} onChange={()=>toggle(item.id)}/><span><Icon name="plus"/></span><b>{selectedIds.includes(item.id)?"Выбрано":"Выбрать"}</b></label>}<ProductCard product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)}/></div>)}</div></section></div>;
}'''
text, count = re.subn(r'function EditorialView\(.*?\n}\n\nfunction QuantityControl', editorial+'\n\nfunction QuantityControl', text, count=1, flags=re.S)
if count != 1: raise SystemExit("EditorialView boundaries were not found")

if "const addBundle = (items: Product[])" not in text:
  marker = "  const addFromPLP = (product: Product, chosenSize: string, quantity: number, unitPrice: number) => {"
  if marker not in text: raise SystemExit("addFromPLP insertion marker was not found")
  add_bundle = '''  const addBundle = (items: Product[]) => {
    const bundleItems: CartItem[] = items.map((product)=>{
      const variant=product.colorVariants?.find(v=>v.name===product.selectedColor)??product.colorVariants?.[0];
      const sku=findProductSku(product,product.selectedColor,product.selectedSize);
      return {...product,price:sku?.price??product.price,image:sku?.image??variant?.image??product.image,gallery:sku?.gallery??product.gallery,position:variant?.position??product.position,selectedSize:sku?.size??product.selectedSize??"",selectedColor:sku?.color??variant?.name??"Молочный",selectedSkuId:sku?.id,quantity:product.quantity??1};
    });
    setCart(current=>[...current,...bundleItems]);
    setCartOpen(true);
  };
'''
  text = text.replace(marker, add_bundle+marker, 1)

text, count = re.subn(r'\{view\s*===\s*"editorial"\s*&&\s*<EditorialView[^\n]*?/\>\}', '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}', text, count=1)
if count != 1: raise SystemExit("EditorialView root render was not found")

for marker in ['ВЫКУПИТЬ ВСЮ ','Соберите весь образ','buyBundle={addBundle}','["ВСЕ","КАПСУЛЫ","КОЛЛЕКЦИИ"]']:
  if marker not in text: raise SystemExit(f"Missing marker: {marker}")
if 'EditorialScenarioLanding' in text: raise SystemExit("Scenario landing still present")

path.write_text(text)
print("Restored pre-constructor Editorial buy-all flow")
