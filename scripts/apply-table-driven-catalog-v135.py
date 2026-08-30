from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import csv
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "public" / "data" / "database"
PAGE = ROOT / "app" / "page.tsx"
GENERATED = ROOT / "app" / "site-database.generated.ts"
RUNTIME = DB / "site_runtime.json"
VARIANTS = DB / "02_product_variants.csv"
IMAGES = DB / "03_product_images.csv"
MARKER = "// TABLE_DRIVEN_CATALOG_IMAGES_V135"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"TABLE_DRIVEN_CATALOG_IMAGES_V135: missing {path.relative_to(ROOT)}")
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(fh, delimiter=";")]


def as_int(value: object) -> int:
    try:
        return int(float(str(value or "0").replace(",", ".")))
    except ValueError:
        return 0


variant_rows = read_csv(VARIANTS)
image_rows = read_csv(IMAGES)
variant_by_id = {row["variant_id"]: row for row in variant_rows if row.get("variant_id")}
images_by_variant: dict[str, list[dict[str, str]]] = defaultdict(list)

for row in image_rows:
    variant_id = row.get("variant_id", "")
    if variant_id not in variant_by_id:
        raise SystemExit(f"TABLE_DRIVEN_CATALOG_IMAGES_V135: image references unknown variant {variant_id}")
    expected_product = variant_by_id[variant_id].get("product_id", "")
    if row.get("product_id", "") != expected_product:
        raise SystemExit(
            f"TABLE_DRIVEN_CATALOG_IMAGES_V135: product mismatch for {variant_id}: "
            f"{row.get('product_id','')} != {expected_product}"
        )
    if not row.get("image_path", ""):
        raise SystemExit(f"TABLE_DRIVEN_CATALOG_IMAGES_V135: empty image_path for {row.get('image_id','')}")
    images_by_variant[variant_id].append(row)

for variant_id, rows in images_by_variant.items():
    rows.sort(key=lambda row: (as_int(row.get("sort_order")), row.get("image_id", "")))
    orders = [as_int(row.get("sort_order")) for row in rows]
    if len(orders) != len(set(orders)):
        raise SystemExit(f"TABLE_DRIVEN_CATALOG_IMAGES_V135: duplicate image sort_order for {variant_id}")

# The modern catalog must never fall back to legacy catalog chunks. This block is
# intentionally idempotent: newer catalog loaders may wrap the same database-only
# contract with runtime/base-path resilience and build-time embedded data.
page = PAGE.read_text(encoding="utf-8")
legacy_block = '''  const chunks=await Promise.all(CATALOG_MASTER_FILES.map(async fileName=>{
    try{const response=await fetch(`${base}/data/${fileName}`,{cache:"no-store"});if(!response.ok)return [];return parseEntityCsv(await response.text())}catch{return []}
  }));
  const databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);
  const sourceRows=databaseRows.length?databaseRows:chunks.flat();'''
strict_block = '''  const databaseRows=await loadSiteDatabaseCatalogRows(base).catch(()=>[] as CatalogMasterRow[]);
  const sourceRows=databaseRows;'''
if legacy_block in page:
    page = page.replace(legacy_block, strict_block, 1)
elif strict_block not in page:
    modern_database_contract = (
        "loadSiteDatabaseCatalogRows(base)" in page
        and "const sourceRows=databaseRows;" in page
        and "CATALOG_MASTER_FILES.map" not in page
    )
    if not modern_database_contract:
        raise SystemExit("TABLE_DRIVEN_CATALOG_IMAGES_V135: catalog source block not found")
if MARKER not in page:
    anchor = "// SITE_DATABASE_CONNECTED_V128"
    if anchor not in page:
        raise SystemExit("TABLE_DRIVEN_CATALOG_IMAGES_V135: site database marker not found")
    page = page.replace(anchor, anchor + "\n" + MARKER, 1)
PAGE.write_text(page, encoding="utf-8")

# apply-site-database-v128.py regenerates this module on every build. Replace
# only its catalog loader after generation, and source gallery data exclusively
# from 03_product_images.csv. No product.primary_image, variant.image_N or
# hard-coded image fallback is allowed here.
generated = GENERATED.read_text(encoding="utf-8")
strict_loader = r'''export async function loadSiteDatabaseCatalogRows(base=""):Promise<SiteDatabaseRow[]> {
  const [products,variants,images,solutions,links]=await Promise.all([
    fetchSiteDbTable(base,"01_products.csv"),
    fetchSiteDbTable(base,"02_product_variants.csv"),
    fetchSiteDbTable(base,"03_product_images.csv"),
    fetchSiteDbTable(base,"18_ready_solutions.csv"),
    fetchSiteDbTable(base,"19_ready_solution_products.csv"),
  ]);
  if(!products.length||!variants.length)return [];
  const productMap=new Map(products.map(row=>[row.product_id,row]));
  const solutionMap=new Map(solutions.map(row=>[row.solution_id,row]));
  const imageMap=new Map<string,SiteDatabaseRow[]>();
  images.forEach(image=>{const list=imageMap.get(image.variant_id)??[];list.push(image);imageMap.set(image.variant_id,list)});
  imageMap.forEach(list=>list.sort((a,b)=>Number(a.sort_order||0)-Number(b.sort_order||0)));
  const required=new Map<string,string[]>(),optional=new Map<string,string[]>(),descriptions=new Map<string,string>();
  links.forEach(link=>{
    const target=link.relation_type==="optional"?optional:required;
    const list=target.get(link.product_id)??[];if(link.solution_name&&!list.includes(link.solution_name))list.push(link.solution_name);target.set(link.product_id,list);
    const desc=solutionMap.get(link.solution_id)?.description;if(desc&&!descriptions.has(link.product_id))descriptions.set(link.product_id,desc);
  });
  return variants.map(variant=>{
    const product=productMap.get(variant.product_id)??{};
    const photos=imageMap.get(variant.variant_id)??[];
    const photo=(order:number)=>photos.find(row=>Number(row.sort_order||0)===order)?.image_path??"";
    return {
      "Артикул":variant.article||variant.product_id,
      "Название товара":product.name||"",
      "Цвет":variant.color_name||"",
      "Аромат":variant.aroma_name||"",
      "Размер":variant.size_label||"",
      "Цена":variant.price_rub||"",
      "Старая цена":variant.old_price_rub||"",
      "Высота":variant.height||"",
      "Ширина":variant.width||"",
      "Объем":variant.volume||"",
      "Диаметр":variant.diameter||"",
      "Комплектация / информация о размере":variant.package_info||"",
      "Материал":variant.material_name||"",
      "Состав":variant.composition||"",
      "Детали":variant.details||"",
      "Коллекция":variant.collection_name||"",
      "Капсула":variant.capsule_name||"",
      "Категория":variant.category_name||product.category_name||"",
      "Подкатегория":variant.subcategory_name||product.subcategory_name||"",
      "Товар входит в готовое решение":(required.get(variant.product_id)??[]).join("\n"),
      "Опционально входит в готовое решение":(optional.get(variant.product_id)??[]).join("\n"),
      "Фото 1":photo(1),
      "Фото 2":photo(2),
      "Фото 3":photo(3),
      "Описание готового решения":descriptions.get(variant.product_id)||"",
    };
  });
}
'''
loader_pattern = r'export async function loadSiteDatabaseCatalogRows\(base=""\):Promise<SiteDatabaseRow\[]> \{.*?\n\}\n'
generated, count = re.subn(loader_pattern, lambda _match: strict_loader, generated, count=1, flags=re.S)
if count != 1:
    raise SystemExit("TABLE_DRIVEN_CATALOG_IMAGES_V135: generated catalog loader not found")
if MARKER not in generated:
    generated = generated.replace(
        "/* SITE_DATABASE_GENERATED_V128",
        "/* SITE_DATABASE_GENERATED_V128\n   TABLE_DRIVEN_CATALOG_IMAGES_V135: catalog gallery source is 03_product_images.csv only.",
        1,
    )
GENERATED.write_text(generated, encoding="utf-8")

# site_runtime.json powers the database-driven collection/capsule/ready-solution
# consumers. Keep its product galleries under the same strict contract so every
# commerce surface resolves a variant's photos from 03_product_images.csv.
if RUNTIME.exists():
    runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
    for product in runtime.get("products", []):
        for variant in product.get("variants", []):
            variant_id = str(variant.get("id", ""))
            variant["photos"] = [row["image_path"] for row in images_by_variant.get(variant_id, [])]
    catalog_rows = runtime.get("catalogRows", [])
    if len(catalog_rows) != len(variant_rows):
        raise SystemExit(
            f"TABLE_DRIVEN_CATALOG_IMAGES_V135: runtime catalog row mismatch "
            f"{len(catalog_rows)} != {len(variant_rows)}"
        )
    for catalog_row, variant in zip(catalog_rows, variant_rows):
        photos = [row["image_path"] for row in images_by_variant.get(variant.get("variant_id", ""), [])]
        catalog_row["Фото 1"] = photos[0] if len(photos) > 0 else ""
        catalog_row["Фото 2"] = photos[1] if len(photos) > 1 else ""
        catalog_row["Фото 3"] = photos[2] if len(photos) > 2 else ""
    runtime["source"] = "public/data/database/*.csv; product photos strictly from 03_product_images.csv"
    runtime["imageSourceTable"] = "03_product_images.csv"
    runtime["imageRowCount"] = len(image_rows)
    RUNTIME.write_text(json.dumps(runtime, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

print(
    "// TABLE_DRIVEN_CATALOG_IMAGES_V135: "
    f"variants={len(variant_rows)}; image_rows={len(image_rows)}; "
    f"variants_with_images={len(images_by_variant)}; catalog_source=database_only; image_source=03_product_images.csv"
)
