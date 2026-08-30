from pathlib import Path
import shutil

root=Path(__file__).resolve().parents[1]
app=root/"app"
page=app/"page.tsx"
storefront=app/"storefront-app.tsx"

# Preserve the fully migrated legacy storefront as a catalog-only client runtime.
if page.exists() and "loadCatalogMasterIntoProducts" in page.read_text(encoding="utf-8"):
    shutil.copyfile(page,storefront)
    print("Captured migrated monolithic storefront in app/storefront-app.tsx")

# Catalog runtime must return to the standalone homepage instead of rendering HomeView inside /catalog/.
if storefront.exists():
    text=storefront.read_text(encoding="utf-8")
    old='const go = (next: View) => { setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };'
    new='const go = (next: View) => { if(next==="home"){const base=process.env.NEXT_PUBLIC_BASE_PATH??"";window.location.href=`${base}/`;return;} setView(next); setMenu(false); window.scrollTo({ top: 0, behavior: "smooth" }); };'
    if old in text:
        text=text.replace(old,new,1)
    storefront.write_text(text,encoding="utf-8")

# Restore the lightweight standalone homepage entry after legacy scripts have finished.
page.write_text('import "./home-standalone.css";\nimport HomeStandalone from "./home-standalone";\n\nexport default function HomePage(){\n  return <HomeStandalone />;\n}\n',encoding="utf-8")

catalog=app/"catalog"
catalog.mkdir(exist_ok=True)
(catalog/"catalog-client.tsx").write_text('''"use client";

import { useEffect, useState } from "react";
import StorefrontApp from "../storefront-app";

export default function CatalogClient(){
  const [category,setCategory]=useState("Все товары");
  useEffect(()=>{
    setCategory(new URLSearchParams(window.location.search).get("category")||"Все товары");
  },[]);
  return <StorefrontApp initialView="catalog" initialCatalogCategory={category}/>;
}
''',encoding="utf-8")
(catalog/"page.tsx").write_text('''import CatalogClient from "./catalog-client";

const BASE=process.env.NEXT_PUBLIC_BASE_PATH??"";

export default function CatalogPage(){
  return <>
    <link rel="preload" as="fetch" href={`${BASE}/data/database/01_products.csv`} crossOrigin="anonymous" />
    <link rel="preload" as="fetch" href={`${BASE}/data/database/02_product_variants.csv`} crossOrigin="anonymous" />
    <link rel="preload" as="fetch" href={`${BASE}/data/database/03_product_images.csv`} crossOrigin="anonymous" />
    <CatalogClient />
  </>;
}
''',encoding="utf-8")

# Root layout stays deliberately tiny. Catalog-specific CSS and enhancers live in /catalog/layout.tsx.
(app/"layout.tsx").write_text('''import type { Metadata } from "next";
import "./globals.css";

export const metadata:Metadata={
  title:"Культура дома — премиальные товары для дома",
  description:"Текстиль, посуда и предметы для дома с русским характером.",
};

export default function RootLayout({children}:{children:React.ReactNode}){
  return <html lang="ru"><body>{children}</body></html>;
}
''',encoding="utf-8")

(catalog/"layout.tsx").write_text('''import "../catalog-filters-v123.css";
import "../catalog-filters-kultura-v124.css";
import "../mobile-quick-add.css";
import "../product-media-scroll.css";
import "../product-card-gallery.css";
import "../boutique-drawer.css";
import "../mobile-pdp-overrides.css";
import "../zara-editorial.css";
import "../luna-editorial.css";
import "../collection-flow.css";
import "../editorial-magazine.css";
import "../ice-editorial-zara.css";
import "../editorial-story-overlay.css";
import "../constructor-entry.css";
import "../menu-zara-premium.css";
import "../site-ux-polish-v1.css";
import "../gift-wrap-flow.css";
import "../image-square-system-v15.css";
import "../collection-purchase-v16.css";
import "../cart-redesign-v17.css";
import "../cart-controls-v18.css";
import "../cart-controls-v19.css";
import "../auth-flow-v20.css";
import "../profile-address-book-v16.css";
import "../profile-address-book-order-v21.css";
import "../unified-stories-v52.css";
import "../commerce-zara-kultura-v41.css";
import "../commerce-hypotheses-v42.css";
import "../commerce-clarity-v43.css";
import "../collections-v65.css";
import "../collections-zara-kultura-v66.css";
import "../mobile-cart-checkout-v67.css";
import "../one-screen-checkout-v68.css";
import "../cart-checkout-mockup-v69.css";
import "../cart-checkout-kultura-v78.css";
import "../editorial-commerce-v81.css";
import "../checkout-kultura-v82.css";
import "../checkout-v83.css";
import "../checkout-bonus-v84.css";
import "../checkout-kultura-v85.css";
import "../truth-commerce.css";
import "../catalog-human-eye-v127.css";
import "../catalog-loading-state-v127.css";
import "../catalog-mobile-premium-v128.css";
import "../catalog-mobile-human-eye-v131.css";
import "../catalog-togas-v132.css";
import "../cart-checkout-human-eye-v136.css";
import { ProductCardGalleryEnhancer } from "../product-card-gallery";
import { CollectionPurchaseEnhancer } from "../collection-purchase-enhancer";
import { ProfileAddressBookEnhancer } from "../profile-address-book";
import { TruthCommerceEnhancer } from "../truth-commerce-enhancer";
import { CatalogLoadingStateV127 } from "../catalog-loading-state-v127";
import { CatalogTogasV132Enhancer } from "../catalog-togas-v132-enhancer";
import { CartCheckoutHumanEyeV136Enhancer } from "../cart-checkout-human-eye-v136-enhancer";

export default function CatalogLayout({children}:{children:React.ReactNode}){
  return <>
    <ProductCardGalleryEnhancer />
    <CollectionPurchaseEnhancer />
    <ProfileAddressBookEnhancer />
    <TruthCommerceEnhancer />
    <CatalogLoadingStateV127 />
    <CatalogTogasV132Enhancer />
    <CartCheckoutHumanEyeV136Enhancer />
    {children}
  </>;
}
''',encoding="utf-8")

# Keep raw CSV as the source of truth, but stop refetching/reparsing identical tables on every mount.
generated=app/"site-database.generated.ts"
if generated.exists():
    text=generated.read_text(encoding="utf-8")
    helper_start=text.find("const fetchSiteDbTable=async(base:string,fileName:string)=>{")
    loader_start=text.find("export async function loadSiteDatabaseCatalogRows",helper_start)
    if helper_start!=-1 and loader_start!=-1:
        helper='''const SITE_DB_TABLE_CACHE=new Map<string,Promise<SiteDatabaseRow[]>>();
const fetchSiteDbTable=(base:string,fileName:string)=>{
  const key=`${base}|${fileName}`;
  const cached=SITE_DB_TABLE_CACHE.get(key);if(cached)return cached;
  const task=(async()=>{try{const response=await fetch(`${base}/data/database/${fileName}`,{cache:"force-cache"});if(!response.ok)return [] as SiteDatabaseRow[];return parseSiteDbCsv(await response.text())}catch{return [] as SiteDatabaseRow[]}})();
  SITE_DB_TABLE_CACHE.set(key,task);task.catch(()=>SITE_DB_TABLE_CACHE.delete(key));return task;
};

'''
        text=text[:helper_start]+helper+text[loader_start:]
    if "async function loadSiteDatabaseCatalogRowsUncached" not in text:
        text=text.replace("export async function loadSiteDatabaseCatalogRows(base=\"\"):Promise<SiteDatabaseRow[]> {","async function loadSiteDatabaseCatalogRowsUncached(base=\"\"):Promise<SiteDatabaseRow[]> {",1)
        text += '''\n\nconst SITE_DB_CATALOG_CACHE=new Map<string,Promise<SiteDatabaseRow[]>>();
export function loadSiteDatabaseCatalogRows(base=""):Promise<SiteDatabaseRow[]> {
  const key=base||"/";const cached=SITE_DB_CATALOG_CACHE.get(key);if(cached)return cached;
  const task=loadSiteDatabaseCatalogRowsUncached(base);SITE_DB_CATALOG_CACHE.set(key,task);task.catch(()=>SITE_DB_CATALOG_CACHE.delete(key));return task;
}\n'''
    generated.write_text(text,encoding="utf-8")
    print("Enabled browser/module caching for catalog CSV tables")

print("Finalized route split: lightweight / and catalog-only runtime at /catalog/")
