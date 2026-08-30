from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

catalog_products = {
2000: '''makeProduct(2000,"KD-PD-2000","Тарелка «Ледяные узоры»","костяной фарфор, 23 см",7990,[
    {color:"Ледяной голубой",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2000-WHITE01.png",gallery:[]},
  ])''',
2001: '''makeProduct(2001,"KD-PD-2001","Чайная пара «Ледяные узоры»","костяной фарфор, 250 мл",6990,[
    {color:"Ночной синий",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2001-DARK01.png",gallery:[]},
    {color:"Белый",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2001-WHITE01.png",gallery:[]},
  ])''',
2003: '''makeProduct(2003,"KD-PD-2003","Плед «Ледяные узоры»","шерсть и хлопок, 140×200 см",12990,[
    {color:"Ледяной голубой",size:"140×200 см",height:"140 см",width:"200 см",packageInfo:"Плед 1 шт",material:"Шерсть и хлопок",composition:"70% шерсть, 30% хлопок",details:"Жаккардовый орнамент",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2003-BLUE01.png",gallery:["/assets/images/KD-PD-2003-BLUE02.png"]},
  ])''',
2004: '''makeProduct(2004,"KD-PD-2004","Декоративная подушка «Ледяные узоры»","хлопок, 50×50 см",5990,[
    {color:"Белый",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2004-WHITE01.png",gallery:[]},
  ])''',
2010: '''makeProduct(2010,"KD-PD-2010","Комплект постельного белья «Ледяные узоры»","сатин, 140×220 / 200×220 / 220×240 см",24990,[
    {color:"Белый",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:24990,image:"/assets/images/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Белый",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:27990,image:"/assets/images/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Белый",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:29990,image:"/assets/images/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Ночной синий",size:"Полуторный 140×220 см",height:"140 см",width:"220 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:24990,image:"/assets/images/KD-PD-2010-DARK01.png",gallery:[]},
    {color:"Ночной синий",size:"Евро 200×220 см",height:"200 см",width:"220 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:27990,image:"/assets/images/KD-PD-2010-DARK01.png",gallery:[]},
    {color:"Ночной синий",size:"Кинг сайз 220×240 см",height:"220 см",width:"240 см",packageInfo:"Наволочка 2 шт, простынь 1 шт, пододеяльник 1 шт",material:"Хлопок-сатин",composition:"100% хлопок-сатин",details:"Вышивка «Ледяные узоры»",collection:"Ледяные узоры",price:29990,image:"/assets/images/KD-PD-2010-DARK01.png",gallery:[]},
  ])''',
}

for product_id, replacement in catalog_products.items():
    pattern = rf'makeProduct\({product_id},"KD-PD-{product_id}".*?\n  \]\)'
    catalog, count = re.subn(pattern, replacement, catalog, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Catalog product KD-PD-{product_id} not found")

page_products = {
2000: '''{ id:2000, name:"Тарелка «Ледяные узоры»", note:"костяной фарфор, 23 см", price:7990, image:"/assets/images/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/assets/images/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/assets/images/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/assets/images/KD-PD-2000-WHITE01.png"},
  ]}''',
2001: '''{ id:2001, name:"Чайная пара «Ледяные узоры»", note:"костяной фарфор, 250 мл", price:6990, image:"/assets/images/KD-PD-2001-DARK01.png", colorVariants:[
    {name:"Ночной синий",hex:"#10233e",image:"/assets/images/KD-PD-2001-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/assets/images/KD-PD-2001-WHITE01.png"},
  ]}''',
2003: '''{ id:2003, name:"Плед «Ледяные узоры»", note:"шерсть и хлопок, 140×200 см", price:12990, image:"/assets/images/KD-PD-2003-BLUE01.png", gallery:["/assets/images/KD-PD-2003-BLUE02.png"], colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/assets/images/KD-PD-2003-BLUE01.png",gallery:["/assets/images/KD-PD-2003-BLUE02.png"]},
  ]}''',
2004: '''{ id:2004, name:"Декоративная подушка «Ледяные узоры»", note:"хлопок, 50×50 см", price:5990, image:"/assets/images/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/assets/images/KD-PD-2004-WHITE01.png"},
  ]}''',
2010: '''{ id:2010, name:"Комплект постельного белья «Ледяные узоры»", note:"сатин, 140×220 / 200×220 / 220×240 см", price:24990, image:"/assets/images/KD-PD-2010-WHITE01.png", hasRichContent:true, colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/assets/images/KD-PD-2010-WHITE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/assets/images/KD-PD-2010-DARK01.png"},
  ]}''',
}

for product_id, replacement in page_products.items():
    pattern = rf'\{{ id:{product_id}, name:.*?\n  \]\}}'
    page, count = re.subn(pattern, replacement, page, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"Storefront product KD-PD-{product_id} not found")

# Add the new blue label to the SKU color dictionaries.
for path_text_name in ("catalog",):
    pass
if '"Ледяной голубой":"#afcbd1"' not in catalog:
    catalog = catalog.replace('  "Небесный":"#9fb2c6",', '  "Небесный":"#9fb2c6",\n  "Ледяной голубой":"#afcbd1",', 1)
if '"Ледяной голубой":"ICE-BLUE"' not in catalog:
    catalog = catalog.replace('  "Небесный":"SKY",', '  "Небесный":"SKY",\n  "Ледяной голубой":"ICE-BLUE",', 1)

# Collection must contain only the new five products.
page, count = re.subn(
    r'(\{ id:"ice", name:"Ледяные узоры"[^\n]*?productIds:)\[[^\]]*\]( \},)',
    r'\1[2000,2001,2003,2004,2010]\2',
    page,
    count=1,
)
if count != 1 and "productIds:[2000,2001,2003,2004,2010]" not in page:
    raise SystemExit("Ice Patterns editorial assortment not found")

# Catalog category mapping for the new products.
category_replacements = {
    '"Посуда и сервировка":[5,10]': '"Посуда и сервировка":[5,10,2000,2001]',
    '"Постельное бельё":[2,4,8,11,12]': '"Постельное бельё":[2,4,8,11,12,2010]',
    '"Пледы и подушки":[3,6,7]': '"Пледы и подушки":[3,6,7,2003,2004]',
}
for old, new in category_replacements.items():
    if old in page:
        page = page.replace(old, new, 1)
    elif new not in page:
        raise SystemExit(f"Category mapping not found: {old}")

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Finalized Ice Patterns names, prices, specs, sizes and category mapping")
