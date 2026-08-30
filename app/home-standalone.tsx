"use client";

import { useEffect, useMemo, useRef, useState } from "react";

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

const NEW_PRODUCTS=[
  {name:"Комплект постельного белья «Лунная сказка»",note:"Шёлк",price:15990,image:"/assets/images/KD-PD-1024-DARK01.png",category:"Постельное белье"},
  {name:"Тарелка «Лунная сказка»",note:"Фарфор",price:5990,image:"/assets/images/moon-plate.png",category:"Посуда и сервировка"},
  {name:"Натяжная простыня из сатина",note:"Шёлк",price:4990,image:"/assets/images/KD-PD-1028-WHITE01.png",category:"Постельное белье"},
  {name:"Наволочка из сатина",note:"Шёлк",price:4990,image:"/assets/images/KD-PD-1128-WHITE01.png",category:"Постельное белье"},
  {name:"Свеча Феникс",note:"Декор для дома",price:4990,image:"/assets/images/KD-PD-2519.png",category:"Декор для дома"},
  {name:"Тарелка обеденная Овация",note:"Фарфор",price:1794,image:"/assets/images/69cfd1dbd8788_big.jpg",category:"Посуда и сервировка"},
];

const CAPSULES=[
  {name:"Лунная сказка",image:"/assets/images/caps_luna_postel.png",href:"/catalog/?category=Все%20товары"},
  {name:"Ледяные узоры",image:"/assets/images/caps_led.png",href:"/catalog/?category=Все%20товары"},
  {name:"Феникс",image:"/assets/images/feniks0.jpg",href:"/catalog/?category=Декор%20для%20дома"},
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

function Icon({name}:{name:"pin"|"search"|"user"|"heart"|"bag"}){
  const p={fill:"none",stroke:"currentColor",strokeWidth:1.7,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="pin")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if(name==="search")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if(name==="user")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if(name==="heart")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
}

export default function HomeStandalone(){
  const heroRef=useRef<HTMLDivElement|null>(null);
  const [hero,setHero]=useState(0);
  const [readyId,setReadyId]=useState(READY[0].id);
  const [menu,setMenu]=useState(false);
  const [cartCount,setCartCount]=useState(0);
  const [favoriteCount,setFavoriteCount]=useState(0);
  const ready=useMemo(()=>READY.find(group=>group.id===readyId)??READY[0],[readyId]);

  useEffect(()=>{
    try{
      const cart=JSON.parse(localStorage.getItem("kultura-cart")||"[]");
      const favorites=JSON.parse(localStorage.getItem("kultura-favorites")||"[]");
      setCartCount(Array.isArray(cart)?cart.reduce((sum:number,item:{quantity?:number})=>sum+Number(item?.quantity||1),0):0);
      setFavoriteCount(Array.isArray(favorites)?favorites.length:0);
    }catch{}
  },[]);

  const navigate=(path:string)=>{window.location.href=url(path)};
  const scrollHero=(index:number)=>{
    const track=heroRef.current;if(!track)return;
    track.scrollTo({left:index*track.clientWidth,behavior:"smooth"});setHero(index);
  };

  return <main className="view-home home-fast">
    <div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <button onClick={()=>navigate("/catalog/")}>ПОДРОБНЕЕ</button></div>
    <header className="header">
      <div className="header-left"><button className="icon-btn hamburger" aria-label="Открыть меню" onClick={()=>setMenu(true)}><i/><i/><i/></button><button className="boutiques" onClick={()=>document.getElementById("home-boutiques")?.scrollIntoView({behavior:"smooth"})}><Icon name="pin"/> Бутики</button></div>
      <button className="logo" onClick={()=>window.scrollTo({top:0,behavior:"smooth"})}>КУЛЬТУРА ДОМА</button>
      <div className="header-actions">
        <button onClick={()=>navigate("/catalog/?search=open")} aria-label="Поиск"><Icon name="search"/></button>
        <button onClick={()=>navigate("/catalog/?account=open")} aria-label="Профиль"><Icon name="user"/></button>
        <button className="favorite-header" onClick={()=>navigate("/catalog/?favorites=open")} aria-label={`Избранное: ${favoriteCount}`}><Icon name="heart"/>{favoriteCount>0&&<b>{favoriteCount}</b>}</button>
        <button className="bag" onClick={()=>navigate("/catalog/?cart=open")} aria-label="Корзина"><Icon name="bag"/>{cartCount>0&&<b>{cartCount}</b>}</button>
      </div>
    </header>

    {menu&&<div className="home-fast-menu" role="dialog" aria-modal="true" aria-label="Меню"><button className="home-fast-menu-close" onClick={()=>setMenu(false)} aria-label="Закрыть">×</button><nav>{CATEGORIES.slice(0,6).map(item=><a key={item.name} href={url(`/catalog/?category=${encodeURIComponent(item.category)}`)}>{item.name}</a>)}<a href={url("/ready-solutions/")}>Готовые решения</a><a href={url("/constructor/")}>Конструктор</a></nav></div>}

    <section className="home-fast-hero" aria-label="Главные истории">
      <div className="home-fast-hero-track" ref={heroRef} onScroll={event=>{const el=event.currentTarget;const next=Math.round(el.scrollLeft/Math.max(1,el.clientWidth));if(next!==hero)setHero(next)}}>
        {HERO.map((item,index)=><article className="home-fast-hero-slide" key={item.label}>
          <picture><source media="(max-width:700px)" srcSet={url(item.mobile)}/><img src={url(item.desktop)} alt="" fetchPriority={index===0?"high":"auto"}/></picture>
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
      <div className="home-fast-product-rail">{NEW_PRODUCTS.map(product=><a className="home-fast-product" key={product.name} href={url(`/catalog/?category=${encodeURIComponent(product.category)}`)}><span className="home-fast-product-media"><img src={url(product.image)} alt={product.name} loading="lazy" decoding="async"/></span><span className="home-fast-product-copy"><strong>{product.name}</strong><small>{product.note}</small><b>{money(product.price)}</b></span></a>)}</div>
    </section>

    <section className="home-fast-section home-fast-film" aria-labelledby="home-film-title">
      <header className="home-fast-head home-fast-film-head"><div><small>О БРЕНДЕ</small><h2 id="home-film-title">Традиции в каждом доме</h2></div></header>
      <video autoPlay muted loop playsInline preload="metadata" poster={url("/assets/images/green.jpeg")}>
        <source media="(max-width:700px)" src={url("/assets/video/kultura-brand-mobile.mp4")} type="video/mp4"/>
        <source src={url("/assets/video/kultura-brand-desktop.mp4")} type="video/mp4"/>
      </video>
    </section>

    <section className="home-fast-section home-fast-capsules" aria-labelledby="home-capsules-title">
      <header className="home-fast-head"><h2 id="home-capsules-title">Капсулы</h2><a href={url("/catalog/")}>Все капсулы</a></header>
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
