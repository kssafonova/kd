from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
HOME=ROOT/"app"/"home-standalone.tsx"
HOME_CSS=ROOT/"app"/"home-standalone.css"
HOME_PAGE=ROOT/"app"/"page.tsx"
STORE=ROOT/"app"/"storefront-app.tsx"
CATALOG_LAYOUT=ROOT/"app"/"catalog"/"layout.tsx"
MENU_CSS=ROOT/"app"/"menu-zara-premium.css"
STORY=ROOT/"app"/"story-index.tsx"
STORY_CSS=ROOT/"app"/"story-index.css"
CAPSULE_PAGE=ROOT/"app"/"capsules"/"page.tsx"
COLLECTION_PAGE=ROOT/"app"/"collections"/"page.tsx"

# ---------------------------------------------------------------------------
# HOME: same premium menu component and same PLP card language, without
# importing the heavy StorefrontApp runtime into the lightweight home route.
# ---------------------------------------------------------------------------
home=HOME.read_text(encoding="utf-8")
if 'from "./shared-kultura-menu"' not in home:
    home=home.replace('import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";','import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";\nimport { SharedKulturaMenu } from "./shared-kultura-menu";',1)

home=home.replace(
'''type HomeCatalogProduct={
  id:number;article?:string;name:string;note?:string;price:number;image:string;category?:string;
  colorVariants?:{name:string;hex:string;image:string;gallery?:string[]}[];
};''',
'''type HomeCatalogProduct={
  id:number;article?:string;name:string;note?:string;price:number;oldPrice?:number;image:string;category?:string;
  switchBy?:"color"|"scent"|"none";
  colorVariants?:{name:string;hex:string;image:string;gallery?:string[]}[];
};''',1)

icon_and_card=r'''function Icon\(\{name\}:\{name:"pin"\|"search"\|"user"\|"heart"\|"bag"\}\)\{.*?\n\}\n\nexport default function HomeStandalone\(\)\{'''
replacement=r'''function Icon({name,filled=false}:{name:"pin"|"search"|"user"|"heart"|"bag"|"cart-add";filled?:boolean}){
  const p={fill:filled?"currentColor":"none",stroke:"currentColor",strokeWidth:1.7,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="pin")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if(name==="search")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if(name==="user")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if(name==="heart")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if(name==="bag")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  return <svg className="cart-add-icon" width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M19.9023 5.46722C19.9023 5.46722 18.3349 1.23513 12.8488 1.23513C7.36279 1.23513 5.79535 5.46722 5.79535 5.46722" stroke="#1D1D1F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M23.7903 9.66602C23.9826 9.6525 24.1729 9.71072 24.3276 9.82445L24.435 9.91812L24.4378 9.92088C24.6787 10.1736 24.7432 10.5335 24.6706 10.8356V10.8384L23.4817 15.6822C22.9732 15.518 22.4395 15.4111 21.8878 15.3667L22.9844 11.3594L2.82812 11.375L3.58452 14.0455C3.59597 14.0919 3.77911 14.8323 3.95923 15.5609C4.04929 15.9252 4.13898 16.2879 4.20583 16.5583C4.23918 16.6932 4.26769 16.8063 4.28711 16.8848C4.2886 16.8909 4.28986 16.8971 4.29124 16.9027L4.7679 18.8314C4.97491 19.6766 5.3842 20.3959 5.91272 20.891C6.43983 21.3849 7.05283 21.6309 7.66094 21.628H14.3025C14.2752 21.8801 14.2598 22.136 14.2598 22.3954C14.2598 22.7674 14.2897 23.1328 14.3452 23.4892H7.6637C6.61391 23.4929 5.61299 23.0647 4.80235 22.3072C3.99487 21.5501 3.41387 20.501 3.12576 19.3246L2.6491 17.3959C2.64772 17.3903 2.64646 17.3827 2.64497 17.3766C2.62553 17.298 2.59706 17.1852 2.56369 17.0501C2.49688 16.7798 2.40708 16.4183 2.31709 16.0541C2.13694 15.3251 1.95383 14.5837 1.94237 14.5373L1.029 10.8425L1.00834 10.7268C0.973543 10.4528 1.0457 10.1447 1.26182 9.92088L1.2632 9.92226C1.35393 9.82758 1.46353 9.75727 1.58281 9.71423C1.58574 9.71301 1.5884 9.71119 1.59108 9.7101L1.59521 9.70872C1.61323 9.70256 1.63192 9.69844 1.65031 9.69357C1.67235 9.6873 1.69064 9.67981 1.70542 9.67704C1.71452 9.67536 1.72434 9.67684 1.73297 9.67566C1.75436 9.67236 1.77608 9.67168 1.79772 9.67015C1.81045 9.66954 1.8217 9.66614 1.83078 9.66602H23.7903Z" fill="#1D1D1F"/><line x1="21.5078" y1="18.076" x2="21.5078" y2="27.1563" stroke="black" strokeWidth="1.5" strokeLinecap="round"/><line x1="17.2812" y1="22.9462" x2="26.3615" y2="22.9462" stroke="black" strokeWidth="1.5" strokeLinecap="round"/></svg>;
}

function HomeProductCard({product,liked,onFavorite,navigate}:{product:HomeCatalogProduct;liked:boolean;onFavorite:(id:number)=>void;navigate:(path:string)=>void}){
  const variants=product.colorVariants?.length?product.colorVariants:[{name:"",hex:"",image:product.image}];
  const [variantIndex,setVariantIndex]=useState(0);
  const chosen=variants[Math.min(variantIndex,variants.length-1)]??variants[0];
  const article=encodeURIComponent(product.article??String(product.id));
  const productPath=`/catalog/?product=${article}`;
  const quickPath=`/catalog/?quick=${article}`;
  const discount=product.oldPrice&&product.oldPrice>product.price?Math.round((1-product.price/product.oldPrice)*100):0;
  return <article className="product-card home-fast-product">
    <button className={`heart ${liked?"liked":""}`} onClick={()=>onFavorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button>
    <button className="product-image" onClick={()=>navigate(productPath)}><img src={url(chosen?.image||product.image)} alt={product.name} loading="lazy" decoding="async"/></button>
    <div className="product-copy">
      <button className="product-link" onClick={()=>navigate(productPath)}><strong>{product.name}</strong><small>{product.switchBy==="none"||!chosen?.name?product.note:<>{chosen.name.toLowerCase()}, {product.note}</>}</small></button>
      {product.switchBy==="scent"&&variants.length>1?<div className="plp-aroma-options" role="group" aria-label={`Аромат товара ${product.name}`}>{variants.slice(0,5).map((variant,index)=><button key={variant.name} className={index===variantIndex?"active":""} onClick={()=>setVariantIndex(index)} aria-label={`Выбрать аромат ${variant.name}`}>{variant.name}</button>)}</div>:variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.slice(0,5).map((variant,index)=><button key={variant.name} className={index===variantIndex?"active":""} style={{background:variant.hex}} onClick={()=>setVariantIndex(index)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}
      <span className={`price ${discount?"sale-price":""}`}>{money(product.price)} {discount>0&&<><del>{money(product.oldPrice!)}</del><mark>−{discount}%</mark></>}</span>
    </div>
    <button className="quick" onClick={()=>navigate(quickPath)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>
  </article>;
}

export default function HomeStandalone(){'''
if "function HomeProductCard" not in home:
    home,count=re.subn(icon_and_card,replacement,home,count=1,flags=re.S)
    if count!=1: raise SystemExit("KULTURA_UNIFIED_V147: home Icon block not found")

home=home.replace('onClick={()=>navigate("/catalog/?open=menu")}', 'onClick={()=>setMenu(true)}',1)
if 'const [favoriteIds,setFavoriteIds]' not in home:
    home=home.replace('const [favoriteCount,setFavoriteCount]=useState(0);','const [favoriteCount,setFavoriteCount]=useState(0);\n  const [favoriteIds,setFavoriteIds]=useState<number[]>([]);',1)
    home=home.replace('setFavoriteCount(Array.isArray(favorites)?favorites.length:0);','setFavoriteCount(Array.isArray(favorites)?favorites.length:0);\n      setFavoriteIds(Array.isArray(favorites)?favorites.map((value:unknown)=>Number(value)).filter((value:number)=>Number.isFinite(value)):[]);',1)

if 'const toggleFavorite=' not in home:
    home=home.replace('  const navigate=(path:string)=>router.push(path);','''  const toggleFavorite=(id:number)=>setFavoriteIds(current=>{
    const next=current.includes(id)?current.filter(value=>value!==id):[...current,id];
    try{localStorage.setItem("kultura-favorites",JSON.stringify(next))}catch{}
    setFavoriteCount(next.length);
    return next;
  });
  const navigate=(path:string)=>router.push(path);''',1)

if '<SharedKulturaMenu' not in home:
    marker='''    </header>

    <section className="home-fast-hero"'''
    shared='''    </header>
    {menu&&<SharedKulturaMenu onClose={()=>setMenu(false)} onCatalog={(category="Все товары")=>navigate(`/catalog/?category=${encodeURIComponent(category)}`)} onNavigate={navigate}/>}

    <section className="home-fast-hero"'''
    if marker not in home: raise SystemExit("KULTURA_UNIFIED_V147: home header marker not found")
    home=home.replace(marker,shared,1)

rail_pattern=r'<div className="home-fast-product-rail">\{NEW_PRODUCTS\.map\(product=>\{.*?</div>\n    </section>'
rail_replacement='''<div className="home-fast-product-rail">{NEW_PRODUCTS.map(product=><HomeProductCard key={product.id} product={product} liked={favoriteIds.includes(product.id)} onFavorite={toggleFavorite} navigate={navigate}/>)}</div>
    </section>'''
home,count=re.subn(rail_pattern,rail_replacement,home,count=1,flags=re.S)
if count!=1 and "<HomeProductCard key={product.id}" not in home:
    raise SystemExit("KULTURA_UNIFIED_V147: homepage New Products rail not found")

home=home.replace('<a href={url("/capsules/")}>Все капсулы</a>','<a href={url("/collections/#capsules")}>Все капсулы и коллекции</a>')
home=home.replace('<a href={url("/catalog/")}>Все капсулы</a>','<a href={url("/collections/#capsules")}>Все капсулы и коллекции</a>')
HOME.write_text(home,encoding="utf-8")

# Home route also needs the exact same premium menu styles as catalog.
home_page=HOME_PAGE.read_text(encoding="utf-8")
if 'import "./menu-zara-premium.css";' not in home_page:
    home_page=home_page.replace('import "./home-standalone.css";','import "./menu-zara-premium.css";\nimport "./home-standalone.css";',1)
HOME_PAGE.write_text(home_page,encoding="utf-8")

# Remove the legacy home-specific typography/icons from New Products. The rail
# keeps its horizontal width, while inner card UI is now the same global PLP UI.
home_css=HOME_CSS.read_text(encoding="utf-8")
home_css=re.sub(
    r'/\* NAV_PERF_V144_SHARED_PRODUCT_CARDS \*/.*\Z',
    '''/* KULTURA_HOME_PLP_CARD_V147 — PLP card internals come from globals.css. */
.home-fast-new .home-fast-product-rail{align-items:stretch}
.home-fast-new .home-fast-product{display:block;flex:0 0 clamp(220px,23vw,330px);color:inherit}
.home-fast-new .home-fast-product .product-image{width:100%}
.home-fast-new .home-fast-product .product-copy{width:calc(100% - 42px)}
@media(max-width:700px){.home-fast-new .home-fast-product{flex-basis:64vw;max-width:280px}}
''',
    home_css,
    count=1,
    flags=re.S,
)
HOME_CSS.write_text(home_css,encoding="utf-8")

# ---------------------------------------------------------------------------
# CATALOG: reuse the same shared menu component. All existing Kultura forms,
# filters, quick-add, PDP and cart remain inside StorefrontApp unchanged.
# ---------------------------------------------------------------------------
store=STORE.read_text(encoding="utf-8")
if 'from "./shared-kultura-menu"' not in store:
    store=store.replace('import { RemoteImage } from "./remote-image";','import { RemoteImage } from "./remote-image";\nimport { SharedKulturaMenu } from "./shared-kultura-menu";',1)

menu_pattern=r'function Menu\(\{ current, setCurrent, close, go, openCatalog \}: \{ current:string; setCurrent:\(s:string\)=>void; close:\(\)=>void; go:\(v:View\)=>void; openCatalog:\(category\?:string\)=>void \}\) \{.*?\n\}\n\nfunction Search'
menu_wrapper='''function Menu({ current:_current, setCurrent:_setCurrent, close, go:_go, openCatalog }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void }) {
  return <SharedKulturaMenu onClose={close} onCatalog={(category)=>{close();openCatalog(category)}} onNavigate={(path)=>{close();window.location.href=`${runtimeStorefrontBase()}${path}`}}/>;
}

function Search'''
if "return <SharedKulturaMenu onClose={close}" not in store:
    store,count=re.subn(menu_pattern,menu_wrapper,store,count=1,flags=re.S)
    if count!=1: raise SystemExit("KULTURA_UNIFIED_V147: Storefront Menu block not found")
STORE.write_text(store,encoding="utf-8")

# Keep all Kultura CSS, but remove seven old client-side DOM enhancers that
# duplicate StorefrontApp behavior and delay hydration/click readiness.
layout=CATALOG_LAYOUT.read_text(encoding="utf-8")
enhancers=("ProductCardGalleryEnhancer|CollectionPurchaseEnhancer|ProfileAddressBookEnhancer|TruthCommerceEnhancer|CatalogLoadingStateV127|CatalogTogasV132Enhancer|CartCheckoutHumanEyeV136Enhancer")
layout=re.sub(rf'import \{{ (?:{enhancers}) \}} from "[^"]+";\n','',layout)
layout=re.sub(rf'\s*<(?:{enhancers})\s*/>','',layout)
CATALOG_LAYOUT.write_text(layout,encoding="utf-8")

# Lower editorial destinations after the core categories, with a quiet warm
# text accent and a hairline rather than a visual card.
menu_css=MENU_CSS.read_text(encoding="utf-8")
menu_override='''

/* KULTURA_MENU_UNIFIED_V147 */
.premium-menu .premium-menu-editorial-lower{
  margin:22px 0 0;
  padding:20px 0 0;
  border-top:1px solid #dededb;
}
.premium-menu .premium-menu-editorial-lower>small{margin-bottom:10px;color:#9a8a7c}
.premium-menu .premium-menu-editorial-lower>button,
.premium-menu .premium-menu-editorial-lower>a{
  min-height:41px;
  padding:6px 0!important;
  color:#6f6257!important;
  font-size:14px;
  letter-spacing:.055em;
}
.premium-menu .premium-menu-editorial-lower>button+button,
.premium-menu .premium-menu-editorial-lower>a+a{margin-top:0}
@media(max-width:700px){
  .premium-menu .premium-menu-editorial-lower{margin-top:20px;padding-top:18px}
  .premium-menu .premium-menu-editorial-lower>button,
  .premium-menu .premium-menu-editorial-lower>a{font-size:13px;min-height:40px}
}
'''
if "KULTURA_MENU_UNIFIED_V147" not in menu_css:
    menu_css+=menu_override
MENU_CSS.write_text(menu_css,encoding="utf-8")

# ---------------------------------------------------------------------------
# CAPSULES + COLLECTIONS: one lightweight server-rendered landing page.
# Both old URLs remain valid and render the same combined page.
# ---------------------------------------------------------------------------
story='''import Link from "next/link";
import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";
import "./story-index.css";

type Product={id:number;article?:string;name:string;image:string;category?:string;collection?:string;capsule?:string};
const PRODUCTS=CATALOG_PRODUCTS_GENERATED as unknown as Product[];
const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";
const asset=(value:string)=>value.startsWith("/assets/")?`${BASE}${value}`:value;
const norm=(value:unknown)=>String(value??"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
const unique=(values:(string|undefined)[])=>Array.from(new Map(values.filter(Boolean).map(value=>[norm(value),String(value)])).values());
const CAPSULE_IMAGES:Record<string,string>={
  "Лунная сказка":"/assets/images/caps_luna_postel.png",
  "Ледяные узоры":"/assets/images/caps_led.png",
  "Феникс":"/assets/images/feniks0.jpg",
  "Нити":"/assets/images/niti0.jpg",
  "Тайна":"/assets/images/tayna0.jpg",
};

function SearchIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>}
function UserIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round"><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>}
function HeartIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7"><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8-1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>}
function BagIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7"><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>}

function StaticHeader(){return <><div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href="/catalog/">ПОДРОБНЕЕ</Link></div><header className="header story-header"><div className="header-left"><Link className="story-menu-button" href="/catalog/?open=menu" aria-label="Открыть меню"><i/><i/><i/></Link></div><Link className="logo" href="/">КУЛЬТУРА ДОМА</Link><div className="header-actions"><Link href="/catalog/?open=search" aria-label="Поиск"><SearchIcon/></Link><Link href="/catalog/?open=account" aria-label="Профиль"><UserIcon/></Link><Link href="/catalog/?open=favorites" aria-label="Избранное"><HeartIcon/></Link><Link href="/catalog/?open=cart" aria-label="Корзина"><BagIcon/></Link></div></header></>}

function StoryCards({kind}:{kind:"capsule"|"collection"}){
  const names=unique(PRODUCTS.map(product=>product[kind]));
  return <div className="collection-grid story-index-grid">{names.map(name=>{const items=PRODUCTS.filter(product=>norm(product[kind])===norm(name));const image=kind==="capsule"?(CAPSULE_IMAGES[name]||items[0]?.image):items[0]?.image;const href=kind==="capsule"?`/catalog/?capsule=${encodeURIComponent(name)}`:`/catalog/?collection=${encodeURIComponent(name)}`;return <article key={`${kind}-${name}`}><Link href={href}><img src={asset(image||"/assets/images/image-placeholder.svg")} alt={name} loading="lazy" decoding="async"/><div><small>{kind==="capsule"?"КАПСУЛА":"КОЛЛЕКЦИЯ"}</small><h2>{name}</h2><p>{items.length} товаров</p><span>СМОТРЕТЬ <b aria-hidden="true">→</b></span></div></Link></article>})}</div>;
}

export default function StoryIndex(){
  return <main className="story-index-page"><StaticHeader/><div className="collections page story-index-shell"><nav className="crumbs"><Link href="/">Главная</Link> / <span>Капсулы и коллекции</span></nav><header className="section-head"><p>КУЛЬТУРА ДОМА · EDITORIAL</p><h1>Капсулы и коллекции</h1><span>Авторские серии и готовые истории для дома — от цельного настроения капсулы до коллекций предметов, связанных общей идеей и материалами.</span></header><nav className="story-index-switch" aria-label="Разделы страницы"><a href="#capsules">Капсулы</a><a href="#collections">Коллекции</a></nav><section id="capsules" className="story-index-group"><header className="story-index-group-head"><small>ГОТОВЫЕ ИСТОРИИ</small><h2>Капсулы</h2><p>Предметы, собранные в цельный образ по цвету, орнаменту и настроению.</p></header><StoryCards kind="capsule"/></section><section id="collections" className="story-index-group"><header className="story-index-group-head"><small>АВТОРСКИЕ СЕРИИ</small><h2>Коллекции</h2><p>Серии предметов, объединённые общей идеей, материалами и визуальным языком.</p></header><StoryCards kind="collection"/></section></div></main>;
}
'''
# Fix a typo-proof heart path by reusing the established site path if this file
# is ever regenerated; visual weight remains identical to the existing header.
story=story.replace('M20.8 5.8c-2.2-2.4-6.1-1.8-8.8-1.4-2.7-3.2-6.6-3.8-8.8-1.4','M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4')
STORY.write_text(story,encoding="utf-8")
CAPSULE_PAGE.write_text('import StoryIndex from "../story-index";\nexport default function CapsulesPage(){return <StoryIndex/>}\n',encoding="utf-8")
COLLECTION_PAGE.write_text('import StoryIndex from "../story-index";\nexport default function CollectionsPage(){return <StoryIndex/>}\n',encoding="utf-8")

story_css=STORY_CSS.read_text(encoding="utf-8")
story_override='''

/* KULTURA_STORIES_UNIFIED_V147 */
.story-index-page{scroll-behavior:smooth}
.story-index-switch{position:sticky;top:78px;z-index:8;background:rgba(255,255,255,.96);backdrop-filter:blur(12px)}
.story-index-switch a{color:inherit;text-decoration:none}
.story-index-group{scroll-margin-top:150px;padding:30px 0 76px}
.story-index-group+.story-index-group{border-top:1px solid var(--line);padding-top:72px}
.story-index-group-head{max-width:620px;margin:0 0 28px;text-align:left}
.story-index-group-head small{color:#98765f;font-size:8px;letter-spacing:.16em}
.story-index-group-head h2{margin:8px 0 10px;font:400 clamp(32px,3.2vw,48px)/1.05 var(--serif)}
.story-index-group-head p{max-width:520px;margin:0;color:#777;line-height:1.55}
@media(max-width:700px){
  .story-index-switch{top:56px;margin-left:-12px;margin-right:-12px;padding-left:12px;padding-right:12px}
  .story-index-group{scroll-margin-top:120px;padding:24px 0 54px}
  .story-index-group+.story-index-group{padding-top:52px}
  .story-index-group-head{margin-bottom:20px}
  .story-index-group-head h2{font-size:29px}
  .story-index-group-head p{font-size:11px}
}
'''
if "KULTURA_STORIES_UNIFIED_V147" not in story_css:
    story_css+=story_override
STORY_CSS.write_text(story_css,encoding="utf-8")

print("KULTURA_UNIFIED_V147: shared home/catalog menu, lower premium story links, combined capsules+collections landing, PLP-identical home New Products cards, lean catalog hydration applied")
