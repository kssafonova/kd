from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "public" / "data" / "database"
OUT = DB / "site_runtime.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh, delimiter=";")]


def table_key(path: Path) -> str:
    return re.sub(r"^\d+_", "", path.stem)


def as_int(value: object, default: int = 0) -> int:
    try:
        return int(float(str(value or "0").replace(",", ".")))
    except ValueError:
        return default


def stable_number(value: str) -> int:
    return 300000 + int(hashlib.sha1(value.encode("utf-8")).hexdigest()[:8], 16) % 500000


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        item = str(value or "").strip()
        if item and item not in seen:
            seen.add(item)
            result.append(item)
    return result


csv_paths = sorted(DB.glob("[0-9][0-9]_*.csv"))
if not csv_paths:
    raise SystemExit("SITE_RUNTIME_V128: database CSV tables not found")

tables: dict[str, list[dict[str, str]]] = {table_key(path): read_csv(path) for path in csv_paths}
required_tables = {
    "products", "product_variants", "collections", "capsules", "ready_solutions",
    "ready_solution_products", "payment_methods", "delivery_methods", "pricing_rules",
    "regions", "address_suggestions", "pickup_points", "stores", "site_contacts", "site_policies",
}
missing = sorted(required_tables - set(tables))
if missing:
    raise SystemExit(f"SITE_RUNTIME_V128: missing tables: {','.join(missing)}")

product_rows = tables["products"]
variant_rows = tables["product_variants"]
product_by_id = {row.get("product_id", ""): row for row in product_rows}
variants_by_product: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in variant_rows:
    variants_by_product[row.get("product_id", "")].append(row)

collections_by_product: dict[str, list[str]] = defaultdict(list)
for row in tables.get("product_collections", []):
    collections_by_product[row.get("product_id", "")].append(row.get("collection_name", ""))
capsules_by_product: dict[str, list[str]] = defaultdict(list)
for row in tables.get("product_capsules", []):
    capsules_by_product[row.get("product_id", "")].append(row.get("capsule_name", ""))

required_by_product: dict[str, list[str]] = defaultdict(list)
optional_by_product: dict[str, list[str]] = defaultdict(list)
solution_product_rows = tables.get("ready_solution_products", [])
for row in solution_product_rows:
    product_id = row.get("product_id", "")
    name = row.get("solution_name", "")
    if row.get("relation_type") == "required":
        required_by_product[product_id].append(name)
    else:
        optional_by_product[product_id].append(name)

products: list[dict[str, object]] = []
for product in product_rows:
    product_id = product.get("product_id", "")
    article = product.get("article", "") or product_id
    variants: list[dict[str, object]] = []
    for row in sorted(variants_by_product.get(product_id, []), key=lambda item: as_int(item.get("variant_order"), 0)):
        photos = unique([row.get("image_1", ""), row.get("image_2", ""), row.get("image_3", "")])
        variants.append({
            "id": row.get("variant_id", ""),
            "variantKey": row.get("variant_id", ""),
            "offerId": row.get("variant_id", ""),
            "article": article,
            "name": product.get("name", ""),
            "color": row.get("color_name", ""),
            "aroma": row.get("aroma_name", ""),
            "size": row.get("size_label", ""),
            "price": as_int(row.get("price_rub"), 0),
            "oldPrice": as_int(row.get("old_price_rub"), 0) or None,
            "height": row.get("height", ""),
            "width": row.get("width", ""),
            "volume": row.get("volume", ""),
            "diameter": row.get("diameter", ""),
            "packageInfo": row.get("package_info", ""),
            "material": row.get("material_name", ""),
            "composition": row.get("composition", ""),
            "details": row.get("details", ""),
            "collection": row.get("collection_name", ""),
            "capsule": row.get("capsule_name", ""),
            "category": row.get("category_name", ""),
            "subcategory": row.get("subcategory_name", ""),
            "readyRequired": unique(required_by_product.get(product_id, [])),
            "readyOptional": unique(optional_by_product.get(product_id, [])),
            "photos": photos,
        })
    products.append({
        "key": article,
        "id": stable_number(article),
        "article": article,
        "name": product.get("name", ""),
        "category": product.get("category_name", ""),
        "subcategory": product.get("subcategory_name", ""),
        "collections": unique(collections_by_product.get(product_id, []) + [product.get("collection_name", "")]),
        "capsules": unique(capsules_by_product.get(product_id, []) + [product.get("capsule_name", "")]),
        "readyRequired": unique(required_by_product.get(product_id, [])),
        "readyOptional": unique(optional_by_product.get(product_id, [])),
        "variants": variants,
    })

product_key_by_id = {str(item["article"]): str(item["key"]) for item in products}
variant_count_by_product = {str(item["article"]): len(item["variants"]) for item in products}
primary_image_by_product = {row.get("product_id", ""): row.get("primary_image", "") for row in product_rows}

collection_links: dict[str, list[str]] = defaultdict(list)
for row in tables.get("product_collections", []):
    collection_links[row.get("collection_name", "")].append(row.get("product_id", ""))
collections = [{
    "name": row.get("collection_name", ""),
    "type": "collection",
    "productKeys": [product_key_by_id.get(pid, pid) for pid in unique(collection_links.get(row.get("collection_name", ""), []))],
    "heroImage": row.get("hero_image", ""),
    "variantCount": as_int(row.get("variant_count"), 0),
} for row in tables.get("collections", [])]

capsule_links: dict[str, list[str]] = defaultdict(list)
for row in tables.get("product_capsules", []):
    capsule_links[row.get("capsule_name", "")].append(row.get("product_id", ""))
capsules = [{
    "name": row.get("capsule_name", ""),
    "type": "capsule",
    "productKeys": [product_key_by_id.get(pid, pid) for pid in unique(capsule_links.get(row.get("capsule_name", ""), []))],
    "heroImage": row.get("hero_image", ""),
    "variantCount": as_int(row.get("variant_count"), 0),
} for row in tables.get("capsules", [])]

solution_links: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"required": [], "optional": []})
for row in solution_product_rows:
    solution_links[row.get("solution_id", "")]["required" if row.get("relation_type") == "required" else "optional"].append(row.get("product_id", ""))
solution_entities: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"collection": [], "capsule": []})
for row in tables.get("ready_solution_entities", []):
    entity_type = row.get("entity_type", "")
    if entity_type in {"collection", "capsule"}:
        solution_entities[row.get("solution_id", "")][entity_type].append(row.get("entity_name", ""))

def solution_space(product_ids: list[str]) -> str:
    categories = " ".join(product_by_id.get(pid, {}).get("category_name", "").lower() for pid in product_ids)
    if "постель" in categories or "плед" in categories:
        return "Спальня и гостиная"
    if "посуда" in categories or "столов" in categories:
        return "Кухня и столовая"
    return "Интерьер"

ready_solutions: list[dict[str, object]] = []
for row in tables.get("ready_solutions", []):
    sid = row.get("solution_id", "")
    required = unique(solution_links[sid]["required"])
    optional = unique(solution_links[sid]["optional"])
    linked = required + [pid for pid in optional if pid not in required]
    hero = next((primary_image_by_product.get(pid, "") for pid in linked if primary_image_by_product.get(pid, "")), "")
    ready_solutions.append({
        "id": sid,
        "name": row.get("solution_name", ""),
        "space": solution_space(linked),
        "requiredProductKeys": [product_key_by_id.get(pid, pid) for pid in required],
        "optionalProductKeys": [product_key_by_id.get(pid, pid) for pid in optional],
        "collections": unique(solution_entities[sid]["collection"]),
        "capsules": unique(solution_entities[sid]["capsule"]),
        "heroImage": hero,
        "requiredVariantCount": sum(variant_count_by_product.get(pid, 0) for pid in required),
        "optionalVariantCount": sum(variant_count_by_product.get(pid, 0) for pid in optional),
        "description": row.get("description", ""),
    })

solution_descriptions = {row.get("solution_name", ""): row.get("description", "") for row in tables.get("ready_solutions", [])}
catalog_rows: list[dict[str, str]] = []
for row in variant_rows:
    pid = row.get("product_id", "")
    product = product_by_id.get(pid, {})
    required_names = unique(required_by_product.get(pid, []))
    optional_names = unique(optional_by_product.get(pid, []))
    descriptions = unique([solution_descriptions.get(name, "") for name in required_names + optional_names])
    catalog_rows.append({
        "Артикул": row.get("article", "") or product.get("article", ""),
        "Название товара": product.get("name", ""),
        "Цвет": row.get("color_name", ""),
        "Аромат": row.get("aroma_name", ""),
        "Размер": row.get("size_label", ""),
        "Цена": row.get("price_rub", ""),
        "Старая цена": row.get("old_price_rub", ""),
        "Высота": row.get("height", ""),
        "Ширина": row.get("width", ""),
        "Объем": row.get("volume", ""),
        "Диаметр": row.get("diameter", ""),
        "Комплектация / информация о размере": row.get("package_info", ""),
        "Материал": row.get("material_name", ""),
        "Состав": row.get("composition", ""),
        "Детали": row.get("details", ""),
        "Коллекция": row.get("collection_name", ""),
        "Капсула": row.get("capsule_name", ""),
        "Категория": row.get("category_name", ""),
        "Подкатегория": row.get("subcategory_name", ""),
        "Товар входит в готовое решение": "\n".join(required_names),
        "Опционально входит в готовое решение": "\n".join(optional_names),
        "Фото 1": row.get("image_1", ""),
        "Фото 2": row.get("image_2", ""),
        "Фото 3": row.get("image_3", ""),
        "Описание готового решения": "\n".join(descriptions),
    })

runtime = {
    "version": "128",
    "source": "public/data/database/*.csv",
    "tableCount": len(tables),
    "tables": tables,
    "catalogRows": catalog_rows,
    "variantCount": len(variant_rows),
    "productCount": len(product_rows),
    "products": products,
    "collections": collections,
    "capsules": capsules,
    "readySolutions": ready_solutions,
}
OUT.write_text(json.dumps(runtime, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"// SITE_RUNTIME_V128: tables={len(tables)}; products={len(products)}; variants={len(variant_rows)}; ready_solutions={len(ready_solutions)}; output={OUT.relative_to(ROOT)}")
