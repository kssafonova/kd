"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "../constructor/data-client";
import { findTableSolution } from "../constructor/table-solutions";
import { resolveTableSolutionCatalogRows } from "../constructor/table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedOptionQuantity,
  type SolutionCategory,
  type SolutionProductOption,
} from "../constructor/table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "../constructor/types";

const CART_KEY = "kultura-cart";
const CART_OFFSET = 998000;
const browserBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const priceOf = (row?: CatalogRow) => Number(String(row?.price || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const norm = (value: string) => String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/[«»"']/g, "").replace(/\s+/g, " ");
const rowImages = (row?: CatalogRow) => Array.from(new Set([row?.primary_image_url, ...(row?.all_image_urls || "").split("|")].filter((value): value is string => Boolean(value))));
const COLLECTION_LABELS: Record<string, string> = { "Камея": "Эхо", "Жар-птица": "Феникс", "Дияф": "Диаф", "Приданное": "Приданое" };
const displayCollectionName = (value: string) => COLLECTION_LABELS[value] || value;
const displayProductName = (value: string) => String(value || "")
  .replace(/мокоши/gi, "Символы")
  .replace(/камея/gi, "Эхо")
  .replace(/жар[ -]?птица/gi, "Феникс")
  .replace(/дияф/gi, "Диаф");

// Merchandising matrix supplied for the four live Ready Solutions. These are
// SOURCE collection names, because CSV matching happens before the public alias.
const SOLUTION_BASE_COLLECTIONS: Record<string, string[]> = {
  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры"],
  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна"],
};
const SOLUTION_EXTRA_COLLECTIONS: Record<string, string[]> = {
  "Зимняя сказка": ["Жар-птица", "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],
  "Красные линии": ["Овация", "Обереги", "Приданое", "Александр"],
  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России", "Жар-птица"],
  "Зеленый салон": ["Камея", "Обереги", "Александр"],
};
const SOURCE_COLLECTION_HINTS = [
  "Мокоши", "Камея", "Жар-птица", "Овация", "Обереги", "Приданное", "Приданое", "Александр",
  "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Купель",
  "Кружево", "Орнаменты России", "Фейерверк", "Дияф", "Ледяные узоры",
  "Лунная сказка", "Нити времени", "Юрма", "Текстура", "Дрёмица",
  "Петербург", "Многоцвет", "Весна",
] as const;
const sourceCollectionForRow = (row?: CatalogRow) => {
  const explicit = String(row?.collection || "").trim();
  if (explicit) return explicit;
  const name = norm(row?.product_name || "");
  if (name.includes("тайн") && name.includes("остров") && name.includes("буян")) return "Тайна острова Буяна";
  if (name.includes("оренбург") && name.includes("узор")) return "Оренбургские узоры";
  if (name.includes("александр")) return "Александр";
  if (name.includes("придан")) return "Приданое";
  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";
};
const solutionConfig = (matrix: Record<string, string[]>, name: string) =>
  Object.entries(matrix).find(([key]) => norm(key) === norm(name))?.[1] || [];

const SOLUTION_REMOVED_PRODUCTS: Record<string, string[]> = {
  "Зимняя сказка": [
    "Тарелка десертная Нити времени",
    "Кружка Нити времени",
    "Чайная пара Нити времени",
    "Салфетка Нити времени",
    "Плейсмат Нити времени",
    "Дорожка Нити времени",
    "Свеча с ароматом Сладкий табак Нити Времени",
    "Свеча с ароматом Копченая клюква Нити Времени",
  ],
  "Красные линии": [
    "Комплект постельного белья с вышивкой Символы",
    "Гетры Оренбургский узор",
    "Носки Оренбургский узор",
  ],
  "Тёплый брутализм": [
    "Тарелка глубокая Юрма",
    "Кружка Юрма",
    "Кофейная пара Юрма",
    "Тарелка обеденная Юрма",
    "Тарелка ассиметричная Юрма",
    "Тарелка асимметричная Юрма",
    "Блюдо овальное Юрма",
    "Стакан Юрма",
    "Кольцо Дрёмица",
    "Набор колец текстура",
    "Хлебница Текстура",
    "Набор для ванной Текстура",
  ],
  "Зеленый салон": [
    "Чайная пара Многоцвет",
    "Молочник Многоцвет",
    "Сахарница Многоцвет",
    "Скатерть Петербург",
    "Бульонная пара Овация",
  ],
};
const productBaseName = (row: CatalogRow) => norm(displayProductName(row.product_name).split(":")[0]);
const isRemovedSolutionProduct = (solutionName: string, row: CatalogRow) => {
  const removed = new Set(solutionConfig(SOLUTION_REMOVED_PRODUCTS, solutionName).map(norm));
  return removed.has(productBaseName(row));
};
const applySolutionCategoryOverrides = (solutionName: string, row: CatalogRow): CatalogRow => {
  if (norm(solutionName) !== norm("Зимняя сказка")) return row;
  const name = productBaseName(row);
  if (name === norm("Плед из кружева")) return { ...row, product_type: "throw" };
  if (name === norm("Подушка с кружевом")) return { ...row, product_type: "decorative_pillow" };
  return row;
};

const COLOR_HEX: Record<string, string> = {
  "белый":"#f6f5f1","молочный":"#ece6da","бежевый":"#d6c4aa","песочный":"#c8aa84","коричневый":"#7b523b","черный":"#1d1d1b","чёрный":"#1d1d1b","синий":"#38506a","темно-синий":"#12263e","ночной синий":"#10233e","голубой":"#9eb8ca","зеленый":"#6f806b","зелёный":"#6f806b","красный":"#8e3d35","бордовый":"#6d2f31","розовый":"#d3aaa5","желтый":"#cfb168","жёлтый":"#cfb168","золотой":"#b59862","серый":"#969696"
};
const swatchColor = (value: string) => COLOR_HEX[norm(value)] || "#d8d5cf";

function useData() {
  const [catalog, setCatalog] = useState<FinalConstructorData | null>(null);
  const [rules, setRules] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let alive = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([nextCatalog, nextRules]) => { if (alive) { setCatalog(nextCatalog); setRules(nextRules); } })
      .catch((reason: unknown) => { if (alive) setError(reason instanceof Error ? reason.message : "Не удалось загрузить данные"); });
    return () => { alive = false; };
  }, []);
  return { catalog, rules, error };
}

function Header() {
  return <><div className="rs71-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</div><header className="rs71-header"><Link href="/" aria-label="Главная" className="rs71-menu">☰</Link><Link href="/" className="rs71-logo">КУЛЬТУРА ДОМА</Link><nav><Link href="/?open=search">Поиск</Link><Link href="/?open=account">Профиль</Link><Link href="/?open=cart">Корзина</Link></nav></header></>;
}
function Footer() { return <footer className="rs71-footer"><strong>КУЛЬТУРА ДОМА</strong><span>Предметы для цельного пространства.</span></footer>; }

type GroupId = "tableware" | "tableTextile" | "bedding" | "decor" | "atmosphere" | "bath";
type GroupItem = { option: SolutionProductOption; subcategoryId: string; subcategoryTitle: string };
type FormGroup = { id: GroupId; title: string; items: GroupItem[] };
const GROUP_META: Record<GroupId,{title:string;categories:string[]}> = {
  tableware:{title:"Посуда и сервировка",categories:["plates","bowls","cupsPairs","greenSalonTeaService","redLinesServing","redLinesTeaService","sugarBowls","milkJugs","teapots","serving","drinkware","cutlery"]},
  tableTextile:{title:"Столовый текстиль",categories:["tableTextile"]},
  bedding:{title:"Постельное бельё",categories:["bedding"]},
  decor:{title:"Декор для дома",categories:["throwsCoverlets","decorativePillows","vases","baskets","games","storage","other"]},
  atmosphere:{title:"Свечи и диффузоры",categories:["atmosphere"]},
  bath:{title:"Для ванной",categories:["bath"]},
};
const GROUP_ORDER: GroupId[] = ["tableware","tableTextile","bedding","decor","atmosphere","bath"];
function buildGroups(categories: SolutionCategory[]): FormGroup[] {
  return GROUP_ORDER.map((id) => {
    const meta = GROUP_META[id];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) => category.slots.flatMap((slot) => slot.options.map((option) => ({ option, subcategoryId: category.id, subcategoryTitle: category.title }))));
    return { id, title: meta.title, items };
  }).filter((group) => group.items.length > 0);
}
function rowId(row: CatalogRow) { const numeric = Number(String(row.offer_id || row.group_id || "").replace(/\D/g,"")); return CART_OFFSET + (numeric > 0 ? numeric : Array.from(row.product_name).reduce((s,c)=>s+c.charCodeAt(0),0)); }
function cartItemFromRow(row: CatalogRow, quantity:number) {
  const images=rowImages(row), price=priceOf(row), color=row.color||"Без цвета", size=row.size||row.volume||"Единый размер", id=rowId(row);
  return { id,name:displayProductName(row.product_name),note:[displayCollectionName(sourceCollectionForRow(row)),row.material].filter(Boolean).join(" · "),price,image:images[0]||"/images/image-placeholder.svg",gallery:images.slice(1),selectedColor:color,selectedSize:size,selectedSkuId:`ready71-${row.offer_id||id}`,quantity,skus:[{id:`ready71-${row.offer_id||id}`,article:row.vendor_code||String(row.offer_id),productId:id,color,colorHex:swatchColor(color),size,material:row.material||"",composition:row.material||"",price,image:images[0]||"/images/image-placeholder.svg",gallery:images.slice(1)}] };
}
function addRowsToSharedCart(rows:Array<{row:CatalogRow;quantity:number}>) {
  let current:any[]=[]; try{current=JSON.parse(localStorage.getItem(CART_KEY)||"[]");}catch{}
  const next=[...current]; rows.forEach(({row,quantity})=>{const item=cartItemFromRow(row,quantity); const index=next.findIndex((x)=>x.id===item.id&&x.selectedColor===item.selectedColor&&x.selectedSize===item.selectedSize); if(index>=0)next[index]={...next[index],quantity:(next[index].quantity||1)+quantity}; else next.push(item);});
  try{localStorage.setItem(CART_KEY,JSON.stringify(next));}catch{}
}

type SelectedRow = { row:CatalogRow; quantity:number; option:SolutionProductOption; group:FormGroup };

function ProductCard({option,selected,color,size,quantity,guests,onToggle,onColor,onSize,onQty}:{option:SolutionProductOption;selected:boolean;color:string;size:string;quantity:number;guests:number;onToggle:()=>void;onColor:(v:string)=>void;onSize:(v:string)=>void;onQty:(v:number)=>void}) {
  const colors=optionColors(option), sizes=optionSizes(option,color), row=pickOptionVariant(option,color,size), image=rowImages(row)[0]||"/images/image-placeholder.svg";
  // READY_AROMA_VARIANT_V74
  const aromaVariant=norm(displayProductName(option.title))===norm("Свеча Феникс");
  return <article className={`rs71-product ${selected?"is-selected":""}`}>
    <div className="rs71-product-media"><RemoteImage src={image} fallbackSrc="/images/image-placeholder.svg" alt={displayProductName(option.title)}/><label className="rs71-check"><input type="checkbox" checked={selected} onChange={onToggle}/><i>✓</i></label></div>
    <div className="rs71-product-copy"><h3>{displayProductName(option.title)}</h3><p>{[displayCollectionName(option.collection||row?.collection||""),row?.material].filter(Boolean).join(" · ")}</p><strong>{money(priceOf(row))}</strong></div>
    {colors.length>1&&(aromaVariant?<div className="rs71-aroma-options"><small>Аромат</small>{colors.map((value)=><button type="button" key={value} className={(color||row?.color)===value?"is-active":""} onClick={()=>onColor(value)}>{value}</button>)}</div>:<div className="rs71-swatches">{colors.map((value)=><button type="button" key={value} title={value} className={(color||row?.color)===value?"is-active":""} style={{background:swatchColor(value)}} onClick={()=>onColor(value)}/>)}</div>)}
    {selected&&<div className="rs71-product-controls">{sizes.length>1&&<div className="rs71-sizes">{sizes.map((value)=><button type="button" key={value} className={size===value?"is-active":""} onClick={()=>onSize(value)}>{value}</button>)}</div>}<div className="rs71-qty"><button type="button" onClick={()=>onQty(Math.max(1,quantity-1))}>−</button><b>{quantity}</b><button type="button" onClick={()=>onQty(quantity+1)}>+</button><span>{option.perPerson?`для ${guests} персон`:"на решение"}</span></div></div>}
  </article>;
}

export function ReadySolutionWizard({scenarioId}:{scenarioId:string}) {
  const solution=findTableSolution(scenarioId); const {catalog,rules,error}=useData();
  const [step,setStep]=useState<1|2|3>(1); const [guests,setGuests]=useState(2); const [selected,setSelected]=useState<Record<string,boolean>>({}); const [colors,setColors]=useState<Record<string,string>>({}); const [sizes,setSizes]=useState<Record<string,string>>({}); const [qty,setQty]=useState<Record<string,number>>({}); const [activeCollections,setActiveCollections]=useState<string[]>([]); const [activeGroup,setActiveGroup]=useState<GroupId|"">(""); const [typeFilter,setTypeFilter]=useState("all"); const [collectionFilter,setCollectionFilter]=useState("all");
  const baseCollections=useMemo(()=>{if(!solution)return[]; const configured=solutionConfig(SOLUTION_BASE_COLLECTIONS,solution.name); return Array.from(new Set((configured.length?configured:solution.collections).filter(Boolean)));},[solution]);
  const baseRows=useMemo(()=>{if(!solution||!catalog)return[]; const resolved=resolveTableSolutionCatalogRows(catalog.catalog,solution).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); const configured=solutionConfig(SOLUTION_BASE_COLLECTIONS,solution.name); if(!configured.length)return resolved; const allowed=new Set(configured.map(norm)); return resolved.filter((row)=>allowed.has(norm(sourceCollectionForRow(row))));},[catalog,solution]);
  useEffect(()=>{if(solution&&!activeCollections.length)setActiveCollections(baseCollections);},[solution,baseCollections,activeCollections.length]);
  const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; return solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);
  const extendedRows=useMemo(()=>{if(!catalog||!solution)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...baseRows,...extra].filter((row)=>!isRemovedSolutionProduct(solution.name,row)).map((row)=>applySolutionCategoryOverrides(solution.name,row));},[catalog,solution,baseRows,activeCollections]);
  const categories=useMemo(()=>solution?buildSolutionCategories(extendedRows,solution.space):[],[extendedRows,solution]); const groups=useMemo(()=>buildGroups(categories),[categories]); const options=useMemo(()=>groups.flatMap((g)=>g.items.map((i)=>i.option)),[groups]); const guestOptions=useMemo(()=>solution?deriveGuestOptions(solution,rules):[2,4,6],[solution,rules]);
  useEffect(()=>{if(!groups.length)return; setActiveGroup((current)=>current&&groups.some((g)=>g.id===current)?current:groups[0].id);},[groups]);
  useEffect(()=>{if(!solution||!options.length)return; setGuests((g)=>guestOptions.includes(g)?g:(guestOptions[0]||2)); const defaults=new Set((solution.defaultProductNames||[]).map(norm)); setSelected((current)=>Object.keys(current).length?current:Object.fromEntries(options.map((o)=>[o.id,defaults.has(norm(o.title))]))); setColors((current)=>Object.keys(current).length?current:Object.fromEntries(options.map((o)=>[o.id,solution.defaultColors?.[o.title]||optionColors(o)[0]||""]))); setSizes((current)=>Object.keys(current).length?current:Object.fromEntries(options.map((o)=>{const c=solution.defaultColors?.[o.title]||optionColors(o)[0]||"";return[o.id,solution.defaultSizes?.[o.title]||optionSizes(o,c)[0]||""];}))); setQty((current)=>Object.keys(current).length?current:Object.fromEntries(options.map((o)=>[o.id,solution.defaultQuantities?.[o.title]||recommendedOptionQuantity(o,guestOptions[0]||2)])));},[solution,options,guestOptions]);
  useEffect(()=>{setQty((current)=>{const next={...current}; options.forEach((o)=>{if(o.perPerson)next[o.id]=recommendedOptionQuantity(o,guests);}); return next;});},[guests,options]);
  const selectedRows=useMemo<SelectedRow[]>(()=>groups.flatMap((group)=>group.items.flatMap(({option})=>{if(!selected[option.id])return[]; const row=pickOptionVariant(option,colors[option.id]||"",sizes[option.id]||""); return row?[{row,quantity:Math.max(1,qty[option.id]||recommendedOptionQuantity(option,guests)),option,group}]:[];})),[groups,selected,colors,sizes,qty,guests]); const total=selectedRows.reduce((sum,item)=>sum+priceOf(item.row)*item.quantity,0);
  if(!solution)return <div className="rs71-page"><Header/><main className="rs71-state">Решение не найдено.</main></div>; if(error)return <div className="rs71-page"><Header/><main className="rs71-state">{error}</main></div>; if(!catalog||!groups.length)return <div className="rs71-page"><Header/><main className="rs71-state">Собираем решение…</main></div>;
  const currentGroup=groups.find((g)=>g.id===activeGroup)||groups[0]; const subtypes=Array.from(new Map(currentGroup.items.map((i)=>[i.subcategoryId,i.subcategoryTitle])).entries()); const groupCollections=Array.from(new Set(currentGroup.items.map((i)=>i.option.collection).filter(Boolean))).slice(0,6); const visibleItems=currentGroup.items.filter((item)=>(typeFilter==="all"||item.subcategoryId===typeFilter)&&(collectionFilter==="all"||norm(item.option.collection)===norm(collectionFilter)));
  const toggleCollection=(name:string)=>setActiveCollections((current)=>current.some((c)=>norm(c)===norm(name))?current.filter((c)=>norm(c)!==norm(name)):[...current,name]);
  const addToCart=()=>{if(!selectedRows.length)return; addRowsToSharedCart(selectedRows.map(({row,quantity})=>({row,quantity}))); window.location.href=`${browserBasePath}/?open=cart`;};
  return <div className="rs71-page"><Header/><main className="rs71-shell">
    <nav className="rs71-crumbs"><Link href="/ready-solutions/">← Готовые решения</Link></nav>
    {step<3&&<section className={`rs71-hero ${step===2?"is-compact":""}`}><div className="rs71-hero-media"><RemoteImage src={solution.heroImage||baseRows[0]?.primary_image_url||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={solution.name}/></div><div className="rs71-hero-copy"><small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small><h1>{solution.name}</h1><p>Готовая композиция, которую можно адаптировать под своё пространство.</p><div>{activeCollections.slice(0,6).map((c)=><span key={c}>{displayCollectionName(c)}</span>)}</div></div></section>}
    <nav className="rs71-steps" aria-label="Шаги"><button className={step===1?"is-active":""} onClick={()=>setStep(1)}><span>01</span>Параметры</button><button className={step===2?"is-active":""} onClick={()=>setStep(2)}><span>02</span>Состав</button><button className={step===3?"is-active":""} disabled={!selectedRows.length} onClick={()=>setStep(3)}><span>03</span>Результат</button></nav>
    {step===1&&<section className="rs71-parameters"><header><small>ПАРАМЕТРЫ</small><h2>Настройте основу</h2><p>Количество персон и коллекции определяют состав решения.</p></header><div className="rs71-param-block"><h3>Количество персон</h3><nav className="rs71-person-rail">{guestOptions.map((v)=><button key={v} className={guests===v?"is-active":""} onClick={()=>setGuests(v)}>{v}</button>)}</nav></div><div className="rs71-param-block"><h3>Коллекции в решении</h3><div className="rs71-collection-grid">{activeCollections.map((name)=>{const row=catalog.catalog.find((r)=>norm(sourceCollectionForRow(r))===norm(name)); return <button type="button" key={name} className="is-active" onClick={()=>toggleCollection(name)}><RemoteImage src={rowImages(row)[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={name}/><i>✓</i><span>{displayCollectionName(name)}</span></button>;})}</div>{extraChoices.length>0&&<><h4>Добавить коллекцию</h4><div className="rs71-collection-grid is-extra">{extraChoices.map((name)=>{const row=catalog.catalog.find((r)=>norm(sourceCollectionForRow(r))===norm(name)); const active=activeCollections.some((c)=>norm(c)===norm(name)); return <button type="button" key={name} className={active?"is-active":""} onClick={()=>toggleCollection(name)}><RemoteImage src={rowImages(row)[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={name}/><i>{active?"✓":"+"}</i><span>{displayCollectionName(name)}</span></button>;})}</div></>}</div></section>}
    {step===2&&<section className="rs71-compose"><header><small>СОСТАВ РЕШЕНИЯ</small><h2>Предметы решения</h2><p>Выберите нужные товары и настройте цвет, размер и количество.</p></header><nav className="rs71-group-rail">{groups.map((g)=><button key={g.id} className={g.id===currentGroup.id?"is-active":""} onClick={()=>{setActiveGroup(g.id);setTypeFilter("all");setCollectionFilter("all");}}>{g.title}<small>{g.items.filter(({option})=>selected[option.id]).length}</small></button>)}</nav><div className="rs71-filter-rails">{subtypes.length>1&&<nav><button className={typeFilter==="all"?"is-active":""} onClick={()=>setTypeFilter("all")}>Все</button>{subtypes.map(([id,title])=><button key={id} className={typeFilter===id?"is-active":""} onClick={()=>setTypeFilter(id)}>{title}</button>)}</nav>}{groupCollections.length>1&&<nav><button className={collectionFilter==="all"?"is-active":""} onClick={()=>setCollectionFilter("all")}>Все коллекции</button>{groupCollections.map((c)=><button key={c} className={norm(collectionFilter)===norm(c)?"is-active":""} onClick={()=>setCollectionFilter(c)}>{displayCollectionName(c)}</button>)}</nav>}</div><div className="rs71-products">{visibleItems.map(({option})=><ProductCard key={option.id} option={option} selected={Boolean(selected[option.id])} color={colors[option.id]||""} size={sizes[option.id]||""} quantity={qty[option.id]||recommendedOptionQuantity(option,guests)} guests={guests} onToggle={()=>setSelected((c)=>({...c,[option.id]:!c[option.id]}))} onColor={(value)=>{setColors((c)=>({...c,[option.id]:value}));setSizes((c)=>({...c,[option.id]:optionSizes(option,value)[0]||""}));}} onSize={(value)=>setSizes((c)=>({...c,[option.id]:value}))} onQty={(value)=>setQty((c)=>({...c,[option.id]:Math.max(1,value)}))}/>)}</div></section>}
    {step===3&&<section className="rs71-result"><header><small>ВАШЕ РЕШЕНИЕ</small><h1>{solution.name}</h1><p>{selectedRows.length} предметов · {guests} персон</p></header><div className="rs71-moodboard">{selectedRows.map(({row,option},index)=><div key={`${option.id}-${row.offer_id}`} className={`rs71-mood-${(index%7)+1}`}><RemoteImage src={rowImages(row)[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={displayProductName(option.title)}/></div>)}</div><div className="rs71-result-groups">{groups.map((group)=>{const items=selectedRows.filter((item)=>item.group.id===group.id); if(!items.length)return null; return <details key={group.id}><summary><span>{group.title}</span><small>{items.length}</small><b>+</b></summary><div>{items.map(({row,option,quantity})=><article key={`${option.id}-${row.offer_id}`}><RemoteImage src={rowImages(row)[0]||"/images/image-placeholder.svg"} fallbackSrc="/images/image-placeholder.svg" alt={displayProductName(option.title)}/><div><h3>{displayProductName(option.title)}</h3><p>{[displayCollectionName(sourceCollectionForRow(row)||option.collection||""),row.color,row.size||row.volume].filter(Boolean).join(" · ")}</p><span>{quantity} × {money(priceOf(row))}</span></div><button type="button" onClick={()=>{setActiveGroup(group.id);setStep(2);}}>Заменить</button><button type="button" onClick={()=>setSelected((c)=>({...c,[option.id]:false}))}>Удалить</button></article>)}</div></details>;})}</div><button type="button" className="rs71-edit" onClick={()=>setStep(2)}>Изменить состав</button></section>}
  </main>
  <div className="rs71-commerce"><div><small>{step===1?`${activeCollections.length} коллекции`:step===2?`${selectedRows.length} выбрано`:`${selectedRows.length} предметов`}</small><strong>{money(total)}</strong></div>{step===1&&<button onClick={()=>setStep(2)}>К СОСТАВУ</button>}{step===2&&<button disabled={!selectedRows.length} onClick={()=>setStep(3)}>К РЕЗУЛЬТАТУ</button>}{step===3&&<button onClick={addToCart}>ДОБАВИТЬ В КОРЗИНУ</button>}</div><Footer/></div>;
}
