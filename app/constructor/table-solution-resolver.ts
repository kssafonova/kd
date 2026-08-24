import type { CatalogRow } from "./types";
import type { TableSolution } from "./table-solutions";

export const normalizeSolutionValue = (value: string) =>
  String(value || "")
    .trim()
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/[«»"']/g, "")
    .replace(/\s+/g, " ");

const matchesLoose = (value: string, target: string) => {
  if (!value || !target) return false;
  return value === target || value.includes(target) || target.includes(value);
};

const collectionOrder = (row: CatalogRow, targets: string[]) => {
  const collection = normalizeSolutionValue(row.collection || "");
  const index = targets.findIndex((target) => matchesLoose(collection, target));
  return index < 0 ? 999 : index;
};

const rowMatchesSolution = (row: CatalogRow, solution: TableSolution) => {
  const collectionTargets = solution.collections.map(normalizeSolutionValue).filter(Boolean);
  const productTargets = solution.productNames.map(normalizeSolutionValue).filter(Boolean);
  const collection = normalizeSolutionValue(row.collection || "");
  const productName = normalizeSolutionValue(row.product_name || "");
  const collectionMatch = collectionTargets.some((target) => matchesLoose(collection, target) || productName.includes(target));
  const explicitProductMatch = productTargets.some((target) => matchesLoose(productName, target));
  return collectionMatch || explicitProductMatch;
};

const COLOR_WORDS = [
  "темно-синий", "темно-синяя", "темно-синее", "темно-синие",
  "ночной синий", "ночная синяя",
  "белый", "белая", "белое", "белые",
  "молочный", "молочная", "молочное", "молочные",
  "синий", "синяя", "синее", "синие",
  "голубой", "голубая", "голубое", "голубые",
  "пудровый", "пудровая", "пудровое", "пудровые",
  "розовый", "розовая", "розовое", "розовые",
  "льняной", "льняная", "льняное", "льняные",
  "бежевый", "бежевая", "бежевое", "бежевые",
  "песочный", "песочная", "песочное", "песочные",
  "серый", "серая", "серое", "серые",
  "зеленый", "зеленая", "зеленое", "зеленые",
  "красный", "красная", "красное", "красные",
  "бордовый", "бордовая", "бордовое", "бордовые",
  "желтый", "желтая", "желтое", "желтые",
  "черный", "черная", "черное", "черные",
  "золотой", "золотая", "золотое", "золотые",
  "серебристый", "серебристая", "серебристое", "серебристые",
];

const canonicalProductName = (row: CatalogRow) => {
  let value = normalizeSolutionValue(String(row.product_name || "").split(":")[0]);
  COLOR_WORDS.forEach((word) => {
    value = value.replace(new RegExp(`(^|\\s)${word.replace(/[.*+?^${}()|[\\]\\]/g, "\\$&")}(?=\\s|$)`, "g"), " ");
  });
  return value.replace(/\s+/g, " ").trim();
};

/**
 * Storefront product identity:
 * - same collection + same base product => one card;
 * - colour and size rows become variants inside that card;
 * - the same generic product name from two different collections stays separate.
 */
export const logicalProductKey = (row: CatalogRow) => {
  const name = canonicalProductName(row);
  const collection = normalizeSolutionValue(row.collection || "");
  if (name) return `product:${collection || "no-collection"}:${name}`;
  const group = String(row.group_id || "").trim();
  return group ? `group:${group}` : `offer:${row.offer_id}`;
};

/** All matching CSV rows, including color and size variants. */
export const resolveTableSolutionCatalogRows = (catalog: CatalogRow[], solution: TableSolution) => {
  const collectionTargets = solution.collections.map(normalizeSolutionValue).filter(Boolean);
  return catalog
    .filter((row) => rowMatchesSolution(row, solution))
    .sort((a, b) => {
      const collectionDiff = collectionOrder(a, collectionTargets) - collectionOrder(b, collectionTargets);
      if (collectionDiff) return collectionDiff;
      const nameDiff = String(a.product_name || "").localeCompare(String(b.product_name || ""), "ru");
      if (nameDiff) return nameDiff;
      const colorDiff = String(a.color || "").localeCompare(String(b.color || ""), "ru");
      if (colorDiff) return colorDiff;
      return String(a.size || "").localeCompare(String(b.size || ""), "ru");
    });
};

/** One representative per logical product; used on the ready-solutions landing. */
export const resolveTableSolutionProducts = (catalog: CatalogRow[], solution: TableSolution) => {
  const rows = resolveTableSolutionCatalogRows(catalog, solution);
  const unique = new Map<string, CatalogRow>();

  rows.forEach((row) => {
    const key = logicalProductKey(row);
    const current = unique.get(key);
    if (!current) {
      unique.set(key, row);
      return;
    }
    const currentScore = Number(Boolean(current.primary_image_url)) + Number(Boolean(current.price));
    const nextScore = Number(Boolean(row.primary_image_url)) + Number(Boolean(row.price));
    if (nextScore > currentScore) unique.set(key, row);
  });

  return Array.from(unique.values());
};
