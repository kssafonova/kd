from pathlib import Path
import re

PAGE = Path("app/page.tsx")
CATALOG = Path("app/catalog-data.ts")

catalog = CATALOG.read_text(encoding="utf-8")

catalog_replacements = {
    'makeProduct(3,"KD-PD-1023","Подушка с кружевом","хлопок, 60×60 см",2990,[':
        'makeProduct(3,"KD-PD-1023","Подушка с кружевом","хлопок, 60×60 см",5990,[',
    'makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",9990,[':
        'makeProduct(6,"KD-PD-1026","Плед из кружева","хлопок, 200×220 см",12990,[',
    'makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",12990,[':
        'makeProduct(7,"KD-PD-1027","Стёганое покрывало «Бархатный ритм»","микровелюр, 200×220 / 220×240 см",8690,[',
    'price:14990,image:"/kd/assets/images/KD-PD-1027-MOL01.png"':
        'price:9990,image:"/kd/assets/images/KD-PD-1027-MOL01.png"',
    'price:14990,image:"/kd/assets/images/KD-PD-1027-PES01.png"':
        'price:9990,image:"/kd/assets/images/KD-PD-1027-PES01.png"',
    'makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",4490,[':
        'makeProduct(10,"KD-PD-1030","Чайная пара «Лунная сказка»","фарфор, 250 мл",6990,[',
    'makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",20990,[':
        'makeProduct(4,"KD-PD-1024","Комплект постельного белья «Лунная сказка»","шёлк, 140×220 / 200×220 / 220×240 см",24990,[',
    'makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",4990,[':
        'makeProduct(5,"KD-PD-1025","Тарелка «Лунная сказка»","фарфор, 23 см",5990,[',
}
for old, new in catalog_replacements.items():
    catalog = catalog.replace(old, new)

CATALOG.write_text(catalog, encoding="utf-8")

page = PAGE.read_text(encoding="utf-8")

base_patterns = [
    (r'\{ id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: 5990, image:'),
    (r'\{ id: 4, name: "Комплект «Нити времени»", note: "сатин, вышивка", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 4, name: "Комплект «Нити времени»", note: "сатин, вышивка", price: 24990, image:'),
    (r'\{ id: 5, name: "Тарелка «Лунная сказка»", note: "фарфор, ручная роспись", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 5, name: "Тарелка «Лунная сказка»", note: "фарфор, ручная роспись", price: 5990, image:'),
    (r'\{ id: 6, name: "Плед из льна и хлопка", note: "140×200 см", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 6, name: "Плед из льна и хлопка", note: "140×200 см", price: 12990, image:'),
    (r'\{ id: 7, name: "Стёганое покрывало «Бархатный ритм»", note: "бархат, 220×240 см", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 7, name: "Стёганое покрывало «Бархатный ритм»", note: "бархат, 220×240 см", price: 8690, oldPrice: 12990, image:'),
    (r'\{ id: 10, name: "Чайная пара «Нити времени»", note: "костяной фарфор, 250 мл", price: \d+(?:, oldPrice: \d+)?, image:',
     '{ id: 10, name: "Чайная пара «Нити времени»", note: "костяной фарфор, 250 мл", price: 6990, image:'),
]
for pattern, replacement in base_patterns:
    page = re.sub(pattern, replacement, page, count=1)

# Handmade badges stay on the Product after catalog SKU overrides are merged.
page = page.replace(
    '{ id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: 5990, image:',
    '{ id: 3, name: "Подушка с кружевом", note: "лён, 50×50 см", price: 5990, image:',
    1,
)
page = re.sub(
    r'(\{ id: 3, name: "Подушка с кружевом"[^\n]*?image: "[^"]+",)(?! badge:)',
    r'\1 badge: "РУЧНАЯ РАБОТА",',
    page,
    count=1,
)
page = re.sub(
    r'(\{ id: 6, name: "Плед из льна и хлопка"[^\n]*?image: "[^"]+",)(?! badge:)',
    r'\1 badge: "РУЧНАЯ РАБОТА",',
    page,
    count=1,
)

# Product cards: prefix prices with “от” when a product has multiple sizes.
old_card = '''  const discount=discountOf(product);\n  return <article className="product-card">'''
new_card = '''  const discount=discountOf(product);\n  const hasMultipleSizes=Boolean(product.skus&&new Set(product.skus.map(item=>item.size)).size>1);\n  return <article className="product-card">'''
page = page.replace(old_card, new_card, 1)
page = page.replace(
    '<span className={`price ${discount?"sale-price":""}`}>{fmt(product.price)} {product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</span>',
    '<span className={`price ${discount?"sale-price":""}`}>{hasMultipleSizes?"от ":""}{fmt(product.price)} {product.oldPrice&&<><del>{hasMultipleSizes?"от ":""}{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}</span>',
    1,
)

# PDP: old price gets “от” before a size is selected.
page = page.replace(
    '{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}',
    '{product.oldPrice&&<><del>{sizes.length>1&&!selectedSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discountOf(product)}%</mark></>}',
    1,
)

# PLP quick-add: same treatment for the crossed-out price.
page = page.replace(
    '{product.oldPrice&&<><del>{fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}',
    '{product.oldPrice&&<><del>{sizes.length>1&&!chosenSize?`от ${fmt(product.oldPrice)}`:fmt(product.oldPrice)}</del><mark>−{discount}%</mark></>}',
    1,
)

PAGE.write_text(page, encoding="utf-8")
print("Applied product pricing, sale presentation and handmade badges")
