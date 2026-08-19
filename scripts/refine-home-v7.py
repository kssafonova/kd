from pathlib import Path
import re

PAGE = Path("app/page.tsx")
text = PAGE.read_text(encoding="utf-8")

# Restore compact square category cards with imagery.
categories_pattern = r'''  const categories=\[\n[\s\S]*?\n  \];\n\n  const newProducts='''
categories_replacement = '''  const categories=[
    {title:"Постельное бельё",meta:"СПАЛЬНЯ",image:"/images/blue-bedroom.png",category:"Постельное бельё"},
    {title:"Пледы и подушки",meta:"ТЕКСТИЛЬ",image:"/images/sky-bolster.png",category:"Пледы и подушки"},
    {title:"Посуда и сервировка",meta:"СТОЛОВАЯ",image:"/images/moon-plate.png",category:"Посуда и сервировка"},
    {title:"Столовый текстиль",meta:"СЕРВИРОВКА",image:"/images/editorial-table.webp",category:"Столовый текстиль"},
    {title:"Домашняя одежда",meta:"ДЛЯ ДОМА",image:"/images/classic-bedroom.png",category:"Домашняя одежда"},
    {title:"Декор для дома",meta:"ИНТЕРЬЕР",image:"/images/beige-bedroom.png",category:"Все товары"},
    {title:"Ванная",meta:"ТЕКСТИЛЬ",image:"/images/russian-bedroom.png",category:"Все товары"},
    {title:"Подарки",meta:"ИДЕИ",image:"/images/time-collection.png",category:"Все товары"},
  ];

  const newProducts='''
if not re.search(categories_pattern, text):
    raise SystemExit("Home categories data block not found")
text = re.sub(categories_pattern, categories_replacement, text, count=1)

# Category cards: image first, concise label below. No inline arrow in each card.
old_card = '''<div id="home-category-rail" className="hv4-category-rail" aria-label="Категории товаров">{categories.map(item=><button className="hv4-category-card" type="button" key={item.title} onClick={()=>openCatalog(item.category)}><strong>{item.title}</strong><small>{item.meta}</small><Icon name="arrow"/></button>)}</div>'''
new_card = '''<div id="home-category-rail" className="hv4-category-rail" aria-label="Категории товаров">{categories.map(item=><button className="hv4-category-card" type="button" key={item.title} onClick={()=>openCatalog(item.category)}><img src={assetUrl(item.image)} alt={item.title}/><span><strong>{item.title}</strong><small>{item.meta}</small></span></button>)}</div>'''
if old_card not in text:
    raise SystemExit("Home category rail markup not found")
text = text.replace(old_card, new_card, 1)

PAGE.write_text(text, encoding="utf-8")
print("Refined homepage V7: square category cards and compact header grouping")
