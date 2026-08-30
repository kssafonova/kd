from pathlib import Path

root=Path(__file__).resolve().parents[1]
app=root/"app"
generated=app/"site-database.generated.ts"

if generated.exists():
    text=generated.read_text(encoding="utf-8")
    marker="const SITE_DB_CATALOG_CACHE=new Map<string,Promise<SiteDatabaseRow[]>>();"
    start=text.find(marker)
    if start!=-1:
        wrapper='''const SITE_DB_CATALOG_CACHE=new Map<string,Promise<SiteDatabaseRow[]>>();
export function loadSiteDatabaseCatalogRows(base=""):Promise<SiteDatabaseRow[]> {
  const key=base||"/";const cached=SITE_DB_CATALOG_CACHE.get(key);if(cached)return cached;
  const task=(async()=>{
    try{
      const response=await fetch(`${base}/data/catalog_master.csv`,{cache:"force-cache"});
      if(response.ok){const projected=parseSiteDbCsv(await response.text());if(projected.length)return projected}
    }catch{}
    return loadSiteDatabaseCatalogRowsUncached(base);
  })();
  SITE_DB_CATALOG_CACHE.set(key,task);task.catch(()=>SITE_DB_CATALOG_CACHE.delete(key));return task;
}
'''
        text=text[:start]+wrapper
        generated.write_text(text,encoding="utf-8")
        print("Catalog runtime now prefers single catalog_master.csv projection")

catalog=app/"catalog"
(catalog/"page.tsx").write_text('''import CatalogClient from "./catalog-client";

const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";

export default function CatalogPage(){
  return <>
    <link rel="preload" as="fetch" href={`${BASE}/data/catalog_master.csv`} crossOrigin="anonymous" />
    <CatalogClient />
  </>;
}
''',encoding="utf-8")
