import Link from "next/link";
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
function HeartIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7"><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>}
function BagIcon(){return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.7"><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>}

function StaticHeader(){return <><div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href="/catalog/">ПОДРОБНЕЕ</Link></div><header className="header story-header"><div className="header-left"><Link className="story-menu-button" href="/catalog/?open=menu" aria-label="Открыть меню"><i/><i/><i/></Link></div><Link className="logo" href="/">КУЛЬТУРА ДОМА</Link><div className="header-actions"><Link href="/catalog/?open=search" aria-label="Поиск"><SearchIcon/></Link><Link href="/catalog/?open=account" aria-label="Профиль"><UserIcon/></Link><Link href="/catalog/?open=favorites" aria-label="Избранное"><HeartIcon/></Link><Link href="/catalog/?open=cart" aria-label="Корзина"><BagIcon/></Link></div></header></>}

export default function StoryIndex({mode}:{mode:"capsules"|"collections"}){
  const field=mode==="capsules"?"capsule":"collection";
  const names=unique(PRODUCTS.map(product=>product[field]));
  const title=mode==="capsules"?"Капсулы":"Коллекции";
  return <main className="story-index-page"><StaticHeader/><div className="collections page story-index-shell"><nav className="crumbs"><Link href="/">Главная</Link> / <span>{title}</span></nav><header className="section-head"><p>КУЛЬТУРА ДОМА · EDITORIAL</p><h1>{title}</h1><span>{mode==="capsules"?"Готовые истории для дома, объединённые цветом, орнаментом и настроением.":"Авторские серии предметов, связанные общей идеей, материалами и визуальным языком."}</span></header><div className="story-index-switch"><Link className={mode==="capsules"?"active":""} href="/capsules/">Капсулы</Link><Link className={mode==="collections"?"active":""} href="/collections/">Коллекции</Link></div><section className="collection-grid story-index-grid">{names.map(name=>{const items=PRODUCTS.filter(product=>norm(product[field])===norm(name));const image=mode==="capsules"?(CAPSULE_IMAGES[name]||items[0]?.image):items[0]?.image;const href=mode==="capsules"?`/catalog/?capsule=${encodeURIComponent(name)}`:`/catalog/?collection=${encodeURIComponent(name)}`;return <article key={name}><Link href={href}><img src={asset(image||"/assets/images/image-placeholder.svg")} alt={name}/><div><small>{mode==="capsules"?"КАПСУЛА":"КОЛЛЕКЦИЯ"}</small><h2>{name}</h2><p>{items.length} товаров</p><span>СМОТРЕТЬ <b aria-hidden="true">→</b></span></div></Link></article>})}</section></div></main>
}
