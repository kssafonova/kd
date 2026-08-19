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
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле. Белый, ледяной голубой и деликатный орнамент создают ощущение тихого зимнего утра.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/images/editorial/caps_led.png","/images/editorial/caps_led_podyshka.png","/images/editorial/caps_led_podyshka2.png","/images/editorial/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КАПСУЛА", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Интерактивный editorial о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/images/editorial/caps_luna_postel.png","/images/editorial/caps_luna_postel2.png","/images/editorial/caps_luna_postel3.png","/images/editorial/caps_luna_serviz.png","/images/editorial/caps_luna_serviz2.png","/images/editorial/caps_luna_serviz3.png"], productIds:[4,10,5,6,3] },
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
    setPlpSize(null); setSizeSheet(false); if(openDrawer)setCartOpen(true);
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
      {view === "editorial" && <EditorialView editorial={editorial} selectProduct={openProduct} favorite={favorite} favorites={favorites} buyBundle={addBundle} />}
      {view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} selectProduct={openProduct} recentlyViewed={recentlyViewed} />}
      <Footer go={go} notice={notice} />

      {menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} />}
      {search && <Search close={() => setSearch(false)} choose={(p) => { setSelected(p); setSearch(false); go("product"); }} />}
      {account && <Account profile={profile} close={() => setAccount(false)} notice={notice} save={setProfile} logout={()=>setProfile(null)} />}
      {favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setSelected(product);setFavoritesOpen(false);go("product")}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}
      {filters && <Filters close={() => setFilters(false)} apply={() => { setFilters(false); notice("Фильтры применены"); }} count={products.length} />}
      {plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,quantity,unitPrice) => addFromPLP(plpSize, chosenSize, quantity, unitPrice)} />}
      {plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} />}
      {sizeSheet && <SizeSheet size={size} setSize={setSize} close={() => setSizeSheet(false)} add={(quantity,unitPrice) => add({...selected,price:unitPrice},size,quantity)} price={selected.price} />}
      {cartOpen && <Cart cart={cart} recentlyViewed={recentlyViewed.map(id=>products.find(product=>product.id===id)!).filter(Boolean)} close={() => setCartOpen(false)} total={total} remove={(i) => setCart((old) => old.filter((_, index) => index !== i))} update={updateCartItem} checkout={() => {setCartOpen(false);setCheckoutOpen(true)}} go={() => { setCartOpen(false); go("catalog"); }} choose={(product)=>{setCartOpen(false);openProduct(product)}} />}
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
  const heroSlides=[
    {label:"НОВИНКИ",title:"Новинки",cta:"Смотреть",desktopImage:"/images/time-hero.png",mobileImage:"/images/blue-bedding-vertical.png",action:()=>openCatalog("Все товары")},
    {label:"СПАЛЬНЯ",title:"Спальня",cta:"Смотреть",desktopImage:"/images/blue-bedroom.png",mobileImage:"/images/editorial/caps_luna_postel.png",action:()=>openCatalog("Постельное бельё")},
    {label:"ДЕКОР ДЛЯ ДОМА",title:"Декор для дома",cta:"Смотреть",desktopImage:"/images/beige-bedroom.png",mobileImage:"/images/russian-bedroom.png",action:()=>openCatalog("Пледы и подушки")},
  ];
  const activeIndex=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[activeIndex];
  const [traditionsPlaying,setTraditionsPlaying]=useState(true);
  const [heroPaused,setHeroPaused]=useState(false);
  const heroTouchStart=useRef<number|null>(null);

  useEffect(()=>{
    if(heroPaused||window.matchMedia("(prefers-reduced-motion: reduce)").matches)return;
    const timer=window.setInterval(()=>setSlide((activeIndex+1)%heroSlides.length),6500);
    return()=>window.clearInterval(timer);
  },[activeIndex,setSlide,heroSlides.length,heroPaused]);

  const shiftHero=(direction:-1|1)=>setSlide((activeIndex+direction+heroSlides.length)%heroSlides.length);

  const scrollHomeRail=(id:string,direction:-1|1)=>{
    const host=document.getElementById(id);
    if(!host)return;
    const rail=(host.matches(".hv4-category-rail,.hv4-solution-rail")?host:host.querySelector(".product-rail")) as HTMLElement|null;
    if(!rail)return;
    rail.scrollBy({left:direction*Math.max(280,rail.clientWidth*.72),behavior:"smooth"});
  };

  const categories=[
    {title:"Постельное бельё",meta:"СПАЛЬНЯ",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Пледы и подушки",meta:"ТЕКСТИЛЬ",image:"/images/sky-bolster.png",category:"Пледы и подушки"},
    {title:"Посуда и сервировка",meta:"СТОЛОВАЯ",image:"/images/moon-plate.png",category:"Посуда и сервировка"},
    {title:"Столовый текстиль",meta:"СЕРВИРОВКА",image:"/images/editorial-table.webp",category:"Столовый текстиль"},
    {title:"Домашняя одежда",meta:"ДЛЯ ДОМА",image:"/images/classic-bedroom.png",category:"Домашняя одежда"},
    {title:"Декор для дома",meta:"ИНТЕРЬЕР",image:"/images/beige-bedroom.png",category:"Все товары"},
    {title:"Ванная",meta:"ТЕКСТИЛЬ",image:"/images/russian-bedroom.png",category:"Все товары"},
    {title:"Подарки",meta:"ИДЕИ",image:"/images/time-collection.png",category:"Все товары"},
  ];

  const newProducts=[2000,2004,2010,2003,4,10,5,6].map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const collectionProductIds=Array.from(new Set(editorials.flatMap(item=>item.productIds)));
  const collectionProducts=collectionProductIds.map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;
  const solutions=[
    {room:"ГОСТИНАЯ",title:"Тихая гостиная",image:"/images/beige-bedroom.png"},
    {room:"СПАЛЬНЯ",title:"Синий бархат ночи",image:"/images/blue-bedroom.png"},
    {room:"КАБИНЕТ",title:"Кабинетное ретро",image:"/images/time-collection.png"},
    {room:"КУХНЯ",title:"Утро в зимнем саду",image:"/images/buyan-editorial.png"},
  ];

  return <main className="home-v4 home-reference-v5 home-togas-v10 home-ux-v11">
    <section className="hv4-hero" aria-label="Главные разделы"
      onPointerEnter={()=>setHeroPaused(true)} onPointerLeave={()=>setHeroPaused(false)}
      onFocusCapture={()=>setHeroPaused(true)} onBlurCapture={()=>setHeroPaused(false)}
      onTouchStart={event=>{heroTouchStart.current=event.touches[0]?.clientX??null;setHeroPaused(true)}}
      onTouchEnd={event=>{const start=heroTouchStart.current;const end=event.changedTouches[0]?.clientX;if(start!==null&&end!==undefined&&Math.abs(end-start)>44)shiftHero(end<start?1:-1);heroTouchStart.current=null;setHeroPaused(false)}}>
      <picture className="hv4-hero-media">
        <source media="(max-width: 700px)" srcSet={assetUrl(hero.mobileImage)}/>
        <img src={assetUrl(hero.desktopImage)} alt={hero.title}/>
      </picture>
      <div className="hv4-hero-copy" aria-live="polite"><h1>{hero.title}</h1><button type="button" onClick={hero.action}><span>{hero.cta}</span><Icon name="arrow"/></button></div>
      <div className="hv4-hero-controls">
        <nav className="hv4-hero-tabs" aria-label="Слайды главной">{heroSlides.map((item,index)=><button type="button" key={item.label} className={index===activeIndex?"active":""} aria-current={index===activeIndex?"true":undefined} onClick={()=>setSlide(index)}>{item.label}</button>)}</nav>
        <div className="hv4-hero-arrows" aria-label="Переключить баннер"><button type="button" aria-label="Предыдущий баннер" onClick={()=>shiftHero(-1)}><Icon name="arrow"/></button><button type="button" aria-label="Следующий баннер" onClick={()=>shiftHero(1)}><Icon name="arrow"/></button></div>
      </div>
    </section>

    <section className="hv4-categories hv4-shell">
      <header className="hv4-head"><div><small>КАТАЛОГ</small><h2>Категории</h2></div><div className="hv4-head-actions"><button className="hv4-rail-arrow prev" type="button" aria-label="Категории назад" onClick={()=>scrollHomeRail("home-category-rail",-1)}><Icon name="arrow"/></button><button className="hv4-rail-arrow" type="button" aria-label="Категории вперёд" onClick={()=>scrollHomeRail("home-category-rail",1)}><Icon name="arrow"/></button><button className="hv4-text-cta" type="button" onClick={()=>openCatalog("Все товары")}>ВЕСЬ КАТАЛОГ</button></div></header>
      <div id="home-category-rail" className="hv4-category-rail" aria-label="Категории товаров">{categories.map(item=><button className="hv4-category-card" type="button" key={item.title} onClick={()=>openCatalog(item.category)}><img src={assetUrl(item.image)} alt={item.title}/><span><strong>{item.title}</strong><small>{item.meta}</small></span></button>)}</div>
    </section>

    <section className="hv4-new hv4-section hv4-shell">
      <header className="hv4-head"><div><small>НОВИНКИ</small><h2>Новое поступление</h2></div><div className="hv4-head-actions"><button className="hv4-rail-arrow prev" type="button" aria-label="Новинки назад" onClick={()=>scrollHomeRail("home-new-rail",-1)}><Icon name="arrow"/></button><button className="hv4-rail-arrow" type="button" aria-label="Новинки вперёд" onClick={()=>scrollHomeRail("home-new-rail",1)}><Icon name="arrow"/></button><button className="hv4-text-cta" type="button" onClick={()=>openCatalog("Все товары")}>СМОТРЕТЬ ВСЕ</button></div></header>
      <div id="home-new-rail"><ProductRail className="hv4-new-rail" items={newProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/></div>
    </section>

    <section className="hv4-traditions-collections" aria-label="Традиции, капсулы и коллекции">
      <div className="hv4-traditions-collections-shell">
        <div className={`hv4-traditions-media ${traditionsPlaying?"is-playing":"is-paused"}`}> 
          <img src={assetUrl("/images/russian-bedroom.png")} alt="Современная русская спальня"/>
          <img src={assetUrl("/images/editorial-table.webp")} alt="Сервировка дома"/>
          <img src={assetUrl("/images/time-hero.png")} alt="Предметы Культура дома"/>
          <div className="hv4-traditions-copy"><div><small>BRAND STORY</small><h2>Традиции в каждом доме</h2></div><span>КУЛЬТУРА ДОМА</span></div>
          <div className="hv4-video-controls" aria-label="Управление историей">
            <button type="button" className="hv4-video-toggle" onClick={()=>setTraditionsPlaying(value=>!value)} aria-label={traditionsPlaying?"Поставить видео на паузу":"Продолжить видео"}>
              {traditionsPlaying?<span className="hv4-pause-icon" aria-hidden="true"><i/><i/></span>:<span className="hv4-play-icon" aria-hidden="true"/>}
            </button>
            <span className="hv4-video-track" aria-hidden="true"><i/></span>
            <small>0:15</small>
          </div>
        </div>

        <div className="hv4-traditions-collections-content">
          <header className="hv4-traditions-collections-head">
            <div><small>КОЛЛЕКЦИИ</small><h2>Капсулы и коллекции</h2></div>
            <div className="hv4-head-actions">
              <button className="hv4-rail-arrow prev" type="button" aria-label="Товары коллекций назад" onClick={()=>scrollHomeRail("home-collection-rail",-1)}><Icon name="arrow"/></button>
              <button className="hv4-rail-arrow" type="button" aria-label="Товары коллекций вперёд" onClick={()=>scrollHomeRail("home-collection-rail",1)}><Icon name="arrow"/></button>
              <button className="hv4-text-cta" type="button" onClick={()=>go("collections")}>СМОТРЕТЬ ВСЕ</button>
            </div>
          </header>
          <div id="home-collection-rail"><ProductRail className="hv4-collection-product-rail" items={collectionProducts} onProduct={onProduct} onQuick={onAdd} favorite={favorite} favorites={favorites}/></div>
        </div>
      </div>
    </section>

    <section className="hv4-solutions">
      <div className="hv4-shell">
        <header className="hv4-head"><div><small>ВДОХНОВЕНИЕ</small><h2>Готовые решения для дома</h2></div><div className="hv4-head-actions"><button className="hv4-rail-arrow prev" type="button" aria-label="Решения назад" onClick={()=>scrollHomeRail("home-solution-rail",-1)}><Icon name="arrow"/></button><button className="hv4-rail-arrow" type="button" aria-label="Решения вперёд" onClick={()=>scrollHomeRail("home-solution-rail",1)}><Icon name="arrow"/></button><a className="hv4-text-cta" href={constructorHref}>СМОТРЕТЬ ВСЕ</a></div></header>
        <div id="home-solution-rail" className="hv4-solution-rail">{solutions.map(item=><a className="hv4-solution-card" href={constructorHref} key={item.room}><img src={assetUrl(item.image)} alt={`${item.room}: ${item.title}`}/><span><small>{item.room}</small><strong>{item.title}</strong><em>СМОТРЕТЬ</em></span></a>)}</div>
      </div>
    </section>

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

function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void }) {
  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];
  const [colorIndex, setColorIndex] = useState(0);
  const chosen = variants[colorIndex];
  const chosenSku=findProductSku(product,chosen.name);
  const chosenProduct = { ...product, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };
  const discount=discountOf(product);
  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);
  const knownPrice=priceKnown(product.price);
  return <article className="product-card"><button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button><button className="product-image" onClick={()=>onClick(chosenProduct)}><ScrollableProductMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, цвет ${chosen.name}`} position={chosen.position||product.position}/>{product.badge&&<span>{product.badge}</span>}</button><div className="product-copy"><button className="product-link" onClick={()=>onClick(chosenProduct)}><strong>{product.name}</strong><small>{chosen.name.toLowerCase()}, {product.note}</small></button>{variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span></div>{selectionMode?<button className={`quick selection-check ${pending?"pending":selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={pending?`Выберите размер для ${product.name}`:selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{pending?"?":selected?"✓":""}</button>:<button className="quick" disabled={!knownPrice} onClick={()=>knownPrice&&onQuick(chosenProduct)} aria-label={knownPrice?`Добавить в корзину ${product.name}`:`Цена товара ${product.name} уточняется`}><Icon name="cart-add"/></button>}</article>;
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
function CollectionsView({ onProduct,onQuick,favorite,favorites,buyBundle }: { onProduct:(product:Product)=>void; onQuick:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  const [storyPreview,setStoryPreview]=useState<Editorial|null>(null);
  const [selectingStory,setSelectingStory]=useState(false);
  const [selectedStoryIds,setSelectedStoryIds]=useState<number[]>([]);
  const [storySizes,setStorySizes]=useState<Record<number,string>>({});

  const storyItems=(storyPreview?.productIds??[]).map(id=>products.find(product=>product.id===id)).filter((product):product is Product=>Boolean(product));

  const sizeOptions=(product:Product)=>Array.from(new Set((product.skus??[]).map(item=>item.size).filter(Boolean)));
  const hasMultipleSizes=(product:Product)=>sizeOptions(product).length>1;
  const selectedColor=(product:Product)=>product.selectedColor??product.skus?.[0]?.color;
  const selectedSize=(product:Product)=>{
    const sizes=sizeOptions(product);
    if(sizes.length===1)return sizes[0];
    return storySizes[product.id]??"";
  };
  const prepareStoryProduct=(product:Product):Product=>{
    const size=selectedSize(product);
    const color=selectedColor(product);
    const sku=size?findProductSku(product,color,size):findProductSku(product,color);
    return {
      ...product,
      price:sku?.price??product.price,
      image:sku?.image??product.image,
      gallery:sku?.gallery??product.gallery,
      selectedColor:sku?.color??color,
      selectedSize:size||(sku?.size??product.selectedSize),
      selectedSkuId:sku?.id??product.selectedSkuId,
      quantity:1,
    };
  };

  const selectedStoryProducts=storyItems.filter(item=>selectedStoryIds.includes(item.id)).map(prepareStoryProduct);
  const pendingSizeIds=storyItems.filter(item=>selectedStoryIds.includes(item.id)&&hasMultipleSizes(item)&&!storySizes[item.id]).map(item=>item.id);
  const storyTotal=storyItems.reduce((sum,item)=>sum+item.price,0);
  const selectedStoryTotal=selectedStoryProducts.reduce((sum,item)=>sum+item.price,0);

  const openStory=(item:Editorial)=>{
    setStoryPreview(item);
    setSelectingStory(false);
    setSelectedStoryIds(item.productIds);
    setStorySizes({});
  };
  const closeStory=()=>{
    setStoryPreview(null);
    setSelectingStory(false);
    setSelectedStoryIds([]);
    setStorySizes({});
  };
  const toggleStoryProduct=(id:number)=>setSelectedStoryIds(current=>current.includes(id)?current.filter(itemId=>itemId!==id):[...current,id]);

  useEffect(()=>{
    if(!storyPreview)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")closeStory()};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[storyPreview]);

  const handleStoryPurchase=()=>{
    if(!storyItems.length)return;
    if(!selectingStory){
      setSelectingStory(true);
      setSelectedStoryIds(storyItems.map(item=>item.id));
      return;
    }
    if(!selectedStoryProducts.length||pendingSizeIds.length)return;
    buyBundle(selectedStoryProducts);
    closeStory();
  };

  return <div className="collections page">
    <header className="section-head editorial-index-head">
      <p>EDITORIAL</p>
      <h1>Капсулы и коллекции</h1>
    </header>

    <div className="collection-grid" aria-label="Капсулы и коллекции">
      {editorials.map((item)=><article key={item.id}>
        <button type="button" onClick={()=>openStory(item)}>
          <img src={assetUrl(item.images[1]??item.images[0])} alt={item.name}/>
          <div>
            <small>{item.kind}</small>
            <h2>{item.name}</h2>
            <p>{item.description}</p>
            <span>СМОТРЕТЬ ИСТОРИЮ <Icon name="arrow"/></span>
          </div>
        </button>
      </article>)}
    </div>

    {storyPreview&&<section className={`editorial-story-overlay ${selectingStory?"story-selection-mode":""}`} role="dialog" aria-modal="true" aria-label={`История ${storyPreview.name}`}>
      <div className={`editorial-story-visual ${storyPreview.images.length<2?"single":""}`}>
        {storyPreview.images.map((image,index)=><figure key={`${storyPreview.id}-story-${image}`}><img src={assetUrl(image)} alt={`${storyPreview.name}, editorial ${index+1}`}/><figcaption>{String(index+1).padStart(2,"0")} / {String(storyPreview.images.length).padStart(2,"0")}</figcaption></figure>)}
      </div>
      <aside className="editorial-story-shop">
        <button className="editorial-story-close" type="button" onClick={closeStory} aria-label="Закрыть историю"><Icon name="close"/></button>
        <header className="editorial-story-shop-head">
          <small>{storyPreview.kind} · EDITORIAL</small>
          <h2>{storyPreview.name}</h2>
          <p>{selectingStory?"Выберите предметы истории и размеры там, где это необходимо.":storyPreview.lead}</p>
          {selectingStory&&<div className="editorial-story-selection-tools"><span>{selectedStoryIds.length} из {storyItems.length} выбрано</span><button type="button" onClick={()=>setSelectedStoryIds(selectedStoryIds.length===storyItems.length?[]:storyItems.map(item=>item.id))}>{selectedStoryIds.length===storyItems.length?"Снять выбор":"Выбрать всё"}</button></div>}
        </header>
        <div className="editorial-story-products" aria-label="Товары из истории">
          <div className="editorial-story-catalog-grid product-grid">
            {storyItems.map(item=>{
              const sizes=sizeOptions(item);
              const multiple=sizes.length>1;
              const selected=selectedStoryIds.includes(item.id);
              const pending=selectingStory&&selected&&multiple&&!storySizes[item.id];
              return <div className={`editorial-story-catalog-item ${selected?"selected":""} ${pending?"pending-size":""}`} key={`story-product-${storyPreview.id}-${item.id}`}>
                <ProductCard product={item} onClick={(product)=>{closeStory();onProduct(product)}} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)} selectionMode={selectingStory} selected={selected} pending={false} onSelect={()=>toggleStoryProduct(item.id)}/>
                {selectingStory&&selected&&multiple&&<label className={`editorial-story-size-select ${pending?"required":""}`}>
                  <span>РАЗМЕР</span>
                  <select value={storySizes[item.id]??""} onChange={event=>setStorySizes(current=>({...current,[item.id]:event.target.value}))}>
                    <option value="">Выбрать размер</option>
                    {sizes.map(size=>{
                      const sku=findProductSku(item,selectedColor(item),size);
                      const available=sku?.available!==false;
                      return <option key={`${item.id}-${size}`} value={size} disabled={!available}>{size}{sku?.price?` · ${fmt(sku.price)}`:""}{!available?" · нет в наличии":""}</option>;
                    })}
                  </select>
                </label>}
              </div>;
            })}
          </div>
        </div>
        <footer className="editorial-story-shop-footer">
          <div className="editorial-story-total">
            <span>{selectingStory?pendingSizeIds.length?`Выберите размер · ${pendingSizeIds.length}`:`${productCountLabel(selectedStoryProducts.length)} выбрано`:`${productCountLabel(storyItems.length)} в истории`}</span>
            <strong>{fmt(selectingStory?selectedStoryTotal:storyTotal)}</strong>
          </div>
          <button className="editorial-story-buy" type="button" disabled={!storyItems.length||(selectingStory&&(!selectedStoryProducts.length||pendingSizeIds.length>0))} onClick={handleStoryPurchase}><span>{selectingStory?"ДОБАВИТЬ В КОРЗИНУ":"КУПИТЬ ИСТОРИЮ"}</span><b>{fmt(selectingStory?selectedStoryTotal:storyTotal)}</b></button>
        </footer>
      </aside>
    </section>}
  </div>;
}

function LunaEditorialView({ editorial, selectProduct, favorite, favorites, quickAdd, addToCart, openCart }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; quickAdd:(product:Product)=>void; addToCart:(product:Product)=>void; openCart:()=>void }) {
  type StoryKind = "bedroom" | "table";
  type StoryMode = "quick" | "builder" | null;
  type StoryLine = { key:string; product:Product; quantity:number; required?:boolean; subtitle:string };
  type AddedState = { title:string; lines:StoryLine[]; total:number };

  const [story,setStory]=useState<StoryKind|null>(null);
  const [mode,setMode]=useState<StoryMode>(null);
  const [builderStep,setBuilderStep]=useState(1);
  const [bedSize,setBedSize]=useState("");
  const [bedOptional,setBedOptional]=useState({blanket:true,pillow:true});
  const [bedQty,setBedQty]=useState({blanket:1,pillow:1});
  const [occasion,setOccasion]=useState("Чай для двоих");
  const [guests,setGuests]=useState<2|4|6>(2);
  const [tableOptional,setTableOptional]=useState({napkin:true,plate:false,vase:false,gift:false});
  const [added,setAdded]=useState<AddedState|null>(null);

  const track=(event:string,detail:Record<string,unknown>={})=>{
    if(typeof window==="undefined")return;
    const payload={event,capsule:"Лунная сказка",story:story??undefined,...detail};
    window.dispatchEvent(new CustomEvent("kd:analytics",{detail:payload}));
    const layer=(window as unknown as {dataLayer?:Record<string,unknown>[]}).dataLayer;
    layer?.push(payload);
  };

  useEffect(()=>{
    if(story)track("story_view",{story});
  // analytics fires only when the user opens a story
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[story]);

  useEffect(()=>{
    if(!story&&!mode&&!added)return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    return()=>{document.body.style.overflow=previous};
  },[story,mode,added]);

  const colorById:Record<number,string>={4:"Ночной синий",10:"Ночной синий",5:"Ночной синий",6:"Синий",3:"Синий"};
  const previewById:Record<number,string>={4:"/images/products/KD-PD-1024-DARK02.png",6:"/images/products/KD-PD-1026-BLUE01.png",3:"/images/products/KD-PD-1023-BLUE02.png"};
  const prepare=(product:Product):Product=>{
    const color=colorById[product.id]??product.selectedColor??product.colorVariants?.[0]?.name;
    const regularPrice=product.oldPrice??product.price;
    const preview=previewById[product.id];
    const variants=(product.colorVariants??[]).filter(variant=>variant.name===color);
    const skus=product.skus?.filter(s=>s.color===color).map(s=>({...s,price:regularPrice,...(preview?{image:preview,gallery:Array.from(new Set([preview,...s.gallery]))}:{})}));
    const sku=skus?.find(s=>s.color===color)??skus?.[0];
    return {...product,oldPrice:undefined,badge:undefined,image:preview??sku?.image??product.image,gallery:sku?.gallery??product.gallery,colorVariants:variants.length?variants:product.colorVariants,skus,selectedColor:sku?.color??color,selectedSize:sku?.size??product.selectedSize,selectedSkuId:sku?.id,price:regularPrice};
  };

  const lunaItems=editorial.productIds.map(id=>products.find(p=>p.id===id)).filter(Boolean).map(p=>prepare(p!));
  const itemById=(id:number)=>lunaItems.find(item=>item.id===id);
  const bedding=itemById(4)!;
  const blanket=itemById(6)!;
  const pillow=itemById(3)!;
  const tea=itemById(10)!;

  const virtualProduct=(id:number,name:string,price:number,image:string,note:string,color:string,size:string,article:string):Product=>({
    id,name,price,image,note,article,selectedColor:color,selectedSize:size,selectedSkuId:article,quantity:1,
    colorVariants:[{name:color,hex:color.includes("син")?"#1b2c49":"#e7ded0",image}],gallery:[image]
  });
  const napkin=virtualProduct(110,"Льняная салфетка с вышивкой",1490,"/images/products/KD-PD-1027-MOL01.png","лён, вышивка","Молочный","45×45 см","KD-STORY-NAPKIN");
  const dessert=virtualProduct(111,"Тарелка десертная «Лунная сказка»",2990,"/images/moon-plate.png","фарфор","Ночной синий","18 см","KD-STORY-PLATE");
  const vase=virtualProduct(112,"Ваза «Ледяные узоры»",5990,"/images/editorial/caps_led_serviz.png","стекло","Ледяной","Стандарт","KD-STORY-VASE");
  const gift=virtualProduct(113,"Подарочная упаковка",490,"/images/editorial/caps_luna_serviz2.png","премиальная упаковка","Молочный","Стандарт","KD-STORY-GIFT");

  const bedSizes=[
    {label:"Полуторный 140×220",price:29990,available:true},
    {label:"Евро 200×220",price:29990,available:true},
    {label:"Кинг сайз 220×240",price:31990,available:true},
  ];
  const bedSizePrice=bedSizes.find(option=>option.label===bedSize)?.price??0;
  const configuredBedding=():Product=>({
    ...bedding,
    price:bedSizePrice||29990,
    selectedSize:bedSize,
    quantity:1,
    skus:bedding.skus?.map(s=>s.size===bedSize?{...s,price:bedSizePrice||s.price}:s),
  });
  const fixed=(product:Product,quantity=1):Product=>{
    const color=product.selectedColor??product.colorVariants?.[0]?.name??"Молочный";
    const options=getProductSizeOptions(product,color);
    const size=options.length===1?options[0][0]:(product.selectedSize??options[0]?.[0]??"Стандарт");
    const sku=findProductSku(product,color,size);
    return {...product,selectedColor:sku?.color??color,selectedSize:sku?.size??size,selectedSkuId:sku?.id??product.selectedSkuId,price:sku?.price??product.price,quantity};
  };

  const bedroomLines=():StoryLine[]=>{
    const lines:StoryLine[]=[];
    if(bedSize)lines.push({key:"bedding",product:configuredBedding(),quantity:1,required:true,subtitle:`Ночной синий · ${bedSize}`});
    if(bedOptional.blanket)lines.push({key:"blanket",product:fixed(blanket,bedQty.blanket),quantity:bedQty.blanket,subtitle:`Синий · ${fixed(blanket).selectedSize}`});
    if(bedOptional.pillow)lines.push({key:"pillow",product:fixed(pillow,bedQty.pillow),quantity:bedQty.pillow,subtitle:`Синий · ${fixed(pillow).selectedSize}`});
    return lines;
  };
  const tableLines=():StoryLine[]=>{
    const lines:StoryLine[]=[{key:"tea",product:fixed({...tea,price:4490},guests),quantity:guests,required:true,subtitle:`Ночной синий · ${guests} персон`}];
    if(tableOptional.napkin)lines.push({key:"napkin",product:{...napkin,quantity:guests},quantity:guests,subtitle:`Молочный · ${guests} шт.`});
    if(tableOptional.plate)lines.push({key:"plate",product:{...dessert,quantity:guests},quantity:guests,subtitle:`Ночной синий · ${guests} шт.`});
    if(tableOptional.vase)lines.push({key:"vase",product:vase,quantity:1,subtitle:"Ледяной · 1 шт."});
    if(tableOptional.gift)lines.push({key:"gift",product:gift,quantity:1,subtitle:"1 упаковка"});
    return lines;
  };
  const currentLines=()=>story==="table"?tableLines():bedroomLines();
  const lineTotal=(line:StoryLine)=>line.product.price*line.quantity;
  const totalOf=(lines:StoryLine[])=>lines.reduce((sum,line)=>sum+lineTotal(line),0);
  const unitsOf=(lines:StoryLine[])=>lines.reduce((sum,line)=>sum+line.quantity,0);
  const deliveryText=(total:number)=>total>=15000?"Бесплатная доставка доступна":`До бесплатной доставки ${fmt(15000-total)}`;

  const storyDefs=[
    {id:"bedroom" as const,kicker:"СПАЛЬНЯ",title:"Спальня для долгих вечеров",intro:"Тёмный шёлк, прохладный синий и кружево — готовый образ, который можно купить целиком или настроить под себя.",images:editorial.images.slice(0,3),price:47970},
    {id:"table" as const,kicker:"СЕРВИРОВКА",title:"Чай для двоих",intro:"Вечерний чай и глубокий синий фарфор. Готовая сервировка для двух персон с возможностью изменить состав.",images:editorial.images.slice(3,6),price:11960},
  ];
  const activeStory=storyDefs.find(item=>item.id===story);

  const closeAll=()=>{setMode(null);setStory(null);setBuilderStep(1)};
  const openStory=(id:StoryKind)=>{
    setStory(id);setMode(null);setBuilderStep(1);setAdded(null);
    if(id==="bedroom"){
      setBedSize("");setBedOptional({blanket:true,pillow:true});setBedQty({blanket:1,pillow:1});
    }else{
      setOccasion("Чай для двоих");setGuests(2);setTableOptional({napkin:true,plate:false,vase:false,gift:false});
    }
  };
  const openQuick=()=>{
    // Quick-buy always opens the canonical ready-made preset, independent of builder edits.
    if(story==="bedroom"){
      setBedSize("");
      setBedOptional({blanket:true,pillow:true});
      setBedQty({blanket:1,pillow:1});
    }else if(story==="table"){
      setOccasion("Чай для двоих");
      setGuests(2);
      setTableOptional({napkin:true,plate:false,vase:false,gift:false});
    }
    setMode("quick");
    track("story_quick_add_open");
  };
  const openBuilder=()=>{setMode("builder");setBuilderStep(1);track("builder_open")};

  const commit=(title:string,lines:StoryLine[])=>{
    lines.forEach(line=>addToCart({...line.product,quantity:line.quantity}));
    const total=totalOf(lines);
    setAdded({title,lines,total});
    setMode(null);
    track(mode==="builder"?"builder_add_to_cart":"story_quick_add",{uniqueItems:lines.length,totalUnits:unitsOf(lines),totalPrice:total});
  };

  const quantity=(value:number,onChange:(next:number)=>void,label:string)=><div className="story-v2-qty" role="group" aria-label={`Количество: ${label}`}><button type="button" onClick={()=>onChange(Math.max(1,value-1))} aria-label={`Уменьшить количество ${label}`}>−</button><b>{value}</b><button type="button" onClick={()=>onChange(value+1)} aria-label={`Увеличить количество ${label}`}>+</button></div>;

  const productRow=(line:StoryLine,controls?:React.ReactNode)=><div className="story-v2-product-row" key={line.key}>
    <img src={assetUrl(line.product.image)} alt={line.product.name}/>
    <div className="story-v2-product-copy"><strong>{line.product.name}</strong><span>{line.subtitle}</span><small>{fmt(line.product.price)} за шт.</small></div>
    <div className="story-v2-product-side">{controls??<b>{line.quantity>1?`${line.quantity} × `:""}{fmt(lineTotal(line))}</b>}</div>
  </div>;

  const summary=(lines:StoryLine[],label?:string)=><aside className="story-v2-summary">
    {label&&<p>{label}</p>}
    <div><span>{lines.length} {lines.length===1?"товар":"товара"} / {unitsOf(lines)} шт.</span><strong>{fmt(totalOf(lines))}</strong></div>
    <small>{deliveryText(totalOf(lines))}</small>
  </aside>;

  const bedroomQuick=()=>{
    const lines=bedroomLines();
    const selectedTarget=1+(bedOptional.blanket?1:0)+(bedOptional.pillow?1:0);
    const ready=lines.length;
    const canAdd=Boolean(bedSize);
    return <>
      <header className="story-v2-sheet-head"><div><small>ГОТОВАЯ ИСТОРИЯ</small><h2>Спальня для долгих вечеров</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="story-v2-sheet-body">
        <div className={`story-v2-quick-required ${!bedSize?"needs-action":""}`}>
          <div className="story-v2-required-label"><span>Обязательно</span>{!bedSize&&<b>Нужен размер</b>}</div>
          <div className="story-v2-quick-title"><img src={assetUrl(bedding.image)} alt={bedding.name}/><div><strong>{bedding.name}</strong><span>Ночной синий</span></div></div>
          <div className="story-v2-size-list" role="radiogroup" aria-label="Выберите размер комплекта">
            {bedSizes.map(option=><button key={option.label} type="button" className={bedSize===option.label?"active":""} disabled={!option.available} onClick={()=>{setBedSize(option.label);track("variant_selected",{size:option.label,price:option.price})}} aria-pressed={bedSize===option.label}><span>{option.label}</span><b>{option.available?fmt(option.price):"Нет в наличии"}</b></button>)}
          </div>
          {!bedSize&&<p className="story-v2-validation">Выберите размер основы, чтобы добавить готовую историю.</p>}
        </div>
        <div className="story-v2-quick-options"><p>ДОПОЛНЕНИЯ</p>
          {[{key:"blanket" as const,item:blanket,selected:bedOptional.blanket,qty:bedQty.blanket},{key:"pillow" as const,item:pillow,selected:bedOptional.pillow,qty:bedQty.pillow}].map(row=>{
            const configured=fixed(row.item,row.qty);
            return <div className={`story-v2-toggle-row ${row.selected?"selected":""}`} key={row.key}>
              <img src={assetUrl(configured.image)} alt={configured.name}/>
              <div><strong>{configured.name}</strong><span>{configured.selectedSize}</span><small>{fmt(configured.price)}</small></div>
              <button className="story-v2-check" type="button" onClick={()=>{setBedOptional(current=>({...current,[row.key]:!current[row.key]}));track(row.selected?"builder_item_remove":"builder_item_add",{item:row.key})}} aria-pressed={row.selected} aria-label={row.selected?`Убрать ${configured.name}`:`Добавить ${configured.name}`}>{row.selected?"✓":""}</button>
            </div>
          })}
        </div>
      </div>
      <footer className="story-v2-sheet-footer">
        <div className="story-v2-ready"><span><b>{ready} из {selectedTarget}</b> товаров готовы</span><strong>{fmt(totalOf(lines))}</strong></div>
        <small>{deliveryText(totalOf(lines))}</small>
        <button className="story-v2-primary" disabled={!canAdd} onClick={()=>canAdd&&commit("Спальня для долгих вечеров",lines)}>{canAdd?`Добавить историю в корзину · ${fmt(totalOf(lines))}`:"Выберите размер"}</button>
        <button className="story-v2-link" type="button" onClick={openBuilder}>Не подходит состав? <u>Настроить историю</u></button>
      </footer>
    </>;
  };

  const tableQuick=()=>{
    const lines=tableLines();
    return <>
      <header className="story-v2-sheet-head"><div><small>ГОТОВАЯ ИСТОРИЯ</small><h2>Чай для двоих</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
      <div className="story-v2-sheet-body">
        <div className="story-v2-quick-options"><p>ГОТОВЫЙ СОСТАВ</p>
          {productRow(lines[0])}
          {productRow(lines.find(line=>line.key==="napkin")!)}
        </div>
        <div className="story-v2-person-note"><span>2 персоны</span><p>Хотите сервировку на 4 или 6 персон? Настройте историю — количество предметов пересчитается автоматически.</p></div>
      </div>
      <footer className="story-v2-sheet-footer">
        <div className="story-v2-ready"><span><b>{lines.length}</b> товара / {unitsOf(lines)} шт.</span><strong>{fmt(totalOf(lines))}</strong></div>
        <small>{deliveryText(totalOf(lines))}</small>
        <button className="story-v2-primary" onClick={()=>commit("Чай для двоих",lines)}>Добавить историю в корзину · {fmt(totalOf(lines))}</button>
        <button className="story-v2-link" type="button" onClick={openBuilder}>Нужно больше персон? <u>Настроить сервировку</u></button>
      </footer>
    </>;
  };

  const builderLines=story==="table"?tableLines():bedroomLines();
  const bedroomBuilder=()=>{
    const next=()=>setBuilderStep(step=>Math.min(4,step+1));
    const back=()=>setBuilderStep(step=>Math.max(1,step-1));
    return <div className="story-v2-builder-layout">
      <section className="story-v2-builder-main">
        <header className="story-v2-builder-head"><div><small>НАСТРОИТЬ ИСТОРИЮ</small><h2>Спальня для долгих вечеров</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <nav className="story-v2-steps" aria-label="Шаги конструктора">{["Основа","Размер","Дополнения","Ваш образ"].map((label,index)=><button key={label} type="button" className={builderStep===index+1?"active":builderStep>index+1?"done":""} onClick={()=>index+1<=builderStep&&setBuilderStep(index+1)}><b>{index+1}</b><span>{label}</span></button>)}</nav>
        <div className="story-v2-step-content">
          {builderStep===1&&<><div className="story-v2-step-title"><small>ШАГ 1</small><h3>Основа</h3><p>Основа образа обязательна. Она уже добавлена — останется выбрать подходящий размер.</p></div><div className="story-v2-base-card"><img src={assetUrl(bedding.image)} alt={bedding.name}/><div><span>ОБЯЗАТЕЛЬНО</span><strong>{bedding.name}</strong><small>Ночной синий</small><b>от {fmt(29990)}</b></div><i>✓</i></div></>}
          {builderStep===2&&<><div className="story-v2-step-title"><small>ШАГ 2</small><h3>Выберите размер</h3><p>Размер комплекта — обязательный параметр. Цена образа обновится сразу после выбора.</p></div><div className="story-v2-builder-sizes">{bedSizes.map(option=><button key={option.label} type="button" className={bedSize===option.label?"active":""} disabled={!option.available} onClick={()=>{setBedSize(option.label);track("variant_selected",{size:option.label,price:option.price})}}><span>{option.label}</span><b>{option.available?fmt(option.price):"Нет в наличии"}</b></button>)}</div>{!bedSize&&<p className="story-v2-validation">Размер пока не выбран — основа не входит в итоговую стоимость.</p>}</>}
          {builderStep===3&&<><div className="story-v2-step-title"><small>ШАГ 3</small><h3>Дополните образ</h3><p>Плед и подушка уже входят в preset. Их можно убрать или изменить количество.</p></div><div className="story-v2-builder-addons">{[{key:"blanket" as const,item:blanket,selected:bedOptional.blanket,qty:bedQty.blanket},{key:"pillow" as const,item:pillow,selected:bedOptional.pillow,qty:bedQty.pillow}].map(row=>{const configured=fixed(row.item,row.qty);return <div className={`story-v2-addon-card ${row.selected?"selected":""}`} key={row.key}><button className="story-v2-addon-media" type="button" onClick={()=>setBedOptional(current=>({...current,[row.key]:!current[row.key]}))}><img src={assetUrl(configured.image)} alt={configured.name}/><span>{row.selected?"Добавлено":"Добавить"}</span></button><div><strong>{configured.name}</strong><small>Размер: {configured.selectedSize}</small><b>{fmt(configured.price)}</b>{row.selected&&quantity(row.qty,nextQty=>setBedQty(current=>({...current,[row.key]:nextQty})),configured.name)}</div></div>})}</div></>}
          {builderStep===4&&<><div className="story-v2-step-title"><small>ШАГ 4</small><h3>Ваш образ</h3><p>Проверьте состав. В корзину попадут отдельные товары с выбранными вариантами и количеством.</p></div><div className="story-v2-review">{builderLines.map(line=>productRow(line,line.key==="blanket"?quantity(bedQty.blanket,nextQty=>setBedQty(current=>({...current,blanket:nextQty})),line.product.name):line.key==="pillow"?quantity(bedQty.pillow,nextQty=>setBedQty(current=>({...current,pillow:nextQty})),line.product.name):undefined))}</div></>}
        </div>
        <div className="story-v2-builder-nav">{builderStep>1?<button className="story-v2-secondary" type="button" onClick={back}>Назад</button>:<span/>}{builderStep<4?<div>{builderStep===3&&<button className="story-v2-skip" type="button" onClick={()=>setBuilderStep(4)}>Пропустить</button>}<button className="story-v2-primary compact" type="button" disabled={builderStep===2&&!bedSize} onClick={next}>{builderStep===2&&!bedSize?"Выберите размер":"Продолжить"}</button></div>:<button className="story-v2-primary compact" type="button" disabled={!bedSize} onClick={()=>bedSize&&commit("Спальня для долгих вечеров",builderLines)}>Добавить образ в корзину · {fmt(totalOf(builderLines))}</button>}</div>
      </section>
      <div className="story-v2-builder-aside">{summary(builderLines,bedSize?"ВАШ ОБРАЗ":"ВЫБЕРИТЕ РАЗМЕР")}</div>
    </div>;
  };

  const tableBuilder=()=>{
    const next=()=>setBuilderStep(step=>Math.min(4,step+1));
    const back=()=>setBuilderStep(step=>Math.max(1,step-1));
    const toggle=(key:keyof typeof tableOptional)=>{setTableOptional(current=>({...current,[key]:!current[key]}));track(tableOptional[key]?"builder_item_remove":"builder_item_add",{item:key})};
    return <div className="story-v2-builder-layout">
      <section className="story-v2-builder-main">
        <header className="story-v2-builder-head"><div><small>НАСТРОИТЬ СЕРВИРОВКУ</small><h2>Лунная сказка</h2></div><button onClick={()=>setMode(null)} aria-label="Закрыть"><Icon name="close"/></button></header>
        <nav className="story-v2-steps" aria-label="Шаги конструктора">{["Повод","Персоны","Дополнения","Ваш набор"].map((label,index)=><button key={label} type="button" className={builderStep===index+1?"active":builderStep>index+1?"done":""} onClick={()=>index+1<=builderStep&&setBuilderStep(index+1)}><b>{index+1}</b><span>{label}</span></button>)}</nav>
        <div className="story-v2-step-content">
          {builderStep===1&&<><div className="story-v2-step-title"><small>ШАГ 1</small><h3>Выберите повод</h3><p>Состав можно изменить позже — выбор задаёт только стартовый сценарий.</p></div><div className="story-v2-occasion-grid">{["Чай для двоих","Ужин с близкими","Праздничный стол"].map(value=><button key={value} type="button" className={occasion===value?"active":""} onClick={()=>setOccasion(value)}><span>{value}</span><small>{value==="Чай для двоих"?"Камерная сервировка":value==="Ужин с близкими"?"Спокойный вечер":"Торжественный стол"}</small></button>)}</div></>}
          {builderStep===2&&<><div className="story-v2-step-title"><small>ШАГ 2</small><h3>Количество персон</h3><p>Количество чайных пар, салфеток и тарелок пересчитывается автоматически.</p></div><div className="story-v2-guests">{([2,4,6] as const).map(value=><button key={value} className={guests===value?"active":""} type="button" onClick={()=>{setGuests(value);track("variant_selected",{guests:value})}}><b>{value}</b><span>персоны</span></button>)}</div>{productRow(tableLines()[0])}</>}
          {builderStep===3&&<><div className="story-v2-step-title"><small>ШАГ 3</small><h3>Дополните сервировку</h3><p>Салфетки входят в preset. Остальные предметы можно добавить по желанию.</p></div><div className="story-v2-table-addons">{[{key:"napkin" as const,item:napkin,label:`${guests} шт.`},{key:"plate" as const,item:dessert,label:`${guests} шт.`},{key:"vase" as const,item:vase,label:"1 шт."},{key:"gift" as const,item:gift,label:"1 шт."}].map(row=>{const selected=tableOptional[row.key];return <button type="button" className={`story-v2-table-addon ${selected?"selected":""}`} key={row.key} onClick={()=>toggle(row.key)}><img src={assetUrl(row.item.image)} alt={row.item.name}/><span><strong>{row.item.name}</strong><small>{row.label}</small><b>{fmt(row.item.price)}</b></span><i>{selected?"✓":"+"}</i></button>})}</div></>}
          {builderStep===4&&<><div className="story-v2-step-title"><small>ШАГ 4</small><h3>Ваш набор</h3><p>{occasion} · {guests} персон. В корзину попадут отдельные позиции.</p></div><div className="story-v2-review">{builderLines.map(line=>productRow(line))}</div></>}
        </div>
        <div className="story-v2-builder-nav">{builderStep>1?<button className="story-v2-secondary" type="button" onClick={back}>Назад</button>:<span/>}{builderStep<4?<div>{builderStep===3&&<button className="story-v2-skip" type="button" onClick={()=>{setTableOptional({napkin:false,plate:false,vase:false,gift:false});setBuilderStep(4)}}>Пропустить</button>}<button className="story-v2-primary compact" type="button" onClick={next}>Продолжить</button></div>:<button className="story-v2-primary compact" type="button" onClick={()=>commit(occasion,builderLines)}>Добавить набор в корзину · {fmt(totalOf(builderLines))}</button>}</div>
      </section>
      <div className="story-v2-builder-aside">{summary(builderLines,`${occasion.toUpperCase()} · ${guests} ПЕРСОН`)}</div>
    </div>;
  };

  return <div className="luna-story-v2-page">
    <section className="luna-story-v2-head"><p>КАПСУЛА</p><h1>Лунная сказка</h1><span>{editorial.lead}</span></section>
    <div className="luna-story-v2-list">{storyDefs.map((entry,index)=><section className={`luna-story-v2-entry ${index%2?"reverse":""}`} key={entry.id}>
      <button className="luna-story-v2-media" type="button" onClick={()=>openStory(entry.id)} aria-label={`Открыть историю ${entry.title}`}>
        <span className="luna-story-v2-media-grid">{entry.images.map((image,imageIndex)=><img src={assetUrl(image)} alt={`${entry.title}, фото ${imageIndex+1}`} key={`${entry.id}-${image}`}/>)}</span>
      </button>
      <div className="luna-story-v2-copy"><small>{entry.kicker}</small><h2>{entry.title}</h2><p>{entry.intro}</p><span>{entry.id==="bedroom"?"3 предмета":"4 предмета"} · от {fmt(entry.price)}</span><button type="button" onClick={()=>openStory(entry.id)}>ОТКРЫТЬ ИСТОРИЮ <Icon name="arrow"/></button></div>
    </section>)}</div>

    {story&&activeStory&&<div className="story-v2-layer" role="dialog" aria-modal="true" aria-label={activeStory.title}>
      <div className="story-v2-landing">
        <header className="story-v2-landing-head"><div><small>ЛУННАЯ СКАЗКА · {activeStory.kicker}</small><h2>{activeStory.title}</h2></div><button type="button" onClick={closeAll} aria-label="Закрыть историю"><Icon name="close"/></button></header>
        <div className="story-v2-landing-grid"><div className="story-v2-landing-gallery">{activeStory.images.map((image,index)=><img src={assetUrl(image)} alt={`${activeStory.title}, фото ${index+1}`} key={image}/>)}</div><aside className="story-v2-landing-info"><p>{activeStory.intro}</p><div className="story-v2-composition"><small>ГОТОВЫЙ ОБРАЗ</small>{(story==="bedroom"?[{name:bedding.name,meta:"Обязательно · выберите размер"},{name:blanket.name,meta:"Добавлено · можно убрать"},{name:pillow.name,meta:"Добавлено · можно убрать"}]:[{name:tea.name,meta:"2 шт. · основа"},{name:napkin.name,meta:"2 шт. · добавлено"}]).map(item=><div key={item.name}><strong>{item.name}</strong><span>{item.meta}</span></div>)}</div><div className="story-v2-landing-price"><span>{story==="bedroom"?"3 предмета":"4 предмета"}</span><strong>от {fmt(activeStory.price)}</strong></div><button className="story-v2-primary" type="button" onClick={openQuick}>Купить историю · от {fmt(activeStory.price)}</button><button className="story-v2-secondary wide" type="button" onClick={openBuilder}>{story==="table"?"Настроить сервировку":"Настроить под себя"}</button><p className="story-v2-landing-note">Без перехода в карточку товара. Состав и варианты настраиваются здесь.</p></aside></div>
      </div>
    </div>}

    {mode==="quick"&&story&&<div className="story-v2-sub-layer" role="dialog" aria-modal="true" aria-label="Купить историю"><button className="story-v2-backdrop" type="button" onClick={()=>setMode(null)} aria-label="Закрыть"/><section className="story-v2-sheet">{story==="bedroom"?bedroomQuick():tableQuick()}</section></div>}

    {mode==="builder"&&story&&<div className="story-v2-builder-layer" role="dialog" aria-modal="true" aria-label="Конструктор истории"><button className="story-v2-backdrop" type="button" onClick={()=>setMode(null)} aria-label="Закрыть"/><div className="story-v2-builder">{story==="bedroom"?bedroomBuilder():tableBuilder()}</div></div>}

    {added&&<div className="story-v2-sub-layer story-v2-confirm-layer" role="dialog" aria-modal="true" aria-label="История добавлена в корзину"><button className="story-v2-backdrop" type="button" onClick={()=>setAdded(null)} aria-label="Закрыть"/><section className="story-v2-confirm"><span className="story-v2-confirm-mark">✓</span><small>ГОТОВО</small><h2>История добавлена в корзину</h2><p>{added.title}</p><div className="story-v2-confirm-list">{added.lines.map(line=>productRow(line))}</div>{summary(added.lines)}<button className="story-v2-primary" type="button" onClick={()=>{setAdded(null);setStory(null);openCart();track("view_cart")}}>Перейти в корзину</button><button className="story-v2-secondary wide" type="button" onClick={()=>{setAdded(null);setStory(null);setBuilderStep(1)}}>Продолжить покупки</button></section></div>}
  </div>;
}


function EditorialView({ editorial, selectProduct, favorite, favorites, buyBundle }: { editorial:Editorial; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[]; buyBundle:(items:Product[])=>void }) {
  const items=editorial.productIds.map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  const [selecting,setSelecting]=useState(false);
  const [selectedIds,setSelectedIds]=useState<number[]>(items.map(item=>item.id));
  useEffect(()=>{setSelecting(false);setSelectedIds(items.map(item=>item.id))},[editorial.id]);
  const selectedItems=items.filter(item=>selectedIds.includes(item.id));
  const total=selectedItems.reduce((sum,item)=>sum+item.price,0);
  const toggle=(id:number)=>setSelectedIds(current=>current.includes(id)?current.filter(itemId=>itemId!==id):[...current,id]);
  const handleBundle=()=>{if(!selecting){setSelecting(true);return}if(selectedItems.length)buyBundle(selectedItems)};
  return <div className="editorial-page"><section className="editorial-cover"><img src={assetUrl(editorial.images[0])} alt={editorial.name}/><div><p>{editorial.kind}</p><h1>{editorial.name}</h1></div></section><section className="editorial-words"><p>{editorial.lead}</p><span>{editorial.description}</span></section><img className="editorial-detail" src={assetUrl(editorial.images[1])} alt={`Детали ${editorial.name}`}/><section className="editorial-words narrow"><p>{editorial.detail}</p></section><section className="editorial-split"><img src={assetUrl(editorial.images[2])} alt="Предметы коллекции"/><img src={assetUrl(editorial.images[3])} alt="Образ коллекции"/></section><section className={`editorial-products ${selecting?"selection-mode":""}`}><div className="editorial-products-head"><div><p>В {editorial.kind==="КАПСУЛА"?"КАПСУЛЕ":"КОЛЛЕКЦИИ"}</p><h2>Соберите весь образ</h2>{selecting&&<div className="selection-help"><span>Отметьте предметы, которые хотите купить</span><button onClick={()=>setSelectedIds(selectedIds.length===items.length?[]:items.map(item=>item.id))}>{selectedIds.length===items.length?"Снять выбор":"Выбрать всё"}</button></div>}</div><button className="primary total-cta" disabled={selecting&&!selectedItems.length} onClick={handleBundle}><span>{selecting?"ДОБАВИТЬ В КОРЗИНУ":"ВЫКУПИТЬ ВСЮ "+(editorial.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ")}</span><b>{fmt(total)}</b></button></div><div className="product-grid">{items.map(item=><div className={`selectable-product ${selectedIds.includes(item.id)?"selected":""}`} key={`${editorial.id}-${item.id}`}>{selecting&&<label className="product-selector"><input type="checkbox" checked={selectedIds.includes(item.id)} onChange={()=>toggle(item.id)}/><span><Icon name="plus"/></span><b>{selectedIds.includes(item.id)?"Выбрано":"Выбрать"}</b></label>}<ProductCard product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={favorites.includes(item.id)}/></div>)}</div></section></div>;
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

function ProductRecommendations({product,selectProduct,favorite,recentlyViewed}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void;recentlyViewed:number[]}){
  const merchGroupOf=(item:Product)=>{
    const preferred=findProductSku(item,item.selectedColor,item.selectedSize);
    const rows=preferred?[preferred,...(item.skus??[]).filter(sku=>sku.id!==preferred.id)]:(item.skus??[]);
    for(const row of rows){
      const value=(row.collection??row.capsule)?.trim();
      if(value)return value.toLocaleLowerCase("ru-RU");
    }
    return "";
  };
  const currentMerchGroup=merchGroupOf(product);
  const collectionProducts=currentMerchGroup
    ? products.filter(item=>item.id!==product.id&&merchGroupOf(item)===currentMerchGroup).slice(0,4)
    : [];
  const viewedProducts=recentlyViewed
    .filter(id=>id!==product.id)
    .map(id=>products.find(item=>item.id===id))
    .filter((item): item is Product=>Boolean(item))
    .slice(0,4);
  return <>
    {collectionProducts.length>0&&<section className="post-rich-recommendations collection-recommendations"><div className="section-head"><p>КОЛЛЕКЦИЯ / КАПСУЛА</p><h2>Товары из этой коллекции</h2></div><ProductRail className="recommendation-product-rail" items={collectionProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
    {viewedProducts.length>0&&<section className="post-rich-recommendations recently-viewed-recommendations" style={{marginTop:0,paddingTop:42}}><div className="section-head"><p>ИСТОРИЯ ПРОСМОТРОВ</p><h2>Вы недавно смотрели</h2></div><ProductRail className="recommendation-product-rail" items={viewedProducts} onProduct={selectProduct} onQuick={selectProduct} favorite={favorite} favorites={[]}/></section>}
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
  const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;

  return <div className="overlay navigation-overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><aside className="menu-panel zara-menu premium-menu"><div className="menu-top"><button onClick={close} aria-label="Закрыть меню"><Icon name="close"/></button><span><Icon name="pin"/> Бутики</span><b>КУЛЬТУРА ДОМА</b></div><div className="menu-body">{!current?<div className="menu-first level-one premium-menu-root">
    <button className="premium-menu-new" onClick={()=>openCatalog("Все товары")}><span>НОВИНКИ</span><Icon name="arrow"/></button>

    <section className="premium-menu-editorial" aria-label="Editorial и готовые решения">
      <small>EDITORIAL</small>
      <button type="button" onClick={()=>go("collections")}><span>КАПСУЛЫ И КОЛЛЕКЦИИ</span><Icon name="arrow"/></button>
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
