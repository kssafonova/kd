from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
HOME=ROOT/"app"/"home-standalone.tsx"
STORE=ROOT/"app"/"storefront-app.tsx"
LAYOUT=ROOT/"app"/"catalog"/"layout.tsx"
HOME_CSS=ROOT/"app"/"home-standalone.css"

# Homepage: keep the current Kultura doma design, but use the same generated
# product source as catalog and switch all internal navigation to Next router.
home=HOME.read_text(encoding="utf-8")
if 'from "next/navigation"' not in home:
    home=home.replace(
        'import { useEffect, useMemo, useRef, useState } from "react";\n',
        'import { useEffect, useMemo, useRef, useState } from "react";\nimport { useRouter } from "next/navigation";\nimport { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";\n',1)

new_products='''type HomeCatalogProduct={
  id:number;article?:string;name:string;note?:string;price:number;image:string;category?:string;
  colorVariants?:{name:string;hex:string;image:string;gallery?:string[]}[];
};
const HOME_CATALOG_PRODUCTS=CATALOG_PRODUCTS_GENERATED as unknown as HomeCatalogProduct[];
const NEW_ARTICLES=["KD-PD-1024","KD-PD-1023","KD-PD-1026","KD-PD-1028","KD-PD-1128","KD-PD-2519"];
const NEW_PRODUCTS=NEW_ARTICLES.map(article=>HOME_CATALOG_PRODUCTS.find(product=>product.article===article)).filter((product):product is HomeCatalogProduct=>Boolean(product));

const CAPSULES=[
  {name:"Лунная сказка",image:"/assets/images/caps_luna_postel.png",href:"/catalog/?capsule=Лунная%20сказка"},
  {name:"Ледяные узоры",image:"/assets/images/caps_led.png",href:"/catalog/?capsule=Ледяные%20узоры"},
  {name:"Феникс",image:"/assets/images/feniks0.jpg",href:"/catalog/?capsule=Феникс"},
];'''
home,count=re.subn(r'const NEW_PRODUCTS=\[.*?\n\];\n\nconst CAPSULES=\[.*?\n\];',new_products,home,count=1,flags=re.S)
if count!=1:
    raise SystemExit("NAV_PERF_V144: homepage product/capsule block not found")

home=home.replace('export default function HomeStandalone(){\n  const heroRef=useRef<HTMLDivElement|null>(null);', 'export default function HomeStandalone(){\n  const router=useRouter();\n  const heroRef=useRef<HTMLDivElement|null>(null);\n  const brandVideoRef=useRef<HTMLVideoElement|null>(null);',1)

marker='''  useEffect(()=>{
    try{
      const cart=JSON.parse(localStorage.getItem("kultura-cart")||"[]");
      const favorites=JSON.parse(localStorage.getItem("kultura-favorites")||"[]");
      setCartCount(Array.isArray(cart)?cart.reduce((sum:number,item:{quantity?:number})=>sum+Number(item?.quantity||1),0):0);
      setFavoriteCount(Array.isArray(favorites)?favorites.length:0);
    }catch{}
  },[]);
'''
extra='''

  useEffect(()=>{
    router.prefetch("/catalog/");
    router.prefetch("/capsules/");
    router.prefetch("/collections/");
    router.prefetch("/ready-solutions/");
    const root=document.querySelector<HTMLElement>(".home-fast");
    const route=(event:MouseEvent)=>{
      if(event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
      const anchor=(event.target as Element|null)?.closest<HTMLAnchorElement>("a[href]");
      if(!anchor||anchor.target==="_blank"||anchor.hasAttribute("download"))return;
      const raw=anchor.getAttribute("href")||"";
      if(!raw||raw.startsWith("#")||raw.startsWith("mailto:")||raw.startsWith("tel:")||raw.startsWith("http"))return;
      const relative=BASE&&raw.startsWith(BASE)?(raw.slice(BASE.length)||"/"):raw;
      if(!relative.startsWith("/"))return;
      event.preventDefault();
      setMenu(false);
      router.push(relative);
    };
    root?.addEventListener("click",route);
    return()=>root?.removeEventListener("click",route);
  },[router]);

  useEffect(()=>{
    const video=brandVideoRef.current;if(!video)return;
    const observer=new IntersectionObserver(entries=>{
      const near=entries.some(entry=>entry.isIntersecting);
      if(near)void video.play().catch(()=>{});else video.pause();
    },{rootMargin:"300px 0px"});
    observer.observe(video);
    return()=>observer.disconnect();
  },[]);
'''
if extra.strip() not in home:
    if marker not in home: raise SystemExit("NAV_PERF_V144: homepage storage effect not found")
    home=home.replace(marker,marker+extra,1)

home=home.replace('const navigate=(path:string)=>{window.location.href=url(path)};','const navigate=(path:string)=>router.push(path);',1)
home=home.replace('<a href={url("/ready-solutions/")}>Готовые решения</a><a href={url("/constructor/")}>Конструктор</a>', '<a href={url("/capsules/")}>Капсулы</a><a href={url("/collections/")}>Коллекции</a><a href={url("/ready-solutions/")}>Готовые решения</a><a href={url("/constructor/")}>Конструктор</a>',1)
home=home.replace('fetchPriority={index===0?"high":"auto"}/>', 'fetchPriority={index===0?"high":"auto"} loading={index===0?"eager":"lazy"} decoding="async"/>',1)

old_rail='''<div className="home-fast-product-rail">{NEW_PRODUCTS.map(product=><a className="home-fast-product" key={product.name} href={url(`/catalog/?category=${encodeURIComponent(product.category)}`)}><span className="home-fast-product-media"><img src={url(product.image)} alt={product.name} loading="lazy" decoding="async"/></span><span className="home-fast-product-copy"><strong>{product.name}</strong><small>{product.note}</small><b>{money(product.price)}</b></span></a>)}</div>'''
new_rail='''<div className="home-fast-product-rail">{NEW_PRODUCTS.map(product=>{const productHref=url(`/catalog/?product=${encodeURIComponent(product.article??String(product.id))}`);return <article className="product-card home-fast-product" key={product.id}><a className="product-image home-fast-product-media" href={productHref}><img src={url(product.image)} alt={product.name} loading="lazy" decoding="async"/></a><div className="product-copy home-fast-product-copy"><a className="product-link" href={productHref}><strong>{product.name}</strong><small>{product.note}</small></a>{product.colorVariants&&product.colorVariants.length>1&&<div className="plp-swatches home-fast-swatches" aria-label={`Варианты ${product.name}`}>{product.colorVariants.slice(0,5).map((variant,index)=><i key={variant.name} className={index===0?"active":""} style={{background:variant.hex}} title={variant.name}/>)}</div>}<span className="price">{money(product.price)}</span></div><a className="quick home-fast-quick" href={productHref} aria-label={`Выбрать ${product.name}`}><Icon name="bag"/></a></article>})}</div>'''
if old_rail not in home: raise SystemExit("NAV_PERF_V144: homepage new product rail not found")
home=home.replace(old_rail,new_rail,1)
home=home.replace('<header className="home-fast-head"><h2 id="home-capsules-title">Капсулы</h2><a href={url("/catalog/")}>Все капсулы</a></header>', '<header className="home-fast-head"><h2 id="home-capsules-title">Капсулы</h2><a href={url("/capsules/")}>Все капсулы</a></header>',1)
home=home.replace('<video autoPlay muted loop playsInline preload="metadata" poster={url("/assets/images/green.jpeg")}>', '<video ref={brandVideoRef} muted loop playsInline preload="none" poster={url("/assets/images/green.jpeg")}>',1)
HOME.write_text(home,encoding="utf-8")

# Make the shared catalog app understand a product deep-link so the exact same
# PDP / size selector / cart flow opens from homepage product cards.
store=STORE.read_text(encoding="utf-8")
store=store.replace('const requestedCollection=params.get("collection");','const requestedCollection=params.get("collection");\n    const requestedProduct=params.get("product");',1)
product_bridge='''    if(requestedProduct){
      const key=String(requestedProduct).trim().toLocaleLowerCase("ru-RU");
      const matched=products.find(item=>String(item.id)===requestedProduct||String(item.article||"").trim().toLocaleLowerCase("ru-RU")===key);
      if(matched){setSelected(matched);setView("product")}
    }
'''
needle='''    if(open==="cart")setCartOpen(true);'''
if product_bridge.strip() not in store:
    if needle not in store: raise SystemExit("NAV_PERF_V144: storefront open bridge not found")
    store=store.replace(needle,product_bridge+needle,1)
store=store.replace('if(section||open||requestedCollection)window.history.replaceState({},"",window.location.pathname);','if(section||open||requestedCollection||requestedProduct)window.history.replaceState({},"",window.location.pathname);',1)
store=store.replace('<button className="logo" onClick={() => go("home")}>КУЛЬТУРА ДОМА</button>','<button className="logo" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/`}}>КУЛЬТУРА ДОМА</button>',1)
store=store.replace('<button type="button" onClick={()=>go("collections")}><span>КАПСУЛЫ</span><Icon name="arrow"/></button>','<a href={`${runtimeStorefrontBase()}/capsules/`} onClick={close}><span>КАПСУЛЫ</span><Icon name="arrow"/></a>\n      <a href={`${runtimeStorefrontBase()}/collections/`} onClick={close}><span>КОЛЛЕКЦИИ</span><Icon name="arrow"/></a>',1)
store=store.replace('<button onClick={()=>go("collections")}>Коллекции</button>','<button onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/collections/`}}>Коллекции</button>',1)
STORE.write_text(store,encoding="utf-8")

# The legacy route split added seven client-side DOM enhancer components on top
# of StorefrontApp. Their core behaviors now exist inside StorefrontApp itself;
# keeping them in the critical path delays hydration and causes double work.
layout=LAYOUT.read_text(encoding="utf-8")
layout=re.sub(r'import \{ (?:ProductCardGalleryEnhancer|CollectionPurchaseEnhancer|ProfileAddressBookEnhancer|TruthCommerceEnhancer|CatalogLoadingStateV127|CatalogTogasV132Enhancer|CartCheckoutHumanEyeV136Enhancer) \} from "[^"]+";\n','',layout)
layout=re.sub(r'\s*<(?:ProductCardGalleryEnhancer|CollectionPurchaseEnhancer|ProfileAddressBookEnhancer|TruthCommerceEnhancer|CatalogLoadingStateV127|CatalogTogasV132Enhancer|CartCheckoutHumanEyeV136Enhancer)\s*/>','',layout)
LAYOUT.write_text(layout,encoding="utf-8")

# Small home-only compatibility layer: same PLP card proportions and swatches,
# while keeping the existing homepage layout and typography.
css=HOME_CSS.read_text(encoding="utf-8")
marker_css='/* NAV_PERF_V144_SHARED_PRODUCT_CARDS */'
if marker_css not in css:
    css+='''\n\n/* NAV_PERF_V144_SHARED_PRODUCT_CARDS */
.home-fast-new .home-fast-product-rail{align-items:stretch}
.home-fast-new .home-fast-product{display:block;flex:0 0 clamp(220px,23vw,330px);color:inherit;text-decoration:none}
.home-fast-new .home-fast-product-media{display:block;width:100%;background:#f3f1ed}
.home-fast-new .home-fast-product-media img{width:100%;aspect-ratio:1/1.08;object-fit:cover}
.home-fast-new .home-fast-product-copy{width:calc(100% - 40px);padding:12px 0;display:flex;flex-direction:column;align-items:flex-start}
.home-fast-new .home-fast-product-copy .product-link{color:inherit;text-decoration:none;display:flex;flex-direction:column;text-align:left}
.home-fast-new .home-fast-product-copy strong{font:400 16px/1.25 var(--serif)}
.home-fast-new .home-fast-product-copy small{font-size:11px;color:#888;margin-top:4px}
.home-fast-new .home-fast-product-copy .price{font-size:14px;margin-top:8px}
.home-fast-new .home-fast-quick{right:1px;bottom:10px;display:grid;place-items:center;color:inherit}
.home-fast-new .home-fast-quick svg{width:27px;height:27px}
.home-fast-new .home-fast-swatches{display:flex;gap:7px;margin-top:9px;min-height:20px}
.home-fast-new .home-fast-swatches i{display:block;width:17px;height:17px;border-radius:50%;border:1px solid #d7d7d3;box-shadow:inset 0 0 0 2px #fff}
.home-fast-new .home-fast-swatches i.active{outline:1px solid #222;outline-offset:1px}
@media(max-width:700px){.home-fast-new .home-fast-product{flex-basis:64vw}.home-fast-new .home-fast-product-copy strong{font-size:13px}.home-fast-new .home-fast-product-copy .price{font-size:12px}}
'''
HOME_CSS.write_text(css,encoding="utf-8")

print("NAV_PERF_V144: client navigation + route prefetch + generated homepage products + product deep links + lazy brand film + lean catalog layout applied")
