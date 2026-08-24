import type { CatalogRow, ConstructorData } from "./types";
import type { TableSolution } from "./table-solutions";
import { logicalProductKey } from "./table-solution-resolver";

export type SolutionProductOption = {
  id: string;
  title: string;
  collection: string;
  variants: CatalogRow[];
};

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
const slug = (value: string) => normalize(value).replace(/[^a-zа-я0-9]+/g, "-").replace(/^-|-$/g, "");
const baseName = (row: CatalogRow) => String(row.product_name || "Товар").split(":")[0].trim();

const categoryMeta: Record<string, { title: string; description: string }> = {
  plates: { title: "Тарелки", description: "Все тарелки собраны вместе независимо от коллекции — выберите подходящую серию для каждого типа." },
  teaPairs: { title: "Чайные и кофейные пары", description: "Выберите пары из предложенных коллекций. Количество рассчитывается на число персон." },
  teaAccessories: { title: "Чай и кофе — дополнения", description: "Чайники, сахарницы, молочники и другие предметы можно подключить по необходимости." },
  serving: { title: "Сервировка и подача", description: "Салатники, блюда, подносы и другие предметы для общей подачи." },
  drinkware: { title: "Бокалы и стекло", description: "Бокалы, стаканы, графины и декантеры из подходящих коллекций." },
  tableTextile: { title: "Столовый текстиль", description: "Скатерти, дорожки, плейсматы и салфетки для выбранного сценария." },
  baskets: { title: "Корзины", description: "Все корзины показаны рядом, чтобы удобно сравнить форму, материал и коллекцию." },
  storage: { title: "Хранение", description: "Органайзеры и другие функциональные предметы для порядка." },
  bedding: { title: "Постельный текстиль", description: "Комплекты, пододеяльники, простыни и наволочки. Цвета и размеры объединены внутри товара." },
  soft: { title: "Пледы и подушки", description: "Мягкий текстиль для завершения решения. Цветовые варианты объединены внутри одной карточки." },
  bath: { title: "Для ванной", description: "Халаты, полотенца, коврики и наборы для ванной." },
  decor: { title: "Декор и атмосфера", description: "Вазы, свечи и декоративные акценты — добавляйте только если они нужны." },
  other: { title: "Дополнения", description: "Остальные найденные предметы решения." },
};

const slotMeta = (row: CatalogRow, space: string) => {
  const name = normalize(row.product_name);
  const type = normalize(row.product_type);
  const normalizedSpace = normalize(space);

  if (hasAny(name, ["тарелка десерт"]) || type.includes("dessert_plate")) return { categoryId: "plates", id: "dessert-plate", title: "Десертная тарелка", perPerson: true };
  if (hasAny(name, ["тарелка глубок"]) || type.includes("deep_plate")) return { categoryId: "plates", id: "deep-plate", title: "Глубокая тарелка", perPerson: true };
  if (hasAny(name, ["тарелка закус"]) || type.includes("snack_plate")) return { categoryId: "plates", id: "snack-plate", title: "Закусочная тарелка", perPerson: true };
  if (hasAny(name, ["тарелка", "блюдце"]) || hasAny(type, ["dinner_plate", "plate"])) return { categoryId: "plates", id: "plate", title: "Тарелка", perPerson: true };

  if (name.includes("чайная пара") || type.includes("tea_pair")) return { categoryId: "teaPairs", id: "tea-pair", title: "Чайная пара", perPerson: true };
  if (name.includes("кофейная пара") || type.includes("coffee_pair")) return { categoryId: "teaPairs", id: "coffee-pair", title: "Кофейная пара", perPerson: true };
  if (name.includes("круж") || type.includes("mug")) return { categoryId: "teaPairs", id: "mug", title: "Кружка", perPerson: true };

  if (name.includes("сахарниц") || type.includes("sugar_bowl")) return { categoryId: "teaAccessories", id: "sugar-bowl", title: "Сахарница", perPerson: false };
  if (hasAny(name, ["молочник", "сливочник"]) || type.includes("milk_jug")) return { categoryId: "teaAccessories", id: "milk-jug", title: "Молочник / сливочник", perPerson: false };
  if (name.includes("чайник") || type.includes("teapot")) return { categoryId: "teaAccessories", id: "teapot", title: "Чайник", perPerson: false };

  if (name.includes("салатник") || type.includes("salad_bowl")) return { categoryId: "serving", id: "salad-bowl", title: "Салатник", perPerson: false };
  if (name.includes("поднос")) return { categoryId: "serving", id: "tray", title: "Поднос", perPerson: false };
  if (name.includes("супниц")) return { categoryId: "serving", id: "soup-tureen", title: "Супница", perPerson: false };
  if (hasAny(name, ["блюдо", "менажниц", "икорниц", "масленк"]) || type.includes("serving_dish")) return { categoryId: "serving", id: "serving-dish", title: "Блюдо для подачи", perPerson: false };

  if (hasAny(name, ["бокал", "рюм"]) || type.includes("wine_glass")) return { categoryId: "drinkware", id: "wine-glass", title: "Бокалы", perPerson: true };
  if (name.includes("стакан") || type.includes("glassware")) return { categoryId: "drinkware", id: "glass", title: "Стаканы", perPerson: true };
  if (hasAny(name, ["графин", "декантер"]) || type.includes("decanter")) return { categoryId: "drinkware", id: "decanter", title: "Графин / декантер", perPerson: false };

  if (name.includes("скатерт") || type.includes("tablecloth")) return { categoryId: "tableTextile", id: "tablecloth", title: "Скатерть", perPerson: false };
  if (name.includes("дорожк") || type.includes("table_runner")) return { categoryId: "tableTextile", id: "runner", title: "Дорожка", perPerson: false };
  if (name.includes("плейсмат") || type.includes("placemat")) return { categoryId: "tableTextile", id: "placemat", title: "Плейсмат", perPerson: true };
  if (name.includes("салфет") || type.includes("napkin")) return { categoryId: "tableTextile", id: "napkin", title: "Салфетка", perPerson: true };

  if (name.includes("корзин")) return { categoryId: "baskets", id: "basket", title: "Корзина", perPerson: false };
  if (hasAny(name, ["органайзер", "хранени"])) return { categoryId: "storage", id: "storage", title: "Хранение", perPerson: false };

  if (hasAny(name, ["комплект постель", "постельное белье"]) || type.includes("bedding_set")) return { categoryId: "bedding", id: "bedding-set", title: "Комплект постельного белья", perPerson: false };
  if (name.includes("пододеяльник") || type.includes("duvet")) return { categoryId: "bedding", id: "duvet", title: "Пододеяльник", perPerson: false };
  if (name.includes("простын") || type.includes("sheet")) return { categoryId: "bedding", id: "sheet", title: "Простыня", perPerson: false };
  if (name.includes("наволоч") || type.includes("pillowcase")) return { categoryId: "bedding", id: "pillowcase", title: "Наволочка", perPerson: false };

  if (name.includes("подушка") || type.includes("decorative_pillow")) return { categoryId: "soft", id: "pillow", title: "Подушка", perPerson: false };
  if (name.includes("плед") || type.includes("throw")) return { categoryId: "soft", id: "throw", title: "Плед", perPerson: false };
  if (name.includes("покрывал") || type.includes("coverlet")) return { categoryId: "soft", id: "coverlet", title: "Покрывало", perPerson: false };

  if (name.includes("халат")) return { categoryId: "bath", id: "robe", title: "Халат", perPerson: normalizedSpace.includes("ванн") };
  if (name.includes("полотен")) return { categoryId: "bath", id: "towel", title: "Полотенце", perPerson: normalizedSpace.includes("ванн") };
  if (name.includes("коврик") && normalizedSpace.includes("ванн")) return { categoryId: "bath", id: "bath-mat", title: "Коврик для ванной", perPerson: false };
  if (name.includes("набор для ванн")) return { categoryId: "bath", id: "bath-set", title: "Набор для ванной", perPerson: false };

  if (hasAny(name, ["ваза", "свеч", "диффузор"]) || hasAny(type, ["vase", "candle", "candle_holder"])) return { categoryId: "decor", id: slug(type || baseName(row)) || "decor", title: baseName(row), perPerson: false };

  return { categoryId: "other", id: slug(type || baseName(row)) || "other", title: baseName(row), perPerson: false };
};

const categoryOrder = ["plates", "teaPairs", "teaAccessories", "serving", "drinkware", "tableTextile", "baskets", "storage", "bedding", "soft", "bath", "decor", "other"];

export const buildSolutionCategories = (rows: CatalogRow[], space: string): SolutionCategory[] => {
  const categoryMap = new Map<string, Map<string, Map<string, CatalogRow[]>>>();
  const slotTitles = new Map<string, { title: string; perPerson: boolean }>();

  rows.forEach((row) => {
    const meta = slotMeta(row, space);
    const optionId = logicalProductKey(row);
    if (!categoryMap.has(meta.categoryId)) categoryMap.set(meta.categoryId, new Map());
    const slotMap = categoryMap.get(meta.categoryId)!;
    if (!slotMap.has(meta.id)) slotMap.set(meta.id, new Map());
    const optionMap = slotMap.get(meta.id)!;
    optionMap.set(optionId, [...(optionMap.get(optionId) || []), row]);
    slotTitles.set(`${meta.categoryId}:${meta.id}`, { title: meta.title, perPerson: meta.perPerson });
  });

  return categoryOrder.filter((categoryId) => categoryMap.has(categoryId)).map((categoryId) => {
    const slotMap = categoryMap.get(categoryId)!;
    const slots: SolutionSlot[] = Array.from(slotMap.entries()).map(([slotId, optionMap]) => {
      const slotInfo = slotTitles.get(`${categoryId}:${slotId}`)!;
      const options: SolutionProductOption[] = Array.from(optionMap.entries()).map(([optionId, variants]) => ({
        id: optionId,
        title: baseName(variants[0]),
        collection: variants[0]?.collection || "Культура Дома",
        variants: Array.from(new Map(variants.map((row) => [row.offer_id, row])).values()),
      })).sort((a, b) => a.collection.localeCompare(b.collection, "ru") || a.title.localeCompare(b.title, "ru"));
      return {
        id: `${categoryId}-${slotId}`,
        title: slotInfo.title,
        description: options.length > 1 ? `Выберите один вариант из ${options.length} предложенных товаров.` : "Можно добавить в решение или убрать.",
        perPerson: slotInfo.perPerson,
        options,
      };
    });
    return { id: categoryId, ...categoryMeta[categoryId], slots };
  });
};

export const recommendedSlotQuantity = (slot: SolutionSlot, guests: number) => slot.perPerson ? Math.max(1, guests) : 1;

export const optionColors = (option: SolutionProductOption) => Array.from(new Set(option.variants.map((row) => row.color).filter(Boolean)));
export const optionSizes = (option: SolutionProductOption, color = "") => Array.from(new Set(option.variants.filter((row) => !color || row.color === color).map((row) => row.size || row.volume).filter(Boolean)));

export const pickOptionVariant = (option: SolutionProductOption, color = "", size = "") => {
  const byColor = color ? option.variants.filter((row) => row.color === color) : option.variants;
  const bySize = size ? byColor.filter((row) => (row.size || row.volume) === size) : byColor;
  return bySize[0] || byColor[0] || option.variants[0];
};

const parseGuestList = (value: string) => String(value || "").split("|").map((item) => Number(item.trim())).filter((item) => Number.isFinite(item) && item > 0);
const collectionTokens = (value: string) => String(value || "").split("|").map(normalize).filter(Boolean);

export const deriveGuestOptions = (solution: TableSolution, data: ConstructorData | null) => {
  const space = normalize(solution.space);
  const fallback = space.includes("кух") || space.includes("столов") ? [2, 4, 6] : [1, 2];
  if (!data) return fallback;

  const solutionCollections = solution.collections.map(normalize).filter(Boolean);
  const solutionName = normalize(solution.name);
  const candidates: Array<{ score: number; guests: number[] }> = [];
  const scoreCollections = (values: string[]) => values.reduce((score, value) => score + (solutionCollections.some((collection) => value.includes(collection) || collection.includes(value)) ? 10 : 0), 0);

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

  data.expansionRules.forEach((row) => {
    const guests = parseGuestList(row.guests_supported);
    if (!guests.length) return;
    const collections = [...collectionTokens(row.lead_collections), ...collectionTokens(row.allowed_collections)];
    const score = (normalize(row.scenario_name) === solutionName ? 100 : 0) + scoreCollections(collections);
    if (score > 0) candidates.push({ score, guests });
  });

  if (!candidates.length) return fallback;
  candidates.sort((a, b) => b.score - a.score);
  return Array.from(new Set(candidates[0].guests)).sort((a, b) => a - b);
};
