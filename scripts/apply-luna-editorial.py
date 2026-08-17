from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")
text = page_path.read_text(encoding="utf-8")

luna_entry = '''  { id:"luna", name:"Лунная сказка", kind:"КАПСУЛА", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Интерактивный editorial о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png","/images/editorial/caps_luna_serviz2.png","/images/editorial/caps_luna_serviz3.png"], productIds:[4,10,5,6,3] },\n'''
editorial_marker = 'const editorials:Editorial[] = [\n'
if 'id:"luna"' not in text:
    if editorial_marker not in text:
        raise SystemExit("Editorial catalogue marker not found")
    text = text.replace(editorial_marker, editorial_marker + luna_entry, 1)

render_variants = [
    '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}',
    '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} add={(product)=>add(product,product.selectedSize,product.quantity)} />}',
    '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} />}',
]
new_render = '{view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} />}'
for old in render_variants:
    if old in text:
        text = text.replace(old, new_render, 1)
        break
else:
    raise SystemExit("EditorialView render marker not found")

luna_component = r'''function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void }) {
  const [activeScene,setActiveScene]=useState<string|null>(null);

  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={
    4:"/images/products/KD-PD-1024-DARK02.png",
    6:"/images/products/KD-PD-1026-BLUE01.png",
    3:"/images/products/KD-PD-1023-BLUE02.png",
  };
  const sceneFallbacks=["/images/time-hero.png","/images/blue-bedroom.png","/images/night-editorial.png","/images/time-table.png","/images/time-tea-pair.png","/images/moon-plate.png"];

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
    {id:"bed-1",image:editorial.images[0],fallback:sceneFallbacks[0],kicker:"СПАЛЬНЯ",title:"Лунный сатин",productIds:[4,6,3]},
    {id:"bed-2",image:editorial.images[1],fallback:sceneFallbacks[1],kicker:"СПАЛЬНЯ",title:"Слои ткани",productIds:[4,3]},
    {id:"bed-3",image:editorial.images[2],fallback:sceneFallbacks[2],kicker:"ДЕТАЛИ",title:"Синий и кружево",productIds:[4,6,3]},
    {id:"table-1",image:editorial.images[3],fallback:sceneFallbacks[3],kicker:"СЕРВИРОВКА",title:"Поздний чай",productIds:[10,5]},
    {id:"table-2",image:editorial.images[4],fallback:sceneFallbacks[4],kicker:"ФАРФОР",title:"Цвет ночного неба",productIds:[10,5]},
    {id:"table-3",image:editorial.images[5],fallback:sceneFallbacks[5],kicker:"СЕРВИРОВКА",title:"После заката",productIds:[10,5,3]},
  ];
  const currentScene=scenes.find(scene=>scene.id===activeScene);
  const currentProducts=(currentScene?.productIds.map(itemById).filter(Boolean)??[]) as Product[];
  const bedroomActive=Boolean(currentScene&&scenes.slice(0,3).some(scene=>scene.id===currentScene.id));
  const tableActive=Boolean(currentScene&&scenes.slice(3).some(scene=>scene.id===currentScene.id));

  const productGrid=(items:Product[],label:string)=><section className="luna-catalog-products" aria-live="polite">
    <div className="section-head row"><div><p>ТОВАРЫ НА ФОТО</p><h2>{label}</h2></div><span>{items.length} товаров</span></div>
    <div className="product-grid">{items.map(item=><ProductCard key={`luna-${activeScene}-${item.id}`} product={item} onClick={selectProduct} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
  </section>;

  return <div className="luna-editorial-page luna-catalog-ux">
    <section className="luna-hero">
      <RemoteImage src={editorial.images[0]} fallbackSrc={sceneFallbacks[0]} alt="Капсула Лунная сказка — спальня"/>
      <div className="luna-hero-shade"/>
      <div className="luna-hero-copy"><p>КАПСУЛА · 2026</p><h1>Лунная сказка</h1><span>{editorial.lead}</span><button type="button" className="luna-catalog-link" onClick={()=>document.getElementById("luna-products")?.scrollIntoView({behavior:"smooth"})}>СМОТРЕТЬ ТОВАРЫ →</button></div>
    </section>

    <section className="luna-intro">
      <p>EDITORIAL</p>
      <h2>Ночная история для современного дома</h2>
      <span>{editorial.detail}</span>
    </section>

    <section className="luna-story-section">
      <div className="luna-story-heading"><p>01 / СПАЛЬНЯ</p><h2>Текстиль в оттенках ночного неба</h2><span>Нажмите на фотографию — ниже появятся товары из этого кадра.</span></div>
      <div className="luna-story-grid luna-story-grid-bedroom">{scenes.slice(0,3).map(scene=><button type="button" key={scene.id} className={`luna-story-card-simple ${activeScene===scene.id?"active":""}`} onClick={()=>setActiveScene(scene.id)} aria-pressed={activeScene===scene.id}>
        <RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/><span><small>{scene.kicker}</small><strong>{scene.title}</strong><em>Товары на фото</em></span>
      </button>)}</div>
    </section>
    {bedroomActive&&productGrid(currentProducts,currentScene?.title??"Товары из образа")}

    <section className="luna-editorial-divider"><p>Лунная сказка строится на одной палитре, но каждый предмет можно выбрать отдельно.</p></section>

    <section className="luna-story-section">
      <div className="luna-story-heading"><p>02 / СЕРВИРОВКА</p><h2>Фарфор как продолжение интерьера</h2><span>Тот же принцип покупки: обычные карточки каталога и стандартное добавление в корзину.</span></div>
      <div className="luna-story-grid luna-story-grid-table">{scenes.slice(3).map(scene=><button type="button" key={scene.id} className={`luna-story-card-simple ${activeScene===scene.id?"active":""}`} onClick={()=>setActiveScene(scene.id)} aria-pressed={activeScene===scene.id}>
        <RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/><span><small>{scene.kicker}</small><strong>{scene.title}</strong><em>Товары на фото</em></span>
      </button>)}</div>
    </section>
    {tableActive&&productGrid(currentProducts,currentScene?.title??"Товары из образа")}

    <section className="luna-product-catalog" id="luna-products">
      <div className="section-head row"><div><p>ЛУННАЯ СКАЗКА</p><h2>Соберите комплект</h2></div><span>Добавляйте нужные предметы так же, как в обычном каталоге.</span></div>
      <div className="product-grid">{preparedItems.map(item=><ProductCard key={`luna-all-${item.id}`} product={item} onClick={selectProduct} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
    </section>
  </div>;
}
'''

if 'function LunaEditorialView' in text:
    text, count = re.subn(r'function LunaEditorialView[\s\S]*?(?=\n\nfunction EditorialView)', luna_component.rstrip(), text, count=1)
    if count != 1:
        raise SystemExit("Failed to replace LunaEditorialView")
else:
    marker = '\nfunction EditorialView('
    if marker not in text:
        raise SystemExit("EditorialView insertion marker not found")
    text = text.replace(marker, '\n' + luna_component + '\nfunction EditorialView(', 1)

old_editorial_signatures = [
    'function EditorialView({ editorial, selectProduct, favorite, favorites }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {',
    'function EditorialView({ editorial, selectProduct, favorite, favorites, add }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; add:(product:Product)=>void }) {',
    'function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void }) {',
]
new_signature = 'function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void }) {'
for old in old_editorial_signatures:
    if old in text:
        text = text.replace(old, new_signature, 1)
        break
else:
    raise SystemExit("EditorialView signature marker not found")

luna_return_patterns = [
    '  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} add={add}/>;\n',
    '  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd}/>;\n',
]
new_luna_return = '  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd}/>;\n'
inserted = False
for old in luna_return_patterns:
    if old in text:
        text = text.replace(old, new_luna_return, 1)
        inserted = True
        break
if not inserted:
    signature_pos = text.find(new_signature)
    if signature_pos < 0:
        raise SystemExit("Cannot locate EditorialView for Luna branch")
    line_end = text.find('\n', signature_pos)
    text = text[:line_end+1] + new_luna_return + text[line_end+1:]

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_CATALOG_UX_V2 \*/[\s\S]*\Z', '', css)
css += r'''

/* LUNA_CATALOG_UX_V2 */
.luna-catalog-ux{background:#fff;color:#1d1d1f;padding-bottom:96px}
.luna-catalog-ux .luna-hero{position:relative;min-height:72vh;margin:0;overflow:hidden;background:#eceff2}
.luna-catalog-ux .luna-hero>img{width:100%;height:72vh;object-fit:cover;display:block}
.luna-catalog-ux .luna-hero-shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,15,25,.42),rgba(8,15,25,.08) 55%,transparent)}
.luna-catalog-ux .luna-hero-copy{position:absolute;left:5vw;bottom:9%;max-width:520px;color:#fff;z-index:2}
.luna-catalog-ux .luna-hero-copy p{font-size:11px;letter-spacing:.14em;margin:0 0 14px}
.luna-catalog-ux .luna-hero-copy h1{font-size:clamp(42px,6vw,86px);font-weight:400;line-height:.96;margin:0 0 18px}
.luna-catalog-ux .luna-hero-copy span{display:block;max-width:420px;font-size:15px;line-height:1.55;margin-bottom:24px}
.luna-catalog-link{appearance:none;border:0;border-bottom:1px solid currentColor;background:transparent;color:inherit;padding:0 0 5px;font:inherit;font-size:12px;letter-spacing:.08em;cursor:pointer}
.luna-catalog-ux .luna-intro{max-width:760px;margin:96px auto;padding:0 32px;text-align:center}
.luna-catalog-ux .luna-intro p,.luna-story-heading p{font-size:11px;letter-spacing:.14em;margin:0 0 16px}
.luna-catalog-ux .luna-intro h2,.luna-story-heading h2{font-weight:400;font-size:clamp(30px,4vw,52px);line-height:1.08;margin:0 0 20px}
.luna-catalog-ux .luna-intro span,.luna-story-heading span{font-size:14px;line-height:1.65;color:#606064}
.luna-story-section{padding:0 32px;margin:0 auto 56px;max-width:1440px}
.luna-story-heading{max-width:620px;margin-bottom:28px}
.luna-story-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.luna-story-card-simple{position:relative;border:0;background:#f3f3f1;padding:0;min-width:0;text-align:left;cursor:pointer;overflow:hidden}
.luna-story-card-simple>img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;transition:transform .35s ease}
.luna-story-card-simple:hover>img{transform:scale(1.01)}
.luna-story-card-simple>span{position:absolute;left:16px;right:16px;bottom:14px;color:#fff;text-shadow:0 1px 10px rgba(0,0,0,.35);display:grid;gap:3px}
.luna-story-card-simple small{font-size:9px;letter-spacing:.12em}
.luna-story-card-simple strong{font-weight:400;font-size:17px}
.luna-story-card-simple em{font-style:normal;font-size:10px;text-decoration:underline;text-underline-offset:3px}
.luna-story-card-simple.active{outline:1px solid #1d1d1f;outline-offset:3px}
.luna-catalog-products,.luna-product-catalog{max-width:1440px;margin:0 auto 96px;padding:0 32px}
.luna-catalog-products .section-head,.luna-product-catalog .section-head{align-items:end;margin-bottom:24px}
.luna-catalog-products .section-head>span,.luna-product-catalog .section-head>span{max-width:380px;font-size:12px;line-height:1.5;color:#68686c}
.luna-editorial-divider{max-width:980px;margin:110px auto;padding:0 32px;text-align:center}
.luna-editorial-divider p{font-size:clamp(26px,3vw,42px);font-weight:400;line-height:1.18;margin:0}
.luna-product-catalog{padding-top:24px;border-top:1px solid #e3e3df}
.luna-product-catalog .product-grid,.luna-catalog-products .product-grid{grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:900px){
  .luna-catalog-ux{padding-bottom:64px}
  .luna-catalog-ux .luna-hero,.luna-catalog-ux .luna-hero>img{height:72svh;min-height:560px}
  .luna-catalog-ux .luna-hero-copy{left:20px;right:20px;bottom:28px}
  .luna-catalog-ux .luna-hero-copy h1{font-size:48px}
  .luna-catalog-ux .luna-intro{margin:64px auto;padding:0 20px}
  .luna-story-section,.luna-catalog-products,.luna-product-catalog{padding-left:16px;padding-right:16px}
  .luna-story-grid{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:8px;padding-bottom:4px;scrollbar-width:none}
  .luna-story-grid::-webkit-scrollbar{display:none}
  .luna-story-card-simple{flex:0 0 78vw;scroll-snap-align:start}
  .luna-story-card-simple>img{aspect-ratio:4/5}
  .luna-catalog-products,.luna-product-catalog{margin-bottom:72px}
  .luna-catalog-products .section-head,.luna-product-catalog .section-head{display:block}
  .luna-catalog-products .section-head>span,.luna-product-catalog .section-head>span{display:block;margin-top:8px}
  .luna-product-catalog .product-grid,.luna-catalog-products .product-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .luna-editorial-divider{margin:76px auto;padding:0 20px}
}
'''
css_path.write_text(css, encoding="utf-8")
print("Applied Luna editorial with standard catalog shopping UX")
