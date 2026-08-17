from pathlib import Path
import re

page_path = Path("app/page.tsx")
css_path = Path("app/globals.css")

text = page_path.read_text(encoding="utf-8")

luna_component = r'''function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void }) {
  const [bundleId,setBundleId]=useState<string|null>(null);

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
    {id:"bed-1",image:editorial.images[0],fallback:sceneFallbacks[0],kicker:"СПАЛЬНЯ",title:"Лунный сатин",copy:"Комплект постельного белья, плед и подушка в глубоком синем.",productIds:[4,6,3]},
    {id:"bed-2",image:editorial.images[1],fallback:sceneFallbacks[1],kicker:"СПАЛЬНЯ",title:"Слои ткани",copy:"Спокойная композиция из сатина и кружева.",productIds:[4,3]},
    {id:"bed-3",image:editorial.images[2],fallback:sceneFallbacks[2],kicker:"ДЕТАЛИ",title:"Синий и кружево",copy:"Текстильные акценты капсулы крупным планом.",productIds:[4,6,3]},
    {id:"table-1",image:editorial.images[3],fallback:sceneFallbacks[3],kicker:"СЕРВИРОВКА",title:"Поздний чай",copy:"Чайная пара и фарфор в одной ночной палитре.",productIds:[10,5]},
    {id:"table-2",image:editorial.images[4],fallback:sceneFallbacks[4],kicker:"ФАРФОР",title:"Цвет ночного неба",copy:"Кобальтовый фарфор как продолжение интерьера.",productIds:[10,5]},
    {id:"table-3",image:editorial.images[5],fallback:sceneFallbacks[5],kicker:"СЕРВИРОВКА",title:"После заката",copy:"Финальная сцена капсулы — текстиль и сервировка в одном ритме.",productIds:[10,5,3]},
  ];
  const activeBundle=scenes.find(scene=>scene.id===bundleId);
  const bundleProducts=(activeBundle?.productIds.map(itemById).filter(Boolean)??[]) as Product[];

  const updateBundleUrl=(id:string|null,mode:"push"|"replace"="push")=>{
    const url=new URL(window.location.href);
    if(id){
      url.searchParams.set("editorial","luna");
      url.searchParams.set("bundle",id);
    }else{
      url.searchParams.delete("editorial");
      url.searchParams.delete("bundle");
    }
    window.history[mode==="push"?"pushState":"replaceState"]({lunaBundle:id},"",`${url.pathname}${url.search}${url.hash}`);
  };
  const openBundle=(id:string)=>{
    setBundleId(id);
    updateBundleUrl(id,"push");
    window.scrollTo({top:0,behavior:"auto"});
  };
  const closeBundle=()=>{
    setBundleId(null);
    updateBundleUrl(null,"replace");
    window.scrollTo({top:0,behavior:"auto"});
  };
  const openProductFromBundle=(product:Product)=>{
    updateBundleUrl(null,"replace");
    setBundleId(null);
    selectProduct(product);
  };

  useEffect(()=>{
    const readBundle=()=>{
      const params=new URLSearchParams(window.location.search);
      const candidate=params.get("editorial")==="luna"?params.get("bundle"):null;
      setBundleId(candidate&&scenes.some(scene=>scene.id===candidate)?candidate:null);
    };
    readBundle();
    window.addEventListener("popstate",readBundle);
    return()=>window.removeEventListener("popstate",readBundle);
  },[]);

  if(activeBundle){
    return <div className="luna-bundle-page">
      <div className="luna-bundle-toolbar">
        <button type="button" onClick={closeBundle} aria-label="Вернуться к Лунной сказке">← <span>Лунная сказка</span></button>
        <p>{activeBundle.kicker}</p>
      </div>
      <div className="luna-bundle-layout">
        <figure className="luna-bundle-visual">
          <RemoteImage src={activeBundle.image} fallbackSrc={activeBundle.fallback} alt={activeBundle.title}/>
          <figcaption><small>{activeBundle.kicker}</small><strong>{activeBundle.title}</strong></figcaption>
        </figure>
        <section className="luna-bundle-shop">
          <header>
            <p>ЛУННАЯ СКАЗКА</p>
            <h1>{activeBundle.title}</h1>
            <span>{activeBundle.copy}</span>
            <small>{bundleProducts.length} {bundleProducts.length===1?"товар":"товара"} в образе</small>
          </header>
          <div className="luna-bundle-grid">
            {bundleProducts.map(item=><ProductCard key={`luna-bundle-${activeBundle.id}-${item.id}`} product={item} onClick={openProductFromBundle} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)}/>) }
          </div>
        </section>
      </div>
    </div>;
  }

  const editorialFrame=(scene:(typeof scenes)[number],className:string)=><button type="button" className={`luna-zara-frame ${className}`} onClick={()=>openBundle(scene.id)} aria-label={`Открыть товары: ${scene.title}`}>
    <RemoteImage src={scene.image} fallbackSrc={scene.fallback} alt={scene.title}/>
    <span className="luna-zara-frame-caption"><small>{scene.kicker}</small><strong>{scene.title}</strong><em>Смотреть товары</em></span>
  </button>;

  return <div className="luna-editorial-page luna-zara-editorial">
    <section className="luna-zara-masthead">
      <p>КАПСУЛА · 2026</p>
      <h1>Лунная сказка</h1>
      <span>{editorial.lead}</span>
    </section>

    <section className="luna-zara-hero">
      {editorialFrame(scenes[0],"luna-zara-frame-hero")}
    </section>

    <section className="luna-zara-copy-block">
      <p>НОВАЯ КАПСУЛА</p>
      <h2>Дом в оттенках ночного неба</h2>
      <span>{editorial.detail}</span>
    </section>

    <section className="luna-zara-single">
      {editorialFrame(scenes[1],"luna-zara-frame-wide")}
    </section>

    <section className="luna-zara-copy-block luna-zara-copy-small">
      <p>ТЕКСТИЛЬ</p>
      <h2>Сатин, кружево и глубокий синий</h2>
      <span>Клик по любому editorial-кадру открывает отдельный образ с товарами из этой сцены.</span>
    </section>

    <section className="luna-zara-duo">
      {editorialFrame(scenes[2],"luna-zara-frame-portrait")}
      {editorialFrame(scenes[3],"luna-zara-frame-portrait")}
    </section>

    <section className="luna-zara-copy-block">
      <p>СЕРВИРОВКА</p>
      <h2>Фарфор как продолжение интерьера</h2>
      <span>Товары внутри образа остаются обычными карточками каталога — с привычным избранным и стандартным добавлением в корзину.</span>
    </section>

    <section className="luna-zara-single luna-zara-single-narrow">
      {editorialFrame(scenes[4],"luna-zara-frame-wide")}
    </section>

    <section className="luna-zara-finale">
      {editorialFrame(scenes[5],"luna-zara-frame-finale")}
    </section>

    <section className="luna-zara-endnote">
      <p>ЛУННАЯ СКАЗКА</p>
      <h2>Выберите кадр, чтобы собрать свой образ.</h2>
    </section>
  </div>;
}'''

if 'function LunaEditorialView' not in text:
    raise SystemExit("LunaEditorialView must be applied before Zara bundle transform")

text, count = re.subn(
    r'function LunaEditorialView[\s\S]*?(?=\n\nfunction EditorialView)',
    luna_component.rstrip(),
    text,
    count=1,
)
if count != 1:
    raise SystemExit("Failed to replace LunaEditorialView with Zara-style bundle flow")

page_path.write_text(text, encoding="utf-8")

css = css_path.read_text(encoding="utf-8")
css = re.sub(r'\n?/\* LUNA_ZARA_EDITORIAL_V3 \*/[\s\S]*\Z', '', css)
css = re.sub(r'\n?/\* LUNA_CATALOG_UX_V2 \*/[\s\S]*\Z', '', css)
css += r'''

/* LUNA_ZARA_EDITORIAL_V3 */
.luna-zara-editorial{background:#fff;color:#1d1d1f;padding-bottom:120px}
.luna-zara-masthead{max-width:760px;margin:0 auto;padding:82px 24px 70px;text-align:center}
.luna-zara-masthead p,.luna-zara-copy-block p,.luna-zara-endnote p{font-size:10px;letter-spacing:.14em;margin:0 0 18px}
.luna-zara-masthead h1{font-size:clamp(44px,6.4vw,92px);font-weight:400;line-height:.96;margin:0 0 24px}
.luna-zara-masthead span{display:block;max-width:560px;margin:0 auto;font-size:14px;line-height:1.65;color:#5d5d61}
.luna-zara-hero,.luna-zara-single,.luna-zara-finale{width:100%}
.luna-zara-single{max-width:1240px;margin:0 auto;padding:0 32px}
.luna-zara-single-narrow{max-width:1040px}
.luna-zara-frame{appearance:none;border:0;background:#f1f1ef;padding:0;display:block;position:relative;width:100%;overflow:hidden;cursor:pointer;text-align:left}
.luna-zara-frame>img{display:block;width:100%;height:auto;object-fit:cover}
.luna-zara-frame-hero>img{height:min(78vh,920px);min-height:620px}
.luna-zara-frame-wide>img{aspect-ratio:16/10}
.luna-zara-frame-portrait>img{aspect-ratio:4/5}
.luna-zara-frame-finale>img{height:min(82vh,980px);min-height:640px}
.luna-zara-frame-caption{position:absolute;left:22px;bottom:20px;display:grid;gap:4px;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.34);opacity:0;transform:translateY(6px);transition:.2s ease}
.luna-zara-frame:hover .luna-zara-frame-caption,.luna-zara-frame:focus-visible .luna-zara-frame-caption{opacity:1;transform:none}
.luna-zara-frame-caption small{font-size:9px;letter-spacing:.12em}
.luna-zara-frame-caption strong{font-size:17px;font-weight:400}
.luna-zara-frame-caption em{font-style:normal;font-size:10px;text-decoration:underline;text-underline-offset:4px}
.luna-zara-copy-block{max-width:690px;margin:0 auto;padding:104px 28px 96px;text-align:center}
.luna-zara-copy-block h2,.luna-zara-endnote h2{font-size:clamp(30px,3.5vw,52px);font-weight:400;line-height:1.08;margin:0 0 20px}
.luna-zara-copy-block span{font-size:14px;line-height:1.68;color:#5f5f62}
.luna-zara-copy-small{max-width:620px;padding-top:92px;padding-bottom:82px}
.luna-zara-duo{max-width:1340px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:0 32px}
.luna-zara-endnote{max-width:720px;margin:0 auto;padding:110px 24px 0;text-align:center}

/* Dedicated editorial bundle, analogous to a shop-the-look detail page. */
.luna-bundle-page{background:#fff;color:#1d1d1f;min-height:100vh;padding-bottom:80px}
.luna-bundle-toolbar{height:58px;padding:0 24px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e8e8e5;background:#fff;position:sticky;top:0;z-index:18}
.luna-bundle-toolbar button{border:0;background:transparent;padding:0;font:inherit;font-size:11px;letter-spacing:.04em;cursor:pointer;display:flex;gap:8px;align-items:center}
.luna-bundle-toolbar p{font-size:9px;letter-spacing:.14em;margin:0}
.luna-bundle-layout{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(420px,.72fr);gap:0;align-items:start}
.luna-bundle-visual{margin:0;background:#f1f1ef;position:sticky;top:58px;height:calc(100vh - 58px);overflow:hidden}
.luna-bundle-visual>img{width:100%;height:100%;object-fit:cover;display:block}
.luna-bundle-visual figcaption{position:absolute;left:20px;bottom:18px;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.35);display:grid;gap:3px}
.luna-bundle-visual figcaption small{font-size:9px;letter-spacing:.12em}
.luna-bundle-visual figcaption strong{font-size:18px;font-weight:400}
.luna-bundle-shop{padding:52px 28px 80px}
.luna-bundle-shop>header{max-width:460px;margin:0 0 34px}
.luna-bundle-shop>header p{font-size:9px;letter-spacing:.14em;margin:0 0 13px}
.luna-bundle-shop>header h1{font-weight:400;font-size:32px;line-height:1.08;margin:0 0 14px}
.luna-bundle-shop>header span{display:block;font-size:13px;line-height:1.55;color:#5f5f62;margin-bottom:12px}
.luna-bundle-shop>header small{font-size:10px;color:#808084}
.luna-bundle-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:36px 14px}
.luna-bundle-grid .product-card{min-width:0}
.luna-bundle-grid .product-image{background:#f4f4f2}

@media(max-width:900px){
  .luna-zara-editorial{padding-bottom:82px}
  .luna-zara-masthead{padding:54px 20px 46px}
  .luna-zara-masthead h1{font-size:52px}
  .luna-zara-frame-hero>img,.luna-zara-frame-finale>img{height:66svh;min-height:500px}
  .luna-zara-copy-block{padding:70px 24px 64px}
  .luna-zara-single{padding:0 16px}
  .luna-zara-duo{padding:0 16px;gap:8px}
  .luna-zara-frame-caption{opacity:1;transform:none;left:12px;bottom:12px}
  .luna-zara-frame-caption strong{font-size:14px}
  .luna-zara-endnote{padding-top:78px}
  .luna-bundle-toolbar{height:50px;padding:0 14px;top:0}
  .luna-bundle-layout{display:block}
  .luna-bundle-visual{position:relative;top:auto;height:auto}
  .luna-bundle-visual>img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}
  .luna-bundle-shop{padding:32px 16px 64px}
  .luna-bundle-shop>header{margin-bottom:26px}
  .luna-bundle-shop>header h1{font-size:28px}
  .luna-bundle-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:30px 8px}
}
'''
css_path.write_text(css, encoding="utf-8")
print("Applied Zara Home-inspired Luna editorial + bundle flow")
