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

const satinSizes = [
  {size:"Полуторный 140×220 см",height:"140 см",width:"220 см"},
  {size:"Евро 200×220 см",height:"200 см",width:"220 см"},
  {size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см"},
];

const fittedSheetRows=(color:string,image:string,gallery:string[]):SkuInput[]=>satinSizes.map(size=>({
  ...size,
  color,
  packageInfo:"Простынь 1 шт",
  material:"Шелк",
  composition:"100% Сатин",
  image,
  gallery,
}));

const productList:CatalogProductOverride[] = [
  makeProduct(3,"KD-PD-1023","Подушка с кружевом","хлопок, 60×60 см",2990,[
    {
      color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",
      material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",
      image:"/images/products/kd-pd-1023/white/01.webp",
      gallery:["/images/products/kd-pd-1023/white/02.webp"],
    },
    {
      color:"Молочный",size:"60×60 см",height:"60 см",width:"60 см",
      material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",
      image:"/images/products/kd-pd-1023/milk/01.webp",
      gallery:["/images/products/kd-pd-1023/milk/02.webp"],
    },
    {
      color:"Синий",size:"60×60 см",height:"60 см",width:"60 см",
      material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",
      image:"/images/products/kd-pd-1023/blue/01.webp",
      gallery:["/images/products/kd-pd-1023/blue/02.webp"],
    },
  ]),

  makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",9990,[
    {
      color:"Белый",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"/images/products/kd-pd-1026/white/01.webp",
      gallery:["/images/products/kd-pd-1026/white/02.webp"],
    },
    {
      color:"Молочный",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"/images/products/kd-pd-1026/milk/01.webp",
      gallery:["/images/products/kd-pd-1026/milk/02.webp"],
    },
    {
      color:"Синий",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"/images/products/kd-pd-1026/blue/01.webp",
      gallery:["/images/products/kd-pd-1026/blue/02.webp"],
    },
  ]),

  makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",12990,[
    {
      color:"Молочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",
      image:"/images/products/kd-pd-1027/milk/01.webp",
      gallery:["/images/products/kd-pd-1027/milk/02.webp"],
    },
    {
      color:"Молочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,
      image:"/images/products/kd-pd-1027/milk/01.webp",
      gallery:["/images/products/kd-pd-1027/milk/02.webp"],
    },
    {
      color:"Песочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",
      image:"/images/products/kd-pd-1027/sand/01.webp",
      gallery:["/images/products/kd-pd-1027/sand/02.webp"],
    },
    {
      color:"Песочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,
      image:"/images/products/kd-pd-1027/sand/01.webp",
      gallery:["/images/products/kd-pd-1027/sand/02.webp"],
    },
  ]),

  makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",4490,[
    {
      color:"Ночной синий",size:"250 мл",diameter:"15 см",packageInfo:"Кружка 1 шт, Блюдце 1 шт",
      material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",
      image:"/images/products/kd-pd-1030/night-blue/01.png",gallery:[],
    },
  ]),

  makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",20990,
    satinSizes.map(size=>({
      ...size,color:"Ночной синий",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",
      material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",
      image:"/images/products/kd-pd-1024/night-blue/01.webp",
      gallery:["/images/products/kd-pd-1024/night-blue/02.webp"],
    }))
  ),

  makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",4990,[
    {
      color:"Ночной синий",size:"23 см",diameter:"23 см",
      material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",
      image:"/images/products/kd-pd-1025/night-blue/01.png",gallery:[],
    },
  ]),

  makeProduct(8,"KD-PD-1028","Натяжная простыня из сатина","шёлк, 140×220 / 200×220 / 220×240 см",4990,[
    ...fittedSheetRows(
      "Пудровый",
      "/images/products/kd-pd-1028/powder/01.jpg",
      [
        "/images/products/kd-pd-1028/powder/02.webp",
        "/images/products/kd-pd-1028/powder/03.webp",
      ],
    ),
    ...fittedSheetRows(
      "Белый",
      "/images/products/kd-pd-1028/white/01.webp",
      ["/images/products/kd-pd-1028/white/02.webp"],
    ),
    ...fittedSheetRows(
      "Ночной синий",
      "/images/products/kd-pd-1028/night-blue/01.webp",
      ["/images/products/kd-pd-1028/night-blue/02.webp"],
    ),
  ]),

  makeProduct(11,"KD-PD-1128","Наволочка из сатина","шёлк, 60×60 см",4990,[
    {
      color:"Пудровый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"/images/products/kd-pd-1128/powder/01.webp",
      gallery:["/images/products/kd-pd-1128/powder/02.webp"],
    },
    {
      color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"/images/products/kd-pd-1128/white/01.webp",
      gallery:[
        "/images/products/kd-pd-1128/white/02.webp",
        "/images/products/kd-pd-1128/white/03.webp",
      ],
    },
    {
      color:"Ночной синий",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"/images/products/kd-pd-1128/night-blue/01.webp",
      gallery:["/images/products/kd-pd-1128/night-blue/02.webp"],
    },
  ]),
];

export const catalogProductOverrides:Record<number,CatalogProductOverride> = Object.fromEntries(
  productList.map(product=>[product.id,product])
);

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  productList.flatMap(product=>product.skus).map(item=>[item.id,item])
);
