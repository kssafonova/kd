from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import re
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
CATALOG = DATA / "catalog_master.csv"
OUT = DATA / "filter-database"

NULLS = {"", "null", "none", "nan"}
FILTER_VERSION = "1.0"


def clean(value: object) -> str:
    text = str(value or "").strip().replace("\ufeff", "")
    return "" if text.lower() in NULLS else text


def norm(value: object) -> str:
    text = clean(value).lower().replace("ё", "е")
    text = text.replace("х", "×").replace("x", "×")
    text = re.sub(r"\s*×\s*", "×", text)
    text = re.sub(r"\s*/\s*", " / ", text)
    return re.sub(r"\s+", " ", text).strip()


def pretty(value: object) -> str:
    text = clean(value)
    if not text:
        return ""
    if text == text.lower():
        return text[:1].upper() + text[1:]
    return text


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha1(norm(value).encode('utf-8')).hexdigest()[:10]}"


TRANSLIT = str.maketrans({
    "а":"a","б":"b","в":"v","г":"g","д":"d","е":"e","ё":"e","ж":"zh","з":"z","и":"i","й":"y",
    "к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f",
    "х":"h","ц":"c","ч":"ch","ш":"sh","щ":"sch","ъ":"","ы":"y","ь":"","э":"e","ю":"yu","я":"ya",
})


def slugify(value: str) -> str:
    text = unicodedata.normalize("NFKD", norm(value)).translate(TRANSLIT)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text or hashlib.sha1(norm(value).encode("utf-8")).hexdigest()[:10]


def money(value: object) -> int | None:
    text = clean(value).replace("\u00a0", " ")
    if not text:
        return None
    number = re.sub(r"[^0-9,.-]", "", text).replace(",", ".")
    try:
        return int(round(float(number)))
    except ValueError:
        return None


def write_csv(filename: str, headers: list[str], rows: list[list[object]]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / filename
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(headers)
        for row in rows:
            writer.writerow(["" if value is None else value for value in row])
    return path


def split_multi(value: object) -> list[str]:
    text = clean(value)
    if not text:
        return []
    text = text.replace("\\n", "\n").replace("\u2028", "\n").replace("\u2029", "\n")
    parts = re.split(r"\n+|\s*,\s*", text)
    result: list[str] = []
    seen: set[str] = set()
    for part in parts:
        item = part.strip(" ;")
        key = norm(item)
        if item and key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def read_catalog() -> list[dict[str, str]]:
    with CATALOG.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{key: clean(value) for key, value in row.items()} for row in csv.DictReader(fh, delimiter=";")]


def canonical_map(values: list[str], prefix: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for raw in values:
        key = norm(raw)
        if not key:
            continue
        if key not in result:
            label = pretty(raw)
            result[key] = {
                "id": stable_id(prefix, key),
                "key": key,
                "label": label,
                "slug": slugify(label),
            }
    return result


def parse_size(raw: str) -> dict[str, object]:
    text = clean(raw)
    n = norm(text)
    if not n:
        return {"key":"", "label":"", "type":"", "d1":None, "d2":None, "d3":None, "unit":"", "bedding":""}
    if n == "единый размер":
        return {"key":"universal", "label":"Единый размер", "type":"universal", "d1":None, "d2":None, "d3":None, "unit":"", "bedding":""}
    vol = re.search(r"(\d+(?:[.,]\d+)?)\s*мл\b", n)
    if vol:
        value = float(vol.group(1).replace(",", "."))
        value_label = str(int(value)) if value.is_integer() else str(value).replace(".", ",")
        return {"key":f"volume:{value:g}", "label":f"{value_label} мл", "type":"volume", "d1":value, "d2":None, "d3":None, "unit":"ml", "bedding":""}
    letter = re.fullmatch(r"[smlx]{1,4}", n)
    if letter:
        label = n.upper()
        return {"key":f"letter:{label}", "label":label, "type":"letter", "d1":None, "d2":None, "d3":None, "unit":"", "bedding":""}
    if "см" in n:
        nums = [float(x.replace(",", ".")) for x in re.findall(r"\d+(?:[.,]\d+)?", n)]
        bedding = ""
        if "полутор" in n:
            bedding = "Полуторный"
        elif "евро" in n:
            bedding = "Евро"
        elif "кинг" in n:
            bedding = "Кинг сайз"
        elif "семейн" in n:
            bedding = "Семейный"
        if len(nums) >= 2 and any(mark in n for mark in ("×",)):
            dims = nums[:3]
            key_dims = "x".join(f"{x:g}" for x in dims)
            prefix = f"{slugify(bedding)}:" if bedding else ""
            label_dims = "×".join((str(int(x)) if x.is_integer() else str(x).replace(".", ",")) for x in dims) + " см"
            label = f"{bedding} {label_dims}".strip()
            return {"key":f"dimensions:{prefix}{key_dims}", "label":label, "type":"bedding" if bedding else "dimensions", "d1":dims[0], "d2":dims[1], "d3":dims[2] if len(dims)>2 else None, "unit":"cm", "bedding":bedding}
        if nums:
            value = nums[0]
            value_label = str(int(value)) if value.is_integer() else str(value).replace(".", ",")
            return {"key":f"single:{value:g}:cm", "label":f"{value_label} см", "type":"single_dimension", "d1":value, "d2":None, "d3":None, "unit":"cm", "bedding":""}
    return {"key":f"named:{n}", "label":pretty(text), "type":"named", "d1":None, "d2":None, "d3":None, "unit":"", "bedding":""}


def atomic_colors(raw: str) -> list[str]:
    text = clean(raw)
    if not text:
        return []
    return [pretty(part.strip()) for part in re.split(r"\s*/\s*", text) if clean(part)]


def color_meta(label: str) -> tuple[str, str]:
    n = norm(label)
    rules = [
        ("ледяной голубой", "ice_blue", "#BFD6DE"),
        ("ночной синий", "navy", "#243746"),
        ("серо-синий", "blue_grey", "#647985"),
        ("небесный", "sky_blue", "#B7D4E6"),
        ("голуб", "light_blue", "#AFC9D7"),
        ("син", "blue", "#35546F"),
        ("молоч", "ivory", "#EEE8DA"),
        ("экрю", "ecru", "#E3D5BD"),
        ("бел", "white", "#F5F3EE"),
        ("пудров", "powder", "#D8B7AE"),
        ("беж", "beige", "#D7C3A5"),
        ("корич", "brown", "#6F4E37"),
        ("черн", "black", "#1E1E1E"),
        ("зелен", "green", "#72816B"),
        ("желт", "yellow", "#D2B65C"),
        ("красн", "red", "#9A443B"),
        ("серебр", "silver", "#B7B9B8"),
        ("золот", "gold", "#C3A05B"),
        ("прозрач", "transparent", "#F4F4F2"),
    ]
    for token, family, hex_value in rules:
        if token in n:
            return family, hex_value
    return "other", "#D8D5CF"


def material_family(label: str) -> str:
    n = norm(label)
    if "костяной фарфор" in n:
        return "bone_porcelain"
    if "фарфор" in n:
        return "porcelain"
    if "хлоп" in n and "шерст" in n:
        return "wool_cotton"
    if "хлоп" in n:
        return "cotton"
    if "сатин" in n:
        return "satin"
    if "шелк" in n:
        return "silk"
    if "лен" in n:
        return "linen"
    if "хрустал" in n:
        return "crystal"
    if "стекл" in n:
        return "glass"
    if "керамик" in n:
        return "ceramic"
    if "кож" in n:
        return "leather"
    if "дерево" in n or "дуб" in n or "орех" in n:
        return "wood"
    if "сталь" in n:
        return "steel"
    if "микровелюр" in n:
        return "microvelour"
    if "бархат" in n:
        return "velvet"
    if "шерст" in n:
        return "wool"
    if "воск" in n or "парафин" in n:
        return "wax"
    return "other"


rows = read_catalog()
if len(rows) != 213:
    raise SystemExit(f"FILTER_DATABASE_V127: expected 213 variants, got {len(rows)}")

# Stable article order is the default popularity order currently used by the catalog.
article_order: list[str] = []
by_article: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in rows:
    article = row["Артикул"]
    if article not in by_article:
        article_order.append(article)
    by_article[article].append(row)

# Canonical dictionaries: deduplicated by normalized value, not by source casing.
category_map = canonical_map([r["Категория"] for r in rows if r["Категория"]], "cat")
subcategory_map = canonical_map([r["Подкатегория"] for r in rows if r["Подкатегория"]], "sub")
collection_map = canonical_map([r["Коллекция"] for r in rows if r["Коллекция"]], "col")
capsule_map = canonical_map([r["Капсула"] for r in rows if r["Капсула"]], "cap")
material_map = canonical_map([r["Материал"] for r in rows if r["Материал"]], "mat")
aroma_map = canonical_map([r["Аромат"] for r in rows if r["Аромат"]], "aro")

size_map: dict[str, dict[str, object]] = {}
for row in rows:
    parsed = parse_size(row["Размер"])
    if parsed["key"] and parsed["key"] not in size_map:
        parsed["id"] = stable_id("siz", str(parsed["key"]))
        parsed["slug"] = slugify(str(parsed["label"]))
        size_map[str(parsed["key"])] = parsed

color_map: dict[str, dict[str, str]] = {}
for row in rows:
    for label in atomic_colors(row["Цвет"]):
        key = norm(label)
        if key and key not in color_map:
            family, swatch = color_meta(label)
            color_map[key] = {
                "id": stable_id("clr", key), "key": key, "label": pretty(label),
                "slug": slugify(label), "family": family, "swatch": swatch,
            }

# Variant identifiers are deterministic within each article.
variant_records: list[dict[str, object]] = []
variant_by_source_row: dict[int, str] = {}
for article in article_order:
    for pos, row in enumerate(by_article[article], 1):
        variant_id = f"{article}__v{pos:03d}"
        variant_by_source_row[id(row)] = variant_id
        parsed_size = parse_size(row["Размер"])
        category = category_map.get(norm(row["Категория"]), {})
        subcategory = subcategory_map.get(norm(row["Подкатегория"]), {})
        collection = collection_map.get(norm(row["Коллекция"]), {})
        capsule = capsule_map.get(norm(row["Капсула"]), {})
        material = material_map.get(norm(row["Материал"]), {})
        aroma = aroma_map.get(norm(row["Аромат"]), {})
        variant_records.append({
            "variant_id": variant_id,
            "product_id": article,
            "article": article,
            "product_name": row["Название товара"],
            "color_raw": row["Цвет"],
            "aroma_id": aroma.get("id", ""), "aroma": aroma.get("label", ""),
            "size_id": size_map.get(str(parsed_size["key"]), {}).get("id", ""), "size": parsed_size["label"],
            "price_rub": money(row["Цена"]), "old_price_rub": money(row["Старая цена"]),
            "height": row["Высота"], "width": row["Ширина"], "volume": row["Объем"], "diameter": row["Диаметр"],
            "package_info": row["Комплектация / информация о размере"],
            "material_id": material.get("id", ""), "material": material.get("label", ""),
            "composition": row["Состав"], "details": row["Детали"],
            "collection_id": collection.get("id", ""), "collection": collection.get("label", ""),
            "capsule_id": capsule.get("id", ""), "capsule": capsule.get("label", ""),
            "category_id": category.get("id", ""), "category": category.get("label", ""),
            "subcategory_id": subcategory.get("id", ""), "subcategory": subcategory.get("label", ""),
            "ready_required": row["Товар входит в готовое решение"], "ready_optional": row["Опционально входит в готовое решение"],
            "photo_1": row["Фото 1"], "photo_2": row["Фото 2"], "photo_3": row["Фото 3"],
            "ready_solution_description": row["Описание готового решения"],
            "available": "true",
        })

# Variant-to-atomic-color M:N relation makes compound source colors filterable by each component.
variant_color_rows: list[list[object]] = []
for row in rows:
    variant_id = variant_by_source_row[id(row)]
    for order, label in enumerate(atomic_colors(row["Цвет"]), 1):
        meta = color_map[norm(label)]
        variant_color_rows.append([variant_id, row["Артикул"], meta["id"], meta["label"], order, row["Цвет"]])

# Facet counts.
def facet_counts(value_fn):
    products: dict[str, set[str]] = defaultdict(set)
    variants: dict[str, set[str]] = defaultdict(set)
    labels: dict[str, str] = {}
    for row in rows:
        variant_id = variant_by_source_row[id(row)]
        values = value_fn(row)
        if isinstance(values, str):
            values = [values] if values else []
        for label in values:
            key = norm(label)
            if not key:
                continue
            labels.setdefault(key, pretty(label))
            products[key].add(row["Артикул"])
            variants[key].add(variant_id)
    return labels, products, variants

color_labels, color_products, color_variants = facet_counts(lambda r: atomic_colors(r["Цвет"]))
size_labels, size_products, size_variants = facet_counts(lambda r: [parse_size(r["Размер"])["label"]] if parse_size(r["Размер"])["label"] else [])
material_labels, material_products, material_variants = facet_counts(lambda r: pretty(r["Материал"]))
aroma_labels, aroma_products, aroma_variants = facet_counts(lambda r: pretty(r["Аромат"]))
collection_labels, collection_products, collection_variants = facet_counts(lambda r: pretty(r["Коллекция"]))
capsule_labels, capsule_products, capsule_variants = facet_counts(lambda r: pretty(r["Капсула"]))
category_labels, category_products, category_variants = facet_counts(lambda r: pretty(r["Категория"]))
subcategory_labels, subcategory_products, subcategory_variants = facet_counts(lambda r: pretty(r["Подкатегория"]))

# Main product table / filter index.
product_rows: list[list[object]] = []
product_filter_index_rows: list[list[object]] = []
for rank, article in enumerate(article_order, 1):
    group = by_article[article]
    first = group[0]
    variant_ids = [variant_by_source_row[id(r)] for r in group]
    prices = [money(r["Цена"]) for r in group if money(r["Цена"]) is not None]
    old_prices = [money(r["Старая цена"]) for r in group if money(r["Старая цена"]) is not None]
    color_ids = sorted({color_map[norm(c)]["id"] for r in group for c in atomic_colors(r["Цвет"])})
    size_ids = sorted({size_map[str(parse_size(r["Размер"])["key"])]["id"] for r in group if parse_size(r["Размер"])["key"]})
    material_ids = sorted({material_map[norm(r["Материал"])]["id"] for r in group if norm(r["Материал"])})
    aroma_ids = sorted({aroma_map[norm(r["Аромат"])]["id"] for r in group if norm(r["Аромат"])})
    collection_ids = sorted({collection_map[norm(r["Коллекция"])]["id"] for r in group if norm(r["Коллекция"])})
    capsule_ids = sorted({capsule_map[norm(r["Капсула"])]["id"] for r in group if norm(r["Капсула"])})
    category = category_map.get(norm(first["Категория"]), {})
    subcategory = subcategory_map.get(norm(first["Подкатегория"]), {})
    images = [r[f"Фото {n}"] for r in group for n in (1,2,3) if r[f"Фото {n}"]]
    product_rows.append([
        article, article, first["Название товара"], rank, len(group),
        category.get("id", ""), category.get("label", ""),
        subcategory.get("id", ""), subcategory.get("label", ""),
        min(prices) if prices else None, max(prices) if prices else None,
        min(old_prices) if old_prices else None, max(old_prices) if old_prices else None,
        images[0] if images else "", "true",
    ])
    product_filter_index_rows.append([
        article, "|".join(variant_ids), "|".join(color_ids), "|".join(size_ids), "|".join(material_ids),
        "|".join(aroma_ids), "|".join(collection_ids), "|".join(capsule_ids),
        category.get("id", ""), subcategory.get("id", ""),
        min(prices) if prices else None, max(prices) if prices else None,
    ])

# Dictionaries with counts.
size_rows: list[list[object]] = []
for meta in size_map.values():
    label = str(meta["label"])
    key = norm(label)
    size_rows.append([
        meta["id"], meta["key"], label, meta["slug"], meta["type"], meta["d1"], meta["d2"], meta["d3"], meta["unit"], meta["bedding"],
        len(size_products.get(key, set())), len(size_variants.get(key, set())),
    ])
size_rows.sort(key=lambda r: (str(r[4]), float(r[5]) if isinstance(r[5], (int,float)) else 999999, str(r[2])))

color_rows: list[list[object]] = []
for key, meta in color_map.items():
    color_rows.append([meta["id"], key, meta["label"], meta["slug"], meta["family"], meta["swatch"], len(color_products.get(key,set())), len(color_variants.get(key,set()))])
color_rows.sort(key=lambda r: (str(r[4]), str(r[2])))

material_rows = []
for key, meta in material_map.items():
    material_rows.append([meta["id"], key, meta["label"], meta["slug"], material_family(meta["label"]), len(material_products.get(key,set())), len(material_variants.get(key,set()))])
material_rows.sort(key=lambda r: str(r[2]))

aroma_rows = [[meta["id"], key, meta["label"], meta["slug"], len(aroma_products.get(key,set())), len(aroma_variants.get(key,set()))] for key, meta in aroma_map.items()]
aroma_rows.sort(key=lambda r: str(r[2]))

# Entity dictionaries.
def entity_rows(mapping, products, variants):
    result = []
    for key, meta in mapping.items():
        result.append([meta["id"], key, meta["label"], meta["slug"], len(products.get(key,set())), len(variants.get(key,set()))])
    return sorted(result, key=lambda r: str(r[2]))

category_rows = entity_rows(category_map, category_products, category_variants)
collection_rows = entity_rows(collection_map, collection_products, collection_variants)
capsule_rows = entity_rows(capsule_map, capsule_products, capsule_variants)

subcategory_rows = []
for key, meta in subcategory_map.items():
    parent_categories = sorted({category_map[norm(r["Категория"])]["id"] for r in rows if norm(r["Подкатегория"]) == key and norm(r["Категория"]) in category_map})
    subcategory_rows.append([meta["id"], key, meta["label"], meta["slug"], "|".join(parent_categories), len(subcategory_products.get(key,set())), len(subcategory_variants.get(key,set()))])
subcategory_rows.sort(key=lambda r: str(r[2]))

# Characteristic dictionary: this is the implementation contract for filters.
filter_config_rows = [
    [1,"subcategory","Тип товара / подкатегория","subcategory_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","subcategory"],
    [2,"collection","Коллекция","collection_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","collection"],
    [3,"capsule","Капсула","capsule_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","capsule"],
    [4,"material","Материал","material_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","material"],
    [5,"size","Размер","size_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","size"],
    [6,"color","Цвет","variant_colors.color_id","color_swatch","true","OR","AND","ANY_VARIANT","dynamic","disabled","color"],
    [7,"aroma","Аромат","aroma_id","checkbox","true","OR","AND","ANY_VARIANT","dynamic","disabled","aroma"],
    [8,"price","Цена","price_rub","range","false","RANGE","AND","ANY_VARIANT","dynamic","disabled","price_from|price_to"],
]

characteristic_rows = [
    ["category","Категория","Категория","string","","false","select","product","11_categories.csv"],
    ["subcategory","Тип товара / подкатегория","Подкатегория","string","","true","checkbox","variant","12_subcategories.csv"],
    ["collection","Коллекция","Коллекция","string","","true","checkbox","variant","09_collections.csv"],
    ["capsule","Капсула","Капсула","string","","true","checkbox","variant","10_capsules.csv"],
    ["material","Материал","Материал","string","","true","checkbox","variant","07_materials.csv"],
    ["size","Размер","Размер","string","","true","checkbox","variant","04_sizes.csv"],
    ["color","Цвет","Цвет","string","","true","color_swatch","variant","05_colors.csv"],
    ["aroma","Аромат","Аромат","string","","true","checkbox","variant","08_aromas.csv"],
    ["price","Цена","Цена","number","RUB","true","range","variant","02_variants.csv"],
    ["old_price","Старая цена","Старая цена","number","RUB","false","range","variant","02_variants.csv"],
    ["height","Высота","Высота","string","","false","text","variant","02_variants.csv"],
    ["width","Ширина","Ширина","string","","false","text","variant","02_variants.csv"],
    ["volume","Объем","Объем","string","","false","text","variant","02_variants.csv"],
    ["diameter","Диаметр","Диаметр","string","","false","text","variant","02_variants.csv"],
    ["composition","Состав","Состав","text","","false","text","variant","02_variants.csv"],
    ["details","Детали","Детали","text","","false","text","variant","02_variants.csv"],
]

# Long EAV table for auditing and future filter expansion.
variant_characteristic_rows: list[list[object]] = []
for record, source in zip(variant_records, rows):
    values = {
        "category": record["category"], "subcategory": record["subcategory"], "collection": record["collection"], "capsule": record["capsule"],
        "material": record["material"], "size": record["size"], "aroma": record["aroma"],
        "price": record["price_rub"], "old_price": record["old_price_rub"],
        "height": record["height"], "width": record["width"], "volume": record["volume"], "diameter": record["diameter"],
        "composition": record["composition"], "details": record["details"],
    }
    for code, value in values.items():
        if value in (None, ""):
            continue
        numeric = value if isinstance(value, int) else ""
        variant_characteristic_rows.append([record["variant_id"], record["product_id"], code, value, norm(value), numeric])
    for color in atomic_colors(source["Цвет"]):
        variant_characteristic_rows.append([record["variant_id"], record["product_id"], "color", color, norm(color), ""])

# Overall filter values and counts. Runtime must recalculate against the current category + other active facets.
filter_value_rows: list[list[object]] = []
def add_filter_values(code: str, mapping: dict[str, dict[str,str]], products_map, variants_map, extra_fn=None):
    for key, meta in mapping.items():
        extra = extra_fn(meta) if extra_fn else ("", "")
        filter_value_rows.append([code, meta["id"], meta["label"], meta["slug"], len(products_map.get(key,set())), len(variants_map.get(key,set())), extra[0], extra[1]])

add_filter_values("collection", collection_map, collection_products, collection_variants)
add_filter_values("capsule", capsule_map, capsule_products, capsule_variants)
add_filter_values("material", material_map, material_products, material_variants, lambda m:(material_family(m["label"]),""))
add_filter_values("aroma", aroma_map, aroma_products, aroma_variants)
add_filter_values("subcategory", subcategory_map, subcategory_products, subcategory_variants)
for meta in size_map.values():
    key = norm(str(meta["label"]))
    filter_value_rows.append(["size", meta["id"], meta["label"], meta["slug"], len(size_products.get(key,set())), len(size_variants.get(key,set())), meta["type"], meta["unit"]])
for key, meta in color_map.items():
    filter_value_rows.append(["color", meta["id"], meta["label"], meta["slug"], len(color_products.get(key,set())), len(color_variants.get(key,set())), meta["family"], meta["swatch"]])
filter_value_rows.sort(key=lambda r: (str(r[0]), str(r[2])))

# Ready-solution relations are included because they are part of the product model and useful for merchandising filters.
solution_names: list[str] = []
for row in rows:
    for value in split_multi(row["Товар входит в готовое решение"]) + split_multi(row["Опционально входит в готовое решение"]):
        if norm(value) and norm(value) not in {norm(x) for x in solution_names}:
            solution_names.append(value)
solution_map = canonical_map(solution_names, "sol")
ready_solution_product_rows: list[list[object]] = []
for article in article_order:
    required: dict[str, str] = {}
    optional: dict[str, str] = {}
    for row in by_article[article]:
        for value in split_multi(row["Товар входит в готовое решение"]):
            required[norm(value)] = value
        for value in split_multi(row["Опционально входит в готовое решение"]):
            optional[norm(value)] = value
    for key, value in required.items():
        if key in solution_map:
            ready_solution_product_rows.append([solution_map[key]["id"], solution_map[key]["label"], article, "required"])
    for key, value in optional.items():
        if key in solution_map and key not in required:
            ready_solution_product_rows.append([solution_map[key]["id"], solution_map[key]["label"], article, "optional"])

solution_rows = []
for key, meta in solution_map.items():
    linked = [r for r in ready_solution_product_rows if r[0] == meta["id"]]
    solution_rows.append([meta["id"], meta["label"], meta["slug"], sum(1 for r in linked if r[3]=="required"), sum(1 for r in linked if r[3]=="optional")])
solution_rows.sort(key=lambda r: str(r[1]))

image_rows = []
for record in variant_records:
    for order in (1,2,3):
        path = record[f"photo_{order}"]
        if path:
            image_rows.append([f"{record['variant_id']}__img{order}", record["variant_id"], record["product_id"], order, path])

# Full normalized variant rows.
variant_headers = [
    "variant_id","product_id","article","product_name","color_raw","aroma_id","aroma","size_id","size","price_rub","old_price_rub",
    "height","width","volume","diameter","package_info","material_id","material","composition","details",
    "collection_id","collection","capsule_id","capsule","category_id","category","subcategory_id","subcategory",
    "ready_required","ready_optional","photo_1","photo_2","photo_3","ready_solution_description","available",
]
variant_rows = [[record.get(h, "") for h in variant_headers] for record in variant_records]

files: list[Path] = []
files.append(write_csv("01_products.csv", ["product_id","article","product_name","popularity_rank","variant_count","category_id","category","subcategory_id","subcategory","min_price_rub","max_price_rub","min_old_price_rub","max_old_price_rub","primary_image","available"], product_rows))
files.append(write_csv("02_variants.csv", variant_headers, variant_rows))
files.append(write_csv("03_filter_config.csv", ["sort_order","filter_code","filter_label","source","ui_control","multi_select","within_group_logic","cross_group_logic","variant_match","values_mode","zero_result_behavior","url_param"], filter_config_rows))
files.append(write_csv("04_sizes.csv", ["size_id","size_key","size_label","slug","size_type","dimension_1","dimension_2","dimension_3","unit","bedding_type","product_count","variant_count"], size_rows))
files.append(write_csv("05_colors.csv", ["color_id","normalized_key","color_label","slug","color_family","swatch_hex","product_count","variant_count"], color_rows))
files.append(write_csv("06_variant_colors.csv", ["variant_id","product_id","color_id","color_label","component_order","source_color_raw"], variant_color_rows))
files.append(write_csv("07_materials.csv", ["material_id","normalized_key","material_label","slug","material_family","product_count","variant_count"], material_rows))
files.append(write_csv("08_aromas.csv", ["aroma_id","normalized_key","aroma_label","slug","product_count","variant_count"], aroma_rows))
files.append(write_csv("09_collections.csv", ["collection_id","normalized_key","collection_label","slug","product_count","variant_count"], collection_rows))
files.append(write_csv("10_capsules.csv", ["capsule_id","normalized_key","capsule_label","slug","product_count","variant_count"], capsule_rows))
files.append(write_csv("11_categories.csv", ["category_id","normalized_key","category_label","slug","product_count","variant_count"], category_rows))
files.append(write_csv("12_subcategories.csv", ["subcategory_id","normalized_key","subcategory_label","slug","parent_category_ids","product_count","variant_count"], subcategory_rows))
files.append(write_csv("13_characteristics.csv", ["characteristic_code","label","source_column","data_type","unit","filterable_default","ui_control","scope","dictionary_table"], characteristic_rows))
files.append(write_csv("14_variant_characteristics.csv", ["variant_id","product_id","characteristic_code","value","normalized_value","numeric_value"], variant_characteristic_rows))
files.append(write_csv("15_filter_values.csv", ["filter_code","value_id","label","slug","product_count","variant_count","group_or_type","swatch_or_unit"], filter_value_rows))
files.append(write_csv("16_product_filter_index.csv", ["product_id","variant_ids","color_ids","size_ids","material_ids","aroma_ids","collection_ids","capsule_ids","category_id","subcategory_id","min_price_rub","max_price_rub"], product_filter_index_rows))
files.append(write_csv("17_ready_solutions.csv", ["solution_id","solution_name","slug","required_product_count","optional_product_count"], solution_rows))
files.append(write_csv("18_ready_solution_products.csv", ["solution_id","solution_name","product_id","relation_type"], ready_solution_product_rows))
files.append(write_csv("19_images.csv", ["image_id","variant_id","product_id","sort_order","path"], image_rows))

relationships = [
    ["02_variants.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["02_variants.csv","size_id","04_sizes.csv","size_id","many-to-one"],
    ["02_variants.csv","material_id","07_materials.csv","material_id","many-to-one"],
    ["02_variants.csv","aroma_id","08_aromas.csv","aroma_id","many-to-one"],
    ["02_variants.csv","collection_id","09_collections.csv","collection_id","many-to-one"],
    ["02_variants.csv","capsule_id","10_capsules.csv","capsule_id","many-to-one"],
    ["02_variants.csv","category_id","11_categories.csv","category_id","many-to-one"],
    ["02_variants.csv","subcategory_id","12_subcategories.csv","subcategory_id","many-to-one"],
    ["06_variant_colors.csv","variant_id","02_variants.csv","variant_id","many-to-one"],
    ["06_variant_colors.csv","color_id","05_colors.csv","color_id","many-to-one"],
    ["14_variant_characteristics.csv","variant_id","02_variants.csv","variant_id","many-to-one"],
    ["18_ready_solution_products.csv","solution_id","17_ready_solutions.csv","solution_id","many-to-one"],
    ["18_ready_solution_products.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["19_images.csv","variant_id","02_variants.csv","variant_id","many-to-one"],
]
files.append(write_csv("20_schema_relationships.csv", ["child_table","child_column","parent_table","parent_column","relationship"], relationships))

manifest_rows = [
    ["01_products.csv","One row per product card/article","product_id",len(product_rows)],
    ["02_variants.csv","Full normalized SKU/variant table","variant_id",len(variant_rows)],
    ["03_filter_config.csv","Filter implementation contract","filter_code",len(filter_config_rows)],
    ["04_sizes.csv","Canonical size dictionary","size_id",len(size_rows)],
    ["05_colors.csv","Atomic canonical color dictionary","color_id",len(color_rows)],
    ["06_variant_colors.csv","Variant-to-color M:N relation; compound colors are split","variant_id+color_id",len(variant_color_rows)],
    ["07_materials.csv","Canonical material dictionary","material_id",len(material_rows)],
    ["08_aromas.csv","Canonical aroma dictionary","aroma_id",len(aroma_rows)],
    ["09_collections.csv","Collection dictionary","collection_id",len(collection_rows)],
    ["10_capsules.csv","Capsule dictionary","capsule_id",len(capsule_rows)],
    ["11_categories.csv","Category dictionary","category_id",len(category_rows)],
    ["12_subcategories.csv","Subcategory dictionary","subcategory_id",len(subcategory_rows)],
    ["13_characteristics.csv","Characteristic metadata / filterability dictionary","characteristic_code",len(characteristic_rows)],
    ["14_variant_characteristics.csv","Long EAV characteristics by variant","variant_id+characteristic_code+value",len(variant_characteristic_rows)],
    ["15_filter_values.csv","Canonical filter values with overall facet counts","filter_code+value_id",len(filter_value_rows)],
    ["16_product_filter_index.csv","Pre-aggregated product-level filter index","product_id",len(product_filter_index_rows)],
    ["17_ready_solutions.csv","Ready solution dictionary","solution_id",len(solution_rows)],
    ["18_ready_solution_products.csv","Ready solution to product relations","solution_id+product_id",len(ready_solution_product_rows)],
    ["19_images.csv","Normalized product images","image_id",len(image_rows)],
    ["20_schema_relationships.csv","Foreign key relationship map","child_table+child_column",len(relationships)],
]
manifest = write_csv("00_manifest.csv", ["file_name","description","primary_key","row_count"], manifest_rows)
files.insert(0, manifest)

readme = OUT / "README.md"
readme.write_text(
    "# Культура дома — база данных для фильтров\n\n"
    f"Версия: {FILTER_VERSION}. Источник: public/data/catalog_master.csv. "
    f"Товаров: {len(article_order)}, SKU/вариантов: {len(rows)}.\n\n"
    "## Как строить фильтры\n"
    "- Разные группы фильтров: AND. Значения внутри одной группы: OR.\n"
    "- Карточка товара проходит фильтр, если условию соответствует хотя бы один ее SKU (ANY_VARIANT).\n"
    "- Цвет фильтруется через 06_variant_colors.csv: составные цвета вроде «Белый / Золотой» связаны сразу с двумя атомарными цветами.\n"
    "- Размеры канонизированы: разные варианты записи знаков x/х/× и пробелов сведены к одному size_id; постельные размеры сохраняют тип (Евро, Полуторный, Кинг сайз).\n"
    "- Значения фасетов на странице категории должны пересчитываться динамически по текущему набору вариантов и другим активным группам фильтров. Общие counts в 15_filter_values.csv — базовые, не замена runtime-пересчету.\n"
    "- Для реализации используйте 03_filter_config.csv + 15_filter_values.csv + 16_product_filter_index.csv; для точной проверки вариантов — 02_variants.csv и M:N 06_variant_colors.csv.\n",
    encoding="utf-8",
)
files.append(readme)

zip_path = OUT / "kultura_doma_filter_database_csv.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(files, key=lambda p: p.name):
        info = zipfile.ZipInfo(path.name)
        info.date_time = (1980, 1, 1, 0, 0, 0)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, path.read_bytes())

print(
    "// FILTER_DATABASE_V127: "
    f"products={len(product_rows)}; variants={len(variant_rows)}; sizes={len(size_rows)}; "
    f"colors={len(color_rows)}; materials={len(material_rows)}; filter_values={len(filter_value_rows)}; "
    f"files={len(files)}; zip={zip_path.relative_to(ROOT)}"
)
