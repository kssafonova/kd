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
  giftPackagingAvailable?: boolean;
};

type ColorVariant = { name: string; hex: string; image: string; gallery?: string[]; position?: string };
type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number; giftWrap?: boolean };
type Slide = { category:string; eyebrow:string; title:string; subtitle:string; image:string; secondaryImage?:string; mobileVideo?:string; align:string; destination:View };
type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };

const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
// PRICE_PENDING_UI_V1
const priceKnown=(value:number)=>Number.isFinite(value)&&value>0;
const productCountLabel=(count:number)=>`${count} ${count===1?"товар":count>=2&&count<=4?"товара":"товаров"}`;

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
function isProductSizeAvailable(product:Product,color:string|undefined,size:string){
  const rows=product.skus?.filter(item=>(!color||item.color===color)&&item.size===size);
  if(!rows?.length)return true;
  return rows.some(item=>item.available!==false);
}
function getUnavailableProductSizes(product:Product,color:string|undefined,sizes:readonly (readonly [string,number])[]){
  return sizes.filter(([name])=>!isProductSizeAvailable(product,color,name)).map(([name])=>name);
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
  { id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: 5990, image: "/images/beige-bedroom.png", badge: "РУЧНАЯ РАБОТА", position: "58% 48%", colorVariants: [
    { name: "Молочный", hex: "#eee8dc", image: "/images/beige-bedroom.png", position: "center 40%" }, { name: "Белый", hex: "#fafafa", image: "/images/zip-product-bed.png" }, { name: "Синий", hex: "#1c3551", image: "/images/zip-collection-night.png" },
  ] },
  { id: 4, name: "Комплект «Нити времени»", note: "сатин, вышивка", price: 24990, image: "/images/time-hero.png", badge: "КАПСУЛА", hasRichContent: true, colorVariants: [
    { name: "Ночной синий", hex: "#10233e", image: "/images/time-hero.png" }, { name: "Небесно-голубой", hex: "#9eb6cf", image: "/images/blue-bedroom.png" }, { name: "Жемчужный", hex: "#e8e5de", image: "/images/zip-product-bed.png" },
  ] },
  { id: 5, name: "Тарелка «Лунная сказка»", note: "фарфор, ручная роспись", price: 5990, image: "/images/moon-plate.png", position: "center", colorVariants: [
    { name: "Ночной синий", hex: "#0c2340", image: "/images/moon-plate.png" }, { name: "Молочный", hex: "#eee8db", image: "/images/zip-hero-summer.png" },
  ] },
  { id: 6, name: "Плед из льна и хлопка", note: "140×200 см", price: 12990, image: "/images/beige-bedroom.png", badge: "РУЧНАЯ РАБОТА", position: "65% 80%", gallery: ["/images/beige-bedroom.png","/images/classic-bedroom.png","/images/zip-product-bed.png"], colorVariants: [
    { name: "Песочный", hex: "#b69a78", image: "/images/beige-bedroom.png" }, { name: "Белый", hex: "#f4f2ec", image: "/images/zip-product-bed.png" }, { name: "Синий", hex: "#203753", image: "/images/zip-collection-night.png" },
  ] },
  { id: 7, name: "Стёганое покрывало «Бархатный ритм»", note: "бархат, 220×240 см", price: 8690, oldPrice: 12990, image: "/images/beige-quilt.jpg", colorVariants: [
    { name: "Песочный", hex: "#c9a982", image: "/images/beige-quilt.jpg" }, { name: "Пудровый", hex: "#e7bca5", image: "/images/peach-sheet.jpg" },
  ] },
  { id: 8, name: "Натяжная простыня из сатина", note: "сатин, 160×200 см", price: 4990, image: "/images/peach-sheet.jpg", colorVariants: [
    { name: "Пудровый", hex: "#e6bca8", image: "/images/peach-sheet.jpg" }, { name: "Молочный", hex: "#efeae1", image: "/images/zip-product-bed.png" },
  ] },
  { id: 9, name: "Сервиз «Северное сияние»", note: "костяной фарфор, 6 персон", price: 24990, image: "/images/russian-service-blue.png", colorVariants:[{name:"Бело-голубой",hex:"#d9edf0",image:"/images/russian-service-blue.png"},{name:"Ночной синий",hex:"#10233e",image:"/images/time-table.png"}] },
  { id: 10, name: "Чайная пара «Нити времени»", note: "костяной фарфор, 250 мл", price: 6990, image: "/images/time-tea-pair.png", gallery:["/images/time-tea-pair.png","/images/time-mug.png","/images/time-table.png"], colorVariants:[{name:"Ночной синий",hex:"#10233e",image:"/images/time-tea-pair.png"}] },
  { id: 11, name: "Подушка «Небесная гладь»", note: "бархат, 25×60 см", price: 4990, image: "/images/sky-bolster.png", colorVariants:[{name:"Небесный",hex:"#9fc2d3",image:"/images/sky-bolster.png"},{name:"Ночной синий",hex:"#203753",image:"/images/time-hero.png"}] },
  { id: 12, name: "Комплект «Голубая светлица»", note: "сатин, вышивка гладью", price: 21990, image: "/images/blue-bedding-vertical.png", hasRichContent: true, colorVariants:[{name:"Ледяной голубой",hex:"#afcbd1",image:"/images/blue-bedding-vertical.png"},{name:"Белый",hex:"#f4f2ec",image:"/images/zip-product-bed.png"}] },

  // ICE_PATTERN_PRODUCTS_V1
  { id:2000, name:"Декоративная подушка «Ледяные узоры»", note:"хлопок, 50×50 см", price:5990, image:"/images/products/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2000-WHITE01.png"},
  ]},
  { id:2001, name:"Тарелка «Ледяные узоры»", note:"костяной фарфор, 23 см", price:7990, image:"/images/products/KD-PD-2001-DARK01.png", colorVariants:[
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2001-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2001-WHITE01.png"},
  ]},
  { id:2003, name:"Плед «Ледяные узоры»", note:"шерсть и хлопок, 140×200 см", price:12990, image:"/images/products/KD-PD-2003-BLUE01.png", gallery:["/images/products/KD-PD-2003-BLUE02.png"], colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ]},
  { id:2004, name:"Чайная пара «Ледяные узоры»", note:"костяной фарфор, 250 мл", price:6990, image:"/images/products/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2004-WHITE01.png"},
  ]},
  { id:2010, name:"Салатник «Ледяные узоры»", note:"костяной фарфор, 24 см", price:9990, image:"/images/products/KD-PD-2010-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2010-WHITE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2010-DARK01.png"},
  ]},
];

const REMOVED_PRODUCT_IDS = new Set([1,9]);
// PRODUCT_PREVIEW_RULES_V1
const catalogPreviewColorByArticle:Record<string,string> = {
  "KD-PD-1028":"Белый",
  "KD-PD-1128":"Белый",
};
const products: Product[] = baseProducts.map(base=>{
  const override=catalogProductOverrides[base.id];
  if(!override)return base;
  const preferredColor=catalogPreviewColorByArticle[override.article];
  const first=(preferredColor?override.skus.find(item=>item.color===preferredColor):undefined)??override.skus[0];
  const colorRows=Array.from(new Map(override.skus.map(item=>[item.color,item])).values());
  const colors=preferredColor
    ? [...colorRows.filter(item=>item.color===preferredColor),...colorRows.filter(item=>item.color!==preferredColor)]
    : colorRows;
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
}).filter(product=>!REMOVED_PRODUCT_IDS.has(product.id));

const slides:Slide[] = [
  { category: "НОВИНКИ", eyebrow: "НОВАЯ ГЛАВА", title: "Дом в цвету", subtitle: "Авторские вазы и сервировка для долгих летних встреч", image: "/images/editorial-vases.webp", secondaryImage: "/images/editorial-table.webp", mobileVideo: "/images/kultura-home-mobile.mp4", align: "left", destination: "catalog" as View },
  { category: "СПАЛЬНЯ", eyebrow: "СПАЛЬНЯ", title: "Белая глава", subtitle: "Постельное бельё с деликатной вышивкой", image: "/images/russian-bedroom.png", align: "left", destination: "catalog" as View },
  { category: "ДЕКОР ДЛЯ ДОМА", eyebrow: "ТИХИЕ ДЕТАЛИ", title: "Естественные оттенки", subtitle: "Тактильный декор для спокойного интерьера", image: "/images/beige-bedroom.png", align: "left", destination: "catalog" as View },
];

const discountOf = (product: Product) => product.oldPrice ? Math.round((1-product.price/product.oldPrice)*100) : 0;

const categories = [
  ["Спальня", "/images/classic-bedroom.png"],
  ["Кухня и столовая", "/images/moon-plate.png"],
  ["Коллекции", "/images/time-collection.png"],
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


// COLLECTION_RENAMES_V51
const makeCollectionEditorialSku = (
  productId:number,
  article:string,
  collection:string,
  color:string,
  size:string,
  material:string,
  price:number,
  image:string,
  gallery:string[] = [],
):CatalogSku => ({
  id:`COL-${productId}-${size}`,
  article,
  productId,
  color,
  colorHex: color.toLowerCase().includes("беж") ? "#d8c7ad" : color.toLowerCase().includes("крас") ? "#8b3030" : "#f5f3ee",
  size,
  material,
  composition:material,
  collection,
  price,
  image,
  gallery,
  available:true,
});

const collectionEditorialProducts:Product[] = [
  // Эхо
  {id:1552,name:"Блюдо овальное Эхо",note:"костяной фарфор, 25×18 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg",selectedColor:"Белый",selectedSize:"25×18 см",skus:[makeCollectionEditorialSku(1552,"УТ-00011436","Эхо","Белый","25×18 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg")]},
  {id:1554,name:"Молочник Эхо",note:"костяной фарфор, 130 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg",selectedColor:"Белый",selectedSize:"130 мл",skus:[makeCollectionEditorialSku(1554,"УТ-00011441","Эхо","Белый","130 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg")]},
  {id:1556,name:"Чайная пара Эхо",note:"костяной фарфор, 250 мл",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1556,"УТ-00011517","Эхо","Белый","250 мл","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg")]},
  {id:1557,name:"Кофейная пара Эхо",note:"костяной фарфор, 90 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg",selectedColor:"Белый",selectedSize:"90 мл",skus:[makeCollectionEditorialSku(1557,"УТ-00011518","Эхо","Белый","90 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg")]},
  {id:1558,name:"Супница Эхо",note:"фарфор, 31×23,7×14 см",price:7273,oldPrice:10390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg",selectedColor:"Белый",selectedSize:"31×23,7×14 см",skus:[makeCollectionEditorialSku(1558,"УТ-00011448","Эхо","Белый","31×23,7×14 см","костяной фарфор",7273,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg")]},
  {id:1561,name:"Сахарница Эхо",note:"костяной фарфор",price:2513,oldPrice:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1561,"УТ-00011440","Эхо","Белый","Единый размер","костяной фарфор",2513,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg")]},
  {id:1562,name:"Тарелка десертная Эхо",note:"костяной фарфор, 20,8 см",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg",selectedColor:"Белый",selectedSize:"20,8 см",skus:[makeCollectionEditorialSku(1562,"УТ-00011432","Эхо","Белый","20,8 см","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg")]},
  {id:1563,name:"Тарелка закусочная Эхо",note:"костяной фарфор, 23,5 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg",selectedColor:"Белый",selectedSize:"23,5 см",skus:[makeCollectionEditorialSku(1563,"УТ-00011433","Эхо","Белый","23,5 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg")]},
  {id:1564,name:"Тарелка обеденная Эхо",note:"костяной фарфор, 26,6 см",price:2793,oldPrice:3990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg",selectedColor:"Белый",selectedSize:"26,6 см",skus:[makeCollectionEditorialSku(1564,"УТ-00011434","Эхо","Белый","26,6 см","костяной фарфор",2793,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg")]},
  {id:1565,name:"Тарелка глубокая Эхо",note:"костяной фарфор, 23 см",price:3353,oldPrice:4790,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg",selectedColor:"Белый",selectedSize:"23 см",skus:[makeCollectionEditorialSku(1565,"УТ-00011435","Эхо","Белый","23 см","костяной фарфор",3353,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg")]},
  {id:1566,name:"Тарелка для супа Эхо",note:"костяной фарфор, 16×11×5 см",price:1533,oldPrice:2190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg",selectedColor:"Белый",selectedSize:"16×11×5 см",skus:[makeCollectionEditorialSku(1566,"УТ-00011447","Эхо","Белый","16×11×5 см","костяной фарфор",1533,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg")]},
  {id:1567,name:"Чайник заварочный Эхо",note:"костяной фарфор, 1800 мл",price:5593,oldPrice:7990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg",selectedColor:"Белый",selectedSize:"1800 мл",skus:[makeCollectionEditorialSku(1567,"УТ-00011438","Эхо","Белый","1800 мл","костяной фарфор",5593,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg")]},

  // Феникс
  {id:1669,name:"Комплект постельного белья Феникс",note:"вышивка, Кинг-сайз",price:16450,oldPrice:32900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg",selectedColor:"Белый",selectedSize:"Кинг-сайз (220х240 см)",skus:[makeCollectionEditorialSku(1669,"УТ-00010374","Феникс","Белый","Кинг-сайз (220х240 см)","текстиль",16450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a301288340ea_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a301287e3819_big.jpg"])]},
  {id:1257,name:"Чайная пара Феникс",note:"фарфор, 250 мл",price:3990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e4b2241_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1257,"УТ-00010254","Феникс","Белый","250 мл","костяной фарфор",3990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e4b2241_big.jpg")]},
  {id:1259,name:"Тарелка десертная Феникс",note:"костяной фарфор",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1259,"УТ-00010255","Феникс","Белый","Единый размер","костяной фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg")]},
  {id:1264,name:"Кружка Феникс",note:"фарфор, 450 мл",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68ee0feabb4b9_big.png",selectedColor:"Белый",selectedSize:"450 мл",skus:[makeCollectionEditorialSku(1264,"УТ-00010256","Феникс","Белый","450 мл","фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/68ee0feabb4b9_big.png")]},
  {id:1260,name:"Салфетка Феникс",note:"лён, 45×45 см",price:995,oldPrice:1990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d2ae09776_big.jpg",selectedColor:"Белый",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1260,"УТ-00010563","Феникс","Белый","45×45 см","лён",995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d2ae09776_big.jpg")]},
  {id:1261,name:"Подушка декоративная Феникс",note:"18×60 см",price:3950,oldPrice:7900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d1802c449_big.jpg",selectedColor:"Бежевый",selectedSize:"18×60 см",skus:[makeCollectionEditorialSku(1261,"УТ-00010596","Феникс","Бежевый","18×60 см","текстиль",3950,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d1802c449_big.jpg")]},
  {id:1262,name:"Подушка декоративная Феникс",note:"40×40 см",price:2995,oldPrice:5990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a05e8f392e1b_big.jpg",selectedColor:"Бежевый",selectedSize:"40×40 см",skus:[makeCollectionEditorialSku(1262,"УТ-00010595","Феникс","Бежевый","40×40 см","текстиль",2995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a05e8f392e1b_big.jpg")]},
  {id:1263,name:"Плейсмат Феникс",note:"лён, 40×50 см",price:1295,oldPrice:2590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d17c5a9c1_big.jpg",selectedColor:"Белый",selectedSize:"40×50 см",skus:[makeCollectionEditorialSku(1263,"УТ-00010579","Феникс","Белый","40×50 см","лён",1295,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d17c5a9c1_big.jpg")]},
  {id:1267,name:"Дорожка Феникс",note:"50×180 см",price:3450,oldPrice:6900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16a6263e_big.jpg",selectedColor:"Белый",selectedSize:"50×180 см",skus:[makeCollectionEditorialSku(1267,"УТ-00010411","Феникс","Белый","50×180 см","текстиль",3450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16a6263e_big.jpg")]},
  {id:1499,name:"Свеча с ароматом Древо жизни Феникс",note:"кокосовый воск, 10 см",price:4990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg",selectedColor:"Белый",selectedSize:"10 см",skus:[makeCollectionEditorialSku(1499,"УТ-00011405","Феникс","Белый","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg")]},
  {id:1500,name:"Свеча с ароматом Сандал и Шалфей Феникс",note:"кокосовый воск, 10 см",price:4990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg",selectedColor:"Белый",selectedSize:"10 см",skus:[makeCollectionEditorialSku(1500,"УТ-00011381","Феникс","Белый","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg")]},
  {id:1266,name:"Ковер Феникс",note:"натуральная шерсть, 150×200 см",price:420000,oldPrice:600000,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg",selectedColor:"Бежевый",selectedSize:"150×200 см",skus:[makeCollectionEditorialSku(1266,"УТ-00010178","Феникс","Бежевый","150×200 см","натуральная шерсть",420000,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg")]},

  // Нити — товары из текущего фида «Нити времени»
  {id:1268,name:"Чайная пара Нити",note:"костяной фарфор, 250 мл",price:4490,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg",selectedColor:"Синий",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1268,"УТ-00010261","Нити","Синий","250 мл","костяной фарфор",4490,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e7620299d06_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc53c6d_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bca1043_big.jpg"]) ]},
  {id:1270,name:"Тарелка десертная Нити",note:"костяной фарфор",price:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg",selectedColor:"Синий",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1270,"УТ-00010262","Нити","Синий","Единый размер","костяной фарфор",3590,"https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e675cf04624_big.jpg"]) ]},
  {id:1287,name:"Кружка Нити",note:"костяной фарфор, 450 мл",price:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68efaf6f5d4d9_big.jpg",selectedColor:"Синий",selectedSize:"450 мл",skus:[makeCollectionEditorialSku(1287,"УТ-00010263","Нити","Синий","450 мл","костяной фарфор",3590,"https://kultura-doma.ru/public/src/images/gallery/catalog/68efaf6f5d4d9_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68ee105cb8a67_big.jpg"]) ]},
  {id:1271,name:"Салфетка Нити",note:"сатин, 45×45 см",price:995,oldPrice:1990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d36ad614e_big.jpg",selectedColor:"Белый",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1271,"УТ-00010564","Нити","Белый","45×45 см","сатин",995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d36ad614e_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e6763f9c9ed_big.jpg"]) ]},
  {id:1272,name:"Подушка декоративная Нити",note:"45×45 см",price:2745,oldPrice:5490,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69e5d18433139_big.jpg",selectedColor:"Голубой",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1272,"УТ-00010599","Нити","Голубой","45×45 см","текстиль",2745,"https://kultura-doma.ru/public/src/images/gallery/catalog/69e5d18433139_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e669d46c745_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/68e61cd4aadc6_big.jpg"]) ]},
  {id:1273,name:"Плейсмат Нити",note:"сатин, 38×47 см",price:1295,oldPrice:2590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg",selectedColor:"Синий",selectedSize:"38×47 см",skus:[makeCollectionEditorialSku(1273,"УТ-00010580","Нити","Синий","38×47 см","сатин",1295,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e6767806b54_big.jpg"]) ]},
  {id:1276,name:"Дорожка Нити",note:"сатин, 50×180 см",price:3450,oldPrice:6900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16b97b10_big.jpg",selectedColor:"Синий",selectedSize:"50×180 см",skus:[makeCollectionEditorialSku(1276,"УТ-00010412","Нити","Синий","50×180 см","сатин",3450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16b97b10_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e678cb78600_big.jpg"]) ]},
];

// COLLECTIONS_REDESIGN_V65
const normalizeRetiredCatalogName=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/[‐‑‒–—]/g,"-").replace(/\s+/g," ");
const isRetiredCatalogProduct=(name:string)=>{const value=normalizeRetiredCatalogName(name);return value.includes("мокоши")||value.includes("овация")||/жар(?:-| )?птица/.test(value)};
for(let index=products.length-1;index>=0;index-=1){if(isRetiredCatalogProduct(products[index].name))products.splice(index,1)}
products.push(...collectionEditorialProducts.filter(item=>!isRetiredCatalogProduct(item.name)&&!products.some(existing=>existing.id===item.id)));

type Editorial = { id:string; name:string; kind:"КАПСУЛА"|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string[]; productIds:number[] };
// COLLECTIONS_REDESIGN_V65_INDEX
const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);
const editorials:Editorial[] = [
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле. Белый, ледяной голубой и деликатный орнамент создают ощущение тихого зимнего утра.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/images/editorial/caps_led.png","/images/editorial/caps_led_podyshka.png","/images/editorial/caps_led_podyshka2.png","/images/editorial/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КОЛЛЕКЦИЯ", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Коллекция о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png"], productIds:[4,10,5,6,3] },
  { id:"echo", name:"Эхо", kind:"КОЛЛЕКЦИЯ", lead:"Светлый фарфор и тонкий рельеф для спокойной, современной сервировки.", detail:"Эхо строится на белом костяном фарфоре и мягком повторении формы — от чайной пары до большого блюда. Коллекция легко собирается как для ежедневного стола, так и для камерного ужина.", description:"Чистая сервировка, в которой декоративность проявляется через пропорции, рельеф и свет.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg"], productIds:collectionProductIds("Эхо") },
  { id:"niti", name:"Нити", kind:"КОЛЛЕКЦИЯ", lead:"Синий орнамент, сатин и фарфор связывают текстиль и сервировку в одну историю.", detail:"Нити соединяет предметы стола и мягкий декор через холодную синюю палитру. Салфетки, плейсматы, фарфор и подушка работают как один набор, но каждый предмет можно выбрать отдельно.", description:"Коллекция о повторяющемся орнаменте и тактильных слоях — от сервировки до декоративного текстиля.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69e5d18433139_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg"], productIds:collectionProductIds("Нити") },
  { id:"phoenix", name:"Феникс", kind:"КОЛЛЕКЦИЯ", lead:"Тёплые акценты, золото и выразительный орнамент для дома с характером.", detail:"Феникс объединяет спальню, сервировку и атмосферный декор. Светлый фон делает рисунок легче, а золотые и красные акценты собирают предметы в цельный образ.", description:"Выразительная коллекция для тех, кто хочет добавить в интерьер один сильный мотив и продолжить его в нескольких зонах дома.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg"], productIds:collectionProductIds("Феникс") },
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
  const [boutiquesOpen,setBoutiquesOpen]=useState(false);
  const [favorites, setFavorites] = useState<number[]>([]);
  const [recentlyViewed,setRecentlyViewed]=useState<number[]>([]);
  const [slide, setSlide] = useState(0);
  // UNIFIED_SITE_QUERY_BRIDGE_V52
  useEffect(()=>{
    const params=new URLSearchParams(window.location.search);
    const section=params.get("section");
    const open=params.get("open");
    const requestedCollection=params.get("collection");
    if(section==="collections")setView("collections");
    if(requestedCollection){
      const key=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
      const aliases:Record<string,string>={"камея":"Эхо","эхо":"Эхо","нити времени":"Нити","нити":"Нити","жар-птица":"Феникс","жар птица":"Феникс","феникс":"Феникс"};
      const requested=aliases[key(requestedCollection)]||requestedCollection;
      const matched=editorials.find(item=>key(item.name)===key(requested));
      if(matched){setEditorial(matched);setView("editorial")}
    }
    if(open==="cart")setCartOpen(true);
    if(open==="search")setSearch(true);
    if(open==="account")setAccount(true);
    if(open==="favorites")setFavoritesOpen(true);
    if(open==="menu"){setMenuSection("");setMenu(true)}
    if(open==="boutiques")setBoutiquesOpen(true);
    if(section||open||requestedCollection)window.history.replaceState({},"",window.location.pathname);
  },[]);
  const [toast, setToast] = useState("");

  useEffect(() => {
    document.body.style.overflow = menu || search || account || favoritesOpen || filters || plpSize || plpAdded || sizeSheet || cartOpen || checkoutOpen || boutiquesOpen ? "hidden" : "";
    return () => { document.body.style.overflow = ""; };
  }, [menu, search, account, favoritesOpen, filters, plpSize, plpAdded, sizeSheet, cartOpen, checkoutOpen, boutiquesOpen]);
  useEffect(()=>{try{const savedProfile=localStorage.getItem("kultura-profile");const savedFavorites=localStorage.getItem("kultura-favorites");const savedViewed=localStorage.getItem("kultura-viewed");const savedCart=localStorage.getItem("kultura-cart");if(savedProfile)setProfile(JSON.parse(savedProfile));if(savedFavorites)setFavorites(JSON.parse(savedFavorites));if(savedViewed)setRecentlyViewed(JSON.parse(savedViewed));if(savedCart)setCart(JSON.parse(savedCart))}catch{}
    try{
      const params=new URLSearchParams(window.location.search);
      if(params.get("cart")==="open"){
        setCartOpen(true);
        const url=new URL(window.location.href);
        url.searchParams.delete("cart");
        window.history.replaceState({},"",url.toString());
      }
    }catch{}
  },[]);
  useEffect(()=>{localStorage.setItem("kultura-favorites",JSON.stringify(favorites))},[favorites]);
  useEffect(()=>{if(profile)localStorage.setItem("kultura-profile",JSON.stringify(profile));else localStorage.removeItem("kultura-profile")},[profile]);
  useEffect(()=>{localStorage.setItem("kultura-viewed",JSON.stringify(recentlyViewed))},[recentlyViewed]);
  useEffect(()=>{localStorage.setItem("kultura-cart",JSON.stringify(cart))},[cart]);

  const total = useMemo(() => cart.reduce((sum, item) => sum + item.price * item.quantity, 0), [cart]);
  const cartCount = useMemo(() => cart.reduce((sum, item) => sum + item.quantity, 0), [cart]);
  const go = (next: View) => { setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };
  const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog")};
  const add = (product: Product, chosenSize = size, quantity = product.quantity ?? 1, openDrawer = true) => {
    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const selectedSku=findProductSku(product,product.selectedColor,chosenSize);
    const item: CartItem = { ...product, price:selectedSku?.price??product.price, image:selectedSku?.image??selectedVariant?.image??product.image, gallery:selectedSku?.gallery??product.gallery, position:selectedVariant?.position??product.position, selectedSize:chosenSize, selectedColor:selectedSku?.color??selectedVariant?.name??"Молочный", selectedSkuId:selectedSku?.id, quantity };
    setCart((current) => [...current, item]);
    setPlpSize(null); setSizeSheet(false); if(openDrawer)setPlpAdded(item);
  };
  const addBundle = (items: Product[]) => {
    const bundleItems: CartItem[] = items.map((product)=>{
      const variant=product.colorVariants?.find(v=>v.name===product.selectedColor)??product.colorVariants?.[0];
      const sku=findProductSku(product,product.selectedColor,product.selectedSize);
      return {...product,price:sku?.price??product.price,image:sku?.image??variant?.image??product.image,gallery:sku?.gallery??product.gallery,position:variant?.position??product.position,selectedSize:sku?.size??product.selectedSize??"",selectedColor:sku?.color??variant?.name??"Молочный",selectedSkuId:sku?.id,quantity:product.quantity??1};
    });
    setCart(current=>[...current,...bundleItems]);
    setCartOpen(true);
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
      <Header onMenu={() => { setMenuSection(""); setMenu(true); }} onSearch={() => setSearch(true)} onAccount={() => setAccount(true)} onFavorites={() => setFavoritesOpen(true)} onCart={() => setCartOpen(true)} onBoutiques={() => setBoutiquesOpen(true)} count={cartCount} favoriteCount={favorites.length} go={go} />
      {view === "home" && <HomeView go={go} openCatalog={openCatalog} slide={slide} setSlide={setSlide} onProduct={openProduct} favorite={favorite} favorites={favorites} onAdd={setPlpSize} openEditorial={(item)=>{setEditorial(item);go("editorial")}} />}
      {view === "catalog" && <CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />}
      {view === "collections" && <CollectionsView onProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}
      {view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} onQuick={setPlpSize} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}
      {view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} recentlyViewed={recentlyViewed} />}
      <Footer go={go} notice={notice} />

      {menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} />}
      {search && <Search close={() => setSearch(false)} choose={(p) => { setSelected(p); setSearch(false); go("product"); }} />}
      {account && <Account profile={profile} close={() => setAccount(false)} notice={notice} save={setProfile} logout={()=>setProfile(null)} />}
      {favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setSelected(product);setFavoritesOpen(false);go("product")}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}
      {filters && <Filters close={() => setFilters(false)} apply={() => { setFilters(false); notice("Фильтры применены"); }} count={products.length} />}
      {plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,quantity,unitPrice) => addFromPLP(plpSize, chosenSize, quantity, unitPrice)} />}
      {plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} selectProduct={(product)=>{setPlpAdded(null);openProduct(product)}} updateGift={(giftWrap)=>{const target=plpAdded;setPlpAdded({...target,giftWrap});setCart(current=>{const next=[...current];for(let i=next.length-1;i>=0;i--){const item=next[i];if(item.id===target.id&&item.selectedSize===target.selectedSize&&item.selectedColor===target.selectedColor){next[i]={...item,giftWrap};break}}return next})}} />}
      {sizeSheet && <SizeSheet size={size} setSize={setSize} close={() => setSizeSheet(false)} add={(quantity,unitPrice) => add({...selected,price:unitPrice},size,quantity)} price={selected.price} />}
      {cartOpen && <Cart cart={cart} profile={profile} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} quickAdd={(product)=>{setCartOpen(false);setPlpSize(product)}} />}
      {checkoutOpen&&<Checkout cart={cart} total={total} profile={profile} close={()=>setCheckoutOpen(false)} editCart={()=>{setCheckoutOpen(false);setCartOpen(true)}} submit={()=>{setCheckoutOpen(false);setCart([]);notice("Заказ оформлен. Подтверждение отправлено на email")}}/>}
      {boutiquesOpen&&<BoutiqueMap close={()=>setBoutiquesOpen(false)}/>}
      {toast && <div className="toast">{toast}</div>}
    </main>
  );
}

function Header({ onMenu, onSearch, onAccount, onFavorites, onCart, onBoutiques, count, favoriteCount, go }: { onMenu:()=>void; onSearch:()=>void; onAccount:()=>void; onFavorites:()=>void; onCart:()=>void; onBoutiques:()=>void; count:number; favoriteCount:number; go:(v:View)=>void }) {
  return <header className="header">
    <div className="header-left"><button className="icon-btn hamburger" aria-label="Открыть меню" onClick={onMenu}><i/><i/><i/></button><button className="boutiques" onClick={onBoutiques}><Icon name="pin"/> Бутики</button></div>
    <button className="logo" onClick={() => go("home")}>КУЛЬТУРА ДОМА</button>
    <div className="header-actions"><button onClick={onSearch} aria-label="Поиск"><Icon name="search"/></button><button onClick={onAccount} aria-label="Профиль"><Icon name="user"/></button><button className="favorite-header" onClick={onFavorites} aria-label={`Избранное: ${favoriteCount}`}><Icon name="heart" filled={favoriteCount>0}/>{favoriteCount>0&&<b>{favoriteCount}</b>}</button><button className="bag" onClick={onCart} aria-label="Корзина"><Icon name="bag"/>{count > 0 && <b>{count}</b>}</button></div>
  </header>;
}


// HOME_BOUTIQUES_MAP_V11
function HomeBoutiques(){
  const boutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124},
  ];
  const [selected,setSelected]=useState(0);
  const boutique=boutiques[selected];
  const delta=.04;
  const mapSrc=`https://www.openstreetmap.org/export/embed.html?bbox=${boutique.lon-delta}%2C${boutique.lat-delta}%2C${boutique.lon+delta}%2C${boutique.lat+delta}&layer=mapnik&marker=${boutique.lat}%2C${boutique.lon}`;
  return <section id="home-boutiques" className="home-boutiques-map" aria-labelledby="home-boutiques-title">
    <div className="home-boutiques-copy">
      <small>БУТИКИ</small>
      <h2 id="home-boutiques-title">Посетите Культура дома</h2>
      <p>Посмотрите материалы, оттенки и коллекции вживую. Выберите город — карта покажет расположение бутика.</p>
      <div className="home-boutique-list" aria-label="Выбрать бутик">
        {boutiques.map((item,index)=><button type="button" key={item.city} className={index===selected?"active":""} onClick={()=>setSelected(index)} aria-pressed={index===selected}>
          <span><Icon name="pin"/><b>{item.city}</b></span>
          <strong>{item.address}</strong>
          <small>{item.hours}</small>
        </button>)}
      </div>
    </div>
    <div className="home-boutiques-map-canvas">
      <iframe key={`${boutique.city}-${selected}`} src={mapSrc} title={`Карта бутика Культура дома — ${boutique.city}`} loading="lazy" referrerPolicy="no-referrer-when-downgrade"/>
      <div className="home-boutiques-map-caption"><div><b>{boutique.city}</b><span>{boutique.address}</span></div><small>{boutique.hours}</small></div>
    </div>
  </section>;
}

function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_SKETCH_ZARA_KULTURA_V45
  const heroSlides=[
    {label:"КАПСУЛА",title:"Лунная сказка",subtitle:"Тихая история для спальни и позднего чаепития",desktopImage:"/images/editorial/caps_luna_postel2.png",mobileImage:"/images/editorial/caps_luna_postel.png",cta:"Смотреть коллекцию",action:()=>openEditorial(editorials[1])},
    {label:"КОЛЛЕКЦИЯ",title:"Ледяные узоры",subtitle:"Светлая зимняя палитра, вышивка и мягкие фактуры",desktopImage:"/images/editorial/caps_led.png",mobileImage:"/images/editorial/caps_led_podyshka.png",cta:"Смотреть коллекцию",action:()=>openEditorial(editorials[0])},
    {label:"ПОСУДА И СЕРВИРОВКА",title:"Дом начинается с ритуалов",subtitle:"Фарфор, текстиль и предметы для красивой повседневности",desktopImage:"/images/time-table.png",mobileImage:"/images/russian-service-blue.png",cta:"Смотреть каталог",action:()=>openCatalog("Посуда и сервировка")},
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const [paused,setPaused]=useState(false);
  const touchStart=useRef<number|null>(null);
  useEffect(()=>{
    if(paused||typeof window==="undefined"||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),7000);
    return()=>window.clearInterval(timer);
  },[activeIndex,paused,setSlide,heroSlides.length]);
  const shift=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);

  const categories=[
    {title:"Постельное бельё",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Пледы",image:"/images/products/KD-PD-2003-BLUE01.png",category:"Пледы и подушки"},
    {title:"Подушки",image:"/images/products/KD-PD-2000-WHITE01.png",category:"Пледы и подушки"},
    {title:"Посуда",image:"/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {title:"Сервировка",image:"/images/time-table.png",category:"Посуда и сервировка"},
    {title:"Декор",image:"/images/beige-bedroom.png",category:"Все товары"},
  ];
  const newProducts=[2000,2004,2010,2003,4,10,5,6].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const collection=editorials[1]??editorials[0];
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;
  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/images/constructor/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/images/constructor/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/images/products/KD-PD-2000-WHITE01.png",href:`${constructorHref}table-7/`},
    {room:"КАБИНЕТ",title:"Тёплый брутализм",image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a4375b9224e0_big.jpg",href:`${constructorHref}table-8/`},
  ];

  return <main className="home-sketch-v45">
    <section className="hs45-hero" aria-label="Главный баннер"
      onPointerEnter={()=>setPaused(true)} onPointerLeave={()=>setPaused(false)}
      onTouchStart={event=>{touchStart.current=event.touches[0]?.clientX??null;setPaused(true)}}
      onTouchEnd={event=>{const start=touchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shift(end<start?1:-1);touchStart.current=null;setPaused(false)}}>
      <picture><source media="(max-width:700px)" srcSet={assetUrl(hero.mobileImage)}/><img src={assetUrl(hero.desktopImage)} alt={hero.title}/></picture>
      <div className="hs45-hero-overlay"/>
      <div className="hs45-hero-copy"><small>{hero.label}</small><h1>{hero.title}</h1><p>{hero.subtitle}</p><button type="button" onClick={hero.action}>{hero.cta}</button></div>
      <div className="hs45-hero-nav"><div>{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===activeIndex?"active":""} onClick={()=>setSlide(index)} aria-label={item.title}/>)}</div><span><button type="button" onClick={()=>shift(-1)} aria-label="Назад">←</button><button type="button" onClick={()=>shift(1)} aria-label="Вперёд">→</button></span></div>
    </section>

    <section className="hs45-categories hs45-shell" aria-labelledby="hs45-categories-title">
      <header className="hs45-head"><div><small>КАТАЛОГ</small><h2 id="hs45-categories-title">Категории</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>Весь каталог →</button></header>
      <div className="hs45-category-row">{categories.map(item=><button type="button" key={item.title} onClick={()=>openCatalog(item.category)}><span><img src={assetUrl(item.image)} alt={item.title}/></span><strong>{item.title}</strong></button>)}</div>
    </section>

    <section className="hs45-new hs45-shell" aria-labelledby="hs45-new-title">
      <header className="hs45-head"><div><small>НОВИНКИ</small><h2 id="hs45-new-title">Новое поступление</h2></div><button type="button" onClick={()=>openCatalog("Все товары")}>Смотреть всё →</button></header>
      <div className="hs45-product-grid">{newProducts.slice(0,4).map(product=><ProductCard key={`home-v45-${product.id}`} product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>
    </section>

    {collection&&<section className="hs45-collection" aria-labelledby="hs45-collection-title">
      <button type="button" className="hs45-collection-media" onClick={()=>openEditorial(collection)}><img src={assetUrl(collection.images[0])} alt={collection.name}/></button>
      <div className="hs45-collection-copy"><small>{collection.kind}</small><h2 id="hs45-collection-title">{collection.name}</h2><p>{collection.lead}</p><button type="button" onClick={()=>openEditorial(collection)}>Смотреть коллекцию →</button></div>
    </section>}

    <section className="hs45-solutions hs45-shell" aria-labelledby="hs45-solutions-title">
      <header className="hs45-head"><div><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2 id="hs45-solutions-title">Пространства, собранные за вас</h2></div><a href={constructorHref}>Все решения →</a></header>
      <div className="hs45-solution-grid">{solutions.map(item=><a href={item.href} key={item.title}><span className="hs45-solution-media"><img src={assetUrl(item.image)} alt={item.title}/></span><span className="hs45-solution-copy"><small>{item.room}</small><strong>{item.title}</strong><em>Собрать решение →</em></span></a>)}</div>
    </section>

    <section className="hs45-boutiques-intro hs45-shell"><small>БУТИКИ</small><h2>Культура Дома рядом</h2><p>Посмотрите материалы, оттенки и фактуры вживую.</p></section>
    <HomeBoutiques/>
  </main>;
}


function CatalogView({ initialCategory, onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {
  const [sort, setSort] = useState("По умолчанию");
  const [category,setCategory]=useState(initialCategory);
  useEffect(()=>setCategory(initialCategory),[initialCategory]);
  const categoryProductIds:Record<string,number[]>={
    "Все товары":products.map(product=>product.id),
    "Посуда и сервировка":[5,10,2001,2004,2010],
    "Постельное бельё":[2,4,8,11,12],
    "Пледы и подушки":[3,6,7,2000,2003],
    "Домашняя одежда":[],
    "Столовый текстиль":[],
  };
  const list = products.filter(product=>(categoryProductIds[category]??[]).includes(product.id)).sort((a,b)=>sort === "Сначала дешевле" ? a.price-b.price : sort === "Сначала дороже" ? b.price-a.price : a.id-b.id);
  return <div className="catalog page"><div className="crumbs">Главная / Каталог / {category}</div><div className="title-line"><h1>{category}</h1><span>{list.length} {list.length===1?"товар":list.length>=2&&list.length<=4?"товара":"товаров"}</span></div>
    <div className="tabs">{["Все товары","Посуда и сервировка","Постельное бельё","Пледы и подушки","Домашняя одежда","Столовый текстиль"].map(x=><button key={x} className={category===x?"active":""} onClick={()=>setCategory(x)}>{x}</button>)}</div>
    <div className="catalog-tools"><select value={sort} onChange={e=>setSort(e.target.value)}><option>По умолчанию</option><option>Сначала дешевле</option><option>Сначала дороже</option></select><button onClick={onFilter}><Icon name="filter"/> Фильтры</button></div>
    {list.length?<div className="product-grid">{list.map(p=><ProductCard key={`${category}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div>:<div className="catalog-empty"><p>В этой категории пока нет товаров</p></div>}
  </div>;
}

function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect, onVariantChange }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void; onVariantChange?:(product:Product)=>void }) { // PRODUCT_CARD_VARIANT_CALLBACK_V34
  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];
  const [colorIndex, setColorIndex] = useState(0);
  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const chosenProduct = { ...product, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };
  const discount=discountOf(product);
  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);
  const knownPrice=priceKnown(product.price);
  const chooseVariant=(index:number)=>{
    setColorIndex(index);
    const variant=variants[index];
    const sku=findProductSku(product,variant.name);
    onVariantChange?.({...product,image:sku?.image??variant.image,gallery:sku?.gallery??variant.gallery??product.gallery,position:variant.position??product.position,selectedColor:variant.name,selectedSize:sku?.size,selectedSkuId:sku?.id});
  };
  return <article className="product-card"><button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button><button className="product-image" onClick={()=>onClick(chosenProduct)}><ScrollableProductMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, цвет ${chosen.name}`} position={chosen.position||product.position}/>{product.badge&&<span>{product.badge}</span>}</button><div className="product-copy"><button className="product-link" onClick={()=>onClick(chosenProduct)}><strong>{product.name}</strong><small>{chosen.name.toLowerCase()}, {product.note}</small></button>{variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>chooseVariant(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span></div>{selectionMode?<button className={`quick selection-check ${pending?"pending":selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={pending?`Выберите размер для ${product.name}`:selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{pending?"?":selected?"✓":""}</button>:<button className="quick" disabled={!knownPrice} onClick={()=>knownPrice&&onQuick(chosenProduct)} aria-label={knownPrice?`Добавить в корзину ${product.name}`:`Цена товара ${product.name} уточняется`}><Icon name="cart-add"/></button>}</article>;
}

// EDITORIAL_STORY_OVERLAY_V1
// EDITORIAL_STORY_OVERLAY_V2
// EDITORIAL_STORY_OVERLAY_V2
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
// EDITORIAL_STORY_OVERLAY_V3
function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle,initialEditorial }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void; initialEditorial?:Editorial }) {
  // COLLECTIONS_UNIFIED_V52
  const [active,setActive]=useState<Editorial|null>(initialEditorial??null);
  const [purchaseMode,setPurchaseMode]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>([]);
  const [sizes,setSizes]=useState<Record<number,string>>({});
  const [variants,setVariants]=useState<Record<number,Product>>({});

  useEffect(()=>{
    if(initialEditorial){
      setActive(initialEditorial);
      setPurchaseMode(false);
      setSelectedIds([]);
      setSizes({});
      setVariants({});
    }
  },[initialEditorial?.id]);

  useEffect(()=>{
    if(!active)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[active]);

  const collectionPrice=(editorial:Editorial)=>{
    const values=editorial.productIds.map(id=>products.find(item=>item.id===id)?.price||0).filter(Boolean);
    return values.length?Math.min(...values):0;
  };
  const items=useMemo(()=>active?active.productIds.map(id=>products.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)):[],[active]);
  const open=(editorial:Editorial)=>{setActive(editorial);setPurchaseMode(false);setSelectedIds([]);setSizes({});setVariants({})};
  const close=()=>{setActive(null);setPurchaseMode(false);setSelectedIds([]);setSizes({});setVariants({})};
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(item=>item!==id):[...current,id]);
  const currentProduct=(item:Product)=>variants[item.id]??item;
  const colorOf=(item:Product)=>{const current=currentProduct(item);return current.selectedColor??current.colorVariants?.[0]?.name??current.skus?.[0]?.color??""};
  const sizeOptions=(item:Product)=>getProductSizeOptions(currentProduct(item),colorOf(item));
  const pending=selectedIds.filter(id=>{
    const item=items.find(product=>product.id===id);
    if(!item)return false;
    return sizeOptions(item).length>1&&!sizes[id];
  });
  const selectedProducts=selectedIds.map(id=>items.find(item=>item.id===id)).filter((item):item is Product=>Boolean(item)).map(item=>{
    const current=currentProduct(item);
    const color=colorOf(item);
    const options=sizeOptions(item);
    const selectedSize=sizes[item.id]??(options.length===1?options[0][0]:"");
    const sku=selectedSize?findProductSku(current,color,selectedSize):findProductSku(current,color);
    return {...current,selectedColor:color,selectedSize:selectedSize||sku?.size||"",selectedSkuId:sku?.id,price:sku?.price??current.price};
  });
  const total=selectedProducts.reduce((sum,item)=>sum+item.price,0);
  const allSelected=items.length>0&&selectedIds.length===items.length;
  const startPurchase=()=>{setPurchaseMode(true);setSelectedIds([]);setSizes({})};
  const finishPurchase=()=>{setPurchaseMode(false);setSelectedIds([]);setSizes({})};
  const addSelected=()=>{if(selectedProducts.length&&pending.length===0){buyBundle(selectedProducts);close()}};
  // READY_SOLUTION_COLLECTION_BRIDGE_V58
  const readySolutionCollection=active?({"Символы":"Мокоши","Эхо":"Камея","Феникс":"Жар-птица"} as Record<string,string>)[active.name]||active.name:"";
  const readySolutionHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/?collection=${encodeURIComponent(readySolutionCollection)}`;

  return <main className="collections-v52">
    <header className="collections-v52-intro">
      <div><small>КУЛЬТУРА ДОМА · EDITORIAL</small><h1>Коллекции</h1></div>
      <p>Истории для дома, собранные вокруг цвета, орнамента и ритуала. Откройте коллекцию как журнал — и выбирайте предметы только тогда, когда они действительно нужны.</p>
    </header>
    <section className="collections-v52-index" aria-label="Коллекции Культура Дома">
      {editorials.map(editorial=><article className="collections-v52-card" key={editorial.id}>
        <button className="collections-v52-card-media" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v52-card-copy"><small>КОЛЛЕКЦИЯ</small><button type="button" onClick={()=>open(editorial)}><h2>{editorial.name}</h2></button><p>{editorial.lead}</p><div><span>{productCountLabel(editorial.productIds.length)}</span><strong>{collectionPrice(editorial)?`от ${fmt(collectionPrice(editorial))}`:""}</strong></div></div>
      </article>)}
    </section>

    {active&&<div className="v52-story-backdrop" role="presentation"><button className="v52-story-dismiss" type="button" onClick={close} aria-label="Закрыть коллекцию"/>
      <section className="v52-story-modal" role="dialog" aria-modal="true" aria-label={`Коллекция ${active.name}`}>
        <header className="v52-story-topbar"><button type="button" onClick={close}>← Коллекции</button><strong>КУЛЬТУРА ДОМА</strong><button type="button" onClick={close} aria-label="Закрыть">×</button></header>
        <div className="v52-story-columns">
          <aside className="v52-story-editorial" aria-label="История коллекции">
            <div className="v52-story-title"><small>КОЛЛЕКЦИЯ</small><h1>{active.name}</h1><p>{active.lead}</p><span>{productCountLabel(items.length)}</span></div>
            {active.images.map((image,index)=><figure key={`${active.id}-${image}`}><img src={assetUrl(image)} alt={`${active.name}, кадр ${index+1}`}/>{index===0&&<figcaption>{active.detail}</figcaption>}</figure>)}
            <div className="v52-story-note"><small>О КОЛЛЕКЦИИ</small><p>{active.description}</p><a className="v52-buy-story v58-ready-solution-link" href={readySolutionHref}>СОБРАТЬ ГОТОВОЕ РЕШЕНИЕ →</a></div>
          </aside>
          <section className="v52-story-commerce" aria-label="Товары коллекции">
            <header className="v52-commerce-head"><div><small>{purchaseMode?"СОБЕРИТЕ СВОЮ ИСТОРИЮ":"ТОВАРЫ КОЛЛЕКЦИИ"}</small><h2>{purchaseMode?"Выберите предметы":"Предметы истории"}</h2><p>{purchaseMode?"Отметьте нужные позиции. Для товаров с несколькими размерами размер можно выбрать после отметки.":"Каждый предмет можно добавить отдельно — привычной кнопкой корзины, как в каталоге."}</p></div>{purchaseMode?<div className="v52-commerce-actions"><button type="button" className="v52-secondary-action" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всё"}</button><button type="button" className="v52-text-action" onClick={finishPurchase}>Отменить</button></div>:<button type="button" className="v52-buy-story" onClick={startPurchase}>КУПИТЬ КОЛЛЕКЦИЮ</button>}</header>
            <div className={`product-grid v52-story-products ${purchaseMode?"is-selection-mode":""}`}>{items.map(item=>{const current=currentProduct(item);const selected=selectedIds.includes(item.id);const options=sizeOptions(item);const needsSize=selected&&options.length>1&&!sizes[item.id];return <div className={`v52-story-product ${selected?"selected":""}`} key={item.id}><ProductCard product={current} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={purchaseMode} selected={selected} pending={needsSize} onSelect={()=>toggle(item.id)} onVariantChange={product=>{setVariants(state=>({...state,[item.id]:product}));setSizes(state=>{const next={...state};delete next[item.id];return next})}}/>{purchaseMode&&selected&&options.length>1&&<label className="v52-inline-size"><span>Размер</span><select value={sizes[item.id]??""} onChange={event=>setSizes(state=>({...state,[item.id]:event.target.value}))}><option value="">Выбрать</option>{options.map(([name])=><option key={name} value={name}>{name}</option>)}</select></label>}</div>})}</div>
            {purchaseMode&&<footer className="v52-purchase-bar"><div><span>{pending.length?`Выберите размер · ${pending.length}`:selectedProducts.length?`Выбрано ${selectedProducts.length} из ${items.length}`:"Выберите товары"}</span><strong>{fmt(total)}</strong></div><button type="button" disabled={!selectedProducts.length||pending.length>0} onClick={addSelected}>ДОБАВИТЬ В КОРЗИНУ</button></footer>}
          </section>
        </div>
      </section>
    </div>}
  </main>;
}

function EditorialView({ editorial, selectProduct, onQuick, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  // Direct/legacy editorial entry uses the same V52 collection experience.
  return <CollectionsView onProduct={selectProduct} onQuick={onQuick} favorite={favorite} favorites={favorites} buyBundle={buyBundle} initialEditorial={editorial}/>;
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
          <div className="lookbook-shop-grid">{items.map(item=><button key={item.id} onClick={()=>{close();selectProduct?.(item)}}><RemoteImage src={item.image} alt={item.name}/><span>{item.name}<b>{priceKnown(item.price)?fmt(item.price):"Цена уточняется"}</b></span></button>)}</div>
        </article>
      </div>
      <div className="lookbook-mobile-progress">{chapterLabels.map((_,index)=><button key={index} className={chapter===index?"active":""} onClick={()=>goChapter(index)} aria-label={`Глава ${index+1}`}/>)}</div>
    </section>
  </div>;
}

function QuantityControl({ quantity, setQuantity, label = "Количество" }: { quantity:number; setQuantity:(quantity:number)=>void; label?:string }) {
  return <div className="quantity-control" aria-label={label}><button onClick={(event)=>{event.stopPropagation();setQuantity(Math.max(1,quantity-1))}} aria-label="Уменьшить количество"><Icon name="minus"/></button><span>{quantity}</span><button onClick={(event)=>{event.stopPropagation();setQuantity(quantity+1)}} aria-label="Увеличить количество"><Icon name="plus"/></button></div>;
}

function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify,unavailableLast=true,unavailableSizes=[],oldPrice}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void;unavailableLast?:boolean;unavailableSizes?:string[];oldPrice?:number}){
  const [notifySize,setNotifySize]=useState("");
  const [notifyEmail,setNotifyEmail]=useState("");
  const submitNotify=(event:React.FormEvent<HTMLFormElement>,name:string)=>{
    event.preventDefault();
    if(!notifyEmail.trim())return;
    notify(name);
    setNotifySize("");
    setNotifyEmail("");
  };
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{
    const unavailable=unavailableSizes.includes(name)||(unavailableLast&&index===sizes.length-1);
    return <div key={name} className={`size-row ${selectedSize===name&&!unavailable?"active":""} ${unavailable?"unavailable":""}`}>
      <button disabled={unavailable} onClick={()=>{if(!unavailable){setSelectedSize(name);setQuantity(1)}}}><span>{name}</span>{selectedSize!==name&&!unavailable&&<b><span>{fmt(price)}</span>{oldPrice&&oldPrice>price&&<del>{fmt(oldPrice)}</del>}</b>}</button>
      {unavailable?<div className="stock-actions"><span>НЕТ В НАЛИЧИИ</span><button type="button" onClick={()=>setNotifySize(current=>current===name?"":name)} aria-label={`Сообщить о поступлении размера ${name}`}><Icon name="mail"/></button></div>:selectedSize===name?<QuantityControl quantity={quantity} setQuantity={setQuantity}/>:null}
      {unavailable&&notifySize===name&&<form className="stock-notify-form" onSubmit={(event)=>submitNotify(event,name)}><label htmlFor={`stock-email-${name}`}>Сообщить о поступлении</label><div><input id={`stock-email-${name}`} type="email" required placeholder="Ваш email" value={notifyEmail} onChange={event=>setNotifyEmail(event.target.value)}/><button type="submit">СООБЩИТЬ</button></div></form>}
    </div>;
  })}</div>;
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
  const unavailableSizes=getUnavailableProductSizes(product,color.name,sizes);
  const autoSize=sizes.length===1&&isProductSizeAvailable(product,color.name,sizes[0][0])?sizes[0][0]:"";
  const effectiveSelectedSize=selectedSize||autoSize;
  const sku=effectiveSelectedSize?findProductSku(product,color.name,effectiveSelectedSize):undefined;
  const mediaSku=findProductSku(product,color.name);
  const gallery=mediaSku?[mediaSku.image,...mediaSku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const unitPrice=sku?.price??sizes.find(([name])=>name===selectedSize)?.[1]??sizes[0]?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize:effectiveSelectedSize,selectedSkuId:sku?.id,quantity};
  const specs=sku??mediaSku??product.skus?.[0];
  const needsSize=Boolean(sizes.length&&!effectiveSelectedSize);
  const selectedUnavailable=Boolean(effectiveSelectedSize&&!isProductSizeAvailable(product,color.name,effectiveSelectedSize));
  const knownUnitPrice=priceKnown(unitPrice);
  const handlePurchase=()=>{if(needsSize||selectedUnavailable||!knownUnitPrice)return;add(selectedProduct)};
  return <div className={`product-page page ${product.hasRichContent?"has-rich":"standard-pdp"}`}><div className="crumbs">Главная / Домашний текстиль / {product.name}</div><div className={`pdp-grid ${product.hasRichContent?"without-thumbs":""}`}>{!product.hasRichContent&&<div className="thumbs">{gallery.map((src,n)=><button key={src} className={n===activeImage?"active":""} onClick={()=>{setActiveImage(n);if(typeof window!=="undefined"&&window.matchMedia("(min-width: 901px)").matches){document.querySelector(`[data-pdp-image-index="${n}"]`)?.scrollIntoView({behavior:"smooth",block:"start"})}}} aria-label={`Фото товара ${n+1}`}><RemoteImage src={src} alt=""/></button>)}</div>}<div className="pdp-main"><ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/></div><div className="pdp-info">{product.badge&&<small className="badge">{product.badge}</small>}<div className="pdp-title"><h1>{product.name}</h1><div><button onClick={()=>favorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button><button onClick={()=>navigator.clipboard?.writeText(location.href)} aria-label="Поделиться"><Icon name="share"/></button></div></div><div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{knownUnitPrice?(sizes.length>1&&!selectedSize?`от ${fmt(unitPrice)}`:fmt(unitPrice)):"Цена уточняется"}</strong>{knownUnitPrice&&product.oldPrice&&<><del>{sizes.length>1&&!selectedSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: {product.article??`KD-PD-${1020+product.id}`}</small><label className="pdp-color-label">Цвет: {color.name}</label>{variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}<p className="pdp-description">Предмет создан в традиции русского гостеприимства: благородная палитра, точная отделка и материалы, которые красиво живут в доме годами.</p><label className="pdp-size-head"><span>РАЗМЕР</span><button onClick={()=>alert(sizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button></label><ProductSizeRows sizes={sizes} selectedSize={effectiveSelectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/><button className={`primary purchase-cta total-cta ${needsSize||selectedUnavailable||!knownUnitPrice?"needs-size":"ready-to-add"}`} disabled={needsSize||selectedUnavailable||!knownUnitPrice} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{selectedUnavailable?"НЕТ В НАЛИЧИИ":!knownUnitPrice?"ЦЕНА УТОЧНЯЕТСЯ":needsSize?"ВЫБРАТЬ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&!selectedUnavailable&&knownUnitPrice&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>setStoresOpen(true)} aria-label="Показать наличие в бутиках"><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button><div className="pdp-accordions">{[
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

function productMerchGroup(item:Product){
  const preferred=findProductSku(item,item.selectedColor,item.selectedSize);
  const rows=preferred?[preferred,...(item.skus??[]).filter(sku=>sku.id!==preferred.id)]:(item.skus??[]);
  for(const row of rows){
    const value=(row.collection??row.capsule)?.trim();
    if(value)return value.toLocaleLowerCase("ru-RU");
  }
  return "";
}

function productFamily(item:Product){
  const value=`${item.name} ${item.note}`.toLowerCase();
  if(/комплект|постель|пододеяль|простын|наволоч/.test(value))return "bedding";
  if(/подуш/.test(value))return "pillow";
  if(/плед|покрывал|одеял/.test(value))return "throw";
  if(/тарел|салатник|сервиз|чайная пара|чаш|бокал|стакан|графин|прибор/.test(value))return "table";
  if(/свеч|аромат|ваза|декор|плейсмат/.test(value))return "decor";
  if(/халат|пижам|сороч|домашн.*одежд/.test(value))return "homewear";
  return "other";
}

const complementaryPreferences:Record<string,string[]>={
  bedding:["pillow","throw","decor"],
  pillow:["bedding","throw","decor"],
  throw:["pillow","bedding","decor"],
  table:["table","decor"],
  decor:["table","bedding","pillow"],
  homewear:["bedding","decor"],
  other:["decor","table","pillow","throw"],
};

function getCollectionRecommendations(product:Product,limit=4){
  const currentMerchGroup=productMerchGroup(product);
  const editorialGroup=editorials.find(item=>item.productIds.includes(product.id));
  if(currentMerchGroup){
    return products.filter(item=>item.id!==product.id&&productMerchGroup(item)===currentMerchGroup).slice(0,limit);
  }
  if(editorialGroup){
    return editorialGroup.productIds
      .filter(id=>id!==product.id)
      .map(id=>products.find(item=>item.id===id))
      .filter((item):item is Product=>Boolean(item))
      .slice(0,limit);
  }
  return [];
}

function getComplementaryRecommendations(product:Product,limit=4){
  const collectionProducts=getCollectionRecommendations(product,12);
  const preferredFamilies=complementaryPreferences[productFamily(product)]??complementaryPreferences.other;
  const excludedIds=new Set([product.id,...collectionProducts.map(item=>item.id)]);
  return products
    .filter(item=>!excludedIds.has(item.id))
    .map(item=>({item,rank:preferredFamilies.indexOf(productFamily(item))}))
    .filter(entry=>entry.rank>=0)
    .sort((a,b)=>a.rank-b.rank||Number(Boolean(b.item.badge))-Number(Boolean(a.item.badge))||a.item.id-b.item.id)
    .map(entry=>entry.item)
    .slice(0,limit);
}

function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  void recentlyViewed;
  const collectionProducts=getCollectionRecommendations(product,4);
  const complementaryProducts=getComplementaryRecommendations(product,4);

  return <>
    {collectionProducts.length>0&&<section className="post-rich-recommendations collection-recommendations"><div className="section-head"><p>КОЛЛЕКЦИЯ / КАПСУЛА</p><h2>Товары из этой коллекции</h2></div><ProductRail className="recommendation-product-rail" items={collectionProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
    {complementaryProducts.length>0&&<section className="post-rich-recommendations complementary-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ПОДОБРАНО К ЭТОМУ ТОВАРУ</p><h2>Дополните образ</h2></div><ProductRail className="recommendation-product-rail" items={complementaryProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
  </>;
}

function Menu({ current, setCurrent, close, go, openCatalog }: { current:string; setCurrent:(s:string)=>void; close:()=>void; go:(v:View)=>void; openCatalog:(category?:string)=>void }) {
  const catalogSections=["Спальня","Кухня и столовая","Декор","Ванная","Одежда для дома"];
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
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;

  return <div className="overlay navigation-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><aside className="menu-panel zara-menu premium-menu"><div className="menu-top"><button onClick={close} aria-label="Закрыть меню"><Icon name="close"/></button><span><Icon name="pin"/> Бутики</span><b>КУЛЬТУРА ДОМА</b></div><div className="menu-body">{!current?<div className="menu-first level-one premium-menu-root">
    <button className="premium-menu-new" onClick={()=>openCatalog("Все товары")}><span>НОВИНКИ</span><Icon name="arrow"/></button>

    <section className="premium-menu-editorial" aria-label="Editorial и готовые решения">
      <small>EDITORIAL</small>
      <button type="button" onClick={()=>go("collections")}><span>КОЛЛЕКЦИИ</span><Icon name="arrow"/></button>
      <a href={constructorHref} onClick={close}><span>ГОТОВЫЕ РЕШЕНИЯ</span><Icon name="arrow"/></a>
    </section>

    <nav className="premium-menu-catalog" aria-label="Каталог">{catalogSections.map(x=><button key={x} onClick={()=>setCurrent(x)}><span>{x}</span><Icon name="chevron"/></button>)}</nav>

    <div className="premium-menu-service">
      <button onClick={()=>setCurrent("Идеи подарков")}><span>ИДЕИ ПОДАРКОВ</span><Icon name="chevron"/></button>
      <button className="premium-menu-certificate" onClick={()=>alert("Электронный сертификат доступен от 3 000 ₽")}><span>ПОДАРОЧНЫЙ СЕРТИФИКАТ</span></button>
    </div>

    <div className="premium-menu-commercial">
      <button className="sale" onClick={()=>setCurrent("РАСПРОДАЖА")}><span>РАСПРОДАЖА</span><Icon name="chevron"/></button>
      <button onClick={()=>setCurrent("Аутлет")}><span>АУТЛЕТ</span><Icon name="chevron"/></button>
    </div>
  </div>:<div className="menu-second level-two premium-menu-level-two" key={current}><button className="menu-back" onClick={()=>setCurrent("")}><Icon name="chevron"/><span>{current}</span></button>{list.map((x,i)=><button key={x} className={i===0?"view-all":""} onClick={()=>openCatalog(i===0?(catalogMap[current]??"Все товары"):(subcategoryMap[x]??catalogMap[current]??"Все товары"))}><span>{x}</span>{i===0&&<Icon name="arrow"/>}</button>)}<div className="premium-menu-level-footer"><button onClick={()=>openCatalog(catalogMap[current]??"Все товары")}>ЛИДЕРЫ ПРОДАЖ</button></div></div>}</div></aside></div>;
}

function Search({ close, choose }: { close:()=>void; choose:(p:Product)=>void }) { const [q,setQ]=useState(""); const result=products.filter(p=>p.name.toLowerCase().includes(q.toLowerCase())); return <div className="overlay"><button className="overlay-bg" onClick={close}/><div className="search-panel"><div><Icon name="search"/><input autoFocus placeholder="Поиск по каталогу" value={q} onChange={e=>setQ(e.target.value)}/><button onClick={close} aria-label="Закрыть поиск"><Icon name="close"/></button></div><p>{q?`Найдено: ${result.length}`:"Популярные запросы: постельное бельё, посуда, подарки"}</p>{q&&<div className="search-results">{result.map(p=><button key={p.id} onClick={()=>choose(p)}><ScrollableProductMedia product={p} alt={p.name} className="search-item-media"/><span>{p.name}<b>{priceKnown(p.price)?fmt(p.price):"Цена уточняется"}</b></span></button>)}</div>}</div></div> }

const KD_CITY_SUGGESTIONS=["Москва","Санкт-Петербург","Казань","Екатеринбург","Новосибирск","Омск","Нижний Новгород","Самара","Ростов-на-Дону","Краснодар"];
const KD_ADDRESS_SUGGESTIONS:Record<string,string[]>={
  "Москва":["ул. Петровка, 12","Тверская ул., 18","Большая Дмитровка ул., 9","Ленинградский проспект, 36","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Большая Конюшенная ул., 15","Литейный проспект, 24","Московский проспект, 73"],
  "Казань":["ул. Баумана, 44","ул. Пушкина, 17","проспект Ямашева, 46"],
  "Екатеринбург":["проспект Ленина, 25","ул. Малышева, 51","ул. Вайнера, 10"],
  "Новосибирск":["Красный проспект, 50","ул. Ленина, 12","ул. Советская, 35"],
  "Омск":["ул. Ленина, 20","проспект Карла Маркса, 24","ул. Гагарина, 8"],
  "Нижний Новгород":["Большая Покровская ул., 28","ул. Белинского, 61"],
  "Самара":["Ленинградская ул., 38","Московское шоссе, 17"],
  "Ростов-на-Дону":["Большая Садовая ул., 65","проспект Будённовский, 32"],
  "Краснодар":["Красная ул., 74","Северная ул., 324"],
};
const KD_PVZ_POINTS:Record<string,string[]>={
  "Москва":["Петровка, 12","Тверская, 18","Кутузовский проспект, 22"],
  "Санкт-Петербург":["Невский проспект, 28","Московский проспект, 73"],
  "Казань":["Баумана, 44","Ямашева, 46"],
  "Екатеринбург":["Ленина, 25","Малышева, 51"],
  "Новосибирск":["Красный проспект, 50","Ленина, 12"],
  "Омск":["Ленина, 20","Карла Маркса, 24"],
  "Нижний Новгород":["Большая Покровская, 28","Белинского, 61"],
  "Самара":["Ленинградская, 38","Московское шоссе, 17"],
  "Ростов-на-Дону":["Большая Садовая, 65","Будённовский, 32"],
  "Краснодар":["Красная, 74","Северная, 324"],
};

function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const query=value.trim().toLowerCase();
  const items=KD_CITY_SUGGESTIONS.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);
  return <label className="v43-field v43-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="address-level2" aria-autocomplete="list" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить город"/>{open&&items.length>0&&<div className="v43-suggestions" role="listbox">{items.map(city=><button type="button" key={city} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(city);setOpen(false)}}>{city}</button>)}</div>}</label>;
}

function AddressSuggestField({city,value,onChange,label="Улица и дом",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const source=KD_ADDRESS_SUGGESTIONS[city]??[];
  const query=value.trim().toLowerCase();
  const items=source.filter(address=>!query||address.toLowerCase().includes(query)).slice(0,6);
  return <label className="v43-field v43-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="street-address" aria-autocomplete="list" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить адрес"/>{open&&items.length>0&&<div className="v43-suggestions" role="listbox">{items.map(address=><button type="button" key={address} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(address);setOpen(false)}}><b>{address}</b><small>{city}</small></button>)}</div>}</label>;
}

type AccountV43Section="overview"|"orders"|"addresses"|"personal"|"bonuses";

function Account({ profile, close, notice, save, logout }: { profile:Profile|null; close:()=>void; notice:(s:string)=>void; save:(profile:Profile)=>void; logout:()=>void }) {
  // AUTH_FLOW_V20
  // COMMERCE_CLARITY_V43
  type AuthMethod="phone"|"email";
  type AuthStep="identify"|"code"|"register";
  const blank:Profile={name:"",surname:"",email:"",phone:"",city:"Москва",address:""};
  const initialMethod:AuthMethod=profile?.phone?"phone":"email";
  const [mode,setMode]=useState<"auth"|"profile">(profile?"profile":"auth");
  const [method,setMethod]=useState<AuthMethod>(initialMethod);
  const [step,setStep]=useState<AuthStep>("identify");
  const [identifier,setIdentifier]=useState(profile?(initialMethod==="phone"?profile.phone:profile.email):"");
  const [code,setCode]=useState("");
  const [draft,setDraft]=useState<Profile>(profile??blank);
  const [section,setSection]=useState<AccountV43Section>("overview");
  const [updates,setUpdates]=useState(true);

  useEffect(()=>{if(profile){setDraft(profile);setMode("profile")}},[profile]);

  const cleanPhone=(value:string)=>value.replace(/\D/g,"");
  const validEmail=(value:string)=>value.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
  const validPhone=(value:string)=>cleanPhone(value).length>=10;
  const contactValid=method==="email"?/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(identifier.trim()):validPhone(identifier);
  const switchMethod=(next:AuthMethod)=>{setMethod(next);setIdentifier(next==="email"?(profile?.email??""):(profile?.phone??""));setCode("");setStep("identify")};
  const requestCode=()=>{if(!contactValid){notice(method==="email"?"Введите корректный email":"Введите корректный номер телефона");return}setCode("");setStep("code");notice(method==="phone"?"Демо-код из SMS — 1234":"Демо-код из письма — 1234")};
  const verifyCode=()=>{if(code.trim()!=="1234"){notice("Неверный код. Для демо используйте 1234");return}const sameProfile=Boolean(profile&&(method==="email"?profile.email.trim().toLowerCase()===identifier.trim().toLowerCase():cleanPhone(profile.phone)===cleanPhone(identifier)));if(sameProfile&&profile){setDraft(profile);setMode("profile");setSection("overview");setStep("identify");notice("Вход выполнен");return}setDraft(current=>({...current,[method==="email"?"email":"phone"]:identifier.trim()}));setStep("register")};
  const register=()=>{const next={...draft,[method==="email"?"email":"phone"]:identifier.trim()};if(!next.name.trim()){notice("Введите имя");return}save(next);setDraft(next);setMode("profile");setSection("overview");setStep("identify");notice("Аккаунт создан")};
  const savePersonal=()=>{if(!draft.name.trim()){notice("Введите имя");return}if(!validEmail(draft.email)){notice("Проверьте email");return}if(draft.phone&&!validPhone(draft.phone)){notice("Проверьте номер телефона");return}save(draft);notice("Личные данные сохранены")};
  const saveAddress=()=>{if(!draft.city.trim()||!draft.address.trim()){notice("Укажите город и адрес");return}save(draft);notice("Адрес сохранён")};
  const signOut=()=>{logout();setDraft(blank);setIdentifier("");setCode("");setStep("identify");setMode("auth");setSection("overview");notice("Вы вышли из аккаунта")};
  const nav:[AccountV43Section,string][]=[["overview","Обзор"],["orders","Заказы"],["addresses","Адреса"],["personal","Личные данные"],["bonuses","Бонусы"]];

  return <div className="overlay auth-overlay account-v43-overlay" data-analytics-step="account_open"><button className="overlay-bg" onClick={close} aria-label="Закрыть личный кабинет"/><aside className={`side-panel account auth-v20 account-v43 ${mode==="profile"?"is-profile":"is-auth"}`} role="dialog" aria-modal="true" aria-label="Личный кабинет">
    <header className="account-v43-head"><button className="account-v43-back" type="button" onClick={close}>← <span>Вернуться</span></button><b>КУЛЬТУРА ДОМА</b><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {mode==="profile"?<div className="account-v43-shell">
      <aside className="account-v43-nav"><div className="account-v43-person"><span>{(draft.name||"К").slice(0,1).toUpperCase()}</span><div><small>ЛИЧНЫЙ КАБИНЕТ</small><strong>{[draft.name,draft.surname].filter(Boolean).join(" ")||"Профиль"}</strong></div></div><nav>{nav.map(([key,label])=><button type="button" key={key} className={section===key?"active":""} onClick={()=>setSection(key)}>{label}<span>→</span></button>)}</nav><button type="button" className="account-v43-signout" onClick={signOut}>Выйти</button></aside>
      <main className="account-v43-main">
        <nav className="account-v43-mobile-nav" aria-label="Разделы личного кабинета">{nav.map(([key,label])=><button type="button" key={key} className={section===key?"active":""} onClick={()=>setSection(key)}>{label}</button>)}</nav>
        {section==="overview"&&<section className="account-v43-view"><header className="account-v43-title"><small>ОБЗОР</small><h1>{draft.name?`Здравствуйте, ${draft.name}`:"Личный кабинет"}</h1><p>Самое важное — заказы, адрес и бонусы — на одном экране.</p></header><div className="account-v43-overview-grid"><button type="button" onClick={()=>setSection("orders")}><small>ЗАКАЗЫ</small><strong>Нет активных</strong><span>Следить за статусом →</span></button><button type="button" onClick={()=>setSection("bonuses")}><small>БОНУСЫ</small><strong>0 бонусов</strong><span>Подробнее →</span></button><button type="button" className="wide" onClick={()=>setSection("addresses")}><small>ОСНОВНОЙ АДРЕС</small><strong>{draft.address?`${draft.city}, ${draft.address}`:"Адрес не добавлен"}</strong><span>{draft.address?"Изменить":"Добавить адрес"} →</span></button></div><section className="account-v43-note"><div><small>БЫСТРОЕ ОФОРМЛЕНИЕ</small><h2>Данные подставятся автоматически</h2></div><p>Имя, телефон и основной адрес будут заполнены в checkout. Их можно изменить перед подтверждением заказа.</p></section></section>}
        {section==="orders"&&<section className="account-v43-view"><header className="account-v43-title"><small>МОИ ЗАКАЗЫ</small><h1>Заказы</h1><p>Здесь будут история покупок и актуальный статус доставки.</p></header><div className="account-v43-empty"><span>○</span><h2>Заказов пока нет</h2><p>После оформления появится понятная цепочка: заказ принят → собран → передан курьеру → доставлен.</p><button type="button" className="primary" onClick={close}>ПРОДОЛЖИТЬ ПОКУПКИ</button></div><label className="account-v43-check"><input type="checkbox" checked={updates} onChange={event=>setUpdates(event.target.checked)}/><span>Получать уведомления об изменении статуса заказа</span></label></section>}
        {section==="addresses"&&<section className="account-v43-view"><header className="account-v43-title"><small>ДОСТАВКА</small><h1>Основной адрес</h1><p>Сохранённый адрес автоматически появится при оформлении заказа.</p></header><div className="account-v43-form account-v43-address-form"><CitySuggestField value={draft.city} required onChange={city=>setDraft({...draft,city,address:city===draft.city?draft.address:""})}/><AddressSuggestField city={draft.city} value={draft.address} required onChange={address=>setDraft({...draft,address})}/></div><div className="account-v43-form-actions"><button type="button" className="primary" onClick={saveAddress}>СОХРАНИТЬ АДРЕС</button><button type="button" onClick={()=>setSection("overview")}>Отмена</button></div></section>}
        {section==="personal"&&<section className="account-v43-view"><header className="account-v43-title"><small>ПРОФИЛЬ</small><h1>Личные данные</h1><p>Только данные, необходимые для связи и оформления заказа.</p></header><div className="account-v43-form"><label className="v43-field"><span>Имя *</span><input value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})} autoComplete="given-name"/></label><label className="v43-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})} autoComplete="family-name"/></label><label className="v43-field"><span>Телефон</span><input type="tel" value={draft.phone} onChange={event=>setDraft({...draft,phone:event.target.value})} autoComplete="tel"/></label><label className="v43-field"><span>Email</span><input type="email" value={draft.email} onChange={event=>setDraft({...draft,email:event.target.value})} autoComplete="email"/></label></div><div className="account-v43-form-actions"><button type="button" className="primary" onClick={savePersonal}>СОХРАНИТЬ</button><button type="button" onClick={()=>setSection("overview")}>Отмена</button></div></section>}
        {section==="bonuses"&&<section className="account-v43-view"><header className="account-v43-title"><small>ПРОГРАММА ЛОЯЛЬНОСТИ</small><h1>Бонусы</h1><p>Баланс показывается до оплаты, чтобы им было проще воспользоваться.</p></header><div className="account-v43-balance"><small>ДОСТУПНО</small><strong>0</strong><span>бонусов</span></div><div className="account-v43-info-rows"><div><b>Как начисляются</b><p>Правила начисления будут отображаться здесь после подключения программы лояльности.</p></div><div><b>Как использовать</b><p>Доступные бонусы будут показаны в корзине и на шаге оплаты.</p></div></div></section>}
      </main>
    </div>:<div className="account-v43-auth">
      {step==="identify"&&<><div className="account-v43-auth-title"><small>ЛИЧНЫЙ КАБИНЕТ</small><h1>Войти или создать аккаунт</h1><p>Без пароля — по короткому коду.</p></div><div className="auth-methods" role="tablist"><button type="button" className={method==="phone"?"active":""} onClick={()=>switchMethod("phone")}>Телефон</button><button type="button" className={method==="email"?"active":""} onClick={()=>switchMethod("email")}>Email</button></div><label className="v43-field"><span>{method==="phone"?"Номер телефона":"Email"}</span><input type={method==="phone"?"tel":"email"} value={identifier} onChange={event=>setIdentifier(event.target.value)} autoComplete={method==="phone"?"tel":"email"} placeholder={method==="phone"?"+7 999 000-00-00":"name@example.com"}/></label><button type="button" className="primary account-v43-auth-cta" disabled={!identifier.trim()} onClick={requestCode}>ПОЛУЧИТЬ КОД</button><p className="auth-legal">Продолжая, вы соглашаетесь с обработкой персональных данных.</p></>}
      {step==="code"&&<><button className="account-v43-auth-back" type="button" onClick={()=>setStep("identify")}>← Назад</button><div className="account-v43-auth-title"><small>ПОДТВЕРЖДЕНИЕ</small><h1>Введите код</h1><p>Код отправлен на {method==="phone"?"номер":"email"} <b>{identifier}</b>.</p></div><label className="v43-field"><span>Код</span><input autoFocus inputMode="numeric" maxLength={4} value={code} onChange={event=>setCode(event.target.value.replace(/\D/g,"").slice(0,4))} placeholder="0000"/></label><button type="button" className="primary account-v43-auth-cta" disabled={code.length!==4} onClick={verifyCode}>ПРОДОЛЖИТЬ</button><button type="button" className="account-v43-resend" onClick={requestCode}>Отправить код ещё раз</button><small className="account-v43-demo">Демо-код: 1234</small></>}
      {step==="register"&&<><button className="account-v43-auth-back" type="button" onClick={()=>setStep("code")}>← Назад</button><div className="account-v43-auth-title"><small>НОВЫЙ АККАУНТ</small><h1>Как к вам обращаться?</h1><p>Остальные данные можно заполнить позже.</p></div><label className="v43-field"><span>Имя *</span><input autoFocus value={draft.name} onChange={event=>setDraft({...draft,name:event.target.value})}/></label><label className="v43-field"><span>Фамилия</span><input value={draft.surname} onChange={event=>setDraft({...draft,surname:event.target.value})}/></label><button type="button" className="primary account-v43-auth-cta" disabled={!draft.name.trim()} onClick={register}>СОЗДАТЬ АККАУНТ</button></>}
    </div>}
  </aside></div>;
}

function Favorites({ids,close,remove,choose,quickAdd}:{ids:number[];close:()=>void;remove:(id:number)=>void;choose:(product:Product)=>void;quickAdd:(product:Product)=>void}){
  const items=products.filter(product=>ids.includes(product.id));
  return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel favorites-drawer"><button className="close" onClick={close} aria-label="Закрыть избранное"><Icon name="close"/></button><p>ИЗБРАННОЕ · {items.length}</p>{items.length===0?<div className="empty"><Icon name="heart"/><h2>Сохраните то, что близко</h2><span>Нажимайте на сердце в карточке, чтобы вернуться к предмету позже.</span><button className="primary" onClick={close}>ПРОДОЛЖИТЬ ПОКУПКИ</button></div>:<div className="favorite-list">{items.map(product=><article key={product.id}><button className="favorite-image" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="favorite-item-media"/></button><div><button className="favorite-title" onClick={()=>choose(product)}>{product.name}</button><span>{product.note}</span><b>{fmt(product.price)}</b><button className="secondary" onClick={()=>quickAdd(product)}>ДОБАВИТЬ</button></div><button className="favorite-remove" onClick={()=>remove(product.id)} aria-label={`Удалить ${product.name} из избранного`}><Icon name="close"/></button></article>)}</div>}</aside></div>;
}

function Filters({ close, apply, count }: { close:()=>void; apply:()=>void; count:number }) { return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel filters"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ФИЛЬТРЫ</p>{["Категория","Материал","Цвет","Размер","Цена"].map((x,i)=><details key={x} open={i===0}><summary>{x}<Icon name="plus"/></summary><label><input type="checkbox"/> Постельное бельё</label><label><input type="checkbox"/> Домашний текстиль</label><label><input type="checkbox"/> Посуда и сервировка</label></details>)}<button className="primary" onClick={apply}>ПОКАЗАТЬ {productCountLabel(count).toUpperCase()}</button><button className="link" onClick={close}>СБРОСИТЬ</button></aside></div> }

function PLPSizeFlow({ product, close, add }: { product:Product; close:()=>void; add:(size:string,quantity:number,unitPrice:number)=>void }) {
  const selectedColor=product.selectedColor??product.colorVariants?.[0]?.name;
  const sizes=getProductSizeOptions(product,selectedColor);
  const unavailableSizes=getUnavailableProductSizes(product,selectedColor,sizes);
  const initialSize=sizes.length===1&&isProductSizeAvailable(product,selectedColor,sizes[0][0])?sizes[0][0]:"";
  const [chosenSize,setChosenSize]=useState(initialSize);
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  useEffect(()=>{setChosenSize(initialSize);setQuantity(1)},[product.id,selectedColor,initialSize]);
  const selectedSku=chosenSize?findProductSku(product,selectedColor,chosenSize):undefined;
  const unitPrice=selectedSku?.price??sizes.find(([item])=>item===chosenSize)?.[1]??sizes[0]?.[1]??product.price;
  const discount=discountOf(product);
  const canAdd=Boolean(chosenSize)&&isProductSizeAvailable(product,selectedColor,chosenSize);
  return <div className="overlay plp-flow"><button className="overlay-bg" onClick={close} aria-label="Закрыть выбор размера"/><section className="plp-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}><div className="flow-handle"/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="plp-modal-media"><ScrollableProductMedia product={product} alt={product.name}/></div><div className="plp-modal-info"><small>{product.badge||"КУЛЬТУРА ДОМА"}</small><h2>{product.name}</h2><p className="modal-note">{product.note}</p><div className="modal-price"><b>{sizes.length>1&&!chosenSize?`от ${fmt(sizes[0]?.[1]??product.price)}`:fmt(unitPrice)}</b>{product.oldPrice&&<><del>{sizes.length>1&&!chosenSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</div><p className="quick-color">Цвет: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p><p className="quick-description">Предмет создан в русской декоративной традиции: ясная форма, благородный цвет и точная отделка.</p><button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/><button className={`primary total-cta ${canAdd?"ready-to-add":"choose-size-disabled"}`} disabled={!canAdd} onClick={()=>canAdd&&add(chosenSize,quantity,unitPrice)}><span>{canAdd?"ДОБАВИТЬ В КОРЗИНУ":"ВЫБРАТЬ РАЗМЕР"}</span>{canAdd&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>
}

function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize)??product.skus?.[0];
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Размер</dt><dd>{sku?.size??product.note}</dd></div>{sku&&<><div><dt>Высота</dt><dd>{sku.height}</dd></div><div><dt>Ширина</dt><dd>{sku.width}</dd></div></>}</dl></section><section><h2>МАТЕРИАЛ И СОСТАВ</h2><h3>{sku?.material??"Материал"}</h3><p>{sku?.composition??"Информация указана в характеристиках товара."}</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}

function isGiftPackagingAvailable(product:Product){
  const inEditorial=editorials.some(item=>item.productIds.includes(product.id));
  const merchandisingTagged=Boolean(product.skus?.some(sku=>Boolean(sku.collection?.trim()||sku.capsule?.trim())));
  const beddingSet=/^Комплект\b/i.test(product.name);
  return product.giftPackagingAvailable===true||inEditorial||merchandisingTagged||beddingSet;
}

function PLPAdded({product,close,openCart,updateGift,selectProduct}:{product:CartItem;close:()=>void;openCart:()=>void;updateGift:(giftWrap:boolean)=>void;selectProduct:(product:Product)=>void}){
  const giftAvailable=isGiftPackagingAvailable(product);
  const complementaryProducts=getComplementaryRecommendations(product,4);
  const [giftWrap,setGiftWrap]=useState(Boolean(product.giftWrap));
  const toggleWrap=(checked:boolean)=>{setGiftWrap(checked);updateGift(checked)};
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><ScrollableProductMedia product={product} alt={product.name} className="added-product-media"/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div>{giftAvailable&&<section className="added-gift-flow" aria-label="Подарочное оформление"><div className="added-gift-head"><div><strong>Оформить как подарок</strong><small>Для этого товара доступна фирменная подарочная упаковка.</small></div></div><label className="added-gift-option"><input type="checkbox" checked={giftWrap} onChange={event=>toggleWrap(event.target.checked)}/><span><b>Добавить подарочную упаковку</b><small>Фирменная упаковка «Культура дома»</small></span></label></section>}{complementaryProducts.length>0&&<section className="added-complementary" aria-label="Дополните образ"><div className="added-complementary-head"><small>ПОДОБРАНО К ТОВАРУ</small><h3>Дополните образ</h3></div><div className="added-complementary-rail">{complementaryProducts.map(item=><button key={item.id} type="button" className="added-complementary-card" onClick={()=>selectProduct(item)}><RemoteImage src={item.image} alt={item.name}/><span><strong>{item.name}</strong><small>{item.note}</small><b>{priceKnown(item.price)?fmt(item.price):"Цена уточняется"}</b></span></button>)}</div></section>}<aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}

function SizeSheet({ size, setSize, close, add, price }: { size:string; setSize:(s:string)=>void; close:()=>void; add:(quantity:number,unitPrice:number)=>void; price:number }) {
  const [quantity,setQuantity]=useState(1);
  const sizes=[["Евро 200×220",price],["Семейный 150×200",price+2000],["Кинг Сайз 220×240",price+2000]] as const;
  const unitPrice=sizes.find(([item])=>item===size)?.[1]??price;
  return <div className="overlay mobile-overlay"><button className="overlay-bg" onClick={close}/><aside className="size-sheet"><i/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="sheet-head"><span>РАЗМЕР</span><button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Руководство по размерам</button></div><ProductSizeRows sizes={sizes} selectedSize={size} setSelectedSize={setSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary total-cta" onClick={()=>add(quantity,unitPrice)}><span>ДОБАВИТЬ В КОРЗИНУ</span><b>{fmt(unitPrice*quantity)}</b></button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></aside></div>
}

function Cart({ cart, profile, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; profile:Profile|null; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const courierShipping=total>=15000?0:300;
  const courierTotal=total+courierShipping;
  const deliveryLeft=Math.max(0,15000-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/15000*100));
  const seedWords=(cart[0]?.name??"").toLowerCase().split(/[^а-яёa-z0-9]+/i).filter(word=>word.length>4).filter(word=>!["комплект","декоративная","постельного","культура","товара"].includes(word));
  const scored=products.filter(product=>!cart.some(item=>item.id===product.id)).map(product=>({product,score:seedWords.reduce((score,word)=>score+(product.name.toLowerCase().includes(word)?2:0),0)})).sort((a,b)=>b.score-a.score);
  const relatedItems=Array.from(new Map(scored.filter(row=>row.score>0).map(row=>[row.product.name,row.product])).values()).slice(0,4);
  const suggestions=relatedItems.length?relatedItems:recentItems.filter(product=>!cart.some(item=>item.id===product.id)).slice(0,4);

  return <div className="overlay cart-v43-overlay" data-analytics-step="cart_open"><aside className="cart-v43" role="dialog" aria-modal="true" aria-label="Корзина">
    <header className="cart-v43-head"><button type="button" onClick={go}>← <span>Продолжить покупки</span></button><b>КУЛЬТУРА ДОМА</b><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {cart.length===0?<main className="cart-v43-empty"><small>КОРЗИНА</small><h1>Здесь пока пусто</h1><p>Добавьте предметы из каталога или вернитесь к недавно просмотренным.</p>{recentItems.length>0&&<section><h2>Недавно просмотренные</h2><div>{recentItems.map(product=><button type="button" key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><span>{product.name}</span><b>{fmt(product.price)}</b></button>)}</div></section>}<button type="button" className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></main>:<main className="cart-v43-layout">
      <section className="cart-v43-content"><header className="cart-v43-title"><small>КОРЗИНА</small><h1>Ваш выбор <span>{itemCount}</span></h1><p>Проверьте количество и упаковку. Размер и цвет остаются такими, как вы выбрали.</p></header>
        <div className="cart-v43-delivery"><div><b>{courierShipping===0?"Бесплатная доставка":"До бесплатной доставки — "+fmt(deliveryLeft)}</b><span>{courierShipping===0?"Для курьера и ПВЗ":"Курьер — 300 ₽ · ПВЗ — бесплатно"}</span></div><i><b style={{width:`${deliveryProgress}%`}}/></i></div>
        <div className="cart-v43-items">{cart.map((item,index)=><article className="cart-v43-item" key={`${item.id}-${index}`}><button className="cart-v43-media" type="button" onClick={()=>choose(item)}><ScrollableProductMedia product={item} alt={item.name} className="cart-item-media"/></button><div className="cart-v43-copy"><div className="cart-v43-item-head"><button type="button" onClick={()=>choose(item)}>{item.name}</button><b>{fmt(item.price*item.quantity)}</b></div><div className="cart-v43-meta"><span>Цвет: {item.selectedColor}</span><span>Размер: {item.selectedSize}</span></div>{isGiftPackagingAvailable(item)&&<label className="cart-v43-gift"><input type="checkbox" checked={Boolean(item.giftWrap)} onChange={event=>update(index,{giftWrap:event.target.checked})}/><span>Подарочная упаковка</span></label>}<div className="cart-v43-actions"><QuantityControl quantity={item.quantity} setQuantity={quantity=>update(index,{quantity})}/><button type="button" onClick={()=>remove(index)}>Удалить</button></div></div></article>)}</div>
        {suggestions.length>0&&<section className="cart-v43-crosssell"><header><small>ДОПОЛНИТЕ КОМПЛЕКТ</small><h2>Может подойти к вашему выбору</h2></header><div>{suggestions.map(product=><article key={product.id}><button className="cart-v43-cross-media" type="button" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/></button><button className="cart-v43-cross-name" type="button" onClick={()=>choose(product)}>{product.name}</button><b>{fmt(product.price)}</b><button className="cart-v43-cross-add" type="button" onClick={()=>quickAdd(product)}>Добавить</button></article>)}</div></section>}
      </section>
      <aside className="cart-v43-summary"><div className="cart-v43-summary-inner"><small>ИТОГ ЗАКАЗА</small><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Курьер</dt><dd>{courierShipping===0?"Бесплатно":fmt(courierShipping)}</dd></div><div><dt>Пункт выдачи</dt><dd>Бесплатно</dd></div></dl><div className="cart-v43-total"><span>Итого при курьере</span><b>{fmt(courierTotal)}</b></div><p>На следующем шаге можно выбрать бесплатный ПВЗ. Итог обновится до подтверждения заказа.</p>{profile?<div className="cart-v43-bonus"><span>Ваш баланс</span><b>0 бонусов</b></div>:<div className="cart-v43-bonus"><span>Бонусы</span><b>Войдите, чтобы увидеть баланс</b></div>}<button type="button" className="primary cart-v43-checkout" data-analytics-step="checkout_start" onClick={checkout}>ПЕРЕЙТИ К ОФОРМЛЕНИЮ</button><div className="cart-v43-trust"><span>✓ Безопасная оплата</span><span>✓ Итог до подтверждения</span></div></div></aside>
    </main>}
  </aside></div>;
}

function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type CheckoutStep=1|2|3;
  type PaymentMethod="card"|"sbp"|"upon";
  const [step,setStep]=useState<CheckoutStep>(1);
  const [delivery,setDelivery]=useState<"courier"|"pickup">("courier");
  const [payment,setPayment]=useState<PaymentMethod|null>(null);
  const [slot,setSlot]=useState("18:00–22:00");
  const [agreed,setAgreed]=useState(true);
  const [notifications,setNotifications]=useState(true);
  const [promoOpen,setPromoOpen]=useState(false);
  const [promo,setPromo]=useState("");
  const [promoStatus,setPromoStatus]=useState("");
  const [pickupPoint,setPickupPoint]=useState("");
  const [access,setAccess]=useState("");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [contactAttempted,setContactAttempted]=useState(false);
  const [deliveryAttempted,setDeliveryAttempted]=useState(false);
  const shellRef=useRef<HTMLDivElement>(null);

  useEffect(()=>{shellRef.current?.scrollTo({top:0,behavior:"smooth"})},[step]);

  const shipping=delivery==="pickup"||total>=15000?0:300;
  const online=payment==="card"||payment==="sbp";
  const onlineDiscount=online?Math.round(total*.03):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const expensive=payable>=30000;
  const pvz=KD_PVZ_POINTS[form.city]??[];
  const phoneDigits=form.phone.replace(/\D/g,"");
  const phoneOk=phoneDigits.length>=10&&(profile?phoneVerified:Boolean(phoneVerified));
  const emailOk=form.email.trim()===""||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const contactOk=form.name.trim().length>0&&phoneOk&&emailOk;
  const deliveryOk=delivery==="courier"?(form.city.trim().length>0&&form.address.trim().length>3):(form.city.trim().length>0&&pickupPoint.length>0);
  const paymentOk=payment!==null;
  const canSubmit=contactOk&&deliveryOk&&paymentOk&&agreed;
  const requestPhoneCode=()=>{if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}setCodeSent(true);setPhoneCode("");setOtpError("")};
  const verifyPhone=()=>{if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}else setOtpError("Неверный код. Для демо используйте 1234")};
  const applyPromo=()=>setPromoStatus(promo.trim()?"Код принят для проверки":"Введите промокод");
  const field=(key:keyof Profile)=>(event:React.ChangeEvent<HTMLInputElement>)=>setForm({...form,[key]:event.target.value});
  const nextFromContacts=()=>{setContactAttempted(true);if(contactOk)setStep(2)};
  const nextFromDelivery=()=>{setDeliveryAttempted(true);if(deliveryOk)setStep(3)};
  const setPhone=(value:string)=>{setForm({...form,phone:value});setPhoneVerified(Boolean(profile?.phone&&value===profile.phone));setCodeSent(false);setOtpError("")};
  const stepLabel=(value:CheckoutStep)=>value===1?"Контакты":value===2?"Доставка":"Оплата";

  return <div className="checkout checkout-v43" ref={shellRef} data-analytics-step="checkout_view">
    <header className="checkout-v43-head"><button type="button" onClick={step===1?close:()=>setStep((step-1) as CheckoutStep)}>← <span>{step===1?"Вернуться":"Назад"}</span></button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    <nav className="checkout-v43-progress" aria-label="Шаги оформления">{([1,2,3] as CheckoutStep[]).map(value=><button type="button" key={value} className={`${step===value?"active":""} ${step>value?"done":""}`} onClick={()=>{if(value<step)setStep(value)}}><i>{step>value?"✓":value}</i><span>{stepLabel(value)}</span></button>)}</nav>
    <form className="checkout-v43-layout" onSubmit={event=>{event.preventDefault();if(canSubmit)submit()}}>
      <main className="checkout-v43-content">
        {step===1&&<section className="checkout-v43-step" data-analytics-step="checkout_contacts"><header><small>ШАГ 1 ИЗ 3</small><h1>Контактные данные</h1><p>{profile?"Мы подставили данные из профиля. Проверьте их перед продолжением.":"Оформить можно без регистрации. Номер подтверждаем коротким кодом, чтобы избежать ошибочных заказов."}</p></header><div className="checkout-v43-fields"><label className="v43-field"><span>Имя *</span><input value={form.name} onChange={field("name")} autoComplete="given-name" name="name" placeholder="Имя"/></label><label className="v43-field"><span>Фамилия</span><input value={form.surname} onChange={field("surname")} autoComplete="family-name" name="surname" placeholder="Необязательно"/></label><label className="v43-field checkout-v43-phone"><span>Телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} autoComplete="tel" inputMode="tel" name="phone" placeholder="+7 999 000-00-00"/>{phoneDigits.length>=10&&!phoneVerified&&<button type="button" onClick={requestPhoneCode}>Подтвердить</button>}{phoneVerified&&<b>✓ Подтверждён</b>}</div></label><label className="v43-field"><span>Email</span><input type="email" value={form.email} onChange={field("email")} autoComplete="email" name="email" placeholder="Для чека и статусов"/></label>{codeSent&&!phoneVerified&&<div className="checkout-v43-otp"><div><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></div><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}</div>{contactAttempted&&!contactOk&&<div className="checkout-v43-inline-error" role="alert">{!form.name.trim()?"Укажите имя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите телефон. ":""}{!emailOk?"Проверьте email.":""}</div>}<button type="button" className="primary checkout-v43-next" onClick={nextFromContacts}>ПРОДОЛЖИТЬ К ДОСТАВКЕ</button></section>}

        {step===2&&<section className="checkout-v43-step" data-analytics-step="checkout_delivery"><header><small>ШАГ 2 ИЗ 3</small><h1>Как доставить заказ?</h1><p>Стоимость и способ доставки выбираются до оплаты.</p></header><div className="checkout-v43-delivery-methods"><button type="button" className={delivery==="courier"?"active":""} onClick={()=>setDelivery("courier")}><i/><div><b>Курьер</b><span>{total>=15000?"Бесплатно":"300 ₽"}</span><small>До двери</small></div></button><button type="button" className={delivery==="pickup"?"active":""} onClick={()=>setDelivery("pickup")}><i/><div><b>Пункт выдачи</b><span>Бесплатно</span><small>Выберите удобный адрес</small></div></button></div><div className="checkout-v43-address"><CitySuggestField value={form.city} required onChange={city=>{setForm({...form,city,address:city===form.city?form.address:""});setPickupPoint("")}}/>{delivery==="courier"?<><AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm({...form,address})}/><label className="v43-field"><span>Квартира, подъезд, домофон</span><input value={access} onChange={event=>setAccess(event.target.value)} name="flat" placeholder="Необязательно"/></label><div className="checkout-v43-slots"><span>Удобное время</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div></>:<div className="checkout-v43-pvz"><span>Выберите пункт выдачи</span>{pvz.length?pvz.map(point=><button type="button" key={point} className={pickupPoint===point?"active":""} onClick={()=>setPickupPoint(point)}><i/><div><b>{point}</b><small>{form.city}</small></div></button>):<p>Выберите город — покажем доступные пункты.</p>}</div>}</div>{deliveryAttempted&&!deliveryOk&&<div className="checkout-v43-inline-error" role="alert">{delivery==="courier"?"Укажите город и адрес доставки.":"Выберите город и пункт выдачи."}</div>}<button type="button" className="primary checkout-v43-next" onClick={nextFromDelivery}>ПРОДОЛЖИТЬ К ОПЛАТЕ</button></section>}

        {step===3&&<section className="checkout-v43-step" data-analytics-step="checkout_payment"><header><small>ШАГ 3 ИЗ 3</small><h1>Оплата и подтверждение</h1><p>Проверьте способ оплаты и итоговую сумму. После нажатия заказ будет создан.</p></header><div className="checkout-v43-payments"><button type="button" className={payment==="card"?"active":""} onClick={()=>setPayment("card")}><i/><div><b>Банковская карта</b><span>−3% при онлайн-оплате</span></div></button><button type="button" className={payment==="sbp"?"active":""} onClick={()=>setPayment("sbp")}><i/><div><b>СБП</b><span>−3% при онлайн-оплате</span></div></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><div><b>При получении</b><span>Без скидки</span></div></button></div>{expensive&&<aside className="checkout-v43-concierge"><small>ЗАКАЗ ОТ 30 000 ₽</small><b>Персональное сопровождение</b><p>Менеджер свяжется в течение часа, чтобы подтвердить наличие, доставку и детали заказа.</p></aside>}<section className="checkout-v43-review"><div><span>Контакты</span><p>{form.name} · {form.phone}{form.email?` · ${form.email}`:""}</p><button type="button" onClick={()=>setStep(1)}>Изменить</button></div><div><span>Доставка</span><p>{delivery==="courier"?`${form.city}, ${form.address}${access?`, ${access}`:""} · ${slot}`:`ПВЗ: ${form.city}, ${pickupPoint}`}</p><button type="button" onClick={()=>setStep(2)}>Изменить</button></div></section><button type="button" className="checkout-v43-promo-toggle" onClick={()=>setPromoOpen(!promoOpen)}>Промокод или сертификат <span>{promoOpen?"−":"+"}</span></button>{promoOpen&&<div className="checkout-v43-promo"><input value={promo} onChange={event=>{setPromo(event.target.value);setPromoStatus("")}} placeholder="Введите код"/><button type="button" onClick={applyPromo}>Применить</button>{promoStatus&&<small>{promoStatus}</small>}</div>}<label className="checkout-v43-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Сообщать об изменении статуса заказа</span></label><label className="checkout-v43-check"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Согласен(на) с условиями продажи и обработкой персональных данных.</span></label>{!paymentOk&&<div className="checkout-v43-inline-error">Выберите способ оплаты.</div>}<button type="submit" className="primary checkout-v43-next" disabled={!canSubmit}>ОФОРМИТЬ ЗАКАЗ · {fmt(payable)}</button></section>}
      </main>
      <aside className="checkout-v43-summary"><div className="checkout-v43-summary-inner"><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header><div className="checkout-v43-summary-items">{cart.slice(0,3).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><div><b>{item.name}</b><span>{item.selectedColor} · {item.selectedSize}</span><small>{item.quantity} × {fmt(item.price)}</small></div></article>)}</div>{cart.length>3&&<small className="checkout-v43-more">Ещё {cart.length-3} поз.</small>}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div>{onlineDiscount>0&&<div className="discount"><dt>Онлайн-оплата −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}<div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div></dl><div className="checkout-v43-total"><span>Итого</span><b>{fmt(payable)}</b></div><p>{delivery==="pickup"?"Пункт выдачи выбран без доплаты.":shipping===0?"Курьерская доставка бесплатна.":"Курьерская доставка включена в итог."}</p>{profile?<div className="checkout-v43-bonus"><span>Бонусы</span><b>0 доступно</b></div>:<div className="checkout-v43-bonus"><span>Бонусы</span><b>Войдите, чтобы увидеть баланс</b></div>}</div></aside>
    </form>
    <div className="checkout-v43-mobile-bar"><div><small>ИТОГО</small><b>{fmt(payable)}</b></div>{step===1?<button type="button" className="primary" onClick={nextFromContacts}>ПРОДОЛЖИТЬ</button>:step===2?<button type="button" className="primary" onClick={nextFromDelivery}>ПРОДОЛЖИТЬ</button>:<button type="button" className="primary" disabled={!canSubmit} onClick={()=>{if(canSubmit)submit()}}>ОФОРМИТЬ</button>}</div>
  </div>;
}

function CheckoutMap({points,selected,choose,mode}:{points:string[];selected:string;choose:(point:string)=>void;mode:"courier"|"pickup"}){
  return <div className="checkout-map"><div className="map-canvas" aria-label="Карта выбора адреса">{points.map((point,index)=><button type="button" key={point} className={`map-pin pin-${index} ${selected===point?"active":""}`} onClick={()=>choose(point)} aria-label={`Выбрать ${point}`}><Icon name="pin"/><span>{index+1}</span></button>)}<i className="river"/><span className="map-label moscow">МОСКВА</span><span className="map-label center">САДОВОЕ КОЛЬЦО</span></div><div className="map-points"><p>{mode==="pickup"?"ВЫБЕРИТЕ БУТИК":"УТОЧНИТЕ ТОЧКУ НА КАРТЕ"}</p>{points.map((point,index)=><button type="button" key={point} className={selected===point?"active":""} onClick={()=>choose(point)}><b>{index+1}</b><span>{point}<small>{mode==="pickup"?"Сегодня до 22:00":"Курьерская доставка"}</small></span></button>)}</div></div>;
}

function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) { return <footer><div className="footer-brand"><div className="logo">КУЛЬТУРА ДОМА</div><p>Подпишитесь на письма о новых коллекциях</p><div><input placeholder="Ваш email"/><button onClick={()=>notice("Спасибо за подписку")}>→</button></div></div><div><p>ПОКУПАТЕЛЯМ</p><button onClick={()=>go("catalog")}>Каталог</button><button onClick={()=>alert("Доставка по России от 1 дня")}>Доставка и оплата</button><button onClick={()=>alert("Возврат в течение 14 дней")}>Возврат</button></div><div><p>О БРЕНДЕ</p><button onClick={()=>go("collections")}>Коллекции</button><button onClick={()=>alert("Русский бренд предметов для дома")}>Наша история</button><button onClick={()=>alert("Москва · Санкт-Петербург · Казань")}>Бутики</button></div><div><p>СВЯЗАТЬСЯ</p><a href="tel:+78005553535">8 800 555-35-35</a><a href="mailto:hello@kultura-doma.ru">hello@kultura-doma.ru</a></div><small>© 2026 Культура дома &nbsp; · &nbsp; Политика конфиденциальности</small></footer> }
