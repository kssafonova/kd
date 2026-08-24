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
    productNames: [
      "Плед ледяные узоры",
      "Подушка ледяные узоры",
      "Плед из кружева",
      "Подушка с кружевом",
      "Подушка декоративная нити времени",
      "Подушка декоративная узоры голубой",
      "Подушка декоративная бархат голубой",
      "Стёганое покрывало «Бархатный ритм»",
      "Комплект постельного белья Голубая светлица",
      "Комплект постельного белья Лунная сказка",
      "Ваза Айсберг белый",
      "Ваза Паскаль синий",
      "Свеча Корона малая",
      "Свеча Корона высокая",
      "Диффузор",
    ],
  },
] as const;

export const TABLE_SOLUTION_IDS = TABLE_SOLUTIONS.map((item) => item.id) as TableSolution["id"][];

export const findTableSolution = (id: string) => TABLE_SOLUTIONS.find((item) => item.id === id);
