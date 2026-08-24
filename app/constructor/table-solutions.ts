export type TableSolution = {
  id: "table-1" | "table-2" | "table-3" | "table-4" | "table-5" | "table-6" | "table-7";
  sourceId: number;
  space: string;
  name: string;
  sourceName: string;
  previewFile: string;
  scrollFile: string;
  collections: string[];
  productNames: string[];
  /** Optional CSV product types allowed for collection-based matching. */
  allowedProductTypes?: string[];
  /** Disable broad collection pulls and use only explicit CSV products. */
  includeCollectionProducts?: boolean;
  /**
   * Product ids from app/catalog-data.ts. These exact products already exist
   * in the GitHub storefront catalog and can be mixed with explicit CSV items.
   */
  githubProductIds?: number[];
};

export const TABLE_SOLUTIONS: readonly TableSolution[] = [
  {
    id: "table-1",
    sourceId: 1,
    space: "Кухня и столовая",
    name: "Зеленый салон",
    sourceName: "Зеленый салон",
    previewFile: "green.jpeg",
    scrollFile: "green2.jpeg",
    collections: ["Петербург", "Многоцвет", "Овация", "Весна"],
    productNames: [],
  },
  {
    id: "table-2",
    sourceId: 2,
    space: "Кухня и столовая",
    name: "Красные линии",
    sourceName: "Красные линии",
    previewFile: "redline1.jpeg",
    scrollFile: "redline2.jpeg",
    collections: ["Мокоши", "Камея"],
    productNames: [
      "Кофейная пара Мокоши",
      "Чайная пара Мокоши",
      "Тарелка десертная Мокоши",
      "Чайная пара Камея",
      "Тарелка десертная Камея",
      "Чайник заварочный Камея",
      "Салатник Камея",
      "Скатерть Мокоши",
      "Плейсмат Мокоши",
      "Дорожка с кисточками Мокоши",
    ],
  },
  {
    id: "table-3",
    sourceId: 3,
    space: "Кухня и столовая",
    name: "Доброе утро",
    sourceName: "Доброе утро",
    previewFile: "bluegold.jpeg",
    scrollFile: "bluegold2.jpeg",
    collections: ["Дияф", "Фейерверк", "Овация", "Александр"],
    productNames: [],
  },
  {
    id: "table-4",
    sourceId: 4,
    space: "Спальня",
    name: "Тихий сон",
    sourceName: "Тихий сон",
    previewFile: "",
    scrollFile: "",
    collections: [],
    productNames: ["Тихий сон"],
  },
  {
    id: "table-5",
    sourceId: 5,
    space: "Кабинет",
    name: "Ретро",
    sourceName: "Ретро",
    previewFile: "",
    scrollFile: "",
    collections: ["Текстура", "Юрма"],
    productNames: ["Игры", "Тарелка Юрма", "Корзина", "Плейсмат"],
  },
  {
    id: "table-6",
    sourceId: 6,
    space: "Ванная",
    name: "Уют",
    sourceName: "Уют",
    previewFile: "",
    scrollFile: "",
    collections: ["Текстура", "Уют"],
    productNames: ["Набор для ванной", "Халат", "Корзина"],
  },
  {
    id: "table-7",
    sourceId: 7,
    space: "Спальня и гостиная",
    name: "Зимняя сказка",
    sourceName: "Зимняя сказка",
    previewFile: "",
    scrollFile: "",
    collections: ["Ледяные узоры", "Лунная сказка", "Нити Времени"],

    // Exact real products from the constructor CSV that are mixed with the
    // custom GitHub storefront assortment below. Broad collection matching is
    // intentionally disabled so unrelated tableware does not enter the scene.
    productNames: [
      "Комплект постельного белья Нити времени",
      "Подушка декоративная Бархат",
      "Подушка декоративная Узоры",
      "Подушка декоративная Нити времени",
      "Ваза Айсберг",
      "Ваза Паскаль",
      "Диффузор Зимняя сказка",
      "Диффузор Сласти",
      "Диффузор Уютный вечер",
      "Свеча Корона высокая, аромат Базилика и Мяты",
      "Свеча Корона высокая, аромат Нежность",
      "Свеча Корона высокая, без аромата",
      "Свеча Корона малая, аромат Серебряный мускус",
      "Свеча Корона малая, аромат Золотой цветок",
      "Свеча Корона малая, без аромата",
    ],
    includeCollectionProducts: false,

    // Exact products previously added to app/catalog-data.ts and GitHub media.
    // Their local photos, sizes and colour variants remain authoritative.
    githubProductIds: [4, 2003, 6, 7, 2000, 3],
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id) as TableSolution["id"][];

export const findTableSolution = (id: string) => TABLE_SOLUTIONS.find((item) => item.id === id);
