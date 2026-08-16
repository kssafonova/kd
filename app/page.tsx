"use client";

import { assetUrl } from "./assets";

import { useEffect, useMemo, useState } from "react";

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
  hasBundle?: boolean;
  hasRichContent?: boolean;
  gallery?: string[];
};

type ColorVariant = { name: string; hex: string; image: string; position?: string };
type CartItem = Product & { selectedSize: string; selectedColor: string; quantity: number };
type Slide = { category:string; eyebrow:string; title:string; subtitle:string; image:string; secondaryImage?:string; mobileVideo?:string; align:string; destination:View };
type Profile = { name:string; surname:string; email:string; phone:string; city:string; address:string };

const fmt = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;

type IconName = "pin" | "search" | "user" | "heart" | "bag" | "filter" | "close" | "chevron" | "share" | "plus" | "minus" | "arrow" | "mail";
function Icon({ name, filled = false }: { name: IconName; filled?: boolean }) {
  const common = { fill: filled ? "currentColor" : "none", stroke: "currentColor", strokeWidth: 1.7, strokeLinecap: "round" as const, strokeLinejoin: "round" as const };
  if (name === "pin") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/></svg>;
  if (name === "search") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.3 15.3 5.2 5.2"/></svg>;
  if (name === "user") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><circle cx="12" cy="7.2" r="4"/><path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6"/></svg>;
  if (name === "heart") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z"/></svg>;
  if (name === "bag") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z"/><path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8"/></svg>;
  if (name === "filter") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M3 6h8m4 0h6M3 12h3m4 0h11M3 18h11m4 0h3"/><circle cx="13" cy="6" r="2"/><circle cx="8" cy="12" r="2"/><circle cx="16" cy="18" r="2"/></svg>;
  if (name === "close") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m5 5 14 14M19 5 5 19"/></svg>;
  if (name === "share") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M12 16V3m0 0L7.5 7.5M12 3l4.5 4.5"/><path d="M5 11v9h14v-9"/></svg>;
  if (name === "plus") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M12 5v14M5 12h14"/></svg>;
  if (name === "minus") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M5 12h14"/></svg>;
  if (name === "mail") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="m4 7 8 6 8-6"/></svg>;
  if (name === "arrow") return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="M4 12h15m-5-5 5 5-5 5"/></svg>;
  return <svg viewBox="0 0 24 24" aria-hidden="true" {...common}><path d="m8 4 8 8-8 8"/></svg>;
}

const products: Product[] = [
  { id: 1, name: "Постельное бельё «Русский узор»", note: "лён и хлопок, вышивка", price: 18990, oldPrice: 25990, image: "/images/russian-bedroom.png", position: "center", hasBundle: true, hasRichContent: true, colorVariants: [
    { name: "Молочный", hex: "#f1eee7", image: "/images/russian-bedroom.png" }, { name: "Песочный", hex: "#c5ad8e", image: "/images/beige-bedroom.png" }, { name: "Ночной синий", hex: "#12243e", image: "/images/zip-collection-night.png" },
  ] },
  { id: 2, name: "Хлопковый пододеяльник с оборкой", note: "хлопок, 200×220 см", price: 18990, image: "/images/zip-product-bed.png", badge: "НОВИНКА", hasBundle: true, gallery: ["/images/zip-product-bed.png","/images/classic-bedroom.png","/images/beige-bedroom.png"], colorVariants: [
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
  { id: 9, name: "Сервиз «Северное сияние»", note: "костяной фарфор, 6 персон", price: 24990, image: "/images/russian-service-blue.png", hasBundle: true, colorVariants:[{name:"Бело-голубой",hex:"#d9edf0",image:"/images/russian-service-blue.png"},{name:"Ночной синий",hex:"#10233e",image:"/images/time-table.png"}] },
  { id: 10, name: "Чайная пара «Нити времени»", note: "костяной фарфор, 250 мл", price: 4490, image: "/images/time-tea-pair.png", gallery:["/images/time-tea-pair.png","/images/time-mug.png","/images/time-table.png"], colorVariants:[{name:"Ночной синий",hex:"#10233e",image:"/images/time-tea-pair.png"}] },
  { id: 11, name: "Подушка «Небесная гладь»", note: "бархат, 25×60 см", price: 4990, image: "/images/sky-bolster.png", colorVariants:[{name:"Небесный",hex:"#9fc2d3",image:"/images/sky-bolster.png"},{name:"Ночной синий",hex:"#203753",image:"/images/time-hero.png"}] },
  { id: 12, name: "Комплект «Голубая светлица»", note: "сатин, вышивка гладью", price: 21990, image: "/images/blue-bedding-vertical.png", hasRichContent: true, colorVariants:[{name:"Ледяной голубой",hex:"#afcbd1",image:"/images/blue-bedding-vertical.png"},{name:"Белый",hex:"#f4f2ec",image:"/images/zip-product-bed.png"}] },
];

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
    const item: CartItem = { ...product, image: selectedVariant?.image ?? product.image, position: selectedVariant?.position ?? product.position, selectedSize: chosenSize, selectedColor: selectedVariant?.name ?? "Молочный", quantity };
    setCart((current) => [...current, item]);
    setPlpSize(null); setSizeSheet(false); setCartOpen(true);
  };
  const addFromPLP = (product: Product, chosenSize: string, quantity: number, unitPrice: number) => {
    const selectedVariant = product.colorVariants?.find((variant) => variant.name === product.selectedColor) ?? product.colorVariants?.[0];
    const item: CartItem = { ...product, price: unitPrice, image: selectedVariant?.image ?? product.image, position: selectedVariant?.position ?? product.position, selectedSize: chosenSize, selectedColor: selectedVariant?.name ?? "Молочный", quantity };
    setCart((current)=>[...current,item]); setPlpSize(null); setPlpAdded(item);
  };
  const addBundle = (items: Product[]) => {
    const bundleItems: CartItem[] = items.map((product)=>({ ...product, selectedSize: product.selectedSize ?? "Евро 200×220", selectedColor: product.selectedColor ?? product.colorVariants?.[0]?.name ?? "Молочный", quantity: product.quantity ?? 1 }));
    setCart((current)=>[...current,...bundleItems]); setCartOpen(true);
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
      {view === "editorial" && <EditorialView editorial={editorial} buyBundle={addBundle} selectProduct={openProduct} favorite={favorite} favorites={favorites} />}
      {view === "product" && <ProductView product={selected} favorite={favorite} liked={favorites.includes(selected.id)} chooseSize={() => setSizeSheet(true)} add={(p) => add(p,p.selectedSize,p.quantity)} buyBundle={addBundle} selectProduct={openProduct} />}
      <Footer go={go} notice={notice} />

      {menu && <Menu current={menuSection} setCurrent={setMenuSection} close={() => { setMenu(false); setMenuSection(""); }} go={go} openCatalog={openCatalog} />}
      {search && <Search close={() => setSearch(false)} choose={(p) => { setSelected(p); setSearch(false); go("product"); }} />}
      {account && <Account profile={profile} close={() => setAccount(false)} notice={notice} save={setProfile} logout={()=>setProfile(null)} />}
      {favoritesOpen&&<Favorites ids={favorites} close={()=>setFavoritesOpen(false)} remove={favorite} choose={(product)=>{setSelected(product);setFavoritesOpen(false);go("product")}} quickAdd={(product)=>{setFavoritesOpen(false);setPlpSize(product)}}/>}
      {filters && <Filters close={() => setFilters(false)} apply={() => { setFilters(false); notice("Фильтры применены"); }} />}
      {plpSize && <PLPSizeFlow product={plpSize} close={() => setPlpSize(null)} add={(chosenSize,quantity,unitPrice) => addFromPLP(plpSize, chosenSize, quantity, unitPrice)} />}
      {plpAdded && <PLPAdded product={plpAdded} close={()=>setPlpAdded(null)} openCart={()=>{setPlpAdded(null);setCartOpen(true)}} selectRecommendation={(product)=>{setPlpAdded(null);setPlpSize(product)}} />}
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
  const current = slides[slide];
  const featuredProducts = slideProductIds[slide].map(id=>products.find(product=>product.id===id)!).filter(Boolean);
  return <>
    <section className={`hero ${current.align} ${current.secondaryImage?"editorial-hero":""}`}>
      <div className={`hero-media ${current.secondaryImage?"split-media":""}`}><img src={assetUrl(current.image)} alt={current.title}/>{current.secondaryImage&&<img src={assetUrl(current.secondaryImage)} alt="Сервировка Культура дома"/>}</div>
      {current.mobileVideo&&<video className="hero-mobile-video" autoPlay muted loop playsInline poster={assetUrl(current.image)}><source src={assetUrl(current.mobileVideo)} type="video/mp4"/></video>}
      <div className="hero-shade"/>
      <div className="hero-copy"><p>{current.eyebrow}</p><h1>{current.title}</h1><span>{current.subtitle}</span><button onClick={() => go(current.destination)}>СМОТРЕТЬ <b>→</b></button></div>
      <button className="hero-arrow prev" onClick={() => setSlide((slide + slides.length - 1) % slides.length)} aria-label="Предыдущий баннер"><Icon name="chevron"/></button>
      <button className="hero-arrow next" onClick={() => setSlide((slide + 1) % slides.length)} aria-label="Следующий баннер"><Icon name="chevron"/></button>
      <div className="hero-dots">{slides.map((_, i)=><button key={i} className={i === slide ? "active" : ""} onClick={() => setSlide(i)} aria-label={`Баннер ${i+1}`}/>)}</div>
      <nav className="hero-nav">{slides.map((item,i)=><button key={item.category} className={i===slide?"active":""} onClick={() => setSlide(i)}>{item.category}</button>)}</nav>
    </section>

    <section className="section home-shelf"><div className="shelf-title"><div><p>КОЛЛЕКЦИИ</p><h2>Выбор для вашего дома</h2></div><button onClick={()=>go("catalog")}>СМОТРЕТЬ ВСЕ →</button></div>
      <div className="category-grid">{categories.map(([name,image], i)=><button className={`category-card c${i}`} key={name} onClick={() => i===2 ? go("collections") : go("catalog")}><img src={assetUrl(image)} alt={name}/><span>{name}</span><b>Смотреть категорию →</b></button>)}</div>
    </section>

    <section className="editorial"><img src={assetUrl("/images/time-hero.png")} alt="Капсула Нити времени"/><div><p>НОВАЯ КАПСУЛА</p><h2>Нити времени</h2><span>Вдохновлена движением звёзд<br/>и бесконечной красотой ночного неба.</span><button onClick={() => go("collections")}>ОТКРЫТЬ ИСТОРИЮ →</button></div></section>

    <section className="section products-section"><div className="section-head row"><div><p>ВЫБОР РЕДАКЦИИ · {current.category}</p><h2>{slide===0?"Современное русское лето":slide===1?"Для спокойной спальни":slide===2?"Искусство сервировки":slide===3?"Детали интерьера":"Предметы из коллекций"}</h2></div><button onClick={()=>go(current.destination)}>СМОТРЕТЬ ВСЕ →</button></div><div className="product-row" key={`featured-${slide}`}>{featuredProducts.map(p=><ProductCard key={`${slide}-${p.id}`} product={p} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(p.id)}/>)}</div></section>

    <section className="manifest"><p>КУЛЬТУРА ДОМА</p><h2>Предметы, с которыми остаётся вечное</h2><span>Натуральные материалы, ручная работа и образы русской культуры —<br/>для современного дома и личных семейных историй.</span><button onClick={()=>go("collections")}>УЗНАТЬ О БРЕНДЕ →</button></section>
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

function ProductCard({ product, onClick, onQuick, favorite, liked }: { product:Product; onClick:(p:Product)=>void; onQuick:(p:Product)=>void; favorite:(n:number)=>void; liked:boolean }) {
  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];
  const [colorIndex, setColorIndex] = useState(0);
  const chosen = variants[colorIndex];
  const chosenProduct = { ...product, image: chosen.image, position: chosen.position ?? product.position, selectedColor: chosen.name };
  const discount=discountOf(product);
  return <article className="product-card"><button className={`heart ${liked?"liked":""}`} onClick={()=>favorite(product.id)} aria-label="Добавить в избранное"><Icon name="heart" filled={liked}/></button><button className="product-image" onClick={()=>onClick(chosenProduct)}><img key={chosen.image} src={assetUrl(chosen.image)} alt={`${product.name}, цвет ${chosen.name}`} style={{objectPosition:chosen.position||product.position||"center"}}/>{product.badge&&<span>{product.badge}</span>}</button><div className="product-copy"><button className="product-link" onClick={()=>onClick(chosenProduct)}><strong>{product.name}</strong><small>{chosen.name.toLowerCase()}, {product.note}</small></button><div className="plp-swatches" role="group" aria-label={`Цвет товара ${product.name}`}>{variants.map((variant,i)=><button key={variant.name} className={i===colorIndex?"active":""} style={{background:variant.hex}} onClick={()=>setColorIndex(i)} aria-label={`Выбрать цвет ${variant.name}`} title={variant.name}/>)}</div><span className={`price ${discount?"sale-price":""}`}>{fmt(product.price)} {product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</span></div><button className="quick" onClick={()=>onQuick(chosenProduct)} aria-label={`Добавить в корзину ${product.name}`}><Icon name="bag"/><i><Icon name="plus"/></i></button></article>;
}

function CollectionsView({ openEditorial }: { openEditorial:(editorial:Editorial)=>void }) {
  const [kind,setKind]=useState("ВСЕ");
  const visible=editorials.filter(item=>kind==="ВСЕ"||(kind==="КАПСУЛЫ"&&item.kind==="КАПСУЛА")||(kind==="КОЛЛЕКЦИИ"&&item.kind==="КОЛЛЕКЦИЯ"));
  return <div className="collections page"><div className="section-head"><p>EDITORIAL</p><h1>Коллекции и капсулы</h1></div><div className="center-tabs">{["ВСЕ","КАПСУЛЫ","КОЛЛЕКЦИИ"].map(x=><button key={x} className={kind===x?"active":""} onClick={()=>setKind(x)}>{x}</button>)}</div><div className="collection-grid">{visible.map((item)=><article key={item.id}><button onClick={()=>openEditorial(item)}><img src={assetUrl(item.images[1])} alt={item.name}/><div><h2>{item.name}</h2><p>{item.description}</p><span>СМОТРЕТЬ {item.kind==="КАПСУЛА"?"КАПСУЛУ":"КОЛЛЕКЦИЮ"} <Icon name="arrow"/></span></div></button></article>)}</div></div>;
}

function EditorialView({ editorial, buyBundle, selectProduct, favorite, favorites }: { editorial:Editorial; buyBundle:(items:Product[])=>void; selectProduct:(product:Product)=>void; favorite:(id:number)=>void; favorites:number[] }) {
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

function QuantityControl({ quantity, setQuantity, label = "Количество" }: { quantity:number; setQuantity:(quantity:number)=>void; label?:string }) {
  return <div className="quantity-control" aria-label={label}><button onClick={(event)=>{event.stopPropagation();setQuantity(Math.max(1,quantity-1))}} aria-label="Уменьшить количество"><Icon name="minus"/></button><span>{quantity}</span><button onClick={(event)=>{event.stopPropagation();setQuantity(quantity+1)}} aria-label="Увеличить количество"><Icon name="plus"/></button></div>;
}

function ProductSizeRows({sizes,selectedSize,setSelectedSize,quantity,setQuantity,notify}:{sizes:readonly (readonly [string,number])[];selectedSize:string;setSelectedSize:(size:string)=>void;quantity:number;setQuantity:(quantity:number)=>void;notify:(size:string)=>void}){
  return <div className="sizes quantity-sizes">{sizes.map(([name,price],index)=>{const unavailable=index===sizes.length-1;return <div key={name} className={`size-row ${selectedSize===name&&!unavailable?"active":""} ${unavailable?"unavailable":""}`}><button onClick={()=>{if(!unavailable){setSelectedSize(name);setQuantity(1)}}}><span>{name}</span>{selectedSize!==name&&!unavailable&&<b>{fmt(price)}</b>}</button>{unavailable?<div className="stock-actions"><button onClick={()=>document.querySelector(".post-rich-recommendations")?.scrollIntoView({behavior:"smooth"})}>СМОТРЕТЬ ПОХОЖИЕ</button><button onClick={()=>notify(name)} aria-label={`Сообщить о поступлении размера ${name}`}><Icon name="mail"/></button></div>:selectedSize===name?<QuantityControl quantity={quantity} setQuantity={setQuantity}/>:null}</div>})}</div>;
}

function ProductView({ product, favorite, liked, chooseSize, add, buyBundle, selectProduct }: { product:Product; favorite:(n:number)=>void; liked:boolean; chooseSize:()=>void; add:(p:Product)=>void; buyBundle:(items:Product[])=>void; selectProduct:(p:Product)=>void }) {
  const [open,setOpen]=useState("");
  const [storesOpen,setStoresOpen]=useState(false);
  const [colorIndex,setColorIndex]=useState(0);
  const [activeImage,setActiveImage]=useState(0);
  const [selectedSize,setSelectedSize]=useState("Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const [bundleSelecting,setBundleSelecting]=useState(false);
  const variants=product.colorVariants??[{name:"Молочный",hex:"#eee",image:product.image}];
  useEffect(()=>{const initial=variants.findIndex(variant=>variant.name===product.selectedColor);setColorIndex(initial>=0?initial:0);setActiveImage(0);setSelectedSize("Евро 200×220");setQuantity(1)},[product.id,product.selectedColor]);
  const color=variants[colorIndex];
  const gallery=product.hasRichContent?[color.image]:(product.gallery??[color.image,...variants.map(x=>x.image)]).filter((x,i,a)=>a.indexOf(x)===i);
  const image=gallery[activeImage]??color.image;
  const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
  const unitPrice=sizes.find(([name])=>name===selectedSize)?.[1]??product.price;
  const selectedProduct={...product,price:unitPrice,image,selectedColor:color.name,selectedSize,quantity};
  const bundleExtras=products.filter(item=>item.id!==product.id).slice(0,2);
  const bundleItems=[selectedProduct,...bundleExtras];
  const [bundleSelectedIds,setBundleSelectedIds]=useState<number[]>(bundleItems.map(item=>item.id));
  useEffect(()=>{setBundleSelecting(false);setBundleSelectedIds(bundleItems.map(item=>item.id))},[product.id]);
  const selectedBundleItems=bundleItems.filter(item=>bundleSelectedIds.includes(item.id));
  const bundleTotal=selectedBundleItems.reduce((sum,item)=>sum+item.price*(item.quantity??1),0);
  const handlePurchase=()=>window.matchMedia("(max-width: 900px)").matches?chooseSize():add(selectedProduct);
  const toggleBundleItem=(id:number)=>setBundleSelectedIds(current=>current.includes(id)?current.filter(itemId=>itemId!==id):[...current,id]);
  const handleBundle=()=>{if(!bundleSelecting){setBundleSelecting(true);return}if(selectedBundleItems.length)buyBundle(selectedBundleItems)};
  return <div className={`product-page page ${product.hasRichContent?"has-rich":"standard-pdp"}`}><div className="crumbs">Главная / Домашний текстиль / {product.name}</div><div className={`pdp-grid ${product.hasRichContent?"without-thumbs":""}`}>{!product.hasRichContent&&<div className="thumbs">{gallery.map((src,n)=><button key={src} className={n===activeImage?"active":""} onClick={()=>setActiveImage(n)} aria-label={`Фото товара ${n+1}`}><img src={assetUrl(src)} alt=""/></button>)}</div>}<div className="pdp-main"><img key={image} src={assetUrl(image)} alt={`${product.name}, ${color.name}`}/></div><div className="pdp-info">{product.badge&&<small className="badge">{product.badge}</small>}<div className="pdp-title"><h1>{product.name}</h1><div><button onClick={()=>favorite(product.id)} aria-label="Добавить в избранное"><Icon name="heart" filled={liked}/></button><button onClick={()=>navigator.clipboard?.writeText(location.href)} aria-label="Поделиться"><Icon name="share"/></button></div></div><div className={`pdp-price ${product.oldPrice?"sale":""}`}><strong>{fmt(unitPrice)}</strong>{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}</div><small className="pdp-code">АРТИКУЛ: KD-PD-{1020+product.id}</small><label>Цвет: {color.name}</label><div className="swatches product-swatches">{variants.map((variant,index)=><button key={variant.name} className={index===colorIndex?"active":""} onClick={()=>{setColorIndex(index);setActiveImage(0)}} style={{background:variant.hex}} aria-label={`Цвет ${variant.name}`}/>)}</div><p className="pdp-description">Предмет создан в традиции русского гостеприимства: благородная палитра, точная отделка и материалы, которые красиво живут в доме годами.</p><label>Размер <button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button></label><ProductSizeRows sizes={sizes} selectedSize={selectedSize} setSelectedSize={setSelectedSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Подписка оформлена. Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary purchase-cta total-cta" onClick={handlePurchase}><span className="purchase-label desktop-label">ДОБАВИТЬ В КОРЗИНУ</span><span className="purchase-label mobile-label">ВЫБЕРИТЕ РАЗМЕР</span><b>{fmt(unitPrice*quantity)}</b></button><button className="pdp-stores-button" onClick={()=>setStoresOpen(true)} aria-label="Показать наличие в бутиках"><span><Icon name="pin"/>НАЛИЧИЕ В МАГАЗИНАХ</span><Icon name="chevron"/></button><div className="pdp-accordions">{[
  {title:"ИНФОРМАЦИЯ О ТОВАРЕ",content:<><p>Натуральные материалы, деликатная отделка и производство с вниманием к деталям.</p><dl><div><dt>Состав</dt><dd>Хлопок / лён</dd></div><div><dt>Уход</dt><dd>Деликатная стирка 30°C</dd></div><div><dt>Производство</dt><dd>Россия</dd></div></dl></>},
  {title:"ДОСТАВКА",content:<><p>Бесплатная доставка при заказе от 15 000 ₽. Доступны курьерская доставка и самовывоз из бутика.</p><small>Срок и доступные способы рассчитываются при оформлении заказа.</small></>},
  {title:"ВОЗВРАТ",content:<><p>Возврат товара надлежащего качества возможен в течение 14 дней при сохранении товарного вида и комплектации.</p><small>Для отдельных категорий могут действовать специальные условия возврата.</small></>}
].map(section=><section className={`pdp-accordion-item ${open===section.title?"open":""}`} key={section.title}><button className="pdp-accordion-trigger" onClick={()=>setOpen(open===section.title?"":section.title)} aria-expanded={open===section.title}><span>{section.title}</span><Icon name="chevron"/></button>{open===section.title&&<div className="pdp-accordion-panel">{section.content}</div>}</section>)}</div>{product.hasBundle&&<section className={`bundle ${bundleSelecting?"selection-mode":""}`}><div className="bundle-heading"><div><p>ГОТОВОЕ РЕШЕНИЕ</p><h3>СОБЕРИТЕ КОМПЛЕКТ</h3>{bundleSelecting&&<span className="selection-caption">Можно убрать лишние предметы</span>}</div><span>{selectedBundleItems.length} из {bundleItems.length}</span></div><div className="bundle-products">{bundleItems.map((item,index)=><article className={bundleSelectedIds.includes(item.id)?"selected":""} key={`${item.id}-${index}`}><div><img src={assetUrl(item.image)} alt={item.name}/>{bundleSelecting?<label className="product-selector compact"><input type="checkbox" checked={bundleSelectedIds.includes(item.id)} onChange={()=>toggleBundleItem(item.id)}/><span><Icon name="plus"/></span></label>:<i>✓</i>}</div><span>{item.name}</span><small>{index===0?`${selectedSize} · ${color.name}`:item.note}</small><b>{fmt(item.price*(item.quantity??1))}</b></article>)}</div><button className="primary bundle-buy total-cta" disabled={bundleSelecting&&!selectedBundleItems.length} onClick={handleBundle}><span>{bundleSelecting?"ДОБАВИТЬ В КОРЗИНУ":"ВЫКУПИТЬ ВЕСЬ КОМПЛЕКТ"}</span><b>{fmt(bundleTotal)}</b></button></section>}</div></div>{product.hasRichContent&&<RichContent product={product}/>}<ProductRecommendations product={product} selectProduct={selectProduct} favorite={favorite}/>{storesOpen&&<BoutiqueMap close={()=>setStoresOpen(false)}/>}</div>;
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

function RichContent({product}:{product:Product}){
  const night=product.id===4;
  return <section className={`rich-content ${night?"night-story":"russian-story"}`}><div className="rich-intro"><p>{night?"КАПСУЛА · НИТИ ВРЕМЕНИ":"КОЛЛЕКЦИЯ · РУССКИЙ УЗОР"}</p><h2>{night?"Тишина, свет и вечные истории":"Вышивка, в которой живёт память"}</h2><span>{night?"Вдохновлена движением звёзд и бесконечной красотой ночного неба.":"Современное прочтение орнаментов, передававшихся из поколения в поколение."}</span></div><img className="rich-wide" src={assetUrl(night?"/images/time-hero.png":"/images/russian-bedroom.png")} alt="История коллекции"/><div className="rich-pair"><img src={assetUrl(night?"/images/night-editorial.png":"/images/poetry-editorial.png")} alt="Детали коллекции"/><div><p>СДЕЛАНО В РОССИИ</p><h3>{night?"Каждая деталь — как напоминание о чём-то важном.":"Натуральные ткани и тонкая ручная работа."}</h3><span>Нежные оттенки, благородные материалы и вышивка, созданная с вниманием к вечному.</span></div></div></section>;
}

function ProductRecommendations({product,selectProduct,favorite}:{product:Product;selectProduct:(product:Product)=>void;favorite:(id:number)=>void}){
  const recommendations=products.filter(item=>item.id!==product.id).slice(0,4);
  return <section className="post-rich-recommendations"><div className="section-head"><p>ПРОДОЛЖИТЬ ВЫБОР</p><h2>Вам может понравиться</h2></div><div>{recommendations.map(item=><ProductCard key={`recommendation-${item.id}`} product={item} onClick={selectProduct} onQuick={selectProduct} favorite={favorite} liked={false}/>)}</div></section>;
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

function Search({ close, choose }: { close:()=>void; choose:(p:Product)=>void }) { const [q,setQ]=useState(""); const result=products.filter(p=>p.name.toLowerCase().includes(q.toLowerCase())); return <div className="overlay"><button className="overlay-bg" onClick={close}/><div className="search-panel"><div><Icon name="search"/><input autoFocus placeholder="Поиск по каталогу" value={q} onChange={e=>setQ(e.target.value)}/><button onClick={close} aria-label="Закрыть поиск"><Icon name="close"/></button></div><p>{q?`Найдено: ${result.length}`:"Популярные запросы: постельное бельё, посуда, подарки"}</p>{q&&<div className="search-results">{result.map(p=><button key={p.id} onClick={()=>choose(p)}><img src={assetUrl(p.image)} alt=""/><span>{p.name}<b>{fmt(p.price)}</b></span></button>)}</div>}</div></div> }

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
  return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel favorites-drawer"><button className="close" onClick={close} aria-label="Закрыть избранное"><Icon name="close"/></button><p>ИЗБРАННОЕ · {items.length}</p>{items.length===0?<div className="empty"><Icon name="heart"/><h2>Сохраните то, что близко</h2><span>Нажимайте на сердце в карточке, чтобы вернуться к предмету позже.</span><button className="primary" onClick={close}>ПРОДОЛЖИТЬ ПОКУПКИ</button></div>:<div className="favorite-list">{items.map(product=><article key={product.id}><button className="favorite-image" onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/></button><div><button className="favorite-title" onClick={()=>choose(product)}>{product.name}</button><span>{product.note}</span><b>{fmt(product.price)}</b><button className="secondary" onClick={()=>quickAdd(product)}>ДОБАВИТЬ</button></div><button className="favorite-remove" onClick={()=>remove(product.id)} aria-label={`Удалить ${product.name} из избранного`}><Icon name="close"/></button></article>)}</div>}</aside></div>;
}

function Filters({ close, apply }: { close:()=>void; apply:()=>void }) { return <div className="overlay"><button className="overlay-bg" onClick={close}/><aside className="side-panel filters"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>ФИЛЬТРЫ</p>{["Категория","Материал","Цвет","Размер","Цена"].map((x,i)=><details key={x} open={i===0}><summary>{x}<Icon name="plus"/></summary><label><input type="checkbox"/> Постельное бельё</label><label><input type="checkbox"/> Домашний текстиль</label><label><input type="checkbox"/> Посуда и сервировка</label></details>)}<button className="primary" onClick={apply}>ПОКАЗАТЬ 24 ТОВАРА</button><button className="link" onClick={()=>location.reload()}>СБРОСИТЬ</button></aside></div> }

function PLPSizeFlow({ product, close, add }: { product:Product; close:()=>void; add:(size:string,quantity:number,unitPrice:number)=>void }) {
  const [chosenSize,setChosenSize]=useState("Евро 200×220");
  const [quantity,setQuantity]=useState(1);
  const [infoOpen,setInfoOpen]=useState(false);
  const sizes=[["Евро 200×220",product.price],["Семейный 150×200",product.price+2000],["Кинг Сайз 220×240",product.price+2000]] as const;
  const unitPrice=sizes.find(([item])=>item===chosenSize)?.[1]??product.price;
  const discount=discountOf(product);
  return <div className="overlay plp-flow"><button className="overlay-bg" onClick={close} aria-label="Закрыть выбор размера"/><section className="plp-modal" role="dialog" aria-modal="true" aria-label={`Добавить ${product.name}`}><div className="flow-handle"/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="plp-modal-media"><img src={assetUrl(product.image)} alt={product.name}/></div><div className="plp-modal-info"><small>{product.badge||"КУЛЬТУРА ДОМА"}</small><h2>{product.name}</h2><p className="modal-note">{product.note}</p><div className="modal-price"><b>{fmt(product.price)}</b>{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</div><p>Цвет: <b>{product.selectedColor ?? product.colorVariants?.[0]?.name}</b></p><p className="quick-description">Предмет создан в русской декоративной традиции: ясная форма, благородный цвет и точная отделка.</p><button className="quick-info-link" onClick={()=>setInfoOpen(true)}>ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ <Icon name="chevron"/></button><div className="sheet-head"><span>Размер и количество</span><button onClick={()=>setInfoOpen(true)}>Размерная сетка</button></div><ProductSizeRows sizes={sizes} selectedSize={chosenSize} setSelectedSize={setChosenSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary total-cta" onClick={()=>add(chosenSize,quantity,unitPrice)}><span>ДОБАВИТЬ В КОРЗИНУ</span><b>{fmt(unitPrice*quantity)}</b></button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></div></section>{infoOpen&&<ProductInfoDrawer product={product} close={()=>setInfoOpen(false)}/>}</div>
}

function ProductInfoDrawer({product,close}:{product:Product;close:()=>void}){
  return <aside className="product-info-drawer" role="dialog" aria-modal="true" aria-label="Информация о товаре"><header><span>ИНФОРМАЦИЯ О ТОВАРЕ</span><button onClick={close} aria-label="Закрыть информацию"><Icon name="close"/></button></header><div><section><h2>РАЗМЕРЫ</h2><dl><div><dt>Высота</dt><dd>0,5 см</dd></div><div><dt>Ширина</dt><dd>{product.id===7?"220":"160"} см</dd></div><div><dt>Длина</dt><dd>{product.id===7?"240":"200"} см</dd></div><div><dt>Вес</dt><dd>1,2 кг</dd></div></dl></section><section><h2>СОСТАВ</h2><h3>ВНЕШНЯЯ ЧАСТЬ</h3><p>100% натуральный хлопок</p><h3>НАПОЛНИТЕЛЬ</h3><p>100% переработанный полиэстер</p></section><section><h2>СЕРТИФИЦИРОВАННЫЕ МАТЕРИАЛЫ</h2><h3>ХЛОПОК, СЕРТИФИЦИРОВАННЫЙ ПО OEKO-TEX®</h3><p>Материал проверен на отсутствие вредных веществ и подходит для ежедневного домашнего использования.</p></section><section><h2>УХОД</h2><ul><li>Деликатная стирка при 30°C</li><li>Не отбеливать</li><li>Гладить при низкой температуре</li><li>Не использовать машинную сушку</li></ul></section><section><h2>ПРОИСХОЖДЕНИЕ</h2><p>Сделано в России</p></section></div></aside>;
}

function PLPAdded({product,close,openCart,selectRecommendation}:{product:CartItem;close:()=>void;openCart:()=>void;selectRecommendation:(product:Product)=>void}){
  const recommendations=products.filter(x=>x.id!==product.id).slice(0,4);
  return <div className="overlay plp-added"><button className="overlay-bg" onClick={close} aria-label="Закрыть"/><section className="plp-added-modal" role="dialog" aria-modal="true" aria-label="Товар добавлен в корзину"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="added-drawer-head"><p className="added-kicker">ДОБАВЛЕНО ТОВАРОВ · {product.quantity}</p><span>КОРЗИНА ОБНОВЛЕНА</span></div><div className="added-product"><img src={assetUrl(product.image)} alt={product.name}/><div><h2>{product.name}</h2><span>{product.selectedColor} · {product.selectedSize}</span><span>Количество: {product.quantity}</span><b>{fmt(product.price*product.quantity)}</b></div></div><div className="added-recommendations"><p>ВАС ТАКЖЕ МОЖЕТ ЗАИНТЕРЕСОВАТЬ</p><div>{recommendations.map(item=><button key={item.id} onClick={()=>selectRecommendation(item)}><img src={assetUrl(item.image)} alt={item.name}/><span>{item.name}</span><small>{item.note}</small><b>{fmt(item.price)}</b></button>)}</div></div><aside><Icon name="bag"/><span>Бесплатная доставка при заказе от 15 000 ₽</span></aside><div className="added-sticky"><button className="primary" onClick={openCart}>ПОСМОТРЕТЬ КОРЗИНУ</button></div></section></div>;
}

function SizeSheet({ size, setSize, close, add, price }: { size:string; setSize:(s:string)=>void; close:()=>void; add:(quantity:number,unitPrice:number)=>void; price:number }) {
  const [quantity,setQuantity]=useState(1);
  const sizes=[["Евро 200×220",price],["Семейный 150×200",price+2000],["Кинг Сайз 220×240",price+2000]] as const;
  const unitPrice=sizes.find(([item])=>item===size)?.[1]??price;
  return <div className="overlay mobile-overlay"><button className="overlay-bg" onClick={close}/><aside className="size-sheet"><i/><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><div className="sheet-head"><span>Размер и количество</span><button onClick={()=>alert("Евро: 200×220 · Семейный: 150×200 · Кинг Сайз: 220×240")}>Размерная сетка</button></div><ProductSizeRows sizes={sizes} selectedSize={size} setSelectedSize={setSize} quantity={quantity} setQuantity={setQuantity} notify={(name)=>alert(`Сообщим, когда размер «${name}» появится в наличии.`)}/><button className="primary total-cta" onClick={()=>add(quantity,unitPrice)}><span>ДОБАВИТЬ В КОРЗИНУ</span><b>{fmt(unitPrice*quantity)}</b></button><button className="stores" onClick={()=>alert("В наличии: Москва, Петровка · Санкт-Петербург, Невский")}><Icon name="pin"/> НАЛИЧИЕ В МАГАЗИНАХ</button></aside></div>
}

function Cart({ cart, recentlyViewed, close, total, remove, update, checkout, go, choose }: { cart:CartItem[]; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void }) {
  const sizeOptions=["Евро 200×220","Семейный 150×200","Кинг Сайз 220×240"];
  return <div className="overlay"><button className="overlay-bg" onClick={close} aria-label="Закрыть корзину"/><aside className="side-panel cart"><button className="close" onClick={close} aria-label="Закрыть"><Icon name="close"/></button><p>{cart.length?`КОРЗИНА · ${cart.reduce((sum,item)=>sum+item.quantity,0)}`:"КОРЗИНА"}</p>{cart.length===0?<>{recentlyViewed.length?<section className="recent-cart"><div><p>НЕДАВНО ПРОСМОТРЕННЫЕ</p><span>Предметы, к которым вы возвращались</span></div><div>{recentlyViewed.map(product=><button key={product.id} onClick={()=>choose(product)}><img src={assetUrl(product.image)} alt={product.name}/><strong>{product.name}</strong><small>{product.note}</small><b>{fmt(product.price)}</b></button>)}</div><button className="secondary" onClick={go}>ПРОДОЛЖИТЬ ПОКУПКИ</button></section>:<div className="empty"><h2>Здесь пока пусто</h2><span>Добавьте предметы, которые сделают дом вашим.</span><button className="primary" onClick={go}>ПЕРЕЙТИ В КАТАЛОГ</button></div>}</>:<><div className="cart-items">{cart.map((p,i)=><article key={`${p.id}-${i}`}><img src={assetUrl(p.image)} alt={`${p.name}, ${p.selectedColor}`}/><div className="cart-item-copy"><strong>{p.name}</strong><span>Цвет: {p.selectedColor}</span><label>Размер<select value={p.selectedSize} onChange={event=>update(i,{selectedSize:event.target.value})}>{sizeOptions.map(option=><option key={option}>{option}</option>)}</select></label><div className="cart-item-bottom"><QuantityControl quantity={p.quantity} setQuantity={quantity=>update(i,{quantity})}/><b>{fmt(p.price*p.quantity)}</b></div></div><button onClick={()=>remove(i)} aria-label="Удалить товар"><Icon name="close"/></button></article>)}</div><p className="recommend-title">ВАМ МОЖЕТ ПОНРАВИТЬСЯ</p><div className="cart-recs">{products.slice(2,4).map(p=><article key={p.id}><img src={assetUrl(p.image)} alt=""/><span>{p.name}</span><b>{fmt(p.price)}</b></article>)}</div><div className="delivery">{total>=15000?"Бесплатная доставка включена":`До бесплатной доставки ${fmt(15000-total)}`}</div><div className="cart-total"><span>ИТОГО</span><b>{fmt(total)}</b></div><button className="primary checkout-cta" onClick={checkout}>ОФОРМИТЬ ЗАКАЗ</button></>}</aside></div>;
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
  return <div className="checkout-overlay" role="dialog" aria-modal="true" aria-label="Оформление заказа"><header><button onClick={close} aria-label="Закрыть оформление"><Icon name="close"/></button><b>КУЛЬТУРА ДОМА</b><span>БЕЗОПАСНОЕ ОФОРМЛЕНИЕ</span></header><form onSubmit={handleSubmit}><div className="checkout-main"><div className="checkout-heading"><p>ОФОРМЛЕНИЕ ЗАКАЗА</p><h1>Ваш заказ</h1></div><section className="checkout-section"><div className="checkout-step"><i>1</i><h2>Контактные данные</h2></div><div className="checkout-fields"><label>Имя<input value={form.name} onChange={setField("name")} name="name" autoComplete="given-name" required/></label><label>Фамилия<input value={form.surname} onChange={setField("surname")} name="surname" autoComplete="family-name" required/></label><label>Email<input value={form.email} onChange={setField("email")} type="email" name="email" autoComplete="email" required/></label><label>Телефон<input value={form.phone} onChange={setField("phone")} type="tel" name="phone" autoComplete="tel" placeholder="+7 999 000-00-00" required/></label></div></section><section className="checkout-section"><div className="checkout-step"><i>2</i><h2>Способ получения</h2></div><div className="checkout-options"><label className={delivery==="courier"?"active":""}><input type="radio" name="delivery" checked={delivery==="courier"} onChange={()=>setDelivery("courier")}/><span><b>Курьерская доставка</b><small>{total>=15000?"Бесплатно":"690 ₽"} · 1–3 дня</small></span></label><label className={delivery==="pickup"?"active":""}><input type="radio" name="delivery" checked={delivery==="pickup"} onChange={()=>setDelivery("pickup")}/><span><b>Самовывоз из бутика</b><small>Бесплатно · сегодня</small></span></label></div>{delivery==="courier"&&<div className="checkout-address"><label>Город<input value={form.city} onChange={setField("city")} name="city" required/></label><label>Улица и дом<input value={form.address} onChange={setField("address")} name="address" required/></label><label>Квартира<input name="flat"/></label><label>Комментарий курьеру<input name="comment"/></label></div>}<CheckoutMap points={points} selected={mapPoint} choose={(point)=>{setMapPoint(point);if(delivery==="courier")setForm({...form,address:point})}} mode={delivery}/></section><section className="checkout-section"><div className="checkout-step"><i>3</i><h2>Оплата</h2></div><div className="checkout-options"><label className={payment==="card"?"active":""}><input type="radio" name="payment" checked={payment==="card"} onChange={()=>setPayment("card")}/><span><b>Банковской картой онлайн</b><small>МИР · Visa · Mastercard</small></span></label><label className={payment==="upon"?"active":""}><input type="radio" name="payment" checked={payment==="upon"} onChange={()=>setPayment("upon")}/><span><b>При получении</b><small>Картой или наличными</small></span></label></div></section></div><aside className="checkout-summary"><div className="summary-title"><h2>Состав заказа</h2><button type="button" onClick={editCart}>ИЗМЕНИТЬ</button></div><div className="summary-items">{cart.map((item,index)=><article key={`${item.id}-${index}`}><img src={assetUrl(item.image)} alt={item.name}/><div><strong>{item.name}</strong><span>{item.selectedColor} · {item.selectedSize}</span><span>Количество: {item.quantity}</span><b>{fmt(item.price*item.quantity)}</b></div></article>)}</div><dl><div><dt>Товары</dt><dd>{fmt(total)}</dd></div><div><dt>Получение</dt><dd>{delivery==="pickup"?`Бутик: ${mapPoint}`:mapPoint}</dd></div><div><dt>Доставка</dt><dd>{deliveryPrice?fmt(deliveryPrice):"Бесплатно"}</dd></div><div className="summary-total"><dt>Итого</dt><dd>{fmt(finalTotal)}</dd></div></dl><label className="checkout-consent"><input type="checkbox" checked={agreed} onChange={event=>setAgreed(event.target.checked)}/><span>Я согласен с условиями продажи и политикой конфиденциальности</span></label><button className="primary" type="submit">ПОДТВЕРДИТЬ ЗАКАЗ · {fmt(finalTotal)}</button><small className="checkout-security">Данные заказа защищены. Оплата проходит на безопасной странице банка.</small></aside></form></div>;
}

function CheckoutMap({points,selected,choose,mode}:{points:string[];selected:string;choose:(point:string)=>void;mode:"courier"|"pickup"}){
  return <div className="checkout-map"><div className="map-canvas" aria-label="Карта выбора адреса">{points.map((point,index)=><button type="button" key={point} className={`map-pin pin-${index} ${selected===point?"active":""}`} onClick={()=>choose(point)} aria-label={`Выбрать ${point}`}><Icon name="pin"/><span>{index+1}</span></button>)}<i className="river"/><span className="map-label moscow">МОСКВА</span><span className="map-label center">САДОВОЕ КОЛЬЦО</span></div><div className="map-points"><p>{mode==="pickup"?"ВЫБЕРИТЕ БУТИК":"УТОЧНИТЕ ТОЧКУ НА КАРТЕ"}</p>{points.map((point,index)=><button type="button" key={point} className={selected===point?"active":""} onClick={()=>choose(point)}><b>{index+1}</b><span>{point}<small>{mode==="pickup"?"Сегодня до 22:00":"Курьерская доставка"}</small></span></button>)}</div></div>;
}

function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) { return <footer><div className="footer-brand"><div className="logo">КУЛЬТУРА ДОМА</div><p>Подпишитесь на письма о новых коллекциях</p><div><input placeholder="Ваш email"/><button onClick={()=>notice("Спасибо за подписку")}>→</button></div></div><div><p>ПОКУПАТЕЛЯМ</p><button onClick={()=>go("catalog")}>Каталог</button><button onClick={()=>alert("Доставка по России от 1 дня")}>Доставка и оплата</button><button onClick={()=>alert("Возврат в течение 14 дней")}>Возврат</button></div><div><p>О БРЕНДЕ</p><button onClick={()=>go("collections")}>Коллекции</button><button onClick={()=>alert("Русский бренд предметов для дома")}>Наша история</button><button onClick={()=>alert("Москва · Санкт-Петербург · Казань")}>Бутики</button></div><div><p>СВЯЗАТЬСЯ</p><a href="tel:+78005553535">8 800 555-35-35</a><a href="mailto:hello@kultura-doma.ru">hello@kultura-doma.ru</a></div><small>© 2026 Культура дома &nbsp; · &nbsp; Политика конфиденциальности</small></footer> }
