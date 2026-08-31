"use client";

import { assetUrl } from "./assets";
import { RemoteImage } from "./remote-image";
import { catalogProductOverrides, type CatalogSku } from "./catalog-data";
import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";
import { loadSiteDatabaseCatalogRows, SITE_DB_ADDRESS_SUGGESTIONS, SITE_DB_CITIES, SITE_DB_CONTACTS, SITE_DB_DELIVERY_METHODS, SITE_DB_PAYMENT_METHODS, SITE_DB_POLICIES, SITE_DB_PVZ_POINTS, SITE_DB_STORES, SITE_DB_STORE_POINTS, SITE_DB_COLOR_GROUPS, SITE_DB_COLOR_GROUP_MEMBERS } from "./site-database.generated";
// SITE_DATABASE_CONNECTED_V128
// TABLE_DRIVEN_CATALOG_IMAGES_V135

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
  category?: string;
  subcategory?: string;
  collection?: string;
  capsule?: string;
  readySolution?: string;
  optionalReadySolution?: string;
  switchBy?: "color" | "scent" | "none";
};

type ColorVariant = { name: string; hex: string; image: string; gallery?: string[]; position?: string };
type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number; giftWrap?: boolean };
type Slide = { category:string; eyebrow:string; title:string; subtitle:string; image:string; secondaryImage?:string; mobileVideo?:string; align:string; destination:View };
type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };

const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
// PRICE_PENDING_UI_V1
const priceKnown=(value:number)=>Number.isFinite(value)&&value>0;
// GROUPED_CATALOG_V95
// GROUPED_CATALOG_V94
// GROUPED_CATALOG_V93
const cleanNulls=(value:unknown)=>{const text=String(value??"").trim();return !text||text.toLowerCase()==="null"?undefined:text};
const splitMultiline=(value:unknown)=>{const text=cleanNulls(value);return text?text.split(/\\n|\n|\u2028|\u2029/g).map(part=>part.trim()).filter(Boolean):[]};
const renderMultiline=(value:unknown)=>{const parts=splitMultiline(value);return parts.length?<>{parts.map((part,index)=><span key={`${part}-${index}`} style={{display:"block",lineHeight:1.18,margin:0}}>{part}</span>)}</>:null};
const parseCatalogPrice=(value:unknown)=>Number(String(cleanNulls(value)??"").replace(/[^\d.,-]/g,"").replace(",","."))||0;
// CATALOG_PRODUCT_NORMALIZATION_V74
const isAromaProduct=(product:Product)=>product.switchBy==="scent";
const productCountLabel=(count:number)=>`${count} ${count===1?"товар":count>=2&&count<=4?"товара":"товаров"}`;
const runtimeStorefrontBase=()=>{
  const configured=(process.env.NEXT_PUBLIC_BASE_PATH??"").replace(/\/$/,"");
  if(configured)return configured;
  if(typeof window==="undefined")return "";
  const path=window.location.pathname;
  if(path==="/kd"||path.startsWith("/kd/"))return "/kd";
  if(window.location.hostname.endsWith("github.io")){const first=path.split("/").filter(Boolean)[0];return first?`/${first}`:""}
  return "";
};

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

type VariantSku=CatalogSku&{scent?:string;sourceColor?:string;volume?:string;oldPrice?:number};
const asVariantSku=(sku:CatalogSku|undefined)=>sku as VariantSku|undefined;
function skuPrimaryMatches(product:Product,sku:CatalogSku,primary?:string){if(!primary||product.switchBy==="none")return true;const extra=asVariantSku(sku);return isAromaProduct(product)?extra?.scent===primary:(extra?.sourceColor??sku.color)===primary}
function findProductSku(product:Product,primary?:string,size?:string,secondaryColor?:string){
  if(!product.skus?.length)return undefined;
  const match=(item:CatalogSku)=>skuPrimaryMatches(product,item,primary)&&(!secondaryColor||asVariantSku(item)?.sourceColor===secondaryColor)&&(!size||item.size===size);
  const selected=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
  if(selected&&match(selected))return selected;
  return product.skus.find(match)??product.skus.find(item=>skuPrimaryMatches(product,item,primary))??product.skus[0];
}
function getProductSecondaryColors(product:Product,primary?:string){
  if(!isAromaProduct(product)||!product.skus?.length)return [] as {name:string;hex:string}[];
  const map=new Map<string,{name:string;hex:string}>();
  product.skus.filter(item=>skuPrimaryMatches(product,item,primary)).forEach(item=>{const name=cleanNulls(asVariantSku(item)?.sourceColor);if(name&&!map.has(name))map.set(name,{name,hex:item.colorHex})});
  return Array.from(map.values());
}
function getProductSizeOptions(product:Product,primary?:string,secondaryColor?:string){
  if(product.skus?.length){const rows=product.skus.filter(item=>skuPrimaryMatches(product,item,primary)&&(!secondaryColor||asVariantSku(item)?.sourceColor===secondaryColor));return Array.from(new Map(rows.map(item=>[item.size,[item.size,item.price] as const])).values())}
  return [["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
}
const isUniversalSizeLabel=(value:unknown)=>String(cleanNulls(value)??"").trim().toLocaleLowerCase("ru-RU")==="единый размер";
function isProductSizeAvailable(product:Product,primary:string|undefined,size:string,secondaryColor?:string){const rows=product.skus?.filter(item=>skuPrimaryMatches(product,item,primary)&&(!secondaryColor||asVariantSku(item)?.sourceColor===secondaryColor)&&item.size===size);if(!rows?.length)return true;return rows.some(item=>item.available!==false)}
function getUnavailableProductSizes(product:Product,primary:string|undefined,sizes:readonly (readonly [string,number])[],secondaryColor?:string){return sizes.filter(([name])=>!isProductSizeAvailable(product,primary,name,secondaryColor)).map(([name])=>name)}

// GROUPED_CATALOG_V100
// GROUPED_CATALOG_V98
// GROUPED_CATALOG_V96
function getProductImages(product:Product){
  if(product.skus?.length){
    const selected=product.selectedSkuId?product.skus.find(item=>item.id===product.selectedSkuId):undefined;
    const sku=selected??product.skus[0];
    return Array.from(new Set([sku?.image,...(sku?.gallery??[])].map(cleanNulls).filter((value):value is string=>Boolean(value))));
  }
  const variant=product.selectedColor?product.colorVariants?.find(item=>item.name===product.selectedColor):undefined;
  const sources=variant?[variant.image,...(variant.gallery??product.gallery??[])]:[product.image,...(product.gallery??[])];
  return Array.from(new Set(sources.map(cleanNulls).filter((value):value is string=>Boolean(value))));
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
function DeferredProductCardMedia({product,alt,position}:{product:Product;alt:string;position?:string}){
  const images=getProductImages(product);
  const sources=images.length?images:[product.image];
  return <div className={`product-media-scroll horizontal-media ${sources.length>1?"is-scrollable":""}`} role="group" aria-label={`${alt}: ${sources.length} фото`} tabIndex={sources.length>1?0:-1}>
    {sources.map((src,index)=><RemoteImage key={`${src}-${index}`} src={src} alt={index===0?alt:`${alt}, фото ${index+1}`} loading="lazy" decoding="async" draggable={false} style={{objectPosition:position||product.position||"center"}}/>)}
  </div>;
}

function ProductRail({items,onProduct,onQuick,favorite,favorites,className=""}:{items:Product[];onProduct:(product:Product)=>void;onQuick:(product:Product)=>void;favorite:(id:number)=>void;favorites:number[];className?:string}){
  return <div className={`product-rail-shell ${className}`.trim()}>
    <div className="product-rail">{items.map(item=><ProductCard key={`${className}-${item.id}`} product={item} onClick={onProduct} onQuick={onQuick} favorite={favorite} liked={favorites.includes(item.id)}/>)}</div>
  </div>;
}

const baseProducts: Product[] = [];

const REMOVED_PRODUCT_IDS = new Set([1,9,1257,1259,1260,1261,1262,1263,1266,1267,1268,1270,1271,1273,1276,1287,1500,1565,1566,1669]);
// PRODUCT_PREVIEW_RULES_V1
const catalogPreviewColorByArticle:Record<string,string> = {
  "KD-PD-1028":"Белый",
  "KD-PD-1128":"Белый",
};
let products: Product[] = baseProducts.map(base=>{
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
if(CATALOG_PRODUCTS_GENERATED.length)products = CATALOG_PRODUCTS_GENERATED as unknown as Product[];


type CatalogMasterRow = Record<string,string>;
let catalogMasterLoaded = CATALOG_PRODUCTS_GENERATED.length>0;
const CATALOG_MASTER_FILES:string[] = ["catalog_master.csv"]; // CATALOG_MASTER_V107
const parseEntityCsv=(source:string):CatalogMasterRow[]=>{
  const text=source.replace(/^\uFEFF/,"");
  const headerLine=text.split(/\r?\n/,1)[0]??"";
  const delimiter=headerLine.includes(";")?";":",";
  const rows:string[][]=[]; let row:string[]=[]; let cell=""; let quoted=false;
  for(let index=0;index<text.length;index+=1){
    const char=text[index];
    if(quoted){
      if(char==='"'&&text[index+1]==='"'){cell+='"';index+=1}
      else if(char==='"')quoted=false;
      else cell+=char;
    }else if(char==='"')quoted=true;
    else if(char===delimiter){row.push(cell);cell=""}
    else if(char==="\n"){row.push(cell.replace(/\r$/,""));if(row.some(value=>value!==""))rows.push(row);row=[];cell=""}
    else cell+=char;
  }
  if(cell.length||row.length){row.push(cell.replace(/\r$/,""));if(row.some(value=>value!==""))rows.push(row)}
  const [headers=[], ...body]=rows;
  return body.map(values=>Object.fromEntries(headers.map((header,index)=>[header.trim(),values[index]??""])));
};
const entityColorHex=(value:string)=>{
  const key=String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/\s+/g," ");
  const colors:Record<string,string>={'бежевый':"#CDB99B",'белый':"#F5F5F2",'белый / голубой':"#93B8CB",'белый / золотой':"#B89A5A",'голубой':"#93B8CB",'желтый':"#D9B84E",'зеленый':"#657A61",'коричневый':"#765A46",'красный':"#9E403B",'ледяной голубой':"#93B8CB",'молочный':"#EEE7DA",'ночной синий':"#142A45",'прозрачный':"#F3F4F2",'пудровый':"#D8B0A4",'серебряный':"#B9B9B4",'серо-синий':"#667B89",'синий':"#496C8A",'черный':"#1D1D1B",'экрю':"#DED0B6"};
  return colors[key]??"#8F8A82";
};
const entityId=(article:string,name:string)=>300000+Array.from(`${article}|${name}`).reduce((sum,char)=>((sum*31)+char.charCodeAt(0))%500000,0);
const tableAssetImage=(value:unknown)=>{const image=cleanNulls(value);if(!image)return undefined;if(image.startsWith("/assets/"))return image;if(image.startsWith("assets/"))return `/${image}`;return undefined};
async function loadCatalogMasterIntoProducts(){
  if(catalogMasterLoaded&&products.length)return;
  const base=runtimeStorefrontBase();
  let databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);
  if(!databaseRows.length&&typeof window!=="undefined"){
    try{
      const directUrl=new URL(`${base}/data/catalog_master.csv`,window.location.origin).toString();
      const response=await fetch(directUrl,{cache:"force-cache"});
      if(response.ok)databaseRows=parseEntityCsv(await response.text());
    }catch{}
  }
  const sourceRows=databaseRows;
  const rows=sourceRows.map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as CatalogMasterRow).filter(row=>row["Артикул"]&&row["Название товара"]);
  if(!rows.length){catalogMasterLoaded=false;return;}
  catalogMasterLoaded=true;
  const grouped=new Map<string,CatalogMasterRow[]>();
  rows.forEach(row=>{const key=String(row["Артикул"]||"").trim();const list=grouped.get(key)||[];list.push(row);grouped.set(key,list)});
  // Product identity follows the canonical article: every table row with the same article is one product with SKU variants.
  // ARTICLE_PRIMARY_GROUPING_V86
  // CANONICAL_TABLE_SYNC_V85
  const incoming:Product[]=[];
  grouped.forEach((variants)=>{
    const first=variants[0],article=cleanNulls(first["Артикул"])??"",name=cleanNulls(first["Название товара"])??article;
    const existing=products.find(product=>String(product.article||"").trim()===article),id=existing?.id??entityId(article,name);
    const category=cleanNulls(first["Категория"]),subcategory=cleanNulls(first["Подкатегория"]);
    const colors=Array.from(new Set(variants.map(row=>cleanNulls(row["Цвет"])).filter(Boolean))),scents=Array.from(new Set(variants.map(row=>cleanNulls(row["Аромат"])).filter(Boolean)));
    const scentMode=scents.length>0&&variants.length>1;
    const switchBy:Product["switchBy"]=scentMode?"scent":colors.length>1?"color":"none";
    const skus:CatalogSku[]=variants.map((row,index)=>{
      const images=[row["Фото 1"],row["Фото 2"],row["Фото 3"]].map(tableAssetImage).filter((value):value is string=>Boolean(value));
      const sourceColor=cleanNulls(row["Цвет"]),scent=cleanNulls(row["Аромат"]),key=(switchBy==="scent"?scent:switchBy==="color"?sourceColor:undefined)??"Единый вариант";
      const size=cleanNulls(row["Размер"])??cleanNulls(row["Объем"])??cleanNulls(row["Диаметр"])??"Единый размер",price=parseCatalogPrice(row["Цена"]),oldPrice=parseCatalogPrice(row["Старая цена"]);
      return {id:`master-${id}-${index}`,article,productId:id,color:key,colorHex:entityColorHex(sourceColor??key),size,height:cleanNulls(row["Высота"]),width:cleanNulls(row["Ширина"]),diameter:cleanNulls(row["Диаметр"]),packageInfo:cleanNulls(row["Комплектация / информация о размере"]),material:cleanNulls(row["Материал"])??"",composition:cleanNulls(row["Состав"])??"",details:cleanNulls(row["Детали"]),collection:cleanNulls(row["Коллекция"]),capsule:cleanNulls(row["Капсула"]),price,image:images[0]??"/assets/images/image-placeholder.svg",gallery:images.slice(1),available:true,...({volume:cleanNulls(row["Объем"]),oldPrice:oldPrice>price?oldPrice:undefined,sourceColor,scent} as any)};
    });
    const firstSku=skus[0],priced=skus.filter(item=>priceKnown(item.price)),minSku=priced.reduce<CatalogSku|undefined>((best,item)=>!best||item.price<best.price?item:best,undefined),price=minSku?.price??0;
    const switchRows=Array.from(new Map(skus.map(item=>[item.color,item])).values());
    incoming.push({id,name,article,note:[cleanNulls(firstSku.material),cleanNulls(firstSku.size)].filter(Boolean).join(", "),price,oldPrice:Number((minSku as any)?.oldPrice)||undefined,image:firstSku.image,gallery:firstSku.gallery,skus,colorVariants:switchRows.map(item=>({name:item.color,hex:item.colorHex,image:item.image,gallery:item.gallery})),category,subcategory,collection:cleanNulls(first["Коллекция"]),capsule:cleanNulls(first["Капсула"]),readySolution:cleanNulls(first["Товар входит в готовое решение"]),optionalReadySolution:cleanNulls(first["Опционально входит в готовое решение"]),switchBy});
  });
  products=incoming;
  const tableCollectionNames=Array.from(new Set(rows.map(row=>String(row["Коллекция"]||"").trim()).filter(Boolean)));
  const editorialKey=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
  const previousEditorials=new Map(editorials.map(item=>[editorialKey(item.name),item]));
  editorials=tableCollectionNames.map((collection,index)=>{
    const productIds=products.filter(product=>product.skus?.some(sku=>String(sku.collection||"").trim()===collection)).map(product=>product.id);
    const productImages=Array.from(new Set(products.filter(product=>productIds.includes(product.id)).flatMap(product=>[product.image,...(product.gallery??[])])).values()).filter(Boolean).slice(0,3);
    const previous=previousEditorials.get(editorialKey(collection));
    const next:Editorial=previous
      ? {...previous,name:collection,kind:"КОЛЛЕКЦИЯ",productIds,images:previous.images?.length?previous.images:productImages}
      : {id:`table-collection-${index+1}`,name:collection,kind:"КОЛЛЕКЦИЯ",lead:"Предметы коллекции, собранные в единую историю для дома.",detail:"Откройте коллекцию и выберите предметы, которые работают вместе.",description:`Коллекция «${collection}» по актуальной товарной таблице Культура Дома.`,images:productImages.length?productImages:["/assets/images/image-placeholder.svg"],productIds};
    return next;
  });
}

const slides:Slide[] = [
  { category: "НОВИНКИ", eyebrow: "НОВАЯ ГЛАВА", title: "Дом в цвету", subtitle: "Авторские вазы и сервировка для долгих летних встреч", image: "/assets/images/editorial-vases.webp", secondaryImage: "/assets/images/editorial-table.webp", mobileVideo: "/assets/images/kultura-home-mobile.mp4", align: "left", destination: "catalog" as View },
  { category: "СПАЛЬНЯ", eyebrow: "СПАЛЬНЯ", title: "Белая глава", subtitle: "Постельное бельё с деликатной вышивкой", image: "/assets/images/russian-bedroom.png", align: "left", destination: "catalog" as View },
  { category: "ДЕКОР ДЛЯ ДОМА", eyebrow: "ТИХИЕ ДЕТАЛИ", title: "Естественные оттенки", subtitle: "Тактильный декор для спокойного интерьера", image: "/assets/images/beige-bedroom.png", align: "left", destination: "catalog" as View },
];

const discountOf = (product: Product) => product.oldPrice ? Math.round((1-product.price/product.oldPrice)*100) : 0;

const categories = [
  ["Спальня", "/assets/images/classic-bedroom.png"],
  ["Кухня и столовая", "/assets/images/moon-plate.png"],
  ["Коллекции", "/assets/images/time-collection.png"],
  ["Домашний текстиль", "/assets/images/russian-bedroom.png"],
  ["Ванная", "/assets/images/zip-product-bed.png"],
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

const collectionEditorialProducts:Product[] = [];

// COLLECTIONS_REDESIGN_V65
const normalizeRetiredCatalogName=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/[‐‑‒–—]/g,"-").replace(/\s+/g," ");
const isRetiredCatalogProduct=(name:string)=>{const value=normalizeRetiredCatalogName(name);return value.includes("мокоши")||value.includes("овация")||/жар(?:-| )?птица/.test(value)};
if(!CATALOG_PRODUCTS_GENERATED.length){if(!CATALOG_PRODUCTS_GENERATED.length){if(!CATALOG_PRODUCTS_GENERATED.length){if(!CATALOG_PRODUCTS_GENERATED.length){for(let index=products.length-1;index>=0;index-=1){if(isRetiredCatalogProduct(products[index].name))products.splice(index,1)}}}}}
// READY_SOLUTIONS_MERCH_V75
type Editorial = { id:string; name:string; kind:"КАПСУЛА"|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string[]; productIds:number[] };
// COLLECTIONS_REDESIGN_V65_INDEX
const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>!REMOVED_PRODUCT_IDS.has(item.id)&&item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);
let editorials:Editorial[] = [
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/assets/images/caps_led.png","/assets/images/caps_led_podyshka.png","/assets/images/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КОЛЛЕКЦИЯ", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю.", description:"Коллекция о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/assets/images/caps_luna_postel.png","/assets/images/caps_luna_postel2.png","/assets/images/caps_luna_serviz.png"], productIds:[4,10,5,6,3] },
  { id:"echo", name:"Эхо", kind:"КОЛЛЕКЦИЯ", lead:"Светлый фарфор и тонкий рельеф для спокойной современной сервировки.", detail:"Эхо строится на белом костяном фарфоре и мягком повторении формы.", description:"Чистая сервировка, где декоративность проявляется через пропорции, рельеф и свет.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg"], productIds:collectionProductIds("Эхо") },
  { id:"niti", name:"Нити", kind:"КОЛЛЕКЦИЯ", lead:"Синий орнамент, сатин и фарфор связывают текстиль и сервировку.", detail:"Нити соединяет предметы стола и мягкий декор через холодную синюю палитру.", description:"Коллекция о повторяющемся орнаменте и тактильных слоях.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/assets/images/69e5d18433139_big__83f18d3de5.jpg"], productIds:collectionProductIds("Нити") },
  { id:"phoenix", name:"Феникс", kind:"КОЛЛЕКЦИЯ", lead:"Тёплые акценты и выразительный орнамент для дома с характером.", detail:"Феникс объединяет сервировку и атмосферный декор в единую историю.", description:"Выразительная коллекция с сильным мотивом и спокойной базой.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg"], productIds:collectionProductIds("Феникс") },
];

export default function Home({initialView="home",initialCatalogCategory="Все товары"}:{initialView?:View;initialCatalogCategory?:string}={}) {
  const [catalogDataReady,setCatalogDataReady]=useState(()=>products.length>0);
  const [catalogDataError,setCatalogDataError]=useState(false);
  const reloadCatalogData=()=>{catalogMasterLoaded=false;setCatalogDataReady(false);setCatalogDataError(false);void loadCatalogMasterIntoProducts().then(()=>{const ready=products.length>0;setCatalogDataReady(ready);setCatalogDataError(!ready)})};
  useEffect(()=>{let mounted=true;void loadCatalogMasterIntoProducts().then(()=>{if(!mounted)return;const ready=products.length>0;setCatalogDataReady(ready);setCatalogDataError(!ready)});return()=>{mounted=false}},[]);
  useEffect(()=>setCatalogCategory(initialCatalogCategory),[initialCatalogCategory]);
  const [view, setView] = useState<View>(initialView);
  const [menu, setMenu] = useState(false);
  const [menuSection, setMenuSection] = useState("");
  const [search, setSearch] = useState(false);
  const [account, setAccount] = useState(false);
  const [favoritesOpen, setFavoritesOpen] = useState(false);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [filters, setFilters] = useState(false);
  const [plpSize, setPlpSize] = useState<Product | null>(null);
  const [plpAdded, setPlpAdded] = useState<CartItem | null>(null);
  const [selected, setSelected] = useState<Product>(()=>products[1]??products[0]??({id:0,name:"",note:"",price:0,image:"/assets/images/image-placeholder.svg"} as Product));
  const [editorial, setEditorial] = useState<Editorial>(editorials[0]);
  const [catalogCategory,setCatalogCategory]=useState(initialCatalogCategory);
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
  const go = (next: View) => { if(next==="home"){window.location.href=`${runtimeStorefrontBase()}/`;return;} setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };
  const openCatalog=(category="Все товары")=>{setCatalogCategory(category);go("catalog");window.history.pushState({},"",`${runtimeStorefrontBase()}/catalog/?category=${encodeURIComponent(category)}`)};
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
      {view === "catalog" && (catalogDataReady?<CatalogView initialCategory={catalogCategory} onFilter={() => setFilters(true)} onAdd={setPlpSize} onProduct={openProduct} favorite={favorite} favorites={favorites} />:<CatalogBootStateV141 error={catalogDataError} retry={reloadCatalogData}/>)}
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

function CatalogBootStateV141({error,retry}:{error:boolean;retry:()=>void}){
  return <section className="catalog-boot-v141" aria-live="polite"><p>КАТАЛОГ</p><h1>{error?"Не удалось загрузить каталог":"Загружаем каталог"}</h1>{error?<><p className="catalog-boot-v141-error">Проверьте соединение и попробуйте ещё раз.</p><button type="button" onClick={retry}>Повторить</button></>:<div className="catalog-boot-v141-grid" aria-hidden="true">{Array.from({length:6},(_,index)=><div className="catalog-boot-v141-card" key={index}><span/><i/><b/></div>)}</div>}</section>;
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
  const legacyBoutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124},
  ];
  const boutiques=SITE_DB_STORES.length?SITE_DB_STORES:legacyBoutiques;
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

// EDITORIAL_COMMERCE_V81
function HomeView({ go, openCatalog, slide, setSlide, onProduct, favorite, favorites, onAdd, openEditorial }: { go:(v:View)=>void; openCatalog:(category?:string)=>void; slide:number; setSlide:(n:number)=>void; onProduct:(product:Product)=>void; favorite:(n:number)=>void; favorites:number[]; onAdd:(product:Product)=>void; openEditorial:(editorial:Editorial)=>void }) {
  // HOME_REDESIGN_V113 — supplied homepage ZIP, 47 source photographs represented.
  void openEditorial;
  const readyBase=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const heroSlides=[
    {eyebrow:"НОВИНКИ",title:"Новые истории дома",text:"Предметы, которые собирают пространство в цельный образ — от спальни до сервировки.",cta:"Смотреть новинки",desktop:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png",action:()=>openCatalog()},
    {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой",text:"Сатин, мягкий свет и спокойные оттенки для пространства, в котором хочется остаться.",cta:"Перейти в спальню",desktop:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png",action:()=>openCatalog("Постельное белье")},
    {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал",text:"Фарфор, текстиль и детали стола в современной культуре русского дома.",cta:"Смотреть сервировку",desktop:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png",action:()=>openCatalog("Посуда и сервировка")},
  ];
  const active=((slide%heroSlides.length)+heroSlides.length)%heroSlides.length;
  const hero=heroSlides[active];
  const atlasStyle=(index:number)=>({
    backgroundImage:`url("${assetUrl("/assets/images/home113-editorial-atlas.svg")}")`,
    backgroundSize:"600% 700%",
    backgroundPosition:`${(index%6)*20}% ${(Math.floor(index/6)*100)/6}%`,
  });
  const categories=[
    {title:"Спальня",note:"Постельное бельё",image:"/assets/images/1spal.png",action:()=>openCatalog("Постельное белье")},
    {title:"Посуда и сервировка",note:"Кухня и столовая",image:"/assets/images/2stol.png",action:()=>openCatalog("Посуда и сервировка")},
    {title:"Столовый текстиль",note:"Скатерти, салфетки, дорожки",image:"/assets/images/3stoltekstil.png",action:()=>openCatalog("Столовый текстиль")},
    {title:"Декор",note:"Предметы для дома",image:"/assets/images/4dekor.png",action:()=>openCatalog("Декор для дома")},
    {title:"Текстиль для дома",note:"Пледы и подушки",image:"/assets/images/5homeclothes.png",action:()=>openCatalog("Пледы и подушки")},
    {title:"Ванная",note:"Для ежедневных ритуалов",image:"/assets/images/6van.png",action:()=>openCatalog()},
    {title:"Outlet",note:"Особые предложения",image:"/assets/images/7outlet.png",action:()=>openCatalog()},
  ];
  const newProducts=products.slice(0,12);
  const capsules=[
    {title:"Нити",meta:"КАПСУЛА · ТЕКСТИЛЬ",imageIndex:7},
    {title:"Тайна",meta:"КАПСУЛА · ТЁМНАЯ ЭСТЕТИКА",imageIndex:22},
    {title:"Ледяные узоры",meta:"КАПСУЛА · ЗИМНЯЯ ИСТОРИЯ",imageIndex:18},
    {title:"Лунная сказка",meta:"КАПСУЛА · СПАЛЬНЯ И СЕРВИРОВКА",imageIndex:12},
    {title:"Феникс",meta:"КАПСУЛА · ДЕКОР",imageIndex:9},
  ];
  const solutions=[
    {title:"Зелёный салон",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Свежая сервировка с зелёными акцентами и светлым текстилем.",indices:[25,26],href:`${readyBase}/ready-solutions/green-salon/`},
    {title:"Красные линии",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Графичная композиция, построенная на красных акцентах и белом фарфоре.",indices:[27,28],href:`${readyBase}/ready-solutions/red-lines/`},
    {title:"Зимняя сказка",meta:"ГОТОВОЕ РЕШЕНИЕ · ДОМ",copy:"Сценарий для зимнего дома: спальня, стол и декор в единой холодной палитре.",indices:[29,30,31,32,33,34],href:`${readyBase}/ready-solutions/winter-fairy-tale/`},
    {title:"Пламя морских глубин",meta:"ГОТОВОЕ РЕШЕНИЕ · СТОЛОВАЯ",copy:"Глубокий синий и тёплый свет — драматичная композиция для вечерней сервировки.",indices:[35,36,37],href:`${readyBase}/ready-solutions/`},
    {title:"Тёплый брутализм",meta:"ГОТОВОЕ РЕШЕНИЕ · ИНТЕРЬЕР",copy:"Кожа, дерево и сдержанные фактуры в собранном мужском интерьере.",indices:[38,39,40],href:`${readyBase}/ready-solutions/warm-brutalism/`},
  ];

  return <main className="home-v113">
    <nav className="home113-nav" aria-label="Навигация по главной">
      <button type="button" onClick={()=>openCatalog()}>Новинки</button>
      <button type="button" onClick={()=>openCatalog("Постельное белье")}>Спальня</button>
      <button type="button" onClick={()=>openCatalog("Посуда и сервировка")}>Кухня и столовая</button>
      <button type="button" onClick={()=>openCatalog("Декор для дома")}>Декор</button>
      <button type="button" onClick={()=>go("collections")}>Капсулы</button>
      <a href={`${readyBase}/ready-solutions/`}>Готовые решения</a>
    </nav>

    <section className="home113-hero" aria-label="Главные истории">
      <div className="home113-hero-art home113-hero-art-desktop" aria-hidden="true" style={{backgroundImage:`url("${assetUrl(hero.desktop)}")`}}/>
      <div className="home113-hero-art home113-hero-art-mobile" aria-hidden="true" style={{backgroundImage:`url("${assetUrl(hero.mobile)}")`}}/>
      <div className="home113-hero-shade"/>
      <div className="home113-hero-copy">
        <small>{hero.eyebrow}</small>
        <h1>{hero.title}</h1>
        <p>{hero.text}</p>
        <button type="button" onClick={hero.action}>{hero.cta}<span aria-hidden="true">↗</span></button>
      </div>
      <div className="home113-hero-controls" aria-label="Выбор баннера">{heroSlides.map((item,index)=><button type="button" key={item.title} className={index===active?"is-active":""} onClick={()=>setSlide(index)}><span>{String(index+1).padStart(2,"0")}</span><b>{item.eyebrow}</b></button>)}</div>
    </section>

    <section className="home113-section home113-category-section">
      <header className="home113-section-head"><div><small>КАТАЛОГ</small><h2>Пространства дома</h2></div><p>Начните с комнаты или категории — дальше предметы складываются в общую композицию.</p></header>
      <div className="home113-category-rail">{categories.map(item=><button type="button" key={item.title} className="home113-category-card" onClick={item.action}><span className="home113-atlas-card home113-category-image" role="img" aria-label={item.title} style={{backgroundImage:`url("${assetUrl(item.image)}")`,backgroundSize:"cover",backgroundPosition:"center center",backgroundRepeat:"no-repeat"}}/><strong>{item.title}</strong><small>{item.note}</small></button>)}</div>
    </section>

    {/* HOME_NEW_PRODUCTS_CAPSULES_V117 */}
    <section className="home117-new-products" aria-labelledby="home117-new-products-title">
      <header className="home117-section-head"><div><small>КАТАЛОГ</small><h2 id="home117-new-products-title">Новинки</h2></div><button type="button" onClick={()=>openCatalog()}>Смотреть все</button></header>
      <div className="home117-product-rail" aria-label="Новинки товаров">{newProducts.map(product=><div className="home117-product-item" key={`home-new-${product.id}`}><ProductCard product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/></div>)}</div>
    </section>

    <section className="home113-capsules home117-capsules" aria-labelledby="home117-capsules-title">
      <header className="home117-section-head home117-capsules-head"><div><small>КАПСУЛЫ</small><h2 id="home117-capsules-title">Капсулы</h2></div><button type="button" onClick={()=>go("collections")}>Смотреть все</button></header>
      <div className="home117-capsule-rail" aria-label="Капсулы Культура дома">{capsules.map(item=><article className="home117-capsule-card" key={item.title}>
        <button type="button" className="home117-capsule-media" onClick={()=>go("collections")} aria-label={`Открыть капсулу ${item.title}`}><span role="img" aria-label={item.title} style={atlasStyle(item.imageIndex)}/></button>
        <div className="home117-capsule-copy"><small>{item.meta}</small><button type="button" onClick={()=>go("collections")}><h3>{item.title}</h3></button><button type="button" className="home117-capsule-link" onClick={()=>go("collections")}>Смотреть капсулу</button></div>
      </article>)}</div>
    </section>

    <section className="home113-solutions">
      <header className="home113-editorial-head home113-editorial-head-light"><small>ГОТОВЫЕ РЕШЕНИЯ</small><h2>Интерьер уже собран</h2><p>Выберите готовую композицию как отправную точку и настройте предметы под своё пространство.</p><a href={`${readyBase}/ready-solutions/`}>Все готовые решения</a></header>
      <div className="home113-solution-list">{solutions.map(item=><article className="home113-solution" key={item.title}>
        <div className="home113-solution-copy"><small>{item.meta}</small><h3>{item.title}</h3><p>{item.copy}</p><a href={item.href}>Собрать решение <span aria-hidden="true">↗</span></a></div>
        <div className="home113-photo-rail home113-solution-rail" aria-label={`Фотографии решения ${item.title}`}>{item.indices.map((atlasIndex,imageIndex)=><a href={item.href} key={atlasIndex} className="home113-photo-card" aria-label={`${item.title}, фото ${imageIndex+1}`}><span role="img" aria-label={`${item.title}, фото ${imageIndex+1}`} style={atlasStyle(atlasIndex)}/></a>)}</div>
      </article>)}</div>
    </section>

    <HomeBoutiques/>
  </main>;
}

// CATALOG_FILTERS_V123
// CATALOG_FILTERS_UX_V125
type CatalogSortV123 = "popular" | "price_asc" | "price_desc";
type CatalogMultiFilterKeyV123 = "subcategories" | "collections" | "capsules" | "materials" | "sizes" | "colors";
type CatalogFilterGroupV123 = "subcategory" | "collection" | "material" | "size" | "color" | "price";
type CatalogFiltersV123 = {
  subcategories:string[];
  collections:string[];
  capsules:string[];
  materials:string[];
  sizes:string[];
  colors:string[];
  priceFrom:string;
  priceTo:string;
};
type CatalogForcedFacetV123 = {group:CatalogFilterGroupV123;value:string;kind?:"collection"|"capsule"};

const emptyCatalogFiltersV123=():CatalogFiltersV123=>({subcategories:[],collections:[],capsules:[],materials:[],sizes:[],colors:[],priceFrom:"",priceTo:""});
const cloneCatalogFiltersV123=(filters:CatalogFiltersV123):CatalogFiltersV123=>({...filters,subcategories:[...filters.subcategories],collections:[...filters.collections],capsules:[...filters.capsules],materials:[...filters.materials],sizes:[...filters.sizes],colors:[...filters.colors]});
const facetNormV123=(value:unknown)=>String(cleanNulls(value)??"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
const sameFacetV123=(left:unknown,right:unknown)=>facetNormV123(left)===facetNormV123(right);
const hasFacetValueV123=(values:string[],value:string)=>values.some(item=>sameFacetV123(item,value));
const withoutFacetValueV123=(values:string[],value:string)=>values.filter(item=>!sameFacetV123(item,value));
const uniqueFacetValuesV123=(values:(string|undefined)[])=>Array.from(new Map(values.map(cleanNulls).filter((value):value is string=>Boolean(value)).map(value=>[facetNormV123(value),value])).values());
const catalogSkuColorV123=(sku:CatalogSku)=>cleanNulls(asVariantSku(sku)?.sourceColor)??cleanNulls(sku.color)??"";
// CATALOG_COLOR_GROUPS_V131
const catalogColorGroupMembersV131=(()=>{
  const map=new Map<string,string[]>();
  SITE_DB_COLOR_GROUP_MEMBERS.forEach(row=>{
    const key=facetNormV123(row.color_name),name=cleanNulls(row.group_name);
    if(!key||!name)return;
    const list=map.get(key)??[];
    if(!list.some(item=>sameFacetV123(item,name)))list.push(name);
    map.set(key,list);
  });
  return map;
})();
const catalogColorGroupHexesV131=new Map(SITE_DB_COLOR_GROUPS.map(row=>[facetNormV123(row.group_name),row.swatch_hex||"#e8e5df"]));
const catalogSkuColorGroupsV131=(sku:CatalogSku)=>{
  const raw=catalogSkuColorV123(sku),exact=catalogColorGroupMembersV131.get(facetNormV123(raw));
  if(exact?.length)return exact;
  const groups=raw.split(/\s*\/\s*/).flatMap(part=>catalogColorGroupMembersV131.get(facetNormV123(part))??[part]).filter(Boolean);
  return uniqueFacetValuesV123(groups);
};
const catalogColorGroupHexV131=(name:string)=>catalogColorGroupHexesV131.get(facetNormV123(name))??"#e8e5df";
const normalizeCatalogColorFiltersV131=(values:string[])=>uniqueFacetValuesV123(values.flatMap(value=>catalogColorGroupMembersV131.get(facetNormV123(value))??[value]));
const availableCatalogSkusV123=(product:Product)=>product.skus?.filter(sku=>sku.available!==false)??[];
const parseCatalogBoundV123=(value:string)=>{const text=String(value??"").trim();if(!text)return undefined;const parsed=Number(text.replace(/\s/g,""));return Number.isFinite(parsed)&&parsed>=0?parsed:undefined};
const catalogNumberV123=(value:number)=>new Intl.NumberFormat("ru-RU").format(Math.round(value));

function toggleCatalogFilterValueV123(filters:CatalogFiltersV123,key:CatalogMultiFilterKeyV123,value:string):CatalogFiltersV123{
  const current=filters[key];
  return {...filters,[key]:hasFacetValueV123(current,value)?withoutFacetValueV123(current,value):[...current,value]};
}

function skuMatchesCatalogFiltersV123(sku:CatalogSku,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const material=cleanNulls(sku.material)??"";
  const size=cleanNulls(sku.size)??"";
  const color=catalogSkuColorV123(sku);
  const colorGroups=catalogSkuColorGroupsV131(sku);
  const price=Number(sku.price)||0;
  if(ignore!=="material"&&filters.materials.length&&!filters.materials.some(value=>sameFacetV123(value,material)))return false;
  if(ignore!=="size"&&filters.sizes.length&&!filters.sizes.some(value=>sameFacetV123(value,size)))return false;
  if(ignore!=="color"&&filters.colors.length&&!filters.colors.some(value=>colorGroups.some(group=>sameFacetV123(value,group))))return false;
  if(ignore!=="price"){
    const from=parseCatalogBoundV123(filters.priceFrom),to=parseCatalogBoundV123(filters.priceTo);
    if(from!==undefined&&price<from)return false;
    if(to!==undefined&&price>to)return false;
  }
  if(forced?.group==="material"&&!sameFacetV123(material,forced.value))return false;
  if(forced?.group==="size"&&!sameFacetV123(size,forced.value))return false;
  if(forced?.group==="color"&&!colorGroups.some(group=>sameFacetV123(group,forced.value)))return false;
  return true;
}

function catalogMatchingSkusV123(product:Product,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const skus=availableCatalogSkusV123(product);
  if(skus.length)return skus.filter(sku=>skuMatchesCatalogFiltersV123(sku,filters,ignore,forced));
  if(forced&&["material","size","color"].includes(forced.group))return [];
  if(ignore!=="price"){
    const from=parseCatalogBoundV123(filters.priceFrom),to=parseCatalogBoundV123(filters.priceTo),price=Number(product.price)||0;
    if(from!==undefined&&price<from)return [];
    if(to!==undefined&&price>to)return [];
  }
  if((ignore!=="material"&&filters.materials.length)||(ignore!=="size"&&filters.sizes.length)||(ignore!=="color"&&filters.colors.length))return [];
  return [null] as (CatalogSku|null)[];
}

function matchesCatalogProductV123(product:Product,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const subcategory=cleanNulls(product.subcategory)??"";
  const collection=cleanNulls(product.collection)??"";
  const capsule=cleanNulls(product.capsule)??"";
  if(ignore!=="subcategory"&&filters.subcategories.length&&!filters.subcategories.some(value=>sameFacetV123(value,subcategory)))return false;
  if(forced?.group==="subcategory"&&!sameFacetV123(subcategory,forced.value))return false;
  if(ignore!=="collection"&&(filters.collections.length||filters.capsules.length)){
    const collectionMatch=filters.collections.some(value=>sameFacetV123(value,collection));
    const capsuleMatch=filters.capsules.some(value=>sameFacetV123(value,capsule));
    if(!collectionMatch&&!capsuleMatch)return false;
  }
  if(forced?.group==="collection"){
    if(forced.kind==="capsule"&&!sameFacetV123(capsule,forced.value))return false;
    if(forced.kind!=="capsule"&&!sameFacetV123(collection,forced.value))return false;
  }
  return catalogMatchingSkusV123(product,filters,ignore,forced).length>0;
}

function catalogFilterDisplayProductV123(product:Product,filters:CatalogFiltersV123){
  const hasSkuFilter=filters.materials.length||filters.sizes.length||filters.colors.length||filters.priceFrom||filters.priceTo;
  if(!hasSkuFilter)return product;
  const matchingSkus=catalogMatchingSkusV123(product,filters).filter((sku):sku is CatalogSku=>Boolean(sku));
  const sku=matchingSkus[0];
  if(!sku)return product;
  const primary=isAromaProduct(product)?sku.color:catalogSkuColorV123(sku);
  return {...product,image:sku.image,gallery:sku.gallery,selectedColor:primary||product.selectedColor,selectedSize:filters.sizes.length?sku.size:product.selectedSize,selectedSkuId:sku.id,...({catalogFilterSkuIds:matchingSkus.map(item=>item.id)} as any)};
}

function catalogSortPriceV123(product:Product,filters:CatalogFiltersV123){
  const prices=catalogMatchingSkusV123(product,filters).map(sku=>sku?Number(sku.price)||0:Number(product.price)||0).filter(price=>priceKnown(price));
  return prices.length?Math.min(...prices):(Number(product.price)||0);
}

function CatalogFilterOptionV123({label,count,checked,disabled,onChange,swatch,kind}:{label:string;count:number;checked:boolean;disabled:boolean;onChange:()=>void;swatch?:string;kind?:string}){
  return <label className={`catalog-filter-option-v123 ${disabled?"is-disabled":""}`}><input type="checkbox" checked={checked} disabled={disabled&&!checked} onChange={onChange}/>{swatch&&<span className="catalog-filter-swatch-v123" style={{background:swatch}} aria-hidden="true"/>}<span className="catalog-filter-option-label-v123">{label}{kind&&<small>{kind}</small>}</span><span className="catalog-filter-count-v123">{count}</span></label>;
}

function CatalogView({ initialCategory, onFilter:_onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {
  const [sort,setSort]=useState<CatalogSortV123>("popular");
  const [filterOpen,setFilterOpen]=useState(false);
  const [applied,setApplied]=useState<CatalogFiltersV123>(()=>emptyCatalogFiltersV123());
  const [draft,setDraft]=useState<CatalogFiltersV123>(()=>emptyCatalogFiltersV123());
  const [visibleCount,setVisibleCount]=useState(18);
  const loadMoreRef=useRef<HTMLDivElement>(null);
  const categoryNames=Array.from(new Set(products.map(product=>cleanNulls(product.category)).filter((value):value is string=>Boolean(value))));
  const categoryKey=categoryNames.join("|");
  const resolveCategory=(value:string)=>categoryNames.find(name=>sameFacetV123(name,value))??"Все товары";
  const [category,setCategory]=useState(()=>resolveCategory(initialCategory));
  const popularityIndex=new Map(products.map((product,index)=>[product.id,index]));

  const parseFiltersFromUrl=()=>{
    const params=new URLSearchParams(window.location.search);
    const list=(key:string)=>params.getAll(key).flatMap(value=>value.split(",")).map(value=>value.trim()).filter(Boolean);
    const filters:CatalogFiltersV123={subcategories:list("subcategory"),collections:list("collection"),capsules:list("capsule"),materials:list("material"),sizes:list("size"),colors:normalizeCatalogColorFiltersV131(list("color")),priceFrom:params.get("price_from")??"",priceTo:params.get("price_to")??""};
    const rawSort=params.get("sort");
    const nextSort:CatalogSortV123=rawSort==="price_asc"||rawSort==="price_desc"?rawSort:"popular";
    const nextCategory=resolveCategory(params.get("category")||initialCategory);
    return {filters,nextSort,nextCategory};
  };

  const writeCatalogUrl=(filters:CatalogFiltersV123,nextSort:CatalogSortV123,nextCategory:string,mode:"push"|"replace"="push")=>{
    if(typeof window==="undefined")return;
    const params=new URLSearchParams();
    params.set("category",nextCategory);
    params.set("sort",nextSort);
    filters.subcategories.forEach(value=>params.append("subcategory",value));
    filters.collections.forEach(value=>params.append("collection",value));
    filters.capsules.forEach(value=>params.append("capsule",value));
    filters.materials.forEach(value=>params.append("material",value));
    filters.sizes.forEach(value=>params.append("size",value));
    filters.colors.forEach(value=>params.append("color",value));
    if(filters.priceFrom)params.set("price_from",filters.priceFrom);
    if(filters.priceTo)params.set("price_to",filters.priceTo);
    const next=`${window.location.pathname}?${params.toString()}`;
    window.history[mode==="push"?"pushState":"replaceState"]({},"",next);
  };

  useEffect(()=>{
    if(typeof window==="undefined")return;
    const restore=()=>{const state=parseFiltersFromUrl();setCategory(state.nextCategory);setSort(state.nextSort);setApplied(state.filters);setDraft(cloneCatalogFiltersV123(state.filters));setFilterOpen(false)};
    restore();
    window.addEventListener("popstate",restore);
    return()=>window.removeEventListener("popstate",restore);
  },[initialCategory,categoryKey]);

  useEffect(()=>{if(typeof document==="undefined")return;requestAnimationFrame(()=>document.querySelector<HTMLElement>(".view-catalog .catalog-category-slider-v141 button.active")?.scrollIntoView({block:"nearest",inline:"center",behavior:"smooth"}))},[category]);

  useEffect(()=>{
    if(!filterOpen||typeof document==="undefined")return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")setFilterOpen(false)};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  },[filterOpen]);

  const baseProducts=products.filter(product=>category==="Все товары"||sameFacetV123(product.category,category));
  const subcategoryOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.subcategory));
  const collectionOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.collection));
  const capsuleOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.capsule));
  const skus=baseProducts.flatMap(product=>availableCatalogSkusV123(product));
  const materialOptions=uniqueFacetValuesV123(skus.map(sku=>sku.material));
  const sizeOptions=uniqueFacetValuesV123(skus.map(sku=>sku.size));
  const colorOptions=uniqueFacetValuesV123(skus.flatMap(sku=>catalogSkuColorGroupsV131(sku)));
  const colorHexes=new Map<string,string>();
  colorOptions.forEach(color=>colorHexes.set(facetNormV123(color),catalogColorGroupHexV131(color)));
  const allPrices=skus.map(sku=>Number(sku.price)||0).filter(price=>priceKnown(price));
  if(!allPrices.length)baseProducts.forEach(product=>{if(priceKnown(product.price))allPrices.push(product.price)});
  const minCatalogPrice=allPrices.length?Math.floor(Math.min(...allPrices)):0;
  const maxCatalogPrice=allPrices.length?Math.ceil(Math.max(...allPrices)):0;
  const facetCount=(group:CatalogFilterGroupV123,value:string,kind?:"collection"|"capsule")=>baseProducts.filter(product=>matchesCatalogProductV123(product,draft,group,{group,value,kind})).length;
  const draftCount=baseProducts.filter(product=>matchesCatalogProductV123(product,draft)).length;

  const filteredProducts=baseProducts.filter(product=>matchesCatalogProductV123(product,applied)).map(product=>catalogFilterDisplayProductV123(product,applied));
  const list=[...filteredProducts].sort((left,right)=>{
    if(sort==="price_asc")return catalogSortPriceV123(left,applied)-catalogSortPriceV123(right,applied);
    if(sort==="price_desc")return catalogSortPriceV123(right,applied)-catalogSortPriceV123(left,applied);
    return (popularityIndex.get(left.id)??Number.MAX_SAFE_INTEGER)-(popularityIndex.get(right.id)??Number.MAX_SAFE_INTEGER);
  });

  const resultKey=[category,sort,applied.subcategories.join("~"),applied.collections.join("~"),applied.capsules.join("~"),applied.materials.join("~"),applied.sizes.join("~"),applied.colors.join("~"),applied.priceFrom,applied.priceTo].join("|");
  useEffect(()=>{setVisibleCount(18)},[resultKey]);
  useEffect(()=>{
    const node=loadMoreRef.current;
    if(!node||visibleCount>=list.length||typeof IntersectionObserver==="undefined")return;
    const observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting))setVisibleCount(current=>Math.min(current+18,list.length))},{rootMargin:"900px 0px"});
    observer.observe(node);
    return()=>observer.disconnect();
  },[visibleCount,list.length,resultKey]);
  const visibleList=list.slice(0,visibleCount);

  const openFilters=()=>{setDraft(cloneCatalogFiltersV123(applied));setFilterOpen(true)};
  const changeDraft=(key:CatalogMultiFilterKeyV123,value:string)=>setDraft(current=>toggleCatalogFilterValueV123(current,key,value));
  const applyDraft=()=>{const next=cloneCatalogFiltersV123(draft);setApplied(next);setFilterOpen(false);writeCatalogUrl(next,sort,category,"push")};
  const resetDraft=()=>setDraft(emptyCatalogFiltersV123());
  const resetAll=()=>{const next=emptyCatalogFiltersV123();setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const changeCategory=(name:string)=>{const next=emptyCatalogFiltersV123();setCategory(name);setApplied(next);setDraft(cloneCatalogFiltersV123(next));setFilterOpen(false);writeCatalogUrl(next,sort,name,"push")};
  const changeSort=(next:CatalogSortV123)=>{setSort(next);writeCatalogUrl(applied,next,category,"push")};
  const removeAppliedValue=(key:CatalogMultiFilterKeyV123,value:string)=>{const next={...applied,[key]:withoutFacetValueV123(applied[key],value)} as CatalogFiltersV123;setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const removePrice=()=>{const next={...applied,priceFrom:"",priceTo:""};setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const activeCount=applied.subcategories.length+applied.collections.length+applied.capsules.length+applied.materials.length+applied.sizes.length+applied.colors.length+(applied.priceFrom||applied.priceTo?1:0);
  const priceChip=applied.priceFrom&&applied.priceTo?`${catalogNumberV123(Number(applied.priceFrom))}–${catalogNumberV123(Number(applied.priceTo))} ₽`:applied.priceFrom?`от ${catalogNumberV123(Number(applied.priceFrom))} ₽`:applied.priceTo?`до ${catalogNumberV123(Number(applied.priceTo))} ₽`:"";
  const renderChip=(key:CatalogMultiFilterKeyV123,value:string)=><button key={`${key}-${value}`} className="catalog-filter-chip-v123" onClick={()=>removeAppliedValue(key,value)}>{value}<span>×</span></button>;

  return <div className="catalog page catalog-v123">
    <nav className="crumbs catalog-crumbs-v141" aria-label="Хлебные крошки"><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/`}}>Главная</button><span>/</span><button type="button" onClick={()=>changeCategory("Все товары")}>Каталог</button>{category!=="Все товары"&&<><span>/</span><b>{category}</b></>}</nav>
    <div className="title-line"><h1>{category}</h1><span>{productCountLabel(list.length)}</span></div>
    <div className="tabs catalog-category-slider-v141" role="tablist" aria-label="Категории каталога">{["Все товары",...categoryNames].map(name=><button key={name} role="tab" aria-selected={category===name} className={category===name?"active":""} onClick={()=>changeCategory(name)}>{name}</button>)}</div>
    <div className="catalog-tools catalog-tools-v123">
      <button className="catalog-filter-trigger-v123" type="button" onClick={openFilters}><span>Фильтры</span>{activeCount>0&&<b>{activeCount}</b>}</button>
      <label className="catalog-sort-v123"><span>Сортировка</span><span className="catalog-sort-select-v125"><select value={sort} onChange={event=>changeSort(event.target.value as CatalogSortV123)} aria-label="Сортировка товаров"><option value="popular">По популярности</option><option value="price_asc">Сначала дешевле</option><option value="price_desc">Сначала дороже</option></select><Icon name="chevron"/></span></label>
    </div>
    {activeCount>0&&<div className="catalog-active-filters-v123" aria-label="Выбранные фильтры">{applied.subcategories.map(value=>renderChip("subcategories",value))}{applied.collections.map(value=>renderChip("collections",value))}{applied.capsules.map(value=>renderChip("capsules",value))}{applied.materials.map(value=>renderChip("materials",value))}{applied.sizes.map(value=>renderChip("sizes",value))}{applied.colors.map(value=>renderChip("colors",value))}{priceChip&&<button className="catalog-filter-chip-v123" onClick={removePrice}>{priceChip}<span>×</span></button>}<button className="catalog-filter-reset-all-v123" onClick={resetAll}>Сбросить все</button></div>}
    {list.length?<><div className="product-grid">{visibleList.map(product=><ProductCard key={`${category}-${product.id}-${product.selectedSkuId??product.selectedColor??"default"}`} product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>{visibleCount<list.length&&<div ref={loadMoreRef} aria-hidden="true" style={{height:1}}/>}</>:<div className="catalog-empty catalog-empty-v123"><p>По выбранным параметрам товаров не найдено</p><button type="button" onClick={resetAll}>Сбросить фильтры</button></div>}
    {filterOpen&&<div className="catalog-filter-layer-v123" role="presentation" onMouseDown={event=>{if(event.target===event.currentTarget)setFilterOpen(false)}}>
      <aside className="catalog-filter-drawer-v123" role="dialog" aria-modal="true" aria-label="Фильтры каталога">
        <header className="catalog-filter-header-v123"><div><h2>Фильтры</h2><span>{productCountLabel(draftCount)}</span></div><button type="button" onClick={()=>setFilterOpen(false)} aria-label="Закрыть фильтры"><Icon name="close"/></button></header>
        <div className="catalog-filter-body-v123">
          {subcategoryOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Тип товара</span>{draft.subcategories.length>0&&<b>{draft.subcategories.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">{subcategoryOptions.map(value=>{const count=facetCount("subcategory",value),checked=hasFacetValueV123(draft.subcategories,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("subcategories",value)}/>})}</div></div></details>}
          {(collectionOptions.length>0||capsuleOptions.length>0)&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Коллекция / капсула</span>{(draft.collections.length+draft.capsules.length)>0&&<b>{draft.collections.length+draft.capsules.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">{collectionOptions.map(value=>{const count=facetCount("collection",value,"collection"),checked=hasFacetValueV123(draft.collections,value);return <CatalogFilterOptionV123 key={`collection-${value}`} label={value} kind="Коллекция" count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("collections",value)}/>})}{capsuleOptions.map(value=>{const count=facetCount("collection",value,"capsule"),checked=hasFacetValueV123(draft.capsules,value);return <CatalogFilterOptionV123 key={`capsule-${value}`} label={value} kind="Капсула" count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("capsules",value)}/>})}</div></div></details>}
          {materialOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Материал</span>{draft.materials.length>0&&<b>{draft.materials.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">{materialOptions.map(value=>{const count=facetCount("material",value),checked=hasFacetValueV123(draft.materials,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("materials",value)}/>})}</div></div></details>}
          {sizeOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Размер</span>{draft.sizes.length>0&&<b>{draft.sizes.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123">{sizeOptions.map(value=>{const count=facetCount("size",value),checked=hasFacetValueV123(draft.sizes,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("sizes",value)}/>})}</div></div></details>}
          {colorOptions.length>0&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Цвет</span>{draft.colors.length>0&&<b>{draft.colors.length}</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-options-v123 catalog-filter-colors-v123">{colorOptions.map(value=>{const count=facetCount("color",value),checked=hasFacetValueV123(draft.colors,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} swatch={colorHexes.get(facetNormV123(value))??"#e8e5df"} onChange={()=>changeDraft("colors",value)}/>})}</div></div></details>}
          {(minCatalogPrice>0||maxCatalogPrice>0)&&<details className="catalog-filter-section-v123 catalog-filter-accordion-v125"><summary><span>Цена</span>{(draft.priceFrom||draft.priceTo)&&<b>1</b>}<Icon name="chevron"/></summary><div className="catalog-filter-accordion-content-v125"><div className="catalog-filter-price-v123"><label><span>От</span><div><input type="number" inputMode="numeric" min={0} placeholder={minCatalogPrice?catalogNumberV123(minCatalogPrice):"0"} value={draft.priceFrom} onChange={event=>setDraft(current=>({...current,priceFrom:event.target.value}))}/><b>₽</b></div></label><span className="catalog-filter-price-dash-v123">—</span><label><span>До</span><div><input type="number" inputMode="numeric" min={0} placeholder={maxCatalogPrice?catalogNumberV123(maxCatalogPrice):""} value={draft.priceTo} onChange={event=>setDraft(current=>({...current,priceTo:event.target.value}))}/><b>₽</b></div></label></div></div></details>}
        </div>
        <footer className="catalog-filter-footer-v123"><button className="catalog-filter-reset-v123" type="button" onClick={resetDraft}>Сбросить</button><button className="catalog-filter-apply-v123" type="button" onClick={applyDraft}>Показать {productCountLabel(draftCount)}</button></footer>
      </aside>
    </div>}
  </div>;
}

function ProductCard({ product, onClick, onQuick, favorite, liked, selectionMode=false, selected=false, pending=false, onSelect, onVariantChange }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean; selectionMode?:boolean; selected?:boolean; pending?:boolean; onSelect?:()=>void; onVariantChange?:(product:Product)=>void }) { // PRODUCT_CARD_VARIANT_CALLBACK_V34
  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];
  // CATALOG_FILTER_VARIANT_V123: start the card on the SKU/variant selected by catalog filters.
  const initialColorIndex=Math.max(0,variants.findIndex(variant=>variant.name===product.selectedColor));
  const [colorIndex, setColorIndex] = useState(initialColorIndex);
  useEffect(()=>{const next=variants.findIndex(variant=>variant.name===product.selectedColor);if(next>=0)setColorIndex(next)},[product.selectedColor,variants.map(variant=>variant.name).join("|")]);
  const chosen = variants[colorIndex]??variants[0];
  const chosenSku=findProductSku(product,chosen.name);
  const allPrimarySkus=(product.skus??[]).filter(item=>skuPrimaryMatches(product,item,chosen.name));
  const catalogFilterSkuIds=((product as Product&{catalogFilterSkuIds?:string[]}).catalogFilterSkuIds??[]);
  const eligibleSkuSet=catalogFilterSkuIds.length?new Set(catalogFilterSkuIds):undefined;
  const primarySkus=eligibleSkuSet?allPrimarySkus.filter(item=>eligibleSkuSet.has(item.id)):allPrimarySkus;
  const eligibleSkus=eligibleSkuSet?(product.skus??[]).filter(item=>eligibleSkuSet.has(item.id)):(product.skus??[]);
  const cardSkus=primarySkus.length?primarySkus:eligibleSkus.length?eligibleSkus:allPrimarySkus;
  const pricedCardSkus=cardSkus.filter(item=>priceKnown(item.price));
  const cardMinSku=pricedCardSkus.reduce<CatalogSku|undefined>((best,item)=>!best||item.price<best.price?item:best,undefined);
  const cardPrice=cardMinSku?.price??product.price;
  const cardOldPrice=Number(asVariantSku(cardMinSku)?.oldPrice)||0;
  const showFromPrice=new Set(cardSkus.map(item=>item.size)).size>1&&new Set(pricedCardSkus.map(item=>item.price)).size>1;
  const discount=cardOldPrice>cardPrice?Math.round((1-cardPrice/cardOldPrice)*100):0;
  const knownPrice=priceKnown(cardPrice);
  const chosenProduct = { ...product, price:cardPrice, oldPrice:cardOldPrice>cardPrice?cardOldPrice:undefined, image: chosenSku?.image??chosen.image, gallery:chosenSku?.gallery??chosen.gallery??product.gallery, position: chosen.position ?? product.position, selectedColor: chosen.name, selectedSize:chosenSku?.size, selectedSkuId:chosenSku?.id };
  const chooseVariant=(index:number)=>{
    setColorIndex(index);
    const variant=variants[index];
    const sku=findProductSku(product,variant.name);
    onVariantChange?.({...product,image:sku?.image??variant.image,gallery:sku?.gallery??variant.gallery??product.gallery,position:variant.position??product.position,selectedColor:variant.name,selectedSize:sku?.size,selectedSkuId:sku?.id});
  };
  return <article className="product-card"><button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button><button className="product-image" onClick={()=>onClick(chosenProduct)}><DeferredProductCardMedia key={`${product.id}-${chosen.name}`} product={chosenProduct} alt={`${product.name}, ${chosen.name}`} position={chosen.position||product.position}/>{product.badge&&<span>{product.badge}</span>}</button><div className="product-copy"><button className="product-link" onClick={()=>onClick(chosenProduct)}><strong>{product.name}</strong><small>{product.switchBy==="none"?product.note:<>{chosen.name.toLowerCase()}, {product.note}</>}</small></button>{isAromaProduct(product)&&variants.length>1&&<div className="plp-aroma-options" role="group" aria-label={`Аромат товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} onClick={()=>chooseVariant(i)} aria-label={`Выбрать аромат ${variant.name}`}>{variant.name}</button>)}</div>}{!isAromaProduct(product)&&variants.length>1&&<div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>chooseVariant(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div>}<span className={`price ${discount?"sale-price":""}`}>{knownPrice?<>{showFromPrice?"от ":""}{fmt(cardPrice)} {cardOldPrice>cardPrice&&<><del>{showFromPrice?"от ":""}{fmt(cardOldPrice)}</del><mark>−{discount}%</mark></>}</>:"Цена уточняется"}</span></div>{selectionMode?<button className={`quick selection-check ${pending?"pending":selected?"selected":""}`} type="button" onClick={(event)=>{event.stopPropagation();onSelect?.()}} aria-pressed={selected} aria-label={pending?`Выберите размер для ${product.name}`:selected?`Убрать ${product.name}`:`Выбрать ${product.name}`}>{pending?"?":selected?"✓":""}</button>:<button className="quick" disabled={!knownPrice} onClick={()=>knownPrice&&onQuick(chosenProduct)} aria-label={knownPrice?`Добавить в корзину ${product.name}`:`Цена товара ${product.name} уточняется`}><Icon name="cart-add"/></button>}</article>;
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
// COLLECTIONS_ZARA_KULTURA_V66
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
      <div><small>КУЛЬТУРА ДОМА · EDITORIAL</small><h1>Капсулы</h1></div>
      <p>Истории для дома, собранные вокруг цвета, орнамента и ритуала. Откройте коллекцию как журнал — и выбирайте предметы только тогда, когда они действительно нужны.</p>
    </header>
    <section className="collections-v52-index" aria-label="Капсулы Культура Дома">
      {editorials.map(editorial=><article className="collections-v52-card" key={editorial.id}>
        <button className="collections-v52-card-media" type="button" onClick={()=>open(editorial)}><img src={assetUrl(editorial.images[0])} alt={editorial.name}/></button>
        <div className="collections-v52-card-copy"><small>КАПСУЛА</small><button type="button" onClick={()=>open(editorial)}><h2>{editorial.name}</h2></button><p>{editorial.lead}</p><div><span>{productCountLabel(editorial.productIds.length)}</span><strong>{collectionPrice(editorial)?`от ${fmt(collectionPrice(editorial))}`:""}</strong></div></div>
      </article>)}
    </section>

    {active&&<div className="v52-story-backdrop" role="presentation"><button className="v52-story-dismiss" type="button" onClick={close} aria-label="Закрыть коллекцию"/>
      <section className="v52-story-modal" role="dialog" aria-modal="true" aria-label={`Коллекция ${active.name}`}>
        <header className="v52-story-topbar"><button type="button" onClick={close}>← Коллекции</button><strong>КУЛЬТУРА ДОМА</strong><button type="button" onClick={close} aria-label="Закрыть">×</button></header>
        <div className="v52-story-columns">
          <aside className="v52-story-editorial" aria-label="История коллекции">
            <div className="v52-story-title"><small>КАПСУЛА</small><h1>{active.name}</h1><p>{active.lead}</p><span>{productCountLabel(items.length)}</span></div>
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
  const [selectedSecondaryColor,setSelectedSecondaryColor]=useState("");
  const [quantity,setQuantity]=useState(1);
  const [sizePrompt,setSizePrompt]=useState(false);
  const variants=product.colorVariants??[{name:"Молочный",hex:"#eee",image:product.image}];
  useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);const nextIndex=initial>=0?initial:0;setColorIndex(nextIndex);setActiveImage(0);setSelectedSize("");setSelectedSecondaryColor("");setQuantity(1);setSizePrompt(false)},[product.id,product.selectedColor]);
  const color=variants[colorIndex];
  const secondaryColors=getProductSecondaryColors(product,color.name);
  const secondaryColor=secondaryColors.some(item=>item.name===selectedSecondaryColor)?selectedSecondaryColor:(secondaryColors[0]?.name??"");
  const sizes=getProductSizeOptions(product,color.name,secondaryColor||undefined);
  const visibleSizes=sizes.filter(([name])=>!isUniversalSizeLabel(name));
  const unavailableSizes=getUnavailableProductSizes(product,color.name,sizes,secondaryColor||undefined);
  const autoSize=sizes.length===1&&isProductSizeAvailable(product,color.name,sizes[0][0],secondaryColor||undefined)?sizes[0][0]:"";
  const effectiveSelectedSize=selectedSize||autoSize;
  const sku=effectiveSelectedSize?findProductSku(product,color.name,effectiveSelectedSize,secondaryColor||undefined):undefined;
  const mediaSku=findProductSku(product,color.name,undefined,secondaryColor||undefined);
  const gallery=mediaSku?[mediaSku.image,...mediaSku.gallery]:product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const unitPrice=sku?.price??(sizes.length?Math.min(...sizes.map(([,value])=>value)):product.price);
  const sizePricesDiffer=new Set(sizes.map(([,value])=>value)).size>1;
  const showFromPrice=sizes.length>1&&sizePricesDiffer&&!selectedSize;
  const selectedProduct={...product,price:unitPrice,image:mediaSku?.image??color.image,gallery:mediaSku?.gallery??product.gallery,selectedColor:color.name,selectedSize:effectiveSelectedSize,selectedSkuId:(sku??mediaSku)?.id,quantity};
  const specs=sku??mediaSku??product.skus?.[0];
  const specsExtra=asVariantSku(specs);
  const currentOldPrice=Number(specsExtra?.oldPrice)||0;
  const solutionTags:string[]=[];
  const needsSize=Boolean(sizes.length>1&&!effectiveSelectedSize);
  const selectedUnavailable=Boolean(effectiveSelectedSize&&!isProductSizeAvailable(product,color.name,effectiveSelectedSize,secondaryColor||undefined));
  const knownUnitPrice=priceKnown(unitPrice);
  const handlePurchase=()=>{if(needsSize||selectedUnavailable||!knownUnitPrice)return;add(selectedProduct)};
  return <div className={`product-page page ${product.hasRichContent?"has-rich":"standard-pdp"}`}><nav className="crumbs catalog-crumbs-v141" aria-label="Хлебные крошки"><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/`}}>Главная</button><span>/</span><button type="button" onClick={()=>{window.location.href=`${runtimeStorefrontBase()}/catalog/?category=${encodeURIComponent(product.category??"Все товары")}`}}>{product.category??"Каталог"}</button><span>/</span><b>{product.name}</b></nav><div className={`pdp-grid ${product.hasRichContent?"without-thumbs":""}`}>{!product.hasRichContent&&<div className="thumbs">{gallery.map((src,n)=><button key={src} className={n===activeImage?"active":""} onClick={()=>{setActiveImage(n);if(typeof window!=="undefined"&&window.matchMedia("(min-width: 901px)").matches){document.querySelector(`[data-pdp-image-index="${n}"]`)?.scrollIntoView({behavior:"smooth",block:"start"})}}} aria-label={`Фото товара ${n+1}`}><RemoteImage src={src} alt=""/></button>)}</div>}<div className="pdp-main"><ScrollableProductMedia key={`${product.id}-${color.name}`} product={selectedProduct} alt={`${product.name}, ${color.name}`} className="pdp-product-media" activeIndex={activeImage} onActiveIndexChange={setActiveImage}/></div><div className="pdp-info">{product.badge&&<small className="badge">{product.badge}</small>}<div className="pdp-title"><h1>{product.name}</h1><div><button onClick={()=>favorite(product.id)} aria-label={liked?`Удалить ${product.name} из избранного`:`Добавить ${product.name} в избранное`}><Icon name="heart" filled={liked}/></button><button onClick={()=>navigator.clipboard?.writeText(location.href)} aria-label="Поделиться"><Icon name="share"/></button></div></div><div className={`pdp-price ${currentOldPrice>unitPrice?"sale":""}`}><strong>{knownUnitPrice?(showFromPrice?`от ${fmt(unitPrice)}`:fmt(unitPrice)):"Цена уточняется"}</strong>{knownUnitPrice&&currentOldPrice>unitPrice&&<><del>{fmt(currentOldPrice)}</del><mark>−{Math.round((1-unitPrice/currentOldPrice)*100)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: {sku?.article??product.article??`KD-PD-${1020+product.id}`}</small>{solutionTags.length>0&&<div className="pdp-aroma-options" aria-label="Готовые решения">{solutionTags.map(tag=><a key={tag} href={`${process.env.NEXT_PUBLIC_BASE_PATH??""}/ready-solutions`}>{tag}</a>)}</div>}{product.switchBy!=="none"&&<label className="pdp-color-label">{isAromaProduct(product)?"Аромат":"Цвет"}: {color.name}</label>}{isAromaProduct(product)&&variants.length>1&&<div className="pdp-aroma-options">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setSelectedSecondaryColor("");setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}}>{variant.name}</button>)}</div>}{isAromaProduct(product)&&secondaryColors.length>0&&<><label className="pdp-color-label">Цвет: {secondaryColor}</label>{secondaryColors.length>1&&<div className="swatches product-swatches">{secondaryColors.map(item=><button key={item.name} className={item.name===secondaryColor?"active":""} onClick={()=>{setSelectedSecondaryColor(item.name);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:item.hex}} aria-label={`Цвет ${item.name}`}/>)}</div>}</>}{product.switchBy==="color"&&variants.length>1&&<div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0);setSelectedSize("");setQuantity(1);setSizePrompt(false)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div>}<p className="pdp-description">Предмет создан в традиции русского гостеприимства: благородная палитра, точная отделка и материалы, которые красиво живут в доме годами.</p>{visibleSizes.length>0&&<><label className="pdp-size-head"><span>РАЗМЕР</span>{visibleSizes.length>1&&<button onClick={()=>alert(visibleSizes.map(([name])=>name).join(" · "))}>Руководство по размерам</button>}</label><ProductSizeRows sizes={visibleSizes} selectedSize={effectiveSelectedSize} setSelectedSize={(name)=>{setSelectedSize(name);setQuantity(1);setSizePrompt(false)}} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}{sizes.length===1&&visibleSizes.length===0&&<div className="single-size-quantity"><span>ЕДИНЫЙ РАЗМЕР</span><QuantityControl quantity={quantity} setQuantity={setQuantity}/></div>}<button className={`primary purchase-cta total-cta ${needsSize||selectedUnavailable||!knownUnitPrice?"needs-size":"ready-to-add"}`} disabled={needsSize||selectedUnavailable||!knownUnitPrice} onClick={handlePurchase} aria-live="polite"><span className="purchase-label">{selectedUnavailable?"НЕТ В НАЛИЧИИ":!knownUnitPrice?"ЦЕНА УТОЧНЯЕТСЯ":needsSize?"ВЫБРАТЬ РАЗМЕР":"ДОБАВИТЬ В КОРЗИНУ"}</span>{!needsSize&&!selectedUnavailable&&knownUnitPrice&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>setStoresOpen(true)} aria-label="Показать наличие в бутиках"><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button><div className="pdp-accordions">{[
  {title:"ХАРАКТЕРИСТИКИ",content:specs?<dl>{cleanNulls(specs.material)&&<div><dt>Материал</dt><dd>{renderMultiline(specs.material)}</dd></div>}{cleanNulls(specs.composition)&&<div><dt>Состав</dt><dd>{renderMultiline(specs.composition)}</dd></div>}{cleanNulls(specs.height)&&<div><dt>Высота</dt><dd>{renderMultiline(specs.height)}</dd></div>}{cleanNulls(specs.width)&&<div><dt>Ширина</dt><dd>{renderMultiline(specs.width)}</dd></div>}{cleanNulls(specsExtra?.volume)&&<div><dt>Объём</dt><dd>{renderMultiline(specsExtra?.volume)}</dd></div>}{cleanNulls(specs.diameter)&&<div><dt>Диаметр</dt><dd>{renderMultiline(specs.diameter)}</dd></div>}{cleanNulls(specs.packageInfo)&&<div><dt>Комплектация</dt><dd>{renderMultiline(specs.packageInfo)}</dd></div>}{cleanNulls(specs.details)&&<div><dt>Детали</dt><dd>{renderMultiline(specs.details)}</dd></div>}{cleanNulls(specs.collection)&&<div><dt>Коллекция</dt><dd>{renderMultiline(specs.collection)}</dd></div>}{cleanNulls(specs.capsule)&&<div><dt>Капсула</dt><dd>{renderMultiline(specs.capsule)}</dd></div>}</dl>:null},
  {title:"ДОСТАВКА И ВОЗВРАТ",content:<><p>Бесплатная доставка при заказе от 15 000 ₽. Доступны курьерская доставка и самовывоз из бутика.</p><small>Срок и доступные способы рассчитываются при оформлении заказа.</small></>}
].map(section=><section className={`pdp-accordion-item ${open===section.title?"open":""}`} key={section.title}><button className="pdp-accordion-trigger" onClick={()=>setOpen(open===section.title?"":section.title)} aria-expanded={open===section.title}><span>{section.title}</span><Icon name="chevron"/></button>{open===section.title&&<div className="pdp-accordion-panel">{section.content}</div>}</section>)}</div></div></div>{product.hasRichContent&&<RichContent product={product} selectProduct={selectProduct}/>}<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite} recentlyViewed={recentlyViewed}/>{storesOpen&&<BoutiqueMap close={()=>setStoresOpen(false)}/>}</div>;
}

function BoutiqueMap({close}:{close:()=>void}){
  const legacyBoutiques=[
    {city:"Москва",address:"Петровка",hours:"Ежедневно · 10:00–22:00",lat:55.7636,lon:37.6156},
    {city:"Санкт-Петербург",address:"Невский проспект",hours:"Ежедневно · 10:00–22:00",lat:59.9357,lon:30.3259},
    {city:"Казань",address:"Улица Баумана",hours:"Ежедневно · 10:00–21:00",lat:55.7903,lon:49.1124}
  ];
  const boutiques=SITE_DB_STORES.length?SITE_DB_STORES:legacyBoutiques;
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
      <button type="button" onClick={()=>go("collections")}><span>КАПСУЛЫ</span><Icon name="arrow"/></button>
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
const SITE_CITY_SUGGESTIONS=SITE_DB_CITIES.length?SITE_DB_CITIES:KD_CITY_SUGGESTIONS;
const SITE_ADDRESS_SUGGESTIONS=Object.keys(SITE_DB_ADDRESS_SUGGESTIONS).length?SITE_DB_ADDRESS_SUGGESTIONS:KD_ADDRESS_SUGGESTIONS;
const SITE_PVZ_POINTS=Object.keys(SITE_DB_PVZ_POINTS).length?SITE_DB_PVZ_POINTS:KD_PVZ_POINTS;

function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const query=value.trim().toLowerCase();
  const items=SITE_CITY_SUGGESTIONS.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);
  return <label className="v43-field v43-suggest-field"><span>{label}{required?" *":""}</span><input value={value} autoComplete="address-level2" aria-autocomplete="list" onFocus={()=>setOpen(true)} onBlur={()=>window.setTimeout(()=>setOpen(false),120)} onChange={event=>{onChange(event.target.value);setOpen(true)}} placeholder="Начните вводить город"/>{open&&items.length>0&&<div className="v43-suggestions" role="listbox">{items.map(city=><button type="button" key={city} onMouseDown={event=>event.preventDefault()} onClick={()=>{onChange(city);setOpen(false)}}>{city}</button>)}</div>}</label>;
}

function AddressSuggestField({city,value,onChange,label="Улица и дом",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const source=SITE_ADDRESS_SUGGESTIONS[city]??[];
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
  const visibleSizes=sizes.filter(([name])=>!isUniversalSizeLabel(name));
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
  return <div className="overlay plp-flow"><button className="overlay-bg" onClick={close} aria-label="Закрыть выбор размера"/><section className="plp-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}><div className="flow-handle"/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="plp-modal-media"><ScrollableProductMedia product={product} alt={product.name}/></div><div className="plp-modal-info"><small>{product.badge||"КУЛЬТУРА ДОМА"}</small><h2>{product.name}</h2><p className="modal-note">{product.note}</p><div className="modal-price"><b>{sizes.length>1&&!chosenSize?`от ${fmt(sizes[0]?.[1]??product.price)}`:fmt(unitPrice)}</b>{product.oldPrice&&<><del>{sizes.length>1&&!chosenSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</div>{product.switchBy!=="none"&&<p className="quick-color">{isAromaProduct(product)?"Аромат":"Цвет"}: {product.selectedColor ?? product.colorVariants?.[0]?.name}</p>}<p className="quick-description">Предмет создан в русской декоративной традиции: ясная форма, благородный цвет и точная отделка.</p><button className="quick-info-link" onClick={()=>setInfoOpen(true)}><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><Icon name="chevron"/></button>{visibleSizes.length>0&&<><div className="sheet-head"><span>РАЗМЕР</span>{visibleSizes.length>1&&<button onClick={()=>setInfoOpen(true)}>Руководство по размерам</button>}</div><ProductSizeRows sizes={visibleSizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} unavailableLast={!product.skus?.length} unavailableSizes={unavailableSizes} oldPrice={product.oldPrice} notify={(name)=>alert(`Спасибо. Сообщим, когда размер «${name}» появится в наличии.`)}/></>}{sizes.length===1&&visibleSizes.length===0&&<div className="single-size-quantity"><span>ЕДИНЫЙ РАЗМЕР</span><QuantityControl quantity={quantity} setQuantity={setQuantity}/></div>}<button className={`primary total-cta ${canAdd?"ready-to-add":"choose-size-disabled"}`} disabled={!canAdd} onClick={()=>canAdd&&add(chosenSize,quantity,unitPrice)}><span>{canAdd?"ДОБАВИТЬ В КОРЗИНУ":"ВЫБРАТЬ РАЗМЕР"}</span>{canAdd&&<b>{fmt(unitPrice*quantity)}</b>}</button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>
}

function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  const sku=findProductSku(product,product.selectedColor,product.selectedSize)??product.skus?.[0];
  const extra=asVariantSku(sku);
  const sizeValue=cleanNulls(sku?.size)==="Единый размер"?undefined:cleanNulls(sku?.size);
  const rows:[string,string|undefined][]=[
    ["Размер",sizeValue],
    ["Высота",cleanNulls(sku?.height)],
    ["Ширина",cleanNulls(sku?.width)],
    ["Объём",cleanNulls(extra?.volume)],
    ["Диаметр",cleanNulls(sku?.diameter)],
    ["Комплектация",cleanNulls(sku?.packageInfo)],
    ["Детали",cleanNulls(sku?.details)],
    ["Коллекция",cleanNulls(sku?.collection)],
    ["Капсула",cleanNulls(sku?.capsule)],
  ];
  const visibleRows=rows.filter((row):row is [string,string]=>Boolean(row[1]));
  const material=cleanNulls(sku?.material);
  const composition=cleanNulls(sku?.composition);
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div>{visibleRows.length>0&&<section><h2>ХАРАКТЕРИСТИКИ</h2><dl>{visibleRows.map(([label,value])=><div key={label}><dt>{label}</dt><dd>{renderMultiline(value)}</dd></div>)}</dl></section>}{(material||composition)&&<section><h2>МАТЕРИАЛ И СОСТАВ</h2>{material&&<h3>{renderMultiline(material)}</h3>}{composition&&<div>{renderMultiline(composition)}</div>}</section>}<section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
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

  return <div className="overlay cart-v43-overlay" data-analytics-step="cart_open"><aside className="cart-v43 cart-v69" role="dialog" aria-modal="true" aria-label="Корзина">
    <header className="cart-v43-head"><button type="button" onClick={go}>← <span>Продолжить покупки</span></button><b>КУЛЬТУРА ДОМА</b><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button></header>
    {cart.length===0?<main className="cart-v43-empty"><small>КОРЗИНА</small><h1>Здесь пока пусто</h1><p>Добавьте предметы из каталога или вернитесь к недавно просмотренным.</p>{recentItems.length>0&&<section><h2>Недавно просмотренные</h2><div>{recentItems.map(product=><button type="button" key={product.id} onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/><span>{product.name}</span><b>{fmt(product.price)}</b></button>)}</div></section>}<button type="button" className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></main>:<main className="cart-v43-layout">
      <section className="cart-v43-content"><header className="cart-v43-title"><small>КОРЗИНА</small><h1>Корзина <span>{itemCount} товаров</span></h1><p>Проверьте количество и упаковку. Размер и цвет остаются такими, как вы выбрали.</p></header>
        <div className="cart-v43-delivery"><div><b>{courierShipping===0?"Бесплатная доставка":"До бесплатной доставки — "+fmt(deliveryLeft)}</b><span>{courierShipping===0?"Для курьера и ПВЗ":"Курьер — 300 ₽ · ПВЗ — бесплатно"}</span></div><i><b style={{width:`${deliveryProgress}%`}}/></i></div>
        <div className="cart-v43-items">{cart.map((item,index)=><article className="cart-v43-item" key={`${item.id}-${index}`}><button className="cart-v43-media" type="button" onClick={()=>choose(item)}><ScrollableProductMedia product={item} alt={item.name} className="cart-item-media"/></button><div className="cart-v43-copy"><div className="cart-v43-item-head"><button type="button" onClick={()=>choose(item)}>{item.name}</button><b>{fmt(item.price*item.quantity)}</b></div><div className="cart-v43-meta"><span>Цвет: {item.selectedColor}</span><span>Размер: {item.selectedSize}</span></div>{isGiftPackagingAvailable(item)&&<label className="cart-v43-gift"><input type="checkbox" checked={Boolean(item.giftWrap)} onChange={event=>update(index,{giftWrap:event.target.checked})}/><span>Подарочная упаковка</span></label>}<div className="cart-v43-actions"><QuantityControl quantity={item.quantity} setQuantity={quantity=>update(index,{quantity})}/><button type="button" onClick={()=>remove(index)}>Удалить</button></div></div></article>)}</div>
        {suggestions.length>0&&<section className="cart-v43-crosssell"><header><small>ДОПОЛНИТЕ ИНТЕРЬЕР</small><h2>До полного образа</h2></header><div>{suggestions.map(product=><article key={product.id}><button className="cart-v43-cross-media" type="button" onClick={()=>choose(product)}><ScrollableProductMedia product={product} alt={product.name} className="recent-item-media"/></button><button className="cart-v43-cross-name" type="button" onClick={()=>choose(product)}>{product.name}</button><b>{fmt(product.price)}</b><button className="cart-v43-cross-add" type="button" onClick={()=>quickAdd(product)}>Добавить</button></article>)}</div></section>}
      </section>
      <aside className="cart-v43-summary"><div className="cart-v43-summary-inner"><small>ИТОГ ЗАКАЗА</small><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Курьер</dt><dd>{courierShipping===0?"Бесплатно":fmt(courierShipping)}</dd></div><div><dt>Пункт выдачи</dt><dd>Бесплатно</dd></div></dl><div className="cart-v43-total"><span>Итого при курьере</span><b>{fmt(courierTotal)}</b></div><p>На следующем шаге можно выбрать бесплатный ПВЗ. Итог обновится до подтверждения заказа.</p>{profile?<div className="cart-v43-bonus"><span>Ваш баланс</span><b>0 бонусов</b></div>:<div className="cart-v43-bonus"><span>Бонусы</span><b>Войдите, чтобы увидеть баланс</b></div>}<button type="button" className="primary cart-v43-checkout" data-analytics-step="checkout_start" onClick={checkout}>ПЕРЕЙТИ К ОФОРМЛЕНИЮ</button><div className="cart-v43-trust"><span>✓ Безопасная оплата</span><span>✓ Итог до подтверждения</span></div></div></aside>
    </main>}
  </aside></div>;
}

// MOBILE_CART_CHECKOUT_V67
// ONE_SCREEN_CHECKOUT_V68
// CART_CHECKOUT_MOCKUP_V69
function Checkout({cart,total,profile,close,editCart,submit}:{cart:CartItem[];total:number;profile:Profile|null;close:()=>void;editCart:()=>void;submit:()=>void}){
  type DeliveryMethod="courier"|"store"|"pvz";
  type PaymentMethod="online"|"upon";
  const [delivery,setDelivery]=useState<DeliveryMethod>("courier");
  const [payment,setPayment]=useState<PaymentMethod>("online");
  const paymentMethods=SITE_DB_PAYMENT_METHODS.length?SITE_DB_PAYMENT_METHODS:[{id:"online",name:"Онлайн — картой / СБП",timing:"prepaid",instruments:["bank_card","sbp"],discountPercent:3,currency:"RUB",active:true,sortOrder:1},{id:"upon",name:"При получении",timing:"on_receipt",instruments:["bank_card","cash"],discountPercent:0,currency:"RUB",active:true,sortOrder:2}] as const;
  const deliveryMethods=SITE_DB_DELIVERY_METHODS.length?SITE_DB_DELIVERY_METHODS:[{id:"courier",name:"Курьером",minDays:2,maxDays:3,baseFeeRub:300,freeFromRub:15000,currency:"RUB",destinationType:"address",active:true,sortOrder:1},{id:"store",name:"Самовывоз",minDays:2,maxDays:3,baseFeeRub:0,freeFromRub:0,currency:"RUB",destinationType:"store",active:true,sortOrder:2},{id:"pvz",name:"ПВЗ",minDays:2,maxDays:3,baseFeeRub:0,freeFromRub:0,currency:"RUB",destinationType:"pvz",active:true,sortOrder:3}] as const;
  const [recipientName,setRecipientName]=useState(profile?.name??"");
  const [form,setForm]=useState<Profile>(profile??{name:"",surname:"",email:"",phone:"",city:"Москва",address:""});
  const [phoneVerified,setPhoneVerified]=useState(Boolean(profile?.phone));
  const [codeSent,setCodeSent]=useState(false);
  const [phoneCode,setPhoneCode]=useState("");
  const [otpError,setOtpError]=useState("");
  const [registeredChoice,setRegisteredChoice]=useState<""|"account"|"guest">("");
  const [submitAttempted,setSubmitAttempted]=useState(false);
  const [notifications,setNotifications]=useState(true);
  const [agreed,setAgreed]=useState(false);
  const [slot,setSlot]=useState("18:00–22:00");
  const [entrance,setEntrance]=useState("");
  const [floor,setFloor]=useState("");
  const [flat,setFlat]=useState("");
  const [pickupPoint,setPickupPoint]=useState("");
  const [storePoint,setStorePoint]=useState("");
  const [pvzQuery,setPvzQuery]=useState("");

  const storePoints:Record<string,string[]>={
    "Москва":["Культура Дома · Петровка"],
    "Санкт-Петербург":["Культура Дома · Невский проспект"],
    "Казань":["Культура Дома · улица Баумана"],
  };
  const activeStorePoints=Object.keys(SITE_DB_STORE_POINTS).length?SITE_DB_STORE_POINTS:storePoints;
  const pvz=SITE_PVZ_POINTS[form.city]??[];
  const stores=activeStorePoints[form.city]??[];
  const filteredPvz=pvz.filter(point=>!pvzQuery.trim()||point.toLocaleLowerCase("ru-RU").includes(pvzQuery.trim().toLocaleLowerCase("ru-RU")));
  const phoneDigits=form.phone.replace(/\D/g,"");
  const profileDigits=(profile?.phone||"").replace(/\D/g,"");
  const demoRegisteredDigits="79261234567";
  const registeredNumber=phoneDigits.length>=10&&(phoneDigits===profileDigits||phoneDigits===demoRegisteredDigits);
  const registeredName=profile?.name?`${profile.name}${profile.surname?` ${profile.surname.slice(0,1)}.`:""}`:"Анна И.";
  const emailOk=!form.email.trim()||/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim());
  const phoneOk=phoneDigits.length>=10&&phoneVerified;
  const contactOk=recipientName.trim().length>1&&phoneOk&&emailOk;
  const deliveryOk=delivery==="courier"
    ? Boolean(form.city.trim()&&form.address.trim().length>3)
    : delivery==="store"?Boolean(form.city.trim()&&storePoint):Boolean(form.city.trim()&&pickupPoint);
  const paymentConfig=paymentMethods.find(item=>item.id===payment);
  const deliveryConfig=deliveryMethods.find(item=>item.id===delivery);
  const onlineDiscount=paymentConfig?.discountPercent?Math.round(total*(Number(paymentConfig.discountPercent)/100)):0;
  const shipping=deliveryConfig?(Number(deliveryConfig.freeFromRub)>0&&total>=Number(deliveryConfig.freeFromRub)?0:Number(deliveryConfig.baseFeeRub)||0):0;
  const payable=Math.max(0,total-onlineDiscount+shipping);
  const canSubmit=contactOk&&deliveryOk&&agreed;
  const selectedPoint=delivery==="store"?storePoint:pickupPoint;
  const recipientFull=[recipientName.trim(),form.surname.trim()].filter(Boolean).join(" ");
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);

  const setPhone=(value:string)=>{
    const digits=value.replace(/\D/g,"");
    setForm(current=>({...current,phone:value}));
    setPhoneVerified(Boolean(profileDigits&&digits===profileDigits));
    setCodeSent(false);setPhoneCode("");setOtpError("");setRegisteredChoice("");
  };
  const requestPhoneCode=()=>{
    if(phoneDigits.length<10){setOtpError("Введите полный номер телефона");return}
    setCodeSent(true);setPhoneCode("");setOtpError("");
  };
  const verifyPhone=()=>{
    if(phoneCode==="1234"){setPhoneVerified(true);setCodeSent(false);setOtpError("")}
    else setOtpError("Неверный код. В прототипе используйте 1234");
  };
  const continueWithAccount=()=>{setRegisteredChoice("account");setPhoneVerified(true);setCodeSent(false);setOtpError("")};
  const continueAsGuest=()=>{setRegisteredChoice("guest");if(!phoneVerified){setCodeSent(true);setPhoneCode("");setOtpError("")}};
  const chooseCity=(city:string)=>{setForm(current=>({...current,city,address:city===current.city?current.address:""}));setPickupPoint("");setStorePoint("");setPvzQuery("")};
  const chooseDelivery=(method:DeliveryMethod)=>{
    setDelivery(method);
    if(method==="pvz"&&!pickupPoint&&pvz[0])setPickupPoint(pvz[0]);
    if(method==="store"&&!storePoint&&stores[0])setStorePoint(stores[0]);
  };
  const submitOrder=()=>{setSubmitAttempted(true);if(canSubmit)submit()};

  return <div className="checkout checkout-v69" data-analytics-step="checkout_view">
    <header className="checkout-v69-head"><button type="button" onClick={close} aria-label="Вернуться в корзину">←</button><b>КУЛЬТУРА ДОМА</b><button type="button" onClick={editCart} aria-label="Открыть корзину"><Icon name="bag"/></button></header>

    <form className="checkout-v69-layout" onSubmit={event=>{event.preventDefault();submitOrder()}}>
      <main className="checkout-v69-main">
        <header className="checkout-v69-title"><h1>Оформление заказа</h1></header>

        <section className="checkout-v69-section checkout-v69-contacts" aria-labelledby="v69-contact-title">
          <h2 id="v69-contact-title">Контактные данные</h2>
          <div className="checkout-v69-fields checkout-v69-name-row">
            <label><span>Имя получателя *</span><input value={recipientName} onChange={event=>setRecipientName(event.target.value)} autoComplete="given-name" placeholder="Имя"/></label>
            <label><span>Фамилия</span><input value={form.surname} onChange={event=>setForm(current=>({...current,surname:event.target.value}))} autoComplete="family-name" placeholder="Необязательно"/></label>
          </div>
          <label className={`checkout-v69-field checkout-v69-phone ${phoneVerified?"is-verified":""}`}><span>Контактный телефон *</span><div><input value={form.phone} onChange={event=>setPhone(event.target.value)} inputMode="tel" autoComplete="tel" placeholder="+7 999 000-00-00"/>{phoneVerified?<b>✓</b>:phoneDigits.length>=10?<button type="button" onClick={requestPhoneCode}>Получить код</button>:null}</div></label>

          {registeredNumber&&!registeredChoice&&<aside className="checkout-v69-account-note"><div><span>ⓘ</span><p>Этот номер привязан к аккаунту <b>{registeredName}</b>. Если продолжить как гость, заказ не появится в личном кабинете, а бонусы не начислятся автоматически.</p></div><button type="button" className="primary" onClick={continueWithAccount}>ВОЙТИ В АККАУНТ <em>(рекомендуем)</em></button><button type="button" onClick={continueAsGuest}>ВСЁ РАВНО ПРОДОЛЖИТЬ КАК ГОСТЬ</button></aside>}
          {registeredNumber&&registeredChoice&&<button type="button" className="checkout-v69-account-change" onClick={()=>setRegisteredChoice("")}>{registeredChoice==="account"?"Оформление с аккаунтом":"Продолжаем как гость"} · изменить</button>}

          {codeSent&&!phoneVerified&&<div className="checkout-v69-otp"><label><span>Код из SMS</span><input inputMode="numeric" maxLength={4} value={phoneCode} onChange={event=>{setPhoneCode(event.target.value.replace(/\D/g,"").slice(0,4));setOtpError("")}} placeholder="0000"/></label><button type="button" onClick={verifyPhone}>ПОДТВЕРДИТЬ</button><small>Демо-код: 1234</small>{otpError&&<em role="alert">{otpError}</em>}</div>}

          <label className="checkout-v69-field"><span>Email для уведомлений</span><input type="email" value={form.email} onChange={event=>setForm(current=>({...current,email:event.target.value}))} autoComplete="email" placeholder="example@mail.ru"/></label>
          <label className="checkout-v69-check"><input type="checkbox" checked={notifications} onChange={event=>setNotifications(event.target.checked)}/><span>Хочу получать статус заказа и уведомления</span></label>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v69-delivery-title">
          <h2 id="v69-delivery-title">Способ получения</h2>
          <div className="checkout-v69-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            {deliveryMethods.map(method=><button key={method.id} type="button" className={delivery===method.id?"active":""} onClick={()=>chooseDelivery(method.id as DeliveryMethod)}><span>{method.id==="courier"?"▱":method.id==="store"?"⌂":"▦"}</span><b>{method.name}</b><small>{method.minDays}–{method.maxDays} дня · {(method.id===delivery&&shipping===0)||Number(method.baseFeeRub)===0?"0 ₽":fmt(Number(method.baseFeeRub))}</small></button>)}
          </div>

          <div className="checkout-v69-delivery-body">
            <CitySuggestField value={form.city} required onChange={chooseCity}/>

            {delivery==="courier"&&<>
              <AddressSuggestField city={form.city} value={form.address} required onChange={address=>setForm(current=>({...current,address}))}/>
              <div className="checkout-v69-address-parts"><label><span>Подъезд</span><input value={entrance} onChange={event=>setEntrance(event.target.value)} placeholder="2"/></label><label><span>Этаж</span><input value={floor} onChange={event=>setFloor(event.target.value)} placeholder="3"/></label><label><span>Квартира</span><input value={flat} onChange={event=>setFlat(event.target.value)} placeholder="8"/></label></div>
              <div className="checkout-v69-map-block"><div className="checkout-v69-map-caption"><b>Адрес на карте</b><span>{form.address?`${form.city}, ${form.address}`:form.city}</span></div><CheckoutMap points={[form.address?`${form.city}, ${form.address}`:form.city]} selected={form.address?`${form.city}, ${form.address}`:form.city} choose={()=>{}} mode="courier"/></div>
              <div className="checkout-v69-slots"><span>Время доставки</span><div>{["18:00–22:00","14:00–18:00","09:00–13:00"].map(value=><button type="button" key={value} className={slot===value?"active":""} onClick={()=>setSlot(value)}><b>{value}</b>{value==="18:00–22:00"&&<small>Рекомендуем</small>}</button>)}</div></div>
            </>}

            {delivery==="store"&&<div className="checkout-v69-pickup"><h3>Выберите бутик</h3>{stores.length?stores.map(point=><button type="button" key={point} className={storePoint===point?"active":""} onClick={()=>setStorePoint(point)}><i/><span><b>{point}</b><small>{form.city} · ежедневно</small></span></button>):<p>В этом городе пока нет доступного самовывоза.</p>}{stores.length>0&&<div className="checkout-v69-map-block"><CheckoutMap points={stores} selected={storePoint} choose={setStorePoint} mode="pickup"/></div>}</div>}

            {delivery==="pvz"&&<div className="checkout-v69-pvz"><label className="checkout-v69-pvz-search"><Icon name="search"/><input value={pvzQuery} onChange={event=>setPvzQuery(event.target.value)} placeholder="Введите адрес или станцию метро"/><Icon name="pin"/></label><div className="checkout-v69-map-block"><CheckoutMap points={filteredPvz.slice(0,5)} selected={pickupPoint} choose={setPickupPoint} mode="pickup"/></div>{selectedPoint&&<div className="checkout-v69-selected-point"><i/><span><b>{selectedPoint}</b><small>Готовность к выдаче: завтра, 09:00–20:00</small></span></div>}</div>}
          </div>
        </section>

        <section className="checkout-v69-section" aria-labelledby="v69-payment-title">
          <h2 id="v69-payment-title">Способ оплаты</h2>
          <div className="checkout-v69-payments">{paymentMethods.map(method=><button key={method.id} type="button" className={payment===method.id?"active":""} onClick={()=>setPayment(method.id as PaymentMethod)}><i/><span><b>{method.name}{Number(method.discountPercent)>0&&<mark>−{method.discountPercent}%</mark>}</b><small>{Number(method.discountPercent)>0?`−${method.discountPercent}% при оплате сейчас`:(method.instruments as readonly string[]).includes("cash")?"Картой или наличными":"Оплата при оформлении"}</small></span></button>)}</div>
        </section>

        <section className="checkout-v69-section checkout-v69-order" aria-labelledby="v69-order-title">
          <div className="checkout-v69-order-head"><h2 id="v69-order-title">Состав заказа</h2><button type="button" onClick={editCart}>Изменить</button></div>
          <dl><div><dt>{itemCount} товаров</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div className="discount"><dt>Скидка при онлайн-оплате</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl>
          <div className="checkout-v69-total"><span>Итого</span><b>{fmt(payable)}</b></div>
          <label className="checkout-v69-check checkout-v69-agree"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен(на) с условиями обработки персональных данных и правилами продажи</span></label>
          {submitAttempted&&!canSubmit&&<div className="checkout-v69-errors" role="alert">{!recipientName.trim()?"Укажите имя получателя. ":""}{phoneDigits.length<10?"Введите телефон. ":!phoneVerified?"Подтвердите номер телефона. ":""}{!emailOk?"Проверьте email. ":""}{!deliveryOk?"Заполните данные доставки. ":""}{!agreed?"Подтвердите согласие с условиями.":""}</div>}
          <button type="submit" className="primary checkout-v69-submit" disabled={submitAttempted&&!canSubmit}>ОФОРМИТЬ ЗАКАЗ — {fmt(payable)}</button>
          <small className="checkout-v69-security">♙ Безопасное оформление и защита данных</small>
        </section>
      </main>

      <aside className="checkout-v69-summary"><div><header><span>Ваш заказ</span><button type="button" onClick={editCart}>Изменить</button></header>{cart.slice(0,3).map((item,index)=><article key={`${item.id}-${index}`}><ScrollableProductMedia product={item} alt={item.name} className="checkout-v43-summary-media"/><span><b>{item.name}</b><small>{item.selectedColor} · {item.selectedSize}</small><em>{item.quantity} × {fmt(item.price)}</em></span></article>)}<dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Доставка</dt><dd>{shipping===0?"Бесплатно":fmt(shipping)}</dd></div>{onlineDiscount>0&&<div><dt>Скидка −3%</dt><dd>−{fmt(onlineDiscount)}</dd></div>}</dl><div className="checkout-v69-summary-total"><span>Итого</span><b>{fmt(payable)}</b></div></div></aside>
    </form>
  </div>;
}

function CheckoutMap({points,selected,choose,mode}:{points:string[];selected:string;choose:(point:string)=>void;mode:"courier"|"pickup"}){
  return <div className="checkout-map"><div className="map-canvas" aria-label="Карта выбора адреса">{points.map((point,index)=><button type="button" key={point} className={`map-pin pin-${index} ${selected===point?"active":""}`} onClick={()=>choose(point)} aria-label={`Выбрать ${point}`}><Icon name="pin"/><span>{index+1}</span></button>)}<i className="river"/><span className="map-label moscow">МОСКВА</span><span className="map-label center">САДОВОЕ КОЛЬЦО</span></div><div className="map-points"><p>{mode==="pickup"?"ВЫБЕРИТЕ БУТИК":"УТОЧНИТЕ ТОЧКУ НА КАРТЕ"}</p>{points.map((point,index)=><button type="button" key={point} className={selected===point?"active":""} onClick={()=>choose(point)}><b>{index+1}</b><span>{point}<small>{mode==="pickup"?"Сегодня до 22:00":"Курьерская доставка"}</small></span></button>)}</div></div>;
}

function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) { return <footer><div className="footer-brand"><div className="logo">КУЛЬТУРА ДОМА</div><p>Подпишитесь на письма о новых коллекциях</p><div><input placeholder="Ваш email"/><button onClick={()=>notice("Спасибо за подписку")}>→</button></div></div><div><p>ПОКУПАТЕЛЯМ</p><button onClick={()=>go("catalog")}>Каталог</button><button onClick={()=>alert(`Доставка по России от ${SITE_DB_POLICIES.delivery_min_days??"1"} дня`)}>Доставка и оплата</button><button onClick={()=>alert(`Возврат в течение ${SITE_DB_POLICIES.return_period_days??"14"} дней`)}>Возврат</button></div><div><p>О БРЕНДЕ</p><button onClick={()=>go("collections")}>Коллекции</button><button onClick={()=>alert("Русский бренд предметов для дома")}>Наша история</button><button onClick={()=>alert(Array.from(new Set(SITE_DB_STORES.map(store=>store.city))).join(" · ")||"Москва · Санкт-Петербург · Казань")}>Бутики</button></div><div><p>СВЯЗАТЬСЯ</p><a href={`tel:${SITE_DB_CONTACTS.support_phone??"+78005553535"}`}>8 800 555-35-35</a><a href={`mailto:${SITE_DB_CONTACTS.support_email??"hello@kultura-doma.ru"}`}>{SITE_DB_CONTACTS.support_email??"hello@kultura-doma.ru"}</a></div><small>© 2026 Культура дома &nbsp; · &nbsp; Политика конфиденциальности</small></footer> }
