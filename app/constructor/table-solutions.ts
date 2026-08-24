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
  /**
   * Optional storefront catalog product types allowed for collection-based
   * matching. Explicit productNames are still matched independently so a
   * solution can add real catalog accessories that do not belong to a named
   * collection.
   */
  allowedProductTypes?: string[];
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
    // Every selector below resolves an existing storefront catalog product.
    // Prices, photos, colors, sizes and URLs are never hardcoded here.
    productNames: [
      "Комплект постельного белья Ледяной узор",
      "Комплект постельного белья Нити времени",
      "Плед Ажур",
      "Плед Соты",
      "Подушка декоративная Пушица",
      "Ваза Айсберг",
      "Ваза Паскаль",
      "Свеча Корона",
      "Диффузор",
    ],
    // Collection matching remains available for real catalog items tagged with
    // the source collections, but it cannot pull unrelated tableware/decor.
    allowedProductTypes: [
      "bedding_set",
      "duvet",
      "sheet",
      "pillowcase",
      "pillowcase_set",
      "throw",
      "coverlet",
      "decorative_pillow",
    ],
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id) as TableSolution["id"][];

export const findTableSolution = (id: string) => TABLE_SOLUTIONS.find((item) => item.id === id);
