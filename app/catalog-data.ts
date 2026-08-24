export type { CatalogSku, CatalogProductOverride } from "./catalog-data-base";
import { catalogProductOverrides as baseOverrides, type CatalogSku } from "./catalog-data-base";

// KD-PD-1022_MEDIA_V1
const duvetImageByColor:Record<string,string> = {
  "Белый":"/images/products/KD-PD-1022-WHITE01.png",
  "Льняной":"/images/products/KD-PD-1022-LEN01.png",
  "Небесный":"/images/products/KD-PD-1022-BLUE01.png",
  "Пудровый":"/images/products/KD-PD-1022-PUDRA01.png",
  "Ночной синий":"/images/products/KD-PD-1022-DARK01.png",
};

const duvet = baseOverrides[2];
if (duvet?.article === "KD-PD-1022") {
  duvet.skus = duvet.skus.map((sku) => {
    const image = duvetImageByColor[sku.color] ?? sku.image;
    return { ...sku, image, gallery: [] };
  });
}

export const catalogProductOverrides = baseOverrides;

export const catalogSkuById:Record<string,CatalogSku> = Object.fromEntries(
  Object.values(catalogProductOverrides).flatMap((product) => product.skus).map((item) => [item.id, item])
);
