from pathlib import Path

root = Path(__file__).resolve().parents[1]
data_path = root / "app" / "constructor" / "data-client.ts"
client_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"

data = data_path.read_text(encoding="utf-8")
client = client_path.read_text(encoding="utf-8")

# Ready Solutions must be able to use legacy source collection names from the
# merchandising CSV (Мокоши / Камея / Жар-птица / Овация). The ordinary
# constructor/storefront filter remains intact in loadConstructorData; only the
# final merchandising catalog used by Ready Solutions keeps the raw CSV rows.
data = data.replace(
    "return { summaries, variants, catalog: filterCatalogRows(catalog) };",
    "return { summaries, variants, catalog };",
)

# Current public-facing collection aliases. Source names remain untouched for
# matching CSV rows; only labels and product names are transformed in the UI.
client = client.replace(
    'const COLLECTION_LABELS: Record<string, string> = { "Мокоши": "Символы", "Камея": "Эхо", "Жар-птица": "Феникс" };',
    'const COLLECTION_LABELS: Record<string, string> = { "Мокоши": "Символы", "Камея": "Эхо", "Жар-птица": "Феникс", "Дияф": "Диаф" };',
)

anchor = 'const displayCollectionName = (value: string) => COLLECTION_LABELS[value] || value;\n'
helpers = '''const displayCollectionName = (value: string) => COLLECTION_LABELS[value] || value;
const displayProductName = (value: string) => String(value || "")
  .replace(/мокоши/gi, "Символы")
  .replace(/камея/gi, "Эхо")
  .replace(/жар[ -]?птица/gi, "Феникс")
  .replace(/дияф/gi, "Диаф");

// Merchandising matrix supplied for the four live Ready Solutions. These are
// SOURCE collection names, because CSV matching happens before the public alias.
const SOLUTION_BASE_COLLECTIONS: Record<string, string[]> = {
  "Красные линии": ["Мокоши", "Овация"],
};
const SOLUTION_EXTRA_COLLECTIONS: Record<string, string[]> = {
  "Зимняя сказка": ["Жар-птица", "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],
  "Красные линии": ["Камея", "Обереги", "Приданное", "Оренбургские узоры"],
  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России", "Жар-птица"],
  "Зеленый салон": ["Камея", "Фейерверк", "Обереги", "Дияф"],
};
const SOURCE_COLLECTION_HINTS = [
  "Мокоши", "Камея", "Жар-птица", "Овация", "Обереги", "Приданное",
  "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Купель",
  "Кружево", "Орнаменты России", "Фейерверк", "Дияф", "Ледяные узоры",
  "Лунная сказка", "Нити времени", "Юрма", "Текстура", "Дрёмица",
  "Петербург", "Многоцвет", "Весна",
] as const;
const sourceCollectionForRow = (row?: CatalogRow) => {
  const explicit = String(row?.collection || "").trim();
  if (explicit) return explicit;
  const name = norm(row?.product_name || "");
  if (name.includes("тайн") && name.includes("остров") && name.includes("буян")) return "Тайна острова Буяна";
  if (name.includes("оренбург") && name.includes("узор")) return "Оренбургские узоры";
  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";
};
'''
if "SOLUTION_EXTRA_COLLECTIONS" not in client:
    if anchor not in client:
        raise RuntimeError("V72 collection helper anchor not found")
    client = client.replace(anchor, helpers, 1)

# Cart and product cards use the new public names while retaining source rows.
client = client.replace(
    'return { id,name:row.product_name,note:[row.collection,row.material].filter(Boolean).join(" · "),price,',
    'return { id,name:displayProductName(row.product_name),note:[displayCollectionName(sourceCollectionForRow(row)),row.material].filter(Boolean).join(" · "),price,',
)
client = client.replace('alt={option.title}', 'alt={displayProductName(option.title)}')
client = client.replace('<h3>{option.title}</h3>', '<h3>{displayProductName(option.title)}</h3>')

old_base = '''  const baseRows=useMemo(()=>solution&&catalog?resolveTableSolutionCatalogRows(catalog.catalog,solution):[],[catalog,solution]);
  const baseCollections=useMemo(()=>solution?Array.from(new Set(solution.collections.filter(Boolean))):[],[solution]);'''
new_base = '''  const baseCollections=useMemo(()=>{if(!solution)return[]; const configured=SOLUTION_BASE_COLLECTIONS[solution.name]; return Array.from(new Set((configured||solution.collections).filter(Boolean)));},[solution]);
  const baseRows=useMemo(()=>{if(!solution||!catalog)return[]; const resolved=resolveTableSolutionCatalogRows(catalog.catalog,solution).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); if(solution.name!=="Красные линии")return resolved; const allowed=new Set(baseCollections.map(norm)); return resolved.filter((row)=>{const collection=sourceCollectionForRow(row); return !collection||allowed.has(norm(collection));});},[catalog,solution,baseCollections]);'''
if old_base in client:
    client = client.replace(old_base, new_base, 1)
elif "SOLUTION_BASE_COLLECTIONS[solution.name]" not in client:
    raise RuntimeError("V72 base collection block not found")

old_extra = '''  const extraChoices=useMemo(()=>{if(!catalog)return[]; const counts=new Map<string,number>(); catalog.catalog.forEach((row)=>{const c=row.collection?.trim(); if(!c||baseCollections.some((b)=>norm(b)===norm(c)))return; counts.set(c,(counts.get(c)||0)+1);}); return Array.from(counts.entries()).sort((a,b)=>b[1]-a[1]).map(([name])=>name).slice(0,6);},[catalog,baseCollections]);'''
new_extra = '''  const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; const available=new Set(catalog.catalog.map((row)=>sourceCollectionForRow(row)).filter(Boolean).map(norm)); return (SOLUTION_EXTRA_COLLECTIONS[solution.name]||[]).filter((name)=>available.has(norm(name))).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);'''
if old_extra in client:
    client = client.replace(old_extra, new_extra, 1)
elif "SOLUTION_EXTRA_COLLECTIONS[solution.name]" not in client:
    raise RuntimeError("V72 extra choices block not found")

old_extended = '''  const extendedRows=useMemo(()=>{if(!catalog)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(row.collection||""))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))); return [...baseRows,...extra];},[catalog,baseRows,activeCollections]);'''
new_extended = '''  const extendedRows=useMemo(()=>{if(!catalog)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...baseRows,...extra];},[catalog,baseRows,activeCollections]);'''
if old_extended in client:
    client = client.replace(old_extended, new_extended, 1)
elif "norm(sourceCollectionForRow(row))" not in client:
    raise RuntimeError("V72 extended rows block not found")

# Collection preview images must also work for rows whose source collection is
# inferred from the product name rather than populated in the CSV column.
client = client.replace(
    'catalog.catalog.find((r)=>norm(r.collection||"")===norm(name))',
    'catalog.catalog.find((r)=>norm(sourceCollectionForRow(r))===norm(name))',
)

# Use aliases in the result metadata as well.
client = client.replace(
    'displayCollectionName(row.collection||option.collection||"")',
    'displayCollectionName(sourceCollectionForRow(row)||option.collection||"")',
)

data_path.write_text(data, encoding="utf-8")
client_path.write_text(client, encoding="utf-8")
print("Ready Solutions V72 CSV collection merchandising applied")
