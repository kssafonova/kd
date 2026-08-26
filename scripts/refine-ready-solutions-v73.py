from pathlib import Path

root = Path(__file__).resolve().parents[1]
client_path = root / "app" / "ready-solutions" / "ready-solutions-v71-client.tsx"
client = client_path.read_text(encoding="utf-8")

# Latest merchandising rules supplied for Ready Solutions.
client = client.replace(
    'const COLLECTION_LABELS: Record<string, string> = { "Мокоши": "Символы", "Камея": "Эхо", "Жар-птица": "Феникс", "Дияф": "Диаф" };',
    'const COLLECTION_LABELS: Record<string, string> = { "Камея": "Эхо", "Жар-птица": "Феникс", "Дияф": "Диаф", "Приданное": "Приданое" };',
)

old_base = '''const SOLUTION_BASE_COLLECTIONS: Record<string, string[]> = {
  "Красные линии": ["Мокоши", "Овация"],
};'''
new_base = '''const SOLUTION_BASE_COLLECTIONS: Record<string, string[]> = {
  "Красные линии": ["Мокоши", "Камея", "Оренбургские узоры"],
  "Зеленый салон": ["Петербург", "Многоцвет", "Овация", "Весна"],
};'''
client = client.replace(old_base, new_base)

old_extra = '''const SOLUTION_EXTRA_COLLECTIONS: Record<string, string[]> = {
  "Зимняя сказка": ["Жар-птица", "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],
  "Красные линии": ["Камея", "Обереги", "Приданное", "Оренбургские узоры"],
  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России", "Жар-птица"],
  "Зеленый салон": ["Камея", "Фейерверк", "Обереги", "Дияф"],
};'''
new_extra = '''const SOLUTION_EXTRA_COLLECTIONS: Record<string, string[]> = {
  "Зимняя сказка": ["Жар-птица", "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Овация"],
  "Красные линии": ["Овация", "Обереги", "Приданое", "Александр"],
  "Тёплый брутализм": ["Купель", "Кружево", "Тайна острова Буяна", "Орнаменты России", "Жар-птица"],
  "Зеленый салон": ["Камея", "Обереги", "Александр"],
};'''
client = client.replace(old_extra, new_extra)

old_hints = '''const SOURCE_COLLECTION_HINTS = [
  "Мокоши", "Камея", "Жар-птица", "Овация", "Обереги", "Приданное",
  "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Купель",
  "Кружево", "Орнаменты России", "Фейерверк", "Дияф", "Ледяные узоры",
  "Лунная сказка", "Нити времени", "Юрма", "Текстура", "Дрёмица",
  "Петербург", "Многоцвет", "Весна",
] as const;'''
new_hints = '''const SOURCE_COLLECTION_HINTS = [
  "Мокоши", "Камея", "Жар-птица", "Овация", "Обереги", "Приданное", "Приданое", "Александр",
  "Оренбургские узоры", "Голубые цветы", "Тайна острова Буяна", "Купель",
  "Кружево", "Орнаменты России", "Фейерверк", "Дияф", "Ледяные узоры",
  "Лунная сказка", "Нити времени", "Юрма", "Текстура", "Дрёмица",
  "Петербург", "Многоцвет", "Весна",
] as const;'''
client = client.replace(old_hints, new_hints)

old_source_tail = '''  if (name.includes("тайн") && name.includes("остров") && name.includes("буян")) return "Тайна острова Буяна";
  if (name.includes("оренбург") && name.includes("узор")) return "Оренбургские узоры";
  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";
};
const COLOR_HEX'''
new_source_tail = '''  if (name.includes("тайн") && name.includes("остров") && name.includes("буян")) return "Тайна острова Буяна";
  if (name.includes("оренбург") && name.includes("узор")) return "Оренбургские узоры";
  if (name.includes("александр")) return "Александр";
  if (name.includes("придан")) return "Приданое";
  return SOURCE_COLLECTION_HINTS.find((value) => name.includes(norm(value))) || "";
};
const solutionConfig = (matrix: Record<string, string[]>, name: string) =>
  Object.entries(matrix).find(([key]) => norm(key) === norm(name))?.[1] || [];

const SOLUTION_REMOVED_PRODUCTS: Record<string, string[]> = {
  "Зимняя сказка": [
    "Тарелка десертная Нити времени",
    "Кружка Нити времени",
    "Чайная пара Нити времени",
    "Салфетка Нити времени",
    "Плейсмат Нити времени",
    "Дорожка Нити времени",
    "Свеча с ароматом Сладкий табак Нити Времени",
    "Свеча с ароматом Копченая клюква Нити Времени",
  ],
  "Красные линии": [
    "Комплект постельного белья с вышивкой Символы",
    "Гетры Оренбургский узор",
    "Носки Оренбургский узор",
  ],
  "Тёплый брутализм": [
    "Тарелка глубокая Юрма",
    "Кружка Юрма",
    "Кофейная пара Юрма",
    "Тарелка обеденная Юрма",
    "Тарелка ассиметричная Юрма",
    "Тарелка асимметричная Юрма",
    "Блюдо овальное Юрма",
    "Стакан Юрма",
    "Кольцо Дрёмица",
    "Набор колец текстура",
    "Хлебница Текстура",
    "Набор для ванной Текстура",
  ],
  "Зеленый салон": [
    "Чайная пара Многоцвет",
    "Молочник Многоцвет",
    "Сахарница Многоцвет",
    "Скатерть Петербург",
    "Бульонная пара Овация",
  ],
};
const productBaseName = (row: CatalogRow) => norm(displayProductName(row.product_name).split(":")[0]);
const isRemovedSolutionProduct = (solutionName: string, row: CatalogRow) => {
  const removed = new Set(solutionConfig(SOLUTION_REMOVED_PRODUCTS, solutionName).map(norm));
  return removed.has(productBaseName(row));
};
const applySolutionCategoryOverrides = (solutionName: string, row: CatalogRow): CatalogRow => {
  if (norm(solutionName) !== norm("Зимняя сказка")) return row;
  const name = productBaseName(row);
  if (name === norm("Плед из кружева")) return { ...row, product_type: "throw" };
  if (name === norm("Подушка с кружевом")) return { ...row, product_type: "decorative_pillow" };
  return row;
};

const COLOR_HEX'''
if old_source_tail not in client and "SOLUTION_REMOVED_PRODUCTS" not in client:
    raise RuntimeError("V73 source helper anchor not found")
client = client.replace(old_source_tail, new_source_tail, 1)

old_base_rows = '''  const baseCollections=useMemo(()=>{if(!solution)return[]; const configured=SOLUTION_BASE_COLLECTIONS[solution.name]; return Array.from(new Set((configured||solution.collections).filter(Boolean)));},[solution]);
  const baseRows=useMemo(()=>{if(!solution||!catalog)return[]; const resolved=resolveTableSolutionCatalogRows(catalog.catalog,solution).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); if(solution.name!=="Красные линии")return resolved; const allowed=new Set(baseCollections.map(norm)); return resolved.filter((row)=>{const collection=sourceCollectionForRow(row); return !collection||allowed.has(norm(collection));});},[catalog,solution,baseCollections]);'''
new_base_rows = '''  const baseCollections=useMemo(()=>{if(!solution)return[]; const configured=solutionConfig(SOLUTION_BASE_COLLECTIONS,solution.name); return Array.from(new Set((configured.length?configured:solution.collections).filter(Boolean)));},[solution]);
  const baseRows=useMemo(()=>{if(!solution||!catalog)return[]; const resolved=resolveTableSolutionCatalogRows(catalog.catalog,solution).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); const configured=solutionConfig(SOLUTION_BASE_COLLECTIONS,solution.name); if(!configured.length)return resolved; const allowed=new Set(configured.map(norm)); return resolved.filter((row)=>allowed.has(norm(sourceCollectionForRow(row))));},[catalog,solution]);'''
if old_base_rows not in client and "const configured=solutionConfig(SOLUTION_BASE_COLLECTIONS" not in client:
    raise RuntimeError("V73 base rows anchor not found")
client = client.replace(old_base_rows, new_base_rows, 1)

old_extra_choices = '''  const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; const available=new Set(catalog.catalog.map((row)=>sourceCollectionForRow(row)).filter(Boolean).map(norm)); return (SOLUTION_EXTRA_COLLECTIONS[solution.name]||[]).filter((name)=>available.has(norm(name))).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);'''
new_extra_choices = '''  const extraChoices=useMemo(()=>{if(!catalog||!solution)return[]; return solutionConfig(SOLUTION_EXTRA_COLLECTIONS,solution.name).filter((name)=>!baseCollections.some((base)=>norm(base)===norm(name))).slice(0,6);},[catalog,solution,baseCollections]);'''
if old_extra_choices not in client and "solutionConfig(SOLUTION_EXTRA_COLLECTIONS" not in client:
    raise RuntimeError("V73 extra choices anchor not found")
client = client.replace(old_extra_choices, new_extra_choices, 1)

old_extended = '''  const extendedRows=useMemo(()=>{if(!catalog)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...baseRows,...extra];},[catalog,baseRows,activeCollections]);'''
new_extended = '''  const extendedRows=useMemo(()=>{if(!catalog||!solution)return baseRows; const keys=new Set(baseRows.map((row)=>String(row.offer_id||row.vendor_code||row.product_name))); const extra=catalog.catalog.filter((row)=>activeCollections.some((c)=>norm(c)===norm(sourceCollectionForRow(row)))&&!keys.has(String(row.offer_id||row.vendor_code||row.product_name))).map((row)=>row.collection?row:{...row,collection:sourceCollectionForRow(row)}); return [...baseRows,...extra].filter((row)=>!isRemovedSolutionProduct(solution.name,row)).map((row)=>applySolutionCategoryOverrides(solution.name,row));},[catalog,solution,baseRows,activeCollections]);'''
if old_extended not in client and "isRemovedSolutionProduct(solution.name,row)" not in client:
    raise RuntimeError("V73 extended rows anchor not found")
client = client.replace(old_extended, new_extended, 1)

client_path.write_text(client, encoding="utf-8")
print("Ready Solutions V73 merchandising rules applied")
