from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

page = PAGE.read_text(encoding="utf-8")
catalog = CATALOG.read_text(encoding="utf-8")

catalog_replacement = '''makeProduct(2010,"KD-PD-2010","Салатник «Ледяные узоры»","костяной фарфор, 24 см",9990,[
    {color:"Белый",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Рельефный орнамент «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2010-WHITE01.png",gallery:[]},
    {color:"Ночной синий",size:"24 см",diameter:"24 см",packageInfo:"Салатник 1 шт",material:"Фарфор",composition:"100% костяной фарфор",details:"Деколь с орнаментом «Ледяные узоры»",collection:"Ледяные узоры",image:"/assets/images/KD-PD-2010-DARK01.png",gallery:[]},
  ])'''

catalog, count = re.subn(
    r'makeProduct\(2010,"KD-PD-2010".*?\n  \]\)',
    catalog_replacement,
    catalog,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit("KD-PD-2010 catalog entry not found")

page_replacement = '''{ id:2010, name:"Салатник «Ледяные узоры»", note:"костяной фарфор, 24 см", price:9990, image:"/assets/images/KD-PD-2010-WHITE01.png", colorVariants:[
    {name:"Белый",hex:"#f7f7f4",image:"/assets/images/KD-PD-2010-WHITE01.png"},
    {name:"Ночной синий",hex:"#10233e",image:"/assets/images/KD-PD-2010-DARK01.png"},
  ]}'''

page, count = re.subn(
    r'\{ id:2010, name:.*?\n  \]\}',
    page_replacement,
    page,
    count=1,
    flags=re.S,
)
if count != 1:
    raise SystemExit("KD-PD-2010 storefront entry not found")

# Move the product from bedding to tableware in the strict PLP mapping.
page = page.replace(
    '"Посуда и сервировка":[5,10,2000,2001]',
    '"Посуда и сервировка":[5,10,2000,2001,2010]',
    1,
)
page = page.replace(
    '"Постельное бельё":[2,4,8,11,12,2010]',
    '"Постельное бельё":[2,4,8,11,12]',
    1,
)

# Also support a build where category mapping was already corrected earlier.
if '"Посуда и сервировка":[5,10,2000,2001,2010]' not in page:
    raise SystemExit("Could not add KD-PD-2010 to Посуда и сервировка")
if '"Постельное бельё":[2,4,8,11,12,2010]' in page:
    raise SystemExit("KD-PD-2010 is still present in Постельное бельё")

CATALOG.write_text(catalog, encoding="utf-8")
PAGE.write_text(page, encoding="utf-8")
print("KD-PD-2010 corrected: Салатник «Ледяные узоры», 24 см, 9 990 ₽")
