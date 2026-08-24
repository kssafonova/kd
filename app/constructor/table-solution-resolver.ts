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

const logicalProductKey = (row: CatalogRow) => {
  const group = String(row.group_id || "").trim();
  if (group) return `group:${group}`;
  return `name:${normalizeSolutionValue(row.product_name || "")}`;
};

/**
 * Returns every logical product we can ground in the CSV catalog for a ready
 * solution. Collection membership is the primary rule. Explicit names from
 * the source table are additive, so a manually listed item is never lost.
 * Size/SKU variants are collapsed to one representative product row.
 */
export const resolveTableSolutionProducts = (catalog: CatalogRow[], solution: TableSolution) => {
  const collectionTargets = solution.collections.map(normalizeSolutionValue).filter(Boolean);
  const productTargets = solution.productNames.map(normalizeSolutionValue).filter(Boolean);
  const unique = new Map<string, CatalogRow>();

  catalog.forEach((row) => {
    const collection = normalizeSolutionValue(row.collection || "");
    const productName = normalizeSolutionValue(row.product_name || "");

    const collectionMatch = collectionTargets.some((target) =>
      matchesLoose(collection, target) || productName.includes(target)
    );
    const explicitProductMatch = productTargets.some((target) =>
      matchesLoose(productName, target)
    );

    if (!collectionMatch && !explicitProductMatch) return;

    const key = logicalProductKey(row);
    const current = unique.get(key);
    if (!current) {
      unique.set(key, row);
      return;
    }

    // Prefer a representative with a usable image and price.
    const currentScore = Number(Boolean(current.primary_image_url)) + Number(Boolean(current.price));
    const nextScore = Number(Boolean(row.primary_image_url)) + Number(Boolean(row.price));
    if (nextScore > currentScore) unique.set(key, row);
  });

  return Array.from(unique.values()).sort((a, b) => {
    const aCollection = normalizeSolutionValue(a.collection || "");
    const bCollection = normalizeSolutionValue(b.collection || "");
    const aCollectionIndex = collectionTargets.findIndex((target) => matchesLoose(aCollection, target));
    const bCollectionIndex = collectionTargets.findIndex((target) => matchesLoose(bCollection, target));
    const ai = aCollectionIndex < 0 ? 999 : aCollectionIndex;
    const bi = bCollectionIndex < 0 ? 999 : bCollectionIndex;
    if (ai !== bi) return ai - bi;
    return String(a.product_name || "").localeCompare(String(b.product_name || ""), "ru");
  });
};
