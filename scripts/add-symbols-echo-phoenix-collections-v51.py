from pathlib import Path

root = Path(__file__).resolve().parents[1]
page_path = root / "app" / "page.tsx"
page = page_path.read_text(encoding="utf-8")

if "COLLECTION_RENAMES_V51" in page:
    print("V51 renamed collections already applied")
    raise SystemExit(0)

marker = 'type Editorial = { id:string; name:string; kind:"КАПСУЛА"|"КОЛЛЕКЦИЯ"; lead:string; detail:string; description:string; images:string[]; productIds:number[] };'
if marker not in page:
    raise RuntimeError("Editorial type marker not found")

products_block = r'''
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
  // Мокоши → «Символы»
  {id:1666,name:"Комплект постельного белья с вышивкой Мокоши",note:"вышивка, коллекция Мокоши",price:21900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg",selectedColor:"Белый",selectedSize:"Полуторный (145х200 см)",skus:[
    makeCollectionEditorialSku(1666,"УТ-00010396","Мокоши","Белый","Полуторный (145х200 см)","текстиль",21900,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a328c24848cf_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a328c2353759_big.jpg"]),
    makeCollectionEditorialSku(1666,"УТ-00010396","Мокоши","Белый","Евро (200х220 см)","текстиль",29900,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg"),
    makeCollectionEditorialSku(1666,"УТ-00010397","Мокоши","Белый","Кинг-сайз (220х240 см)","текстиль",33900,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg"),
    makeCollectionEditorialSku(1666,"УТ-00010398","Мокоши","Белый","Семейный (145х200 см х 2 шт)","текстиль",35900,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg"),
  ]},
  {id:1328,name:"Кофейная пара Мокоши",note:"фарфор, 75 мл",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69441f32012f2_big.jpg",selectedColor:"Белый",selectedSize:"75 мл",skus:[makeCollectionEditorialSku(1328,"УТ-00010932","Мокоши","Белый","75 мл","фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/69441f32012f2_big.jpg")]},
  {id:1329,name:"Тарелка десертная Мокоши",note:"фарфор, 19 см",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/694150e829683_big.jpg",selectedColor:"Белый",selectedSize:"19 см",skus:[makeCollectionEditorialSku(1329,"УТ-00010931","Мокоши","Белый","19 см","фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/694150e829683_big.jpg")]},
  {id:1330,name:"Чайная пара Мокоши",note:"фарфор, 250 мл",price:4590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/694151510f837_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1330,"УТ-00010930","Мокоши","Белый","250 мл","фарфор",4590,"https://kultura-doma.ru/public/src/images/gallery/catalog/694151510f837_big.jpg")]},
  {id:1354,name:"Плейсмат Мокоши",note:"сатин, 40×50 см",price:1590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f219228e2f7_big.jpg",selectedColor:"Белый",selectedSize:"40×50 см",skus:[makeCollectionEditorialSku(1354,"УТ-00010587","Мокоши","Белый","40×50 см","сатин",1590,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f219228e2f7_big.jpg")]},
  {id:1368,name:"Скатерть Мокоши",note:"сатин, 180×180 см",price:19900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3015125e4e0_big.jpg",selectedColor:"Белый",selectedSize:"180×180 см",skus:[makeCollectionEditorialSku(1368,"УТ-00010450","Мокоши","Белый","180×180 см","сатин",19900,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3015125e4e0_big.jpg")]},
  {id:1369,name:"Дорожка с кисточками Мокоши",note:"лён, 50×180 см",price:14900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f218c75fc49_big.jpg",selectedColor:"Белый",selectedSize:"50×180 см",skus:[makeCollectionEditorialSku(1369,"УТ-00010414","Мокоши","Белый","50×180 см","лён",14900,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f218c75fc49_big.jpg")]},
  {id:1437,name:"Подушка декоративная Алатырь",note:"40×40 см",price:5990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69e233fdc6992_big.jpg",selectedColor:"Бежевый",selectedSize:"40×40 см",skus:[makeCollectionEditorialSku(1437,"УТ-00011033","Мокоши","Бежевый","40×40 см","текстиль",5990,"https://kultura-doma.ru/public/src/images/gallery/catalog/69e233fdc6992_big.jpg")]},
  {id:1438,name:"Подушка декоративная Мокоши",note:"40×40 см",price:5990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69e234045d0a5_big.jpg",selectedColor:"Бежевый",selectedSize:"40×40 см",skus:[makeCollectionEditorialSku(1438,"УТ-00011034","Мокоши","Бежевый","40×40 см","текстиль",5990,"https://kultura-doma.ru/public/src/images/gallery/catalog/69e234045d0a5_big.jpg")]},

  // Камея → «Эхо»
  {id:1552,name:"Блюдо овальное Камея",note:"костяной фарфор, 25×18 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg",selectedColor:"Белый",selectedSize:"25×18 см",skus:[makeCollectionEditorialSku(1552,"УТ-00011436","Камея","Белый","25×18 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg")]},
  {id:1554,name:"Молочник Камея",note:"костяной фарфор, 130 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg",selectedColor:"Белый",selectedSize:"130 мл",skus:[makeCollectionEditorialSku(1554,"УТ-00011441","Камея","Белый","130 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394aeea5edf_big.jpg")]},
  {id:1556,name:"Чайная пара Камея",note:"костяной фарфор, 250 мл",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1556,"УТ-00011517","Камея","Белый","250 мл","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg")]},
  {id:1557,name:"Кофейная пара Камея",note:"костяной фарфор, 90 мл",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg",selectedColor:"Белый",selectedSize:"90 мл",skus:[makeCollectionEditorialSku(1557,"УТ-00011518","Камея","Белый","90 мл","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af3ed506_big.jpg")]},
  {id:1558,name:"Супница Камея",note:"фарфор, 31×23,7×14 см",price:7273,oldPrice:10390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg",selectedColor:"Белый",selectedSize:"31×23,7×14 см",skus:[makeCollectionEditorialSku(1558,"УТ-00011448","Камея","Белый","31×23,7×14 см","костяной фарфор",7273,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg")]},
  {id:1561,name:"Сахарница Камея",note:"костяной фарфор",price:2513,oldPrice:3590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1561,"УТ-00011440","Камея","Белый","Единый размер","костяной фарфор",2513,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af59a5dc_big.jpg")]},
  {id:1562,name:"Тарелка десертная Камея",note:"костяной фарфор, 20,8 см",price:1673,oldPrice:2390,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg",selectedColor:"Белый",selectedSize:"20,8 см",skus:[makeCollectionEditorialSku(1562,"УТ-00011432","Камея","Белый","20,8 см","костяной фарфор",1673,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a73285a37b_big.jpg")]},
  {id:1563,name:"Тарелка закусочная Камея",note:"костяной фарфор, 23,5 см",price:2233,oldPrice:3190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg",selectedColor:"Белый",selectedSize:"23,5 см",skus:[makeCollectionEditorialSku(1563,"УТ-00011433","Камея","Белый","23,5 см","костяной фарфор",2233,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a739923911_big.jpg")]},
  {id:1564,name:"Тарелка обеденная Камея",note:"костяной фарфор, 26,6 см",price:2793,oldPrice:3990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg",selectedColor:"Белый",selectedSize:"26,6 см",skus:[makeCollectionEditorialSku(1564,"УТ-00011434","Камея","Белый","26,6 см","костяной фарфор",2793,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a06d76222d16_big.jpg")]},
  {id:1565,name:"Тарелка глубокая Камея",note:"костяной фарфор, 23 см",price:3353,oldPrice:4790,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg",selectedColor:"Белый",selectedSize:"23 см",skus:[makeCollectionEditorialSku(1565,"УТ-00011435","Камея","Белый","23 см","костяной фарфор",3353,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a7324b8aea_big.jpg")]},
  {id:1566,name:"Тарелка для супа Камея",note:"костяной фарфор, 16×11×5 см",price:1533,oldPrice:2190,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg",selectedColor:"Белый",selectedSize:"16×11×5 см",skus:[makeCollectionEditorialSku(1566,"УТ-00011447","Камея","Белый","16×11×5 см","костяной фарфор",1533,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a732cb2a24_big.jpg")]},
  {id:1567,name:"Чайник заварочный Камея",note:"костяной фарфор, 1800 мл",price:5593,oldPrice:7990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg",selectedColor:"Белый",selectedSize:"1800 мл",skus:[makeCollectionEditorialSku(1567,"УТ-00011438","Камея","Белый","1800 мл","костяной фарфор",5593,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg")]},

  // Жар-птица → «Феникс»
  {id:1669,name:"Комплект постельного белья Жар-птица",note:"вышивка, Кинг-сайз",price:16450,oldPrice:32900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg",selectedColor:"Белый",selectedSize:"Кинг-сайз (220х240 см)",skus:[makeCollectionEditorialSku(1669,"УТ-00010374","Жар-птица","Белый","Кинг-сайз (220х240 см)","текстиль",16450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg",["https://kultura-doma.ru/public/src/images/gallery/catalog/6a301288340ea_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a301287e3819_big.jpg"])]},
  {id:1257,name:"Чайная пара Жар-птица",note:"фарфор, 250 мл",price:3990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e4b2241_big.jpg",selectedColor:"Белый",selectedSize:"250 мл",skus:[makeCollectionEditorialSku(1257,"УТ-00010254","Жар-птица","Белый","250 мл","костяной фарфор",3990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e4b2241_big.jpg")]},
  {id:1259,name:"Тарелка десертная Жар-птица",note:"костяной фарфор",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg",selectedColor:"Белый",selectedSize:"Единый размер",skus:[makeCollectionEditorialSku(1259,"УТ-00010255","Жар-птица","Белый","Единый размер","костяной фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a2034e6d7d40_big.jpg")]},
  {id:1264,name:"Кружка Жар-птица",note:"фарфор, 450 мл",price:2990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/68ee0feabb4b9_big.png",selectedColor:"Белый",selectedSize:"450 мл",skus:[makeCollectionEditorialSku(1264,"УТ-00010256","Жар-птица","Белый","450 мл","фарфор",2990,"https://kultura-doma.ru/public/src/images/gallery/catalog/68ee0feabb4b9_big.png")]},
  {id:1260,name:"Салфетка Жар-птица",note:"лён, 45×45 см",price:995,oldPrice:1990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d2ae09776_big.jpg",selectedColor:"Белый",selectedSize:"45×45 см",skus:[makeCollectionEditorialSku(1260,"УТ-00010563","Жар-птица","Белый","45×45 см","лён",995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a43d2ae09776_big.jpg")]},
  {id:1261,name:"Подушка декоративная Жар-птица",note:"18×60 см",price:3950,oldPrice:7900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d1802c449_big.jpg",selectedColor:"Бежевый",selectedSize:"18×60 см",skus:[makeCollectionEditorialSku(1261,"УТ-00010596","Жар-птица","Бежевый","18×60 см","текстиль",3950,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d1802c449_big.jpg")]},
  {id:1262,name:"Подушка декоративная Жар-птица",note:"40×40 см",price:2995,oldPrice:5990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a05e8f392e1b_big.jpg",selectedColor:"Бежевый",selectedSize:"40×40 см",skus:[makeCollectionEditorialSku(1262,"УТ-00010595","Жар-птица","Бежевый","40×40 см","текстиль",2995,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a05e8f392e1b_big.jpg")]},
  {id:1263,name:"Плейсмат Жар-птица",note:"лён, 40×50 см",price:1295,oldPrice:2590,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d17c5a9c1_big.jpg",selectedColor:"Белый",selectedSize:"40×50 см",skus:[makeCollectionEditorialSku(1263,"УТ-00010579","Жар-птица","Белый","40×50 см","лён",1295,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d17c5a9c1_big.jpg")]},
  {id:1267,name:"Дорожка Жар-птица",note:"50×180 см",price:3450,oldPrice:6900,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16a6263e_big.jpg",selectedColor:"Белый",selectedSize:"50×180 см",skus:[makeCollectionEditorialSku(1267,"УТ-00010411","Жар-птица","Белый","50×180 см","текстиль",3450,"https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d16a6263e_big.jpg")]},
  {id:1499,name:"Свеча с ароматом Древо жизни Жар-птица",note:"кокосовый воск, 10 см",price:4990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg",selectedColor:"Белый",selectedSize:"10 см",skus:[makeCollectionEditorialSku(1499,"УТ-00011405","Жар-птица","Белый","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a5f7f739b7a1_big.jpg")]},
  {id:1500,name:"Свеча с ароматом Сандал и Шалфей Жар-птица",note:"кокосовый воск, 10 см",price:4990,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg",selectedColor:"Белый",selectedSize:"10 см",skus:[makeCollectionEditorialSku(1500,"УТ-00011381","Жар-птица","Белый","10 см","кокосовый воск",4990,"https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg")]},
  {id:1266,name:"Ковер Жар-птица",note:"натуральная шерсть, 150×200 см",price:420000,oldPrice:600000,image:"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg",selectedColor:"Бежевый",selectedSize:"150×200 см",skus:[makeCollectionEditorialSku(1266,"УТ-00010178","Жар-птица","Бежевый","150×200 см","натуральная шерсть",420000,"https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg")]},
];

products.push(...collectionEditorialProducts.filter(item=>!products.some(existing=>existing.id===item.id)));
'''

page = page.replace(marker, products_block + "\n" + marker, 1)

array_start = page.find("const editorials:Editorial[] = [")
array_end = page.find("];\n\nexport default function Home()", array_start)
if array_start < 0 or array_end < 0:
    raise RuntimeError("Editorial array boundaries not found")

new_editorials = r'''
  { id:"symbols", name:"Символы", kind:"КОЛЛЕКЦИЯ", lead:"Знаки, орнаменты и вышивка в спокойной бело-красной палитре — современное прочтение коллекции Мокоши.", detail:"Символы соединяют графичный фарфор, столовый текстиль, вышитое постельное бельё и декоративные подушки. Народные мотивы остаются узнаваемыми, но собраны в сдержанной современной композиции.", description:"Современная коллекция о знаках и орнаментах русского дома.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3c3324b26a_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a3015125e4e0_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69e234045d0a5_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/694150e829683_big.jpg"], productIds:[1666,1328,1329,1330,1354,1368,1369,1437,1438] },
  { id:"echo", name:"Эхо", kind:"КОЛЛЕКЦИЯ", lead:"Белый костяной фарфор, мягкий рельеф и классические пропорции — новая история коллекции Камея.", detail:"Эхо построено на тихом рельефе и молочно-белой палитре. Чайные и кофейные пары, тарелки и предметы подачи работают как единый сервиз, который легко сочетать с современным текстилем и стеклом.", description:"Сдержанная фарфоровая коллекция с рельефом и классическими формами.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/6a3a77a9a9ef4_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a394af134502_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69f06b7fd6aff_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50b12627f2e_big.jpg"], productIds:[1552,1554,1556,1557,1558,1561,1562,1563,1564,1565,1566,1567] },
  { id:"phoenix", name:"Феникс", kind:"КОЛЛЕКЦИЯ", lead:"Золото, красные акценты и сказочный орнамент — выразительная новая глава коллекции Жар-птица.", detail:"Феникс объединяет спальню, сервировку и декор одной графикой. Золотые и красные детали появляются на фарфоре, текстиле, свечах и мягких предметах, создавая яркий акцент без театральной перегруженности.", description:"Выразительная коллекция с золотыми акцентами и мотивом Жар-птицы.", images:["https://kultura-doma.ru/public/src/images/gallery/catalog/69b3cde6c50d3_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6a50bb991f970_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/6978bc918b851_big.jpg","https://kultura-doma.ru/public/src/images/gallery/catalog/69f1d1802c449_big.jpg"], productIds:[1669,1257,1259,1264,1260,1261,1262,1263,1267,1499,1500,1266] },
'''

page = page[:array_end] + new_editorials + page[array_end:]
page_path.write_text(page, encoding="utf-8")
print("Added Symbols, Echo and Phoenix collections with real catalog products")
