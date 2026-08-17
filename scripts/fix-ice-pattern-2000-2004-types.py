from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

# CANONICAL ICE PATTERNS PRODUCT MAP
# 2000 decorative pillow / 2001 plate / 2003 plaid / 2004 tea pair / 2010 salad bowl

catalog_products = {
2000: '''makeProduct(2000,"KD-PD-2000","Декоративная подушка «Ледяные узоры»","хлопок, 50×50 см",5990,[
    {color:"Ледяной голубой",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-WHITE01.png",gallery:[]},
  ])''',
2001: '''makeProduct(2001,"KD-PD-2001","Тарелка «Ледяные узоры»","костяной фарфор, 23 см",7990,[
    {color:"Ночной синий",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-DARK01.png",gallery:[]},
    {color:"Белый",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-WHITE01.png",gallery:[]},
  ])''',
2003: '''makeProduct(2003,"KD-PD-2003","Плед «Ледяные узоры»","шерсть и хлопок, 140×200 см",12990,[
    {color:"Ледяной голубой",size:"140×200 см",height:"140 см",width:"200 см",packageInfo:"Плед 1 шт",material:"Шерсть и хлопок",composition:"70% шерсть, 30% хлопок",details:"Жаккардовый орнамент",collection:"Ледяные узоры",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ])''',
2004: '''makeProduct(2004,"KD-PD-2004","Чайная пара «Ледяные узоры»","костяной фарфор, 250 мл",6990,[
    {color:"Белый",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2004-WHITE01.png",gallery:[]},
  ])''',
2010: '''makeProduct(2010,"KD-PD-2010","Салатник «Ледяные узоры»","костяной фарфор, 24 см",9990,[
    {color:"Белый",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Ночной синий",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2010-DARK01.png",gallery:[]},
  ])''',
}

for product_id, replacement in catalog_products.items():
    catalog, count = re.subn(
        rf'makeProduct\({product_id},"KD-PD-{product_id}".*?\n  \]\)',
        replacement,
        catalog,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"KD-PD-{product_id} catalog entry not found")

page_products = {
2000: '''{ id:2000, name:"Декоративная подушка «Ледяные узоры»", note:"хлопок, 50×50 см", price:5990, image:"/images/products/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2000-WHITE01.png"},
  ]}''',
2001: '''{ id:2001, name:"Тарелка «Ледяные узоры»", note:"костяной фарфор, 23 см", price:7990, image:"/images/products/KD-PD-2001-DARK01.png", colorVariants:[
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2001-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2001-WHITE01.png"},
  ]}''',
2003: '''{ id:2003, name:"Плед «Ледяные узоры»", note:"шерсть и хлопок, 140×200 см", price:12990, image:"/images/products/KD-PD-2003-BLUE01.png", gallery:["/images/products/KD-PD-2003-BLUE02.png"], colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2003-BLUE01.png",gallery:["/images/products/KD-PD-2003-BLUE02.png"]},
  ]}''',
2004: '''{ id:2004, name:"Чайная пара «Ледяные узоры»", note:"костяной фарфор, 250 мл", price:6990, image:"/images/products/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2004-WHITE01.png"},
  ]}''',
2010: '''{ id:2010, name:"Салатник «Ледяные узоры»", note:"костяной фарфор, 24 см", price:9990, image:"/images/products/KD-PD-2010-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2010-WHITE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2010-DARK01.png"},
  ]}''',
}

for product_id, replacement in page_products.items():
    page, count = re.subn(
        rf'\{{ id:{product_id}, name:.*?\n  \]\}}',
        replacement,
        page,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"KD-PD-{product_id} storefront entry not found")

# Keep exact current category placement regardless of previous patch order.
category_mapping = '''  const categoryProductIds:Record<string,number[]>={
    "Все товары":products.map(product=>product.id),
    "Посуда и сервировка":[5,10,2001,2004,2010],
    "Постельное бельё":[2,4,8,11,12],
    "Пледы и подушки":[3,6,7,2000,2003],
    "Домашняя одежда":[],
    "Столовый текстиль":[],
  };'''
page, count = re.subn(
    r'  const categoryProductIds:Record<string,number\[\]>=\{.*?\n  \};',
    category_mapping,
    page,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit("Catalog category mapping block not found")

page, count = re.subn(
    r'(\{ id:"ice", name:"Ледяные узоры"[^\n]*?productIds:)\[[^\]]*\]( \},)',
    r'\1[2000,2001,2003,2004,2010]\2',
    page,
    count=1,
)
if count != 1 and 'productIds:[2000,2001,2003,2004,2010]' not in page:
    raise SystemExit("Ice Patterns editorial assortment not found")

if '"Ледяной голубой":"#afcbd1"' not in catalog:
    catalog = catalog.replace('  "Небесный":"#9fb2c6",', '  "Небесный":"#9fb2c6",\n  "Ледяной голубой":"#afcbd1",', 1)
if '"Ледяной голубой":"ICE-BLUE"' not in catalog:
    catalog = catalog.replace('  "Небесный":"SKY",', '  "Небесный":"SKY",\n  "Ледяной голубой":"ICE-BLUE",', 1)

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Canonical Ice Patterns: 2000 pillow, 2001 plate, 2003 plaid, 2004 tea pair, 2010 salad bowl")
