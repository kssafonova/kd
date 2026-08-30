from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
data_client_path = root / "app" / "constructor" / "data-client.ts"

s = page_path.read_text(encoding="utf-8")
if "COLLECTIONS_REDESIGN_V65" in s:
    print("Collections V65 already applied")
    raise SystemExit

collection_start = s.index("const collectionEditorialProducts:Product[] = [")

# Remove the retired Mokoshi merchandising block from the storefront source.
mokoshi_start = s.index("  // Мокоши → «Символы»", collection_start)
echo_start = s.index("  // Камея → «Эхо»", mokoshi_start)
s = s[:mokoshi_start] + s[echo_start:]

# Turn the former Cameo and Firebird source groups into the customer-facing
# Echo and Phoenix products. Product URLs and vendor codes remain grounded in
# the existing source rows; only the merchandising/product display language changes.
echo_start = s.index("  // Камея → «Эхо»", collection_start)
phoenix_start = s.index("  // Жар-птица → «Феникс»", echo_start)
array_close = s.index("\n];\n\nproducts.push(", phoenix_start)

echo_segment = s[echo_start:phoenix_start]
echo_segment = echo_segment.replace("// Камея → «Эхо»", "// Эхо")
echo_segment = echo_segment.replace("Камея", "Эхо")

phoenix_segment = s[phoenix_start:array_close]
phoenix_segment = phoenix_segment.replace("// Жар-птица → «Феникс»", "// Феникс")
phoenix_segment = phoenix_segment.replace("Жар-птица", "Феникс").replace("Жар птица", "Феникс")

s = s[:echo_start] + echo_segment + phoenix_segment + s[array_close:]

# Add Niti from real rows in the current eligible catalogue feed. We keep the
# feed prices, materials and imagery; display copy is shortened from
# “Нити времени” to the requested collection name “Нити”.
array_close = s.index("\n];\n\nproducts.push(", collection_start)
niti_products = r'''

  // Нити — товары из текущего фида «Нити времени»
  {id:1268,name:"Чайная пара Нити",note:"костяной фарфор, 250 мл",price:4490,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg",selectedColor:"Синий",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1268,"УТ-00010261","Нити","Синий","250 мл","костяной фарфор",4490,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e7620299d06_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc53c6d_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bca1043_big.jpg"]) ]},
  {id:1270,name:"Тарелка десертная Нити",note:"костяной фарфор",price:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg",selectedColor:"Синий",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1270,"УТ-00010262","Нити","Синий","Единый размер","костяной фарфор",3590,"https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e675cf04624_big.jpg"]) ]},
  {id:1287,name:"Кружка Нити",note:"костяной фарфор, 450 мл",price:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68efaf6f5d4d9_big.jpg",selectedColor:"Синий",selectedSize:"450 мл",skus:[makeCollectionEditorialSku(1287,"УТ-00010263","Нити","Синий","450 мл","костяной фарфор",3590,"https://kultura-doma.ru/public/src/images/gallery/catalog/68efaf6f5d4d9_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68ee105cb8a67_big.jpg"]) ]},
  {id:1271,name:"Салфетка Нити",note:"сатин, 45×45 см",price:995,oldPrice:1990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d36ad614e_big.jpg",selectedColor:"Белый",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1271,"УТ-00010564","Нити","Белый","45×45 см","сатин",995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d36ad614e_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e6763f9c9ed_big.jpg"]) ]},
  {id:1272,name:"Подушка декоративная Нити",note:"45×45 см",price:2745,oldPrice:5490,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/assets/images/69e5d18433139_big__83f18d3de5.jpg",selectedColor:"Голубой",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1272,"УТ-00010599","Нити","Голубой","45×45 см","текстиль",2745,"https://kultura-doma.ru/public/src/images/gallery/catalog/assets/images/69e5d18433139_big__83f18d3de5.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e669d46c745_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/68e61cd4aadc6_big.jpg"]) ]},
  {id:1273,name:"Плейсмат Нити",note:"сатин, 38×47 см",price:1295,oldPrice:2590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg",selectedColor:"Синий",selectedSize:"38×47 см",skus:[makeCollectionEditorialSku(1273,"УТ-00010580","Нити","Синий","38×47 см","сатин",1295,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e6767806b54_big.jpg"]) ]},
  {id:1276,name:"Дорожка Нити",note:"сатин, 50×180 см",price:3450,oldPrice:6900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16b97b10_big.jpg",selectedColor:"Синий",selectedSize:"50×180 см",skus:[makeCollectionEditorialSku(1276,"УТ-00010412","Нити","Синий","50×180 см","сатин",3450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16b97b10_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/68e678cb78600_big.jpg"]) ]},'''
s = s[:array_close] + niti_products + s[array_close:]

# Retire the requested names from the actual storefront product array, not just
# from collection navigation. This also protects catalogue/search/PDP entry paths
# driven by the shared products array.
old_push = "products.push(...collectionEditorialProducts.filter(item=>!products.some(existing=>existing.id===item.id)));"
if old_push not in s:
    raise RuntimeError("collection products push marker not found")
visibility_block = r'''// COLLECTIONS_REDESIGN_V65
const normalizeRetiredCatalogName=(value:string)=>String(value||"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е").replace(/[‐‑‒–—]/g,"-").replace(/\s+/g," ");
const isRetiredCatalogProduct=(name:string)=>{const value=normalizeRetiredCatalogName(name);return value.includes("мокоши")||value.includes("овация")||/жар(?:-| )?птица/.test(value)};
for(let index=products.length-1;index>=0;index-=1){if(isRetiredCatalogProduct(products[index].name))products.splice(index,1)}
products.push(...collectionEditorialProducts.filter(item=>!isRetiredCatalogProduct(item.name)&&!products.some(existing=>existing.id===item.id)));'''
s = s.replace(old_push, visibility_block, 1)

# Rebuild the collection index around the two existing stories plus Echo, Niti
# and Phoenix. Product ids are derived from the collection SKUs so the stories
# stay in sync with the real commerce cards.
editorials_start = s.index("// COLLECTIONS_ONLY_V49\nconst editorials:Editorial[] = [")
editorials_end = s.index("\n];\n\nexport default function Home()", editorials_start) + len("\n];")
editorials_block = r'''// COLLECTIONS_REDESIGN_V65_INDEX
const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);
const editorials:Editorial[] = [
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле. Белый, ледяной голубой и деликатный орнамент создают ощущение тихого зимнего утра.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/assets/images/caps_led.png","/assets/images/caps_led_podyshka.png","/assets/images/caps_led_podyshka2.png","/assets/images/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КОЛЛЕКЦИЯ", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю: вышитый текстиль, кружево, кобальтовый фарфор и свет, который делает дом почти театральным.", description:"Коллекция о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/assets/images/caps_luna_postel.png","/assets/images/caps_luna_postel2.png","/assets/images/caps_luna_postel3.png","/assets/images/caps_luna_serviz.png"], productIds:[4,10,5,6,3] },
  { id:"echo", name:"Эхо", kind:"КОЛЛЕКЦИЯ", lead:"Светлый фарфор и тонкий рельеф для спокойной, современной сервировки.", detail:"Эхо строится на белом костяном фарфоре и мягком повторении формы — от чайной пары до большого блюда. Коллекция легко собирается как для ежедневного стола, так и для камерного ужина.", description:"Чистая сервировка, в которой декоративность проявляется через пропорции, рельеф и свет.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg"], productIds:collectionProductIds("Эхо") },
  { id:"niti", name:"Нити", kind:"КОЛЛЕКЦИЯ", lead:"Синий орнамент, сатин и фарфор связывают текстиль и сервировку в одну историю.", detail:"Нити соединяет предметы стола и мягкий декор через холодную синюю палитру. Салфетки, плейсматы, фарфор и подушка работают как один набор, но каждый предмет можно выбрать отдельно.", description:"Коллекция о повторяющемся орнаменте и тактильных слоях — от сервировки до декоративного текстиля.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/assets/images/69e5d18433139_big__83f18d3de5.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3d12c459adc_big.jpg"], productIds:collectionProductIds("Нити") },
  { id:"phoenix", name:"Феникс", kind:"КОЛЛЕКЦИЯ", lead:"Тёплые акценты, золото и выразительный орнамент для дома с характером.", detail:"Феникс объединяет спальню, сервировку и атмосферный декор. Светлый фон делает рисунок легче, а золотые и красные акценты собирают предметы в цельный образ.", description:"Выразительная коллекция для тех, кто хочет добавить в интерьер один сильный мотив и продолжить его в нескольких зонах дома.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg"], productIds:collectionProductIds("Феникс") },
];'''
s = s[:editorials_start] + editorials_block + s[editorials_end:]

# Query aliases now target only collection names that actually exist on the
# landing page, including the feed source name “Нити времени”.
s = re.sub(
    r'const aliases:Record<string,string>=\{[^}]*\};',
    'const aliases:Record<string,string>={"камея":"Эхо","эхо":"Эхо","нити времени":"Нити","нити":"Нити","жар-птица":"Феникс","жар птица":"Феникс","феникс":"Феникс"};',
    s,
    count=1,
)

# Collection details are immediately shoppable: visible black checkboxes and a
# single sticky Buy action at the bottom, with no duplicate purchase mode CTA.
s = s.replace('const [purchaseMode,setPurchaseMode]=useState(false);', 'const [purchaseMode,setPurchaseMode]=useState(Boolean(initialEditorial));', 1)
s = s.replace('const open=(editorial:Editorial)=>{setActive(editorial);setPurchaseMode(false);setSelectedIds([]);setSizes({});setVariants({})};', 'const open=(editorial:Editorial)=>{setActive(editorial);setPurchaseMode(true);setSelectedIds([]);setSizes({});setVariants({})};', 1)

commerce_anchor = s.index('<section className="v52-story-commerce" aria-label="Товары коллекции">')
head_start = s.index('<header className="v52-commerce-head">', commerce_anchor)
head_end = s.index('</header>', head_start) + len('</header>')
new_head = '''<header className="v52-commerce-head"><div><small>ТОВАРЫ КОЛЛЕКЦИИ</small><h2>Выберите предметы</h2><p>Отметьте нужные позиции. Если у товара несколько размеров, размер появится после выбора.</p></div><div className="v65-commerce-actions"><button type="button" onClick={()=>setSelectedIds(allSelected?[]:items.map(item=>item.id))}>{allSelected?"Снять выбор":"Выбрать всё"}</button></div></header>'''
s = s[:head_start] + new_head + s[head_end:]
s = s.replace('selectionMode={purchaseMode}', 'selectionMode={true}', 1)
s = s.replace('{purchaseMode&&selected&&options.length>1&&', '{selected&&options.length>1&&', 1)
footer_match = re.search(r'\{purchaseMode&&<footer className="v52-purchase-bar">(.*?)</footer>\}', s, re.S)
if not footer_match:
    raise RuntimeError("collection purchase footer not found")
footer_inner = footer_match.group(1).replace('ДОБАВИТЬ В КОРЗИНУ', 'КУПИТЬ')
footer = '<footer className="v52-purchase-bar">' + footer_inner + '</footer>'
s = s[:footer_match.start()] + footer + s[footer_match.end():]

# Keep the collection → ready-solutions bridge aligned with source collection names.
s = s.replace(
    '{"Символы":"Мокоши","Эхо":"Камея","Феникс":"Жар-птица"}',
    '{"Эхо":"Камея","Нити":"Нити времени","Феникс":"Жар-птица"}',
    1,
)

page_path.write_text(s, encoding="utf-8")

# Constructor / Ready Solutions must follow the same retired-product rule. Cameo
# stays available as the source behind customer-facing Echo; Ovation is removed.
d = data_client_path.read_text(encoding="utf-8")
d = re.sub(
    r'const REMOVED_CATALOG_NAME_TOKENS = \[.*?\] as const;',
    'const REMOVED_CATALOG_NAME_TOKENS = [\n  "мокоши",\n  "жар-птица",\n  "жар птица",\n  "жарптица",\n  "овация",\n] as const;',
    d,
    count=1,
    flags=re.S,
)
data_client_path.write_text(d, encoding="utf-8")
print("Collections V65 applied")
