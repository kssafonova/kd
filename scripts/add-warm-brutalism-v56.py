from pathlib import Path

root = Path(__file__).resolve().parents[1]
table_path = root / "app" / "constructor" / "table-solutions.ts"
resolver_path = root / "app" / "constructor" / "table-solution-resolver.ts"
builder_path = root / "app" / "constructor" / "table-solution-builder.ts"

table = table_path.read_text(encoding="utf-8")
resolver = resolver_path.read_text(encoding="utf-8")
builder = builder_path.read_text(encoding="utf-8")

# Exact-offer ready solutions: keep the existing curated name-based scenarios,
# but allow new scenarios to be pinned to concrete catalog offer_ids.
table = table.replace(
    'id: "table-1" | "table-2" | "table-7";',
    'id: "table-1" | "table-2" | "table-7" | "table-8";',
)
if "offerIds?: string[];" not in table:
    table = table.replace(
        "  productNames: string[];\n",
        "  productNames: string[];\n  /** Exact catalog offer_ids used when a scenario must not pull similarly named products. */\n  offerIds?: string[];\n  /** Explicit guest choices for scenarios whose person logic is not covered by source scenario metadata. */\n  guestOptions?: number[];\n",
    )

if 'name: "Тёплый брутализм"' not in table:
    block = '''  {
    id: "table-8",
    sourceId: 8,
    space: "Кабинет",
    name: "Тёплый брутализм",
    sourceName: "Тёплый брутализм",
    previewFile: "",
    scrollFile: "",
    collections: ["Юрма", "Текстура", "Дрёмица"],
    productNames: [],
    // Exact SKU list supplied for the cabinet scenario. The resolver uses these
    // offer_ids directly, so no unrelated products from the same collections enter.
    offerIds: [
      "1348", "1396", "1397", "1401", "1403",
      "554", "555", "553", "277",
      "1233", "1236", "543", "542", "546", "545", "273", "272",
      "1242", "1243", "1235", "566",
      "286", "287", "370", "371", "885",
      "379", "378", "381", "380", "382", "383",
    ],
    includeCollectionProducts: false,
    guestOptions: [1, 2, 4],

    // Brown is the primary warm-brutalist palette. Beige is a softer alternative
    // and black is the contrast option; same products are merged into one card.
    defaultColors: {
      "Плейсмат Текстура": "коричневый",
      "Набор колец Текстура": "коричневый",
      "Конверт для приборов Текстура": "коричневый",
      "Салфетница Текстура": "коричневый",
      "Хлебница Текстура": "коричневый",
      "Корзина Текстура": "коричневый",
      "Игра крестики - нолики Текстура": "бежевый",
      "Игра шашки Текстура": "бежевый",
      "Игра домино Текстура": "бежевый",
    },

    // A compact curated starting composition; every supplied SKU remains available
    // as an option in the product step.
    defaultProductNames: [
      "Тарелка обеденная Юрма",
      "Тарелка глубокая Юрма",
      "Блюдо овальное Юрма",
      "Кружка Юрма",
      "Кофейная пара Юрма",
      "Плейсмат Текстура",
      "Подставка под бокал Текстура",
      "Кольцо Дрёмица",
      "Конверт для приборов Текстура",
      "Менажница Дрёмица",
      "Корзина Текстура",
      "Обложка для ежедневника Текстура",
      "Игра крестики - нолики Текстура",
    ],
  },
'''
    table = table.replace("] as const;", block + "] as const;")

# Resolve exact offers before broad name/collection matching.
if "const offerTargets" not in resolver:
    resolver = resolver.replace(
        "  const productTargets = solution.productNames.map(normalizeSolutionValue).filter(Boolean);\n",
        "  const productTargets = solution.productNames.map(normalizeSolutionValue).filter(Boolean);\n  const offerTargets = new Set((solution.offerIds || []).map((value) => String(value).trim()).filter(Boolean));\n",
    )
    resolver = resolver.replace(
        "  const productType = normalizeSolutionValue(row.product_type || \"\");\n",
        "  const productType = normalizeSolutionValue(row.product_type || \"\");\n  const offerId = String(row.offer_id || \"\").trim();\n",
    )
    resolver = resolver.replace(
        "  const explicitProductMatch = productTargets.some((target) => matchesLoose(productName, target));\n\n  return collectionMatch || explicitProductMatch;",
        "  const explicitProductMatch = productTargets.some((target) => matchesLoose(productName, target));\n  const explicitOfferMatch = offerTargets.has(offerId);\n\n  return collectionMatch || explicitProductMatch || explicitOfferMatch;",
    )

# Some rows in the constructor feed have no collection value although the source
# product name contains the collection. Infer it only for this exact cabinet solution,
# so UI labels and product-variant grouping remain faithful to the supplied mapping.
if "WARM_BRUTALISM_COLLECTION_INFERENCE_V56" not in resolver:
    resolver = resolver.replace(
        "  return sourceRows.sort((a, b) => {",
        '''  // WARM_BRUTALISM_COLLECTION_INFERENCE_V56
  const normalizedRows = solution.id === "table-8" ? sourceRows.map((row) => {
    if (row.collection) return row;
    const name = normalizeSolutionValue(row.product_name || "");
    const collection = name.includes("юрма") ? "Юрма"
      : name.includes("текстура") ? "Текстура"
      : name.includes("дремица") ? "Дрёмица"
      : "";
    return collection ? { ...row, collection } : row;
  }) : sourceRows;

  return normalizedRows.sort((a, b) => {''',
    )

# The cabinet scenario uses some leather desk/table accessories whose source
# product types are too generic. Classify them by user-facing merchandising role.
marker = '  if (hasAny(name, ["скатерт", "плейсмат", "салфет", "дорожк", "раннер"]) || hasAny(type, ["tablecloth", "placemat", "napkin", "table_runner"])) {'
if "WARM_BRUTALISM_ACCESSORY_MAPPING_V56" not in builder:
    special = '''  // WARM_BRUTALISM_ACCESSORY_MAPPING_V56
  // Leather desk/table accessories belong to table textile in the form even when
  // the source feed calls them wine glass/other. Shared holders/sets stay quantity 1.
  if (name.includes("подставка под бокал")) return { id: "tableTextile", perPerson: true };
  if (hasAny(name, ["подставка для салфеток", "салфетница"])) return { id: "tableTextile", perPerson: false };
  if (name.includes("набор колец")) return { id: "tableTextile", perPerson: false };
  if (name.includes("кольцо")) return { id: "tableTextile", perPerson: true };
  if (name.includes("конверт для приборов")) return { id: "tableTextile", perPerson: true };

'''
    builder = builder.replace(marker, special + marker)
    builder = builder.replace(
        '  if (name.includes("корзин")) return { id: "baskets", perPerson: false };',
        '  if (name.includes("корзин")) return { id: "baskets", perPerson: false };\n  if (hasAny(name, ["хлебниц", "ежедневник"])) return { id: "storage", perPerson: false };',
    )
    builder = builder.replace(
        '  if (hasAny(name, ["игра", "шахмат", "нарды", "домино", "лото"]) || hasAny(type, ["game", "board_game"])) {',
        '  if (hasAny(name, ["игра", "шахмат", "нарды", "домино", "лото", "крестики-нолики", "шашки"]) || hasAny(type, ["game", "board_game"])) {',
    )

# Cabinet has an explicit 1/2/4-person choice; do not let unrelated historical
# scenario metadata override it.
if "solution.guestOptions?.length" not in builder:
    builder = builder.replace(
        "export const deriveGuestOptions = (solution: TableSolution, data: ConstructorData | null) => {\n",
        "export const deriveGuestOptions = (solution: TableSolution, data: ConstructorData | null) => {\n  if (solution.guestOptions?.length) return Array.from(new Set(solution.guestOptions.filter((value) => Number.isFinite(value) && value > 0))).sort((a, b) => a - b);\n",
    )

table_path.write_text(table, encoding="utf-8")
resolver_path.write_text(resolver, encoding="utf-8")
builder_path.write_text(builder, encoding="utf-8")

print("Warm Brutalism V56 ready solution applied")
