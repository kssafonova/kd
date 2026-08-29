export type { CatalogSku, CatalogProductOverride } from "./catalog-data-base";
import { catalogProductOverrides as baseOverrides, type CatalogSku } from "./catalog-data-base";

// No legacy hardcoded products: runtime products are loaded from the refreshed CSV catalog.
export const catalogProductOverrides = baseOverrides;

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  Object.values(catalogProductOverrides).flatMap((product) => product.skus).map((item) => [item.id, item])
);
