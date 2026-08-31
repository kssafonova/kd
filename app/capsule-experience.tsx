"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";
import { SharedKulturaMenu } from "./shared-kultura-menu";

type CapsuleSku={
  id:string;article?:string;productId?:number;color?:string;colorHex?:string;sourceColor?:string;
  size?:string;price:number;image?:string;gallery?:string[];available?:boolean;
};
type CapsuleProduct={
  id:number;article?:string;name:string;note?:string;price:number;image:string;gallery?:string[];
  capsule?:string;selectedColor?:string;selectedSize?:string;selectedSkuId?:string;quantity?:number;
  skus?:CapsuleSku[];
};
type CapsuleName="Лунная сказка"|"Ледяные узоры"|"Тайна"|"Нити"|"Феникс";
type IconName="menu"|"search"|"user"|"heart"|"bag"|"close"|"arrow"|"check";

const PRODUCTS=CATALOG_PRODUCTS_GENERATED as unknown as CapsuleProduct[];
const BASE=(process.env.NEXT_PUBLIC_BASE_PATH??"").replace(/\/$/,"");
const norm=(value:unknown)=>String(value??"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
const asset=(value:string)=>value.startsWith("/assets/")?`${BASE}${value}`:value;
const money=(value:number)=>`${new Intl.NumberFormat("ru-RU").format(Math.round(value))} ₽`;
const unique=<T,>(values:T[])=>Array.from(new Set(values));

const CAPSULE_ORDER:CapsuleName[]=["Лунная сказка","Ледяные узоры","Тайна","Нити","Феникс"];
const CAPSULE_GALLERIES:Record<CapsuleName,string[]>={
  "Лунная сказка":[
    "/assets/images/caps_luna_postel.png","/assets/images/caps_luna_postel2.png","/assets/images/caps_luna_postel3.png",
    "/assets/images/caps_luna_serviz.png","/assets/images/caps_luna_serviz2.png","/assets/images/caps_luna_serviz3.png",
  ],
  "Ледяные узоры":[
    "/assets/images/caps_led.png","/assets/images/caps_led_podyshka.png","/assets/images/caps_led_podyshka2.png","/assets/images/caps_led_serviz.png",
  ],
  "Тайна":["/assets/images/tayna0.jpg","/assets/images/tayna1.jpg","/assets/images/tayna2.jpg"],
  "Нити":["/assets/images/niti0.jpg","/assets/images/niti1.jpg"],
  "Феникс":["/assets/images/feniks0.jpg","/assets/images/feniks1.jpg","/assets/images/feniks2.jpg"],
};
const CAPSULE_COPY:Record<CapsuleName,string>={
  "Лунная сказка":"Холодный свет, тонкое кружево и спокойная палитра для спальни и сервировки.",
  "Ледяные узоры":"Светлые фактуры и зимняя графика, собранные в цельный интерьерный образ.",
  "Тайна":"Глубокие оттенки и выразительные детали для камерного, почти театрального настроения.",
  "Нити":"Тактильные материалы и спокойный ритм линий — мягкая современная интерпретация традиции.",
  "Феникс":"Тёплые акценты и декоративная пластика, которые собирают пространство вокруг одного образа.",
};

function Icon({name}:{name:IconName}){
  const p={fill:"none",stroke:"currentColor",strokeWidth:1.55,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="search")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="10.5" cy="10.5" r="6.4"/><path d="m15.2 15.2 5.2 5.2"/></svg>;
  if(name==="user")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if(name==="heart")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if(name==="bag")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if(name==="close")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if(name==="arrow")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
  if(name==="check")return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="m5 12 4.2 4.2L19 6.8"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...p}><path d="M4 7h16M4 12h16M4 17h16"/></svg>;
}

function Header({onMenu}:{onMenu:()=>void}){
  return <>
    <div className="promo capsule-v160-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href="/catalog/">ПОДРОБНЕЕ</Link></div>
    <header className="header capsule-v160-header">
      <div className="header-left"><button className="capsule-v160-menu" onClick={onMenu} aria-label="Открыть меню"><Icon name="menu"/></button></div>
      <Link className="logo" href="/">КУЛЬТУРА ДОМА</Link>
      <div className="header-actions">
        <Link href="/catalog/?open=search" aria-label="Поиск"><Icon name="search"/></Link>
        <Link href="/catalog/?open=account" aria-label="Профиль"><Icon name="user"/></Link>
        <Link href="/catalog/?open=favorites" aria-label="Избранное"><Icon name="heart"/></Link>
        <Link href="/catalog/?cart=open" aria-label="Корзина"><Icon name="bag"/></Link>
      </div>
    </header>
  </>;
}

function availableSkus(product:CapsuleProduct){return (product.skus??[]).filter(sku=>sku.available!==false&&Number(sku.price)>0)}
function requiresExplicitSelection(product:CapsuleProduct){
  const skus=availableSkus(product);
  return unique(skus.map(sku=>norm(sku.size)).filter(Boolean)).length>1;
}
function defaultSkuId(product:CapsuleProduct){
  const skus=availableSkus(product);
  if(!skus.length)return "";
  return requiresExplicitSelection(product)?"":skus[0].id;
}
function skuLabel(sku:Partial<CapsuleSku>){
  const color=String(sku.sourceColor??sku.color??"").trim();
  const size=String(sku.size??"").trim();
  const cleanColor=norm(color)==="единый вариант"?"":color;
  return [cleanColor,size].filter(Boolean).join(" · ")||"Единый вариант";
}
function productBasePrice(product:CapsuleProduct){
  const values=availableSkus(product).map(sku=>Number(sku.price)).filter(value=>Number.isFinite(value)&&value>0);
  return values.length?Math.min(...values):Number(product.price)||0;
}

function CapsuleDialog({name,onClose}:{name:CapsuleName;onClose:()=>void}){
  const items=useMemo(()=>PRODUCTS.filter(product=>norm(product.capsule)===norm(name)),[name]);
  const [selection,setSelection]=useState<Record<number,string>>({});
  const [included,setIncluded]=useState<Record<number,boolean>>({});
  const dialogRef=useRef<HTMLElement|null>(null);

  useEffect(()=>{
    const initialSelection:Record<number,string>={};
    const initialIncluded:Record<number,boolean>={};
    items.forEach(product=>{
      initialSelection[product.id]=defaultSkuId(product);
      initialIncluded[product.id]=true;
    });
    setSelection(initialSelection);
    setIncluded(initialIncluded);
  },[items]);

  useEffect(()=>{
    const previousOverflow=document.body.style.overflow;
    const previousActive=document.activeElement instanceof HTMLElement?document.activeElement:null;
    document.body.style.overflow="hidden";
    const root=dialogRef.current;
    root?.querySelector<HTMLElement>("[data-capsule-close]")?.focus();

    const key=(event:KeyboardEvent)=>{
      if(event.key==="Escape"){
        event.preventDefault();
        onClose();
        return;
      }
      if(event.key!=="Tab"||!root)return;
      const focusable=Array.from(root.querySelectorAll<HTMLElement>('a[href],button:not([disabled]),select:not([disabled]),input:not([disabled]),[tabindex]:not([tabindex="-1"])')).filter(element=>element.offsetParent!==null);
      if(!focusable.length)return;
      const first=focusable[0];
      const last=focusable[focusable.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}
    };
    window.addEventListener("keydown",key);
    return()=>{
      document.body.style.overflow=previousOverflow;
      window.removeEventListener("keydown",key);
      previousActive?.focus();
    };
  },[onClose]);

  const selectedSku=(product:CapsuleProduct)=>availableSkus(product).find(sku=>sku.id===selection[product.id]);
  const chosenItems=items.filter(product=>included[product.id]!==false);
  const missing=chosenItems.filter(product=>requiresExplicitSelection(product)&&!selectedSku(product));
  const total=chosenItems.reduce((sum,product)=>sum+(selectedSku(product)?.price??productBasePrice(product)),0);
  const toggleIncluded=(productId:number)=>setIncluded(current=>({...current,[productId]:current[productId]===false}));

  const buyAll=()=>{
    if(missing.length||!chosenItems.length)return;
    const bundle=chosenItems.map(product=>{
      const sku=selectedSku(product)??availableSkus(product)[0];
      const gallery=sku?.gallery?.length?sku.gallery:product.gallery;
      return {
        ...product,
        price:sku?.price??product.price,
        image:sku?.image??product.image,
        gallery,
        selectedSize:sku?.size??product.selectedSize??"",
        selectedColor:sku?.sourceColor??sku?.color??product.selectedColor??"Единый вариант",
        selectedSkuId:sku?.id,
        quantity:1,
      };
    });
    let current:unknown[]=[];
    try{
      const raw=localStorage.getItem("kultura-cart");
      const parsed=raw?JSON.parse(raw):[];
      current=Array.isArray(parsed)?parsed:[];
    }catch{}
    localStorage.setItem("kultura-cart",JSON.stringify([...current,...bundle]));
    window.location.href=`${BASE}/catalog/?cart=open`;
  };

  const gallery=CAPSULE_GALLERIES[name];
  const ctaLabel=!chosenItems.length?"ВЫБЕРИТЕ ТОВАРЫ":missing.length?`ВЫБЕРИТЕ ВАРИАНТЫ · ${missing.length}`:`ДОБАВИТЬ КОМПЛЕКТ · ${chosenItems.length}`;

  return <div className="capsule-overlay-v160" role="presentation">
    <section ref={dialogRef} className="capsule-dialog-v160" role="dialog" aria-modal="true" aria-labelledby="capsule-v160-title" tabIndex={-1}>
      <button data-capsule-close className="capsule-close-v160" onClick={onClose} aria-label="Закрыть капсулу"><Icon name="close"/></button>

      <div className="capsule-story-v160">
        <div className="capsule-story-meta-v160"><span>КАПСУЛА · {name}</span><span>{gallery.length} ОБРАЗОВ</span></div>
        <div className="capsule-gallery-v160" aria-label={`Фотографии капсулы ${name}`}>
          {gallery.map((image,index)=><figure key={image}>
            <img src={asset(image)} alt={`${name}, образ ${index+1}`} loading={index<2?"eager":"lazy"} decoding="async"/>
            <figcaption>{String(index+1).padStart(2,"0")} / {String(gallery.length).padStart(2,"0")}</figcaption>
          </figure>)}
        </div>
      </div>

      <aside className="capsule-shop-v160">
        <header className="capsule-shop-head-v160">
          <small>СОБЕРИТЕ ОБРАЗ</small>
          <h2 id="capsule-v160-title">{name}</h2>
          <p>{CAPSULE_COPY[name]}</p>
          <div className="capsule-shop-hint-v160"><span>Все предметы выбраны по умолчанию.</span><span>Снимите ненужные и настройте варианты.</span></div>
        </header>

        <div className="capsule-products-v160" aria-label={`Товары капсулы ${name}`}>
          {items.map(product=>{
            const skus=availableSkus(product);
            const current=selectedSku(product);
            const isIncluded=included[product.id]!==false;
            const needs=isIncluded&&requiresExplicitSelection(product)&&!current;
            const image=current?.image??product.image;
            return <article key={product.id} className={`capsule-product-v160 ${isIncluded?"is-included":"is-excluded"} ${needs?"needs-selection":""}`}>
              <div className="capsule-product-media-v160">
                <Link href={`/catalog/?product=${encodeURIComponent(product.article??String(product.id))}`} aria-label={`Открыть ${product.name}`}><img src={asset(image)} alt={product.name} loading="lazy" decoding="async"/></Link>
                <button type="button" className="capsule-inclusion-v160" aria-pressed={isIncluded} aria-label={isIncluded?`Убрать ${product.name} из комплекта`:`Добавить ${product.name} в комплект`} onClick={()=>toggleIncluded(product.id)}>
                  <span>{isIncluded&&<Icon name="check"/>}</span>{isIncluded?"В КОМПЛЕКТЕ":"ДОБАВИТЬ"}
                </button>
              </div>

              <div className="capsule-product-copy-v160">
                <div className="capsule-product-name-v160">
                  <Link href={`/catalog/?product=${encodeURIComponent(product.article??String(product.id))}`}>{product.name}</Link>
                  {product.note&&<small>{product.note}</small>}
                </div>

                {skus.length>1?<label className="capsule-option-v160">
                  <span>{needs?"ВЫБЕРИТЕ ВАРИАНТ":"ВАРИАНТ"}</span>
                  <select disabled={!isIncluded} value={selection[product.id]??""} onChange={event=>setSelection(currentSelection=>({...currentSelection,[product.id]:event.target.value}))} aria-label={`Вариант товара ${product.name}`}>
                    <option value="" disabled>Выберите вариант / размер</option>
                    {skus.map(sku=><option key={sku.id} value={sku.id}>{skuLabel(sku)} · {money(sku.price)}</option>)}
                  </select>
                </label>:<div className="capsule-fixed-option-v160">{skuLabel(skus[0]??{})}</div>}

                <strong className="capsule-product-price-v160">{current?money(current.price):<>от {money(productBasePrice(product))}</>}</strong>
              </div>
            </article>;
          })}
        </div>

        <footer className="capsule-buybar-v160">
          <div className="capsule-buybar-summary-v160">
            <span>{missing.length?`Нужно выбрать варианты: ${missing.length}`:`Выбрано ${chosenItems.length} из ${items.length}`}</span>
            <strong>{money(total)}</strong>
          </div>
          <button type="button" disabled={Boolean(missing.length)||!chosenItems.length} onClick={buyAll}>{ctaLabel}<Icon name="arrow"/></button>
        </footer>
      </aside>
    </section>
  </div>;
}

export default function CapsuleExperience(){
  const [menu,setMenu]=useState(false);
  const [active,setActive]=useState<CapsuleName|null>(null);
  const capsules=useMemo(()=>CAPSULE_ORDER.map(name=>({name,items:PRODUCTS.filter(product=>norm(product.capsule)===norm(name))})).filter(item=>item.items.length),[]);
  const navigate=(path:string)=>{window.location.href=`${BASE}${path}`};

  return <main className="capsules-v160-page">
    <Header onMenu={()=>setMenu(true)}/>
    {menu&&<SharedKulturaMenu onClose={()=>setMenu(false)} onCatalog={(category="Все товары")=>navigate(`/catalog/?category=${encodeURIComponent(category)}`)} onNavigate={navigate}/>}

    <div className="capsules-v160-shell">
      <nav className="crumbs"><Link href="/">Главная</Link> / <span>Капсулы</span></nav>
      <header className="capsules-v160-intro">
        <small>КУЛЬТУРА ДОМА · EDITORIAL</small>
        <h1>Капсулы</h1>
        <div><p>Цельные истории для дома, в которых предметы уже собраны по настроению, фактуре и цвету.</p><p>Откройте образ, оставьте нужные предметы и добавьте готовый комплект в корзину.</p></div>
      </header>

      <section className="capsules-grid-v160" aria-label="Все капсулы">
        {capsules.map(({name,items},index)=><button key={name} className={`capsule-card-v160 capsule-card-${index}`} onClick={()=>setActive(name)} aria-haspopup="dialog">
          <span className="capsule-card-media-v160"><img src={asset(CAPSULE_GALLERIES[name][0])} alt="" loading={index<2?"eager":"lazy"} decoding="async"/></span>
          <span className="capsule-card-copy-v160">
            <small>КАПСУЛА · {items.length} ТОВАРОВ</small>
            <strong>{name}</strong>
            <span>{CAPSULE_COPY[name]}</span>
            <em>СМОТРЕТЬ И СОБРАТЬ <Icon name="arrow"/></em>
          </span>
        </button>)}
      </section>
    </div>

    {active&&<CapsuleDialog name={active} onClose={()=>setActive(null)}/>} 
  </main>;
}
