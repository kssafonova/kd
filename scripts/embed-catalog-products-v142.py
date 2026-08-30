from __future__ import annotations

from collections import OrderedDict
from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
SOURCE = ROOT / "public" / "data" / "catalog_master.csv"
if not SOURCE.exists():
    SOURCE = ROOT / "data" / "catalog_master.csv"
OUT = APP / "catalog-products.generated.ts"
STOREFRONT = APP / "storefront-app.tsx"
HOME = APP / "home-standalone.tsx"
CATALOG_PAGE = APP / "catalog" / "page.tsx"


def clean(value):
    text = str(value or "").strip()
    return None if not text or text.lower() == "null" else text


def price(value):
    text = clean(value)
    if not text:
        return 0
    text = text.replace("\u00a0", "").replace("\u202f", "").replace(" ", "")
    text = re.sub(r"[^0-9,.-]", "", text).replace(",", ".")
    try:
        return int(round(float(text)))
    except ValueError:
        return 0


def color_hex(value):
    key = (clean(value) or "").lower().replace("ё", "е").strip()
    colors = {
        "бежевый": "#CDB99B", "белый": "#F5F5F2", "белый / голубой": "#93B8CB",
        "белый / золотой": "#B89A5A", "голубой": "#93B8CB", "небесный": "#AFC9D7",
        "желтый": "#D9B84E", "зеленый": "#657A61", "коричневый": "#765A46",
        "красный": "#9E403B", "ледяной голубой": "#93B8CB", "молочный": "#EEE7DA",
        "ночной синий": "#142A45", "прозрачный": "#F3F4F2", "пудровый": "#D8B0A4",
        "серебряный": "#B9B9B4", "серо-синий": "#667B89", "синий": "#496C8A",
        "черный": "#1D1D1B", "экрю": "#DED0B6",
    }
    return colors.get(key, "#8F8A82")


def entity_id(article: str, name: str) -> int:
    total = 0
    for char in f"{article}|{name}":
        total = ((total * 31) + ord(char)) % 500000
    return 300000 + total


def asset(value):
    image = clean(value)
    if not image:
        return None
    if image.startswith("/assets/"):
        return image
    if image.startswith("assets/"):
        return "/" + image
    return None


with SOURCE.open("r", encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle, delimiter=";")
    rows = [dict(row) for row in reader if clean(row.get("Артикул")) and clean(row.get("Название товара"))]

by_article: OrderedDict[str, list[dict]] = OrderedDict()
for row in rows:
    by_article.setdefault(clean(row.get("Артикул")) or "", []).append(row)

products = []
for article, variants in by_article.items():
    first = variants[0]
    name = clean(first.get("Название товара")) or article
    pid = entity_id(article, name)
    colors = list(dict.fromkeys(filter(None, (clean(row.get("Цвет")) for row in variants))))
    scents = list(dict.fromkeys(filter(None, (clean(row.get("Аромат")) for row in variants))))
    scent_mode = bool(scents and len(variants) > 1)
    switch_by = "scent" if scent_mode else "color" if len(colors) > 1 else "none"
    skus = []
    for index, row in enumerate(variants):
        images = [image for image in (asset(row.get("Фото 1")), asset(row.get("Фото 2")), asset(row.get("Фото 3"))) if image]
        source_color = clean(row.get("Цвет"))
        scent = clean(row.get("Аромат"))
        primary = (scent if switch_by == "scent" else source_color if switch_by == "color" else None) or "Единый вариант"
        size = clean(row.get("Размер")) or clean(row.get("Объем")) or clean(row.get("Диаметр")) or "Единый размер"
        current_price = price(row.get("Цена"))
        old_price = price(row.get("Старая цена"))
        sku = {
            "id": f"master-{pid}-{index}",
            "article": article,
            "productId": pid,
            "color": primary,
            "colorHex": color_hex(source_color or primary),
            "size": size,
            "height": clean(row.get("Высота")),
            "width": clean(row.get("Ширина")),
            "diameter": clean(row.get("Диаметр")),
            "packageInfo": clean(row.get("Комплектация / информация о размере")),
            "material": clean(row.get("Материал")) or "",
            "composition": clean(row.get("Состав")) or "",
            "details": clean(row.get("Детали")),
            "collection": clean(row.get("Коллекция")),
            "capsule": clean(row.get("Капсула")),
            "price": current_price,
            "image": images[0] if images else "/assets/images/image-placeholder.svg",
            "gallery": images[1:],
            "available": True,
            "volume": clean(row.get("Объем")),
            "oldPrice": old_price if old_price > current_price else None,
            "sourceColor": source_color,
            "scent": scent,
        }
        skus.append({key: value for key, value in sku.items() if value is not None})

    priced = [sku for sku in skus if sku["price"] > 0]
    min_sku = min(priced, key=lambda item: item["price"]) if priced else skus[0]
    first_sku = skus[0]
    switch_rows = []
    seen_primary = set()
    for sku in skus:
        if sku["color"] in seen_primary:
            continue
        seen_primary.add(sku["color"])
        switch_rows.append(sku)
    note = ", ".join(filter(None, [clean(first_sku.get("material")), clean(first_sku.get("size"))]))
    product = {
        "id": pid,
        "name": name,
        "article": article,
        "note": note,
        "price": min_sku["price"],
        "oldPrice": min_sku.get("oldPrice"),
        "image": first_sku["image"],
        "gallery": first_sku["gallery"],
        "skus": skus,
        "colorVariants": [
            {"name": sku["color"], "hex": sku["colorHex"], "image": sku["image"], "gallery": sku["gallery"]}
            for sku in switch_rows
        ],
        "category": clean(first.get("Категория")),
        "subcategory": clean(first.get("Подкатегория")),
        "collection": clean(first.get("Коллекция")),
        "capsule": clean(first.get("Капсула")),
        "readySolution": clean(first.get("Товар входит в готовое решение")),
        "optionalReadySolution": clean(first.get("Опционально входит в готовое решение")),
        "switchBy": switch_by,
    }
    products.append({key: value for key, value in product.items() if value is not None})

payload = json.dumps(products, ensure_ascii=False, separators=(",", ":"))
OUT.write_text(
    "/* AUTO-GENERATED from public/data/catalog_master.csv. Do not edit manually. */\n"
    f"export const CATALOG_PRODUCTS_GENERATED = {payload} as const;\n",
    encoding="utf-8",
)

text = STOREFRONT.read_text(encoding="utf-8")
import_marker = 'import { catalogProductOverrides, type CatalogSku } from "./catalog-data";\n'
if 'CATALOG_PRODUCTS_GENERATED' not in text and import_marker in text:
    text = text.replace(import_marker, import_marker + 'import { CATALOG_PRODUCTS_GENERATED } from "./catalog-products.generated";\n', 1)

product_marker = ').filter(product=>!REMOVED_PRODUCT_IDS.has(product.id));\n\n\ntype CatalogMasterRow'
if 'products = CATALOG_PRODUCTS_GENERATED' not in text and product_marker in text:
    text = text.replace(
        product_marker,
        ').filter(product=>!REMOVED_PRODUCT_IDS.has(product.id));\nif(CATALOG_PRODUCTS_GENERATED.length)products = CATALOG_PRODUCTS_GENERATED as unknown as Product[];\n\n\ntype CatalogMasterRow',
        1,
    )

text = text.replace('let catalogMasterLoaded = false;', 'let catalogMasterLoaded = CATALOG_PRODUCTS_GENERATED.length>0;', 1)
text = text.replace('useState(()=>catalogMasterLoaded&&products.length>0)', 'useState(()=>products.length>0)', 1)

# Keep selected product valid even if the data source is temporarily empty.
text = text.replace('const [selected, setSelected] = useState<Product>(products[1]);', 'const [selected, setSelected] = useState<Product>(()=>products[1]??products[0]??({id:0,name:"",note:"",price:0,image:"/assets/images/image-placeholder.svg"} as Product));', 1)

# Auto-center the selected category in the horizontal slider after a switch.
category_effect_marker = '  useEffect(()=>{\n    if(!filterOpen||typeof document==="undefined")return;\n'
if 'catalog-category-slider-v141 button.active' not in text and category_effect_marker in text:
    text = text.replace(
        category_effect_marker,
        '  useEffect(()=>{if(typeof document==="undefined")return;requestAnimationFrame(()=>document.querySelector<HTMLElement>(".view-catalog .catalog-category-slider-v141 button.active")?.scrollIntoView({block:"nearest",inline:"center",behavior:"smooth"}))},[category]);\n\n' + category_effect_marker,
        1,
    )

STOREFRONT.write_text(text, encoding="utf-8")

# One query contract for all header actions: ?open=...
home_text = HOME.read_text(encoding="utf-8")
home_text = home_text.replace('/catalog/?search=open', '/catalog/?open=search')
home_text = home_text.replace('/catalog/?account=open', '/catalog/?open=account')
home_text = home_text.replace('/catalog/?favorites=open', '/catalog/?open=favorites')
home_text = home_text.replace('/catalog/?cart=open', '/catalog/?open=cart')
HOME.write_text(home_text, encoding="utf-8")

# Runtime CSV is now a fallback/debug source, not a render blocker. No preload needed.
CATALOG_PAGE.write_text('''import CatalogClient from "./catalog-client";\n\nexport default function CatalogPage(){\n  return <CatalogClient />;\n}\n''', encoding="utf-8")

print(f"Embedded {len(products)} grouped catalog products from {len(rows)} CSV rows; catalog renders without runtime CSV wait")
