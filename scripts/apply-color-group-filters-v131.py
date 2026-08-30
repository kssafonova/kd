from __future__ import annotations

from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "public" / "data" / "database"
FDB = ROOT / "public" / "data" / "filter-database"
PAGE = ROOT / "app" / "page.tsx"
GENERATED = ROOT / "app" / "site-database.generated.ts"


def clean(value: object) -> str:
    return str(value or "").strip().replace("\ufeff", "")


def norm(value: object) -> str:
    return re.sub(r"\s+", " ", clean(value).lower().replace("ё", "е")).strip()


def stable_id(prefix: str, value: str) -> str:
    return f"{prefix}_{hashlib.sha1(norm(value).encode('utf-8')).hexdigest()[:10]}"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        return list(reader.fieldnames or []), [{k: clean(v) for k, v in row.items()} for row in reader]


def write_csv(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh, delimiter=";", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


GROUPS = [
    ("Синий", "#35546F", 1),
    ("Голубой", "#AFC9D7", 2),
    ("Белый", "#F5F3EE", 3),
    ("Бежевый", "#D7C3A5", 4),
    ("Коричневый", "#6F4E37", 5),
    ("Черный", "#1E1E1E", 6),
    ("Пудровый", "#D8B7AE", 7),
    ("Зеленый", "#72816B", 8),
    ("Красный", "#9A443B", 9),
    ("Желтый", "#D2B65C", 10),
    ("Золотой", "#C3A05B", 11),
    ("Серебряный", "#B7B9B8", 12),
    ("Прозрачный", "#F4F4F2", 13),
]
GROUP_BY_NAME = {norm(name): (stable_id("cgrp", name), name, hex_value, order) for name, hex_value, order in GROUPS}


def group_for_atom(value: str) -> tuple[str, str, str, int]:
    n = norm(value)
    if any(token in n for token in ("серо-синий", "ночной синий")) or n == "синий":
        return GROUP_BY_NAME[norm("Синий")]
    if any(token in n for token in ("ледяной голубой", "небесный")) or n == "голубой":
        return GROUP_BY_NAME[norm("Голубой")]
    if any(token in n for token in ("молочный", "экрю")) or n == "белый":
        return GROUP_BY_NAME[norm("Белый")]
    aliases = {
        "бежевый": "Бежевый", "коричневый": "Коричневый", "черный": "Черный",
        "пудровый": "Пудровый", "зеленый": "Зеленый", "красный": "Красный",
        "желтый": "Желтый", "золотой": "Золотой", "серебряный": "Серебряный",
        "прозрачный": "Прозрачный",
    }
    for token, group_name in aliases.items():
        if token in n:
            return GROUP_BY_NAME[norm(group_name)]
    # Unknown future shade: retain a stable standalone group instead of dropping it.
    name = clean(value) or "Другой"
    return stable_id("cgrp", name), name, "#D8D5CF", 999


def groups_for_raw(value: str) -> list[tuple[str, str, str, int]]:
    parts = [clean(part) for part in re.split(r"\s*/\s*", clean(value)) if clean(part)]
    if not parts and clean(value):
        parts = [clean(value)]
    result: list[tuple[str, str, str, int]] = []
    seen: set[str] = set()
    for part in parts:
        group = group_for_atom(part)
        if group[0] not in seen:
            seen.add(group[0])
            result.append(group)
    return result


# ----- Main site database color group tables -----
color_headers, color_rows = read_csv(DB / "06_colors.csv")
if not color_rows:
    raise SystemExit("CATALOG_COLOR_GROUPS_V131: public/data/database/06_colors.csv is missing or empty")

all_groups = {group[0]: group for group in GROUP_BY_NAME.values()}
member_rows: list[list[object]] = []
for row in color_rows:
    raw = row.get("color_name", "")
    for group in groups_for_raw(raw):
        all_groups[group[0]] = group
        member_rows.append([row.get("color_id", ""), raw, group[0], group[1]])

group_rows = sorted(all_groups.values(), key=lambda item: (item[3], item[1]))
write_csv(DB / "34_color_groups.csv", ["group_id", "group_name", "normalized_name", "swatch_hex", "sort_order"], [[gid, name, norm(name), hex_value, order] for gid, name, hex_value, order in group_rows])
write_csv(DB / "35_color_group_members.csv", ["color_id", "color_name", "group_id", "group_name"], member_rows)

_, product_color_rows = read_csv(DB / "07_product_colors.csv")
product_group_rows: list[list[object]] = []
seen_pg: set[tuple[str, str]] = set()
for row in product_color_rows:
    product_id, raw = row.get("product_id", ""), row.get("color_name", "")
    for group in groups_for_raw(raw):
        key = (product_id, group[0])
        if key not in seen_pg:
            seen_pg.add(key)
            product_group_rows.append([product_id, group[0], group[1]])
write_csv(DB / "36_product_color_groups.csv", ["product_id", "group_id", "group_name"], product_group_rows)

manifest_path = DB / "00_database_manifest.csv"
manifest_headers, manifest = read_csv(manifest_path)
manifest = [row for row in manifest if row.get("file_name") not in {"34_color_groups.csv", "35_color_group_members.csv", "36_product_color_groups.csv"}]
manifest.extend([
    {"file_name":"34_color_groups.csv","description":"Canonical grouped colors used by the catalog filter","primary_key":"group_id","row_count":str(len(group_rows)),"column_count":"5","source_type":"generated"},
    {"file_name":"35_color_group_members.csv","description":"Raw catalog colors to grouped filter colors M:N relation","primary_key":"color_id+group_id","row_count":str(len(member_rows)),"column_count":"4","source_type":"generated"},
    {"file_name":"36_product_color_groups.csv","description":"Product-to-grouped-color M:N relation for catalog filtering","primary_key":"product_id+group_id","row_count":str(len(product_group_rows)),"column_count":"3","source_type":"generated"},
])
write_csv(manifest_path, manifest_headers, [[row.get(h, "") for h in manifest_headers] for row in manifest])

rel_path = DB / "32_schema_relationships.csv"
rel_headers, relations = read_csv(rel_path)
extra_relations = [
    ["35_color_group_members.csv", "color_id", "06_colors.csv", "color_id", "many-to-one"],
    ["35_color_group_members.csv", "group_id", "34_color_groups.csv", "group_id", "many-to-one"],
    ["36_product_color_groups.csv", "product_id", "01_products.csv", "product_id", "many-to-one"],
    ["36_product_color_groups.csv", "group_id", "34_color_groups.csv", "group_id", "many-to-one"],
]
existing_rel = {(row.get("child_table", ""), row.get("child_column", ""), row.get("parent_table", ""), row.get("parent_column", "")) for row in relations}
for rel in extra_relations:
    if tuple(rel[:4]) not in existing_rel:
        relations.append(dict(zip(rel_headers, rel)))
write_csv(rel_path, rel_headers, [[row.get(h, "") for h in rel_headers] for row in relations])

# ----- Filter database: expose grouped colors rather than marketing shade names -----
_, f_colors = read_csv(FDB / "05_colors.csv")
filter_group_counts: dict[str, dict[str, object]] = {gid: {"group": group, "product_count": 0, "variant_count": 0} for gid, group in all_groups.items()}
for row in f_colors:
    group = group_for_atom(row.get("color_label", ""))
    bucket = filter_group_counts.setdefault(group[0], {"group": group, "product_count": 0, "variant_count": 0})
    bucket["product_count"] = int(bucket["product_count"]) + int(row.get("product_count") or 0)
    bucket["variant_count"] = int(bucket["variant_count"]) + int(row.get("variant_count") or 0)

f_group_rows = []
for bucket in filter_group_counts.values():
    gid, name, hex_value, order = bucket["group"]  # type: ignore[misc]
    f_group_rows.append([gid, norm(name), name, re.sub(r"[^a-z0-9]+", "-", norm(name)).strip("-") or gid, hex_value, order, bucket["product_count"], bucket["variant_count"]])
f_group_rows.sort(key=lambda row: (int(row[5]), str(row[2])))
write_csv(FDB / "21_color_groups.csv", ["group_id", "normalized_key", "group_label", "slug", "swatch_hex", "sort_order", "product_count_sum", "variant_count_sum"], f_group_rows)

_, f_variant_colors = read_csv(FDB / "06_variant_colors.csv")
variant_group_rows: list[list[object]] = []
seen_vg: set[tuple[str, str]] = set()
for row in f_variant_colors:
    group = group_for_atom(row.get("color_label", ""))
    key = (row.get("variant_id", ""), group[0])
    if key not in seen_vg:
        seen_vg.add(key)
        variant_group_rows.append([row.get("variant_id", ""), row.get("product_id", ""), group[0], group[1], row.get("source_color_raw", "")])
write_csv(FDB / "22_variant_color_groups.csv", ["variant_id", "product_id", "group_id", "group_label", "source_color_raw"], variant_group_rows)

config_path = FDB / "03_filter_config.csv"
config_headers, config_rows = read_csv(config_path)
for row in config_rows:
    if row.get("filter_code") == "color":
        row["source"] = "variant_color_groups.group_id"
write_csv(config_path, config_headers, [[row.get(h, "") for h in config_headers] for row in config_rows])

f_manifest_path = FDB / "00_manifest.csv"
f_manifest_headers, f_manifest = read_csv(f_manifest_path)
f_manifest = [row for row in f_manifest if row.get("file_name") not in {"21_color_groups.csv", "22_variant_color_groups.csv"}]
f_manifest.extend([
    {"file_name":"21_color_groups.csv","description":"Grouped colors displayed in the catalog filter","primary_key":"group_id","row_count":str(len(f_group_rows))},
    {"file_name":"22_variant_color_groups.csv","description":"Variant-to-grouped-color M:N relation","primary_key":"variant_id+group_id","row_count":str(len(variant_group_rows))},
])
write_csv(f_manifest_path, f_manifest_headers, [[row.get(h, "") for h in f_manifest_headers] for row in f_manifest])

# ----- Generated TS: expose color group tables as connected site data -----
groups_json = json.dumps([{k: str(v) for k, v in zip(["group_id","group_name","normalized_name","swatch_hex","sort_order"], row)} for row in [[gid, name, norm(name), hex_value, order] for gid, name, hex_value, order in group_rows]], ensure_ascii=False, separators=(",", ":"))
members_json = json.dumps([{k: str(v) for k, v in zip(["color_id","color_name","group_id","group_name"], row)} for row in member_rows], ensure_ascii=False, separators=(",", ":"))
generated = GENERATED.read_text(encoding="utf-8")
if "SITE_DB_COLOR_GROUPS" not in generated:
    anchor = "export const SITE_DB_COLORS = "
    pos = generated.find(anchor)
    if pos < 0:
        raise SystemExit("CATALOG_COLOR_GROUPS_V131: SITE_DB_COLORS export not found")
    line_end = generated.find("\n", pos)
    insertion = f'\nexport const SITE_DB_COLOR_GROUPS = {groups_json} as SiteDatabaseRow[];\nexport const SITE_DB_COLOR_GROUP_MEMBERS = {members_json} as SiteDatabaseRow[];'
    generated = generated[:line_end] + insertion + generated[line_end:]
    GENERATED.write_text(generated, encoding="utf-8")

# ----- Catalog runtime filter: group shades under one filter value -----
text = PAGE.read_text(encoding="utf-8")
import_old = 'SITE_DB_STORES, SITE_DB_STORE_POINTS } from "./site-database.generated";'
import_new = 'SITE_DB_STORES, SITE_DB_STORE_POINTS, SITE_DB_COLOR_GROUPS, SITE_DB_COLOR_GROUP_MEMBERS } from "./site-database.generated";'
if import_old in text:
    text = text.replace(import_old, import_new, 1)
elif "SITE_DB_COLOR_GROUPS" not in text.split("\n", 8)[4:8].__str__():
    raise SystemExit("CATALOG_COLOR_GROUPS_V131: site database import signature not found")

if "// CATALOG_COLOR_GROUPS_V131" not in text:
    helper_anchor = 'const catalogSkuColorV123=(sku:CatalogSku)=>cleanNulls(asVariantSku(sku)?.sourceColor)??cleanNulls(sku.color)??"";'
    helper = r'''
// CATALOG_COLOR_GROUPS_V131
const catalogColorGroupMembersV131=(()=>{
  const map=new Map<string,string[]>();
  SITE_DB_COLOR_GROUP_MEMBERS.forEach(row=>{
    const key=facetNormV123(row.color_name),name=cleanNulls(row.group_name);
    if(!key||!name)return;
    const list=map.get(key)??[];
    if(!list.some(item=>sameFacetV123(item,name)))list.push(name);
    map.set(key,list);
  });
  return map;
})();
const catalogColorGroupHexesV131=new Map(SITE_DB_COLOR_GROUPS.map(row=>[facetNormV123(row.group_name),row.swatch_hex||"#e8e5df"]));
const catalogSkuColorGroupsV131=(sku:CatalogSku)=>{
  const raw=catalogSkuColorV123(sku),exact=catalogColorGroupMembersV131.get(facetNormV123(raw));
  if(exact?.length)return exact;
  const groups=raw.split(/\s*\/\s*/).flatMap(part=>catalogColorGroupMembersV131.get(facetNormV123(part))??[part]).filter(Boolean);
  return uniqueFacetValuesV123(groups);
};
const catalogColorGroupHexV131=(name:string)=>catalogColorGroupHexesV131.get(facetNormV123(name))??"#e8e5df";
const normalizeCatalogColorFiltersV131=(values:string[])=>uniqueFacetValuesV123(values.flatMap(value=>catalogColorGroupMembersV131.get(facetNormV123(value))??[value]));'''
    if helper_anchor not in text:
        raise SystemExit("CATALOG_COLOR_GROUPS_V131: catalogSkuColorV123 anchor not found")
    text = text.replace(helper_anchor, helper_anchor + helper, 1)

    old_match = '  const color=catalogSkuColorV123(sku);\n  const price=Number(sku.price)||0;'
    new_match = '  const color=catalogSkuColorV123(sku);\n  const colorGroups=catalogSkuColorGroupsV131(sku);\n  const price=Number(sku.price)||0;'
    if old_match not in text:
        raise SystemExit("CATALOG_COLOR_GROUPS_V131: sku color match anchor not found")
    text = text.replace(old_match, new_match, 1)
    text = text.replace('if(ignore!=="color"&&filters.colors.length&&!filters.colors.some(value=>sameFacetV123(value,color)))return false;', 'if(ignore!=="color"&&filters.colors.length&&!filters.colors.some(value=>colorGroups.some(group=>sameFacetV123(value,group))))return false;', 1)
    text = text.replace('if(forced?.group==="color"&&!sameFacetV123(color,forced.value))return false;', 'if(forced?.group==="color"&&!colorGroups.some(group=>sameFacetV123(group,forced.value)))return false;', 1)

    old_parse = 'colors:list("color"),priceFrom:params.get("price_from")??"",priceTo:params.get("price_to")??""};'
    new_parse = 'colors:normalizeCatalogColorFiltersV131(list("color")),priceFrom:params.get("price_from")??"",priceTo:params.get("price_to")??""};'
    if old_parse not in text:
        raise SystemExit("CATALOG_COLOR_GROUPS_V131: URL color parse anchor not found")
    text = text.replace(old_parse, new_parse, 1)

    old_options = '  const colorOptions=uniqueFacetValuesV123(skus.map(sku=>catalogSkuColorV123(sku)));\n  const colorHexes=new Map<string,string>();\n  skus.forEach(sku=>{const color=catalogSkuColorV123(sku);if(color&&!colorHexes.has(facetNormV123(color)))colorHexes.set(facetNormV123(color),sku.colorHex||"#e8e5df")});'
    new_options = '  const colorOptions=uniqueFacetValuesV123(skus.flatMap(sku=>catalogSkuColorGroupsV131(sku)));\n  const colorHexes=new Map<string,string>();\n  colorOptions.forEach(color=>colorHexes.set(facetNormV123(color),catalogColorGroupHexV131(color)));'
    if old_options not in text:
        raise SystemExit("CATALOG_COLOR_GROUPS_V131: color option anchor not found")
    text = text.replace(old_options, new_options, 1)

PAGE.write_text(text, encoding="utf-8")
print(f"// CATALOG_COLOR_GROUPS_V131: groups={len(group_rows)}; color_members={len(member_rows)}; product_links={len(product_group_rows)}; variant_links={len(variant_group_rows)}; blue_group=Синий+Серо-синий+Ночной синий")
