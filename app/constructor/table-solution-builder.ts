import type { CatalogRow, ConstructorData } from "./types";
import type { TableSolution } from "./table-solutions";
import { logicalProductKey } from "./table-solution-resolver";

export type SolutionProductOption = {
  id: string;
  title: string;
  collection: string;
  perPerson: boolean;
  variants: CatalogRow[];
};

/**
 * Kept as a compatibility layer for the landing page. Every broad shopping
 * category contains one slot and that slot supports MULTIPLE product options
 * in the detail constructor.
 */
export type SolutionSlot = {
  id: string;
  title: string;
  description: string;
  perPerson: boolean;
  options: SolutionProductOption[];
};

export type SolutionCategory = {
  id: string;
  title: string;
  description: string;
  slots: SolutionSlot[];
};

const normalize = (value: string) => String(value || "")
  .trim()
  .toLocaleLowerCase("ru-RU")
  .replace(/ё/g, "е")
  .replace(/[«»"']/g, "")
  .replace(/\s+/g, " ");

const hasAny = (value: string, tokens: string[]) => tokens.some((token) => value.includes(token));
const baseName = (row: CatalogRow) => String(row.product_name || "Товар").split(":")[0].trim();

const categoryMeta: Record<string, { title: string; description: string }> = {
  plates: {
    title: "Тарелки",
    description: "Все обычные, десертные и закусочные тарелки из коллекций решения — можно выбрать несколько одновременно.",
  },
  bowls: {
    title: "Салатники и глубокие тарелки",
    description: "Все салатники и глубокие тарелки собраны в одном блоке для сравнения и множественного выбора.",
  },
  cupsPairs: {
    title: "Кружки, чайные и кофейные пары",
    description: "Кружки, чайные и кофейные пары из разных коллекций показаны вместе. Можно выбрать несколько вариантов.",
  },
  greenSalonTeaService: {
    title: "Чайники, сахарницы и молочники",
    description: "Чайники, сахарницы, молочники и сливочники собраны в одном блоке, как в сценарии «Зеленый салон».",
  },
  sugarBowls: {
    title: "Сахарницы",
    description: "Все сахарницы из предложенных коллекций — выберите одну, несколько или не добавляйте ни одной.",
  },
  milkJugs: {
    title: "Молочники и сливочники",
    description: "Все молочники и сливочники собраны вместе независимо от коллекции.",
  },
  teapots: {
    title: "Чайники",
    description: "Все заварочные и сервировочные чайники из сценария в одном блоке.",
  },
  serving: {
    title: "Блюда и подача",
    description: "Блюда, подносы, супницы, менажницы и другие общие предметы для подачи.",
  },
  drinkware: {
    title: "Бокалы, стаканы и графины",
    description: "Стекло и предметы для напитков из разных коллекций — можно комбинировать несколько позиций.",
  },
  cutlery: {
    title: "Столовые приборы",
    description: "Вилки, ложки, ножи и другие столовые приборы, найденные в коллекциях решения.",
  },
  tableTextile: {
    title: "Скатерти, плейсматы и тканевые салфетки",
    description: "Скатерти, дорожки, плейсматы и тканевые салфетки собраны вместе — выбирайте нужные элементы сервировки.",
  },
  baskets: {
    title: "Корзины",
    description: "Все корзины показаны рядом, чтобы удобно сравнить форму, материал, размер и коллекцию.",
  },
  games: {
    title: "Игры",
    description: "Все настольные игры, шахматы, нарды и игровые аксессуары, найденные в сценарии.",
  },
  storage: {
    title: "Хранение и организация",
    description: "Органайзеры и другие функциональные предметы для хранения.",
  },
  bedding: {
    title: "Постельное бельё",
    description: "Комплекты, пододеяльники, простыни и наволочки из каталога сайта. Цвета и размеры объединены внутри одной карточки товара.",
  },
  throwsCoverlets: {
    title: "Пледы и покрывала",
    description: "Пледы и покрывала из каталога сайта, подходящие к выбранным коллекциям решения.",
  },
  decorativePillows: {
    title: "Декоративные подушки",
    description: "Декоративные подушки из каталога сайта. Цветовые варианты одного товара объединены в одной карточке.",
  },
  bath: {
    title: "Для ванной",
    description: "Халаты, полотенца, коврики и наборы для ванной из предложенного решения.",
  },
  vases: {
    title: "Вазы и предметы интерьера",
    description: "Вазы и интерьерные акценты из каталога сайта — можно выбрать одну или несколько позиций.",
  },
  atmosphere: {
    title: "Свечи и диффузоры",
    description: "Свечи, подсвечники и ароматы для дома из каталога сайта собраны в одном атмосферном блоке.",
  },
  other: {
    title: "Дополнения",
    description: "Остальные найденные предметы, которые можно добавить к решению по желанию.",
  },
};

const isGreenSalonRows = (rows: CatalogRow[]) => {
  const names = rows.map((row) => normalize(row.product_name));
  return names.some((name) => name.includes("пасхальная весна")) &&
    names.some((name) => name.includes("петербург")) &&
    names.some((name) => name.includes("овация"));
};

const categoryForRow = (row: CatalogRow, space: string, greenSalon = false) => {
  const name = normalize(row.product_name);
  const type = normalize(row.product_type);
  const normalizedSpace = normalize(space);

  // Green Salon follows the approved merchandising screenshot: tea pots,
  // sugar bowls and milk/cream jugs are one comparison group.
  if (greenSalon && (
    name.includes("сахарниц") || type.includes("sugar_bowl") ||
    hasAny(name, ["молочник", "сливочник"]) || type.includes("milk_jug") ||
    name.includes("чайник") || type.includes("teapot")
  )) return { id: "greenSalonTeaService", perPerson: false };

  // Egg stands are a serving accessory in the approved Green Salon layout.
  if (greenSalon && hasAny(name, ["подставка для яйца", "подставка для яиц"])) {
    return { id: "serving", perPerson: false };
  }

  // The order is intentional: deep plates belong with bowls, not with plates.
  if (hasAny(name, ["тарелка глубок", "салатник"]) || hasAny(type, ["deep_plate", "salad_bowl"])) {
    return { id: "bowls", perPerson: name.includes("тарелка глубок") || type.includes("deep_plate") };
  }

  if (hasAny(name, ["тарелка", "блюдце"]) || hasAny(type, ["dinner_plate", "dessert_plate", "snack_plate", "plate"])) {
    return { id: "plates", perPerson: true };
  }

  if (hasAny(name, ["круж", "чашк", "чайная пара", "кофейная пара"]) || hasAny(type, ["mug", "tea_pair", "coffee_pair"])) {
    return { id: "cupsPairs", perPerson: true };
  }

  if (name.includes("сахарниц") || type.includes("sugar_bowl")) return { id: "sugarBowls", perPerson: false };
  if (hasAny(name, ["молочник", "сливочник"]) || type.includes("milk_jug")) return { id: "milkJugs", perPerson: false };
  if (name.includes("чайник") || type.includes("teapot")) return { id: "teapots", perPerson: false };

  if (hasAny(name, ["скатерт", "плейсмат", "салфет", "дорожк", "раннер"]) || hasAny(type, ["tablecloth", "placemat", "napkin", "table_runner"])) {
    return { id: "tableTextile", perPerson: hasAny(name, ["плейсмат", "салфет"]) || hasAny(type, ["placemat", "napkin"]) };
  }

  if (name.includes("корзин")) return { id: "baskets", perPerson: false };

  if (hasAny(name, ["игра", "шахмат", "нарды", "домино", "лото"]) || hasAny(type, ["game", "board_game"])) {
    return { id: "games", perPerson: false };
  }

  if (hasAny(name, ["свеч", "диффузор", "аромат для дома", "аромадиффузор", "подсвечник"]) || hasAny(type, ["candle", "candle_holder", "diffuser"])) {
    return { id: "atmosphere", perPerson: false };
  }

  if (name.includes("ваза") || type.includes("vase")) return { id: "vases", perPerson: false };

  if (hasAny(name, ["вилка", "ложка", "нож", "прибор"]) || hasAny(type, ["cutlery", "fork", "spoon", "knife"])) {
    return { id: "cutlery", perPerson: true };
  }

  if (hasAny(name, ["бокал", "стакан", "рюм", "графин", "декантер"]) || hasAny(type, ["wine_glass", "glassware", "decanter"])) {
    const shared = hasAny(name, ["графин", "декантер"]) || type.includes("decanter");
    return { id: "drinkware", perPerson: !shared };
  }

  if (hasAny(name, ["блюдо", "поднос", "супниц", "менажниц", "икорниц", "масленк"]) || hasAny(type, ["serving_dish", "tray", "tureen"])) {
    return { id: "serving", perPerson: false };
  }

  if (hasAny(name, ["комплект постель", "постельное белье", "пододеяльник", "простын", "наволоч"]) || hasAny(type, ["bedding_set", "duvet", "sheet", "pillowcase"])) {
    return { id: "bedding", perPerson: false };
  }

  if (name.includes("подушка") || type.includes("decorative_pillow")) {
    return { id: "decorativePillows", perPerson: false };
  }

  if (hasAny(name, ["плед", "покрывал"]) || hasAny(type, ["throw", "coverlet"])) {
    return { id: "throwsCoverlets", perPerson: false };
  }

  if (hasAny(name, ["халат", "полотен", "коврик для ванн", "набор для ванн"]) || normalizedSpace.includes("ванн")) {
    return { id: "bath", perPerson: hasAny(name, ["халат", "полотен"]) };
  }

  if (hasAny(name, ["органайзер", "хранени"])) return { id: "storage", perPerson: false };

  return { id: "other", perPerson: false };
};

const categoryOrder = [
  "plates",
  "bowls",
  "cupsPairs",
  "greenSalonTeaService",
  "sugarBowls",
  "milkJugs",
  "teapots",
  "serving",
  "drinkware",
  "cutlery",
  "tableTextile",
  "baskets",
  "games",
  "storage",
  "bedding",
  "throwsCoverlets",
  "decorativePillows",
  "bath",
  "vases",
  "atmosphere",
  "other",
];

export const buildSolutionCategories = (rows: CatalogRow[], space: string): SolutionCategory[] => {
  const categoryMap = new Map<string, Map<string, { perPerson: boolean; variants: CatalogRow[] }>>();
  const greenSalon = isGreenSalonRows(rows);

  rows.forEach((row) => {
    const category = categoryForRow(row, space, greenSalon);
    const optionId = logicalProductKey(row);
    if (!categoryMap.has(category.id)) categoryMap.set(category.id, new Map());
    const optionMap = categoryMap.get(category.id)!;
    const current = optionMap.get(optionId) || { perPerson: category.perPerson, variants: [] };
    current.perPerson = current.perPerson || category.perPerson;
    current.variants.push(row);
    optionMap.set(optionId, current);
  });

  return categoryOrder
    .filter((categoryId) => categoryMap.has(categoryId))
    .map((categoryId) => {
      const optionMap = categoryMap.get(categoryId)!;
      const options: SolutionProductOption[] = Array.from(optionMap.entries())
        .map(([optionId, value]) => {
          const variants = Array.from(new Map(value.variants.map((row) => [row.offer_id, row])).values());
          const representative = variants.find((row) => row.primary_image_url && row.price) || variants.find((row) => row.primary_image_url) || variants[0];
          return {
            id: optionId,
            title: baseName(representative),
            collection: representative?.collection || "Культура Дома",
            perPerson: value.perPerson,
            variants,
          };
        })
        .sort((a, b) => a.collection.localeCompare(b.collection, "ru") || a.title.localeCompare(b.title, "ru"));

      const meta = categoryMeta[categoryId];
      const slot: SolutionSlot = {
        id: categoryId,
        title: meta.title,
        description: "Выберите один или несколько товаров из предложенных вариантов.",
        perPerson: options[0]?.perPerson || false,
        options,
      };
      return { id: categoryId, ...meta, slots: [slot] };
    });
};

export const recommendedOptionQuantity = (option: SolutionProductOption, guests: number) => {
  if (option.perPerson) return Math.max(1, guests);
  const name = normalize(option.title);
  if (name.includes("подушка") && guests > 1) return 2;
  return 1;
};

export const recommendedSlotQuantity = (slot: SolutionSlot, guests: number) => {
  const option = slot.options[0];
  return option ? recommendedOptionQuantity(option, guests) : 1;
};

export const optionColors = (option: SolutionProductOption) => Array.from(new Set(option.variants.map((row) => row.color).filter(Boolean)));
export const optionSizes = (option: SolutionProductOption, color = "") => Array.from(new Set(option.variants
  .filter((row) => !color || row.color === color)
  .map((row) => row.size || row.volume)
  .filter(Boolean)));

export const pickOptionVariant = (option: SolutionProductOption, color = "", size = "") => {
  const byColor = color ? option.variants.filter((row) => row.color === color) : option.variants;
  const bySize = size ? byColor.filter((row) => (row.size || row.volume) === size) : byColor;
  return bySize[0] || byColor[0] || option.variants[0];
};

const parseGuestList = (value: string) => String(value || "")
  .split("|")
  .map((item) => Number(item.trim()))
  .filter((item) => Number.isFinite(item) && item > 0);

const collectionTokens = (value: string) => String(value || "")
  .split("|")
  .map(normalize)
  .filter(Boolean);

export const deriveGuestOptions = (solution: TableSolution, data: ConstructorData | null) => {
  const fallback = normalize(solution.space).includes("кух") ? [2, 4, 6] : [1, 2];
  if (!data) return fallback;

  const solutionCollections = solution.collections.map(normalize).filter(Boolean);
  const solutionName = normalize(solution.name);
  const candidates: Array<{ score: number; guests: number[] }> = [];

  const scoreCollections = (values: string[]) => values.reduce((score, value) =>
    score + (solutionCollections.some((collection) => value.includes(collection) || collection.includes(value)) ? 10 : 0), 0);

  const scenarioGroups = new Map<string, { name: string; guests: string; collections: string[] }>();
  data.scenarios.forEach((row) => {
    const entry = scenarioGroups.get(row.scenario_id) || { name: row.scenario_name, guests: row.guests_supported, collections: [] };
    entry.collections.push(...collectionTokens(row.allowed_collections), normalize(row.entry_collection));
    if (!entry.guests) entry.guests = row.guests_supported;
    scenarioGroups.set(row.scenario_id, entry);
  });

  scenarioGroups.forEach((entry) => {
    const guests = parseGuestList(entry.guests);
    if (!guests.length) return;
    const score = (normalize(entry.name) === solutionName ? 100 : 0) + scoreCollections(entry.collections.filter(Boolean));
    if (score > 0) candidates.push({ score, guests });
  });

  const expansionGroups = new Map<string, { name: string; guests: string; collections: string[]; spaces: string[] }>();
  data.expansionRules.forEach((row) => {
    const entry = expansionGroups.get(row.scenario_id) || { name: row.scenario_name, guests: row.guests_supported, collections: [], spaces: [] };
    entry.collections.push(...collectionTokens(row.lead_collections), ...collectionTokens(row.allowed_collections));
    entry.spaces.push(...collectionTokens(row.space));
    expansionGroups.set(row.scenario_id, entry);
  });

  expansionGroups.forEach((entry) => {
    const guests = parseGuestList(entry.guests);
    if (!guests.length) return;
    const space = normalize(solution.space);
    const spaceScore = entry.spaces.some((candidate) =>
      (space.includes("кух") && candidate.includes("kitchen")) ||
      (space.includes("столов") && candidate.includes("dining")) ||
      (space.includes("спаль") && candidate.includes("bedroom")) ||
      (space.includes("кабин") && candidate.includes("living"))
    ) ? 3 : 0;
    const score = (normalize(entry.name) === solutionName ? 100 : 0) + scoreCollections(entry.collections.filter(Boolean)) + spaceScore;
    if (score > 0) candidates.push({ score, guests });
  });

  if (!candidates.length) return fallback;
  candidates.sort((a, b) => b.score - a.score);
  return Array.from(new Set(candidates[0].guests)).sort((a, b) => a - b);
};
