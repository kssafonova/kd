from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

# FINAL ICE PATTERNS TYPE MAP
# 2000 decorative pillow / 2001 plate / 2003 plaid / 2004 tea pair / 2010 salad bowl

catalog_2000 = '''makeProduct(2000,"KD-PD-2000","Декоративная подушка «Ледяные узоры»","хлопок, 50×50 см",5990,[
    {color:"Ледяной голубой",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-WHITE01.png",gallery:[]},
  ])'''

catalog_2001 = '''makeProduct(2001,"KD-PD-2001","Тарелка «Ледяные узоры»","костяной фарфор, 23 см",7990,[
    {color:"Ночной синий",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-DARK01.png",gallery:[]},
    {color:"Белый",size:"23 см",diameter:"23 см",packageInfo:"Тарелка 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2001-WHITE01.png",gallery:[]},
  ])'''

catalog_2004 = '''makeProduct(2004,"KD-PD-2004","Чайная пара «Ледяные узоры»","костяной фарфор, 250 мл",6990,[
    {color:"Белый",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2004-WHITE01.png",gallery:[]},
  ])'''

for product_id, replacement in ((2000,catalog_2000),(2001,catalog_2001),(2004,catalog_2004)):
    catalog, count = re.subn(rf'makeProduct\({product_id},"KD-PD-{product_id}".*?\n  \]\)', replacement, catalog, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"KD-PD-{product_id} catalog entry not found")

page_2000 = '''{ id:2000, name:"Декоративная подушка «Ледяные узоры»", note:"хлопок, 50×50 см", price:5990, image:"/images/products/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2000-WHITE01.png"},
  ]}'''

page_2001 = '''{ id:2001, name:"Тарелка «Ледяные узоры»", note:"костяной фарфор, 23 см", price:7990, image:"/images/products/KD-PD-2001-DARK01.png", colorVariants:[
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2001-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2001-WHITE01.png"},
  ]}'''

page_2004 = '''{ id:2004, name:"Чайная пара «Ледяные узоры»", note:"костяной фарфор, 250 мл", price:6990, image:"/images/products/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2004-WHITE01.png"},
  ]}'''

for product_id, replacement in ((2000,page_2000),(2001,page_2001),(2004,page_2004)):
    page, count = re.subn(rf'\{{ id:{product_id}, name:.*?\n  \]\}}', replacement, page, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"KD-PD-{product_id} storefront entry not found")

page = page.replace('"Посуда и сервировка":[5,10,2000,2001,2010]', '"Посуда и сервировка":[5,10,2001,2004,2010]', 1)
page = page.replace('"Пледы и подушки":[3,6,7,2003,2004]', '"Пледы и подушки":[3,6,7,2000,2003]', 1)

if '"Посуда и сервировка":[5,10,2001,2004,2010]' not in page:
    raise SystemExit("Final tableware mapping is incorrect")
if '"Пледы и подушки":[3,6,7,2000,2003]' not in page:
    raise SystemExit("Final plaids and pillows mapping is incorrect")
if 'makeProduct(2003,"KD-PD-2003","Плед «Ледяные узоры»"' not in catalog:
    raise SystemExit("KD-PD-2003 must remain a plaid")
if 'makeProduct(2010,"KD-PD-2010","Салатник «Ледяные узоры»"' not in catalog:
    raise SystemExit("KD-PD-2010 must remain a salad bowl")

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Final Ice Patterns mapping: 2000 pillow, 2001 plate, 2003 plaid, 2004 tea pair, 2010 salad bowl")
