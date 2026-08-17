export type CatalogSku = {
  id:string;
  article:string;
  productId:number;
  color:string;
  colorHex:string;
  size:string;
  height?:string;
  width?:string;
  diameter?:string;
  packageInfo?:string;
  material:string;
  composition:string;
  details?:string;
  collection?:string;
  price:number;
  image:string;
  gallery:string[];
};

export type CatalogProductOverride = {
  id:number;
  article:string;
  name:string;
  note:string;
  skus:CatalogSku[];
};

type SkuInput = Omit<CatalogSku,"id"|"article"|"productId"|"colorHex"|"price"> & {price?:number};

const COLOR_HEX:Record<string,string> = {
  "Белый":"#f7f7f4",
  "Молочный":"#e9e1d2",
  "Синий":"#8ba7c0",
  "Песочный":"#c9ad88",
  "Ночной синий":"#10233e",
  "Пудровый":"#e6bca8",
};

const COLOR_CODE:Record<string,string> = {
  "Белый":"WHITE",
  "Молочный":"MILK",
  "Синий":"BLUE",
  "Песочный":"SAND",
  "Ночной синий":"NIGHT-BLUE",
  "Пудровый":"POWDER",
};

const sizeCode=(size:string)=>size
  .toUpperCase()
  .replaceAll("×","X")
  .replaceAll("СМ","")
  .replaceAll("МЛ","ML")
  .replaceAll("ПОЛУТОРНЫЙ","SINGLE")
  .replaceAll("ЕВРО","EURO")
  .replaceAll("КИНГ САЙЗ","KING")
  .replace(/[^A-Z0-9]+/g,"-")
  .replace(/^-|-$/g,"");

const makeProduct=(
  id:number,
  article:string,
  name:string,
  note:string,
  basePrice:number,
  rows:SkuInput[],
):CatalogProductOverride=>({
  id,
  article,
  name,
  note,
  skus:rows.map(row=>({
    ...row,
    id:`${article}-${COLOR_CODE[row.color]??row.color}-${sizeCode(row.size)}`,
    article,
    productId:id,
    colorHex:COLOR_HEX[row.color]??"#d8d5cf",
    price:row.price??basePrice,
  })),
});

const productList:CatalogProductOverride[] = [
  makeProduct(3,"KD-PD-1023","Подушка с кружевом","хлопок, 60×60 см",2990,[
    {color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-WHITE01.png",gallery:["/kd/images/products/KD-PD-1023-WHITE02.png"]},
    {color:"Молочный",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-BEIGE01.png",gallery:["/kd/images/products/KD-PD-1023-BEIGE02.png"]},
    {color:"Синий",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-BLUE01.png",gallery:["/kd/images/products/KD-PD-1023-BLUE02.png"]},
  ]),

  makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",9990,[
    {color:"Белый",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-WHITE01.png",gallery:["/kd/images/products/KD-PD-1026-WHITE02.png"]},
    {color:"Молочный",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-BIEGE01.png",gallery:["/kd/images/products/KD-PD-1026-BIEGE02.png"]},
    {color:"Синий",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-BLUE01.png",gallery:["/kd/images/products/KD-PD-1026-BLUE02.png"]},
  ]),

  makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",12990,[
    {color:"Молочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",image:"/kd/images/products/KD-PD-1027-MOL01.png",gallery:["/kd/images/products/KD-PD-1027-MOL02.png"]},
    {color:"Молочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",price:14990,image:"/kd/images/products/KD-PD-1027-MOL01.png",gallery:["/kd/images/products/KD-PD-1027-MOL02.png"]},
    {color:"Песочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",image:"/kd/images/products/KD-PD-1027-PES01.png",gallery:["/kd/images/products/KD-PD-1027-PES02.png"]},
    {color:"Песочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",price:14990,image:"/kd/images/products/KD-PD-1027-PES01.png",gallery:["/kd/images/products/KD-PD-1027-PES02.png"]},
  ]),

  makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",4490,[
    {color:"Ночной синий",size:"250 мл",diameter:"15 см",packageInfo:"Кружка 1 шт, Блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",image:"/kd/images/time-tea-pair.png",gallery:[]},
  ]),

  makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",20990,[
    {color:"Ночной синий",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
  ]),

  makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",4990,[
    {color:"Ночной синий",size:"23 см",diameter:"23 см",material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",image:"https://kssafonova.github.io/kd/images/moon-plate.png",gallery:[]},
  ]),

  makeProduct(8,"KD-PD-1028","Натяжная простыня из сатина","шёлк, 140×220 / 200×220 / 220×240 см",4990,[
    {color:"Пудровый",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"https://kssafonova.github.io/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png","/kd/images/products/KD-PD-1028-PUDRA03.png"]},
    {color:"Пудровый",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"https://kssafonova.github.io/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png","/kd/images/products/KD-PD-1028-PUDRA03.png"]},
    {color:"Пудровый",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"https://kssafonova.github.io/kd/images/peach-sheet.jpg",gallery:["/kd/images/products/KD-PD-1028-PUDRA02.png","/kd/images/products/KD-PD-1028-PUDRA03.png"]},
    {color:"Белый",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-WHITE01.png",gallery:["/kd/images/products/KD-PD-1028-WHITE03.png"]},
    {color:"Белый",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-WHITE01.png",gallery:["/kd/images/products/KD-PD-1028-WHITE03.png"]},
    {color:"Белый",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-WHITE01.png",gallery:["/kd/images/products/KD-PD-1028-WHITE03.png"]},
    {color:"Ночной синий",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-DARK01.png",gallery:["/kd/images/products/KD-PD-1028-DARK02.png"]},
    {color:"Ночной синий",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-DARK01.png",gallery:["/kd/images/products/KD-PD-1028-DARK02.png"]},
    {color:"Ночной синий",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Простынь 1 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1028-DARK01.png",gallery:["/kd/images/products/KD-PD-1028-DARK02.png"]},
  ]),

  makeProduct(11,"KD-PD-1128","Наволочка из сатина","шёлк, 60×60 см",4990,[
    {color:"Пудровый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1128-PUDRA01.png",gallery:["/kd/images/products/KD-PD-1128-PUDRA03.png"]},
    {color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1128-WHITE01.png",gallery:["/kd/images/products/KD-PD-1128-WHITE02.png","/kd/images/products/KD-PD-1128-WHITE03.png"]},
    {color:"Ночной синий",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1128-DARK01.png",gallery:["/kd/images/products/KD-PD-1128-DARK02.png"]},
  ]),
];

export const catalogProductOverrides:Record<number,CatalogProductOverride> = Object.fromEntries(
  productList.map(product=>[product.id,product])
);

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  productList.flatMap(product=>product.skus).map(item=>[item.id,item])
);
