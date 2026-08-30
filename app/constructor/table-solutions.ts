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
 * Ready solutions from the canonical project table.
 * Product composition is resolved at runtime from catalog_truth.json.gz.b64
 * using required:/optional: relation tags, so the metadata here only defines
 * public routes and presentation.
 */
export const TABLE_SOLUTIONS: readonly TableSolution[] = [
  {
    id: "green-salon",
    sourceId: 1,
    space: "Кухня и столовая",
    name: "Зеленый салон",
    sourceName: "Зеленый салон",
    previewFile: "green.jpeg",
    scrollFile: "green2.jpeg",
    heroImage: "/assets/images/green.jpeg",
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
    previewFile: "redline1.jpeg",
    scrollFile: "redline2.jpeg",
    heroImage: "/assets/images/redline1.jpeg",
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
    id: "warm-brutalism",
    sourceId: 4,
    space: "Интерьер",
    name: "Теплый брутализм",
    sourceName: "Теплый брутализм",
    previewFile: "bluegold.jpeg",
    scrollFile: "bluegold2.jpeg",
    heroImage: "/assets/images/bluegold.jpeg",
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
