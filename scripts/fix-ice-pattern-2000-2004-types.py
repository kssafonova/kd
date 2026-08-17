from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

catalog_2000 = '''makeProduct(2000,"KD-PD-2000","Декоративная подушка «Ледяные узоры»","хлопок, 50×50 см",5990,[
    {color:"Ледяной голубой",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-BLUE01.png",gallery:[]},
    {color:"Ночной синий",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-DARK01.png",gallery:[]},
    {color:"Белый",size:"50×50 см",height:"50 см",width:"50 см",packageInfo:"Декоративная подушка 1 шт",material:"Хлопок",composition:"Внешняя часть: 100% хлопок, наполнитель: 100% пух",details:"Декоративный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2000-WHITE01.png",gallery:[]},
  ])'''

catalog, count = re.subn(r'makeProduct\(2000,"KD-PD-2000".*?\n  \]\)', catalog_2000, catalog, count=1, flags=re.S)
if count != 1:
    raise SystemExit("KD-PD-2000 catalog entry not found")

page_2000 = '''{ id:2000, name:"Декоративная подушка «Ледяные узоры»", note:"хлопок, 50×50 см", price:5990, image:"/images/products/KD-PD-2000-BLUE01.png", colorVariants:[
    {name:"Ледяной голубой",hex:"#afcbd1",image:"/images/products/KD-PD-2000-BLUE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/images/products/KD-PD-2000-DARK01.png"},
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2000-WHITE01.png"},
  ]}'''

page, count = re.subn(r'\{ id:2000, name:.*?\n  \]\}', page_2000, page, count=1, flags=re.S)
if count != 1:
    raise SystemExit("KD-PD-2000 storefront entry not found")

catalog_2004 = '''makeProduct(2004,"KD-PD-2004","Чайная пара «Ледяные узоры»","костяной фарфор, 250 мл",6990,[
    {color:"Белый",size:"250 мл",diameter:"15 см",packageInfo:"Чашка 1 шт, блюдце 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/images/products/KD-PD-2004-WHITE01.png",gallery:[]},
  ])'''

catalog, count = re.subn(r'makeProduct\(2004,"KD-PD-2004".*?\n  \]\)', catalog_2004, catalog, count=1, flags=re.S)
if count != 1:
    raise SystemExit("KD-PD-2004 catalog entry not found")

page_2004 = '''{ id:2004, name:"Чайная пара «Ледяные узоры»", note:"костяной фарфор, 250 мл", price:6990, image:"/images/products/KD-PD-2004-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/images/products/KD-PD-2004-WHITE01.png"},
  ]}'''

page, count = re.subn(r'\{ id:2004, name:.*?\n  \]\}', page_2004, page, count=1, flags=re.S)
if count != 1:
    raise SystemExit("KD-PD-2004 storefront entry not found")

page = page.replace('"Посуда и сервировка":[5,10,2000,2001,2010]', '"Посуда и сервировка":[5,10,2001,2004,2010]', 1)
page = page.replace('"Пледы и подушки":[3,6,7,2003,2004]', '"Пледы и подушки":[3,6,7,2000,2003]', 1)

if '"Посуда и сервировка":[5,10,2001,2004,2010]' not in page:
    raise SystemExit("Could not place KD-PD-2004 in Посуда и сервировка or remove KD-PD-2000")
if '"Пледы и подушки":[3,6,7,2000,2003]' not in page:
    raise SystemExit("Could not place KD-PD-2000 in Пледы и подушки or remove KD-PD-2004")

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("Corrected KD-PD-2000 as decorative pillow and KD-PD-2004 as tea pair")
