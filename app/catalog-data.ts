export type CatalogSku = {
  id:string;
  article:string;
  productId:number;
  color:string;
  colorHex:string;
  size:string;
  height:string;
  width:string;
  material:string;
  composition:string;
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

export const catalogProductOverrides:Record<number,CatalogProductOverride> = {
  3:{
    id:3,
    article:"KD-PD-1023",
    name:"Подушка с кружевом",
    note:"хлопок, 60×60 см",
    skus:[
      {id:"KD-PD-1023-WHITE-60X60",article:"KD-PD-1023",productId:3,color:"Белый",colorHex:"#f7f7f4",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% хлопок; Наполнитель: 100% пух",price:2990,image:"/images/zip-product-bed.png",gallery:["/images/classic-bedroom.png"]},
      {id:"KD-PD-1023-MILK-60X60",article:"KD-PD-1023",productId:3,color:"Молочный",colorHex:"#e9e1d2",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% хлопок; Наполнитель: 100% пух",price:2990,image:"/images/beige-bedroom.png",gallery:["/images/russian-bedroom.png"]},
      {id:"KD-PD-1023-BLUE-60X60",article:"KD-PD-1023",productId:3,color:"Синий",colorHex:"#8ba7c0",size:"60×60 см",height:"60 см",width:"60 см",material:"Хлопок",composition:"Внешняя часть: 100% хлопок; Наполнитель: 100% пух",price:2990,image:"/images/blue-bedroom.png",gallery:["/images/zip-collection-night.png"]}
    ]
  },
  6:{
    id:6,
    article:"KD-PD-1026",
    name:"Плед из кружева",
    note:"хлопок, 200×220 см",
    skus:[
      {id:"KD-PD-1026-WHITE-200X220",article:"KD-PD-1026",productId:6,color:"Белый",colorHex:"#f7f7f4",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок; 30% лён",price:9990,image:"/images/zip-product-bed.png",gallery:["/images/classic-bedroom.png"]},
      {id:"KD-PD-1026-MILK-200X220",article:"KD-PD-1026",productId:6,color:"Молочный",colorHex:"#e9e1d2",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок; 30% лён",price:9990,image:"/images/beige-bedroom.png",gallery:["/images/russian-bedroom.png"]},
      {id:"KD-PD-1026-BLUE-200X220",article:"KD-PD-1026",productId:6,color:"Синий",colorHex:"#8ba7c0",size:"200×220 см",height:"200 см",width:"220 см",material:"Хлопок",composition:"70% хлопок; 30% лён",price:9990,image:"/images/blue-bedroom.png",gallery:["/images/zip-collection-night.png"]}
    ]
  },
  7:{
    id:7,
    article:"KD-PD-1027",
    name:"Стёганое покрывало «Бархатный ритм»",
    note:"микровелюр, 200×220 / 220×240 см",
    skus:[
      {id:"KD-PD-1027-MILK-EURO-200X220",article:"KD-PD-1027",productId:7,color:"Молочный",colorHex:"#e8dfcf",size:"Евро 200×220 см",height:"200 см",width:"220 см",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:12990,image:"/images/beige-quilt.jpg",gallery:["/images/classic-bedroom.png"]},
      {id:"KD-PD-1027-MILK-KING-220X240",article:"KD-PD-1027",productId:7,color:"Молочный",colorHex:"#e8dfcf",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,image:"/images/beige-quilt.jpg",gallery:["/images/classic-bedroom.png"]},
      {id:"KD-PD-1027-SAND-EURO-200X220",article:"KD-PD-1027",productId:7,color:"Песочный",colorHex:"#c9ad88",size:"Евро 200×220 см",height:"200 см",width:"220 см",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:12990,image:"/images/beige-bedroom.png",gallery:["/images/beige-quilt.jpg"]},
      {id:"KD-PD-1027-SAND-KING-220X240",article:"KD-PD-1027",productId:7,color:"Песочный",colorHex:"#c9ad88",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",material:"Микровелюр",composition:"Внешняя часть: 100% микровелюр; Наполнитель: 100% полиэфирное волокно",price:14990,image:"/images/beige-bedroom.png",gallery:["/images/beige-quilt.jpg"]}
    ]
  }
};

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  Object.values(catalogProductOverrides)
    .flatMap(product=>product.skus)
    .map(item=>[item.id,item])
);
