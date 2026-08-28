export type TableSolution = {
  id: string;
  sourceId: number;
  space: string;
  name: string;
  sourceName: string;
  previewFile: string;
  scrollFile: string;
  collections: string[];
  productNames: string[];
  defaultProductNames?: string[];
  defaultQuantities?: Record<string, number>;
  defaultColors?: Record<string, string>;
  defaultSizes?: Record<string, string>;
  productOrder?: string[];
  heroImage?: string;
  allowedProductTypes?: string[];
  includeCollectionProducts?: boolean;
  githubProductIds?: number[];
};

/**
 * Static routes for the five ready solutions defined by the XLSX source of truth.
 * Product composition itself is loaded from catalog_truth.json.gz.b64 at runtime,
 * so this file is intentionally routing/metadata only and does not duplicate
 * required/optional product relationships from the spreadsheet.
 */
export const TABLE_SOLUTIONS: readonly TableSolution[] = [
  {
    id: "green-salon",
    sourceId: 1,
    space: "Кухня и столовая",
    name: "Зеленый салон",
    sourceName: "Зеленый салон",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: [],
    includeCollectionProducts: false,
  },
  {
    id: "red-lines",
    sourceId: 2,
    space: "Кухня и столовая",
    name: "Красные линии",
    sourceName: "Красные линии",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: [],
    includeCollectionProducts: false,
  },
  {
    id: "winter-fairy-tale",
    sourceId: 3,
    space: "Спальня и гостиная",
    name: "Зимняя сказка",
    sourceName: "Зимняя сказка",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: [],
    includeCollectionProducts: false,
  },
  {
    id: "flame-of-sea-depths",
    sourceId: 4,
    space: "Интерьер",
    name: "Пламя морских глубин",
    sourceName: "Пламя морских глубин",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: [],
    includeCollectionProducts: false,
  },
  {
    id: "warm-brutalism",
    sourceId: 5,
    space: "Интерьер",
    name: "Теплый брутализм",
    sourceName: "Теплый брутализм",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: [],
    includeCollectionProducts: false,
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id);

const normalize = (value: string) =>
  String(value || "")
    .trim()
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/[«»"']/g, "")
    .replace(/[^a-zа-я0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");

export const findTableSolution = (id: string) =>
  TABLE_SOLUTIONS.find(
    (item) =>
      item.id === id ||
      normalize(item.name) === normalize(id) ||
      normalize(item.sourceName) === normalize(id),
  );
