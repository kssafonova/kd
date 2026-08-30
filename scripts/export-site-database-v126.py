from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import io
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "public" / "data"
OUT = DATA / "database"
CATALOG = DATA / "catalog_master.csv"
PAGE = ROOT / "app" / "page.tsx"

NULLS = {"", "null", "none", "nan"}


def clean(value: object) -> str:
    text = str(value or "").strip().replace("\ufeff", "")
    return "" if text.lower() in NULLS else text


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", clean(value).lower().replace("ё", "е")).strip()


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha1(norm(value).encode('utf-8')).hexdigest()[:10]}"


def money(value: object) -> int:
    text = clean(value).replace("\u00a0", " ")
    if not text:
        return 0
    digits = re.sub(r"[^0-9,.-]", "", text).replace(",", ".")
    try:
        return int(round(float(digits)))
    except ValueError:
        return 0


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
        if item and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def read_catalog() -> tuple[list[str], list[list[str]]]:
    text = CATALOG.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    first_break = text.find("\n")
    header_line = text[:first_break]
    header = next(csv.reader([header_line], delimiter=";", quotechar='"'))
    body = text[first_break + 1 :]
    records = [chunk for chunk in re.split(r"(?=^KD-PD-)", body, flags=re.MULTILINE) if chunk.strip()]
    rows: list[list[str]] = []
    for chunk in records:
        # Catalog source can contain physical line breaks inside fields. Record
        # boundaries are article prefixes, so internal breaks can safely become
        # explicit \n markers before CSV parsing.
        safe = chunk.strip("\n").replace("\n", "\\n")
        row = next(csv.reader([safe], delimiter=";", quotechar='"'))
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        elif len(row) > len(header):
            # Preserve the fixed 25-column contract. Extra fragments can only
            # belong to the final long-text field.
            row = row[: len(header) - 1] + [";".join(row[len(header) - 1 :])]
        rows.append([clean(v) for v in row])
    return header, rows


def write_csv(name: str, headers: list[str], rows: list[list[object]]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / name
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(headers)
        for row in rows:
            writer.writerow(["" if v is None else v for v in row])
    return path


def read_comma_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: clean(v) for k, v in row.items()} for row in csv.DictReader(fh)]


def parse_ts_array(text: str, name: str) -> list[str]:
    match = re.search(rf"const\s+{re.escape(name)}\s*=\[(.*?)\];", text, re.S)
    return re.findall(r'"([^"]+)"', match.group(1)) if match else []


def parse_ts_string_array_object(text: str, name: str) -> dict[str, list[str]]:
    match = re.search(rf"const\s+{re.escape(name)}[^=]*=\{{(.*?)\n\}};", text, re.S)
    if not match:
        return {}
    result: dict[str, list[str]] = {}
    for item in re.finditer(r'"([^"]+)"\s*:\s*\[(.*?)\]', match.group(1), re.S):
        result[item.group(1)] = re.findall(r'"([^"]+)"', item.group(2))
    return result


def parse_local_string_array_object(text: str, name: str) -> dict[str, list[str]]:
    match = re.search(rf"const\s+{re.escape(name)}[^=]*=\{{(.*?)\n\s*\}};", text, re.S)
    if not match:
        return {}
    result: dict[str, list[str]] = {}
    for item in re.finditer(r'"([^"]+)"\s*:\s*\[(.*?)\]', match.group(1), re.S):
        result[item.group(1)] = re.findall(r'"([^"]+)"', item.group(2))
    return result


def parse_size(label: str) -> tuple[str, str, str, str, str]:
    text = clean(label)
    if not text:
        return "", "", "", "", ""
    low = norm(text)
    if low == "единый размер":
        return "universal", "", "", "", ""
    volume = re.search(r"([\d.,]+)\s*мл\b", low)
    if volume:
        return "volume", volume.group(1).replace(",", "."), "", "ml", ""
    dims = re.search(r"(\d+(?:[.,]\d+)?)\s*[xх×]\s*(\d+(?:[.,]\d+)?)\s*см\b", low)
    if dims:
        return "dimensions", dims.group(1).replace(",", "."), dims.group(2).replace(",", "."), "cm", ""
    single = re.search(r"(\d+(?:[.,]\d+)?)\s*см\b", low)
    if single:
        return "single_dimension", single.group(1).replace(",", "."), "", "cm", ""
    if re.fullmatch(r"[smlx]{1,4}", low):
        return "letter", low.upper(), "", "", ""
    return "named", "", "", "", text


header, raw_rows = read_catalog()
idx = {name: i for i, name in enumerate(header)}

def col(row: list[str], name: str) -> str:
    return row[idx[name]] if name in idx else ""

# Current catalog order is kept as a stable default PLP order.
article_order: list[str] = []
by_article: dict[str, list[list[str]]] = defaultdict(list)
for row in raw_rows:
    article = col(row, "Артикул")
    if article not in by_article:
        article_order.append(article)
    by_article[article].append(row)

category_names: list[str] = []
subcategory_pairs: list[tuple[str, str]] = []
collection_names: list[str] = []
capsule_names: list[str] = []
color_names: list[str] = []
aroma_names: list[str] = []
material_names: list[str] = []
size_names: list[str] = []

for row in raw_rows:
    category = col(row, "Категория")
    subcategory = col(row, "Подкатегория")
    collection = col(row, "Коллекция")
    capsule = col(row, "Капсула")
    color = col(row, "Цвет")
    aroma = col(row, "Аромат")
    material = col(row, "Материал")
    size = col(row, "Размер")
    if category and category not in category_names:
        category_names.append(category)
    if category and subcategory and (category, subcategory) not in subcategory_pairs:
        subcategory_pairs.append((category, subcategory))
    if collection and collection not in collection_names:
        collection_names.append(collection)
    if capsule and capsule not in capsule_names:
        capsule_names.append(capsule)
    if color and color not in color_names:
        color_names.append(color)
    if aroma and aroma not in aroma_names:
        aroma_names.append(aroma)
    if material and material not in material_names:
        material_names.append(material)
    if size and size not in size_names:
        size_names.append(size)

category_ids = {name: stable_id("cat", name) for name in category_names}
subcategory_ids = {(cat, sub): stable_id("sub", f"{cat}|{sub}") for cat, sub in subcategory_pairs}
collection_ids = {name: stable_id("col", name) for name in collection_names}
capsule_ids = {name: stable_id("cap", name) for name in capsule_names}
color_ids = {name: stable_id("clr", name) for name in color_names}
aroma_ids = {name: stable_id("aro", name) for name in aroma_names}
material_ids = {name: stable_id("mat", name) for name in material_names}
size_ids = {name: stable_id("siz", name) for name in size_names}

variant_rows: list[list[object]] = []
image_rows: list[list[object]] = []
product_size_rows: list[list[object]] = []
product_color_rows: list[list[object]] = []
product_aroma_rows: list[list[object]] = []
product_material_rows: list[list[object]] = []
product_collection_rows: list[list[object]] = []
product_capsule_rows: list[list[object]] = []
product_rows: list[list[object]] = []

for catalog_rank, article in enumerate(article_order, 1):
    variants = by_article[article]
    first = variants[0]
    product_id = article
    prices = [money(col(r, "Цена")) for r in variants if money(col(r, "Цена")) > 0]
    old_prices = [money(col(r, "Старая цена")) for r in variants if money(col(r, "Старая цена")) > 0]
    collections = [col(r, "Коллекция") for r in variants if col(r, "Коллекция")]
    capsules = [col(r, "Капсула") for r in variants if col(r, "Капсула")]
    materials = [col(r, "Материал") for r in variants if col(r, "Материал")]
    images = [col(r, f"Фото {n}") for r in variants for n in (1, 2, 3) if col(r, f"Фото {n}")]
    ready_present = any(col(r, "Товар входит в готовое решение") or col(r, "Опционально входит в готовое решение") for r in variants)
    category = col(first, "Категория")
    subcategory = col(first, "Подкатегория")
    collection = collections[0] if collections else ""
    capsule = capsules[0] if capsules else ""
    product_rows.append([
        product_id, article, col(first, "Название товара"), catalog_rank,
        category_ids.get(category, ""), category,
        subcategory_ids.get((category, subcategory), ""), subcategory,
        collection_ids.get(collection, ""), collection,
        capsule_ids.get(capsule, ""), capsule,
        " | ".join(dict.fromkeys(materials)), len(variants),
        min(prices) if prices else "", max(prices) if prices else "",
        min(old_prices) if old_prices else "", max(old_prices) if old_prices else "",
        images[0] if images else "", "true" if ready_present else "false",
    ])

    seen_pc: set[tuple[str, str]] = set()
    seen_pa: set[tuple[str, str]] = set()
    seen_pm: set[tuple[str, str]] = set()
    seen_ps: set[tuple[str, str]] = set()
    seen_pcol: set[tuple[str, str]] = set()
    seen_pcap: set[tuple[str, str]] = set()

    for variant_order, row in enumerate(variants, 1):
        variant_id = f"{article}__v{variant_order:03d}"
        color = col(row, "Цвет")
        aroma = col(row, "Аромат")
        size = col(row, "Размер")
        material = col(row, "Материал")
        collection = col(row, "Коллекция")
        capsule = col(row, "Капсула")
        category = col(row, "Категория")
        subcategory = col(row, "Подкатегория")
        variant_rows.append([
            variant_id, product_id, article, variant_order,
            color_ids.get(color, ""), color, aroma_ids.get(aroma, ""), aroma,
            size_ids.get(size, ""), size,
            money(col(row, "Цена")) or "", money(col(row, "Старая цена")) or "",
            col(row, "Высота"), col(row, "Ширина"), col(row, "Объем"), col(row, "Диаметр"),
            col(row, "Комплектация / информация о размере"),
            material_ids.get(material, ""), material, col(row, "Состав"), col(row, "Детали"),
            collection_ids.get(collection, ""), collection,
            capsule_ids.get(capsule, ""), capsule,
            category_ids.get(category, ""), category,
            subcategory_ids.get((category, subcategory), ""), subcategory,
            col(row, "Фото 1"), col(row, "Фото 2"), col(row, "Фото 3"),
        ])
        for image_order in (1, 2, 3):
            path = col(row, f"Фото {image_order}")
            if path:
                image_rows.append([f"{variant_id}__img{image_order}", variant_id, product_id, image_order, path])
        if size:
            key = (product_id, size)
            if key not in seen_ps:
                seen_ps.add(key)
                product_size_rows.append([product_id, size_ids[size], size])
        if color:
            key = (product_id, color)
            if key not in seen_pc:
                seen_pc.add(key)
                product_color_rows.append([product_id, color_ids[color], color])
        if aroma:
            key = (product_id, aroma)
            if key not in seen_pa:
                seen_pa.add(key)
                product_aroma_rows.append([product_id, aroma_ids[aroma], aroma])
        if material:
            key = (product_id, material)
            if key not in seen_pm:
                seen_pm.add(key)
                product_material_rows.append([product_id, material_ids[material], material])
        if collection:
            key = (product_id, collection)
            if key not in seen_pcol:
                seen_pcol.add(key)
                product_collection_rows.append([product_id, collection_ids[collection], collection])
        if capsule:
            key = (product_id, capsule)
            if key not in seen_pcap:
                seen_pcap.add(key)
                product_capsule_rows.append([product_id, capsule_ids[capsule], capsule])

# Dictionaries and dimensions.
category_rows = [[category_ids[name], name, i] for i, name in enumerate(category_names, 1)]
subcategory_rows = [[subcategory_ids[(cat, sub)], category_ids[cat], cat, sub, i] for i, (cat, sub) in enumerate(subcategory_pairs, 1)]
color_rows = [[color_ids[name], name, norm(name)] for name in color_names]
aroma_rows = [[aroma_ids[name], name, norm(name)] for name in aroma_names]
material_rows = [[material_ids[name], name, norm(name)] for name in material_names]
size_rows = []
for name in size_names:
    kind, a, b, unit, named = parse_size(name)
    size_rows.append([size_ids[name], name, kind, a, b, unit, named])

collection_stats: dict[str, dict[str, object]] = defaultdict(lambda: {"products": set(), "variants": 0, "image": ""})
capsule_stats: dict[str, dict[str, object]] = defaultdict(lambda: {"products": set(), "variants": 0, "image": ""})
for row in raw_rows:
    article = col(row, "Артикул")
    image = col(row, "Фото 1")
    collection = col(row, "Коллекция")
    capsule = col(row, "Капсула")
    if collection:
        collection_stats[collection]["products"].add(article)
        collection_stats[collection]["variants"] += 1
        if not collection_stats[collection]["image"] and image:
            collection_stats[collection]["image"] = image
    if capsule:
        capsule_stats[capsule]["products"].add(article)
        capsule_stats[capsule]["variants"] += 1
        if not capsule_stats[capsule]["image"] and image:
            capsule_stats[capsule]["image"] = image
collection_rows = [[collection_ids[n], n, i, len(collection_stats[n]["products"]), collection_stats[n]["variants"], collection_stats[n]["image"]] for i, n in enumerate(collection_names, 1)]
capsule_rows = [[capsule_ids[n], n, i, len(capsule_stats[n]["products"]), capsule_stats[n]["variants"], capsule_stats[n]["image"]] for i, n in enumerate(capsule_names, 1)]

# Ready solutions from the current catalog master.
solution_product_map: dict[str, dict[str, str]] = defaultdict(dict)
solution_descriptions: dict[str, str] = {}
for row in raw_rows:
    article = col(row, "Артикул")
    for name in split_multi(col(row, "Товар входит в готовое решение")):
        solution_product_map[name][article] = "required"
    for name in split_multi(col(row, "Опционально входит в готовое решение")):
        solution_product_map[name].setdefault(article, "optional")
    description = col(row, "Описание готового решения")
    if description:
        for name in split_multi(col(row, "Товар входит в готовое решение")) + split_multi(col(row, "Опционально входит в готовое решение")):
            solution_descriptions.setdefault(name, description)

solution_names = list(solution_product_map.keys())
solution_ids = {name: stable_id("sol", name) for name in solution_names}
ready_solution_rows: list[list[object]] = []
ready_solution_product_rows: list[list[object]] = []
ready_solution_entity_rows: list[list[object]] = []
for i, name in enumerate(solution_names, 1):
    links = solution_product_map[name]
    required = [a for a, t in links.items() if t == "required"]
    optional = [a for a, t in links.items() if t == "optional"]
    entity_links: set[tuple[str, str]] = set()
    for article, relation in links.items():
        rows = by_article.get(article, [])
        product_name = col(rows[0], "Название товара") if rows else ""
        ready_solution_product_rows.append([solution_ids[name], name, article, article, product_name, relation])
        for r in rows:
            collection = col(r, "Коллекция")
            capsule = col(r, "Капсула")
            if collection:
                entity_links.add(("collection", collection))
            if capsule:
                entity_links.add(("capsule", capsule))
    for entity_type, entity_name in sorted(entity_links):
        entity_id = collection_ids.get(entity_name, "") if entity_type == "collection" else capsule_ids.get(entity_name, "")
        ready_solution_entity_rows.append([solution_ids[name], name, entity_type, entity_id, entity_name])
    ready_solution_rows.append([
        solution_ids[name], name, i, len(required), len(optional), len(links),
        len([x for x in entity_links if x[0] == "collection"]),
        len([x for x in entity_links if x[0] == "capsule"]),
        solution_descriptions.get(name, ""),
    ])

# Constructor/scenario source tables already present in the repository.
scenario_source = read_comma_csv(DATA / "kultura_doma_constructor_scenarios.csv")
preset_source = read_comma_csv(DATA / "kultura-doma-constructor-presets-final.csv")
scenario_rows: list[list[object]] = []
seen_scenarios: set[str] = set()
for row in scenario_source:
    sid = row.get("scenario_id", "")
    if not sid or sid in seen_scenarios:
        continue
    seen_scenarios.add(sid)
    scenario_rows.append([
        sid, row.get("scenario_name", ""), row.get("occasion", ""), row.get("guests_supported", ""),
        row.get("lead_collection_slug", ""), row.get("entry_collection", ""), row.get("styling_message", ""),
    ])

product_name_map: dict[str, list[str]] = defaultdict(list)
for article in article_order:
    name = col(by_article[article][0], "Название товара")
    product_name_map[norm(name)].append(article)
constructor_item_rows: list[list[object]] = []
for row in preset_source:
    pname = row.get("product_name", "")
    matches = product_name_map.get(norm(pname), [])
    matched_article = matches[0] if len(matches) == 1 else ""
    source_collection = row.get("collection", "")
    constructor_item_rows.append([
        row.get("scenario_id", ""), row.get("scenario_name", ""), row.get("sort_order", ""),
        row.get("preset_status", ""), row.get("default_quantity", ""), row.get("quantity_rule", ""),
        row.get("variant_selection_required", ""), matched_article, matched_article,
        pname, source_collection, collection_ids.get(source_collection, ""), row.get("product_type", ""),
        row.get("price_rub", ""), row.get("product_url", ""), row.get("primary_image_url", ""),
        row.get("selection_reason", ""), "exact_name" if matched_article else "unmatched_source_item",
    ])

# Checkout, geography and store configuration from the live UI source.
page_text = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
cities = parse_ts_array(page_text, "KD_CITY_SUGGESTIONS")
address_map = parse_ts_string_array_object(page_text, "KD_ADDRESS_SUGGESTIONS")
pvz_map = parse_ts_string_array_object(page_text, "KD_PVZ_POINTS")
store_map = parse_local_string_array_object(page_text, "storePoints")

region_ids = {city: stable_id("reg", city) for city in cities}
region_rows = []
address_rows = []
pickup_rows = []
for i, city in enumerate(cities, 1):
    region_rows.append([
        region_ids[city], city, i, "true" if city in store_map and store_map[city] else "false",
        len(address_map.get(city, [])), len(pvz_map.get(city, [])), "RUB", "RU",
    ])
    for j, address in enumerate(address_map.get(city, []), 1):
        address_rows.append([f"{region_ids[city]}__addr{j:03d}", region_ids[city], city, address, "courier_suggestion", j])
    for j, point in enumerate(pvz_map.get(city, []), 1):
        pickup_rows.append([f"{region_ids[city]}__pvz{j:03d}", region_ids[city], city, "pvz", point, point, j])
    for j, point in enumerate(store_map.get(city, []), 1):
        pickup_rows.append([f"{region_ids[city]}__store{j:03d}", region_ids[city], city, "store", point, point, j])

boutique_rows = []
seen_boutiques: set[tuple[str, str]] = set()
for item in re.finditer(r'\{city:"([^"]+)",address:"([^"]+)",hours:"([^"]+)",lat:([\d.]+),lon:([\d.]+)\}', page_text):
    city, address, hours, lat, lon = item.groups()
    if (city, address) in seen_boutiques:
        continue
    seen_boutiques.add((city, address))
    boutique_rows.append([
        stable_id("store", f"{city}|{address}"), region_ids.get(city, stable_id("reg", city)), city,
        address, hours, float(lat), float(lon), "true",
    ])

online_discount_match = re.search(r"onlineDiscount=payment===\"online\"\?Math\.round\(total\*([\d.]+)\):0", page_text)
shipping_match = re.search(r"shipping=delivery===\"courier\"\?\(total>=(\d+)\?0:(\d+)\):0", page_text)
online_discount = float(online_discount_match.group(1)) * 100 if online_discount_match else 3.0
free_threshold = int(shipping_match.group(1)) if shipping_match else 15000
courier_fee = int(shipping_match.group(2)) if shipping_match else 300

payment_rows = [
    ["online", "Онлайн — картой / СБП", "prepaid", "bank_card|sbp", online_discount, "RUB", "true", 1],
    ["upon", "При получении", "on_receipt", "bank_card|cash", 0, "RUB", "true", 2],
]
delivery_rows = [
    ["courier", "Курьером", 2, 3, courier_fee, free_threshold, "RUB", "address", "true", 1],
    ["store", "Самовывоз", 2, 3, 0, 0, "RUB", "store", "true", 2],
    ["pvz", "ПВЗ", 2, 3, 0, 0, "RUB", "pvz", "true", 3],
]
pricing_rows = [
    ["online_payment_discount", "Скидка при онлайн-оплате", "payment_method=online", "percent_discount", online_discount, "", "RUB", "true"],
    ["courier_free_threshold", "Бесплатная курьерская доставка от порога", f"delivery_method=courier AND order_total>={free_threshold}", "shipping_fee", 0, free_threshold, "RUB", "true"],
    ["courier_base_fee", "Базовая стоимость курьерской доставки", f"delivery_method=courier AND order_total<{free_threshold}", "shipping_fee", courier_fee, free_threshold, "RUB", "true"],
]

phone_match = re.search(r'href="tel:([^"]+)"', page_text)
email_match = re.search(r'href="mailto:([^"]+)"', page_text)
return_match = re.search(r"Возврат в течение\s+(\d+)\s+д", page_text)
delivery_note_match = re.search(r"Доставка по России от\s+(\d+)\s+д", page_text)
contacts_rows = [
    ["support_phone", "Телефон", phone_match.group(1) if phone_match else "+78005553535", "customer_support", "true"],
    ["support_email", "Email", email_match.group(1) if email_match else "hello@kultura-doma.ru", "customer_support", "true"],
]
policy_rows = [
    ["return_period_days", "Срок возврата", int(return_match.group(1)) if return_match else 14, "days", "true"],
    ["delivery_min_days", "Минимальный заявленный срок доставки по России", int(delivery_note_match.group(1)) if delivery_note_match else 1, "days", "true"],
    ["currency", "Валюта магазина", "RUB", "ISO-4217", "true"],
]

# Write all normalized database tables.
tables: dict[str, tuple[list[str], list[list[object]], str, str]] = {
    "01_products.csv": (["product_id","article","name","catalog_sort_order","category_id","category_name","subcategory_id","subcategory_name","collection_id","collection_name","capsule_id","capsule_name","materials","variant_count","min_price_rub","max_price_rub","min_old_price_rub","max_old_price_rub","primary_image","has_ready_solution"], product_rows, "product_id", "Current catalog grouped by article"),
    "02_product_variants.csv": (["variant_id","product_id","article","variant_order","color_id","color_name","aroma_id","aroma_name","size_id","size_label","price_rub","old_price_rub","height","width","volume","diameter","package_info","material_id","material_name","composition","details","collection_id","collection_name","capsule_id","capsule_name","category_id","category_name","subcategory_id","subcategory_name","image_1","image_2","image_3"], variant_rows, "variant_id", "All current SKU/variant rows"),
    "03_product_images.csv": (["image_id","variant_id","product_id","sort_order","image_path"], image_rows, "image_id", "Normalized product gallery images"),
    "04_sizes.csv": (["size_id","size_label","size_type","value_1","value_2","unit","named_value"], size_rows, "size_id", "Unique size dictionary"),
    "05_product_sizes.csv": (["product_id","size_id","size_label"], product_size_rows, "product_id+size_id", "Product-to-size M:N links"),
    "06_colors.csv": (["color_id","color_name","normalized_name"], color_rows, "color_id", "Unique color dictionary"),
    "07_product_colors.csv": (["product_id","color_id","color_name"], product_color_rows, "product_id+color_id", "Product-to-color M:N links"),
    "08_aromas.csv": (["aroma_id","aroma_name","normalized_name"], aroma_rows, "aroma_id", "Unique aroma dictionary"),
    "09_product_aromas.csv": (["product_id","aroma_id","aroma_name"], product_aroma_rows, "product_id+aroma_id", "Product-to-aroma M:N links"),
    "10_materials.csv": (["material_id","material_name","normalized_name"], material_rows, "material_id", "Unique material dictionary"),
    "11_product_materials.csv": (["product_id","material_id","material_name"], product_material_rows, "product_id+material_id", "Product-to-material M:N links"),
    "12_categories.csv": (["category_id","category_name","sort_order"], category_rows, "category_id", "Catalog categories"),
    "13_subcategories.csv": (["subcategory_id","category_id","category_name","subcategory_name","sort_order"], subcategory_rows, "subcategory_id", "Catalog subcategories"),
    "14_collections.csv": (["collection_id","collection_name","sort_order","product_count","variant_count","hero_image"], collection_rows, "collection_id", "Collections derived from catalog"),
    "15_product_collections.csv": (["product_id","collection_id","collection_name"], product_collection_rows, "product_id+collection_id", "Product-to-collection links"),
    "16_capsules.csv": (["capsule_id","capsule_name","sort_order","product_count","variant_count","hero_image"], capsule_rows, "capsule_id", "Capsules derived from catalog"),
    "17_product_capsules.csv": (["product_id","capsule_id","capsule_name"], product_capsule_rows, "product_id+capsule_id", "Product-to-capsule links"),
    "18_ready_solutions.csv": (["solution_id","solution_name","sort_order","required_product_count","optional_product_count","total_product_count","collection_count","capsule_count","description"], ready_solution_rows, "solution_id", "Ready solutions derived from current catalog relations"),
    "19_ready_solution_products.csv": (["solution_id","solution_name","product_id","article","product_name","relation_type"], ready_solution_product_rows, "solution_id+product_id", "Required/optional product links for ready solutions"),
    "20_ready_solution_entities.csv": (["solution_id","solution_name","entity_type","entity_id","entity_name"], ready_solution_entity_rows, "solution_id+entity_type+entity_id", "Collections/capsules participating in each ready solution"),
    "21_constructor_scenarios.csv": (["scenario_id","scenario_name","occasion","guests_supported","lead_collection_slug","entry_collection","styling_message"], scenario_rows, "scenario_id", "Constructor scenario definitions from repository source data"),
    "22_constructor_scenario_items.csv": (["scenario_id","scenario_name","sort_order","preset_status","default_quantity","quantity_rule","variant_selection_required","product_id","article","source_product_name","source_collection","collection_id","product_type","price_rub","product_url","primary_image_url","selection_reason","catalog_match_status"], constructor_item_rows, "scenario_id+sort_order", "Constructor scenario item links"),
    "23_payment_methods.csv": (["payment_method_id","name","timing","instruments","discount_percent","currency","is_active","sort_order"], payment_rows, "payment_method_id", "Live checkout payment options"),
    "24_delivery_methods.csv": (["delivery_method_id","name","min_days","max_days","base_fee_rub","free_from_rub","currency","destination_type","is_active","sort_order"], delivery_rows, "delivery_method_id", "Live checkout delivery options"),
    "25_pricing_rules.csv": (["rule_id","rule_name","condition","effect_type","effect_value","threshold_rub","currency","is_active"], pricing_rows, "rule_id", "Checkout discount and delivery price rules"),
    "26_regions.csv": (["region_id","city","sort_order","has_store","address_suggestion_count","pvz_count","currency","country_code"], region_rows, "region_id", "Cities available in checkout autocomplete"),
    "27_address_suggestions.csv": (["address_id","region_id","city","address","address_type","sort_order"], address_rows, "address_id", "Checkout courier address suggestions"),
    "28_pickup_points.csv": (["point_id","region_id","city","point_type","point_name","address","sort_order"], pickup_rows, "point_id", "PVZ and store pickup options"),
    "29_stores.csv": (["store_id","region_id","city","address","hours","latitude","longitude","is_active"], boutique_rows, "store_id", "Boutiques shown on the site"),
    "30_site_contacts.csv": (["contact_id","contact_type","value","purpose","is_active"], contacts_rows, "contact_id", "Footer contact channels"),
    "31_site_policies.csv": (["policy_id","policy_name","value","unit","is_active"], policy_rows, "policy_id", "Site-level policy/configuration values exposed in UI"),
}

written: list[Path] = []
for filename, (headers, rows, _pk, _desc) in tables.items():
    written.append(write_csv(filename, headers, rows))

relationships = [
    ["02_product_variants.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["03_product_images.csv","variant_id","02_product_variants.csv","variant_id","many-to-one"],
    ["05_product_sizes.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["05_product_sizes.csv","size_id","04_sizes.csv","size_id","many-to-one"],
    ["07_product_colors.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["07_product_colors.csv","color_id","06_colors.csv","color_id","many-to-one"],
    ["09_product_aromas.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["09_product_aromas.csv","aroma_id","08_aromas.csv","aroma_id","many-to-one"],
    ["11_product_materials.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["11_product_materials.csv","material_id","10_materials.csv","material_id","many-to-one"],
    ["13_subcategories.csv","category_id","12_categories.csv","category_id","many-to-one"],
    ["15_product_collections.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["15_product_collections.csv","collection_id","14_collections.csv","collection_id","many-to-one"],
    ["17_product_capsules.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["17_product_capsules.csv","capsule_id","16_capsules.csv","capsule_id","many-to-one"],
    ["19_ready_solution_products.csv","solution_id","18_ready_solutions.csv","solution_id","many-to-one"],
    ["19_ready_solution_products.csv","product_id","01_products.csv","product_id","many-to-one"],
    ["20_ready_solution_entities.csv","solution_id","18_ready_solutions.csv","solution_id","many-to-one"],
    ["22_constructor_scenario_items.csv","scenario_id","21_constructor_scenarios.csv","scenario_id","many-to-one"],
    ["22_constructor_scenario_items.csv","product_id","01_products.csv","product_id","optional many-to-one"],
    ["27_address_suggestions.csv","region_id","26_regions.csv","region_id","many-to-one"],
    ["28_pickup_points.csv","region_id","26_regions.csv","region_id","many-to-one"],
    ["29_stores.csv","region_id","26_regions.csv","region_id","many-to-one"],
]
written.append(write_csv("32_schema_relationships.csv", ["child_table","child_column","parent_table","parent_column","relationship"], relationships))

source_files = sorted(p for p in DATA.glob("*.csv") if p.is_file())
source_rows = [[p.name, p.as_posix().replace(ROOT.as_posix() + "/", ""), p.stat().st_size] for p in source_files]
written.append(write_csv("33_source_tables.csv", ["source_file","repository_path","size_bytes"], source_rows))

manifest_rows: list[list[object]] = []
for filename, (headers, rows, pk, desc) in tables.items():
    manifest_rows.append([filename, desc, pk, len(rows), len(headers), "generated"])
manifest_rows.append(["32_schema_relationships.csv", "Foreign-key relationship map", "child_table+child_column", len(relationships), 5, "generated"])
manifest_rows.append(["33_source_tables.csv", "Original CSV source files already present in public/data", "source_file", len(source_rows), 3, "generated"])
manifest = write_csv("00_database_manifest.csv", ["file_name","description","primary_key","row_count","column_count","source_type"], manifest_rows)
written.insert(0, manifest)

readme_lines = [
    "# Культура дома — CSV database export",
    "",
    "Нормализованный экспорт данных сайта. Разделитель во всех CSV: `;`, кодировка UTF-8 with BOM.",
    "",
    f"- Товарных карточек: {len(product_rows)}",
    f"- SKU/вариантов: {len(variant_rows)}",
    f"- Категорий: {len(category_rows)}",
    f"- Подкатегорий: {len(subcategory_rows)}",
    f"- Коллекций: {len(collection_rows)}",
    f"- Капсул: {len(capsule_rows)}",
    f"- Готовых решений: {len(ready_solution_rows)}",
    f"- Регионов checkout: {len(region_rows)}",
    "",
    "Начните с `00_database_manifest.csv` и `32_schema_relationships.csv`.",
    "",
    "Источники: `public/data/catalog_master.csv`, текущие CSV конструктора в `public/data/`, и конфигурация checkout/бутиков из `app/page.tsx`.",
]
readme = OUT / "README.md"
readme.write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

# Deterministic ZIP so repeated builds do not generate spurious changes.
zip_path = OUT / "kultura_doma_site_database_csv.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in sorted(written + [readme], key=lambda p: p.name):
        info = zipfile.ZipInfo(f"database/{path.name}")
        info.date_time = (1980, 1, 1, 0, 0, 0)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, path.read_bytes())
    for path in source_files:
        info = zipfile.ZipInfo(f"source/{path.name}")
        info.date_time = (1980, 1, 1, 0, 0, 0)
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, path.read_bytes())

print(
    "// SITE_DATABASE_V126: "
    f"tables={len(written)}; products={len(product_rows)}; variants={len(variant_rows)}; "
    f"ready_solutions={len(ready_solution_rows)}; regions={len(region_rows)}; zip={zip_path.relative_to(ROOT)}"
)
