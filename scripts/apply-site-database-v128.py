from __future__ import annotations

from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "public" / "data" / "database"
PAGE = ROOT / "app" / "page.tsx"
GENERATED = ROOT / "app" / "site-database.generated.ts"


def read_csv(name: str) -> list[dict[str, str]]:
    path = DB / name
    if not path.exists():
        raise SystemExit(f"SITE_DATABASE_CONNECTED_V128: missing {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(fh, delimiter=";")]


def as_number(value: str) -> int | float:
    text = (value or "").strip().replace(",", ".")
    if not text:
        return 0
    try:
        number = float(text)
        return int(number) if number.is_integer() else number
    except ValueError:
        return 0


def truth(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "да"}


payments = [
    {
        "id": r["payment_method_id"],
        "name": r["name"],
        "timing": r["timing"],
        "instruments": [x for x in r["instruments"].split("|") if x],
        "discountPercent": as_number(r["discount_percent"]),
        "currency": r["currency"],
        "active": truth(r["is_active"]),
        "sortOrder": as_number(r["sort_order"]),
    }
    for r in read_csv("23_payment_methods.csv") if truth(r["is_active"])
]
payments.sort(key=lambda x: x["sortOrder"])

deliveries = [
    {
        "id": r["delivery_method_id"],
        "name": r["name"],
        "minDays": as_number(r["min_days"]),
        "maxDays": as_number(r["max_days"]),
        "baseFeeRub": as_number(r["base_fee_rub"]),
        "freeFromRub": as_number(r["free_from_rub"]),
        "currency": r["currency"],
        "destinationType": r["destination_type"],
        "active": truth(r["is_active"]),
        "sortOrder": as_number(r["sort_order"]),
    }
    for r in read_csv("24_delivery_methods.csv") if truth(r["is_active"])
]
deliveries.sort(key=lambda x: x["sortOrder"])

regions = read_csv("26_regions.csv")
regions.sort(key=lambda r: as_number(r["sort_order"]))
cities = [r["city"] for r in regions if r["city"]]

addresses: dict[str, list[str]] = {}
for row in sorted(read_csv("27_address_suggestions.csv"), key=lambda r: (r["city"], as_number(r["sort_order"]))):
    addresses.setdefault(row["city"], []).append(row["address"])

pvz: dict[str, list[str]] = {}
store_points: dict[str, list[str]] = {}
for row in sorted(read_csv("28_pickup_points.csv"), key=lambda r: (r["city"], as_number(r["sort_order"]))):
    target = store_points if row["point_type"] == "store" else pvz if row["point_type"] == "pvz" else None
    if target is not None:
        target.setdefault(row["city"], []).append(row["point_name"] or row["address"])

stores = [
    {
        "id": r["store_id"],
        "city": r["city"],
        "address": r["address"],
        "hours": r["hours"],
        "lat": float(r["latitude"] or 0),
        "lon": float(r["longitude"] or 0),
    }
    for r in read_csv("29_stores.csv") if truth(r["is_active"])
]

contacts = {r["contact_id"]: r["value"] for r in read_csv("30_site_contacts.csv") if truth(r["is_active"])}
policies = {r["policy_id"]: r["value"] for r in read_csv("31_site_policies.csv") if truth(r["is_active"])}

# These tables are also exported into the generated module so the whole commerce
# schema is represented in one source-connected layer, not only checkout config.
ready_solutions = read_csv("18_ready_solutions.csv")
collections = read_csv("14_collections.csv")
capsules = read_csv("16_capsules.csv")
categories = read_csv("12_categories.csv")
subcategories = read_csv("13_subcategories.csv")
sizes = read_csv("04_sizes.csv")
colors = read_csv("06_colors.csv")
materials = read_csv("10_materials.csv")


def js(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


generated = f'''/* SITE_DATABASE_GENERATED_V128
   Generated from public/data/database/*.csv by scripts/apply-site-database-v128.py.
   Do not hand-edit this file; edit the CSV source/export pipeline instead. */

export type SiteDatabaseRow = Record<string,string>;

export const SITE_DB_PAYMENT_METHODS = {js(payments)} as const;
export const SITE_DB_DELIVERY_METHODS = {js(deliveries)} as const;
export const SITE_DB_CITIES = {js(cities)} as string[];
export const SITE_DB_ADDRESS_SUGGESTIONS = {js(addresses)} as Record<string,string[]>;
export const SITE_DB_PVZ_POINTS = {js(pvz)} as Record<string,string[]>;
export const SITE_DB_STORE_POINTS = {js(store_points)} as Record<string,string[]>;
export const SITE_DB_STORES = {js(stores)} as Array<{{id:string;city:string;address:string;hours:string;lat:number;lon:number}}>;
export const SITE_DB_CONTACTS = {js(contacts)} as Record<string,string>;
export const SITE_DB_POLICIES = {js(policies)} as Record<string,string>;
export const SITE_DB_READY_SOLUTIONS = {js(ready_solutions)} as SiteDatabaseRow[];
export const SITE_DB_COLLECTIONS = {js(collections)} as SiteDatabaseRow[];
export const SITE_DB_CAPSULES = {js(capsules)} as SiteDatabaseRow[];
export const SITE_DB_CATEGORIES = {js(categories)} as SiteDatabaseRow[];
export const SITE_DB_SUBCATEGORIES = {js(subcategories)} as SiteDatabaseRow[];
export const SITE_DB_SIZES = {js(sizes)} as SiteDatabaseRow[];
export const SITE_DB_COLORS = {js(colors)} as SiteDatabaseRow[];
export const SITE_DB_MATERIALS = {js(materials)} as SiteDatabaseRow[];

const parseSiteDbCsv=(source:string):SiteDatabaseRow[]=>{{
  const text=source.replace(/^\\uFEFF/,"");
  const rows:string[][]=[];let row:string[]=[];let cell="";let quoted=false;
  for(let i=0;i<text.length;i++){{
    const ch=text[i];
    if(ch==='"'){{if(quoted&&text[i+1]==='"'){{cell+='"';i++}}else quoted=!quoted}}
    else if(ch===';'&&!quoted){{row.push(cell);cell=""}}
    else if((ch==='\\n'||ch==='\\r')&&!quoted){{
      if(ch==='\\r'&&text[i+1]==='\\n')i++;
      row.push(cell);cell="";if(row.some(value=>value!==""))rows.push(row);row=[];
    }}else cell+=ch;
  }}
  if(cell||row.length){{row.push(cell);if(row.some(value=>value!==""))rows.push(row)}}
  const headers=(rows.shift()??[]).map(value=>value.trim());
  return rows.map(values=>Object.fromEntries(headers.map((key,index)=>[key,(values[index]??"").trim()])) as SiteDatabaseRow);
}};

const fetchSiteDbTable=async(base:string,fileName:string)=>{{
  try{{const response=await fetch(`${{base}}/data/database/${{fileName}}`,{{cache:"no-store"}});if(!response.ok)return [] as SiteDatabaseRow[];return parseSiteDbCsv(await response.text())}}catch{{return [] as SiteDatabaseRow[]}}
}};

export async function loadSiteDatabaseCatalogRows(base=""):Promise<SiteDatabaseRow[]> {{
  const [products,variants,solutions,links]=await Promise.all([
    fetchSiteDbTable(base,"01_products.csv"),
    fetchSiteDbTable(base,"02_product_variants.csv"),
    fetchSiteDbTable(base,"18_ready_solutions.csv"),
    fetchSiteDbTable(base,"19_ready_solution_products.csv"),
  ]);
  if(!products.length||!variants.length)return [];
  const productMap=new Map(products.map(row=>[row.product_id,row]));
  const solutionMap=new Map(solutions.map(row=>[row.solution_id,row]));
  const required=new Map<string,string[]>(),optional=new Map<string,string[]>(),descriptions=new Map<string,string>();
  links.forEach(link=>{{
    const target=link.relation_type==="optional"?optional:required;
    const list=target.get(link.product_id)??[];if(link.solution_name&&!list.includes(link.solution_name))list.push(link.solution_name);target.set(link.product_id,list);
    const desc=solutionMap.get(link.solution_id)?.description;if(desc&&!descriptions.has(link.product_id))descriptions.set(link.product_id,desc);
  }});
  return variants.map(variant=>{{
    const product=productMap.get(variant.product_id)??{{}};
    return {{
      "Артикул":variant.article||variant.product_id,
      "Название товара":product.name||"",
      "Цвет":variant.color_name||"",
      "Аромат":variant.aroma_name||"",
      "Размер":variant.size_label||"",
      "Цена":variant.price_rub||"",
      "Старая цена":variant.old_price_rub||"",
      "Высота":variant.height||"",
      "Ширина":variant.width||"",
      "Объем":variant.volume||"",
      "Диаметр":variant.diameter||"",
      "Комплектация / информация о размере":variant.package_info||"",
      "Материал":variant.material_name||"",
      "Состав":variant.composition||"",
      "Детали":variant.details||"",
      "Коллекция":variant.collection_name||"",
      "Капсула":variant.capsule_name||"",
      "Категория":variant.category_name||product.category_name||"",
      "Подкатегория":variant.subcategory_name||product.subcategory_name||"",
      "Товар входит в готовое решение":(required.get(variant.product_id)??[]).join("\\n"),
      "Опционально входит в готовое решение":(optional.get(variant.product_id)??[]).join("\\n"),
      "Фото 1":variant.image_1||product.primary_image||"",
      "Фото 2":variant.image_2||"",
      "Фото 3":variant.image_3||"",
      "Описание готового решения":descriptions.get(variant.product_id)||"",
    }};
  }});
}}
'''
GENERATED.write_text(generated, encoding="utf-8")

text = PAGE.read_text(encoding="utf-8")
original = text
marker = "// SITE_DATABASE_CONNECTED_V128"

if marker not in text:
    import_anchor = 'import { catalogProductOverrides, type CatalogSku } from "./catalog-data";'
    import_line = 'import { loadSiteDatabaseCatalogRows, SITE_DB_ADDRESS_SUGGESTIONS, SITE_DB_CITIES, SITE_DB_CONTACTS, SITE_DB_DELIVERY_METHODS, SITE_DB_PAYMENT_METHODS, SITE_DB_POLICIES, SITE_DB_PVZ_POINTS, SITE_DB_STORES, SITE_DB_STORE_POINTS } from "./site-database.generated";'
    if import_anchor not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: catalog-data import anchor not found")
    text = text.replace(import_anchor, import_anchor + "\n" + import_line + "\n" + marker, 1)

    old_rows = '  const rows=chunks.flat().map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as CatalogMasterRow).filter(row=>row["Артикул"]&&row["Название товара"]);'
    new_rows = '  const databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);\n  const sourceRows=databaseRows.length?databaseRows:chunks.flat();\n  const rows=sourceRows.map(row=>Object.fromEntries(Object.entries(row).map(([key,value])=>[key,cleanNulls(value)??""])) as CatalogMasterRow).filter(row=>row["Артикул"]&&row["Название товара"]);'
    if old_rows not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: catalog row source anchor not found")
    text = text.replace(old_rows, new_rows, 1)

    pvz_block = re.search(r'(const KD_PVZ_POINTS:Record<string,string\[]>\s*=\s*\{.*?\n\};)', text, re.S)
    if not pvz_block:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: KD_PVZ_POINTS block not found")
    aliases = '''\nconst SITE_CITY_SUGGESTIONS=SITE_DB_CITIES.length?SITE_DB_CITIES:KD_CITY_SUGGESTIONS;
const SITE_ADDRESS_SUGGESTIONS=Object.keys(SITE_DB_ADDRESS_SUGGESTIONS).length?SITE_DB_ADDRESS_SUGGESTIONS:KD_ADDRESS_SUGGESTIONS;
const SITE_PVZ_POINTS=Object.keys(SITE_DB_PVZ_POINTS).length?SITE_DB_PVZ_POINTS:KD_PVZ_POINTS;'''
    text = text[:pvz_block.end()] + aliases + text[pvz_block.end():]
    text = text.replace('const items=KD_CITY_SUGGESTIONS.filter(', 'const items=SITE_CITY_SUGGESTIONS.filter(', 1)
    text = text.replace('const source=KD_ADDRESS_SUGGESTIONS[city]??[];', 'const source=SITE_ADDRESS_SUGGESTIONS[city]??[];', 1)
    text = text.replace('const pvz=KD_PVZ_POINTS[form.city]??[];', 'const pvz=SITE_PVZ_POINTS[form.city]??[];', 1)

    # Keep legacy literals as build/export fallback, but make the database values primary at runtime.
    store_match = re.search(r'(  const storePoints:Record<string,string\[]>\s*=\s*\{.*?\n  \};)', text, re.S)
    if not store_match:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: checkout storePoints block not found")
    text = text[:store_match.end()] + '\n  const activeStorePoints=Object.keys(SITE_DB_STORE_POINTS).length?SITE_DB_STORE_POINTS:storePoints;' + text[store_match.end():]
    text = text.replace('const stores=storePoints[form.city]??[];', 'const stores=activeStorePoints[form.city]??[];', 1)

    for function_name in ("HomeBoutiques", "BoutiqueMap"):
        pattern = rf'(function {function_name}\([^)]*\)\{{\n  )const boutiques=(\[.*?\]);'
        match = re.search(pattern, text, re.S)
        if not match:
            raise SystemExit(f"SITE_DATABASE_CONNECTED_V128: {function_name} boutiques block not found")
        replacement = match.group(1) + 'const legacyBoutiques=' + match.group(2) + ';\n  const boutiques=SITE_DB_STORES.length?SITE_DB_STORES:legacyBoutiques;'
        text = text[:match.start()] + replacement + text[match.end():]

    state_anchor = '  const [delivery,setDelivery]=useState<DeliveryMethod>("courier");\n  const [payment,setPayment]=useState<PaymentMethod>("online");'
    state_replacement = state_anchor + '\n  const paymentMethods=SITE_DB_PAYMENT_METHODS.length?SITE_DB_PAYMENT_METHODS:[{id:"online",name:"Онлайн — картой / СБП",timing:"prepaid",instruments:["bank_card","sbp"],discountPercent:3,currency:"RUB",active:true,sortOrder:1},{id:"upon",name:"При получении",timing:"on_receipt",instruments:["bank_card","cash"],discountPercent:0,currency:"RUB",active:true,sortOrder:2}] as const;\n  const deliveryMethods=SITE_DB_DELIVERY_METHODS.length?SITE_DB_DELIVERY_METHODS:[{id:"courier",name:"Курьером",minDays:2,maxDays:3,baseFeeRub:300,freeFromRub:15000,currency:"RUB",destinationType:"address",active:true,sortOrder:1},{id:"store",name:"Самовывоз",minDays:2,maxDays:3,baseFeeRub:0,freeFromRub:0,currency:"RUB",destinationType:"store",active:true,sortOrder:2},{id:"pvz",name:"ПВЗ",minDays:2,maxDays:3,baseFeeRub:0,freeFromRub:0,currency:"RUB",destinationType:"pvz",active:true,sortOrder:3}] as const;'
    if state_anchor not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: checkout state anchor not found")
    text = text.replace(state_anchor, state_replacement, 1)

    calc_old = '  const onlineDiscount=payment==="online"?Math.round(total*.03):0;\n  const shipping=delivery==="courier"?(total>=15000?0:300):0;'
    calc_new = '  const paymentConfig=paymentMethods.find(item=>item.id===payment);\n  const deliveryConfig=deliveryMethods.find(item=>item.id===delivery);\n  const onlineDiscount=paymentConfig?.discountPercent?Math.round(total*(Number(paymentConfig.discountPercent)/100)):0;\n  const shipping=deliveryConfig?(Number(deliveryConfig.freeFromRub)>0&&total>=Number(deliveryConfig.freeFromRub)?0:Number(deliveryConfig.baseFeeRub)||0):0;'
    if calc_old not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: checkout pricing anchor not found")
    text = text.replace(calc_old, calc_new, 1)

    delivery_old = '''          <div className="checkout-v69-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            <button type="button" className={delivery==="courier"?"active":""} onClick={()=>chooseDelivery("courier")}><span>▱</span><b>Курьером</b><small>2–3 дня · {shipping===0?"0 ₽":"300 ₽"}</small></button>
            <button type="button" className={delivery==="store"?"active":""} onClick={()=>chooseDelivery("store")}><span>⌂</span><b>Самовывоз</b><small>2–3 дня · 0 ₽</small></button>
            <button type="button" className={delivery==="pvz"?"active":""} onClick={()=>chooseDelivery("pvz")}><span>▦</span><b>ПВЗ</b><small>2–3 дня · 0 ₽</small></button>
          </div>'''
    delivery_new = '''          <div className="checkout-v69-delivery-tabs" role="radiogroup" aria-label="Способ получения">
            {deliveryMethods.map(method=><button key={method.id} type="button" className={delivery===method.id?"active":""} onClick={()=>chooseDelivery(method.id as DeliveryMethod)}><span>{method.id==="courier"?"▱":method.id==="store"?"⌂":"▦"}</span><b>{method.name}</b><small>{method.minDays}–{method.maxDays} дня · {(method.id===delivery&&shipping===0)||Number(method.baseFeeRub)===0?"0 ₽":fmt(Number(method.baseFeeRub))}</small></button>)}
          </div>'''
    if delivery_old not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: delivery tabs anchor not found")
    text = text.replace(delivery_old, delivery_new, 1)

    payment_old = '<div className="checkout-v69-payments"><button type="button" className={payment==="online"?"active":""} onClick={()=>setPayment("online")}><i/><span><b>Онлайн — картой / СБП <mark>−3%</mark></b><small>−3% при оплате сейчас</small></span></button><button type="button" className={payment==="upon"?"active":""} onClick={()=>setPayment("upon")}><i/><span><b>При получении</b><small>Картой или наличными</small></span></button></div>'
    payment_new = '<div className="checkout-v69-payments">{paymentMethods.map(method=><button key={method.id} type="button" className={payment===method.id?"active":""} onClick={()=>setPayment(method.id as PaymentMethod)}><i/><span><b>{method.name}{Number(method.discountPercent)>0&&<mark>−{method.discountPercent}%</mark>}</b><small>{Number(method.discountPercent)>0?`−${method.discountPercent}% при оплате сейчас`:method.instruments.includes("cash")?"Картой или наличными":"Оплата при оформлении"}</small></span></button>)}</div>'
    if payment_old not in text:
        raise SystemExit("SITE_DATABASE_CONNECTED_V128: payment options anchor not found")
    text = text.replace(payment_old, payment_new, 1)

    text = text.replace('alert("Доставка по России от 1 дня")', 'alert(`Доставка по России от ${SITE_DB_POLICIES.delivery_min_days??"1"} дня`)', 1)
    text = text.replace('alert("Возврат в течение 14 дней")', 'alert(`Возврат в течение ${SITE_DB_POLICIES.return_period_days??"14"} дней`)', 1)
    text = text.replace('alert("Москва · Санкт-Петербург · Казань")', 'alert(Array.from(new Set(SITE_DB_STORES.map(store=>store.city))).join(" · ")||"Москва · Санкт-Петербург · Казань")', 1)
    text = text.replace('<a href="tel:+78005553535">8 800 555-35-35</a>', '<a href={`tel:${SITE_DB_CONTACTS.support_phone??"+78005553535"}`}>8 800 555-35-35</a>', 1)
    text = text.replace('<a href="mailto:hello@kultura-doma.ru">hello@kultura-doma.ru</a>', '<a href={`mailto:${SITE_DB_CONTACTS.support_email??"hello@kultura-doma.ru"}`}>{SITE_DB_CONTACTS.support_email??"hello@kultura-doma.ru"}</a>', 1)

PAGE.write_text(text, encoding="utf-8")
print(
    "// SITE_DATABASE_CONNECTED_V128: "
    f"generated={GENERATED.relative_to(ROOT)}; page_changed={text != original}; "
    f"payments={len(payments)}; deliveries={len(deliveries)}; cities={len(cities)}; stores={len(stores)}; "
    f"catalog_source=database/01+02+18+19 with catalog_master fallback"
)
