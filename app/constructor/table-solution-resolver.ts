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

const baseProductName = (row: CatalogRow) => normalizeSolutionValue(String(row.product_name || "").split(":")[0]);

/**
 * Product identity intentionally prefers the catalog-facing product name over
 * group_id: the source feed may store different colours as separate 1C groups.
 * This lets one storefront product contain all colour/size variants.
 */
export const logicalProductKey = (row: CatalogRow) => {
  const name = baseProductName(row);
  if (name) return `name:${name}`;
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
