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
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000dcb081f78263e374de7b6c4e&ts=496365&p=fs&cid=1&sig=6578dc64f0b53f1732153f68ee757b46979668d4313ce38d97de8a51d266071e&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_000000005344822f8042779ff6d3f96a&ts=496365&p=fs&cid=1&sig=73cf2755209b7b3a47854a151c12f102ede9516074c7c8e7cdc8eeeda8b1aa96&v=0"],
    },
    {
      color:"Молочный",size:"60×60 см",height:"60 см",width:"60 см",
      material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000c078822f90b12fee221ddc89&ts=496365&p=fs&cid=1&sig=dc241ae6d68adbd034fe4e666f23c697435cec3e9d7669167044015b74f6547c&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_000000009e88822f8fd120274c5dba60&ts=496365&p=fs&cid=1&sig=512bf3d6c408c19af8c393afc1bb61741922dd4c7ebebef5d94129babecdd73b&v=0"],
    },
    {
      color:"Синий",size:"60×60 см",height:"60 см",width:"60 см",
      material:"Хлопок",composition:"Внешняя часть: 100% Хлопок, Наполнитель: 100% Пух",details:"Кружево",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000007038822f97a7d1db2709bbd0&ts=496365&p=fs&cid=1&sig=46b7b595c9c585d2c8a22a053bf244fd312426e6f471060e846f8bedc111abc2&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_0000000029b0822f90fcd9855aa6af2a&ts=496365&p=fs&cid=1&sig=0cc2fada5e957a070af96e96f66cd666eb17c972e1b13c6d3a02f6b507307a72&v=0"],
    },
  ]),

  makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",9990,[
    {
      color:"Белый",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000d9bc820a84447e7575174cb8&ts=496365&p=fs&cid=1&sig=976f6f59703b90f6fccca3ba4defa6e3b1a1dc5f1b978de7bcc01f090eebda57&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000a33881f493e13ee993826095&ts=496365&p=fs&cid=1&sig=588a9a9c742506231b6f6cc2ca79a1acdced65f27c3d7e756e274fc761ec9c17&v=0"],
    },
    {
      color:"Молочный",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000001c6081f495c62eed4fb5e8ef&ts=496365&p=fs&cid=1&sig=4b3e920e75783cb348d056c8cee6e0294398e1698d8bc733d1cbf5a4538b1ff5&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_000000006b3481f4a0213cecee3990a9&ts=496365&p=fs&cid=1&sig=53c9b13ef6054b706d62fb733b41fccc9ed5da995eb43f075d3409613b6ecdb3&v=0"],
    },
    {
      color:"Синий",size:"200×220 см",height:"200 см",width:"220 см",
      material:"Хлопок",composition:"70% хлопок, 30% лен",details:"Кружево",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000001ca881f49fee9cbdb71cccf5&ts=496365&p=fs&cid=1&sig=297ad3c9482d3a051f3c4f12997b743010d909eb2f64eeb309a8c420ac50bb1c&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000d80081f4b377cbc8658defae&ts=496365&p=fs&cid=1&sig=9ccd572e5a946ff63dafa9b87df8988e4bb8ac13b4c51d4839b8ce4fdcf27c92&v=0"],
    },
  ]),

  makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",12990,[
    {
      color:"Молочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000007db481f487c330f8e25d5da8&ts=496365&p=fs&cid=1&sig=842bfd64633f741eeb80d595beeaf9f4fe9335a31c23a4dbaf8d560b5ed972ff&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000d89c81f4980fc919b036ce49&ts=496365&p=fs&cid=1&sig=a64711e38f73fabff9acbed4c18caf0f00fa472f9d30ad3d0532f4487d13dfeb&v=0"],
    },
    {
      color:"Молочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000007db481f487c330f8e25d5da8&ts=496365&p=fs&cid=1&sig=842bfd64633f741eeb80d595beeaf9f4fe9335a31c23a4dbaf8d560b5ed972ff&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000d89c81f4980fc919b036ce49&ts=496365&p=fs&cid=1&sig=a64711e38f73fabff9acbed4c18caf0f00fa472f9d30ad3d0532f4487d13dfeb&v=0"],
    },
    {
      color:"Песочный",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000396881f4abc3cf0a7ea2e5c3&ts=496365&p=fs&cid=1&sig=234033a1986c7409936db6c3a15464de82354714580a87536db1429d33dca0f0&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000d1cc81f4b4b21ea4b809fd8a&ts=496365&p=fs&cid=1&sig=fcc2cc2b6aeed3c4f763b6bf881e00dc771664cc791f65ff71f01903d9d7488f&v=0"],
    },
    {
      color:"Песочный",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Покрывало 1 шт",
      material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000396881f4abc3cf0a7ea2e5c3&ts=496365&p=fs&cid=1&sig=234033a1986c7409936db6c3a15464de82354714580a87536db1429d33dca0f0&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000d1cc81f4b4b21ea4b809fd8a&ts=496365&p=fs&cid=1&sig=fcc2cc2b6aeed3c4f763b6bf881e00dc771664cc791f65ff71f01903d9d7488f&v=0"],
    },
  ]),

  makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",4490,[
    {
      color:"Ночной синий",size:"250 мл",diameter:"15 см",packageInfo:"Кружка 1 шт, Блюдце 1 шт",
      material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",
      image:"/images/time-tea-pair.png",gallery:[],
    },
  ]),

  makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",20990,
    satinSizes.map(size=>({
      ...size,color:"Ночной синий",packageInfo:"Наволочка 2 шт, Простынь 1 шт, Пододеяльник 1 шт",
      material:"Шелк",composition:"100% Сатин",details:"Вышивка",collection:"Лунная сказка",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000fc0c824683f04eafcb7bbf0f&ts=496366&p=fs&cid=1&sig=a4db082beaa947abe6dc1f2fb2e0c6e92ae4e9e27ff3ddac1d54bab0cbb00982&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_000000007b1082438e369a82084b9709&ts=496366&p=fs&cid=1&sig=6ce85558f2b6e1446bf2cedaf5b438363b88381b8facbaa740f4cb0876b123df&v=0"],
    }))
  ),

  makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",4990,[
    {
      color:"Ночной синий",size:"23 см",diameter:"23 см",
      material:"Фарфор",composition:"100% костяной фарфор",details:"Рисунок",collection:"Лунная сказка",
      image:"/images/moon-plate.png",gallery:[],
    },
  ]),

  makeProduct(8,"KD-PD-1028","Натяжная простыня из сатина","шёлк, 140×220 / 200×220 / 220×240 см",4990,[
    ...fittedSheetRows(
      "Пудровый",
      "/images/peach-sheet.jpg",
      [
        "https://chatgpt.com/backend-api/estuary/content?id=file_0000000040a8820aa80cad3bae1089d1&ts=496367&p=fs&cid=1&sig=55d219d2b6d157506aabd67555f000c3469d3cc99433b95af6e9f34eea374c53&v=0",
        "https://chatgpt.com/backend-api/estuary/content?id=file_00000000366881f4a91c0578cb18e10d&ts=496367&p=fs&cid=1&sig=c56e8415a364844e90b365e64df64d05f8adf8a321579808deeea4fa31ef8765&v=0",
      ],
    ),
    ...fittedSheetRows(
      "Белый",
      "https://chatgpt.com/backend-api/estuary/content?id=file_00000000d2dc8243aaa2a927cf4f5633&ts=496367&p=fs&cid=1&sig=54ff8e7bf8fe59392ed21f4bfa59bed24c4d9bdb4dd563a713e3d0cc0443754c&v=0",
      ["https://chatgpt.com/backend-api/estuary/content?id=file_00000000ce18820a8e723075d09ca308&ts=496367&p=fs&cid=1&sig=c903e912b802253d1e36d0e2118040e04d02f458951b7763cc5becdb8fde1632&v=0"],
    ),
    ...fittedSheetRows(
      "Ночной синий",
      "https://chatgpt.com/backend-api/estuary/content?id=file_00000000f40c82438807d0c7873fb3f8&ts=496367&p=fs&cid=1&sig=41bd9b7d131409cfa5ce4204d39571d81f31ef7ac46bbfa2e9e4d790cf911d36&v=0",
      ["https://chatgpt.com/backend-api/estuary/content?id=file_00000000320c820a933dd67d68e30d69&ts=496367&p=fs&cid=1&sig=8d6bd857ce896465feb5f38ef575db7a841d6911641f63bd340cda4b83450f2c&v=0"],
    ),
  ]),

  makeProduct(11,"KD-PD-1128","Наволочка из сатина","шёлк, 60×60 см",4990,[
    {
      color:"Пудровый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_000000009f008246956bd66ed828cfcb&ts=496367&p=fs&cid=1&sig=55bf3ae164dcaa893256b903e1253f3f7a608a9457c9ae1ad9d3f0faf13bf956&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000366881f4a91c0578cb18e10d&ts=496367&p=fs&cid=1&sig=c56e8415a364844e90b365e64df64d05f8adf8a321579808deeea4fa31ef8765&v=0"],
    },
    {
      color:"Белый",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000fbc081f4be767e97e54efcc0&ts=496367&p=fs&cid=1&sig=2ac8f8cd131625891e1c7b368ca4f84739fddca4e415dd4f6b096912e7f86755&v=0",
      gallery:[
        "https://chatgpt.com/backend-api/estuary/content?id=file_000000003ef081f4b1974cafd62a14b3&ts=496367&p=fs&cid=1&sig=2f19475fc9e0bda730bd83224b63a80676a9609114cd27eb24edfecfc65527e9&v=0",
        "https://chatgpt.com/backend-api/estuary/content?id=file_0000000035a881f48fff4e4fb2dd4a18&ts=496367&p=fs&cid=1&sig=82d4a35b1b87e919f937af583b6066194e17834d5e612b909d5b77386cb24171&v=0",
      ],
    },
    {
      color:"Ночной синий",size:"60×60 см",height:"60 см",width:"60 см",packageInfo:"Наволочка 2 шт",
      material:"Шелк",composition:"100% Сатин",
      image:"https://chatgpt.com/backend-api/estuary/content?id=file_00000000dbf0820aacb64a8fb5320501&ts=496367&p=fs&cid=1&sig=00bb12940a292875631ccf49099ae572a970af3692128d41799ba8b78a542b87&v=0",
      gallery:["https://chatgpt.com/backend-api/estuary/content?id=file_00000000734481f4a1bb0849f7b4b525&ts=496367&p=fs&cid=1&sig=f31fa81063aee8235cc793b589de1efc16a9277f6385b605820bd1294483c9ab&v=0"],
    },
  ]),
];

export const catalogProductOverrides:Record<number,CatalogProductOverride> = Object.fromEntries(
  productList.map(product=>[product.id,product])
);

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  productList.flatMap(product=>product.skus).map(item=>[item.id,item])
);
