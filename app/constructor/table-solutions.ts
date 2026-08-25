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
  /** Optional product names selected when the constructor first opens. */
  defaultProductNames?: string[];
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

    // Final curated assortment from the approved Green Salon screenshot.
    // The list is explicit so unrelated products from these collections do not
    // enter the ready solution automatically.
    productNames: [
      // Тарелки
      "Тарелка для яиц Пасхальная Весна",
      "Тарелка закусочная Весна",
      "Тарелка обеденная Весна",
      "Тарелка Петербург",
      "Тарелка десертная Овация",
      "Тарелка закусочная Овация",
      "Тарелка обеденная Овация",

      // Салатники и глубокие тарелки
      "Салатник Петербург",
      "Салатник порционный Овация",
      "Салатник Овация",
      "Тарелка глубокая Овация",

      // Кружки, чайные и кофейные пары
      "Кружка Весна",
      "Кофейная пара Овация",
      "Кружка Овация",
      "Чайная пара Овация",
      "Кружка Петербург",
      "Чайная пара Петербург",

      // Чайники, сахарницы и молочники
      "Сахарница Овация",
      "Сахарница Петербург",
      "Сливочник Петербург",
      "Чайник Овация",
      "Молочник Овация",
      "Чайник Петербург",

      // Блюда и подача
      "Блюдо овальное Овация",
      "Блюдо Петербург",
      "Подставка для яйца Овация",
      "Ваза для фруктов Весна",

      // Скатерти, плейсматы и тканевые салфетки
      "Плейсмат Весна",
      "Салфетка Весна",
      "Скатерть Весна",
      "Дорожка Петербург",
      "Салфетки Петербург",
      "Скатерть Петербург",
      "Дорожка Многоцвет",
      "Скатерть Многоцвет",

      // Свечи и диффузоры
      "Свеча Весна",
      "Свеча Многоцветы",
    ],
    includeCollectionProducts: false,
    defaultProductNames: [],
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

    // Final curated assortment from the approved Red Lines screenshot.
    productNames: [
      // Тарелки
      "Тарелка десертная Камея",
      "Тарелка для супа Камея",
      "Тарелка закусочная Камея",
      "Тарелка обеденная Камея",
      "Тарелка десертная Мокоши",

      // Блюда, салатники и подача
      "Салатник Камея",
      "Тарелка глубокая Камея",
      "Блюдо овальное Камея",
      "Супница Камея",

      // Кружки, чайные и кофейные пары
      "Кофейная пара Камея",
      "Кружка Камея",
      "Чайная пара Камея",
      "Кофейная пара Мокоши",
      "Чайная пара Мокоши",

      // Чайники, сахарницы и молочники
      "Сахарница Камея",
      "Молочник Камея",
      "Чайник заварочный Камея",

      // Скатерти, плейсматы и тканевые салфетки
      "Дорожка с кисточками Мокоши",
      "Плейсмат Мокоши",
      "Салфетка Мокоши",
      "Скатерть Мокоши",
    ],
    includeCollectionProducts: false,

    // Match the checked cards in the approved screenshot at 2 persons.
    defaultProductNames: [
      "Тарелка десертная Камея",
      "Тарелка десертная Мокоши",
      "Салатник Камея",
      "Чайная пара Камея",
      "Кофейная пара Мокоши",
      "Чайная пара Мокоши",
      "Сахарница Камея",
      "Молочник Камея",
      "Чайник заварочный Камея",
      "Дорожка с кисточками Мокоши",
      "Плейсмат Мокоши",
      "Скатерть Мокоши",
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
    githubProductIds: [4, 2003, 6, 7, 2000, 3],
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id) as TableSolution["id"][];

export const findTableSolution = (id: string) => TABLE_SOLUTIONS.find((item) => item.id === id);
