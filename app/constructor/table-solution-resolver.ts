import { catalogProductOverrides, type CatalogProductOverride, type CatalogSku } from "../catalog-data";
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
  const typeTargets = (solution.allowedProductTypes || []).map(normalizeSolutionValue).filter(Boolean);

  const collection = normalizeSolutionValue(row.collection || "");
  const productName = normalizeSolutionValue(row.product_name || "");
  const productType = normalizeSolutionValue(row.product_type || "");

  const rawCollectionMatch = collectionTargets.some(
    (target) => matchesLoose(collection, target) || productName.includes(target),
  );
  const typeMatch = !typeTargets.length || typeTargets.some((target) => matchesLoose(productType, target));
  const collectionMatch = solution.includeCollectionProducts !== false && rawCollectionMatch && typeMatch;
  const explicitProductMatch = productTargets.some((target) => matchesLoose(productName, target));

  return collectionMatch || explicitProductMatch;
};

const normalizeLocalImage = (value: string) => {
  const path = String(value || "").trim();
  return path.startsWith("/kd/images/") ? path.slice(3) : path;
};

const inferGithubProductType = (product: CatalogProductOverride) => {
  const name = normalizeSolutionValue(product.name);
  if (name.includes("комплект постельного белья")) return "bedding_set";
  if (name.includes("пододеяльник")) return "duvet";
  if (name.includes("простын")) return "sheet";
  if (name.includes("наволоч")) return "pillowcase";
  if (name.includes("покрывал")) return "coverlet";
  if (name.includes("плед")) return "throw";
  if (name.includes("подушка")) return "decorative_pillow";
  if (name.includes("тарел")) return "plate";
  if (name.includes("салатник")) return "salad_bowl";
  if (name.includes("чайная пара")) return "tea_pair";
  return "other";
};

const fallbackGithubCollection = (product: CatalogProductOverride, sku: CatalogSku) => {
  if (sku.collection) return sku.collection;
  const name = normalizeSolutionValue(product.name);
  if (name.includes("ледяные узоры")) return "Ледяные узоры";
  if (name.includes("лунная сказка")) return "Лунная сказка";
  return "Культура Дома";
};

const githubProductRows = (solution: TableSolution): CatalogRow[] => {
  const ids = solution.githubProductIds || [];
  return ids.flatMap((productId) => {
    const product = catalogProductOverrides[productId];
    if (!product) return [];
    const productType = inferGithubProductType(product);

    return product.skus.map((sku) => {
      const image = normalizeLocalImage(sku.image);
      const gallery = Array.from(new Set([image, ...sku.gallery.map(normalizeLocalImage)].filter(Boolean)));
      return {
        offer_id: sku.id,
        group_id: String(product.id),
        vendor_code: sku.article || product.article,
        collection: fallbackGithubCollection(product, sku),
        product_name: product.name,
        product_url: "",
        product_type: productType,
        constructor_role: "bedroom_layer",
        mix_role: "",
        builder_domain: "bedroom",
        palette: "",
        style_tags: "",
        price: String(sku.price || 0),
        old_price: "",
        color: sku.color || "",
        size: sku.size || "",
        material: sku.material || "",
        volume: "",
        availability_status: sku.available === false ? "out_of_stock" : "available",
        primary_image_url: image,
        all_image_urls: gallery.join("|"),
      } satisfies CatalogRow;
    });
  });
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

export const logicalProductKey = (row: CatalogRow) => {
  const name = canonicalProductName(row);
  const collection = normalizeSolutionValue(row.collection || "");
  if (name) return `product:${collection || "no-collection"}:${name}`;
  const group = String(row.group_id || "").trim();
  return group ? `group:${group}` : `offer:${row.offer_id}`;
};

/**
 * All matching rows, including colour and size variants.
 * A ready solution may combine exact products from the GitHub storefront
 * catalog with explicit products from constructor CSV. When the same logical
 * product exists in both sources, the GitHub storefront version wins so its
 * local imagery and variants stay authoritative.
 */
export const resolveTableSolutionCatalogRows = (catalog: CatalogRow[], solution: TableSolution) => {
  const collectionTargets = solution.collections.map(normalizeSolutionValue).filter(Boolean);
  const csvRows = catalog.filter((row) => rowMatchesSolution(row, solution));
  const githubRows = solution.githubProductIds?.length ? githubProductRows(solution) : [];
  const githubKeys = new Set(githubRows.map(logicalProductKey));
  const sourceRows = githubRows.length
    ? [...githubRows, ...csvRows.filter((row) => !githubKeys.has(logicalProductKey(row)))]
    : csvRows;

  return sourceRows.sort((a, b) => {
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
