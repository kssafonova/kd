"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";
import { SharedKulturaMenu } from "./shared-kultura-menu";

const BASE = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const url = (path:string) => path.startsWith("/") ? `${BASE}${path}` : path;
const money = (value:number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

type ReadyCard={title:string;note:string;image:string};
type ReadyGroup={id:string;label:string;cards:ReadyCard[]};

const HERO=[
  {label:"НОВИНКИ",title:"Новое для дома",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png",href:"/catalog/"},
  {label:"СПАЛЬНЯ",title:"Тактильный покой",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png",href:"/catalog/?category=Постельное%20белье"},
  {label:"СТОЛОВАЯ",title:"Сервировка как ритуал",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png",href:"/catalog/?category=Посуда%20и%20сервировка"},
];

const CATEGORIES=[
  {name:"Спальня",image:"/assets/images/1spal.png",category:"Постельное белье"},
  {name:"Посуда и сервировка",image:"/assets/images/2stol.png",category:"Посуда и сервировка"},
  {name:"Столовый текстиль",image:"/assets/images/3stoltekstil.png",category:"Столовый текстиль"},
  {name:"Декор",image:"/assets/images/4dekor.png",category:"Декор для дома"},
  {name:"Текстиль для дома",image:"/assets/images/5homeclothes.png",category:"Пледы и подушки"},
  {name:"Ванная",image:"/assets/images/6van.png",category:"Декор для дома"},
  {name:"Outlet",image:"/assets/images/7outlet.png",category:"Все товары"},
];

type HomeCatalogProduct={
  id:number;article?:string;name:string;note?:string;price:number;oldPrice?:number;image:string;category?:string;
  switchBy?:"color"|"scent"|"none";
  colorVariants?:{name:string;hex:string;image:string;gallery?:string[]}[];
};
const HOME_CATALOG_PRODUCTS=CATALOG_PRODUCTS_GENERATED as unknown as HomeCatalogProduct[];
const NEW_ARTICLES=["KD-PD-1024","KD-PD-1023","KD-PD-1026","KD-PD-1028","KD-PD-1128","KD-PD-2519"];
const NEW_PRODUCTS=NEW_ARTICLES.map(article=>HOME_CATALOG_PRODUCTS.find(product=>product.article===article)).filter((product):product is HomeCatalogProduct=>Boolean(product));

const CAPSULES=[
  {name:"Лунная сказка",image:"/assets/images/caps_luna_postel.png",href:"/catalog/?capsule=Лунная%20сказка"},
  {name:"Ледяные узоры",image:"/assets/images/caps_led.png",href:"/catalog/?capsule=Ледяные%20узоры"},
  {name:"Феникс",image:"/assets/images/feniks0.jpg",href:"/catalog/?capsule=Феникс"},
];

const READY:ReadyGroup[]=[
  {id:"kitchen",label:"Кухня и столовая",cards:[
    {title:"Красные линии",note:"Сервировка и столовый текстиль",image:"/assets/images/3_stol_desktop.png"},
    {title:"Зелёный салон",note:"Спокойная композиция для стола",image:"/assets/images/2stol.png"},
    {title:"Зимняя сказка",note:"Светлая сервировка",image:"/assets/images/time-table.png"},
  ]},
  {id:"bed-living",label:"Спальня и гостиная",cards:[
    {title:"Зимняя сказка",note:"Постельное бельё и мягкие фактуры",image:"/assets/images/2_sleep_desktop.png"},
    {title:"Зелёный салон",note:"Текстиль и декор для гостиной",image:"/assets/images/green.jpeg"},
    {title:"Тёплый брутализм",note:"Глубокие оттенки и фактуры",image:"/assets/images/1_new_desktop.png"},
  ]},
  {id:"office",label:"Кабинет",cards:[
    {title:"Тёплый брутализм",note:"Сдержанное рабочее пространство",image:"/assets/images/4dekor.png"},
    {title:"Зелёный салон",note:"Спокойный цвет и детали",image:"/assets/images/green.jpeg"},
    {title:"Красные линии",note:"Один выразительный акцент",image:"/assets/images/niti0.jpg"},
  ]},
];

function Icon({name,filled=false}:{name:"pin"|"search"|"user"|"heart"|"bag"|"cart-add";filled?:boolean}){
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

export default function HomeStandalone(){
  const router=useRouter();
  const heroRef=useRef<HTMLDivElement|null>(null);
  const brandVideoRef=useRef<HTMLVideoElement|null>(null);
  const [hero,setHero]=useState(0);
  const [readyId,setReadyId]=useState(READY[0].id);
  const [menu,setMenu]=useState(false);
  const [cartCount,setCartCount]=useState(0);
  const [favoriteCount,setFavoriteCount]=useState(0);
  const [favoriteIds,setFavoriteIds]=useState<number[]>([]);
  const ready=useMemo(()=>READY.find(group=>group.id===readyId)??READY[0],[readyId]);

  useEffect(()=>{
    try{
      const cart=JSON.parse(localStorage.getItem("kultura-cart")||"[]");
      const favorites=JSON.parse(localStorage.getItem("kultura-favorites")||"[]");
      setCartCount(Array.isArray(cart)?cart.reduce((sum:number,item:{quantity?:number})=>sum+Number(item?.quantity||1),0):0);
      setFavoriteCount(Array.isArray(favorites)?favorites.length:0);
      setFavoriteIds(Array.isArray(favorites)?favorites.map((value:unknown)=>Number(value)).filter((value:number)=>Number.isFinite(value)):[]);
    }catch{}
  },[]);


  useEffect(()=>{
    const prefetched=new Set<string>();
    const prefetchIntent=(event:Event)=>{
      const anchor=(event.target as Element|null)?.closest<HTMLAnchorElement>("a[href]");
      if(!anchor)return;
      const raw=anchor.getAttribute("href")||"";
      const relative=BASE&&raw.startsWith(BASE)?(raw.slice(BASE.length)||"/"):raw;
      if(!relative.startsWith("/")||prefetched.has(relative))return;
      prefetched.add(relative);
      router.prefetch(relative);
    };
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
    root?.addEventListener("pointerover",prefetchIntent,{passive:true});
    root?.addEventListener("touchstart",prefetchIntent,{passive:true});
    return()=>{root?.removeEventListener("click",route);root?.removeEventListener("pointerover",prefetchIntent);root?.removeEventListener("touchstart",prefetchIntent)};
  },[router]);

  const toggleFavorite=(id:number)=>setFavoriteIds(current=>{
    const next=current.includes(id)?current.filter(value=>value!==id):[...current,id];
    try{localStorage.setItem("kultura-favorites",JSON.stringify(next))}catch{}
    setFavoriteCount(next.length);
    return next;
  });
  const navigate=(path:string)=>router.push(path);
  const scrollHero=(index:number)=>{
    const track=heroRef.current;if(!track)return;
    track.scrollTo({left:index*track.clientWidth,behavior:"smooth"});setHero(index);
  };

  return <main className="view-home home-fast">
    <div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <button onClick={()=>navigate("/catalog/")}>ПОДРОБНЕЕ</button></div>
    <header className="header">
      <div className="header-left"><button className="icon-btn hamburger" aria-label="Открыть меню" onClick={()=>setMenu(true)}><i/><i/><i/></button><button className="boutiques" onClick={()=>navigate("/catalog/?open=boutiques")}><Icon name="pin"/> Бутики</button></div>
      <button className="logo" onClick={()=>window.scrollTo({top:0,behavior:"smooth"})}>КУЛЬТУРА ДОМА</button>
      <div className="header-actions">
        <button onClick={()=>navigate("/catalog/?open=search")} aria-label="Поиск"><Icon name="search"/></button>
        <button onClick={()=>navigate("/catalog/?open=account")} aria-label="Профиль"><Icon name="user"/></button>
        <button className="favorite-header" onClick={()=>navigate("/catalog/?open=favorites")} aria-label={`Избранное: ${favoriteCount}`}><Icon name="heart"/>{favoriteCount>0&&<b>{favoriteCount}</b>}</button>
        <button className="bag" onClick={()=>navigate("/catalog/?open=cart")} aria-label="Корзина"><Icon name="bag"/>{cartCount>0&&<b>{cartCount}</b>}</button>
      </div>
    </header>
    {menu&&<SharedKulturaMenu onClose={()=>setMenu(false)} onCatalog={(category="Все товары")=>navigate(`/catalog/?category=${encodeURIComponent(category)}`)} onNavigate={navigate}/>}

    <section className="home-fast-hero" aria-label="Главные истории">
      <div className="home-fast-hero-track" ref={heroRef} onScroll={event=>{const el=event.currentTarget;const next=Math.round(el.scrollLeft/Math.max(1,el.clientWidth));if(next!==hero)setHero(next)}}>
        {HERO.map((item,index)=><article className="home-fast-hero-slide" key={item.label}>
          <picture><source media="(max-width:700px)" srcSet={url(item.mobile)}/><img src={url(item.desktop)} alt="" fetchPriority={index===0?"high":"auto"} loading={index===0?"eager":"lazy"} decoding="async"/></picture>
          <div className="home-fast-hero-shade"/>
          <div className="home-fast-hero-copy"><small>{item.label}</small><h1>{item.title}</h1><a href={url(item.href)}>Смотреть <span aria-hidden="true">→</span></a></div>
        </article>)}
      </div>
      <div className="home-fast-hero-dots" aria-label="Переключение баннеров">{HERO.map((item,index)=><button key={item.label} className={hero===index?"is-active":""} onClick={()=>scrollHero(index)} aria-label={`Баннер ${index+1}`}/>)}</div>
    </section>

    <section className="home-fast-section home-fast-categories" aria-labelledby="home-categories-title">
      <header className="home-fast-head"><h2 id="home-categories-title">Для дома</h2><a href={url("/catalog/")}>Весь каталог</a></header>
      <div className="home-fast-category-rail">{CATEGORIES.map(item=><a className="home-fast-category" key={item.name} href={url(`/catalog/?category=${encodeURIComponent(item.category)}`)}><img src={url(item.image)} alt="" loading="lazy" decoding="async"/><strong>{item.name}</strong></a>)}</div>
    </section>

    <section className="home-fast-section home-fast-new" aria-labelledby="home-new-title">
      <header className="home-fast-head"><h2 id="home-new-title">Новинки</h2><a href={url("/catalog/")}>Смотреть все</a></header>
      <div className="home-fast-product-rail">{NEW_PRODUCTS.map(product=><HomeProductCard key={product.id} product={product} liked={favoriteIds.includes(product.id)} onFavorite={toggleFavorite} navigate={navigate}/>)}</div>
    </section>

    <section className="home-fast-section home-fast-film" aria-labelledby="home-film-title">
      <header className="home-fast-head home-fast-film-head"><div><small>О БРЕНДЕ</small><h2 id="home-film-title">Традиции в каждом доме</h2></div></header>
      <video ref={brandVideoRef} muted loop playsInline preload="none" poster={url("/assets/images/green.jpeg")}>
        
        
      </video>
    </section>

    <section className="home-fast-section home-fast-capsules" aria-labelledby="home-capsules-title">
      <header className="home-fast-head"><h2 id="home-capsules-title">Капсулы</h2><a href={url("/collections/#capsules")}>Все капсулы и коллекции</a></header>
      <div className="home-fast-capsule-grid">{CAPSULES.map(item=><a key={item.name} href={url(item.href)} className="home-fast-capsule"><img src={url(item.image)} alt="" loading="lazy" decoding="async"/><strong>{item.name}</strong></a>)}</div>
    </section>

    <section className="home-fast-section home-fast-ready" aria-labelledby="home-ready-title">
      <header className="home-fast-head home-fast-ready-head"><div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2 id="home-ready-title">Выберите пространство</h2></div><a href={url("/ready-solutions/")}>Все решения</a></header>
      <div className="home-fast-tabs" role="tablist" aria-label="Пространства дома">{READY.map(group=><button key={group.id} role="tab" aria-selected={readyId===group.id} className={readyId===group.id?"is-active":""} onClick={()=>setReadyId(group.id)}>{group.label}</button>)}</div>
      <div className="home-fast-ready-grid" aria-live="polite">{ready.cards.map(card=><a className="home-fast-ready-card" key={`${ready.id}-${card.title}`} href={url(`/ready-solutions/?space=${encodeURIComponent(ready.id)}`)}><img src={url(card.image)} alt="" loading="lazy" decoding="async"/><span><strong>{card.title}</strong><small>{card.note}</small><em>Смотреть решение →</em></span></a>)}</div>
    </section>

    <section className="home-fast-constructor" aria-labelledby="home-constructor-title"><div className="home-fast-constructor-media"><img src={url("/assets/images/green.jpeg")} alt="" loading="lazy" decoding="async"/></div><div className="home-fast-constructor-copy"><small>КОНСТРУКТОР</small><h2 id="home-constructor-title">Соберите решение под свой дом</h2><p>Возьмите готовую композицию за основу, оставьте нужные предметы, замените детали и выберите количество.</p><a href={url("/constructor/")}>Собрать своё решение <span aria-hidden="true">→</span></a></div></section>

    <section id="home-boutiques" className="home-fast-boutiques" aria-labelledby="home-boutiques-title"><div className="home-fast-boutiques-media"><img src={url("/assets/images/1_new_desktop.png")} alt="Интерьер Культура дома" loading="lazy" decoding="async"/></div><div className="home-fast-boutiques-copy"><small>БУТИКИ</small><h2 id="home-boutiques-title">Увидеть дом вживую</h2><p>Познакомьтесь с материалами, сервировкой и сочетаниями предметов в пространствах Культура дома.</p><a href={url("/catalog/")}>Выбрать бутик <span aria-hidden="true">→</span></a></div></section>
  </main>;
}
