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
  capsule?:string;
  price:number;
  image:string;
  gallery:string[];
  available?:boolean;
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
  "Серо-синий":"#738699",
  "Ночной синий":"#10233e",
  "Пудровый":"#e6bca8",
  "Льняной":"#d2c1aa",
  "Небесный":"#9fb2c6",
  "Ледяной голубой":"#afcbd1",
};

const COLOR_CODE:Record<string,string> = {
  "Белый":"WHITE",
  "Молочный":"MILK",
  "Синий":"BLUE",
  "Песочный":"SAND",
  "Серо-синий":"GREY-BLUE",
  "Ночной синий":"NIGHT-BLUE",
  "Пудровый":"POWDER",
  "Льняной":"LINEN",
  "Небесный":"SKY",
  "Ледяной голубой":"ICE-BLUE",
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
  makeProduct(2,"KD-PD-1022","Пододеяльник из сатина","сатин, 140×220 / 200×220 / 220×240 см",18990,[
    {color:"Белый",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-product-bed.png",gallery:["/images/classic-bedroom.png"]},
    {color:"Белый",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-product-bed.png",gallery:["/images/classic-bedroom.png"]},
    {color:"Белый",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-product-bed.png",gallery:["/images/classic-bedroom.png"],available:false},
    {color:"Льняной",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/beige-bedroom.png",gallery:["/images/classic-bedroom.png"]},
    {color:"Льняной",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/beige-bedroom.png",gallery:["/images/classic-bedroom.png"]},
    {color:"Льняной",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/beige-bedroom.png",gallery:["/images/classic-bedroom.png"],available:false},
    {color:"Небесный",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/blue-bedroom.png",gallery:["/images/blue-bedding-vertical.png"]},
    {color:"Небесный",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/blue-bedroom.png",gallery:["/images/blue-bedding-vertical.png"]},
    {color:"Небесный",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/blue-bedroom.png",gallery:["/images/blue-bedding-vertical.png"],available:false},
    {color:"Пудровый",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/peach-sheet.jpg",gallery:["/images/products/KD-PD-1028-PUDRA02.png"]},
    {color:"Пудровый",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/peach-sheet.jpg",gallery:["/images/products/KD-PD-1028-PUDRA02.png"]},
    {color:"Пудровый",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/peach-sheet.jpg",gallery:["/images/products/KD-PD-1028-PUDRA02.png"],available:false},
    {color:"Ночной синий",size:"Полуторный (140×220 см)",height:"140 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-collection-night.png",gallery:["/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Евро (200×220 см)",height:"200 см",width:"220 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-collection-night.png",gallery:["/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Кинг сайз (220×240 см)",height:"220 см",width:"240 см",packageInfo:"Пододеяльник 1 шт.",material:"Шелк",composition:"100% Сатин",image:"/images/zip-collection-night.png",gallery:["/images/products/KD-PD-1024-DARK02.png"],available:false},
  ]),

  makeProduct(3,"KD-PD-1023","Подушка с кружевом","хлопок, 60×60 см",5990,[
    {color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-WHITE02.png",gallery:["/kd/images/products/KD-PD-1023-WHITE02.png"]},
    {color:"Молочный",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-BEIGE01.png",gallery:["/kd/images/products/KD-PD-1023-BEIGE02.png"]},
    {color:"Синий",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",image:"/kd/images/products/KD-PD-1023-BLUE02.png",gallery:["/kd/images/products/KD-PD-1023-BLUE02.png"]},
  ]),

  makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",12990,[
    {color:"Белый",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-WHITE01.png",gallery:["/kd/images/products/KD-PD-1026-WHITE02.png"]},
    {color:"Молочный",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-BEIGE01.png",gallery:["/kd/images/products/KD-PD-1026-BEIGE02.png"]},
    {color:"Синий",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",image:"/kd/images/products/KD-PD-1026-BLUE01.png",gallery:["/kd/images/products/KD-PD-1026-BLUE02.png"]},
  ]),

  makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",8690,[
    {color:"Молочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",image:"/kd/images/products/KD-PD-1027-MOL01.png",gallery:[]},
    {color:"Молочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",price:9990,image:"/kd/images/products/KD-PD-1027-MOL01.png",gallery:[]},
    {color:"Серо-синий",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",image:"/kd/images/products/KD-PD-1027-PES01.png",gallery:[]},
    {color:"Серо-синий",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр Наполнитель: 100% полиэфирное волокно",price:9990,image:"/kd/images/products/KD-PD-1027-PES01.png",gallery:[]},
  ]),

  makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",6990,[
    {color:"Ночной синий",size:"250 мл",diameter:"15 см",packageInfo:"Кружка 1 шт, Блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",image:"/kd/images/time-tea-pair.png",gallery:[]},
  ]),

  makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",24990,[
    {color:"Ночной синий",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
    {color:"Ночной синий",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",image:"/kd/images/products/KD-PD-1024-DARK01.png",gallery:["/kd/images/products/KD-PD-1024-DARK02.png"]},
  ]),

  makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",5990,[
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
    {color:"Ночной синий",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",material:"Шелк",composition:"100% Сатин",image:"/kd/images/products/KD-PD-1128-DARK01.png",gallery:["/kd/images/products/KD-PD-1128-DARK03.png"]},
  ]),

  // ICE_PATTERN_PRODUCTS_V1
  makeProduct(2000,"KD-PD-2000","Декоративная подушка «Ледяные узоры»","хлопок, 50×50 см",5990,[
    {color:"Ледяной голубой",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2001,"KD-PD-2001","Тарелка «Ледяные узоры»","костяной фарфор, 23 см",7990,[
    {color:"Ночной синий",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-DARK01.png",gallery:[]},
    {color:"Белый",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2003,"KD-PD-2003","Плед «Ледяные узоры»","шерсть и хлопок, 140×200 см",12990,[
    {color:"Ледяной голубой",size:"140×200 см",height:"140 см",width:"200 см",packageInfo:"Плед 1 шт",material:"Шерсть и хлопок",composition:"70% шерсть, 30% хлопок",details:"Жаккардовый орнамент",collection:"Ледяные узоры",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ]),
  makeProduct(2004,"KD-PD-2004","Чайная пара «Ледяные узоры»","костяной фарфор, 250 мл",6990,[
    {color:"Белый",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2004-WHITE01.png",gallery:[]},
  ]),
  makeProduct(2010,"KD-PD-2010","Салатник «Ледяные узоры»","костяной фарфор, 24 см",9990,[
    {color:"Белый",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Ночной синий",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-DARK01.png",gallery:[]},
  ]),
];

export const catalogProductOverrides:Record<number,CatalogProductOverride> = Object.fromEntries(
  productList.map(product=>[product.id,product])
);

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  productList.flatMap(product=>product.skus).map(item=>[item.id,item])
);
