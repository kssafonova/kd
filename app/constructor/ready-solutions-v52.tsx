"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS, findTableSolution, type TableSolution } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedOptionQuantity,
  type SolutionCategory,
  type SolutionProductOption,
} from "./table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "./types";

const CART_KEY = "kultura-cart";
const CART_OFFSET = 980000;
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const money = (value:number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const priceOf = (row?:CatalogRow) => Number(String(row?.price||"").replace(/[^\d.,-]/g,"").replace(",","."))||0;
const norm = (value:string) => String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/[«»"']/g,"").replace(/\s+/g," ");
const rowImages = (row?:CatalogRow) => Array.from(new Set([row?.primary_image_url,...(row?.all_image_urls||"").split("|")].filter((value):value is string=>Boolean(value))));
const rowId = (row:CatalogRow) => {
  const numeric=Number(String(row.offer_id||row.group_id||"").replace(/\D/g,""));
  if(Number.isFinite(numeric)&&numeric>0)return CART_OFFSET+numeric;
  return CART_OFFSET+Array.from(row.product_name).reduce((sum,char)=>sum+char.charCodeAt(0),0);
};

function SiteIcon({name}:{name:"search"|"user"|"heart"|"bag"|"pin"}){
  const common={fill:"none",stroke:"currentColor",strokeWidth:1.6,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="search")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if(name==="user")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if(name==="heart")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if(name==="pin")return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
}

function IntegratedHeaderV52(){
  return <>
    <div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href={`${basePath}/`}>ПОДРОБНЕЕ</Link></div>
    <header className="header v52-integrated-header">
      <div className="header-left"><Link className="icon-btn hamburger" href={`${basePath}/`} aria-label="Каталог"><i/><i/><i/></Link><Link className="boutiques" href={`${basePath}/?open=boutiques`}><SiteIcon name="pin"/> Бутики</Link></div>
      <Link className="logo" href={`${basePath}/`}>КУЛЬТУРА ДОМА</Link>
      <div className="header-actions"><Link href={`${basePath}/?open=search`} aria-label="Поиск"><SiteIcon name="search"/></Link><Link href={`${basePath}/?open=account`} aria-label="Профиль"><SiteIcon name="user"/></Link><Link href={`${basePath}/?open=favorites`} aria-label="Избранное"><SiteIcon name="heart"/></Link><Link className="bag" href={`${basePath}/?open=cart`} aria-label="Корзина"><SiteIcon name="bag"/></Link></div>
    </header>
  </>;
}

function useConstructorData(){
  const [catalog,setCatalog]=useState<FinalConstructorData|null>(null);
  const [rules,setRules]=useState<ConstructorData|null>(null);
  const [error,setError]=useState("");
  useEffect(()=>{let alive=true;Promise.all([loadFinalConstructorData(),loadConstructorData().catch(()=>null)]).then(([nextCatalog,nextRules])=>{if(alive){setCatalog(nextCatalog);setRules(nextRules)}}).catch((reason:unknown)=>{if(alive)setError(reason instanceof Error?reason.message:"Не удалось загрузить данные")});return()=>{alive=false}},[]);
  return {catalog,rules,error};
}

function solutionImage(solution:TableSolution,rows:CatalogRow[]){return solution.heroImage||(solution.previewFile?`/images/constructor/${solution.previewFile}`:rows[0]?.primary_image_url)||"/images/image-placeholder.svg"}
function orderedCategories(categories:SolutionCategory[],solution:TableSolution){
  const order=solution.productOrder?.map(norm)??[];
  if(!order.length)return categories;
  return categories.map(category=>({...category,slots:category.slots.map(slot=>({...slot,options:[...slot.options].sort((a,b)=>{const ai=order.indexOf(norm(a.title));const bi=order.indexOf(norm(b.title));return(ai<0?9999:ai)-(bi<0?9999:bi)})}))}));
}

function cartItemFromRow(row:CatalogRow,quantity=1){
  const images=rowImages(row);
  const price=priceOf(row);
  const color=row.color||"Без цвета";
  const size=row.size||row.volume||"Единый размер";
  const id=rowId(row);
  return {id,name:row.product_name,note:[row.collection,row.material].filter(Boolean).join(" · "),price,image:images[0]||"/images/image-placeholder.svg",gallery:images.slice(1),selectedColor:color,selectedSize:size,selectedSkuId:`constructor-${row.offer_id||id}`,quantity,skus:[{id:`constructor-${row.offer_id||id}`,article:row.vendor_code||String(row.offer_id),productId:id,color,colorHex:"#d8d5cf",size,material:row.material||"",composition:row.material||"",price,image:images[0]||"/images/image-placeholder.svg",gallery:images.slice(1)}]};
}
function addRowsToSharedCart(rows:Array<{row:CatalogRow;quantity:number}>){
  let current:any[]=[];try{current=JSON.parse(localStorage.getItem(CART_KEY)||"[]")}catch{}
  const next=[...current];
  rows.forEach(({row,quantity})=>{const item=cartItemFromRow(row,quantity);const index=next.findIndex(existing=>existing.id===item.id&&existing.selectedColor===item.selectedColor&&existing.selectedSize===item.selectedSize);if(index>=0)next[index]={...next[index],quantity:(next[index].quantity||1)+quantity};else next.push(item)});
  try{localStorage.setItem(CART_KEY,JSON.stringify(next))}catch{}
}

function SolutionQuickAddV52({option,close}:{option:SolutionProductOption;close:()=>void}){
  const colors=optionColors(option);
  const [color,setColor]=useState(colors[0]||"");
  const sizes=optionSizes(option,color);
  const [size,setSize]=useState(sizes[0]||"");
  const [quantity,setQuantity]=useState(1);
  useEffect(()=>{const next=optionSizes(option,color);setSize(next[0]||"")},[color,option]);
  const row=pickOptionVariant(option,color,size);
  const images=rowImages(row);
  const add=()=>{if(!row)return;addRowsToSharedCart([{row,quantity}]);close();window.setTimeout(()=>window.location.assign(`${basePath}/?open=cart`),80)};
  return <div className="v52-quick-backdrop"><button type="button" className="v52-quick-dismiss" onClick={close} aria-label="Закрыть"/><section className="v52-quick-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${option.title}`}><button className="v52-quick-close" type="button" onClick={close}>×</button><div className="v52-quick-media"><RemoteImage src={images[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></div><div className="v52-quick-copy"><small>{option.collection||"КУЛЬТУРА ДОМА"}</small><h2>{option.title}</h2><strong>{money(priceOf(row))}</strong>{colors.length>1&&<div className="v52-option-row"><span>Цвет</span><div>{colors.map(item=><button type="button" key={item} className={color===item?"active":""} onClick={()=>setColor(item)}>{item}</button>)}</div></div>}{sizes.length>1&&<label className="v52-option-select"><span>Размер</span><select value={size} onChange={event=>setSize(event.target.value)}>{sizes.map(item=><option value={item} key={item}>{item}</option>)}</select></label>}<div className="v52-quantity"><button type="button" onClick={()=>setQuantity(value=>Math.max(1,value-1))}>−</button><span>{quantity}</span><button type="button" onClick={()=>setQuantity(value=>value+1)}>+</button></div><button className="v52-primary" type="button" onClick={add}>ДОБАВИТЬ В КОРЗИНУ · {money(priceOf(row)*quantity)}</button></div></section></div>;
}

function SolutionProductCardV52({option,configure,selected,color,size,quantity,onToggle,onColor,onSize,onQuantity,onQuick}:{option:SolutionProductOption;configure:boolean;selected:boolean;color:string;size:string;quantity:number;onToggle:()=>void;onColor:(value:string)=>void;onSize:(value:string)=>void;onQuantity:(value:number)=>void;onQuick:()=>void}){
  const colors=optionColors(option);
  const sizes=optionSizes(option,color);
  const row=pickOptionVariant(option,color,size);
  const image=rowImages(row)[0]||"/images/image-placeholder.svg";
  return <article className={`product-card v52-solution-product ${selected?"selected":""}`}>
    <button className="product-image" type="button" onClick={configure?onToggle:onQuick}><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={option.title}/></button>
    <div className="product-copy"><button className="product-link" type="button" onClick={configure?onToggle:onQuick}><strong>{option.title}</strong><small>{option.collection||row?.material||"Культура Дома"}</small></button><span className="price">{money(priceOf(row))}</span></div>
    {configure?<button className={`quick selection-check ${selected?"selected":""}`} type="button" onClick={onToggle} aria-pressed={selected}>{selected?"✓":""}</button>:<button className="quick" type="button" onClick={onQuick} aria-label={`Добавить ${option.title}`}><svg viewBox="0 0 28 28" aria-hidden="true"><path d="M4 9h19l-1.4 14H5.4L4 9Z" fill="none" stroke="currentColor" strokeWidth="1.3"/><path d="M9 9V6a5 5 0 0 1 10 0v3M19 18h7M22.5 14.5v7" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round"/></svg></button>}
    {configure&&selected&&<div className="v52-solution-controls">{colors.length>1&&<div className="v52-solution-swatches">{colors.map(item=><button type="button" key={item} className={color===item?"active":""} onClick={()=>onColor(item)} title={item}><span>{item.slice(0,1)}</span></button>)}</div>}{sizes.length>1&&<label><span>Размер</span><select value={size} onChange={event=>onSize(event.target.value)}><option value="">Выбрать</option>{sizes.map(item=><option value={item} key={item}>{item}</option>)}</select></label>}<div className="v52-solution-qty"><button type="button" onClick={()=>onQuantity(Math.max(1,quantity-1))}>−</button><span>{quantity}</span><button type="button" onClick={()=>onQuantity(quantity+1)}>+</button></div></div>}
  </article>;
}

function ReadySolutionOverlayV52({solution,catalog,rules,close}:{solution:TableSolution;catalog:FinalConstructorData;rules:ConstructorData|null;close:()=>void}){
  const rows=useMemo(()=>resolveTableSolutionCatalogRows(catalog.catalog,solution),[catalog,solution]);
  const categories=useMemo(()=>orderedCategories(buildSolutionCategories(rows,solution.space),solution),[rows,solution]);
  const options=useMemo(()=>categories.flatMap(category=>category.slots.flatMap(slot=>slot.options)),[categories]);
  const guestOptions=useMemo(()=>deriveGuestOptions(solution,rules),[solution,rules]);
  const [guests,setGuests]=useState(guestOptions[0]||2);
  const [configure,setConfigure]=useState(false);
  const [selected,setSelected]=useState<Record<string,boolean>>({});
  const [colors,setColors]=useState<Record<string,string>>({});
  const [sizes,setSizes]=useState<Record<string,string>>({});
  const [qty,setQty]=useState<Record<string,number>>({});
  const [quick,setQuick]=useState<SolutionProductOption|null>(null);
  const isDining=solution.space.toLocaleLowerCase("ru-RU").includes("кухн");

  useEffect(()=>{const previous=document.body.style.overflow;document.body.style.overflow="hidden";return()=>{document.body.style.overflow=previous}},[]);
  useEffect(()=>{if(!guestOptions.includes(guests))setGuests(guestOptions[0]||2)},[guestOptions,guests]);

  const beginConfigure=()=>{
    const defaults=(solution.defaultProductNames??solution.productNames).map(norm);
    const nextSelected:Record<string,boolean>={};const nextColors:Record<string,string>={};const nextSizes:Record<string,string>={};const nextQty:Record<string,number>={};
    options.forEach(option=>{const title=norm(option.title);nextSelected[option.id]=defaults.some(target=>target===title||target.includes(title)||title.includes(target));const defaultColor=Object.entries(solution.defaultColors??{}).find(([name])=>norm(name)===title)?.[1]??optionColors(option)[0]??"";const defaultSize=Object.entries(solution.defaultSizes??{}).find(([name])=>norm(name)===title)?.[1]??"";const defaultQty=Object.entries(solution.defaultQuantities??{}).find(([name])=>norm(name)===title)?.[1]??recommendedOptionQuantity(option,guests);nextColors[option.id]=defaultColor;if(defaultSize)nextSizes[option.id]=defaultSize;nextQty[option.id]=defaultQty});
    setSelected(nextSelected);setColors(nextColors);setSizes(nextSizes);setQty(nextQty);setConfigure(true);
  };
  const selectedRows=options.filter(option=>selected[option.id]).map(option=>{const color=colors[option.id]??optionColors(option)[0]??"";const size=sizes[option.id]??"";const available=optionSizes(option,color);const missingSize=available.length>1&&!size;const row=pickOptionVariant(option,color,size);return {option,row,missingSize,quantity:qty[option.id]??recommendedOptionQuantity(option,guests)}});
  const pending=selectedRows.filter(item=>item.missingSize).length;
  const total=selectedRows.reduce((sum,item)=>sum+priceOf(item.row)*item.quantity,0);
  const addSolution=()=>{if(!selectedRows.length||pending)return;addRowsToSharedCart(selectedRows.map(item=>({row:item.row,quantity:item.quantity})));window.location.assign(`${basePath}/?open=cart`)};
  const storyImages=Array.from(new Set([solutionImage(solution,rows),...rows.slice(0,5).map(row=>row.primary_image_url).filter(Boolean)]));

  return <div className="v52-story-backdrop v52-ready-backdrop"><button className="v52-story-dismiss" type="button" onClick={close} aria-label="Закрыть решение"/><section className="v52-story-modal" role="dialog" aria-modal="true" aria-label={solution.name}>
    <header className="v52-story-topbar"><button type="button" onClick={close}>← Готовые решения</button><strong>КУЛЬТУРА ДОМА</strong><button type="button" onClick={close}>×</button></header>
    <div className="v52-story-columns">
      <aside className="v52-story-editorial"><div className="v52-story-title"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно купить как есть или адаптировать под свой дом.</p><span>{solution.collections.join(" · ")}</span></div>{storyImages.map((image,index)=><figure key={`${solution.id}-${index}`}><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={`${solution.name}, ${index+1}`}/>{index===0&&<figcaption>Соберите пространство из уже сочетающихся предметов — без лишнего выбора и перегруженного конструктора.</figcaption>}</figure>)}</aside>
      <section className="v52-story-commerce v52-ready-commerce"><header className="v52-commerce-head"><div><small>{configure?"НАСТРОЙКА РЕШЕНИЯ":"СОСТАВ РЕШЕНИЯ"}</small><h2>{configure?"Оставьте только нужное":"Предметы пространства"}</h2><p>{configure?"Чекбоксы включены только в режиме настройки. Цвет, размер и количество появляются после выбора предмета.":"Каждый предмет можно купить отдельно. Чтобы изменить весь состав, включите режим настройки решения."}</p></div>{configure?<div className="v52-commerce-actions">{isDining&&guestOptions.length>1&&<label className="v52-guests"><span>Персон</span><select value={guests} onChange={event=>setGuests(Number(event.target.value))}>{guestOptions.map(value=><option key={value} value={value}>{value}</option>)}</select></label>}<button className="v52-text-action" type="button" onClick={()=>setConfigure(false)}>Отменить</button></div>:<button className="v52-buy-story" type="button" onClick={beginConfigure}>НАСТРОИТЬ РЕШЕНИЕ</button>}</header>
        <div className="v52-ready-groups">{categories.map(category=><section className="v52-ready-group" key={category.id}><header><h3>{category.title}</h3><span>{category.slots.flatMap(slot=>slot.options).length} поз.</span></header><div className="product-grid v52-story-products">{category.slots.flatMap(slot=>slot.options).map(option=>{const color=colors[option.id]??optionColors(option)[0]??"";const size=sizes[option.id]??"";return <SolutionProductCardV52 key={option.id} option={option} configure={configure} selected={Boolean(selected[option.id])} color={color} size={size} quantity={qty[option.id]??recommendedOptionQuantity(option,guests)} onToggle={()=>setSelected(state=>({...state,[option.id]:!state[option.id]}))} onColor={value=>{setColors(state=>({...state,[option.id]:value}));setSizes(state=>({...state,[option.id]:""}))}} onSize={value=>setSizes(state=>({...state,[option.id]:value}))} onQuantity={value=>setQty(state=>({...state,[option.id]:value}))} onQuick={()=>setQuick(option)}/>})}</div></section>)}</div>
        {configure&&<footer className="v52-purchase-bar"><div><span>{pending?`Выберите размер · ${pending}`:selectedRows.length?`Выбрано ${selectedRows.length} позиций`:"Выберите товары"}</span><strong>{money(total)}</strong></div><button type="button" disabled={!selectedRows.length||pending>0} onClick={addSolution}>ДОБАВИТЬ РЕШЕНИЕ</button></footer>}
      </section>
    </div>
  </section>{quick&&<SolutionQuickAddV52 option={quick} close={()=>setQuick(null)}/>}</div>;
}

export function ReadySolutionsLandingV52({initialScenarioId}:{initialScenarioId?:string}={}){
  const {catalog,rules,error}=useConstructorData();
  const [activeId,setActiveId]=useState(initialScenarioId??"");
  useEffect(()=>{if(initialScenarioId)setActiveId(initialScenarioId)},[initialScenarioId]);
  const cards=useMemo(()=>!catalog?[]:TABLE_SOLUTIONS.map(solution=>{const rows=resolveTableSolutionCatalogRows(catalog.catalog,solution);return {solution,rows,image:solutionImage(solution,rows),count:Array.from(new Set(rows.map(row=>norm(row.product_name)))).length}}),[catalog]);
  const activeSolution=activeId?findTableSolution(activeId):undefined;
  return <div className="v52-ready-page"><IntegratedHeaderV52/><main className="v52-ready-main"><header className="v52-ready-intro"><div><small>КУЛЬТУРА ДОМА · ГОТОВЫЕ РЕШЕНИЯ</small><h1>Готовые решения</h1></div><p>Интерьерные истории, уже собранные стилистом. Откройте решение как журнал, купите отдельный предмет или настройте весь состав в одном окне.</p></header>{error?<div className="v52-ready-state">{error}</div>:!catalog?<div className="v52-ready-state">Загружаем решения…</div>:<section className="v52-ready-grid">{cards.map(({solution,rows,image,count})=><article className="v52-ready-card" key={solution.id}><button type="button" onClick={()=>setActiveId(solution.id)}><span><RemoteImage src={image} fallbackSrc={rows[0]?.primary_image_url} alt={solution.name}/></span><small>{solution.space}</small><h2>{solution.name}</h2><p>{solution.collections.join(" · ")}</p><div><em>{count} позиций</em><b>Открыть →</b></div></button></article>)}</section>}</main>{catalog&&activeSolution&&<ReadySolutionOverlayV52 solution={activeSolution} catalog={catalog} rules={rules} close={()=>setActiveId("")}/>}</div>;
}

export function ReadySolutionDetailV52({scenarioId}:{scenarioId:string}){return <ReadySolutionsLandingV52 initialScenarioId={scenarioId}/>}
