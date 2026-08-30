from pathlib import Path
import re

page_path=Path("app/page.tsx")
css_path=Path("app/globals.css")
text=page_path.read_text(encoding="utf-8")

component=r'''function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {
  const [story,setStory]=useState<"bedroom"|"table"|null>(null);
  const [builderOpen,setBuilderOpen]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [qty,setQty]=useState<Record<number,number>>({});
  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={4:"/assets/images/KD-PD-1024-DARK02.png",6:"/assets/images/KD-PD-1026-BLUE01.png",3:"/assets/images/KD-PD-1023-BLUE02.png"};
  const fallbacks=["/assets/images/time-hero.png","/assets/images/blue-bedroom.png","/assets/images/night-editorial.png","/assets/images/time-table.png","/assets/images/time-tea-pair.png","/assets/images/moon-plate.png"];

  const prepare=(product:Product):Product=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const preview=previewById[product.id];
    const skus=product.skus?.map(s=>s.color===color&&preview?{...s,image:preview,gallery:Array.from(new Set([preview,...s.gallery]))}:s);
    const sku=skus?.find(s=>s.color===color)??skus?.[0];
    return {...product,image:preview??sku?.image??product.image,gallery:sku?.gallery??product.gallery,skus,selectedColor:sku?.color??color,selectedSize:sku?.size??product.selectedSize,selectedSkuId:sku?.id,price:sku?.price??product.price};
  };
  const items=editorial.productIds.map(id=>products.find(p=>p.id===id)).filter(Boolean).map(p=>prepare(p!));
  const itemById=(id:number)=>items.find(p=>p.id===id);
  const groups=[
    {id:"bedroom" as const,title:"Спальня",images:editorial.images.slice(0,3),fallbacks:fallbacks.slice(0,3),productIds:[4,6,3]},
    {id:"table" as const,title:"Сервировка",images:editorial.images.slice(3,6),fallbacks:fallbacks.slice(3,6),productIds:[10,5,3]}
  ];
  const active=groups.find(g=>g.id===story);
  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];

  useEffect(()=>{if(!story&&!builderOpen)return;const old=document.body.style.overflow;document.body.style.overflow="hidden";return()=>{document.body.style.overflow=old}},[story,builderOpen]);

  const configured=(item:Product)=>{
    const color=colorById[item.id]??item.selectedColor;
    const options=getProductSizeOptions(item,color);
    const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";
    const sku=findProductSku(item,color,size);
    const quantity=qty[item.id]??1;
    return {...item,price:sku?.price??item.price,image:sku?.image??item.image,gallery:sku?.gallery??item.gallery,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id,quantity};
  };
  const total=selectedIds.reduce((sum,id)=>{const item=itemById(id);if(!item)return sum;const p=configured(item);return sum+p.price*(p.quantity??1)},0);
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(x=>x!==id):[...current,id]);
  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);chosen.forEach(addToCart)};

  const gallery=(group:(typeof groups)[number],reverse=false)=><section className={`luna-clean-group ${reverse?"reverse":""}`}>
    <h2>{group.title}</h2>
    <div className="luna-clean-gallery">{group.images.map((src,i)=><button key={`${group.id}-${i}`} type="button" onClick={()=>setStory(group.id)}><RemoteImage src={src} fallbackSrc={group.fallbacks[i]} alt={`${group.title}, кадр ${i+1}`}/></button>)}</div>
    <button className="luna-clean-link" type="button" onClick={()=>setStory(group.id)}>СМОТРЕТЬ ИСТОРИЮ</button>
  </section>;

  return <div className="luna-clean-page">
    <section className="luna-clean-head"><p>КАПСУЛА</p><h1>Лунная сказка</h1><span>{editorial.lead}</span></section>
    {gallery(groups[0])}
    {gallery(groups[1],true)}
    <section className="luna-clean-builder-entry"><h2>Соберите капсулу</h2><button type="button" onClick={()=>setBuilderOpen(true)}>СОБРАТЬ КАПСУЛУ</button></section>

    {active&&<div className="luna-clean-overlay" role="dialog" aria-modal="true">
      <button className="luna-clean-backdrop" onClick={()=>setStory(null)} aria-label="Закрыть"/>
      <section className="luna-clean-story">
        <header><strong>{active.title}</strong><button type="button" onClick={()=>setStory(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-clean-story-images">{active.images.map((src,i)=><RemoteImage key={`${active.id}-story-${i}`} src={src} fallbackSrc={active.fallbacks[i]} alt={`${active.title}, кадр ${i+1}`}/>)}</div>
        <div className="luna-clean-products">{storyProducts.map(item=><ProductCard key={`${active.id}-${item.id}`} product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
      </section>
    </div>}

    {builderOpen&&<div className="luna-clean-overlay" role="dialog" aria-modal="true">
      <button className="luna-clean-backdrop" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"/>
      <section className="luna-clean-builder">
        <header><strong>Соберите капсулу</strong><button type="button" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-clean-builder-tools"><span>{selectedIds.length} из {items.length}</span><button type="button" onClick={()=>setSelectedIds(selectedIds.length===items.length?[]:items.map(i=>i.id))}>{selectedIds.length===items.length?"СНЯТЬ ВСЕ":"ВЫБРАТЬ ВСЕ"}</button></div>
        <div className="luna-clean-builder-list">{items.map(item=>{const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const sku=findProductSku(item,color,size);const price=sku?.price??item.price;const quantity=qty[item.id]??1;return <article className={selected?"selected":""} key={item.id}>
          <button className="luna-clean-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected}>{selected?"✓":""}</button>
          <RemoteImage src={previewById[item.id]??item.image} alt={item.name}/>
          <div><h3>{item.name}</h3>{options.length>1?<select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select>:<small>{size}</small>}<div className="luna-clean-row"><strong>{fmt(price*quantity)}</strong><span><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))}>−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))}>+</button></span></div></div>
        </article>})}</div>
        <footer><div><span>{selectedIds.length} позиций</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addAll}>ДОБАВИТЬ В КОРЗИНУ</button></footer>
      </section>
    </div>}
  </div>;
}'''

text,count=re.subn(r'function LunaEditorialView[\s\S]*?(?=\n\nfunction EditorialView)',component,text,count=1)
if count!=1: raise SystemExit("LunaEditorialView replacement failed")
page_path.write_text(text,encoding="utf-8")

css=css_path.read_text(encoding="utf-8")
css=re.sub(r'\n?/\* LUNA_(?:ZARA_EDITORIAL_V3|PREMIUM_EDITORIAL_V4|CLEAN_GROUPS_V6) \*/[\s\S]*\Z','',css)
css+=r'''

/* LUNA_CLEAN_GROUPS_V6 */
.luna-clean-page{background:#fff;color:#1d1d1f}
.luna-clean-head{max-width:680px;margin:auto;padding:76px 24px 70px;text-align:center}.luna-clean-head p{font-size:10px;letter-spacing:.15em;margin:0 0 14px}.luna-clean-head h1{font-size:clamp(46px,6vw,86px);font-weight:400;line-height:.98;margin:0 0 20px}.luna-clean-head span{font-size:14px;line-height:1.55;color:#666}
.luna-clean-group{max-width:1380px;margin:0 auto 112px;padding:0 28px}.luna-clean-group h2{font-size:21px;font-weight:400;margin:0 0 16px}.luna-clean-gallery{display:grid;grid-template-columns:1.6fr .75fr;grid-template-rows:1fr 1fr;gap:9px}.luna-clean-gallery button{border:0;background:#f4f4f2;padding:0;overflow:hidden;cursor:pointer}.luna-clean-gallery button:first-child{grid-row:1/3}.luna-clean-gallery img{width:100%;height:100%;display:block;object-fit:cover}.luna-clean-gallery button:first-child img{aspect-ratio:1.35/1}.luna-clean-gallery button:not(:first-child) img{aspect-ratio:1.5/1}.luna-clean-group.reverse .luna-clean-gallery{grid-template-columns:.75fr 1.6fr}.luna-clean-group.reverse .luna-clean-gallery button:first-child{grid-column:2}.luna-clean-group.reverse .luna-clean-gallery button:nth-child(n+2){grid-column:1}.luna-clean-link{margin-top:16px;border:0;border-bottom:1px solid;background:transparent;padding:0 0 4px;font:inherit;font-size:11px;letter-spacing:.08em;cursor:pointer}
.luna-clean-builder-entry{border-top:1px solid #e8e8e5;padding:68px 24px 80px;text-align:center;background:#fff}.luna-clean-builder-entry h2{font-size:36px;font-weight:400;margin:0 0 22px}.luna-clean-builder-entry button,.luna-clean-builder footer>button{height:44px;border:0;background:#1d1d1f;color:#fff;padding:0 24px;font:inherit;font-size:10px;letter-spacing:.08em;cursor:pointer}
.luna-clean-overlay{position:fixed;inset:0;z-index:55;display:flex;align-items:center;justify-content:center;padding:24px}.luna-clean-backdrop{position:absolute;inset:0;border:0;background:rgba(0,0,0,.22)}.luna-clean-story,.luna-clean-builder{position:relative;background:#fff;width:min(1120px,96vw);max-height:92vh;overflow:auto;box-shadow:0 16px 60px rgba(0,0,0,.14)}.luna-clean-story>header,.luna-clean-builder>header{height:56px;position:sticky;top:0;z-index:4;background:#fff;border-bottom:1px solid #ecece9;display:flex;align-items:center;justify-content:space-between;padding:0 18px}.luna-clean-story header strong,.luna-clean-builder header strong{font-size:14px;font-weight:400}.luna-clean-story header button,.luna-clean-builder header button{width:34px;height:34px;border:0;background:transparent;padding:6px}.luna-clean-story header svg,.luna-clean-builder header svg{width:100%;height:100%}
.luna-clean-story-images{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;padding:16px}.luna-clean-story-images img{width:100%;aspect-ratio:4/5;object-fit:cover}.luna-clean-products{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:10px 16px 28px}
.luna-clean-builder{width:min(820px,96vw)}.luna-clean-builder-tools{display:flex;justify-content:space-between;padding:12px 18px;border-bottom:1px solid #ecece9;font-size:11px}.luna-clean-builder-tools button{border:0;background:transparent;font:inherit;font-size:10px;text-decoration:underline}.luna-clean-builder-list{padding:0 18px 108px}.luna-clean-builder-list article{display:grid;grid-template-columns:30px 96px 1fr;gap:12px;align-items:center;padding:16px 0;border-bottom:1px solid #ecece9;opacity:.4}.luna-clean-builder-list article.selected{opacity:1}.luna-clean-builder-list article>img{width:96px;height:116px;object-fit:cover}.luna-clean-check{width:22px;height:22px;border:1px solid #aaa;background:#fff}.selected .luna-clean-check{background:#1d1d1f;color:#fff;border-color:#1d1d1f}.luna-clean-builder-list h3{font-size:14px;font-weight:400;margin:0 0 9px}.luna-clean-builder-list select{height:34px;max-width:300px;border:1px solid #d8d8d5;background:#fff;padding:0 8px;font:inherit;font-size:11px}.luna-clean-builder-list small{font-size:10px;color:#666}.luna-clean-row{display:flex;align-items:center;justify-content:space-between;margin-top:10px}.luna-clean-row strong{font-size:13px;font-weight:400}.luna-clean-row>span{display:flex;align-items:center;border:1px solid #ddd}.luna-clean-row>span button{width:30px;height:30px;border:0;background:#fff;font-size:15px}.luna-clean-row b{width:24px;text-align:center;font-size:11px;font-weight:400}.luna-clean-builder footer{position:sticky;bottom:0;background:#fff;border-top:1px solid #ddd;display:flex;align-items:center;justify-content:space-between;padding:12px 18px;gap:16px}.luna-clean-builder footer>div{display:grid}.luna-clean-builder footer span{font-size:10px;color:#666}.luna-clean-builder footer strong{font-size:17px;font-weight:400}
@media(max-width:700px){.luna-clean-head{padding:48px 20px 46px}.luna-clean-head h1{font-size:48px}.luna-clean-head span{font-size:13px}.luna-clean-group{padding:0;margin-bottom:70px}.luna-clean-group h2{padding:0 16px;font-size:18px;margin-bottom:11px}.luna-clean-gallery,.luna-clean-group.reverse .luna-clean-gallery{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:7px;padding:0 16px;scrollbar-width:none}.luna-clean-gallery::-webkit-scrollbar{display:none}.luna-clean-gallery button,.luna-clean-group.reverse .luna-clean-gallery button,.luna-clean-group.reverse .luna-clean-gallery button:first-child,.luna-clean-group.reverse .luna-clean-gallery button:nth-child(n+2){flex:0 0 84vw;grid-column:auto;grid-row:auto;scroll-snap-align:start}.luna-clean-gallery img,.luna-clean-gallery button:first-child img,.luna-clean-gallery button:not(:first-child) img{width:84vw;height:62vh;min-height:420px;max-height:590px;aspect-ratio:auto;object-fit:cover}.luna-clean-link{margin:13px 16px 0}.luna-clean-builder-entry{padding:50px 20px 62px}.luna-clean-builder-entry h2{font-size:30px}.luna-clean-overlay{padding:0;align-items:stretch}.luna-clean-story,.luna-clean-builder{width:100%;max-width:none;height:100dvh;max-height:none;box-shadow:none}.luna-clean-story-images{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;padding:0;gap:0;scrollbar-width:none}.luna-clean-story-images::-webkit-scrollbar{display:none}.luna-clean-story-images img{flex:0 0 100vw;width:100vw;height:48vh;min-height:320px;aspect-ratio:auto;scroll-snap-align:start}.luna-clean-products{grid-template-columns:repeat(2,1fr);padding:18px 10px 28px;gap:8px}.luna-clean-builder-list{padding:0 12px 104px}.luna-clean-builder-list article{grid-template-columns:26px 78px 1fr;gap:9px;padding:13px 0}.luna-clean-builder-list article>img{width:78px;height:100px}.luna-clean-builder-list select{width:100%}.luna-clean-builder footer{padding:11px 12px env(safe-area-inset-bottom,11px)}}
'''
css_path.write_text(css,encoding="utf-8")
print("Applied clean grouped Luna editorial")
