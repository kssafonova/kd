import type { CatalogRow, ConstructorData } from "./types";
import type { TableSolution } from "./table-solutions";

export type SolutionPreset = "basic" | "balanced" | "full";

export type SolutionProductGroup = {
  id: string;
  title: string;
  description: string;
  rows: CatalogRow[];
};

export const SOLUTION_PRESETS: Array<{
  id: SolutionPreset;
  title: string;
  description: string;
}> = [
  { id: "basic", title: "Базовый", description: "Только ключевые предметы — быстро собрать основу." },
  { id: "balanced", title: "Оптимальный", description: "Основа, подача и акценты без перегрузки." },
  { id: "full", title: "Полный образ", description: "Все найденные предметы коллекций в одном решении." },
];

const normalize = (value: string) => String(value || "")
  .trim()
  .toLocaleLowerCase("ru-RU")
  .replace(/ё/g, "е")
  .replace(/[«»"']/g, "")
  .replace(/\s+/g, " ");

const hasAny = (value: string, tokens: string[]) => tokens.some((token) => value.includes(token));

const groupMeta: Record<string, Pick<SolutionProductGroup, "title" | "description">> = {
  personal: { title: "На каждую персону", description: "Тарелки, пары, кружки и предметы, количество которых зависит от числа гостей." },
  tea: { title: "Чай и кофе", description: "Чайники, сахарницы, молочники и предметы для чайного сценария." },
  serving: { title: "Для подачи", description: "Салатники, блюда, подносы и сервировочные предметы." },
  drinkware: { title: "Напитки и стекло", description: "Бокалы, стаканы, графины и декантеры." },
  tableTextile: { title: "Текстиль для стола", description: "Скатерти, дорожки, салфетки и плейсматы." },
  bedding: { title: "Постельный текстиль", description: "Комплекты, пододеяльники, простыни и наволочки." },
  soft: { title: "Мягкий текстиль", description: "Пледы, покрывала и декоративные подушки." },
  bath: { title: "Для ванной", description: "Халаты, полотенца, наборы и аксессуары для ванной." },
  storage: { title: "Хранение", description: "Корзины и функциональные предметы для порядка." },
  decor: { title: "Декор и атмосфера", description: "Вазы, свечи и акцентные предметы, завершающие образ." },
  other: { title: "Дополнения", description: "Дополнительные предметы, которые можно подключить к решению." },
};

export const solutionGroupId = (row: CatalogRow, space: string) => {
  const type = normalize(row.product_type);
  const name = normalize(row.product_name);
  const role = normalize(row.constructor_role);
  const normalizedSpace = normalize(space);

  if (hasAny(type, ["bedding_set", "duvet", "sheet", "pillowcase"]) || hasAny(name, ["комплект постель", "пододеяльник", "простын", "наволоч"])) return "bedding";
  if (hasAny(type, ["decorative_pillow", "throw", "coverlet"]) || hasAny(name, ["плед", "покрывал", "подушка"])) return "soft";
  if (hasAny(name, ["халат", "полотен", "набор для ванн", "коврик для ванн"]) || normalizedSpace.includes("ванн")) {
    if (hasAny(name, ["корзин", "органайзер"])) return "storage";
    return "bath";
  }
  if (hasAny(type, ["tablecloth", "table_runner", "napkin", "placemat"]) || hasAny(name, ["скатерт", "дорожк", "салфет", "плейсмат"])) return "tableTextile";
  if (hasAny(type, ["wine_glass", "glassware", "decanter"]) || hasAny(name, ["бокал", "стакан", "рюм", "графин", "декантер"])) return "drinkware";
  if (hasAny(type, ["tea_pair", "coffee_pair", "mug", "dinner_plate", "snack_plate", "dessert_plate"]) || hasAny(name, ["чайная пара", "кофейная пара", "кружка", "тарелка"])) return "personal";
  if (hasAny(type, ["teapot", "sugar_bowl", "milk_jug"]) || hasAny(name, ["чайник", "сахарниц", "сливочник", "молочник"])) return "tea";
  if (hasAny(type, ["serving_dish", "salad_bowl"]) || hasAny(name, ["салатник", "блюдо", "менажниц", "поднос", "супниц", "икорниц", "масленк"])) return "serving";
  if (hasAny(name, ["корзин", "органайзер", "хранени"])) return "storage";
  if (hasAny(type, ["vase", "candle", "candle_holder"]) || hasAny(role, ["atmosphere"]) || hasAny(name, ["ваза", "свеч", "диффузор", "ширма"])) return "decor";
  return "other";
};

const groupOrder = ["personal", "tea", "serving", "drinkware", "tableTextile", "bedding", "soft", "bath", "storage", "decor", "other"];

export const buildSolutionGroups = (rows: CatalogRow[], space: string): SolutionProductGroup[] => {
  const map = new Map<string, CatalogRow[]>();
  rows.forEach((row) => {
    const id = solutionGroupId(row, space);
    map.set(id, [...(map.get(id) || []), row]);
  });
  return groupOrder
    .filter((id) => map.has(id))
    .map((id) => ({ id, ...groupMeta[id], rows: map.get(id) || [] }));
};

export const isPerPersonProduct = (row: CatalogRow, space: string) => {
  const group = solutionGroupId(row, space);
  const name = normalize(row.product_name);
  if (name.startsWith("набор ")) return false;
  if (group === "personal") return true;
  if (group === "tableTextile" && hasAny(name, ["салфет", "плейсмат"])) return true;
  return false;
};

export const recommendedProductQuantity = (row: CatalogRow, space: string, guests: number) => {
  if (isPerPersonProduct(row, space)) return Math.max(1, guests);
  const name = normalize(row.product_name);
  if (solutionGroupId(row, space) === "soft" && hasAny(name, ["подушка"]) && guests > 1) return 2;
  return 1;
};

export const selectionForPreset = (groups: SolutionProductGroup[], preset: SolutionPreset) => {
  const selected = new Set<string>();
  groups.forEach((group) => {
    let limit = group.rows.length;
    if (preset === "basic") {
      if (group.id === "decor" || group.id === "other") limit = 0;
      else limit = Math.min(1, group.rows.length);
    }
    if (preset === "balanced") {
      if (group.id === "decor" || group.id === "other") limit = Math.min(1, group.rows.length);
      else limit = Math.min(2, group.rows.length);
    }
    group.rows.slice(0, limit).forEach((row) => selected.add(row.offer_id));
  });
  return selected;
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
