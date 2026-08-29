export type CatalogSku = {
  id:string;
  article:string;
  productId:number;
  color:string;
  colorHex:string;
  size:string;
  height?:string;
  width?:string;
  diameter?:string;
  packageInfo?:string;
  material:string;
  composition:string;
  details?:string;
  collection?:string;
  capsule?:string;
  price:number;
  image:string;
  gallery:string[];
  available?:boolean;
};

export type CatalogProductOverride = {
  id:number;
  article:string;
  name:string;
  note:string;
  skus:CatalogSku[];
};

// The storefront catalog is sourced only from public/data/catalog_xlsx_full.csv.
// Legacy hardcoded product overrides were intentionally removed during the full catalog refresh.
export const catalogProductOverrides:Record<number,CatalogProductOverride> = {};
