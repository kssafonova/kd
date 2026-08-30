from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"
TRUTH = ROOT / "app" / "truth-commerce-enhancer.tsx"
CONSTRUCTOR = ROOT / "app" / "constructor" / "data-client.ts"
SITE_DB = ROOT / "app" / "site-database.ts"

SITE_DB_SOURCE = r'''"use client";

import { useEffect, useState } from "react";

export type SiteDatabaseRow = Record<string, string>;
export type SiteDatabase = {
  version: string;
  source: string;
  tableCount: number;
  tables: Record<string, SiteDatabaseRow[]>;
  catalogRows: SiteDatabaseRow[];
  variantCount: number;
  productCount: number;
  products: Array<Record<string, unknown>>;
  collections: Array<Record<string, unknown>>;
  capsules: Array<Record<string, unknown>>;
  readySolutions: Array<Record<string, unknown>>;
};

const BASE = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
let cache: SiteDatabase | null = null;
let pending: Promise<SiteDatabase> | null = null;

export const siteDatabaseUrl = () => `${BASE}/data/database/site_runtime.json`;

export function loadSiteDatabase(): Promise<SiteDatabase> {
  if (cache) return Promise.resolve(cache);
  if (!pending) {
    pending = fetch(siteDatabaseUrl(), { cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error(`Не удалось загрузить базу данных сайта: ${response.status}`);
        return response.json() as Promise<SiteDatabase>;
      })
      .then((data) => {
        cache = data;
        return data;
      })
      .catch((error) => {
        pending = null;
        throw error;
      });
  }
  return pending;
}

export function useSiteDatabase() {
  const [data, setData] = useState<SiteDatabase | null>(cache);
  useEffect(() => {
    let active = true;
    loadSiteDatabase().then((next) => { if (active) setData(next); }).catch(() => {});
    return () => { active = false; };
  }, []);
  return data;
}

export function siteTable(data: SiteDatabase | null, name: string): SiteDatabaseRow[] {
  return data?.tables?.[name] ?? [];
}
'''
SITE_DB.write_text(SITE_DB_SOURCE, encoding="utf-8")

# Truth-commerce pages: use the normalized CSV runtime instead of the legacy XLSX blob.
truth = TRUTH.read_text(encoding="utf-8")
if 'from "./site-database"' not in truth:
    truth = truth.replace('import { useEffect, useMemo, useState } from "react";\n', 'import { useEffect, useMemo, useState } from "react";\nimport { useSiteDatabase } from "./site-database";\n', 1)
truth, truth_count = re.subn(
    r'function useTruth\(\)\{const\[d,setD\]=useState<D\|null>\(null\);useEffect\(\(\)=>\{.*?;return d\}',
    'function useTruth(){return useSiteDatabase() as unknown as D|null}',
    truth,
    count=1,
    flags=re.S,
)
if truth_count == 0 and 'function useTruth(){return useSiteDatabase() as unknown as D|null}' not in truth:
    raise SystemExit("SITE_DATABASE_RUNTIME_V128: truth useTruth signature not found")
truth = truth.replace("КАТАЛОГ · XLSX TRUTH", "КАТАЛОГ · БАЗА ДАННЫХ")
truth = truth.replace("ГОТОВЫЕ РЕШЕНИЯ · XLSX TRUTH", "ГОТОВЫЕ РЕШЕНИЯ · БАЗА ДАННЫХ")
truth = truth.replace("синхронизированы с XLSX", "синхронизированы с базой данных")
TRUTH.write_text(truth, encoding="utf-8")

# Constructor: its product catalog now comes from the same normalized runtime.
constructor = CONSTRUCTOR.read_text(encoding="utf-8")
constructor_pattern = r'async function loadTruthData\(\): Promise<TruthData> \{.*?\n\}\n\nasync function loadTruthCatalog'
constructor_replacement = '''async function loadTruthData(): Promise<TruthData> {
  const response = await fetch(constructorDataUrl("database/site_runtime.json"), { cache: "no-store" });
  if (!response.ok) throw new Error(`Не удалось загрузить базу данных сайта: ${response.status}`);
  return response.json() as Promise<TruthData>;
}

async function loadTruthCatalog'''
constructor, constructor_count = re.subn(constructor_pattern, constructor_replacement, constructor, count=1, flags=re.S)
if constructor_count == 0 and 'constructorDataUrl("database/site_runtime.json")' not in constructor:
    raise SystemExit("SITE_DATABASE_RUNTIME_V128: constructor truth loader signature not found")
CONSTRUCTOR.write_text(constructor, encoding="utf-8")

page = PAGE.read_text(encoding="utf-8")
if "// SITE_DATABASE_RUNTIME_V128" not in page:
    if 'from "./site-database"' not in page:
        page = page.replace('import { catalogProductOverrides, type CatalogSku } from "./catalog-data";\n', 'import { catalogProductOverrides, type CatalogSku } from "./catalog-data";\nimport { loadSiteDatabase, useSiteDatabase } from "./site-database";\n', 1)
    page = page.replace("// CATALOG_SKU_MODEL_V1", "// CATALOG_SKU_MODEL_V1\n// SITE_DATABASE_RUNTIME_V128", 1)

    old_loader = '''  const chunks=await Promise.all(CATALOG_MASTER_FILES.map(async fileName=>{
    try{const response=await fetch(`${base}/data/${fileName}`,{cache:"no-store"});if(!response.ok)return [];return parseEntityCsv(await response.text())}catch{return []}
  }));'''
    new_loader = '''  const runtime=await loadSiteDatabase().catch(()=>null);
  const runtimeRows=(runtime?.catalogRows??[]) as CatalogMasterRow[];
  const chunks=runtimeRows.length?[runtimeRows]:await Promise.all(CATALOG_MASTER_FILES.map(async fileName=>{
    try{const response=await fetch(`${base}/data/${fileName}`,{cache:"no-store"});if(!response.ok)return [];return parseEntityCsv(await response.text())}catch{return []}
  }));'''
    if old_loader not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: catalog loader signature not found")
    page = page.replace(old_loader, new_loader, 1)

    old_city = '''function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const query=value.trim().toLowerCase();
  const items=KD_CITY_SUGGESTIONS.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);'''
    new_city = '''function CitySuggestField({value,onChange,label="Город",required=false}:{value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const db=useSiteDatabase();
  const dbCities=(db?.tables?.["regions"]??[]).filter(row=>row.is_active!=="false").map(row=>row.city).filter(Boolean);
  const citySource=dbCities.length?dbCities:KD_CITY_SUGGESTIONS;
  const query=value.trim().toLowerCase();
  const items=citySource.filter(city=>!query||city.toLowerCase().includes(query)).slice(0,6);'''
    if old_city not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: city field signature not found")
    page = page.replace(old_city, new_city, 1)

    old_address = '''function AddressSuggestField({city,value,onChange,label="Улица и дом",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const source=KD_ADDRESS_SUGGESTIONS[city]??[];'''
    new_address = '''function AddressSuggestField({city,value,onChange,label="Улица и дом",required=false}:{city:string;value:string;onChange:(value:string)=>void;label?:string;required?:boolean}){
  const [open,setOpen]=useState(false);
  const db=useSiteDatabase();
  const dbSource=(db?.tables?.["address_suggestions"]??[]).filter(row=>row.city===city).sort((a,b)=>Number(a.sort_order||0)-Number(b.sort_order||0)).map(row=>row.address).filter(Boolean);
  const source=dbSource.length?dbSource:(KD_ADDRESS_SUGGESTIONS[city]??[]);'''
    if old_address not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: address field signature not found")
    page = page.replace(old_address, new_address, 1)

    old_cart = '''function Cart({ cart, profile, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; profile:Profile|null; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const courierShipping=total>=15000?0:300;
  const courierTotal=total+courierShipping;
  const deliveryLeft=Math.max(0,15000-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/15000*100));'''
    new_cart = '''function Cart({ cart, profile, recentlyViewed, close, total, remove, update, checkout, go, choose, quickAdd }: { cart:CartItem[]; profile:Profile|null; recentlyViewed:Product[]; close:()=>void; total:number; remove:(i:number)=>void; update:(index:number,patch:Partial<CartItem>)=>void; checkout:()=>void; go:()=>void; choose:(product:Product)=>void; quickAdd:(product:Product)=>void }) {
  const db=useSiteDatabase();
  const courierConfig=(db?.tables?.["delivery_methods"]??[]).find(row=>row.delivery_method_id==="courier");
  const courierFee=Number(courierConfig?.base_fee_rub||300);
  const freeThreshold=Number(courierConfig?.free_from_rub||15000);
  const recentItems=recentlyViewed.slice(0,6);
  const itemCount=cart.reduce((sum,item)=>sum+item.quantity,0);
  const courierShipping=total>=freeThreshold?0:courierFee;
  const courierTotal=total+courierShipping;
  const deliveryLeft=Math.max(0,freeThreshold-total);
  const deliveryProgress=Math.min(100,Math.max(0,total/Math.max(1,freeThreshold)*100));'''
    if old_cart not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: cart signature not found")
    page = page.replace(old_cart, new_cart, 1)
    page = page.replace('<span>{courierShipping===0?"Для курьера и ПВЗ":"Курьер — 300 ₽ · ПВЗ — бесплатно"}</span>', '<span>{courierShipping===0?"Для курьера и ПВЗ":`Курьер — ${fmt(courierFee)} · ПВЗ — бесплатно`}</span>', 1)

    old_checkout_hook = '''  const [pickupPoint,setPickupPoint]=useState("");
  const [storePoint,setStorePoint]=useState("");
  const [pvzQuery,setPvzQuery]=useState("");

  const storePoints:Record<string,string[]>={'''
    new_checkout_hook = '''  const [pickupPoint,setPickupPoint]=useState("");
  const [storePoint,setStorePoint]=useState("");
  const [pvzQuery,setPvzQuery]=useState("");
  const db=useSiteDatabase();
  const deliveryConfigs=db?.tables?.["delivery_methods"]??[];
  const paymentConfigs=db?.tables?.["payment_methods"]??[];
  const pickupConfigs=db?.tables?.["pickup_points"]??[];
  const courierConfig=deliveryConfigs.find(row=>row.delivery_method_id==="courier");
  const storeConfig=deliveryConfigs.find(row=>row.delivery_method_id==="store");
  const pvzConfig=deliveryConfigs.find(row=>row.delivery_method_id==="pvz");
  const onlineConfig=paymentConfigs.find(row=>row.payment_method_id==="online");
  const uponConfig=paymentConfigs.find(row=>row.payment_method_id==="upon");

  const storePoints:Record<string,string[]>={'''
    if old_checkout_hook not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: checkout hook signature not found")
    page = page.replace(old_checkout_hook, new_checkout_hook, 1)

    old_points = '''  const pvz=KD_PVZ_POINTS[form.city]??[];
  const stores=storePoints[form.city]??[];'''
    new_points = '''  const dbPvz=pickupConfigs.filter(row=>row.city===form.city&&row.point_type==="pvz").sort((a,b)=>Number(a.sort_order||0)-Number(b.sort_order||0)).map(row=>row.point_name||row.address).filter(Boolean);
  const dbStores=pickupConfigs.filter(row=>row.city===form.city&&row.point_type==="store").sort((a,b)=>Number(a.sort_order||0)-Number(b.sort_order||0)).map(row=>row.point_name||row.address).filter(Boolean);
  const pvz=dbPvz.length?dbPvz:(KD_PVZ_POINTS[form.city]??[]);
  const stores=dbStores.length?dbStores:(storePoints[form.city]??[]);'''
    if old_points not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: checkout points signature not found")
    page = page.replace(old_points, new_points, 1)

    old_pricing = '''  const onlineDiscount=payment==="online"?Math.round(total*.03):0;
  const shipping=delivery==="courier"?(total>=15000?0:300):0;'''
    new_pricing = '''  const onlineDiscountPercent=Number(onlineConfig?.discount_percent||3);
  const onlineDiscount=payment==="online"?Math.round(total*(onlineDiscountPercent/100)):0;
  const courierFee=Number(courierConfig?.base_fee_rub||300);
  const courierFreeFrom=Number(courierConfig?.free_from_rub||15000);
  const shipping=delivery==="courier"?(total>=courierFreeFrom?0:courierFee):Number((delivery==="store"?storeConfig:pvzConfig)?.base_fee_rub||0);'''
    if old_pricing not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: checkout pricing signature not found")
    page = page.replace(old_pricing, new_pricing, 1)

    old_delivery_ui = '''            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>chooseDelivery("courier")}><span>▱</span><b>Курьером</b><small>2–3 дня · {shipping===0?"0 ₽":"300 ₽"}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>chooseDelivery("store")}><span>⌂</span><b>Самовывоз</b><small>2–3 дня · 0 ₽</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>chooseDelivery("pvz")}><span>▦</span><b>ПВЗ</b><small>2–3 дня · 0 ₽</small></button>'''
    new_delivery_ui = '''            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>chooseDelivery("courier")}><span>▱</span><b>{courierConfig?.name||"Курьером"}</b><small>{courierConfig?.min_days||2}–{courierConfig?.max_days||3} дня · {shipping===0?"0 ₽":fmt(courierFee)}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>chooseDelivery("store")}><span>⌂</span><b>{storeConfig?.name||"Самовывоз"}</b><small>{storeConfig?.min_days||2}–{storeConfig?.max_days||3} дня · {Number(storeConfig?.base_fee_rub||0)===0?"0 ₽":fmt(Number(storeConfig?.base_fee_rub||0))}</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>chooseDelivery("pvz")}><span>▦</span><b>{pvzConfig?.name||"ПВЗ"}</b><small>{pvzConfig?.min_days||2}–{pvzConfig?.max_days||3} дня · {Number(pvzConfig?.base_fee_rub||0)===0?"0 ₽":fmt(Number(pvzConfig?.base_fee_rub||0))}</small></button>'''
    if old_delivery_ui not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: checkout delivery UI signature not found")
    page = page.replace(old_delivery_ui, new_delivery_ui, 1)

    old_payment_ui = '''          <div className="checkout-v69-payments"><button type="button" className={payment==="online"?"active":""} onClick={()=>setPayment("online")}><i/><span><b>Онлайн — картой / СБП <mark>−3%</mark></b><small>−3% при оплате сейчас</small></span></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><span><b>При получении</b><small>Картой или наличными</small></span></button></div>'''
    new_payment_ui = '''          <div className="checkout-v69-payments"><button type="button" className={payment==="online"?"active":""} onClick={()=>setPayment("online")}><i/><span><b>{onlineConfig?.name||"Онлайн — картой / СБП"}{onlineDiscountPercent>0&&<mark>−{onlineDiscountPercent}%</mark>}</b><small>{onlineDiscountPercent>0?`−${onlineDiscountPercent}% при оплате сейчас`:"Оплата онлайн"}</small></span></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><span><b>{uponConfig?.name||"При получении"}</b><small>{(uponConfig?.instruments||"bank_card|cash").includes("cash")?"Картой или наличными":"Картой"}</small></span></button></div>'''
    if old_payment_ui not in page:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: checkout payment UI signature not found")
    page = page.replace(old_payment_ui, new_payment_ui, 1)

    footer_pattern = r'function Footer\(\{ go, notice \}: \{ go:\(v:View\)=>void; notice:\(s:string\)=>void \}\) \{ return <footer>.*?</footer> \}'
    footer_replacement = '''function Footer({ go, notice }: { go:(v:View)=>void; notice:(s:string)=>void }) {
  const db=useSiteDatabase();
  const contacts=db?.tables?.["site_contacts"]??[];
  const policies=db?.tables?.["site_policies"]??[];
  const stores=db?.tables?.["stores"]??[];
  const supportPhone=contacts.find(row=>row.contact_id==="support_phone")?.value||"+78005553535";
  const supportEmail=contacts.find(row=>row.contact_id==="support_email")?.value||"hello@kultura-doma.ru";
  const returnDays=policies.find(row=>row.policy_id==="return_period_days")?.value||"14";
  const deliveryMinDays=policies.find(row=>row.policy_id==="delivery_min_days")?.value||"1";
  const boutiqueCities=Array.from(new Set(stores.filter(row=>row.is_active!=="false").map(row=>row.city).filter(Boolean)));
  return <footer><div className="footer-brand"><div className="logo">КУЛЬТУРА ДОМА</div><p>Подпишитесь на письма о новых коллекциях</p><div><input placeholder="Ваш email"/><button onClick={()=>notice("Спасибо за подписку")}>→</button></div></div><div><p>ПОКУПАТЕЛЯМ</p><button onClick={()=>go("catalog")}>Каталог</button><button onClick={()=>alert(`Доставка по России от ${deliveryMinDays} дня`)}>Доставка и оплата</button><button onClick={()=>alert(`Возврат в течение ${returnDays} дней`)}>Возврат</button></div><div><p>О БРЕНДЕ</p><button onClick={()=>go("collections")}>Коллекции</button><button onClick={()=>alert("Русский бренд предметов для дома")}>Наша история</button><button onClick={()=>alert((boutiqueCities.length?boutiqueCities:["Москва","Санкт-Петербург","Казань"]).join(" · "))}>Бутики</button></div><div><p>СВЯЗАТЬСЯ</p><a href={`tel:${supportPhone}`}>{supportPhone}</a><a href={`mailto:${supportEmail}`}>{supportEmail}</a></div><small>© 2026 Культура дома &nbsp; · &nbsp; Политика конфиденциальности</small></footer>;
}'''
    page, footer_count = re.subn(footer_pattern, footer_replacement, page, count=1, flags=re.S)
    if footer_count != 1:
        raise SystemExit("SITE_DATABASE_RUNTIME_V128: footer signature not found")

PAGE.write_text(page, encoding="utf-8")
print("// SITE_DATABASE_RUNTIME_V128: normalized CSV database connected to catalog, checkout, geography, footer, truth commerce and constructor")
