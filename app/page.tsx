"use client";

import { assetUrl } from "./assets";
import { RemoteImage } from "./remote-image";
import { catalogProductOverrides, type CatalogSku } from "./catalog-data";

// CATALOG_SKU_MODEL_V1

import { useEffect, useMemo, useRef, useState } from "react";

type View = "home" | "catalog" | "collections" | "editorial" | "product";
type Product = {
  id: number;
  name: string;
  note: string;
  price: number;
  oldPrice?: number;
  image: string;
  position?: string;
  badge?: string;
  selectedColor?: string;
  selectedSize?: string;
  quantity?: number;
  colorVariants?: ColorVariant[];
  hasRichContent?: boolean;
  gallery?: string[];
  article?: string;
  skus?: CatalogSku[];
  selectedSkuId?: string;
};

type ColorVariant = { name: string; hex: string; image: string; gallery?: string[]; position?: string };
type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number };
type Slide = { category:string; eyebrow:string; title:string; subtitle:string; image:string; secondaryImage?:string; mobileVideo?:string; align:string; destination:View };
type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };

const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

type IconName = "pin" | "search" | "user" | "heart" | "bag" | "cart-add" | "filter" | "close" | "chevron" | "share" | "plus" | "minus" | "arrow" | "mail";
function Icon({ name, filled = false }: { name: IconName; filled?: boolean }) {
  const common = { fill: filled ? "currentColor" : "none", stroke: "currentColor", strokeWidth: 1.7, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "pin") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if (name === "search") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if (name === "user") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if (name === "heart") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if (name === "bag") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if (name === "cart-add") return <svg className="cart-add-icon" width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M19.9023 5.46722C19.9023 5.46722 18.3349 1.23513 12.8488 1.23513C7.36279 1.23513 5.79535 5.46722 5.79535 5.46722" stroke="#1D1D1F" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/><path d="M23.7903 9.66602C23.9826 9.6525 24.1729 9.71072 24.3276 9.82445L24.435 9.91812L24.4378 9.92088C24.6787 10.1736 24.7432 10.5335 24.6706 10.8356V10.8384L23.4817 15.6822C22.9732 15.518 22.4395 15.4111 21.8878 15.3667L22.9844 11.3594L2.82812 11.375L3.58452 14.0455C3.59597 14.0919 3.77911 14.8323 3.95923 15.5609C4.04929 15.9252 4.13898 16.2879 4.20583 16.5583C4.23918 16.6932 4.26769 16.8063 4.28711 16.8848C4.2886 16.8909 4.28986 16.8971 4.29124 16.9027L4.7679 18.8314C4.97491 19.6766 5.3842 20.3959 5.91272 20.891C6.43983 21.3849 7.05283 21.6309 7.66094 21.628H14.3025C14.2752 21.8801 14.2598 22.136 14.2598 22.3954C14.2598 22.7674 14.2897 23.1328 14.3452 23.4892H7.6637C6.61391 23.4929 5.61299 23.0647 4.80235 22.3072C3.99487 21.5501 3.41387 20.501 3.12576 19.3246L2.6491 17.3959C2.64772 17.3903 2.64646 17.3827 2.64497 17.3766C2.62553 17.298 2.59706 17.1852 2.56369 17.0501C2.49688 16.7798 2.40708 16.4183 2.31709 16.0541C2.13694 15.3251 1.95383 14.5837 1.94237 14.5373L1.029 10.8425L1.00834 10.7268C0.973543 10.4528 1.0457 10.1447 1.26182 9.92088L1.2632 9.92226C1.35393 9.82758 1.46353 9.75727 1.58281 9.71423C1.58574 9.71301 1.5884 9.71119 1.59108 9.7101L1.59521 9.70872C1.61323 9.70256 1.63192 9.69844 1.65031 9.69357C1.67235 9.6873 1.69064 9.67981 1.70542 9.67704C1.71452 9.67536 1.72434 9.67684 1.73297 9.67566C1.75436 9.67236 1.77608 9.67168 1.79772 9.67015C1.81045 9.66954 1.8217 9.66614 1.83078 9.66602H23.7903Z" fill="#1D1D1F"/><line x1="21.5078" y1="18.076" x2="21.5078" y2="27.1563" stroke="black" strokeWidth="1.5" strokeLinecap="round"/><line x1="17.2812" y1="22.9462" x2="26.3615" y2="22.9462" stroke="black" strokeWidth="1.5" strokeLinecap="round"/></svg>;
  if (name === "filter") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M3 6h8m4 0h6M3 12h3m4 0h11M3 18h11m4 0h3"/><circle cx="13" cy="6" r="2"/><circle cx="8" cy="12" r="2"/><circle cx="16" cy="18" r="2"/></svg>;
  if (name === "close") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if (name === "share") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M12 16V3m0 0L7.5 7.5M12 3l4.5 4.5"/><path d="M5 11v9h14v-9"/></svg>;
  if (name === "plus") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M12 5v14M5 12h14"/></svg>;
  if (name === "minus") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M5 12h14"/></svg>;
  if (name === "mail") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m4 7 8 6 8-6"/></svg>;
  if (name === "arrow") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m8 4 8 8-8 8"/></svg>;
}

function findProductSku(product:Product,color?:string,size?:string){
  if(!product.skus?.length)return undefined;
  const selectedById=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
  if(selectedById&&(!color||selectedById.color===color)&&(!size||selectedById.size===size))return selectedById;
  return product.skus.find(item=>(!color||item.color===color)&&(!size||item.size===size))
    ??product.skus.find(item=>!color||item.color===color)
    ??product.skus[0];
}
function getProductSizeOptions(product:Product,color?:string){
  if(product.skus?.length){
    const rows=product.skus.filter(item=>!color||item.color===color);
    return Array.from(new Map(rows.map(item=>[item.size,[item.size,item.price] as const])).values());
  }
  return [["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
}

function getProductImages(product:Product){
  if(product.skus?.length){
    const selectedById=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
    const mediaColor=product.selectedColor??selectedById?.color;
    const mediaSku=product.skus.find(item=>!mediaColor||item.color===mediaColor)??product.skus[0];
    return Array.from(new Set([mediaSku.image,...mediaSku.gallery].filter(Boolean)));
  }
  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;
  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];
  return Array.from(new Set(sources.filter(Boolean)));
}
function ScrollableProductMedia({product,alt,className="",position,activeIndex,onActiveIndexChange}:{product:Product;alt:string;className?:string;position?:string;activeIndex?:number;onActiveIndexChange?:(index:number)=>void}){
  const images=getProductImages(product);
  const vertical=className.includes("pdp-product-media");
  const trackRef=useRef<HTMLDivElement>(null);
  const [mobile,setMobile]=useState(false);
  const imagesKey=images.join("|");

  useEffect(()=>{
    if(!vertical)return;
    const mediaQuery=window.matchMedia("(max-width: 900px)");
    const update=()=>setMobile(mediaQuery.matches);
    update();
    mediaQuery.addEventListener?.("change",update);
    return()=>mediaQuery.removeEventListener?.("change",update);
  },[vertical]);

  useEffect(()=>{
    if(!vertical||!mobile||activeIndex===undefined)return;
    const node=trackRef.current;
    const target=node?.children[activeIndex] as HTMLElement|undefined;
    if(!node||!target)return;
    node.scrollTo({left:target.offsetLeft,top:0,behavior:"smooth"});
  },[activeIndex,mobile,vertical,imagesKey]);

  useEffect(()=>{
    if(!vertical||mobile||!onActiveIndexChange)return;
    const node=trackRef.current;
    if(!node)return;
    const children=Array.from(node.children) as HTMLElement[];
    const observer=new IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting);
      if(!visible.length)return;
      visible.sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
      const next=Number((visible[0].target as HTMLElement).dataset.pdpImageIndex??0);
      if(Number.isFinite(next))onActiveIndexChange(next);
    },{root:null,rootMargin:"-110px 0px -38% 0px",threshold:[.15,.3,.5,.7,.85]});
    children.forEach(child=>observer.observe(child));
    return()=>observer.disconnect();
  },[vertical,mobile,onActiveIndexChange,imagesKey]);

  const syncMobileIndex=()=>{
    if(!vertical||!mobile||!onActiveIndexChange)return;
    const node=trackRef.current;
    if(!node||node.clientWidth<=0)return;
    const next=Math.max(0,Math.min(images.length-1,Math.round(node.scrollLeft/node.clientWidth)));
    if(next!==activeIndex)onActiveIndexChange(next);
  };

  return <div ref={trackRef} className={`product-media-scroll ${images.length>1?"is-scrollable":""} ${vertical?"vertical-media":"horizontal-media"} ${className}`.trim()} role="group" aria-label={`${alt}: ${images.length} фото`} onScroll={vertical&&mobile?syncMobileIndex:undefined}>{images.map((src,index)=><RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} data-pdp-image-index={vertical?index:undefined} style={{objectPosition:position||product.position||"center"}} draggable={false}/>)}</div>;
}
function ProductRail({items,onProduct,onQuick,favorite,favorites,className=""}:{items:Product[];onProduct:(product:Product)=>void;onQuick:(product:Product)=>void;favorite:(id:number)=>void;favorites:number[];className?:string}){
  return <div className={`product-rail-shell ${className}`.trim()}>
    <div className="product-rail">{items.map(item=><ProductCard key={`${className}-${item.id}`} product={item} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
  </div>;
}

const baseProducts: Product[] = [
  { id: 1, name: "Постельное бельё «Русский узор»", note: "лён и хлопок, вышивка", price: 18990, oldPrice: 25990, image: "/images/russian-bedroom.png", position: "center", hasRichContent: true, colorVariants: [
    { name: "Молочный", hex: "#f1eee7", image: "/images/russian-bedroom.png" }, { name: "Песочный", hex: "#c5ad8e", image: "/images/beige-bedroom.png" }, { name: "Ночной синий", hex: "#12243e", image: "/images/zip-collection-night.png" },
  ] },
  { id: 2, name: "Хлопковый пододеяльник с оборкой", note: "хлопок, 200×220 см", price: 18990, image: "/images/zip-product-bed.png", badge: "НОВИНКА", gallery: ["/images/zip-product-bed.png","/images/classic-bedroom.png","/images/beige-bedroom.png"], colorVariants: [
    { name: "Белый", hex: "#f7f6f1", image: "/images/zip-product-bed.png" }, { name: "Льняной", hex: "#d2c1aa", image: "/images/beige-bedroom.png" }, { name: "Небесный", hex: "#9fb2c6", image: "/images/blue-bedroom.png" },
  ] },
  { id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: 2990, oldPrice: 3990, image: "/images/beige-bedroom.png", position: "58% 48%", colorVariants: [
    { name: "Молочный", hex: "#eee8dc", image: "/images/beige-bedroom.png", position: "center 40%" }, { name: "Белый", hex: "#fafafa", image: "/images/zip-product-bed.png" }, { name: "Синий", hex: "#1c3551", image: "/images/zip-collection-night.png" },
  ] },
  { id: 4, name: "Комплект «Нити времени»", note: "сатин, вышивка", price: 20990, oldPrice: 29990, image: "/images/time-hero.png", badge: "КАПСУЛА", hasRichContent: true, colorVariants: [
    { name: "Ночной синий", hex: "#10233e", image: "/images/time-hero.png" }, { name: "Небесно-голубой", hex: "#9eb6cf", image: "/images/blue-bedroom.png" }, { name: "Жемчужный", hex: "#e8e5de", image: "/images/zip-product-bed.png" },
  ] },
  { id: 5, name: "Тарелка «Лунная сказка»", note: "фарфор, ручная роспись", price: 4990, oldPrice: 6990, image: "/images/moon-plate.png", position: "center", colorVariants: [
    { name: "Ночной синий", hex: "#0c2340", image: "/images/moon-plate.png" }, { name: "Молочный", hex: "#eee8db", image: "/images/zip-hero-summer.png" },
  ] },
  { id: 6, name: "Плед из льна и хлопка", note: "140×200 см", price: 9990, oldPrice: 13990, image: "/images/beige-bedroom.png", position: "65% 80%", gallery: ["/images/beige-bedroom.png","/images/classic-bedroom.png","/images/zip-product-bed.png"], colorVariants: [
    { name: "Песочный", hex: "#b69a78", image: "/images/beige-bedroom.png" }, { name: "Белый", hex: "#f4f2ec", image: "/images/zip-product-bed.png" }, { name: "Синий", hex: "#203753", image: "/images/zip-collection-night.png" },
  ] },
  { id: 7, name: "Стёганое покрывало «Бархатный ритм»", note: "бархат, 220×240 см", price: 12990, image: "/images/beige-quilt.jpg", colorVariants: [
    { name: "Песочный", hex: "#c9a982", image: "/images/beige-quilt.jpg" }, { name: "Пудровый", hex: "#e7bca5", image: "/images/peach-sheet.jpg" },
  ] },
  { id: 8, name: "Натяжная простыня из сатина", note: "сатин, 160×200 см", price: 4990, image: "/images/peach-sheet.jpg", colorVariants: [
    { name: "Пудровый", hex: "#e6bca8", image: "/images/peach-sheet.jpg" }, { name: "Молочный", hex: "#efeae1", image: "/images/zip-product-bed.png" },
  ] },
  { id: 9, name: "Сервиз «Северное сияние»", note: "костяной фарфор, 6 персон", price: 24990, image: "/images/russian-service-blue.png", colorVariants:[{name:"Бело-голубой",hex:"#d9edf0",image:"/images/russian-service-blue.png"},{name:"Ночной синий",hex:"#10233e",image:"/images/time-table.png"}] },
  { id: 10, name: "Чайная пара «Нити времени»", note: "костяной фарфор, 250 мл", price: 4490, image: "/images/time-tea-pair.png", gallery:["/images/time-tea-pair.png","/images/time-mug.png","/images/time-table.png"], colorVariants:[{name:"Ночной синий",hex:"#10233e",image:"/images/time-tea-pair.png"}] },
  { id: 11, name: "Подушка «Небесная гладь»", note: "бархат, 25×60 см", price: 4990, image: "/images/sky-bolster.png", colorVariants:[{name:"Небесный",hex:"#9fc2d3",image:"/images/sky-bolster.png"},{name:"Ночной синий",hex:"#203753",image:"/images/time-hero.png"}] },
  { id: 12, name: "Комплект «Голубая светлица»", note: "сатин, вышивка гладью", price: 21990, image: "/images/blue-bedding-vertical.png", hasRichContent: true, colorVariants:[{name:"Ледяной голубой",hex:"#afcbd1",image:"/images/blue-bedding-vertical.png"},{name:"Белый",hex:"#f4f2ec",image:"/images/zip-product-bed.png"}] },
];

const products: Product[] = baseProducts.map(base=>{
  const override=catalogProductOverrides[base.id];
  if(!override)return base;
  const first=override.skus[0];
  const colors=Array.from(new Map(override.skus.map(item=>[item.color,item])).values());
  return {
    ...base,
    name:override.name,
    note:override.note,
    article:override.article,
    skus:override.skus,
    price:Math.min(...override.skus.map(item=>item.price)),
    image:first.image,
    gallery:first.gallery,
    colorVariants:colors.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery}))
  };
});

const slides:Slide[] = [
  { category: "НОВИНКИ", eyebrow: "НОВАЯ ГЛАВА", title: "Дом в цвету", subtitle: "Авторские вазы и сервировка для долгих летних встреч", image: "/images/editorial-vases.webp", secondaryImage: "/images/editorial-table.webp", mobileVideo: "/images/kultura-home-mobile.mp4", align: "left", destination: "catalog" as View },
  { category: "СПАЛЬНЯ", eyebrow: "СПАЛЬНЯ", title: "Белая глава", subtitle: "Постельное бельё с деликатной вышивкой", image: "/images/russian-bedroom.png", align: "left", destination: "catalog" as View },
  { category: "КУХНЯ И СТОЛОВАЯ", eyebrow: "СЕРВИРОВКА", title: "Тайна острова Буяна", subtitle: "Фарфор, сотканный из моря и русского орнамента", image: "/images/buyan-editorial.png", align: "right", destination: "catalog" as View },
  { category: "ДЕКОР ДЛЯ ДОМА", eyebrow: "ТИХИЕ ДЕТАЛИ", title: "Естественные оттенки", subtitle: "Тактильный декор для спокойного интерьера", image: "/images/beige-bedroom.png", align: "left", destination: "catalog" as View },
  { category: "КАПСУЛЫ И КОЛЛЕКЦИИ", eyebrow: "КАПСУЛА", title: "Нити времени", subtitle: "Тишина, свет и вечные истории", image: "/images/time-hero.png", align: "right", destination: "collections" as View },
];

const discountOf = (product: Product) => product.oldPrice ? Math.round((1-product.price/product.oldPrice)*100) : 0;

const categories = [
  ["Спальня", "/images/classic-bedroom.png"],
  ["Кухня и столовая", "/images/moon-plate.png"],
  ["Капсулы и коллекции", "/images/time-collection.png"],
  ["Домашний текстиль", "/images/russian-bedroom.png"],
  ["Ванная", "/images/zip-product-bed.png"],
];

const slideProductIds = [
  [9,10,11,12],
  [1,2,7,12],
  [9,10,5,3],
  [3,6,2,4],
  [4,5,1,2],
];

type Editorial = { id:string; name:string; kind:"КАПСУЛА"|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string[]; productIds:number[] };
const editorials:Editorial[] = [
  { id:"luna", name:"Лунная сказка", kind:"КАПСУЛА", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Интерактивный editorial о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png","/images/editorial/caps_luna_serviz2.png","/images/editorial/caps_luna_serviz3.png"], productIds:[4,10,5,6,3] },
  { id:"time", name:"Нити времени", kind:"КАПСУЛА", lead:"Вдохновлена движением звёзд и бесконечной красотой ночного неба.", detail:"Каждая деталь — как напоминание о чём-то важном. Нежные оттенки, благородные материалы и вышивка, созданная с вниманием к вечному.", description:"Капсула о тишине, свете и вечных историях.", images:["/images/time-hero.png","/images/night-editorial.png","/images/blue-bedroom.png","/images/moon-plate.png"], productIds:[4,5,3,6] },
  { id:"buyan", name:"Тайна острова Буяна", kind:"КАПСУЛА", lead:"Солнце, ветер и солёный воздух в узорах русского фарфора.", detail:"Кобальтовые цветы и чистые линии сервировки переносят к морю, где каждый предмет становится частью общего пейзажа.", description:"Сервировка, созданная для долгих летних встреч.", images:["/images/buyan-editorial.png","/images/zip-hero-summer.png","/images/moon-plate.png","/images/poetry-editorial.png"], productIds:[5,3,1,6] },
  { id:"poetry", name:"Стихи", kind:"КОЛЛЕКЦИЯ", lead:"Красота в словах, жестах и продуманных мелочах.", detail:"Строки на ткани напоминают: самое важное остаётся рядом — в утреннем чае, семейном столе и прикосновении натурального льна.", description:"Поэтическая коллекция для тихих домашних ритуалов.", images:["/images/poetry-editorial.png","/images/zip-hero-summer.png","/images/russian-bedroom.png","/images/beige-bedroom.png"], productIds:[1,3,6,5] },
  { id:"firebird", name:"Жар-птица", kind:"КОЛЛЕКЦИЯ", lead:"Сказочные узоры и тёплые краски для современного дома.", detail:"Образ Жар-птицы раскрывается в вышивке, насыщенных оттенках и деталях, которые хочется рассматривать.", description:"Русская сказка, рассказанная языком предметного дизайна.", images:["/images/russian-bedroom.png","/images/classic-bedroom.png","/images/moon-plate.png","/images/time-collection.png"], productIds:[1,5,3,4] },
];

export default function Home() {
  const [view, setView] = useState<View>("home");
  const [menu, setMenu] = useState(false);
  const [menuSection, setMenuSection] = useState("");
  const [search, setSearch] = useState(false);
  const [account, setAccount] = useState(false);
  const [favoritesOpen, setFavoritesOpen] = useState(false);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [filters, setFilters] = useState(false);
  const [plpSize, setPlpSize] = useState<Product | null>(null);
  const [plpAdded, setPlpAdded] = useState<CartItem | null>(null);
  const [selected, setSelected] = useState<Product>(products[1]);
  const [editorial, setEditorial] = useState<Editorial>(editorials[0]);
  const [catalogCategory,setCatalogCategory]=useState("Все товары");
  const [sizeSheet, setSizeSheet] = useState(false);
  const [size, setSize] = useState("Евро 200×220");
  const [cart, setCart] = useState<CartItem[]>([]);
  const [cartOpen, setCartOpen] = useState(false);
  const [checkoutOpen, setCheckoutOpen] = useState(false);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [recentlyViewed,setRecentlyViewed]=useState<number[]>([]);
  const [slide, setSlide] = useState(0);
  const [toast, setToast] = useState("");

  useEffect(() => {
    document.body.style.overflow = menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen]);
  useEffect(()=>{try{const savedProfile=localStorage.getItem("kultura-profile");const savedFavorites=localStorage.getItem("kultura-favorites");const savedViewed=localStorage.getItem("kultura-viewed");if(savedProfile)setProfile(JSON.parse(savedProfile));if(savedFavorites)setFavorites(JSON.parse(savedFavorites));if(savedViewed)setRecentlyViewed(JSON.parse(savedViewed))}catch{}},[]);
  useEffect(()=>{localStorage.setItem("kultura-favorites",JSON.stringify(favorites))},[favorites]);
  useEffect(()=>{if(profile)localStorage.setItem("kultura-profile",JSON.stringify(profile));else localStorage.removeItem("kultura-profile")},[profile]);
  useEffect(()=>{localStorage.setItem("kultura-viewed",JSON.stringify(recentlyViewed))},[recentlyViewed]);

  const total = useMemo(() => cart.reduce((sum, item) => sum + item.price * item.quantity, 0), [cart]);
  const cartCount = useMemo(() => cart.reduce((sum, item) => sum + item.quantity, 0), [cart]);
  const go = (next: View) => { setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };
  const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog")};
  const add = (product: Product, chosenSize = size, quantity = product.quantity ?? 1) => {
    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const selectedSku=findProductSku(product,product.selectedColor,chosenSize);
    const item: CartItem = { ...product, price:selectedSku?.price??product.price, image:selectedSku?.image??selectedVariant?.image??product.image, gallery:selectedSku?.gallery??product.gallery, position:selectedVariant?.position??product.position, selectedSize:chosenSize, selectedColor:selectedSku?.color??selectedVariant?.name??"Молочный", selectedSkuId:selectedSku?.id, quantity };
    setCart((current) => [...current, item]);
    setPlpSize(null); setSizeSheet(false); setCartOpen(true);
  };
  const addFromPLP = (product: Product, chosenSize: string, quantity: number, unitPrice: number) => {
    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const selectedSku=findProductSku(product,product.selectedColor,chosenSize);
    const item: CartItem = { ...product, price:selectedSku?.price??unitPrice, image:selectedSku?.image??selectedVariant?.image??product.image, gallery:selectedSku?.gallery??product.gallery, position:selectedVariant?.position??product.position, selectedSize:chosenSize, selectedColor:selectedSku?.color??selectedVariant?.name??"Молочный", selectedSkuId:selectedSku?.id, quantity };
    setCart((current)=>[...current,item]); setPlpSize(null); setPlpAdded(item);
  };
  const favorite = (id: number) => setFavorites((old) => old.includes(id) ? old.filter((x) => x !== id) : [...old, id]);
  const openProduct=(product:Product)=>{setSelected(product);setRecentlyViewed(current=>[product.id,...current.filter(id=>id!==product.id)].slice(0,6));go("product")};
  const updateCartItem = (index:number, patch:Partial<CartItem>) => setCart(current=>current.map((item,itemIndex)=>itemIndex===index?{...item,...patch}:item));
  const notice = (text: string) => { setToast(text); window.setTimeout(() => setToast(""), 2200); };

  return (
    <main className={`view-${view}`}>
      <div className="promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <button onClick={() => go("catalog")}>ПОДРОБНЕЕ</button></div>
      <Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />
      {view === "home" && <HomeView go={go} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} />}
      {view === "catalog" && <CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />}
      {view === "collections" && <CollectionsView openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}
      {view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} quickAdd={setPlpSize} addToCart={(product)=>add(product,product.selectedSize,product.quantity)} />}
      {view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} recentlyViewed={recentlyViewed} />}
      <Footer go={go} notice={notice} />

      {menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} />}
      {search && <Search close={() => setSearch(false)} choose={(p) => { setSelected(p); setSearch(false); go("product"); }} />}
      {account && <Account profile={profile} close={() => setAccount(false)} notice={notice} save={setProfile} logout={()=>setProfile(null)} />}
      {favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setSelected(product);setFavoritesOpen(false);go("product")}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}
      {filters && <Filters close={() => setFilters(false)} apply={() => { setFilters(false); notice("Фильтры применены"); }} />}
      {plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,quantity,unitPrice) => addFromPLP(plpSize, chosenSize, quantity, unitPrice)} />}
      {plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} />}
      {sizeSheet && <SizeSheet size={size} setSize={setSize} close={() => setSizeSheet(false)} add={(quantity,unitPrice) => add({...selected,price:unitPrice},size,quantity)} price={selected.price} />}
      {cartOpen && <Cart cart={cart} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} />}
      {checkoutOpen&&<Checkout cart={cart} total={total} profile={profile} close={()=>setCheckoutOpen(false)} editCart={()=>{setCheckoutOpen(false);setCartOpen(true)}} submit={()=>{setCheckoutOpen(false);setCart([]);notice("Заказ оформлен. Подтверждение отправлено на email")}}/>}
      {toast && <div className="toast">{toast}</div>}
    </main>
  );
}

function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {
  return <header className="header">
    <div className="header-left"><button className="icon-btn hamburger" aria-label="Открыть меню" onClick={onMenu}><i/><i/><i/></button><button className="boutiques" onClick={() => alert("Бутики: Москва · Санкт-Петербург · Казань")}><Icon name="pin"/> Бутики</button></div>
    <button className="logo" onClick={() => go("home")}>КУЛЬТУРА ДОМА</button>
    <div className="header-actions"><button onClick={onSearch} aria-label="Поиск"><Icon name="search"/></button><button onClick={onAccount} aria-label="Профиль"><Icon name="user"/></button><button className="favorite-header" onClick={onFavorites} aria-label={`Избранное: ${favoriteCount}`}><Icon name="heart" filled={favoriteCount>0}/>{favoriteCount>0&&<b>{favoriteCount}</b>}</button><button className="bag" onClick={onCart} aria-label="Корзина"><Icon name="bag"/>{count > 0 && <b>{count}</b>}</button></div>
  </header>;
}

function HomeView({ go, slide, setSlide, onProduct, favorite, favorites, onAdd }: { go:(v:View)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void }) {
  const homeSlides=[
    {category:"СПАЛЬНЯ",image:"/images/blue-bedroom.png",destination:"catalog" as View},
    {category:"РАСПРОДАЖА",image:"/images/russian-bedroom.png",destination:"catalog" as View},
    {category:"КУХНЯ И СТОЛОВАЯ",image:"/images/buyan-editorial.png",destination:"catalog" as View},
    {category:"ДЕКОР ДЛЯ ДОМА",image:"/images/beige-bedroom.png",destination:"catalog" as View},
  ];
  const activeIndex=((slide%homeSlides.length)+homeSlides.length)%homeSlides.length;
  const current=homeSlides[activeIndex];
  const homeCategories=[
    ["Кухня и столовая","/images/moon-plate.png"],
    ["Домашний текстиль","/images/russian-bedroom.png"],
    ["Спальня","/images/classic-bedroom.png"],
    ["Декор для дома","/images/zip-product-bed.png"],
    ["Аутлет","/images/beige-bedroom.png"],
  ] as const;
  const bestsellers=[1,2,7,12].map(id=>products.find(product=>product.id===id)!).filter(Boolean);

  return <>
    <section className="hero home-reference-hero">
      <div className="hero-media"><img src={assetUrl(current.image)} alt={current.category}/></div>
      <div className="hero-shade"/>
      <button className="hero-arrow prev" onClick={() => setSlide((activeIndex + homeSlides.length - 1) % homeSlides.length)} aria-label="Предыдущий баннер"><Icon name="chevron"/></button>
      <button className="hero-arrow next" onClick={() => setSlide((activeIndex + 1) % homeSlides.length)} aria-label="Следующий баннер"><Icon name="chevron"/></button>
      <div className="hero-dots">{homeSlides.map((_,i)=><button key={i} className={i===activeIndex?"active":""} onClick={()=>setSlide(i)} aria-label={`Баннер ${i+1}`}/>)}</div>
      <nav className="hero-nav">{homeSlides.map((item,i)=><button key={item.category} className={i===activeIndex?"active":""} onClick={()=>setSlide(i)}>{item.category}</button>)}</nav>
    </section>

    <section className="home-reference-shelf">
      <div className="home-reference-heading"><p>ДЛЯ ВАШЕГО ДОМА</p><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>
      <div className="category-grid">{homeCategories.map(([name,image],i)=><button className="category-card" key={name} onClick={()=>i===2?go("catalog"):go("catalog")}><img src={assetUrl(image)} alt={name}/><span>{name}</span><b>Смотреть категорию →</b></button>)}</div>
    </section>

    <section className="home-reference-products">
      <div className="home-reference-products-head"><div><p>ВЫБОР РЕДАКЦИИ · СПАЛЬНЯ</p><h2>ХИТЫ ПРОДАЖ</h2></div><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>
      <ProductRail className="home-product-rail" items={bestsellers} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/>
    </section>

    <section className="manifest home-reference-manifest"><p>КУЛЬТУРА ДОМА</p><h2>Предметы, с которыми остаётся вечное</h2><span>Натуральные материалы, ручная работа и образы русской культуры —<br/>для современного дома и личных семейных историй.</span><button onClick={()=>go("collections")}>УЗНАТЬ О БРЕНДЕ →</button></section>
  </>;
}

function CatalogView({ initialCategory, onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {
  const [sort, setSort] = useState("По умолчанию");
  const [category,setCategory]=useState(initialCategory);
  useEffect(()=>setCategory(initialCategory),[initialCategory]);
  const categoryProductIds:Record<string,number[]>={
    "Все товары":products.map(product=>product.id),
    "Посуда и сервировка":[5,9,10,3,1],
    "Постельное бельё":[1,2,4,6,8,12],
    "Пледы и подушки":[3,4,6,7,11],
    "Домашняя одежда":[2,3,6,8],
    "Столовый текстиль":[1,3,5],
  };
  const list = products.filter(product=>(categoryProductIds[category]??[]).includes(product.id)).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);
  return <div className="catalog page"><div className="crumbs">Главная / Каталог / Домашний текстиль</div><div className="title-line"><h1>Домашний текстиль</h1><span>345 товаров</span></div>
    <div className="tabs">{["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Домашняя одежда","Столовый текстиль"].map(x=><button key={x} className={category===x?"active":""} onClick={()=>setCategory(x)}>{x}</button>)}</div>
    <div className="catalog-tools"><select value={sort} onChange={e=>setSort(e.target.value)}><option>По умолчанию</option><option>Сначала дешевле</option><option>Сначала дороже</option></select><button onClick={onFilter}><Icon name="filter"/> Фильтры</button></div>
    <div className="product-grid">{list.map(p=><ProductCard key={`${category}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div>
  </div>;
}

function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void }) {
  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];
  const [colorIndex, setColorIndex] = useState(0);
  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const chosenProduct = { ...product, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };
  const discount=discountOf(product);
  return <article className="product-card"><button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label="Добавить в избранное"><Icon name="heart" filled={liked}/></button><button className="product-image" onClick={()=>onClick(chosenProduct)}><ScrollableProductMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, цвет ${chosen.name}`} position={chosen.position||product.position}/>{product.badge&&<span>{product.badge}</span>}</button><div className="product-copy"><button className="product-link" onClick={()=>onClick(chosenProduct)}><strong>{product.name}</strong><small>{chosen.name.toLowerCase()}, {product.note}</small></button>{variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}<span className={`price ${discount?"sale-price":""}`}>{fmt(product.price)} {product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</span></div>{selectionMode?<button className={`quick selection-check ${pending?"pending":selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={pending?`Выберите размер для ${product.name}`:selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{pending?"?":selected?"✓":""}</button>:<button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="cart-add"/></button>}</article>;
}

function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  const [kind,setKind]=useState("ВСЕ");
  const visible=editorials.filter(item=>kind==="ВСЕ"||(kind==="КАПСУЛЫ"&&item.kind==="КАПСУЛА")||(kind==="КОЛЛЕКЦИИ"&&item.kind==="КОЛЛЕКЦИЯ"));
  return <div className="collections page"><div className="section-head"><p>EDITORIAL</p><h1>Коллекции и капсулы</h1></div><div className="center-tabs">{["ВСЕ","КАПСУЛЫ","КОЛЛЕКЦИИ"].map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div><div className="collection-grid">{visible.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ {item.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ"} <Icon name="arrow"/></span></div></button></article>)}</div></div>;
}

function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {
  const [story,setStory]=useState<"bedroom"|"table"|null>(null);
  const [storyBuying,setStoryBuying]=useState(false);
  const [storyExcludedIds,setStoryExcludedIds]=useState<number[]>([]);
  const [builderOpen,setBuilderOpen]=useState(false);
  const [builderIds,setBuilderIds]=useState<number[]>(editorial.productIds);
  const [builderTitle,setBuilderTitle]=useState("Соберите капсулу");
  const [selectedIds,setSelectedIds]=useState<number[]>(editorial.productIds);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [qty,setQty]=useState<Record<number,number>>({});
  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={4:"/images/products/KD-PD-1024-DARK02.png",6:"/images/products/KD-PD-1026-BLUE01.png",3:"/images/products/KD-PD-1023-BLUE02.png"};
  const fallbacks=["/images/time-hero.png","/images/blue-bedroom.png","/images/night-editorial.png","/images/time-table.png","/images/time-tea-pair.png","/images/moon-plate.png"];

  const prepare=(product:Product):Product=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const regularPrice=product.oldPrice??product.price;
    const preview=previewById[product.id];
    const variants=(product.colorVariants??[]).filter(variant=>variant.name===color);
    const skus=product.skus?.filter(s=>s.color===color).map(s=>({...s,price:regularPrice,...(preview?{image:preview,gallery:Array.from(new Set([preview,...s.gallery]))}:{} )}));
    const sku=skus?.find(s=>s.color===color)??skus?.[0];
    return {
      ...product,
      oldPrice:undefined,
      badge:undefined,
      image:preview??sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      colorVariants:variants.length?variants:product.colorVariants,
      skus,
      selectedColor:sku?.color??color,
      selectedSize:sku?.size??product.selectedSize,
      selectedSkuId:sku?.id,
      price:regularPrice,
    };
  };
  const items=editorial.productIds.map(id=>products.find(p=>p.id===id)).filter(Boolean).map(p=>prepare(p!));
  const itemById=(id:number)=>items.find(p=>p.id===id);
  const groups=[
    {id:"bedroom" as const,title:"Спальня",images:editorial.images.slice(0,3),fallbacks:fallbacks.slice(0,3),productIds:[4,6,3]},
    {id:"table" as const,title:"Сервировка",images:editorial.images.slice(3,6),fallbacks:fallbacks.slice(3,6),productIds:[10,5,3]}
  ];
  const active=groups.find(g=>g.id===story);
  const storyProducts=(active?.productIds.map(itemById).filter(Boolean)??[]) as Product[];
  const storyPendingIds=storyProducts.filter(item=>!storyExcludedIds.includes(item.id)).filter(item=>{const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);return options.length>1&&!sizes[item.id]}).map(item=>item.id);
  const storyReady=storyPendingIds.length===0&&selectedIds.length>0;
  const pendingStoryProducts=storyProducts.filter(item=>storyPendingIds.includes(item.id));
  const builderItems=builderIds.map(itemById).filter(Boolean) as Product[];

  useEffect(()=>{if(!story&&!builderOpen)return;const old=document.body.style.overflow;document.body.style.overflow="hidden";return()=>{document.body.style.overflow=old}},[story,builderOpen]);

  const configured=(item:Product)=>{
    const color=colorById[item.id]??item.selectedColor;
    const options=getProductSizeOptions(item,color);
    const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";
    const sku=findProductSku(item,color,size);
    const quantity=qty[item.id]??1;
    return {...item,price:item.price,image:sku?.image??item.image,gallery:sku?.gallery??item.gallery,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id,quantity};
  };
  const total=selectedIds.reduce((sum,id)=>{const item=itemById(id);if(!item)return sum;const p=configured(item);return sum+p.price*(p.quantity??1)},0);
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(x=>x!==id):[...current,id]);
  const focusStorySize=(id:number)=>setTimeout(()=>document.getElementById(`story-size-${id}`)?.focus(),0);
  const toggleStoryItem=(item:Product,requiresSize:boolean,hasSize:boolean)=>{const id=item.id;const selected=selectedIds.includes(id);const excluded=storyExcludedIds.includes(id);if(selected){setSelectedIds(current=>current.filter(x=>x!==id));setStoryExcludedIds(current=>current.includes(id)?current:[...current,id]);return}if(excluded){setStoryExcludedIds(current=>current.filter(x=>x!==id));if(requiresSize&&!hasSize){focusStorySize(id);return}setSelectedIds(current=>current.includes(id)?current:[...current,id]);return}if(requiresSize&&!hasSize){setStoryExcludedIds(current=>current.includes(id)?current:[...current,id]);return}setSelectedIds(current=>current.includes(id)?current:[...current,id])};
  const openBuilder=(ids:number[],title:string)=>{setBuilderIds(ids);setSelectedIds(ids);setBuilderTitle(title);setBuilderOpen(true)};
  const startStoryPurchase=()=>{if(!active)return;const initialSelected=active.productIds.filter(id=>{const item=itemById(id);if(!item)return false;const color=colorById[item.id]??item.selectedColor;return getProductSizeOptions(item,color).length<=1});setSelectedIds(initialSelected);setStoryExcludedIds([]);setSizes(current=>{const next={...current};active.productIds.forEach(id=>delete next[id]);return next});setStoryBuying(true)};
  const closeStory=()=>{setStoryBuying(false);setStoryExcludedIds([]);setStory(null)};
  const addStory=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length||!storyReady)return;setStoryBuying(false);setStoryExcludedIds([]);setStory(null);chosen.forEach(addToCart)};
  const addAll=()=>{const chosen=selectedIds.map(itemById).filter(Boolean).map(p=>configured(p!));if(!chosen.length)return;setBuilderOpen(false);setStoryBuying(false);setStory(null);chosen.forEach(addToCart)};

  const gallery=(group:(typeof groups)[number],reverse=false)=><section className={`luna-clean-group ${reverse?"reverse":""}`}>
    <h2>{group.title}</h2>
    <div className="luna-clean-gallery">{group.images.map((src,i)=><button key={`${group.id}-${i}`} type="button" onClick={()=>{setStoryBuying(false);setStory(group.id)}}><RemoteImage src={src} fallbackSrc={group.fallbacks[i]} alt={`${group.title}, кадр ${i+1}`}/></button>)}</div>
    <button className="luna-clean-link" type="button" onClick={()=>{setStoryBuying(false);setStory(group.id)}}>СМОТРЕТЬ ИСТОРИЮ</button>
  </section>;

  return <div className="luna-clean-page">
    <section className="luna-clean-head"><p>КАПСУЛА</p><h1>Лунная сказка</h1><span>{editorial.lead}</span></section>
    {gallery(groups[0])}
    {gallery(groups[1],true)}
    <section className="luna-clean-builder-entry"><h2>Соберите капсулу</h2><button type="button" onClick={()=>openBuilder(editorial.productIds,"Соберите капсулу")}>СОБРАТЬ КАПСУЛУ</button></section>

    {active&&<div className="luna-clean-overlay" role="dialog" aria-modal="true">
      <button className="luna-clean-backdrop" onClick={closeStory} aria-label="Закрыть"/>
      <section className="luna-clean-story">
        <header><strong>{active.title}</strong><button type="button" onClick={closeStory} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-clean-story-images">{active.images.map((src,i)=><RemoteImage key={`${active.id}-story-${i}`} src={src} fallbackSrc={active.fallbacks[i]} alt={`${active.title}, кадр ${i+1}`}/>)}</div>
        <div className={`luna-clean-products ${storyBuying?"is-buying":""}`}>{storyProducts.map(item=>{const selected=selectedIds.includes(item.id);const excluded=storyExcludedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const requiresSize=options.length>1;const size=sizes[item.id]??(requiresSize?"":(options[0]?.[0]??item.selectedSize??""));const pending=storyBuying&&requiresSize&&!size&&!excluded;const quantity=qty[item.id]??1;return <div className={`luna-story-card-shell ${storyBuying?(pending?"pending-size":selected?"selected":"excluded"):""}`} key={`${active.id}-${item.id}`}>
          {pending&&<span className="luna-story-size-badge">Нужен размер</span>}
          <ProductCard product={item} onClick={quickAdd} onQuick={quickAdd} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={storyBuying} selected={selected} pending={pending} onSelect={()=>toggleStoryItem(item,requiresSize,Boolean(size))}/>
          {storyBuying&&<><div className={`luna-story-card-config ${pending?"has-error":""}`}>{requiresSize?<label><span>Размер</span><select id={`story-size-${item.id}`} value={size} aria-invalid={pending} onChange={e=>{const value=e.target.value;setSizes(current=>({...current,[item.id]:value}));setStoryExcludedIds(current=>current.filter(x=>x!==item.id));setSelectedIds(current=>current.includes(item.id)?current:[...current,item.id])}} aria-label={`Выберите размер ${item.name}`}><option value="" disabled>Выберите размер</option>{options.map(([o])=><option key={o} value={o}>{o}</option>)}</select></label>:<span className="luna-story-fixed-size">{size}</span>}{selected&&<div className="luna-story-card-qty"><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))} aria-label="Увеличить количество">+</button></div>}</div>{pending&&<div className="luna-story-size-error">⚠ Выберите размер, чтобы добавить в набор</div>}</>}
        </div>})}</div>
        {!storyBuying?<div className="luna-clean-story-buy"><button type="button" onClick={startStoryPurchase}>КУПИТЬ ИСТОРИЮ</button></div>:<div className="luna-clean-story-buy luna-story-buy-active"><button className="luna-story-buy-cancel" type="button" onClick={()=>{setStoryBuying(false);setStoryExcludedIds([])}}>ОТМЕНА</button><div className="luna-story-buy-summary"><div className="luna-story-buy-total"><span><b>{selectedIds.length} из {storyProducts.length}</b> товаров готовы</span><strong>{fmt(total)}</strong></div>{storyPendingIds.length>0&&<div className="luna-story-buy-note">⚠ {pendingStoryProducts[0]?.name}: не выбран размер — не учтён в сумме</div>}{storyPendingIds.length>0&&<div className="luna-story-buy-hint">Выберите размер в карточке выше</div>}</div><button className="luna-story-buy-add" type="button" aria-disabled={!storyReady} onClick={()=>{if(!storyReady){const id=storyPendingIds[0];if(id)focusStorySize(id);return}addStory()}}>{storyPendingIds.length>0?"ВЫБРАТЬ РАЗМЕР, ЧТОБЫ ПРОДОЛЖИТЬ":"ДОБАВИТЬ В КОРЗИНУ"}</button></div>}
      </section>
    </div>}

    {builderOpen&&<div className="luna-clean-overlay" role="dialog" aria-modal="true">
      <button className="luna-clean-backdrop" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"/>
      <section className="luna-clean-builder">
        <header><strong>{builderTitle}</strong><button type="button" onClick={()=>setBuilderOpen(false)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <div className="luna-clean-builder-tools"><span>{selectedIds.length} из {builderItems.length}</span><button type="button" onClick={()=>setSelectedIds(selectedIds.length===builderItems.length?[]:builderItems.map(i=>i.id))}>{selectedIds.length===builderItems.length?"СНЯТЬ ВСЕ":"ВЫБРАТЬ ВСЕ"}</button></div>
        <div className="luna-clean-builder-list">{builderItems.map(item=>{const selected=selectedIds.includes(item.id);const color=colorById[item.id]??item.selectedColor;const options=getProductSizeOptions(item,color);const size=sizes[item.id]??options[0]?.[0]??item.selectedSize??"";const sku=findProductSku(item,color,size);const price=sku?.price??item.price;const quantity=qty[item.id]??1;return <article className={selected?"selected":""} key={item.id}>
          <button className="luna-clean-check" type="button" onClick={()=>toggle(item.id)} aria-pressed={selected}>{selected?"✓":""}</button>
          <RemoteImage src={previewById[item.id]??item.image} alt={item.name}/>
          <div><h3>{item.name}</h3>{options.length>1?<select value={size} onChange={e=>setSizes(current=>({...current,[item.id]:e.target.value}))}>{options.map(([o])=><option key={o}>{o}</option>)}</select>:<small>{size}</small>}<div className="luna-clean-row"><strong>{fmt(price*quantity)}</strong><span><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:Math.max(1,quantity-1)}))}>−</button><b>{quantity}</b><button type="button" onClick={()=>setQty(current=>({...current,[item.id]:quantity+1}))}>+</button></span></div></div>
        </article>})}</div>
        <footer><div><span>{selectedIds.length} позиций</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedIds.length} onClick={addAll}>{builderIds.length===items.length?"ДОБАВИТЬ КАПСУЛУ В КОРЗИНУ":"ДОБАВИТЬ ИСТОРИЮ В КОРЗИНУ"}</button></footer>
      </section>
    </div>}
  </div>;
}

function EditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void }) {
  if(editorial.id==="luna")return <LunaEditorialView editorial={editorial} selectProduct={selectProduct} favorite={favorite} favorites={favorites} quickAdd={quickAdd} addToCart={addToCart}/>;
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const variant=editorial.id==="time"?"cinematic":editorial.id==="buyan"?"offset":editorial.id==="poetry"?"magazine":"gallery";
  const chapter=editorial.id==="time"?"NIGHT STUDY":editorial.id==="buyan"?"SUMMER TABLE":editorial.id==="poetry"?"POETRY OF HOME":"FOLKLORE REFRAMED";
  const index=editorial.id==="time"?"01":editorial.id==="buyan"?"02":editorial.id==="poetry"?"03":"04";
  const productImage=items[0]?.image||editorial.images[0];

  return <div className={`editorial-page zara-editorial editorial-variant-${variant}`}>
    <section className="zh-editorial-cover">
      <img src={assetUrl(editorial.images[0])} alt={editorial.name}/>
      <div className="zh-editorial-cover-copy"><span>{index} / EDITORIAL</span><p>{editorial.kind}</p><h1>{editorial.name}</h1></div>
    </section>

    <section className="zh-editorial-lead">
      <p>{chapter}</p>
      <h2>{editorial.lead}</h2>
      <span>{editorial.description}</span>
    </section>

    <section className="zh-editorial-spread">
      <figure className="zh-editorial-spread-main"><img src={assetUrl(editorial.images[1])} alt={`История ${editorial.name}`}/><figcaption>01 / STORY</figcaption></figure>
      <div className="zh-editorial-spread-copy"><span>{index}</span><p>THE STORY</p><h3>{editorial.detail}</h3></div>
    </section>

    {variant==="magazine"&&<section className="zh-editorial-type-page"><span>WORDS / OBJECTS / HOME</span><h2>Красота начинается с паузы между вещами.</h2><p>Редакционная композиция строится как журнальный разворот: крупный текст, свободное поле и один выразительный предмет.</p></section>}

    {variant==="offset"&&<section className="zh-editorial-side-note"><p>02 / TABLE STORY</p><h3>Сервировка не как набор предметов, а как готовая сцена для долгого разговора.</h3></section>}

    <section className="zh-editorial-mosaic">
      <figure className="zh-editorial-mosaic-a"><img src={assetUrl(editorial.images[2])} alt="Деталь коллекции"/><figcaption>DETAIL / 02</figcaption></figure>
      <figure className="zh-editorial-mosaic-b"><img src={assetUrl(editorial.images[3])} alt="Образ коллекции"/><figcaption>ATMOSPHERE / 03</figcaption></figure>
      <div className="zh-editorial-mosaic-copy"><span>03</span><p>OBJECTS IN CONTEXT</p><h3>Вещи раскрываются через масштаб, фактуру и соседство с другими предметами.</h3></div>
    </section>

    <figure className="zh-editorial-full-frame">
      <RemoteImage src={productImage} alt={`Предмет из ${editorial.name}`}/>
      <figcaption><span>04</span><p>SHOP THE STORY</p></figcaption>
    </figure>

    {variant==="gallery"&&<section className="zh-editorial-quote"><p>FOLKLORE / NOW</p><h2>Традиция может звучать современно, когда её не копируют буквально.</h2></section>}
    {variant==="cinematic"&&<section className="zh-editorial-quote"><p>NIGHT / LIGHT / TEXTURE</p><h2>Спокойный интерьер строится не из декора, а из света, материалов и ритма.</h2></section>}

    <section className="editorial-products zh-editorial-products">
      <div className="editorial-products-head"><div><p>SHOP THE STORY</p><h2>Предметы {editorial.kind==="КАПСУЛА"?"капсулы":"коллекции"}</h2></div></div>
      <div className="product-grid">{items.map(item=><ProductCard product={item} key={`${editorial.id}-${item.id}`} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
    </section>
  </div>;
}

function LookbookViewer({editorial,items,close,selectProduct}:{editorial:Editorial;items:Product[];close:()=>void;selectProduct?:(product:Product)=>void}){
  const [chapter,setChapter]=useState(0);
  const chapterLabels=["COVER","STORY","DETAILS","NOTE","SHOP"];
  useEffect(()=>{
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")close()};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  },[close]);
  const goChapter=(index:number)=>{
    setChapter(index);
    document.getElementById(`lookbook-${editorial.id}-${index}`)?.scrollIntoView({behavior:"smooth",block:"nearest",inline:"start"});
  };
  return <div className="lookbook-overlay" role="dialog" aria-modal="true" aria-label={`Lookbook ${editorial.name}`}>
    <button className="lookbook-backdrop" onClick={close} aria-label="Закрыть lookbook"/>
    <section className="lookbook-shell">
      <header className="lookbook-header"><div><span>{editorial.kind}</span><b>{editorial.name}</b></div><nav>{chapterLabels.map((label,index)=><button key={label} className={chapter===index?"active":""} onClick={()=>goChapter(index)}>{String(index+1).padStart(2,"0")} {label}</button>)}</nav><button className="lookbook-close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="lookbook-track">
        <article id={`lookbook-${editorial.id}-0`} className="lookbook-page lookbook-cover-page">
          <img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><p>01 / COVER</p><h2>{editorial.name}</h2><span>{editorial.lead}</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-1`} className="lookbook-page lookbook-story-page">
          <figure><img src={assetUrl(editorial.images[1])} alt="История коллекции"/><figcaption>PHOTOGRAPHY / STORY</figcaption></figure><div><p>02 / THE STORY</p><h2>{editorial.description}</h2><span>{editorial.detail}</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-2`} className="lookbook-page lookbook-details-page">
          <figure><img src={assetUrl(editorial.images[2])} alt="Детали коллекции"/></figure><figure><img src={assetUrl(editorial.images[3])} alt="Атмосфера коллекции"/></figure><div><p>03 / DETAILS</p><h2>Материал, свет и масштаб</h2><span>Вместо длинного текста — два визуальных кадра и короткая редакционная заметка.</span></div>
        </article>
        <article id={`lookbook-${editorial.id}-3`} className="lookbook-page lookbook-note-page">
          <div><p>04 / EDITOR'S NOTE</p><h2>{editorial.id==="time"?"Тишина — тоже часть интерьера.":editorial.id==="buyan"?"Сервировка начинается с атмосферы.":editorial.id==="poetry"?"Дом хранит смысл в мелочах.":"Традиция становится современной, когда остаётся живой."}</h2><span>{editorial.lead}</span></div><img src={assetUrl(editorial.images[0])} alt="Редакционный кадр"/>
        </article>
        <article id={`lookbook-${editorial.id}-4`} className="lookbook-page lookbook-shop-page">
          <div className="lookbook-shop-head"><p>05 / SHOP THE STORY</p><h2>Предметы из истории</h2></div>
          <div className="lookbook-shop-grid">{items.map(item=><button key={item.id} onClick={()=>{close();selectProduct?.(item)}}><RemoteImage src={item.image} alt={item.name}/><span>{item.name}<b>{fmt(item.price)}</b></span></button>)}</div>
        </article>
      </div>
      <div className="lookbook-mobile-progress">{chapterLabels.map((_,index)=><button key={index} className={chapter===index?"active":""} onClick={()=>goChapter(index)} aria-label={`Глава ${index+1}`}/>)}</div>
    </section>
  </div>;
}

function QuantityControl({ quantity, setQuantity, label = "Количество" }: { quantity:number; setQuantity:(quantity:number)=>void; label?:string }) {
  return <div className="quantity-control" aria-label={label}><button onClick={(event)=>{event.stopPropagation();setQuantity(Math.max(1,quantity-1))}} aria-label="Уменьшить количество"><Icon name="minus"/></button><span>{quantity}</span><button onClick={(event)=>{event.stopPropagation();setQuantity(quantity+1)}} aria-label="Увеличить количество"><Icon name="plus"/></button></div>;
}

function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableLast=true}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableLast?:boolean}){
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=unavailableLast&&index===sizes.length-1;return <div key={name} className={`size-row ${selectedSize===name&&!unavailable?"active":""} ${unavailable?"unavailable":""}`}><button onClick={()=>{if(!unavailable){setSelectedSize(name);setQuantity(1)}}}><span>{name}</span>{selectedSize!==name&&!unavailable&&<b>{fmt(price)}</b>}</button>{unavailable?<div className="stock-actions"><button onClick={()=>document.querySelector(".post-rich-recommendations")?.scrollIntoView({behavior:"smooth"})}>СМОТРЕТЬ ПОХОЖИЕ</button><button onClick={()=>notify(name)} aria-label={`Сообщить о поступлении размера ${name}`}><Icon name="mail"/></button></div>:selectedSize===name?<QuantityControl quantity={quantity} setQuantity={setQuantity}/>:null}</div>})}</div>;
}

function ProductView({ product, favorite, liked, chooseSize, add, selectProduct, recentlyViewed }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; selectProduct:(p:Product)=>void; recentlyViewed:number[] }) {
  const [open,setOpen]=useState("ХАРАКТЕРИСТИКИ");
  const [storesOpen,setStoresOpen]=useState(false);
  const [colorIndex,setColorIndex]=useState(0);
  const [activeImage,setActiveImage]=useState(0);
  const [selectedSize,setSelectedSize]=useState("");
  const [quantity,setQuantity]=useState(1);
  const [sizePrompt,setSizePrompt]=useState(false);
  const variants=product.colorVariants??[{name:"Молочный",hex:"#eee",image:product.image}];
  useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);const nextIndex=initial>=0?initial:0;setColorIndex(nextIndex);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)},[product.id,product.selectedColor]);
  const color=variants[colorIndex];
  const sizes=getProductSizeOptions(product,color.name);
  const sku=selectedSize?findProductSku(product,color.name,selectedSize):undefined;
  const mediaSku=findProductSku(product,color.name);
  const gallery=mediaSku?[mediaSku.image,...mediaSku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??sizes[0]?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize,selectedSkuId:sku?.id,quantity};
  const specs=sku??mediaSku??product.skus?.[0];
  const needsSize=Boolean(sizes.length&&!selectedSize);
  const handlePurchase=()=>{if(needsSize){setSizePrompt(true);return}add(selectedProduct)};
  return <div className={`product-page page ${product.hasRichContent?"has-rich":"standard-pdp"}`}><div className="crumbs">Главная / Домашний текстиль / {product.name}</div><div className={`pdp-grid ${product.hasRichContent?"without-thumbs":""}`}>{!product.hasRichContent&&<div className="thumbs">{gallery.map((src,n)=><button key={src} className={n===activeImage?"active":""} onClick={()=>{setActiveImage(n);if(typeof window!=="undefined"&&window.matchMedia("(min-width: 901px)").matches){document.querySelector(`[data-pdp-image-index="${n}"]`)?.scrollIntoView({behavior:"smooth",block:"start"})}}} aria-label={`Фото товара ${n+1}`}><RemoteImage src={src} alt=""/></button>)}</div>}<div className="pdp-main"><ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/></div><div className="pdp-info">{product.badge&&<small className="badge">{product.badge}</small>}<div className="pdp-title"><h1>{product.name}</h1><div><button onClick={()=>favorite(product.id)} aria-label="Добавить в избранное"><Icon name="heart" filled={liked}/></button><button onClick={()=>navigator.clipboard?.writeText(location.href)} aria-label="Поделиться"><Icon name="share"/></button></div></div><div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)}</strong>{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: {product.article??`KD-PD-${1020+product.id}`}</small><label className="pdp-color-label">Цвет: {color.name}</label>{variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}<p className="pdp-description">Предмет создан в традиции русского гостеприимства: благородная палитра, точная отделка и материалы, которые красиво живут в доме годами.</p><label className="pdp-size-head"><span>РАЗМЕР</span><button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button></label><ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/><button className={`primary purchase-cta total-cta ${needsSize?"needs-size":"ready-to-add"} ${sizePrompt&&needsSize?"choose-size-state":""}`} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{needsSize?(sizePrompt?"ВЫБЕРИТЕ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"):"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>setStoresOpen(true)} aria-label="Показать наличие в бутиках"><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button><div className="pdp-accordions">{[
  {title:"ХАРАКТЕРИСТИКИ",content:specs?<><p>{specs.collection?`${specs.material}. ${specs.size}. Коллекция «${specs.collection}».`:`${specs.material}. ${specs.size}.`}</p><dl><div><dt>Материал</dt><dd>{specs.material}</dd></div><div><dt>Состав</dt><dd>{specs.composition}</dd></div>{specs.height&&<div><dt>Высота</dt><dd>{specs.height}</dd></div>}{specs.width&&<div><dt>Ширина</dt><dd>{specs.width}</dd></div>}{specs.diameter&&<div><dt>Диаметр</dt><dd>{specs.diameter}</dd></div>}{specs.packageInfo&&<div><dt>Комплектация</dt><dd>{specs.packageInfo}</dd></div>}{specs.details&&<div><dt>Детали</dt><dd>{specs.details}</dd></div>}{specs.collection&&<div><dt>Коллекция</dt><dd>{specs.collection}</dd></div>}</dl></>:<p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p>},
  {title:"ДОСТАВКА И ВОЗВРАТ",content:<><p>Бесплатная доставка при заказе от 15 000 ₽. Доступны курьерская доставка и самовывоз из бутика.</p><small>Срок и доступные способы рассчитываются при оформлении заказа.</small></>}
].map(section=><section className={`pdp-accordion-item ${open===section.title?"open":""}`} key={section.title}><button className="pdp-accordion-trigger" onClick={()=>setOpen(open===section.title?"":section.title)} aria-expanded={open===section.title}><span>{section.title}</span><Icon name="chevron"/></button>{open===section.title&&<div className="pdp-accordion-panel">{section.content}</div>}</section>)}</div></div></div>{product.hasRichContent&&<RichContent product={product} selectProduct={selectProduct}/>}<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>{storesOpen&&<BoutiqueMap close={()=>setStoresOpen(false)}/>}</div>;
}

function BoutiqueMap({close}:{close:()=>void}){
  const boutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124}
  ];
  const [selected,setSelected]=useState(0);
  const boutique=boutiques[selected];
  const delta=.035;
  const mapSrc=`https://www.openstreetmap.org/export/embed.html?bbox=${boutique.lon-delta}%2C${boutique.lat-delta}%2C${boutique.lon+delta}%2C${boutique.lat+delta}&layer=mapnik&marker=${boutique.lat}%2C${boutique.lon}`;
  return <div className="boutique-map-overlay" role="dialog" aria-modal="true" aria-label="Наличие в магазинах"><button className="boutique-map-backdrop" onClick={close} aria-label="Закрыть карту"/><section className="boutique-map-modal"><header><div><small>НАЛИЧИЕ В МАГАЗИНАХ</small><h2>Бутики Культура дома</h2></div><button className="boutique-map-close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header><div className="boutique-map-body"><aside>{boutiques.map((item,index)=><button key={item.city} className={index===selected?"active":""} onClick={()=>setSelected(index)}><span><Icon name="pin"/><b>{item.city}</b></span><strong>{item.address}</strong><small>{item.hours}</small><i>{index===selected?"На карте":"Показать на карте"}</i></button>)}</aside><div className="boutique-map-canvas"><iframe key={`${boutique.city}-${selected}`} src={mapSrc} title={`Карта бутика — ${boutique.city}`} loading="lazy"/><div className="boutique-map-caption"><div><b>{boutique.city}</b><span>{boutique.address}</span></div><small>{boutique.hours}</small></div></div></div></section></div>;
}

function RichContent({product,selectProduct}:{product:Product;selectProduct:(product:Product)=>void}){
  const [lookbookOpen,setLookbookOpen]=useState(false);
  const related=product.id===4?editorials.find(item=>item.id==="time"):editorials.find(item=>item.productIds.includes(product.id)&&item.kind==="КОЛЛЕКЦИЯ");
  if(!related)return null;
  const items=related.productIds.map(id=>products.find(item=>item.id===id)!).filter(Boolean);
  return <section className="pdp-story-entry">
    <button className="pdp-story-entry-media" onClick={()=>setLookbookOpen(true)}><img src={assetUrl(related.images[1])} alt={`История ${related.name}`}/><span>EDITORIAL / LOOKBOOK</span></button>
    <div className="pdp-story-entry-copy"><p>{related.kind}</p><h2>История «{related.name}»</h2><span>{related.description}</span><button onClick={()=>setLookbookOpen(true)}>СМОТРЕТЬ LOOKBOOK →</button></div>
    {lookbookOpen&&<LookbookViewer editorial={related} items={items} close={()=>setLookbookOpen(false)} selectProduct={selectProduct}/>} 
  </section>;
}

function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  const categoryGroups=[
    [1,2,4,8,12],
    [3,6,7,11],
    [5,9,10]
  ];
  const categoryIds=categoryGroups.find(group=>group.includes(product.id))??products.map(item=>item.id);
  const categoryProducts=products.filter(item=>item.id!==product.id&&categoryIds.includes(item.id)).slice(0,4);
  const viewedProducts=recentlyViewed
    .filter(id=>id!==product.id)
    .map(id=>products.find(item=>item.id===id))
    .filter((item): item is Product=>Boolean(item))
    .slice(0,4);
  return <>
    <section className="post-rich-recommendations category-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Товары из этой категории</h2></div><ProductRail className="recommendation-product-rail" items={categoryProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>
    {viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><ProductRail className="recommendation-product-rail" items={viewedProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
  </>;
}

function Menu({ current, setCurrent, close, go, openCatalog }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void }) {
  const level1=["РАСПРОДАЖА","Спальня","Кухня и столовая","Декор","Ванная","Одежда для дома","Идеи подарков","Аутлет"];
  const subs:Record<string,string[]>={
    "РАСПРОДАЖА":["Смотреть все","Летнее предложение","До −35% на текстиль","До −30% на сервировку"],
    "Спальня":["Смотреть все","Комплекты постельного белья","Одеяла и подушки","Пледы и покрывала","Наволочки","Пододеяльники","Простыни","Наматрасники"],
    "Кухня и столовая":["Смотреть все","Блюда и тарелки","Салатники","Стаканы и бокалы","Графины","Чашки","Столовые приборы","Вазы и этажерки","Прочие предметы сервировки"],
    "Декор":["Смотреть все","Вазы","Свечи и ароматы","Декоративные подушки","Предметы интерьера"],
    "Ванная":["Смотреть все","Полотенца","Халаты","Коврики","Аксессуары для ванной"],
    "Одежда для дома":["Смотреть все","Сорочки","Пижамы","Халаты","Домашние костюмы"],
    "Идеи подарков":["Смотреть все","Для неё","Для него","Новоселье","Подарочный сертификат"],
    "Аутлет":["Смотреть все","Последний размер","Архив коллекций","До −50%"],
  };
  const list=subs[current]||[];
  const catalogMap:Record<string,string>={"Спальня":"Постельное бельё","Кухня и столовая":"Посуда и сервировка","Декор":"Пледы и подушки","Ванная":"Все товары","Одежда для дома":"Домашняя одежда","РАСПРОДАЖА":"Все товары","Идеи подарков":"Все товары","Аутлет":"Все товары"};
  const subcategoryMap:Record<string,string>={"Комплекты постельного белья":"Постельное бельё","Пододеяльники":"Постельное бельё","Простыни":"Постельное бельё","Наматрасники":"Постельное бельё","Одеяла и подушки":"Пледы и подушки","Пледы и покрывала":"Пледы и подушки","Наволочки":"Пледы и подушки","Блюда и тарелки":"Посуда и сервировка","Салатники":"Посуда и сервировка","Стаканы и бокалы":"Посуда и сервировка","Графины":"Посуда и сервировка","Чашки":"Посуда и сервировка","Столовые приборы":"Посуда и сервировка","Пижамы":"Домашняя одежда","Халаты":"Домашняя одежда","Домашние костюмы":"Домашняя одежда"};
  return <div className="overlay navigation-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><aside className="menu-panel zara-menu"><div className="menu-top"><button onClick={close} aria-label="Закрыть меню"><Icon name="close"/></button><span><Icon name="pin"/> Бутики</span><b>КУЛЬТУРА ДОМА</b></div><div className="menu-body">{!current?<div className="menu-first level-one"><button className="menu-feature" onClick={()=>openCatalog("Все товары")}>НОВИНКИ</button><button className="menu-feature" onClick={()=>go("collections")}>КАПСУЛЫ И КОЛЛЕКЦИИ</button>{level1.map(x=><button key={x} className={x==="РАСПРОДАЖА"?"sale":""} onClick={()=>setCurrent(x)}>{x}<Icon name="chevron"/></button>)}<hr/><button onClick={()=>go("collections")}>EDITORIAL</button><button onClick={()=>alert("Электронный сертификат доступен от 3 000 ₽")}>ПОДАРОЧНЫЙ СЕРТИФИКАТ</button></div>:<div className="menu-second level-two" key={current}><button className="menu-back" onClick={()=>setCurrent("")}><Icon name="chevron"/> {current}</button>{list.map((x,i)=><button key={x} className={i===0?"view-all":""} onClick={()=>openCatalog(i===0?(catalogMap[current]??"Все товары"):(subcategoryMap[x]??catalogMap[current]??"Все товары"))}>{x}{i===0&&<Icon name="arrow"/>}</button>)}<hr/><button onClick={()=>openCatalog(catalogMap[current]??"Все товары")}>ЛИДЕРЫ ПРОДАЖ</button></div>}</div></aside></div>;
}

function Search({ close, choose }: { close:()=>void; choose:(p:Product)=>void }) { const [q,setQ]=useState(""); const result=products.filter(p=>p.name.toLowerCase().includes(q.toLowerCase())); return <div className="overlay"><button className="overlay-bg" onClick={close}/><div className="search-panel"><div><Icon name="search"/><input autoFocus placeholder="Поиск по каталогу" value={q} onChange={e=>setQ(e.target.value)}/><button onClick={close} aria-label="Закрыть поиск"><Icon name="close"/></button></div><p>{q?`Найдено: ${result.length}`:"Популярные запросы: постельное бельё, посуда, подарки"}</p>{q&&<div className="search-results">{result.map(p=><button key={p.id} onClick={()=>choose(p)}><ScrollableProductMedia product={p} alt={p.name} className="search-item-media"/><span>{p.name}<b>{fmt(p.price)}</b></span></button>)}</div>}</div></div> }

function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  const [mode,setMode]=useState<"login"|"register"|"profile">(profile?"profile":"login");
  const [draft,setDraft]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const finish=(message:string,profileDraft=draft)=>{if(!profileDraft.email||!profileDraft.name){notice("Заполните имя и email");return}save(profileDraft);setDraft(profileDraft);setMode("profile");notice(message)};
  return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel account"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ЛИЧНЫЙ КАБИНЕТ</p>{mode==="profile"?<><h2>{draft.name}, добро пожаловать</h2><span>Ваши данные сохраняются на этом устройстве и подставляются при оформлении заказа.</span><AccountFields draft={draft} setDraft={setDraft}/><button className="primary" onClick={()=>finish("Данные профиля сохранены")}>СОХРАНИТЬ ДАННЫЕ</button><button className="link" onClick={()=>{logout();setDraft({name:"",surname:"",email:"",phone:"",city:"Москва",address:""});setMode("login");notice("Вы вышли из аккаунта")}}>ВЫЙТИ</button></>:mode==="login"?<><h2>С возвращением</h2><span>Войдите, чтобы сохранять избранное и быстрее оформлять заказы.</span><input value={draft.email} onChange={event=>setDraft({...draft,email:event.target.value})} placeholder="Email"/><input placeholder="Пароль" type="password"/><button className="primary" onClick={()=>finish("Вход выполнен",{...draft,name:draft.name||"Анна"})}>ВОЙТИ</button><button className="link" onClick={()=>setMode("register")}>СОЗДАТЬ АККАУНТ</button></>:<><h2>Создать аккаунт</h2><span>Сохраните контакты, адрес и любимые предметы в одном месте.</span><AccountFields draft={draft} setDraft={setDraft}/><input placeholder="Придумайте пароль" type="password"/><button className="primary" onClick={()=>finish("Аккаунт создан")}>ЗАРЕГИСТРИРОВАТЬСЯ</button><button className="link" onClick={()=>setMode("login")}>У МЕНЯ УЖЕ ЕСТЬ АККАУНТ</button></>}</aside></div>
}

function AccountFields({draft,setDraft}:{draft:Profile;setDraft:(profile:Profile)=>void}){
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setDraft({...draft,[key]:event.target.value});
  return <div className="account-fields"><input value={draft.name} onChange={field("name")} placeholder="Имя"/><input value={draft.surname} onChange={field("surname")} placeholder="Фамилия"/><input type="email" value={draft.email} onChange={field("email")} placeholder="Email"/><input type="tel" value={draft.phone} onChange={field("phone")} placeholder="Телефон"/><input value={draft.city} onChange={field("city")} placeholder="Город"/><input value={draft.address} onChange={field("address")} placeholder="Адрес"/></div>;
}

function Favorites({ids,close,remove,choose,quickAdd}:{ids:number[];close:()=>void;remove:(id:number)=>void;choose:(product:Product)=>void;quickAdd:(product:Product)=>void}){
  const items=products.filter(product=>ids.includes(product.id));
  return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel favorites-drawer"><button className="close" onClick={close} aria-label="Закрыть избранное"><Icon name="close"/></button><p>ИЗБРАННОЕ · {items.length}</p>{items.length===0?<div className="empty"><Icon name="heart"/><h2>Сохраните то, что близко</h2><span>Нажимайте на сердце в карточке, чтобы вернуться к предмету позже.</span><button className="primary" onClick={close}>ПРОДОЛЖИТЬ ПОКУПКИ</button></div>:<div className="favorite-list">{items.map(product=><article key={product.id}><button className="favorite-image" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="favorite-item-media"/></button><div><button className="favorite-title" onClick={()=>choose(product)}>{product.name}</button><span>{product.note}</span><b>{fmt(product.price)}</b><button className="secondary" onClick={()=>quickAdd(product)}>ДОБАВИТЬ</button></div><button className="favorite-remove" onClick={()=>remove(product.id)} aria-label={`Удалить ${product.name} из избранного`}><Icon name="close"/></button></article>)}</div>}</aside></div>;
}

function Filters({ close, apply }: { close:()=>void; apply:()=>void }) { return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel filters"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ФИЛЬТРЫ</p>{["Категория","Материал","Цвет","Размер","Цена"].map((x,i)=><details key={x} open={i===0}><summary>{x}<Icon name="plus"/></summary><label><input type="checkbox"/> Постельное бельё</label><label><input type="checkbox"/> Домашний текстиль</label><label><input type="checkbox"/> Посуда и сервировка</label></details>)}<button className="primary" onClick={apply}>ПОКАЗАТЬ 24 ТОВАРА</button><button className="link" onClick={()=>location.reload()}>СБРОСИТЬ</button></aside></div> }

function PLPSizeFlow({ product, close, add }: { product:Product; close:()=>void; add:(size:string,quantity:number,unitPrice:number)=>void }) {
  const selectedColor=product.selectedColor??product.colorVariants?.[0]?.name;
  const [chosenSize,setChosenSize]=useState(findProductSku(product,selectedColor)?.size??"Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  const sizes=getProductSizeOptions(product,selectedColor);
  const selectedSku=findProductSku(product,selectedColor,chosenSize);
  const unitPrice=selectedSku?.price??sizes.find(([item])=>item===chosenSize)?.[1]??product.price;
  const discount=discountOf(product);
  return <div className="overlay plp-flow"><button className="overlay-bg" onClick={close} aria-label="Закрыть выбор размера"/><section className="plp-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}><div className="flow-handle"/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="plp-modal-media"><ScrollableProductMedia product={product} alt={product.name}/></div><div className="plp-modal-info"><small>{product.badge||"КУЛЬТУРА ДОМА"}</small><h2>{product.name}</h2><p className="modal-note">{product.note}</p><div className="modal-price"><b>{sizes.length>1?`от ${fmt(sizes[0]?.[1]??product.price)}`:fmt(sizes[0]?.[1]??product.price)}</b>{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</div><p className="quick-color">Цвет: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p><p className="quick-description">Предмет создан в русской декоративной традиции: ясная форма, благородный цвет и точная отделка.</p><button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary total-cta" onClick={()=>add(chosenSize,quantity,unitPrice)}><span>ДОБАВИТЬ В КОРЗИНУ</span><b>{fmt(unitPrice*quantity)}</b></button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>
}

function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize)??product.skus?.[0];
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Размер</dt><dd>{sku?.size??product.note}</dd></div>{sku&&<><div><dt>Высота</dt><dd>{sku.height}</dd></div><div><dt>Ширина</dt><dd>{sku.width}</dd></div></>}</dl></section><section><h2>МАТЕРИАЛ И СОСТАВ</h2><h3>{sku?.material??"Материал"}</h3><p>{sku?.composition??"Информация указана в характеристиках товара."}</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}

function PLPAdded({product,close,openCart}:{product:CartItem;close:()=>void;openCart:()=>void}){
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><ScrollableProductMedia product={product} alt={product.name} className="added-product-media"/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div><aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}

function SizeSheet({ size, setSize, close, add, price }: { size:string; setSize:(s:string)=>void; close:()=>void; add:(quantity:number,unitPrice:number)=>void; price:number }) {
  const [quantity,setQuantity]=useState(1);
  const sizes=[["Евро 200×220",price],["Семейный 150×200",price+2000],["Кинг Сайз 220×240",price+2000]] as const;
  const unitPrice=sizes.find(([item])=>item===size)?.[1]??price;
  return <div className="overlay mobile-overlay"><button className="overlay-bg" onClick={close}/><aside className="size-sheet"><i/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={size} setSelectedSize={setSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary total-cta" onClick={()=>add(quantity,unitPrice)}><span>ДОБАВИТЬ В КОРЗИНУ</span><b>{fmt(unitPrice*quantity)}</b></button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></aside></div>
}

function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  return <div className="overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть корзину"/><aside className="side-panel cart"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>{cart.length?`КОРЗИНА · ${cart.reduce((sum,item)=>sum+item.quantity,0)}`:"КОРЗИНА"}</p>{cart.length===0?<>{recentItems.length?<section className="recent-cart"><div><p>НЕДАВНО ПРОСМОТРЕННЫЕ</p><span>Предметы, к которым вы возвращались</span></div><div>{recentItems.map(product=><button key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><strong>{product.name}</strong><small>{product.note}</small><b>{fmt(product.price)}</b></button>)}</div><button className="secondary" onClick={go}>ПРОДОЛЖИТЬ ПОКУПКИ</button></section>:<div className="empty"><h2>Здесь пока пусто</h2><span>Добавьте предметы, которые сделают дом вашим.</span><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></div>}</>:<><div className="cart-items">{cart.map((p,i)=><article key={`${p.id}-${i}`}><ScrollableProductMedia product={p} alt={`${p.name}, ${p.selectedColor}`} className="cart-item-media"/><div className="cart-item-copy"><strong>{p.name}</strong><span>Цвет: {p.selectedColor}</span><label>Размер<select value={p.selectedSize} onChange={event=>{const nextSize=event.target.value;const nextSku=findProductSku(p,p.selectedColor,nextSize);update(i,{selectedSize:nextSize,selectedSkuId:nextSku?.id,price:nextSku?.price??p.price,image:nextSku?.image??p.image,gallery:nextSku?.gallery??p.gallery})}}>{getProductSizeOptions(p,p.selectedColor).map(([option])=><option key={option}>{option}</option>)}</select></label><div className="cart-item-bottom"><QuantityControl quantity={p.quantity} setQuantity={quantity=>update(i,{quantity})}/><b>{fmt(p.price*p.quantity)}</b></div></div><button onClick={()=>remove(i)} aria-label="Удалить товар"><Icon name="close"/></button></article>)}</div><div className="delivery">{total>=15000?"Бесплатная доставка включена":`До бесплатной доставки ${fmt(15000-total)}`}</div><div className="cart-total"><span>ИТОГО</span><b>{fmt(total)}</b></div><button className="primary checkout-cta" onClick={checkout}>ОФОРМИТЬ ЗАКАЗ</button></>}</aside></div>;
}

function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  const [delivery,setDelivery]=useState<"courier"|"pickup">("courier");
  const [payment,setPayment]=useState<"card"|"upon">("card");
  const [agreed,setAgreed]=useState(true);
  const [mapPoint,setMapPoint]=useState("Петровка, 12");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const deliveryPrice=delivery==="courier"&&total<15000?690:0;
  const finalTotal=total+deliveryPrice;
  const handleSubmit=(event:React.FormEvent)=>{event.preventDefault();if(!agreed){alert("Подтвердите согласие с условиями заказа");return}submit()};
  const setField=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:event.target.value});
  const points=delivery==="pickup"?["Петровка, 12","Кутузовский проспект, 48","Большая Конюшенная, 12"]:["Петровка, 12","Арбат, 20","Большая Ордынка, 31"];
  useEffect(()=>{setMapPoint(points[0])},[delivery]);
  return <div className="checkout-overlay" role="dialog" aria-modal="true" aria-label="Оформление заказа"><header><button onClick={close} aria-label="Закрыть оформление"><Icon name="close"/></button><b>КУЛЬТУРА ДОМА</b><span>БЕЗОПАСНОЕ ОФОРМЛЕНИЕ</span></header><form onSubmit={handleSubmit}><div className="checkout-main"><div className="checkout-heading"><p>ОФОРМЛЕНИЕ ЗАКАЗА</p><h1>Ваш заказ</h1></div><section className="checkout-section"><div className="checkout-step"><i>1</i><h2>Контактные данные</h2></div><div className="checkout-fields"><label>Имя<input value={form.name} onChange={setField("name")} name="name" autoComplete="given-name" required/></label><label>Фамилия<input value={form.surname} onChange={setField("surname")} name="surname" autoComplete="family-name" required/></label><label>Email<input value={form.email} onChange={setField("email")} type="email" name="email" autoComplete="email" required/></label><label>Телефон<input value={form.phone} onChange={setField("phone")} type="tel" name="phone" autoComplete="tel" placeholder="+7 999 000-00-00" required/></label></div></section><section className="checkout-section"><div className="checkout-step"><i>2</i><h2>Способ получения</h2></div><div className="checkout-options"><label className={delivery==="courier"?"active":""}><input type="radio" name="delivery" checked={delivery==="courier"} onChange={()=>setDelivery("courier")}/><span><b>Курьерская доставка</b><small>{total>=15000?"Бесплатно":"690 ₽"} · 1–3 дня</small></span></label><label className={delivery==="pickup"?"active":""}><input type="radio" name="delivery" checked={delivery==="pickup"} onChange={()=>setDelivery("pickup")}/><span><b>Самовывоз из бутика</b><small>Бесплатно · сегодня</small></span></label></div>{delivery==="courier"&&<div className="checkout-address"><label>Город<input value={form.city} onChange={setField("city")} name="city" required/></label><label>Улица и дом<input value={form.address} onChange={setField("address")} name="address" required/></label><label>Квартира<input name="flat"/></label><label>Комментарий курьеру<input name="comment"/></label></div>}<CheckoutMap points={points} selected={mapPoint} choose={(point)=>{setMapPoint(point);if(delivery==="courier")setForm({...form,address:point})}} mode={delivery}/></section><section className="checkout-section"><div className="checkout-step"><i>3</i><h2>Оплата</h2></div><div className="checkout-options"><label className={payment==="card"?"active":""}><input type="radio" name="payment" checked={payment==="card"} onChange={()=>setPayment("card")}/><span><b>Банковской картой онлайн</b><small>МИР · Visa · Mastercard</small></span></label><label className={payment==="upon"?"active":""}><input type="radio" name="payment" checked={payment==="upon"} onChange={()=>setPayment("upon")}/><span><b>При получении</b><small>Картой или наличными</small></span></label></div></section></div><aside className="checkout-summary"><div className="summary-title"><h2>Состав заказа</h2><button type="button" onClick={editCart}>ИЗМЕНИТЬ</button></div><div className="summary-items">{cart.map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-item-media"/><div><strong>{item.name}</strong><span>{item.selectedColor} · {item.selectedSize}</span><span>Количество: {item.quantity}</span><b>{fmt(item.price*item.quantity)}</b></div></article>)}</div><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Получение</dt><dd>{delivery==="pickup"?`Бутик: ${mapPoint}`:mapPoint}</dd></div><div><dt>Доставка</dt><dd>{deliveryPrice?fmt(deliveryPrice):"Бесплатно"}</dd></div><div className="summary-total"><dt>Итого</dt><dd>{fmt(finalTotal)}</dd></div></dl><label className="checkout-consent"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен с условиями продажи и политикой конфиденциальности</span></label><button className="primary" type="submit">ПОДТВЕРДИТЬ ЗАКАЗ · {fmt(finalTotal)}</button><small className="checkout-security">Данные заказа защищены. Оплата проходит на безопасной странице банка.</small></aside></form></div>;
}

function CheckoutMap({points,selected,choose,mode}:{points:string[];selected:string;choose:(point:string)=>void;mode:"courier"|"pickup"}){
  return <div className="checkout-map"><div className="map-canvas" aria-label="Карта выбора адреса">{points.map((point,index)=><button type="button" key={point} className={`map-pin pin-${index} ${selected===point?"active":""}`} onClick={()=>choose(point)} aria-label={`Выбрать ${point}`}><Icon name="pin"/><span>{index+1}</span></button>)}<i className="river"/><span className="map-label moscow">МОСКВА</span><span className="map-label center">САДОВОЕ КОЛЬЦО</span></div><div className="map-points"><p>{mode==="pickup"?"ВЫБЕРИТЕ БУТИК":"УТОЧНИТЕ ТОЧКУ НА КАРТЕ"}</p>{points.map((point,index)=><button type="button" key={point} className={selected===point?"active":""} onClick={()=>choose(point)}><b>{index+1}</b><span>{point}<small>{mode==="pickup"?"Сегодня до 22:00":"Курьерская доставка"}</small></span></button>)}</div></div>;
}

function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) { return <footer><div className="footer-brand"><div className="logo">КУЛЬТУРА ДОМА</div><p>Подпишитесь на письма о новых коллекциях</p><div><input placeholder="Ваш email"/><button onClick={()=>notice("Спасибо за подписку")}>→</button></div></div><div><p>ПОКУПАТЕЛЯМ</p><button onClick={()=>go("catalog")}>Каталог</button><button onClick={()=>alert("Доставка по России от 1 дня")}>Доставка и оплата</button><button onClick={()=>alert("Возврат в течение 14 дней")}>Возврат</button></div><div><p>О БРЕНДЕ</p><button onClick={()=>go("collections")}>Коллекции</button><button onClick={()=>alert("Русский бренд предметов для дома")}>Наша история</button><button onClick={()=>alert("Москва · Санкт-Петербург · Казань")}>Бутики</button></div><div><p>СВЯЗАТЬСЯ</p><a href="tel:+78005553535">8 800 555-35-35</a><a href="mailto:hello@kultura-doma.ru">hello@kultura-doma.ru</a></div><small>© 2026 Культура дома &nbsp; · &nbsp; Политика конфиденциальности</small></footer> }
