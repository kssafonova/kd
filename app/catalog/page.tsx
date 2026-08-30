import CatalogClient from "./catalog-client";

const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";

export default function CatalogPage(){
  return <>
    <link rel="preload" as="fetch" href={`${BASE}/data/database/01_products.csv`} crossOrigin="anonymous" />
    <link rel="preload" as="fetch" href={`${BASE}/data/database/02_product_variants.csv`} crossOrigin="anonymous" />
    <link rel="preload" as="fetch" href={`${BASE}/data/database/03_product_images.csv`} crossOrigin="anonymous" />
    <CatalogClient />
  </>;
}
