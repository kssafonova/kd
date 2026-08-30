from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
text = page_path.read_text(encoding="utf-8")

# Keep single-colour products visually clean in every catalogue ProductCard.
old_swatches = '<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>'
new_swatches = '{variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}'
if old_swatches in text:
    text = text.replace(old_swatches, new_swatches, 1)

# Pass the real cart action into the editorial so the capsule configurator can add all configured items at once.
old_render = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} />}'
new_render = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} addToCart={(product)=>add(product,product.selectedSize,product.quantity)} />}'
if old_render in text:
    text = text.replace(old_render, new_render, 1)

luna_component = r'''function LunaEditorialView({ editorial, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {
  const [storyId,setStoryId]=useState<string|null>(null);
  const [builderOpen,setBuilderOpen]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [configuredSizes,setConfiguredSizes]=useState<Record<number,string>>({});
  const [configuredQty,setConfiguredQty]=useState<Record<number,number>>({});

  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={
    4:"/assets/images/KD-PD-1024-DARK02.png",
    6:"/assets/images/KD-PD-1026-BLUE01.png",
    3:"/assets/images/KD-PD-1023-BLUE02.png",
  };
  const sceneFallbacks=["/assets/images/time-hero.png","/assets/images/blue-bedroom.png","/assets/images/night-editorial.png","/assets/images/time-table.png","/assets/images/time-tea-pair.png","/assets/images/moon-plate.png"];

  const prepareProduct=(product:Product):Product=>{
    const preferredColor=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const preferredImage=previewById[product.id];
    const variants=[...(product.colorVariants??[])];
    variants.sort((a,b)=>a.name===preferredColor?-1:b.name===preferredColor?1:0);
    const adjustedVariants=variants.map(variant=>variant.name===preferredColor&&preferredImage?{...variant,image:preferredImage}:variant);
    const adjustedSkus=product.skus?.map(sku=>sku.color===preferredColor&&preferredImage?{...sku,image:preferredImage,gallery:Array.from(new Set([preferredImage,...sku.gallery]))}:sku);
    const targetSku=adjustedSkus?.find(sku=>sku.color===preferredColor)??adjustedSkus?.[0];
    return {
      ...product,
      image:preferredImage??targetSku?.image??product.image,
      gallery:targetSku?.gallery??product.gallery,
      colorVariants:adjustedVariants.length?adjustedVariants:product.colorVariants,
      skus:adjustedSkus,
      selectedColor:targetSku?.color??preferredColor,
      selectedSize:targetSku?.size??product.selectedSize,
      selectedSkuId:targetSku?.id,
      price:targetSku?.price??product.price,
    };
  };

  const preparedItems=editorial.productIds.map(id=>products.find(product=>product.id===id)).filter(Boolean).map(item=>prepareProduct(item!));
  const itemById=(id:number)=>preparedItems.find(item=>item.id===id);
  const scenes=[
    {id:"bed-1",image:editorial.images[0],fallback:sceneFallbacks[0],kicker:"СПАЛЬНЯ",title:"Лунный сатин",copy:"Комплект постельного белья, плед и подушка в глубоком синем.",productIds:[4,6,3]},
    {id:"bed-2",image:editorial.images[1],fallback:sceneFallbacks[1],kicker:"ТЕКСТИЛЬ",title:"Слои ткани",copy:"Сатин и кружево собираются в спокойную многослойную композицию.",productIds:[4,3]},
    {id:"bed-3",image:editorial.images[2],fallback:sceneFallbacks[2],kicker:"ДЕТАЛИ",title:"Синий и кружево",copy:"Тактильные детали капсулы крупным планом.",productIds:[4,6,3]},
    {id:"table-1",image:editorial.images[3],fallback:sceneFallbacks[3],kicker:"СЕРВИРОВКА",title:"Поздний чай",copy:"Чайная пара и тарелка продолжают ночную палитру текстиля.",productIds:[10,5]},
    {id:"table-2",image:editorial.images[4],fallback:sceneFallbacks[4],kicker:"ФАРФОР",title:"Цвет ночного неба",copy:"Кобальтовый фарфор как самостоятельный акцент и часть общей истории.",productIds:[10,5]},
    {id:"table-3",image:editorial.images[5],fallback:sceneFallbacks[5],kicker:"ПОСЛЕ ЗАКАТА",title:"Дом после заката",copy:"Финальный образ соединяет сервировку и текстиль в одном визуальном ритме.",productIds:[10,5,3]},
  ];
  const activeStory=scenes.find(scene=>scene.id===storyId);
  const storyProducts=(activeStory?.productIds.map(itemById).filter(Boolean)??[]) as Product[];

  useEffect(()=>{
    if(!storyId&&!builderOpen)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[storyId,builderOpen]);

  const configuredProduct=(item:Product)=>{
    const color=colorById[item.id]??item.selectedColor;
    const sizes=getProductSizeOptions(item,color);
    const size=configuredSizes[item.id]??sizes[0]?.[0]??item.selectedSize??"";
    const sku=findProductSku(item,color,size);
    const quantity=configuredQty[item.id]??1;
    return {...item,price:sku?.price??item.price,image:sku?.image??item.image,gallery:sku?.gallery??item.gallery,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id,quantity};
  };
  const configuredTotal=selectedIds.reduce((sum,id)=>{const item=itemById(id);if(!item)return sum;const configured=configuredProduct(item);return sum+configured.price*(configured.quantity??1)},0);
  const toggleItem=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const addConfiguredCapsule=()=>{
    const chosen=selectedIds.map(itemById).filter(Boolean).map(item=>configuredProduct(item!));
    if(!chosen.length)return;
    setBuilderOpen(false);
    chosen.forEach(addToCart);
  };

  const editorialFrame=(scene:(typeof scenes)[number],className:string)=><figure className={`luna-premium-frame ${className}`}>
    <button type="button" className="luna-premium-image-button" onClick={()=>setStoryId(scene.id)} aria-label={`Открыть историю ${scene.title}`}><RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/></button>
    <figcaption><div><small>{scene.kicker}</small><strong>{scene.title}</strong></div><button type="button" onClick={()=>setStoryId(scene.id)}>СМОТРЕТЬ ИСТОРИЮ</button></figcaption>
  </figure>;

  return <div className="luna-editorial-page luna-premium-editorial">
    <section className="luna-premium-masthead"><p>КАПСУЛА · 2026</p><h1>Лунная сказка</h1><span>{editorial.lead}</span><button type="button" onClick={()=>setBuilderOpen(true)}>СОБРАТЬ КАПСУЛУ</button></section>

    <section className="luna-premium-hero">{editorialFrame(scenes[0],"hero-frame")}</section>

    <section className="luna-premium-copy"><p>НОВАЯ КАПСУЛА</p><h2>Дом в оттенках ночного неба</h2><span>{editorial.detail}</span></section>

    <section className="luna-premium-asym">
      <div className="luna-premium-asym-main">{editorialFrame(scenes[1],"tall-frame")}</div>
      <div className="luna-premium-asym-side"><div className="luna-premium-side-note"><p>01 / ТЕКСТИЛЬ</p><h3>Один цвет.<br/>Разный характер материалов.</h3><span>Большие спокойные поверхности сменяются камерными деталями, чтобы история читалась как журнал, а не как товарная сетка.</span></div>{editorialFrame(scenes[2],"compact-frame")}</div>
    </section>

    <section className="luna-premium-scroll-chapter"><header><p>02 / СЕРВИРОВКА</p><h2>История продолжается за столом</h2><span>Проведите по горизонтали — каждый кадр открывается отдельно.</span></header><div className="luna-premium-scroll">{editorialFrame(scenes[3],"scroll-wide")}{editorialFrame(scenes[4],"scroll-narrow")}</div></section>

    <section className="luna-premium-finale"><div className="luna-premium-finale-copy"><p>03 / AFTER DARK</p><h2>Предметы можно собрать в один комплект — или оставить только нужное.</h2><span>В конструкторе размеры и количество настраиваются сразу для всех позиций.</span><button type="button" onClick={()=>setBuilderOpen(true)}>НАСТРОИТЬ КАПСУЛУ</button></div>{editorialFrame(scenes[5],"finale-frame")}</section>

    <section className="luna-premium-builder-callout"><div><p>ЛУННАЯ СКАЗКА · 5 ПРЕДМЕТОВ</p><h2>Соберите капсулу за один шаг</h2><span>Выберите нужные позиции, размеры и количество — без переходов между карточками.</span></div><button type="button" onClick={()=>setBuilderOpen(true)}>СОБРАТЬ КАПСУЛУ</button></section>

    {!storyId&&!builderOpen&&<button className="luna-mobile-builder-bar" type="button" onClick={()=>setBuilderOpen(true)}>СОБРАТЬ КАПСУЛУ · {preparedItems.length}</button>}

    {activeStory&&<div className="luna-story-overlay" role="dialog" aria-modal="true" aria-label={`История ${activeStory.title}`}>
      <button className="luna-overlay-backdrop" onClick={()=>setStoryId(null)} aria-label="Закрыть историю"/>
      <section className="luna-story-sheet">
        <header className="luna-overlay-header"><div><small>{activeStory.kicker}</small><strong>{activeStory.title}</strong></div><button type="button" onClick={()=>setStoryId(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-story-body"><figure><RemoteImage src={activeStory.image} fallbackSrc={activeStory.fallback} alt={activeStory.title}/><figcaption>{activeStory.copy}</figcaption></figure><section className="luna-story-products"><div className="luna-story-products-head"><p>ПРЕДМЕТЫ ИЗ ИСТОРИИ</p><span>{storyProducts.length} {storyProducts.length===1?"товар":"товара"}</span></div><div className="luna-story-product-grid">{storyProducts.map(item=><ProductCard key={`story-${activeStory.id}-${item.id}`} product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div></section></div>
      </section>
    </div>}

    {builderOpen&&<div className="luna-builder-overlay" role="dialog" aria-modal="true" aria-label="Собрать капсулу Лунная сказка">
      <button className="luna-overlay-backdrop" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть конструктор"/>
      <section className="luna-builder-sheet">
        <header className="luna-overlay-header"><div><small>ЛУННАЯ СКАЗКА</small><strong>Соберите капсулу</strong></div><button type="button" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-builder-toolbar"><span>Выбрано {selectedIds.length} из {preparedItems.length}</span><button type="button" onClick={()=>setSelectedIds(selectedIds.length===preparedItems.length?[]:preparedItems.map(item=>item.id))}>{selectedIds.length===preparedItems.length?"СНЯТЬ ВСЕ":"ВЫБРАТЬ ВСЕ"}</button></div>
        <div className="luna-builder-items">{preparedItems.map(item=>{
          const selected=selectedIds.includes(item.id);
          const color=colorById[item.id]??item.selectedColor;
          const sizes=getProductSizeOptions(item,color);
          const size=configuredSizes[item.id]??sizes[0]?.[0]??item.selectedSize??"";
          const sku=findProductSku(item,color,size);
          const unitPrice=sku?.price??item.price;
          const quantity=configuredQty[item.id]??1;
          return <article className={`luna-config-item ${selected?"selected":""}`} key={item.id}>
            <button className="luna-config-toggle" type="button" onClick={()=>toggleItem(item.id)} aria-pressed={selected}><i>{selected?"✓":""}</i></button>
            <RemoteImage src={previewById[item.id]??item.image} alt={item.name}/>
            <div className="luna-config-copy"><small>{item.article}</small><h3>{item.name}</h3>{sizes.length>1?<label><span>Размер</span><select value={size} onChange={event=>setConfiguredSizes(current=>({...current,[item.id]:event.target.value}))}>{sizes.map(([option])=><option key={option} value={option}>{option}</option>)}</select></label>:<p>{size}</p>}<div className="luna-config-bottom"><strong>{fmt(unitPrice*quantity)}</strong><div className="luna-config-qty"><button type="button" onClick={()=>setConfiguredQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))}>−</button><span>{quantity}</span><button type="button" onClick={()=>setConfiguredQty(current=>({...current,[item.id]:quantity+1}))}>+</button></div></div></div>
          </article>})}</div>
        <footer className="luna-builder-footer"><div><span>{selectedIds.length} позиций</span><strong>{fmt(configuredTotal)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addConfiguredCapsule}>ДОБАВИТЬ В КОРЗИНУ</button></footer>
      </section>
    </div>}
  </div>;
}'''

if 'function LunaEditorialView' not in text:
    raise SystemExit("LunaEditorialView must exist before premium transform")
text, count = re.subn(r'function LunaEditorialView[\s\S]*?(?=\n\nfunction EditorialView)', luna_component.rstrip(), text, count=1)
if count != 1:
    raise SystemExit("Failed to replace LunaEditorialView")

old_signatures = [
  'function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void }) {',
  'function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {'
]
new_signature='function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {'
for old in old_signatures:
    if old in text:
        text=text.replace(old,new_signature,1)
        break
old_return='  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd}/>;'
new_return='  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd} addToCart={addToCart}/>;'
if old_return in text:
    text=text.replace(old_return,new_return,1)
elif new_return not in text:
    raise SystemExit("Luna EditorialView branch not found")

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_ZARA_EDITORIAL_V3 \*/[\s\S]*\Z', '', css)
css = re.sub(r'\n?/\* LUNA_PREMIUM_FLOW_V4 \*/[\s\S]*\Z', '', css)
css += r'''

/* LUNA_PREMIUM_FLOW_V4 */
.luna-premium-editorial{background:#fff;color:#1d1d1f;padding-bottom:120px}
.luna-premium-masthead{max-width:840px;margin:0 auto;padding:86px 28px 72px;text-align:center}
.luna-premium-masthead p,.luna-premium-copy p,.luna-premium-side-note p,.luna-premium-scroll-chapter header p,.luna-premium-finale-copy p,.luna-premium-builder-callout p{font-size:10px;letter-spacing:.15em;margin:0 0 16px}
.luna-premium-masthead h1{font-size:clamp(52px,7vw,104px);font-weight:400;line-height:.92;margin:0 0 26px}
.luna-premium-masthead span{display:block;max-width:600px;margin:0 auto 28px;font-size:14px;line-height:1.7;color:#606064}
.luna-premium-masthead>button,.luna-premium-finale-copy>button,.luna-premium-builder-callout>button{border:0;background:#1d1d1f;color:#fff;min-height:48px;padding:0 28px;font:inherit;font-size:10px;letter-spacing:.08em;cursor:pointer}
.luna-premium-hero{width:100%;padding:0}
.luna-premium-frame{margin:0}
.luna-premium-image-button{display:block;width:100%;padding:0;border:0;background:#f1f1ef;cursor:pointer;overflow:hidden}
.luna-premium-image-button img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .55s ease}
.luna-premium-image-button:hover img{transform:scale(1.008)}
.luna-premium-frame figcaption{display:flex;justify-content:space-between;align-items:flex-end;gap:18px;padding:14px 2px 0}
.luna-premium-frame figcaption>div{display:grid;gap:4px}
.luna-premium-frame figcaption small{font-size:9px;letter-spacing:.12em;color:#76767a}
.luna-premium-frame figcaption strong{font-size:16px;font-weight:400}
.luna-premium-frame figcaption>button{border:0;border-bottom:1px solid #1d1d1f;background:transparent;padding:0 0 4px;font:inherit;font-size:10px;letter-spacing:.07em;cursor:pointer;white-space:nowrap}
.hero-frame .luna-premium-image-button{height:min(88vh,1000px)}
.hero-frame figcaption{padding:14px 28px 0}
.luna-premium-copy{max-width:760px;margin:0 auto;padding:112px 28px 106px;text-align:center}
.luna-premium-copy h2,.luna-premium-scroll-chapter h2,.luna-premium-finale-copy h2,.luna-premium-builder-callout h2{font-size:clamp(32px,4vw,58px);font-weight:400;line-height:1.06;margin:0 0 20px}
.luna-premium-copy span,.luna-premium-side-note span,.luna-premium-scroll-chapter header span,.luna-premium-finale-copy span,.luna-premium-builder-callout span{font-size:14px;line-height:1.7;color:#616165}
.luna-premium-asym{max-width:1380px;margin:0 auto 118px;padding:0 34px;display:grid;grid-template-columns:minmax(0,1.5fr) minmax(300px,.7fr);gap:72px;align-items:end}
.tall-frame .luna-premium-image-button{aspect-ratio:4/5}
.luna-premium-asym-side{display:grid;gap:52px}
.luna-premium-side-note{max-width:420px;padding-right:30px}
.luna-premium-side-note h3{font-size:clamp(28px,3vw,46px);font-weight:400;line-height:1.08;margin:0 0 20px}
.compact-frame .luna-premium-image-button{aspect-ratio:4/5}
.luna-premium-scroll-chapter{padding:0 0 122px}
.luna-premium-scroll-chapter>header{max-width:680px;padding:0 34px 34px}
.luna-premium-scroll{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:0 34px 10px;scrollbar-width:none}
.luna-premium-scroll::-webkit-scrollbar{display:none}
.luna-premium-scroll .luna-premium-frame{flex:0 0 auto;scroll-snap-align:start}
.scroll-wide{width:min(72vw,1080px)}
.scroll-wide .luna-premium-image-button{aspect-ratio:16/10}
.scroll-narrow{width:min(43vw,620px)}
.scroll-narrow .luna-premium-image-button{aspect-ratio:4/5}
.luna-premium-finale{max-width:1380px;margin:0 auto 118px;padding:0 34px;display:grid;grid-template-columns:minmax(300px,.65fr) minmax(0,1.35fr);gap:70px;align-items:center}
.luna-premium-finale-copy{max-width:470px}
.luna-premium-finale-copy>button{margin-top:28px}
.finale-frame .luna-premium-image-button{aspect-ratio:4/5}
.luna-premium-builder-callout{max-width:1220px;margin:0 auto;padding:56px 34px;border-top:1px solid #dededb;border-bottom:1px solid #dededb;display:flex;align-items:end;justify-content:space-between;gap:40px}
.luna-premium-builder-callout>div{max-width:720px}
.luna-mobile-builder-bar{display:none}

.luna-story-overlay,.luna-builder-overlay{position:fixed;inset:0;z-index:90;display:grid;place-items:center;padding:24px}
.luna-overlay-backdrop{position:absolute;inset:0;border:0;background:rgba(10,15,24,.48);backdrop-filter:blur(4px)}
.luna-story-sheet,.luna-builder-sheet{position:relative;z-index:2;background:#fff;width:min(1380px,96vw);max-height:94vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 24px 80px rgba(0,0,0,.2)}
.luna-overlay-header{height:62px;display:flex;align-items:center;justify-content:space-between;padding:0 22px;border-bottom:1px solid #e9e9e6;flex:0 0 auto}
.luna-overlay-header>div{display:grid;gap:2px}.luna-overlay-header small{font-size:9px;letter-spacing:.13em;color:#747478}.luna-overlay-header strong{font-size:17px;font-weight:400}
.luna-overlay-header>button{width:36px;height:36px;border:0;background:transparent;padding:7px;cursor:pointer}.luna-overlay-header svg{width:22px;height:22px}
.luna-story-body{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(430px,.8fr);min-height:0;overflow:auto}
.luna-story-body>figure{margin:0;background:#eef0f1;min-height:0}.luna-story-body>figure img{display:block;width:100%;height:calc(94vh - 62px);object-fit:cover}.luna-story-body>figure figcaption{padding:12px 16px;font-size:11px;color:#666;display:none}
.luna-story-products{padding:30px 24px 44px;overflow:auto}.luna-story-products-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px}.luna-story-products-head p{font-size:10px;letter-spacing:.12em;margin:0}.luna-story-products-head span{font-size:11px;color:#777}
.luna-story-product-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 10px}.luna-story-product-grid .product-card{min-width:0}

.luna-builder-sheet{width:min(1040px,95vw)}
.luna-builder-toolbar{display:flex;justify-content:space-between;align-items:center;padding:16px 22px;border-bottom:1px solid #ecece9;font-size:11px}.luna-builder-toolbar button{border:0;background:transparent;font:inherit;font-size:10px;text-decoration:underline;text-underline-offset:4px;cursor:pointer}
.luna-builder-items{overflow:auto;padding:0 22px}
.luna-config-item{display:grid;grid-template-columns:28px 112px minmax(0,1fr);gap:18px;align-items:center;padding:18px 0;border-bottom:1px solid #ecece9;opacity:.45}.luna-config-item.selected{opacity:1}
.luna-config-toggle{width:22px;height:22px;border:1px solid #a9a9a5;background:#fff;padding:0;display:grid;place-items:center;cursor:pointer}.luna-config-item.selected .luna-config-toggle{background:#1d1d1f;color:#fff;border-color:#1d1d1f}.luna-config-toggle i{font-style:normal;font-size:12px}
.luna-config-item>img{width:112px;height:138px;object-fit:cover;background:#f2f2f0}.luna-config-copy{min-width:0}.luna-config-copy>small{font-size:9px;letter-spacing:.08em;color:#777}.luna-config-copy h3{font-size:16px;font-weight:400;margin:4px 0 12px}.luna-config-copy>p{font-size:11px;color:#777;margin:0 0 12px}.luna-config-copy label{display:flex;align-items:center;gap:14px;font-size:10px;margin-bottom:12px}.luna-config-copy select{min-width:210px;border:0;border-bottom:1px solid #aaa;background:#fff;padding:7px 20px 7px 0;font:inherit;font-size:11px}
.luna-config-bottom{display:flex;align-items:center;justify-content:space-between;gap:20px}.luna-config-bottom strong{font-size:13px;font-weight:400}.luna-config-qty{display:flex;align-items:center;border:1px solid #ddd}.luna-config-qty button{width:32px;height:30px;border:0;background:#fff;font-size:17px;cursor:pointer}.luna-config-qty span{min-width:28px;text-align:center;font-size:11px}
.luna-builder-footer{padding:16px 22px 18px;border-top:1px solid #e5e5e2;background:#fff;display:grid;grid-template-columns:1fr minmax(260px,360px);gap:20px;align-items:center}.luna-builder-footer>div{display:flex;justify-content:space-between;gap:20px;font-size:11px}.luna-builder-footer strong{font-size:16px;font-weight:400}.luna-builder-footer>button{border:0;background:#1d1d1f;color:#fff;min-height:48px;font:inherit;font-size:10px;letter-spacing:.06em;cursor:pointer}.luna-builder-footer>button:disabled{opacity:.35;cursor:not-allowed}

@media(max-width:900px){
  .luna-premium-editorial{padding-bottom:92px}
  .luna-premium-masthead{padding:58px 20px 44px;text-align:left}.luna-premium-masthead h1{font-size:56px}.luna-premium-masthead span{margin-left:0}.luna-premium-masthead>button{width:100%}
  .hero-frame .luna-premium-image-button{height:74svh;min-height:520px}.hero-frame figcaption{padding:12px 16px 0}
  .luna-premium-frame figcaption{align-items:center}.luna-premium-frame figcaption strong{font-size:14px}.luna-premium-frame figcaption>button{font-size:9px}
  .luna-premium-copy{padding:72px 20px 68px;text-align:left}
  .luna-premium-asym{display:block;padding:0 16px;margin-bottom:78px}.luna-premium-asym-main{width:100%}.luna-premium-asym-side{margin-top:68px;gap:34px}.luna-premium-side-note{padding:0 4px;max-width:90%}.compact-frame{width:78%;margin-left:auto}
  .luna-premium-scroll-chapter{padding-bottom:82px}.luna-premium-scroll-chapter>header{padding:0 20px 24px}.luna-premium-scroll{padding:0 16px 6px;gap:8px}.scroll-wide{width:86vw}.scroll-narrow{width:70vw}
  .luna-premium-finale{display:flex;flex-direction:column;padding:0 16px;margin-bottom:84px;gap:38px}.luna-premium-finale-copy{padding:0 4px}.finale-frame{width:100%}
  .luna-premium-builder-callout{margin:0 16px;padding:36px 4px;display:block}.luna-premium-builder-callout>button{width:100%;margin-top:26px}
  .luna-mobile-builder-bar{display:block;position:fixed;left:12px;right:12px;bottom:12px;z-index:38;height:50px;border:0;background:#1d1d1f;color:#fff;font:inherit;font-size:10px;letter-spacing:.06em;box-shadow:0 8px 24px rgba(0,0,0,.18)}

  .luna-story-overlay,.luna-builder-overlay{padding:0;place-items:stretch}.luna-overlay-backdrop{display:none}.luna-story-sheet,.luna-builder-sheet{width:100%;height:100dvh;max-height:none;box-shadow:none}.luna-overlay-header{height:56px;padding:0 14px;position:sticky;top:0;z-index:3;background:#fff}.luna-overlay-header>button{width:40px;height:40px}
  .luna-story-body{display:block;overflow:auto}.luna-story-body>figure img{height:44svh;min-height:300px}.luna-story-body>figure figcaption{display:block;padding:12px 16px 0;background:#fff;line-height:1.5}.luna-story-products{padding:22px 12px 44px;overflow:visible}.luna-story-products-head{padding:0 4px;margin-bottom:14px}.luna-story-product-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 6px}.luna-story-product-grid .product-copy small{font-size:9px}
  .luna-builder-toolbar{padding:13px 14px}.luna-builder-items{padding:0 14px}.luna-config-item{grid-template-columns:24px 86px minmax(0,1fr);gap:12px;padding:14px 0}.luna-config-item>img{width:86px;height:108px}.luna-config-copy h3{font-size:13px;margin-bottom:8px}.luna-config-copy label{display:grid;gap:4px;margin-bottom:8px}.luna-config-copy select{width:100%;min-width:0}.luna-config-bottom{gap:8px}.luna-config-qty button{width:28px;height:28px}.luna-builder-footer{grid-template-columns:1fr;padding:12px 14px calc(12px + env(safe-area-inset-bottom));gap:10px}.luna-builder-footer>button{width:100%}
}
'''
css_path.write_text(css, encoding="utf-8")
print("Applied premium Luna editorial overlays, capsule builder and single-colour swatch cleanup")
