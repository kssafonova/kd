from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
ready_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
marker = "// EDITORIAL_COMMERCE_V81"

page = page_path.read_text(encoding="utf-8")
ready = ready_path.read_text(encoding="utf-8")

# --- Collections / Echo: full CSV-grounded image assortment ---
echo_segment = r'''  // Эхо — полный ассортимент из CSV «Камея», изображения и галереи из фида
  {id:1552,name:"Блюдо овальное Эхо",note:"костяной фарфор, 25х18 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg",selectedColor:"Белый",selectedSize:"25х18 см",skus:[makeCollectionEditorialSku(1552,"УТ-00011436","Эхо","Белый","25х18 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a575b5c5163_big.jpg"])]},
  {id:1553,name:"Блюдо овальное Эхо",note:"костяной фарфор, 36х26 см",price:4473,oldPrice:6390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a832033_big.jpg",selectedColor:"Белый",selectedSize:"36х26 см",skus:[makeCollectionEditorialSku(1553,"УТ-00011437","Эхо","Белый","36х26 см","костяной фарфор",4473,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a832033_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a575cbeca53_big.jpg"])]},
  {id:1554,name:"Молочник Эхо",note:"костяной фарфор, 130 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg",selectedColor:"Белый",selectedSize:"130 мл",skus:[makeCollectionEditorialSku(1554,"УТ-00011441","Эхо","Белый","130 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15ad53ba204_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69a5765de48a1_big.jpg"])]},
  {id:1555,name:"Кружка Эхо",note:"костяной фарфор, 350 мл",price:1953,oldPrice:2790,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aefe9f00_big.jpg",selectedColor:"Белый",selectedSize:"350 мл",skus:[makeCollectionEditorialSku(1555,"УТ-00011442","Эхо","Белый","350 мл","костяной фарфор",1953,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aefe9f00_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a5787c5c475_big.jpg"])]},
  {id:1556,name:"Чайная пара Эхо",note:"костяной фарфор, 250 мл",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1556,"УТ-00011517","Эхо","Белый","250 мл","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a5760b0ab4b_big.jpg"])]},
  {id:1557,name:"Кофейная пара Эхо",note:"костяной фарфор, 90 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg",selectedColor:"Белый",selectedSize:"90 мл",skus:[makeCollectionEditorialSku(1557,"УТ-00011518","Эхо","Белый","90 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15ad989a8a5_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3a736d_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af4453b5_big.jpg"])]},
  {id:1558,name:"Супница Эхо",note:"костяной фарфор, 31х23,7х14 см",price:7273,oldPrice:10390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg",selectedColor:"Белый",selectedSize:"31х23,7х14 см",skus:[makeCollectionEditorialSku(1558,"УТ-00011448","Эхо","Белый","31х23,7х14 см","костяной фарфор",7273,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15b01297ff6_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b801a49b_big.jpg"])]},
  {id:1559,name:"Салатник Эхо",note:"костяной фарфор",price:903,oldPrice:1290,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a85f308820_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1559,"УТ-00011449","Эхо","Белый","Единый размер","костяной фарфор",903,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a85f308820_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a5751851cd4_big.jpg"])]},
  {id:1560,name:"Салатник Эхо",note:"костяной фарфор, 20 см",price:3283,oldPrice:4690,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a861165ce4_big.jpg",selectedColor:"Белый",selectedSize:"20 см",skus:[makeCollectionEditorialSku(1560,"УТ-00011450","Эхо","Белый","20 см","костяной фарфор",3283,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a861165ce4_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15afd9285dd_big.jpg"])]},
  {id:1561,name:"Сахарница Эхо",note:"костяной фарфор",price:2513,oldPrice:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1561,"УТ-00011440","Эхо","Белый","Единый размер","костяной фарфор",2513,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15aede2722f_big.jpg"])]},
  {id:1562,name:"Тарелка десертная Эхо",note:"костяной фарфор, 20,8 см",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg",selectedColor:"Белый",selectedSize:"20,8 см",skus:[makeCollectionEditorialSku(1562,"УТ-00011432","Эхо","Белый","20,8 см","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a5772a9dbd2_big.jpg"])]},
  {id:1563,name:"Тарелка закусочная Эхо",note:"костяной фарфор, 23,5 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg",selectedColor:"Белый",selectedSize:"23,5 см",skus:[makeCollectionEditorialSku(1563,"УТ-00011433","Эхо","Белый","23,5 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a576f26a902_big.jpg"])]},
  {id:1564,name:"Тарелка обеденная Эхо",note:"костяной фарфор, 26,6 см",price:2793,oldPrice:3990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg",selectedColor:"Белый",selectedSize:"26,6 см",skus:[makeCollectionEditorialSku(1564,"УТ-00011434","Эхо","Белый","26,6 см","костяной фарфор",2793,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a576c56bb35_big.jpg"])]},
  {id:1565,name:"Тарелка глубокая Эхо",note:"костяной фарфор, 23 см",price:3353,oldPrice:4790,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg",selectedColor:"Белый",selectedSize:"23 см",skus:[makeCollectionEditorialSku(1565,"УТ-00011435","Эхо","Белый","23 см","костяной фарфор",3353,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/69a5769a92bc5_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324f2ff1_big.jpg"])]},
  {id:1566,name:"Тарелка для супа Эхо",note:"костяной фарфор, 16х11х5 см",price:1533,oldPrice:2190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg",selectedColor:"Белый",selectedSize:"16х11х5 см",skus:[makeCollectionEditorialSku(1566,"УТ-00011447","Эхо","Белый","16х11х5 см","костяной фарфор",1533,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a15b0794dc81_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/699f0fd03a5c0_big.jpg"])]},
  {id:1567,name:"Чайник заварочный Эхо",note:"костяной фарфор, 1800 мл",price:5593,oldPrice:7990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg",selectedColor:"Белый",selectedSize:"1800 мл",skus:[makeCollectionEditorialSku(1567,"УТ-00011438","Эхо","Белый","1800 мл","костяной фарфор",5593,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/699f11c473620_big.jpg"])]},
  {id:1568,name:"Чайник заварочный Эхо",note:"костяной фарфор, 900 мл",price:4473,oldPrice:6390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af835e91_big.jpg",selectedColor:"Белый",selectedSize:"900 мл",skus:[makeCollectionEditorialSku(1568,"УТ-00011439","Эхо","Белый","900 мл","костяной фарфор",4473,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af835e91_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/699d71e583d98_big.jpg"])]},

'''
echo_start = page.find("  // Эхо", page.find("const collectionEditorialProducts:Product[] = ["))
phoenix_start = page.find("  // Феникс", echo_start)
if echo_start >= 0 and phoenix_start > echo_start:
    page = page[:echo_start] + echo_segment + page[phoenix_start:]

# Keep collection index complete and editorial.
idx_start = page.find("// COLLECTIONS_REDESIGN_V65_INDEX")
idx_end = page.find("\n];\n\nexport default function Home()", idx_start)
if idx_start >= 0 and idx_end > idx_start:
    idx_end += len("\n];")
    index_block = r'''// COLLECTIONS_REDESIGN_V65_INDEX
const collectionProductIds=(collection:string)=>collectionEditorialProducts.filter(item=>!REMOVED_PRODUCT_IDS.has(item.id)&&item.skus?.some(sku=>sku.collection===collection)).map(item=>item.id);
const editorials:Editorial[] = [
  { id:"ice", name:"Ледяные узоры", kind:"КОЛЛЕКЦИЯ", lead:"Светлая зимняя палитра, прозрачный голубой и мягкие фактуры для спокойной спальни.", detail:"Истории спальни построены на холодном свете, вышивке и тактильном текстиле.", description:"Коллекция для спальни о свете, воздухе и узорах, напоминающих морозное стекло.", images:["/assets/images/caps_led.png","/assets/images/caps_led_podyshka.png","/assets/images/caps_led_serviz.png"], productIds:[2000,2001,2003,2004,2010] },
  { id:"luna", name:"Лунная сказка", kind:"КОЛЛЕКЦИЯ", lead:"Ночная палитра, мягкий блеск сатина и фарфор цвета глубокого неба.", detail:"Лунная сказка соединяет спальню и сервировку в одну тихую историю.", description:"Коллекция о ночных домашних ритуалах — от спальни до позднего чаепития.", images:["/assets/images/caps_luna_postel.png","/assets/images/caps_luna_postel2.png","/assets/images/caps_luna_serviz.png"], productIds:[4,10,5,6,3] },
  { id:"echo", name:"Эхо", kind:"КОЛЛЕКЦИЯ", lead:"Светлый фарфор и тонкий рельеф для спокойной современной сервировки.", detail:"Эхо строится на белом костяном фарфоре и мягком повторении формы.", description:"Чистая сервировка, где декоративность проявляется через пропорции, рельеф и свет.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg"], productIds:collectionProductIds("Эхо") },
  { id:"niti", name:"Нити", kind:"КОЛЛЕКЦИЯ", lead:"Синий орнамент, сатин и фарфор связывают текстиль и сервировку.", detail:"Нити соединяет предметы стола и мягкий декор через холодную синюю палитру.", description:"Коллекция о повторяющемся орнаменте и тактильных слоях.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/68f21aab5a5cf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f82bc133aa_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/assets/images/69e5d18433139_big__83f18d3de5.jpg"], productIds:collectionProductIds("Нити") },
  { id:"phoenix", name:"Феникс", kind:"КОЛЛЕКЦИЯ", lead:"Тёплые акценты и выразительный орнамент для дома с характером.", detail:"Феникс объединяет сервировку и атмосферный декор в единую историю.", description:"Выразительная коллекция с сильным мотивом и спокойной базой.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg"], productIds:collectionProductIds("Феникс") },
];'''
    page = page[:idx_start] + index_block + page[idx_end:]

old_categories = r'''  const categories=[
    {eyebrow:"СПАЛЬНЯ",title:"Постельное бельё",image:"/assets/images/blue-bedroom.png",category:"Постельное бельё"},
    {eyebrow:"КУХНЯ И СТОЛОВАЯ",title:"Посуда и сервировка",image:"/assets/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {eyebrow:"ТЕКСТИЛЬ И ДЕКОР",title:"Пледы и подушки",image:"/assets/images/beige-bedroom.png",category:"Пледы и подушки"},
  ];'''
new_categories = r'''  const categories=[
    {eyebrow:"СПАЛЬНЯ",title:"Постельное бельё",image:"/assets/images/blue-bedroom.png",category:"Постельное бельё"},
    {eyebrow:"КУХНЯ И СТОЛОВАЯ",title:"Посуда и сервировка",image:"/assets/images/russian-service-blue.png",category:"Посуда и сервировка"},
    {eyebrow:"ГОСТИНАЯ",title:"Пледы и подушки",image:"/assets/images/beige-bedroom.png",category:"Пледы и подушки"},
    {eyebrow:"СТОЛОВАЯ",title:"Столовый текстиль",image:"/assets/images/editorial-table.png",category:"Столовый текстиль"},
    {eyebrow:"ИНТЕРЬЕР",title:"Декор для дома",image:"/assets/images/green.jpeg",category:"Декор для дома"},
    {eyebrow:"АТМОСФЕРА",title:"Свечи и диффузоры",image:"/assets/images/redline1.jpeg",category:"Свечи и диффузоры"},
  ];'''
if old_categories in page:
    page = page.replace(old_categories, new_categories, 1)

page = page.replace('const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/constructor/`;', 'const constructorHref=`${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;', 1)
old_solutions = r'''  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/assets/images/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/assets/images/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/assets/images/caps_led.png",href:`${constructorHref}table-7/`},
  ];'''
new_solutions = r'''  const solutions=[
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Зеленый салон",image:"/assets/images/green.jpeg",href:`${constructorHref}table-1/`},
    {room:"КУХНЯ И СТОЛОВАЯ",title:"Красные линии",image:"/assets/images/redline1.jpeg",href:`${constructorHref}table-2/`},
    {room:"СПАЛЬНЯ И ГОСТИНАЯ",title:"Зимняя сказка",image:"/assets/images/caps_led.png",href:`${constructorHref}table-7/`},
    {room:"КАБИНЕТ",title:"Тёплый брутализм",image:"/assets/images/green.jpeg",href:`${constructorHref}table-8/`},
  ];'''
if old_solutions in page:
    page = page.replace(old_solutions, new_solutions, 1)

editorial_start = page.find('    <section className="zh44-editorials" aria-label="Капсулы и коллекции">')
category_start = page.find('    <section className="zh44-categories zh44-section">', editorial_start)
if editorial_start >= 0 and category_start > editorial_start:
    collections_banner = r'''    <section className="zh81-collections-banner" aria-label="Коллекции">
      <picture><source media="(max-width: 700px)" srcSet={assetUrl("/assets/images/caps_luna_postel.png")}/><img src={assetUrl("/assets/images/caps_luna_postel2.png")} alt="Коллекции Культура Дома"/></picture>
      <div className="zh81-collections-copy"><small>КОЛЛЕКЦИИ</small><h2>Истории, собранные для дома</h2><p>Фарфор, текстиль и декор объединены общей палитрой и мотивом. Выберите коллекцию и соберите её целиком или по предметам.</p><button type="button" onClick={()=>go("collections")}>Смотреть коллекции <Icon name="arrow"/></button></div>
    </section>

'''
    page = page[:editorial_start] + collections_banner + page[category_start:]

if marker not in page:
    pos = page.find("function HomeView(")
    if pos >= 0:
        page = page[:pos] + marker + "\n" + page[pos:]

old_extra = 'const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; return solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);'
new_extra = 'const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; const removedBase=baseCollections.filter((base)=>!activeCollections.some((active)=>norm(active)===norm(base))); const configured=solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name); return Array.from(new Map([...removedBase,...configured].map((name)=>[norm(name),name])).values()).filter((name)=>!activeCollections.some((active)=>norm(active)===norm(name))).slice(0,6);},[catalog,solution,baseCollections,activeCollections]);'
if old_extra in ready:
    ready = ready.replace(old_extra, new_extra, 1)

old_extended = 'const extendedRows=useMemo(()=>{if(!catalog||!solution)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...baseRows,...extra].filter((row)=>!isRemovedSolutionProduct(solution.name,row)).map((row)=>applySolutionCategoryOverrides(solution.name,row));},[catalog,solution,baseRows,activeCollections]);'
new_extended = 'const extendedRows=useMemo(()=>{if(!catalog||!solution)return[]; const active=new Set(activeCollections.map(norm)); const curated=baseRows.filter((row)=>active.has(norm(sourceCollectionForRow(row)))); const keys=new Set(curated.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>active.has(norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...curated,...extra].filter((row)=>!isRemovedSolutionProduct(solution.name,row)).map((row)=>applySolutionCategoryOverrides(solution.name,row));},[catalog,solution,baseRows,activeCollections]);'
if old_extended in ready:
    ready = ready.replace(old_extended, new_extended, 1)

ready = ready.replace('{step<3&&<section className={`rs71-hero ${step===2?"is-compact":""}`}>', '<section className="rs71-hero is-compact">', 1)
ready = ready.replace('</div></section>}\n    <nav className="rs71-steps"', '</div></section>\n    <nav className="rs71-steps"', 1)

header_start = ready.find("function Header() {")
footer_start = ready.find("function Footer()", header_start)
if header_start >= 0 and footer_start > header_start:
    header = r'''function Header() {
  return <><div className="rs71-promo">БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽</div><header className="rs71-header"><div className="rs81-header-left"><Link href="/?open=menu" aria-label="Меню" className="rs71-menu"><span/><span/><span/></Link><Link href="/?open=boutiques" className="rs81-boutiques">Бутики</Link></div><Link href="/" className="rs71-logo">КУЛЬТУРА ДОМА</Link><nav><Link href="/?open=search">Поиск</Link><Link href="/?open=account">Профиль</Link><Link href="/?open=favorites">Избранное</Link><Link href="/?open=cart">Корзина</Link></nav></header></>;
}
'''
    ready = ready[:header_start] + header + ready[footer_start:]

if marker not in ready:
    ready = ready.replace("// READY_SOLUTIONS_GROUPS_V80", "// READY_SOLUTIONS_GROUPS_V80\n" + marker, 1)

page_path.write_text(page, encoding="utf-8")
ready_path.write_text(ready, encoding="utf-8")
print("Editorial commerce V81 applied")
