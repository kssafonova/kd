"use client";

import Link from "next/link";
import {createContext,useCallback,useContext,useEffect,useMemo,useRef,useState} from "react";
import {CATALOG_PRODUCTS_GENERATED} from "./catalog-products.generated";

const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";
const href=(path:string)=>path.startsWith("/")?`${BASE}${path}`:path;
const asset=(path:string)=>path.startsWith("/assets/")?`${BASE}${path}`:path;
const rub=(value:number)=>`${new Intl.NumberFormat("ru-RU").format(Math.round(Number(value)||0))} ₽`;
const norm=(value:unknown)=>String(value??"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
const uniq=(values:(string|undefined)[])=>Array.from(new Map(values.filter(Boolean).map(value=>[norm(value),String(value)])).values());

type Sku={id:string;article?:string;color?:string;sourceColor?:string;colorHex?:string;size?:string;material?:string;composition?:string;collection?:string;capsule?:string;price?:number;oldPrice?:number;image?:string;gallery?:string[];available?:boolean;details?:string};
type Variant={name:string;hex?:string;image?:string;gallery?:string[]};
type Product={id:number;article?:string;name:string;note?:string;price:number;oldPrice?:number;image:string;gallery?:string[];category?:string;subcategory?:string;collection?:string;capsule?:string;switchBy?:string;skus?:Sku[];colorVariants?:Variant[]};
type CartLine={key:string;productId:number;name:string;price:number;image:string;quantity:number;color?:string;size?:string};
type Panel="menu"|"search"|"account"|"favorites"|"cart"|"checkout"|"quick"|null;

const PRODUCTS=CATALOG_PRODUCTS_GENERATED as unknown as Product[];
const CATEGORY_ORDER=["Все товары","Посуда и сервировка","Пледы и подушки","Постельное белье","Декор для дома","Столовый текстиль"];
const CATEGORIES=CATEGORY_ORDER.filter(name=>name==="Все товары"||PRODUCTS.some(product=>norm(product.category)===norm(name)));
const CAPSULE_IMAGE:Record<string,string>={
  "Лунная сказка":"/assets/images/caps_luna_postel.png",
  "Ледяные узоры":"/assets/images/caps_led.png",
  "Феникс":"/assets/images/feniks0.jpg",
  "Тайна":"/assets/images/tayna0.jpg",
  "Нити":"/assets/images/niti0.jpg",
};

function productImages(product:Product,variant?:Variant){
  return uniq([variant?.image,...(variant?.gallery??[]),product.image,...(product.gallery??[])]).filter(Boolean);
}
function productSkus(product:Product){return (product.skus??[]).filter(sku=>sku.available!==false)}
function variantSkus(product:Product,variant?:Variant){
  const skus=productSkus(product);if(!variant)return skus;
  return skus.filter(sku=>norm(sku.color)===norm(variant.name)||norm(sku.sourceColor)===norm(variant.name));
}
function productPrice(product:Product,variant?:Variant,size?:string){
  let skus=variantSkus(product,variant);if(size)skus=skus.filter(sku=>norm(sku.size)===norm(size));
  const prices=skus.map(sku=>Number(sku.price)||0).filter(Boolean);return prices.length?Math.min(...prices):Number(product.price)||0;
}
function selectedSku(product:Product,variant?:Variant,size?:string){
  let skus=variantSkus(product,variant);if(size)skus=skus.filter(sku=>norm(sku.size)===norm(size));
  return skus[0]??productSkus(product)[0];
}
function isAroma(product:Product){return product.switchBy==="aroma"||productSkus(product).some(sku=>Boolean((sku as any).aroma))}

function Icon({name}:{name:"menu"|"search"|"user"|"heart"|"bag"|"close"|"filter"|"chevron"|"minus"|"plus"}){
  const p={fill:"none",stroke:"currentColor",strokeWidth:1.6,strokeLinecap:"round" as const,strokeLinejoin:"round" as const};
  if(name==="menu")return <svg viewBox="0 0 24 24" {...p}><path d="M3 6h18M3 12h18M3 18h18"/></svg>;
  if(name==="search")return <svg viewBox="0 0 24 24" {...p}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.4 15.4 5.1 5.1"/></svg>;
  if(name==="user")return <svg viewBox="0 0 24 24" {...p}><circle cx="12" cy="7" r="4"/><path d="M4.3 21c.8-4.4 3.4-6.6 7.7-6.6s7 2.2 7.7 6.6"/></svg>;
  if(name==="heart")return <svg viewBox="0 0 24 24" {...p}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if(name==="bag")return <svg viewBox="0 0 24 24" {...p}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if(name==="close")return <svg viewBox="0 0 24 24" {...p}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if(name==="filter")return <svg viewBox="0 0 24 24" {...p}><path d="M4 6h16M7 12h10M10 18h4"/></svg>;
  if(name==="chevron")return <svg viewBox="0 0 24 24" {...p}><path d="m9 5 7 7-7 7"/></svg>;
  if(name==="minus")return <svg viewBox="0 0 24 24" {...p}><path d="M5 12h14"/></svg>;
  return <svg viewBox="0 0 24 24" {...p}><path d="M12 5v14M5 12h14"/></svg>;
}

type CommerceValue={panel:Panel;setPanel:(panel:Panel)=>void;quick:Product|null;openQuick:(product:Product)=>void;cart:CartLine[];favorites:number[];toggleFavorite:(id:number)=>void;addProduct:(product:Product,variant?:Variant,size?:string)=>void;changeQty:(key:string,delta:number)=>void;removeLine:(key:string)=>void};
const CommerceContext=createContext<CommerceValue|null>(null);
const useCommerce=()=>{const value=useContext(CommerceContext);if(!value)throw new Error("CommerceProvider missing");return value};

function CommerceProvider({children}:{children:React.ReactNode}){
  const [panel,setPanelState]=useState<Panel>(null);
  const [quick,setQuick]=useState<Product|null>(null);
  const [cart,setCart]=useState<CartLine[]>([]);
  const [favorites,setFavorites]=useState<number[]>([]);
  const hydrated=useRef(false);

  useEffect(()=>{
    try{
      const storedCart=JSON.parse(localStorage.getItem("kultura-cart")||"[]");
      if(Array.isArray(storedCart))setCart(storedCart.map((item:any,index:number)=>({key:String(item.key??`${item.productId??item.id??index}-${item.color??""}-${item.size??""}`),productId:Number(item.productId??item.id),name:String(item.name??"Товар"),price:Number(item.price)||0,image:String(item.image??"/assets/images/image-placeholder.svg"),quantity:Math.max(1,Number(item.quantity)||1),color:item.color??item.selectedColor,size:item.size??item.selectedSize})).filter((item:CartLine)=>item.productId));
      const storedFavorites=JSON.parse(localStorage.getItem("kultura-favorites")||"[]");
      if(Array.isArray(storedFavorites))setFavorites(storedFavorites.map(Number).filter(Boolean));
    }catch{}
    const params=new URLSearchParams(window.location.search);const requested=params.get("open") as Panel;
    if(["menu","search","account","favorites","cart","checkout"].includes(String(requested)))setPanelState(requested);
    hydrated.current=true;
  },[]);
  useEffect(()=>{if(hydrated.current)localStorage.setItem("kultura-cart",JSON.stringify(cart))},[cart]);
  useEffect(()=>{if(hydrated.current)localStorage.setItem("kultura-favorites",JSON.stringify(favorites))},[favorites]);
  useEffect(()=>{if(!panel)return;const before=document.body.style.overflow;document.body.style.overflow="hidden";return()=>{document.body.style.overflow=before}},[panel]);

  const setPanel=useCallback((next:Panel)=>{setPanelState(next);if(next!=="quick")setQuick(current=>next===null?null:current)},[]);
  const openQuick=useCallback((product:Product)=>{setQuick(product);setPanelState("quick")},[]);
  const toggleFavorite=useCallback((id:number)=>setFavorites(current=>current.includes(id)?current.filter(value=>value!==id):[...current,id]),[]);
  const addProduct=useCallback((product:Product,variant?:Variant,size?:string)=>{
    const sku=selectedSku(product,variant,size);const chosenSize=size||sku?.size;const chosenColor=variant?.name||sku?.sourceColor||sku?.color;const price=Number(sku?.price)||productPrice(product,variant,chosenSize);const image=variant?.image||sku?.image||product.image;const key=`${product.id}-${norm(chosenColor)}-${norm(chosenSize)}`;
    setCart(current=>{const found=current.find(line=>line.key===key);return found?current.map(line=>line.key===key?{...line,quantity:line.quantity+1}:line):[...current,{key,productId:product.id,name:product.name,price,image,quantity:1,color:chosenColor,size:chosenSize}]});
    setPanelState("cart");
  },[]);
  const changeQty=useCallback((key:string,delta:number)=>setCart(current=>current.map(line=>line.key===key?{...line,quantity:Math.max(1,line.quantity+delta)}:line)),[]);
  const removeLine=useCallback((key:string)=>setCart(current=>current.filter(line=>line.key!==key)),[]);
  const value=useMemo(()=>({panel,setPanel,quick,openQuick,cart,favorites,toggleFavorite,addProduct,changeQty,removeLine}),[panel,setPanel,quick,openQuick,cart,favorites,toggleFavorite,addProduct,changeQty,removeLine]);
  return <CommerceContext.Provider value={value}>{children}</CommerceContext.Provider>;
}

function Header(){
  const {setPanel,cart,favorites}=useCommerce();const count=cart.reduce((sum,line)=>sum+line.quantity,0);
  return <>
    <div className="fast-promo"><span>БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</span><Link href="/catalog/">ПОДРОБНЕЕ</Link></div>
    <header className="fast-header">
      <div className="fast-header-side fast-header-left"><button className="fast-icon-btn" onClick={()=>setPanel("menu")} aria-label="Меню"><Icon name="menu"/></button><Link className="fast-boutiques" href="/#boutiques">Бутики</Link></div>
      <Link className="fast-logo" href="/">КУЛЬТУРА ДОМА</Link>
      <div className="fast-header-side fast-actions">
        <button className="fast-icon-btn" onClick={()=>setPanel("search")} aria-label="Поиск"><Icon name="search"/></button>
        <button className="fast-icon-btn" onClick={()=>setPanel("account")} aria-label="Профиль"><Icon name="user"/></button>
        <button className="fast-icon-btn" onClick={()=>setPanel("favorites")} aria-label="Избранное"><Icon name="heart"/>{favorites.length>0&&<b>{favorites.length}</b>}</button>
        <button className="fast-icon-btn" onClick={()=>setPanel("cart")} aria-label="Корзина"><Icon name="bag"/>{count>0&&<b>{count}</b>}</button>
      </div>
    </header>
  </>;
}

function Footer(){return <footer className="fast-footer"><div><Link className="fast-logo" href="/">КУЛЬТУРА ДОМА</Link><p>Предметы для дома с русским характером.</p></div><nav><Link href="/catalog/">Каталог</Link><Link href="/capsules/">Капсулы</Link><Link href="/collections/">Коллекции</Link><Link href="/ready-solutions/">Готовые решения</Link></nav><small>© 2026 Культура дома</small></footer>}

function MenuPanel(){const {setPanel}=useCommerce();return <PanelShell title="Меню" onClose={()=>setPanel(null)} side="left"><nav className="fast-menu-nav"><Link href="/catalog/" onClick={()=>setPanel(null)}>Все товары</Link>{CATEGORIES.filter(name=>name!=="Все товары").map(name=><Link key={name} href={`/catalog/?category=${encodeURIComponent(name)}`} onClick={()=>setPanel(null)}>{name}</Link>)}<hr/><Link href="/capsules/" onClick={()=>setPanel(null)}>Капсулы</Link><Link href="/collections/" onClick={()=>setPanel(null)}>Коллекции</Link><Link href="/ready-solutions/" onClick={()=>setPanel(null)}>Готовые решения</Link><Link href="/constructor/" onClick={()=>setPanel(null)}>Конструктор</Link></nav></PanelShell>}

function PanelShell({title,onClose,children,side="right",wide=false}:{title:string;onClose:()=>void;children:React.ReactNode;side?:"left"|"right";wide?:boolean}){return <div className="fast-overlay" role="presentation" onMouseDown={event=>{if(event.target===event.currentTarget)onClose()}}><section className={`fast-drawer fast-drawer-${side} ${wide?"is-wide":""}`} role="dialog" aria-modal="true" aria-label={title}><header><h2>{title}</h2><button className="fast-icon-btn" onClick={onClose} aria-label="Закрыть"><Icon name="close"/></button></header><div className="fast-drawer-body">{children}</div></section></div>}

function SearchPanel(){
  const {setPanel,openQuick}=useCommerce();const [query,setQuery]=useState("");const results=useMemo(()=>{const q=norm(query);if(q.length<2)return [];return PRODUCTS.filter(product=>norm([product.name,product.article,product.note,product.category,product.collection,product.capsule].join(" ")).includes(q)).slice(0,12)},[query]);
  return <PanelShell title="Поиск" onClose={()=>setPanel(null)} wide><div className="fast-search-box"><Icon name="search"/><input autoFocus value={query} onChange={event=>setQuery(event.target.value)} placeholder="Что вы ищете?"/></div>{query.length<2?<p className="fast-muted">Введите хотя бы 2 символа</p>:results.length?<div className="fast-search-results">{results.map(product=><button key={product.id} onClick={()=>openQuick(product)}><img src={asset(product.image)} alt=""/><span><strong>{product.name}</strong><small>{product.note}</small></span><b>{rub(product.price)}</b></button>)}</div>:<p className="fast-muted">Ничего не найдено</p>}</PanelShell>
}

function AccountPanel(){
  const {setPanel}=useCommerce();const [saved,setSaved]=useState(false);const [contact,setContact]=useState("");useEffect(()=>{try{const profile=JSON.parse(localStorage.getItem("kultura-profile")||"{}");setContact(profile.contact||"")}catch{}},[]);
  const submit=(event:React.FormEvent)=>{event.preventDefault();localStorage.setItem("kultura-profile",JSON.stringify({contact}));setSaved(true)};
  return <PanelShell title="Профиль" onClose={()=>setPanel(null)}><div className="fast-account"><h3>{saved?"Данные сохранены":"Войти или зарегистрироваться"}</h3><p>Используйте номер телефона или email. Для прототипа данные сохраняются локально.</p><form onSubmit={submit}><label>Телефон или email<input required value={contact} onChange={event=>setContact(event.target.value)} placeholder="+7 999 000-00-00 или email"/></label><button className="fast-primary" type="submit">Продолжить</button></form></div></PanelShell>
}

function FavoritesPanel(){
  const {setPanel,favorites,openQuick,toggleFavorite}=useCommerce();const items=PRODUCTS.filter(product=>favorites.includes(product.id));
  return <PanelShell title={`Избранное${items.length?` · ${items.length}`:""}`} onClose={()=>setPanel(null)}>{items.length?<div className="fast-mini-list">{items.map(product=><article key={product.id}><button className="fast-mini-main" onClick={()=>openQuick(product)}><img src={asset(product.image)} alt=""/><span><strong>{product.name}</strong><small>{product.note}</small><b>{rub(product.price)}</b></span></button><button className="fast-text-btn" onClick={()=>toggleFavorite(product.id)}>Удалить</button></article>)}</div>:<EmptyState title="В избранном пока пусто" action="Перейти в каталог" href="/catalog/"/>}</PanelShell>
}

function CartPanel(){
  const {setPanel,cart,changeQty,removeLine}=useCommerce();const total=cart.reduce((sum,line)=>sum+line.price*line.quantity,0);
  return <PanelShell title={`Корзина${cart.length?` · ${cart.reduce((sum,line)=>sum+line.quantity,0)}`:""}`} onClose={()=>setPanel(null)}>{cart.length?<><div className="fast-cart-list">{cart.map(line=><article key={line.key}><img src={asset(line.image)} alt=""/><div><strong>{line.name}</strong><small>{[line.color,line.size].filter(Boolean).join(" · ")}</small><b>{rub(line.price)}</b><div className="fast-qty"><button onClick={()=>changeQty(line.key,-1)} aria-label="Уменьшить"><Icon name="minus"/></button><span>{line.quantity}</span><button onClick={()=>changeQty(line.key,1)} aria-label="Увеличить"><Icon name="plus"/></button></div><button className="fast-text-btn" onClick={()=>removeLine(line.key)}>Удалить</button></div></article>)}</div><div className="fast-cart-total"><span>Итого</span><strong>{rub(total)}</strong></div><button className="fast-primary" onClick={()=>setPanel("checkout")}>Оформить заказ</button></>:<EmptyState title="Корзина пока пуста" action="Перейти в каталог" href="/catalog/"/>}</PanelShell>
}

function CheckoutPanel(){
  const {setPanel,cart}=useCommerce();const [done,setDone]=useState(false);const total=cart.reduce((sum,line)=>sum+line.price*line.quantity,0);
  if(done)return <PanelShell title="Заказ оформлен" onClose={()=>setPanel(null)} wide><div className="fast-success"><span>✓</span><h3>Спасибо за заказ</h3><p>Это интерактивный прототип: заказ не отправлен в реальную систему.</p><button className="fast-primary" onClick={()=>setPanel(null)}>Продолжить покупки</button></div></PanelShell>;
  return <PanelShell title="Оформление заказа" onClose={()=>setPanel("cart")} wide><form className="fast-checkout" onSubmit={event=>{event.preventDefault();setDone(true)}}><section><h3>Контактные данные</h3><div className="fast-form-grid"><label>Имя<input required placeholder="Имя"/></label><label>Телефон или email<input required placeholder="+7 999 000-00-00"/></label></div></section><section><h3>Доставка</h3><label className="fast-radio"><input type="radio" name="delivery" defaultChecked/>Курьерская доставка</label><label className="fast-radio"><input type="radio" name="delivery"/>Самовывоз</label><label>Адрес<input required placeholder="Город, улица, дом"/></label></section><section><h3>Оплата</h3><label className="fast-radio"><input type="radio" name="payment" defaultChecked/>Банковской картой онлайн</label><label className="fast-radio"><input type="radio" name="payment"/>СБП</label></section><div className="fast-cart-total"><span>К оплате</span><strong>{rub(total)}</strong></div><button className="fast-primary" type="submit">Подтвердить заказ · {rub(total)}</button></form></PanelShell>
}

function QuickPanel(){
  const {quick,setPanel,addProduct,favorites,toggleFavorite}=useCommerce();const product=quick;const [variantIndex,setVariantIndex]=useState(0);const [size,setSize]=useState("");const [imageIndex,setImageIndex]=useState(0);
  useEffect(()=>{setVariantIndex(0);setSize("");setImageIndex(0)},[product?.id]);
  if(!product)return null;const variants=product.colorVariants??[];const variant=variants[variantIndex];const skus=variantSkus(product,variant);const sizes=uniq(skus.map(sku=>sku.size));const chosenSize=size||sizes[0]||"";const images=productImages(product,variant);const price=productPrice(product,variant,chosenSize);const liked=favorites.includes(product.id);
  return <PanelShell title="Товар" onClose={()=>setPanel(null)} wide><div className="fast-quick"><div className="fast-quick-media"><img src={asset(images[imageIndex]||product.image)} alt={product.name}/>{images.length>1&&<><button className="fast-media-prev" onClick={()=>setImageIndex(index=>(index-1+images.length)%images.length)} aria-label="Предыдущее фото">‹</button><button className="fast-media-next" onClick={()=>setImageIndex(index=>(index+1)%images.length)} aria-label="Следующее фото">›</button><div className="fast-media-dots">{images.map((_,index)=><button key={index} className={index===imageIndex?"is-active":""} onClick={()=>setImageIndex(index)} aria-label={`Фото ${index+1}`}/>)}</div></>}</div><div className="fast-quick-copy"><small>КУЛЬТУРА ДОМА</small><div className="fast-quick-title"><h2>{product.name}</h2><button className={`fast-heart ${liked?"is-active":""}`} onClick={()=>toggleFavorite(product.id)} aria-label="Избранное"><Icon name="heart"/></button></div><p>{product.note}</p><strong className="fast-quick-price">{rub(price)}</strong>{variants.length>1&&<div className="fast-choice"><span>{isAroma(product)?"Аромат":"Цвет"}</span><div className={isAroma(product)?"fast-aroma-list":"fast-swatch-list"}>{variants.map((item,index)=>isAroma(product)?<button key={item.name} className={index===variantIndex?"is-active":""} onClick={()=>{setVariantIndex(index);setSize("");setImageIndex(0)}}>{item.name}</button>:<button key={item.name} className={index===variantIndex?"is-active":""} title={item.name} aria-label={item.name} style={{background:item.hex||"#eee"}} onClick={()=>{setVariantIndex(index);setSize("");setImageIndex(0)}}/>)}</div></div>}{sizes.length>0&&<div className="fast-choice"><span>Размер</span><div className="fast-size-list">{sizes.map(value=><button key={value} className={norm(value)===norm(chosenSize)?"is-active":""} onClick={()=>setSize(value)}>{value}</button>)}</div></div>}<button className="fast-primary" onClick={()=>addProduct(product,variant,chosenSize)}>Добавить в корзину · {rub(price)}</button><details><summary>Информация о товаре</summary><p>{[skus[0]?.material,skus[0]?.composition,skus[0]?.details].filter(Boolean).join(" · ")||product.note}</p></details></div></div></PanelShell>
}

function EmptyState({title,action,href:to}:{title:string;action:string;href:string}){return <div className="fast-empty"><h3>{title}</h3><Link className="fast-primary" href={to}>{action}</Link></div>}

function Overlays(){const {panel}=useCommerce();if(!panel)return null;if(panel==="menu")return <MenuPanel/>;if(panel==="search")return <SearchPanel/>;if(panel==="account")return <AccountPanel/>;if(panel==="favorites")return <FavoritesPanel/>;if(panel==="cart")return <CartPanel/>;if(panel==="checkout")return <CheckoutPanel/>;if(panel==="quick")return <QuickPanel/>;return null}

function SiteFrame({children}:{children:React.ReactNode}){return <CommerceProvider><div className="fast-site"><Header/><main>{children}</main><Footer/><Overlays/></div></CommerceProvider>}

function ProductCard({product,priority=false}:{product:Product;priority?:boolean}){
  const {openQuick,addProduct,favorites,toggleFavorite}=useCommerce();const variants=product.colorVariants??[];const [variantIndex,setVariantIndex]=useState(0);const variant=variants[variantIndex];const liked=favorites.includes(product.id);const skus=variantSkus(product,variant);const sizes=uniq(skus.map(sku=>sku.size));const price=productPrice(product,variant,sizes[0]);const image=variant?.image||skus[0]?.image||product.image;const oldPrice=Number(skus[0]?.oldPrice)||Number(product.oldPrice)||0;
  const quickAdd=()=>{if(sizes.length>1||variants.length>1){openQuick(product);return}addProduct(product,variant,sizes[0])};
  return <article className="fast-product-card"><div className="fast-product-media"><button className="fast-product-image" onClick={()=>openQuick(product)}><img src={asset(image)} alt={product.name} loading={priority?"eager":"lazy"} decoding="async" fetchPriority={priority?"high":"auto"}/></button><button className={`fast-card-heart ${liked?"is-active":""}`} onClick={()=>toggleFavorite(product.id)} aria-label="Избранное"><Icon name="heart"/></button></div><button className="fast-product-copy" onClick={()=>openQuick(product)}><strong>{product.name}</strong><small>{[variant?.name&&variants.length>1?variant.name.toLocaleLowerCase("ru-RU"):"",product.note].filter(Boolean).join(", ")}</small><span><b>{rub(price)}</b>{oldPrice>price&&<del>{rub(oldPrice)}</del>}</span></button>{variants.length>1&&!isAroma(product)&&<div className="fast-card-swatches">{variants.slice(0,6).map((item,index)=><button key={item.name} className={index===variantIndex?"is-active":""} style={{background:item.hex||"#eee"}} title={item.name} aria-label={item.name} onClick={()=>setVariantIndex(index)}/>)}</div>}{variants.length>1&&isAroma(product)&&<div className="fast-card-aromas">{variants.slice(0,2).map((item,index)=><button key={item.name} className={index===variantIndex?"is-active":""} onClick={()=>setVariantIndex(index)}>{item.name}</button>)}</div>}<button className="fast-card-add" onClick={quickAdd} aria-label="Добавить в корзину"><Icon name="bag"/><span>Добавить</span></button></article>
}

function ProductRail({products}:{products:Product[]}){return <div className="fast-product-rail">{products.map((product,index)=><ProductCard key={product.id} product={product} priority={index<2}/>)}</div>}

const HERO=[
  {eyebrow:"НОВИНКИ",title:"Новое для дома",image:"/assets/images/1_new_desktop.png",mobile:"/assets/images/1_new_mobile.png",to:"/catalog/"},
  {eyebrow:"СПАЛЬНЯ",title:"Тактильный покой",image:"/assets/images/2_sleep_desktop.png",mobile:"/assets/images/2_sleep_mobile.png",to:"/catalog/?category=Постельное%20белье"},
  {eyebrow:"СТОЛОВАЯ",title:"Сервировка как ритуал",image:"/assets/images/3_stol_desktop.png",mobile:"/assets/images/3_stol_mobile.png",to:"/catalog/?category=Посуда%20и%20сервировка"},
];
const HOME_CATEGORIES=[
  ["Спальня","Постельное белье","/assets/images/1spal.png"],
  ["Посуда и сервировка","Посуда и сервировка","/assets/images/2stol.png"],
  ["Столовый текстиль","Столовый текстиль","/assets/images/3stoltekstil.png"],
  ["Декор","Декор для дома","/assets/images/4dekor.png"],
  ["Текстиль для дома","Пледы и подушки","/assets/images/5homeclothes.png"],
];
const NEW_ARTICLES=["KD-PD-1024","KD-PD-1023","KD-PD-1026","KD-PD-1028","KD-PD-1128","KD-PD-2519"];
const NEW_PRODUCTS=NEW_ARTICLES.map(article=>PRODUCTS.find(product=>product.article===article)).filter((product):product is Product=>Boolean(product)).concat(PRODUCTS).filter((product,index,array)=>array.findIndex(item=>item.id===product.id)===index).slice(0,8);

function LazyBrandVideo(){const ref=useRef<HTMLVideoElement|null>(null);const [ready,setReady]=useState(false);useEffect(()=>{const node=ref.current;if(!node)return;const observer=new IntersectionObserver(entries=>{if(entries.some(entry=>entry.isIntersecting)){setReady(true);observer.disconnect()}},{rootMargin:"250px"});observer.observe(node);return()=>observer.disconnect()},[]);return <video ref={ref} muted loop playsInline autoPlay={ready} preload="none" poster={asset("/assets/images/green.jpeg")}>{ready&&<source src={asset("/assets/video/kultura-brand-desktop.mp4")} type="video/mp4"/>}</video>}

function HomeContent(){
  const heroRef=useRef<HTMLDivElement|null>(null);const [hero,setHero]=useState(0);const capsules=uniq(PRODUCTS.map(product=>product.capsule)).slice(0,5);
  return <>
    <section className="fast-hero"><div className="fast-hero-track" ref={heroRef} onScroll={event=>{const node=event.currentTarget;setHero(Math.round(node.scrollLeft/Math.max(1,node.clientWidth)))}}>{HERO.map((item,index)=><article key={item.eyebrow}><picture><source media="(max-width:700px)" srcSet={asset(item.mobile)}/><img src={asset(item.image)} alt="" fetchPriority={index===0?"high":"auto"}/></picture><div className="fast-hero-copy"><small>{item.eyebrow}</small><h1>{item.title}</h1><Link href={item.to}>Смотреть</Link></div></article>)}</div><div className="fast-hero-dots">{HERO.map((_,index)=><button key={index} className={hero===index?"is-active":""} onClick={()=>heroRef.current?.scrollTo({left:index*(heroRef.current?.clientWidth||0),behavior:"smooth"})}/>)}</div></section>
    <section className="fast-section"><SectionHead title="Для дома" to="/catalog/" action="Весь каталог"/><div className="fast-category-rail">{HOME_CATEGORIES.map(([name,category,image])=><Link key={name} href={`/catalog/?category=${encodeURIComponent(category)}`}><img src={asset(image)} alt="" loading="lazy"/><strong>{name}</strong></Link>)}</div></section>
    <section className="fast-section"><SectionHead title="Новинки" to="/catalog/" action="Смотреть все"/><ProductRail products={NEW_PRODUCTS}/></section>
    <section className="fast-section fast-brand"><div className="fast-brand-copy"><small>О БРЕНДЕ</small><h2>Традиции в каждом доме</h2></div><LazyBrandVideo/></section>
    <section className="fast-section"><SectionHead title="Капсулы" to="/capsules/" action="Все капсулы"/><div className="fast-story-rail">{capsules.map(name=><Link key={name} href={`/catalog/?capsule=${encodeURIComponent(name)}`}><img src={asset(CAPSULE_IMAGE[name]||PRODUCTS.find(product=>product.capsule===name)?.image||"/assets/images/image-placeholder.svg")} alt="" loading="lazy"/><strong>{name}</strong></Link>)}<Link className="fast-story-more" href="/collections/"><span>Коллекции</span><strong>Смотреть все →</strong></Link></div></section>
    <section className="fast-section fast-ready"><SectionHead title="Готовые решения" to="/ready-solutions/" action="Смотреть все"/><div className="fast-ready-grid"><Link href="/ready-solutions/"><img src={asset("/assets/images/3_stol_desktop.png")} alt="" loading="lazy"/><strong>Красные линии</strong></Link><Link href="/ready-solutions/"><img src={asset("/assets/images/green.jpeg")} alt="" loading="lazy"/><strong>Зелёный салон</strong></Link><Link href="/constructor/"><img src={asset("/assets/images/2_sleep_desktop.png")} alt="" loading="lazy"/><strong>Собрать своё решение</strong></Link></div></section>
    <div id="boutiques" className="fast-boutiques-block"><small>БУТИКИ</small><h2>Посмотреть предметы вживую</h2><p>Москва · Санкт-Петербург</p></div>
  </>
}
function SectionHead({title,to,action}:{title:string;to:string;action:string}){return <header className="fast-section-head"><h2>{title}</h2><Link href={to}>{action}</Link></header>}

export function FastHome(){return <SiteFrame><HomeContent/></SiteFrame>}

type Filters={subcategory:string[];material:string[];color:string[];collection:string[];capsule:string[];size:string[];min:string;max:string};
const emptyFilters=():Filters=>({subcategory:[],material:[],color:[],collection:[],capsule:[],size:[],min:"",max:""});
const toggle=(values:string[],value:string)=>values.some(item=>norm(item)===norm(value))?values.filter(item=>norm(item)!==norm(value)):[...values,value];
function skuColor(sku:Sku){return sku.sourceColor||sku.color||""}
function productMatches(product:Product,category:string,filters:Filters,query:string){
  if(category!=="Все товары"&&norm(product.category)!==norm(category))return false;if(query&& !norm([product.name,product.article,product.note].join(" ")).includes(norm(query)))return false;
  if(filters.subcategory.length&&!filters.subcategory.some(value=>norm(value)===norm(product.subcategory)))return false;
  if(filters.collection.length&&!filters.collection.some(value=>norm(value)===norm(product.collection)))return false;
  if(filters.capsule.length&&!filters.capsule.some(value=>norm(value)===norm(product.capsule)))return false;
  const skus=productSkus(product);const skuMatch=skus.some(sku=>{
    if(filters.material.length&&!filters.material.some(value=>norm(value)===norm(sku.material)))return false;
    if(filters.color.length&&!filters.color.some(value=>norm(value)===norm(skuColor(sku))))return false;
    if(filters.size.length&&!filters.size.some(value=>norm(value)===norm(sku.size)))return false;
    const price=Number(sku.price)||Number(product.price)||0;if(filters.min&&price<Number(filters.min))return false;if(filters.max&&price>Number(filters.max))return false;return true;
  });return skus.length?skuMatch:!(filters.material.length||filters.color.length||filters.size.length||filters.min||filters.max);
}

function CategoryRail({category,onChange}:{category:string;onChange:(value:string)=>void}){const ref=useRef<HTMLDivElement|null>(null);return <div className="fast-category-slider-shell"><button className="fast-slider-arrow is-left" onClick={()=>ref.current?.scrollBy({left:-300,behavior:"smooth"})} aria-label="Назад">‹</button><div className="fast-category-slider" ref={ref}>{CATEGORIES.map(name=><button key={name} className={norm(name)===norm(category)?"is-active":""} onClick={()=>onChange(name)}>{name}</button>)}</div><button className="fast-slider-arrow is-right" onClick={()=>ref.current?.scrollBy({left:300,behavior:"smooth"})} aria-label="Вперёд">›</button></div>}

function FilterDrawer({filters,setFilters,onClose,count,products}:{filters:Filters;setFilters:(filters:Filters)=>void;onClose:()=>void;count:number;products:Product[]}){
  const subcategories=uniq(products.map(product=>product.subcategory));const collections=uniq(products.map(product=>product.collection));const capsules=uniq(products.map(product=>product.capsule));const skus=products.flatMap(product=>productSkus(product));const materials=uniq(skus.map(sku=>sku.material));const colors=uniq(skus.map(sku=>skuColor(sku)));const sizes=uniq(skus.map(sku=>sku.size));
  return <div className="fast-overlay fast-filter-overlay" onMouseDown={event=>{if(event.target===event.currentTarget)onClose()}}><section className="fast-filter-drawer"><header><div><h2>Фильтры</h2><small>{count} товаров</small></div><button className="fast-icon-btn" onClick={onClose}><Icon name="close"/></button></header><div className="fast-filter-scroll"><FilterGroup title="Тип товара" values={subcategories} selected={filters.subcategory} onToggle={value=>setFilters({...filters,subcategory:toggle(filters.subcategory,value)})}/><FilterGroup title="Цвет" values={colors} selected={filters.color} onToggle={value=>setFilters({...filters,color:toggle(filters.color,value)})} swatches/><FilterGroup title="Материал" values={materials} selected={filters.material} onToggle={value=>setFilters({...filters,material:toggle(filters.material,value)})}/><FilterGroup title="Размер" values={sizes} selected={filters.size} onToggle={value=>setFilters({...filters,size:toggle(filters.size,value)})}/><FilterGroup title="Капсула" values={capsules} selected={filters.capsule} onToggle={value=>setFilters({...filters,capsule:toggle(filters.capsule,value)})}/><FilterGroup title="Коллекция" values={collections} selected={filters.collection} onToggle={value=>setFilters({...filters,collection:toggle(filters.collection,value)})}/><details className="fast-filter-group"><summary>Цена</summary><div className="fast-price-row"><label>От<input inputMode="numeric" value={filters.min} onChange={event=>setFilters({...filters,min:event.target.value.replace(/\D/g,"")})}/></label><label>До<input inputMode="numeric" value={filters.max} onChange={event=>setFilters({...filters,max:event.target.value.replace(/\D/g,"")})}/></label></div></details></div><footer><button className="fast-secondary" onClick={()=>setFilters(emptyFilters())}>Сбросить</button><button className="fast-primary" onClick={onClose}>Показать {count}</button></footer></section></div>
}
function FilterGroup({title,values,selected,onToggle,swatches=false}:{title:string;values:string[];selected:string[];onToggle:(value:string)=>void;swatches?:boolean}){const [more,setMore]=useState(false);const shown=more?values:values.slice(0,8);return <details className="fast-filter-group"><summary>{title}{selected.length>0&&<b>{selected.length}</b>}</summary><div>{shown.map(value=><label key={value}><input type="checkbox" checked={selected.some(item=>norm(item)===norm(value))} onChange={()=>onToggle(value)}/>{swatches&&<i className="fast-filter-swatch" style={{background:colorHex(value)}}/>}<span>{labelCase(value)}</span></label>)}{values.length>8&&<button className="fast-more" onClick={()=>setMore(value=>!value)}>{more?"Скрыть":"Показать ещё"}</button>}</div></details>}
function labelCase(value:string){const text=String(value).trim();return text?text.charAt(0).toLocaleUpperCase("ru-RU")+text.slice(1).toLocaleLowerCase("ru-RU"):text}
function colorHex(value:string){const colors:Record<string,string>={"белый":"#f5f4ef","молочный":"#eee7da","экрю":"#ded0b6","бежевый":"#cdb99b","голубой":"#93b8cb","синий":"#496c8a","ночной синий":"#142a45","серо-синий":"#667b89","зеленый":"#657a61","зелёный":"#657a61","красный":"#9e403b","коричневый":"#765a46","черный":"#1d1d1b","чёрный":"#1d1d1b","желтый":"#d9b84e","жёлтый":"#d9b84e","пудровый":"#d8b0a4","серебряный":"#b9b9b4","прозрачный":"#f3f4f2"};return colors[norm(value)]||"#e8e5df"}

function CatalogContent(){
  const [category,setCategory]=useState("Все товары");const [filters,setFilters]=useState<Filters>(emptyFilters);const [sort,setSort]=useState("popular");const [filterOpen,setFilterOpen]=useState(false);const [visible,setVisible]=useState(24);const [query,setQuery]=useState("");
  useEffect(()=>{const params=new URLSearchParams(window.location.search);setCategory(CATEGORIES.find(name=>norm(name)===norm(params.get("category")))||"Все товары");setQuery(params.get("q")||"");const next=emptyFilters();const capsule=params.get("capsule"),collection=params.get("collection");if(capsule)next.capsule=[capsule];if(collection)next.collection=[collection];setFilters(next)},[]);
  const base=useMemo(()=>category==="Все товары"?PRODUCTS:PRODUCTS.filter(product=>norm(product.category)===norm(category)),[category]);
  const filtered=useMemo(()=>{const rows=PRODUCTS.filter(product=>productMatches(product,category,filters,query));if(sort==="price_asc")return [...rows].sort((a,b)=>a.price-b.price);if(sort==="price_desc")return [...rows].sort((a,b)=>b.price-a.price);return rows},[category,filters,query,sort]);
  const activeCount=Object.entries(filters).reduce((sum,[key,value])=>sum+(Array.isArray(value)?value.length:(value?1:0)),0);const page=filtered.slice(0,visible);
  const changeCategory=(value:string)=>{setCategory(value);setFilters(emptyFilters());setVisible(24);const params=new URLSearchParams();if(value!=="Все товары")params.set("category",value);history.pushState({},"",`${location.pathname}${params.size?`?${params}`:""}`);window.scrollTo({top:0,behavior:"smooth"})};
  return <div className="fast-catalog"><nav className="fast-crumbs"><Link href="/">Главная</Link><span>/</span><Link href="/catalog/">Каталог</Link></nav><header className="fast-catalog-title"><div><h1>{category}</h1><span>{filtered.length} товаров</span></div></header><CategoryRail category={category} onChange={changeCategory}/><div className="fast-catalog-tools"><button onClick={()=>setFilterOpen(true)}><Icon name="filter"/><span>Фильтры{activeCount?` (${activeCount})`:""}</span></button><label><span>Сортировка</span><select value={sort} onChange={event=>setSort(event.target.value)}><option value="popular">По популярности</option><option value="price_asc">Сначала дешевле</option><option value="price_desc">Сначала дороже</option></select></label></div>{activeCount>0&&<div className="fast-active-filters"><button onClick={()=>setFilters(emptyFilters())}>Сбросить все</button>{filters.capsule.map(value=><span key={value}>Капсула: {value}</span>)}{filters.collection.map(value=><span key={value}>Коллекция: {value}</span>)}</div>}{page.length?<div className="fast-product-grid">{page.map((product,index)=><ProductCard key={product.id} product={product} priority={index<6}/>)}</div>:<div className="fast-no-results"><h2>По выбранным фильтрам товаров нет</h2><button className="fast-primary" onClick={()=>setFilters(emptyFilters())}>Сбросить фильтры</button></div>}{visible<filtered.length&&<button className="fast-load-more" onClick={()=>setVisible(value=>value+24)}>Показать ещё <span>{Math.min(24,filtered.length-visible)}</span></button>}{filterOpen&&<FilterDrawer filters={filters} setFilters={value=>{setFilters(value);setVisible(24)}} onClose={()=>setFilterOpen(false)} count={filtered.length} products={base}/>}</div>
}
export function FastCatalog(){return <SiteFrame><CatalogContent/></SiteFrame>}

function StoriesContent({mode}:{mode:"capsules"|"collections"}){
  const key=mode==="capsules"?"capsule":"collection";const names=uniq(PRODUCTS.map(product=>product[key]));return <div className="fast-stories"><nav className="fast-crumbs"><Link href="/">Главная</Link><span>/</span><span>{mode==="capsules"?"Капсулы":"Коллекции"}</span></nav><header><small>КУЛЬТУРА ДОМА</small><h1>{mode==="capsules"?"Капсулы":"Коллекции"}</h1><p>{mode==="capsules"?"Готовые истории, объединённые цветом, фактурой и настроением.":"Предметы, связанные общей идеей и авторской эстетикой."}</p></header><div className="fast-stories-grid">{names.map(name=>{const products=PRODUCTS.filter(product=>norm(product[key])===norm(name));const image=mode==="capsules"?(CAPSULE_IMAGE[name]||products[0]?.image):products[0]?.image;return <Link key={name} href={`/catalog/?${key}=${encodeURIComponent(name)}`}><img src={asset(image||"/assets/images/image-placeholder.svg")} alt="" loading="lazy"/><div><small>{mode==="capsules"?"КАПСУЛА":"КОЛЛЕКЦИЯ"}</small><h2>{name}</h2><span>{products.length} товаров →</span></div></Link>})}</div></div>
}
export function FastCapsules(){return <SiteFrame><StoriesContent mode="capsules"/></SiteFrame>}
export function FastCollections(){return <SiteFrame><StoriesContent mode="collections"/></SiteFrame>}
