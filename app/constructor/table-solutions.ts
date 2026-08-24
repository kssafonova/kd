export type TableSolution = {
  id: "table-1" | "table-2" | "table-7";
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
    id: "table-7",
    sourceId: 7,
    space: "Спальня и гостиная",
    name: "Зимняя сказка",
    sourceName: "Зимняя сказка",
    previewFile: "",
    scrollFile: "",
    collections: ["Ледяные узоры", "Лунная сказка", "Нити Времени"],

    // Final approved CSV additions for the Winter Fairy Tale scenario.
    // Broad collection matching remains disabled so only these exact catalog
    // items are mixed with the GitHub storefront products below.
    productNames: [
      "Комплект постельного белья Нити времени",
      "Подушка декоративная Бархат",
      "Подушка декоративная Узоры",
      "Ваза Айсберг",
      "Ваза Паскаль",
      "Диффузор Зимняя сказка",
      "Диффузор Сласти",
      "Диффузор Уютный вечер",
      "Свеча Корона высокая, аромат Базилика и Мяты",
      "Свеча Корона высокая, аромат Нежность",
      "Свеча Корона высокая, без аромата",
      "Свеча Корона малая, аромат Серебряный мускус",
      "Свеча Корона малая, без аромата",
    ],
    includeCollectionProducts: false,

    // Exact products previously added to app/catalog-data.ts and GitHub media:
    // Лунная сказка, Ледяные узоры, кружево and Бархатный ритм.
    githubProductIds: [4, 2003, 6, 7, 2000, 3],
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id) as TableSolution["id"][];

export const findTableSolution = (id: string) => TABLE_SOLUTIONS.find((item) => item.id === id);
