import CatalogClient from "./catalog-client";

const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";

export default function CatalogPage(){
  return <>
    <link rel="preload" as="fetch" href={`${BASE}/data/catalog_master.csv`} crossOrigin="anonymous" />
    <CatalogClient />
  </>;
}
