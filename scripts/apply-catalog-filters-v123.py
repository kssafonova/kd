from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "app" / "page.tsx"

MARKER = "// CATALOG_FILTERS_V123"

CATALOG_VIEW = r'''// CATALOG_FILTERS_V123
type CatalogSortV123 = "popular" | "price_asc" | "price_desc";
type CatalogMultiFilterKeyV123 = "subcategories" | "collections" | "capsules" | "materials" | "sizes" | "colors";
type CatalogFilterGroupV123 = "subcategory" | "collection" | "material" | "size" | "color" | "price";
type CatalogFiltersV123 = {
  subcategories:string[];
  collections:string[];
  capsules:string[];
  materials:string[];
  sizes:string[];
  colors:string[];
  priceFrom:string;
  priceTo:string;
};
type CatalogForcedFacetV123 = {group:CatalogFilterGroupV123;value:string;kind?:"collection"|"capsule"};

const emptyCatalogFiltersV123=():CatalogFiltersV123=>({subcategories:[],collections:[],capsules:[],materials:[],sizes:[],colors:[],priceFrom:"",priceTo:""});
const cloneCatalogFiltersV123=(filters:CatalogFiltersV123):CatalogFiltersV123=>({...filters,subcategories:[...filters.subcategories],collections:[...filters.collections],capsules:[...filters.capsules],materials:[...filters.materials],sizes:[...filters.sizes],colors:[...filters.colors]});
const facetNormV123=(value:unknown)=>String(cleanNulls(value)??"").trim().toLocaleLowerCase("ru-RU").replace(/ё/g,"е");
const sameFacetV123=(left:unknown,right:unknown)=>facetNormV123(left)===facetNormV123(right);
const hasFacetValueV123=(values:string[],value:string)=>values.some(item=>sameFacetV123(item,value));
const withoutFacetValueV123=(values:string[],value:string)=>values.filter(item=>!sameFacetV123(item,value));
const uniqueFacetValuesV123=(values:(string|undefined)[])=>Array.from(new Map(values.map(cleanNulls).filter((value):value is string=>Boolean(value)).map(value=>[facetNormV123(value),value])).values());
const catalogSkuColorV123=(sku:CatalogSku)=>cleanNulls(asVariantSku(sku)?.sourceColor)??cleanNulls(sku.color)??"";
const availableCatalogSkusV123=(product:Product)=>product.skus?.filter(sku=>sku.available!==false)??[];
const parseCatalogBoundV123=(value:string)=>{const text=String(value??"").trim();if(!text)return undefined;const parsed=Number(text.replace(/\s/g,""));return Number.isFinite(parsed)&&parsed>=0?parsed:undefined};
const catalogNumberV123=(value:number)=>new Intl.NumberFormat("ru-RU").format(Math.round(value));

function toggleCatalogFilterValueV123(filters:CatalogFiltersV123,key:CatalogMultiFilterKeyV123,value:string):CatalogFiltersV123{
  const current=filters[key];
  return {...filters,[key]:hasFacetValueV123(current,value)?withoutFacetValueV123(current,value):[...current,value]};
}

function skuMatchesCatalogFiltersV123(sku:CatalogSku,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const material=cleanNulls(sku.material)??"";
  const size=cleanNulls(sku.size)??"";
  const color=catalogSkuColorV123(sku);
  const price=Number(sku.price)||0;
  if(ignore!=="material"&&filters.materials.length&&!filters.materials.some(value=>sameFacetV123(value,material)))return false;
  if(ignore!=="size"&&filters.sizes.length&&!filters.sizes.some(value=>sameFacetV123(value,size)))return false;
  if(ignore!=="color"&&filters.colors.length&&!filters.colors.some(value=>sameFacetV123(value,color)))return false;
  if(ignore!=="price"){
    const from=parseCatalogBoundV123(filters.priceFrom),to=parseCatalogBoundV123(filters.priceTo);
    if(from!==undefined&&price<from)return false;
    if(to!==undefined&&price>to)return false;
  }
  if(forced?.group==="material"&&!sameFacetV123(material,forced.value))return false;
  if(forced?.group==="size"&&!sameFacetV123(size,forced.value))return false;
  if(forced?.group==="color"&&!sameFacetV123(color,forced.value))return false;
  return true;
}

function catalogMatchingSkusV123(product:Product,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const skus=availableCatalogSkusV123(product);
  if(skus.length)return skus.filter(sku=>skuMatchesCatalogFiltersV123(sku,filters,ignore,forced));
  if(forced&&["material","size","color"].includes(forced.group))return [];
  if(ignore!=="price"){
    const from=parseCatalogBoundV123(filters.priceFrom),to=parseCatalogBoundV123(filters.priceTo),price=Number(product.price)||0;
    if(from!==undefined&&price<from)return [];
    if(to!==undefined&&price>to)return [];
  }
  if((ignore!=="material"&&filters.materials.length)||(ignore!=="size"&&filters.sizes.length)||(ignore!=="color"&&filters.colors.length))return [];
  return [null] as (CatalogSku|null)[];
}

function matchesCatalogProductV123(product:Product,filters:CatalogFiltersV123,ignore?:CatalogFilterGroupV123,forced?:CatalogForcedFacetV123){
  const subcategory=cleanNulls(product.subcategory)??"";
  const collection=cleanNulls(product.collection)??"";
  const capsule=cleanNulls(product.capsule)??"";
  if(ignore!=="subcategory"&&filters.subcategories.length&&!filters.subcategories.some(value=>sameFacetV123(value,subcategory)))return false;
  if(forced?.group==="subcategory"&&!sameFacetV123(subcategory,forced.value))return false;
  if(ignore!=="collection"&&(filters.collections.length||filters.capsules.length)){
    const collectionMatch=filters.collections.some(value=>sameFacetV123(value,collection));
    const capsuleMatch=filters.capsules.some(value=>sameFacetV123(value,capsule));
    if(!collectionMatch&&!capsuleMatch)return false;
  }
  if(forced?.group==="collection"){
    if(forced.kind==="capsule"&&!sameFacetV123(capsule,forced.value))return false;
    if(forced.kind!=="capsule"&&!sameFacetV123(collection,forced.value))return false;
  }
  return catalogMatchingSkusV123(product,filters,ignore,forced).length>0;
}

function catalogFilterDisplayProductV123(product:Product,filters:CatalogFiltersV123){
  const hasSkuFilter=filters.materials.length||filters.sizes.length||filters.colors.length||filters.priceFrom||filters.priceTo;
  if(!hasSkuFilter)return product;
  const matchingSkus=catalogMatchingSkusV123(product,filters).filter((sku):sku is CatalogSku=>Boolean(sku));
  const sku=matchingSkus[0];
  if(!sku)return product;
  const primary=isAromaProduct(product)?sku.color:catalogSkuColorV123(sku);
  return {...product,image:sku.image,gallery:sku.gallery,selectedColor:primary||product.selectedColor,selectedSize:filters.sizes.length?sku.size:product.selectedSize,selectedSkuId:sku.id,...({catalogFilterSkuIds:matchingSkus.map(item=>item.id)} as any)};
}

function catalogSortPriceV123(product:Product,filters:CatalogFiltersV123){
  const prices=catalogMatchingSkusV123(product,filters).map(sku=>sku?Number(sku.price)||0:Number(product.price)||0).filter(price=>priceKnown(price));
  return prices.length?Math.min(...prices):(Number(product.price)||0);
}

function CatalogFilterOptionV123({label,count,checked,disabled,onChange,swatch,kind}:{label:string;count:number;checked:boolean;disabled:boolean;onChange:()=>void;swatch?:string;kind?:string}){
  return <label className={`catalog-filter-option-v123 ${disabled?"is-disabled":""}`}><input type="checkbox" checked={checked} disabled={disabled&&!checked} onChange={onChange}/>{swatch&&<span className="catalog-filter-swatch-v123" style={{background:swatch}} aria-hidden="true"/>}<span className="catalog-filter-option-label-v123">{label}{kind&&<small>{kind}</small>}</span><span className="catalog-filter-count-v123">{count}</span></label>;
}

function CatalogView({ initialCategory, onFilter:_onFilter, onAdd, onProduct, favorite, favorites }: { initialCategory:string; onFilter:()=>void; onAdd:(p:Product)=>void; onProduct:(p:Product)=>void; favorite:(n:number)=>void; favorites:number[] }) {
  const [sort,setSort]=useState<CatalogSortV123>("popular");
  const [filterOpen,setFilterOpen]=useState(false);
  const [applied,setApplied]=useState<CatalogFiltersV123>(()=>emptyCatalogFiltersV123());
  const [draft,setDraft]=useState<CatalogFiltersV123>(()=>emptyCatalogFiltersV123());
  const categoryNames=Array.from(new Set(products.map(product=>cleanNulls(product.category)).filter((value):value is string=>Boolean(value))));
  const categoryKey=categoryNames.join("|");
  const resolveCategory=(value:string)=>categoryNames.find(name=>sameFacetV123(name,value))??"Все товары";
  const [category,setCategory]=useState(()=>resolveCategory(initialCategory));
  const popularityIndex=new Map(products.map((product,index)=>[product.id,index]));

  const parseFiltersFromUrl=()=>{
    const params=new URLSearchParams(window.location.search);
    const list=(key:string)=>params.getAll(key).flatMap(value=>value.split(",")).map(value=>value.trim()).filter(Boolean);
    const filters:CatalogFiltersV123={subcategories:list("subcategory"),collections:list("collection"),capsules:list("capsule"),materials:list("material"),sizes:list("size"),colors:list("color"),priceFrom:params.get("price_from")??"",priceTo:params.get("price_to")??""};
    const rawSort=params.get("sort");
    const nextSort:CatalogSortV123=rawSort==="price_asc"||rawSort==="price_desc"?rawSort:"popular";
    const nextCategory=resolveCategory(params.get("category")||initialCategory);
    return {filters,nextSort,nextCategory};
  };

  const writeCatalogUrl=(filters:CatalogFiltersV123,nextSort:CatalogSortV123,nextCategory:string,mode:"push"|"replace"="push")=>{
    if(typeof window==="undefined")return;
    const params=new URLSearchParams();
    params.set("category",nextCategory);
    params.set("sort",nextSort);
    filters.subcategories.forEach(value=>params.append("subcategory",value));
    filters.collections.forEach(value=>params.append("collection",value));
    filters.capsules.forEach(value=>params.append("capsule",value));
    filters.materials.forEach(value=>params.append("material",value));
    filters.sizes.forEach(value=>params.append("size",value));
    filters.colors.forEach(value=>params.append("color",value));
    if(filters.priceFrom)params.set("price_from",filters.priceFrom);
    if(filters.priceTo)params.set("price_to",filters.priceTo);
    const next=`${window.location.pathname}?${params.toString()}`;
    window.history[mode==="push"?"pushState":"replaceState"]({},"",next);
  };

  useEffect(()=>{
    if(typeof window==="undefined")return;
    const restore=()=>{const state=parseFiltersFromUrl();setCategory(state.nextCategory);setSort(state.nextSort);setApplied(state.filters);setDraft(cloneCatalogFiltersV123(state.filters));setFilterOpen(false)};
    restore();
    window.addEventListener("popstate",restore);
    return()=>window.removeEventListener("popstate",restore);
  },[initialCategory,categoryKey]);

  useEffect(()=>{
    if(!filterOpen||typeof document==="undefined")return;
    const previous=document.body.style.overflow;
    document.body.style.overflow="hidden";
    const onKey=(event:KeyboardEvent)=>{if(event.key==="Escape")setFilterOpen(false)};
    window.addEventListener("keydown",onKey);
    return()=>{document.body.style.overflow=previous;window.removeEventListener("keydown",onKey)};
  },[filterOpen]);

  const baseProducts=products.filter(product=>category==="Все товары"||sameFacetV123(product.category,category));
  const subcategoryOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.subcategory));
  const collectionOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.collection));
  const capsuleOptions=uniqueFacetValuesV123(baseProducts.map(product=>product.capsule));
  const skus=baseProducts.flatMap(product=>availableCatalogSkusV123(product));
  const materialOptions=uniqueFacetValuesV123(skus.map(sku=>sku.material));
  const sizeOptions=uniqueFacetValuesV123(skus.map(sku=>sku.size));
  const colorOptions=uniqueFacetValuesV123(skus.map(sku=>catalogSkuColorV123(sku)));
  const colorHexes=new Map<string,string>();
  skus.forEach(sku=>{const color=catalogSkuColorV123(sku);if(color&&!colorHexes.has(facetNormV123(color)))colorHexes.set(facetNormV123(color),sku.colorHex||"#e8e5df")});
  const allPrices=skus.map(sku=>Number(sku.price)||0).filter(price=>priceKnown(price));
  if(!allPrices.length)baseProducts.forEach(product=>{if(priceKnown(product.price))allPrices.push(product.price)});
  const minCatalogPrice=allPrices.length?Math.floor(Math.min(...allPrices)):0;
  const maxCatalogPrice=allPrices.length?Math.ceil(Math.max(...allPrices)):0;
  const facetCount=(group:CatalogFilterGroupV123,value:string,kind?:"collection"|"capsule")=>baseProducts.filter(product=>matchesCatalogProductV123(product,draft,group,{group,value,kind})).length;
  const draftCount=baseProducts.filter(product=>matchesCatalogProductV123(product,draft)).length;

  const filteredProducts=baseProducts.filter(product=>matchesCatalogProductV123(product,applied)).map(product=>catalogFilterDisplayProductV123(product,applied));
  const list=[...filteredProducts].sort((left,right)=>{
    if(sort==="price_asc")return catalogSortPriceV123(left,applied)-catalogSortPriceV123(right,applied);
    if(sort==="price_desc")return catalogSortPriceV123(right,applied)-catalogSortPriceV123(left,applied);
    return (popularityIndex.get(left.id)??Number.MAX_SAFE_INTEGER)-(popularityIndex.get(right.id)??Number.MAX_SAFE_INTEGER);
  });

  const openFilters=()=>{setDraft(cloneCatalogFiltersV123(applied));setFilterOpen(true)};
  const changeDraft=(key:CatalogMultiFilterKeyV123,value:string)=>setDraft(current=>toggleCatalogFilterValueV123(current,key,value));
  const applyDraft=()=>{const next=cloneCatalogFiltersV123(draft);setApplied(next);setFilterOpen(false);writeCatalogUrl(next,sort,category,"push")};
  const resetDraft=()=>setDraft(emptyCatalogFiltersV123());
  const resetAll=()=>{const next=emptyCatalogFiltersV123();setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const changeCategory=(name:string)=>{const next=emptyCatalogFiltersV123();setCategory(name);setApplied(next);setDraft(cloneCatalogFiltersV123(next));setFilterOpen(false);writeCatalogUrl(next,sort,name,"push")};
  const changeSort=(next:CatalogSortV123)=>{setSort(next);writeCatalogUrl(applied,next,category,"push")};
  const removeAppliedValue=(key:CatalogMultiFilterKeyV123,value:string)=>{const next={...applied,[key]:withoutFacetValueV123(applied[key],value)} as CatalogFiltersV123;setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const removePrice=()=>{const next={...applied,priceFrom:"",priceTo:""};setApplied(next);setDraft(cloneCatalogFiltersV123(next));writeCatalogUrl(next,sort,category,"push")};
  const activeCount=applied.subcategories.length+applied.collections.length+applied.capsules.length+applied.materials.length+applied.sizes.length+applied.colors.length+(applied.priceFrom||applied.priceTo?1:0);
  const priceChip=applied.priceFrom&&applied.priceTo?`${catalogNumberV123(Number(applied.priceFrom))}–${catalogNumberV123(Number(applied.priceTo))} ₽`:applied.priceFrom?`от ${catalogNumberV123(Number(applied.priceFrom))} ₽`:applied.priceTo?`до ${catalogNumberV123(Number(applied.priceTo))} ₽`:"";
  const renderChip=(key:CatalogMultiFilterKeyV123,value:string)=><button key={`${key}-${value}`} className="catalog-filter-chip-v123" onClick={()=>removeAppliedValue(key,value)}>{value}<span>×</span></button>;

  return <div className="catalog page catalog-v123">
    <div className="crumbs">Главная / Каталог / {category}</div>
    <div className="title-line"><h1>{category}</h1><span>{productCountLabel(list.length)}</span></div>
    <div className="tabs">{["Все товары",...categoryNames].map(name=><button key={name} className={category===name?"active":""} onClick={()=>changeCategory(name)}>{name}</button>)}</div>
    <div className="catalog-tools catalog-tools-v123">
      <label className="catalog-sort-v123"><span>Сортировка</span><select value={sort} onChange={event=>changeSort(event.target.value as CatalogSortV123)} aria-label="Сортировка товаров"><option value="popular">По популярности</option><option value="price_asc">Сначала дешевле</option><option value="price_desc">Сначала дороже</option></select></label>
      <button className="catalog-filter-trigger-v123" type="button" onClick={openFilters}><Icon name="filter"/><span>Фильтры</span>{activeCount>0&&<b>{activeCount}</b>}</button>
    </div>
    {activeCount>0&&<div className="catalog-active-filters-v123" aria-label="Выбранные фильтры">{applied.subcategories.map(value=>renderChip("subcategories",value))}{applied.collections.map(value=>renderChip("collections",value))}{applied.capsules.map(value=>renderChip("capsules",value))}{applied.materials.map(value=>renderChip("materials",value))}{applied.sizes.map(value=>renderChip("sizes",value))}{applied.colors.map(value=>renderChip("colors",value))}{priceChip&&<button className="catalog-filter-chip-v123" onClick={removePrice}>{priceChip}<span>×</span></button>}<button className="catalog-filter-reset-all-v123" onClick={resetAll}>Сбросить все</button></div>}
    {list.length?<div className="product-grid">{list.map(product=><ProductCard key={`${category}-${product.id}-${product.selectedSkuId??product.selectedColor??"default"}`} product={product} onClick={onProduct} onQuick={onAdd} favorite={favorite} liked={favorites.includes(product.id)}/>)}</div>:<div className="catalog-empty catalog-empty-v123"><p>По выбранным параметрам товаров не найдено</p><button type="button" onClick={resetAll}>Сбросить фильтры</button></div>}
    {filterOpen&&<div className="catalog-filter-layer-v123" role="presentation" onMouseDown={event=>{if(event.target===event.currentTarget)setFilterOpen(false)}}>
      <aside className="catalog-filter-drawer-v123" role="dialog" aria-modal="true" aria-label="Фильтры каталога">
        <header className="catalog-filter-header-v123"><div><h2>Фильтры</h2><span>{productCountLabel(draftCount)}</span></div><button type="button" onClick={()=>setFilterOpen(false)} aria-label="Закрыть фильтры"><Icon name="close"/></button></header>
        <div className="catalog-filter-body-v123">
          {subcategoryOptions.length>0&&<section className="catalog-filter-section-v123"><h3>Тип товара</h3><div className="catalog-filter-options-v123">{subcategoryOptions.map(value=>{const count=facetCount("subcategory",value),checked=hasFacetValueV123(draft.subcategories,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("subcategories",value)}/>})}</div></section>}
          {(collectionOptions.length>0||capsuleOptions.length>0)&&<section className="catalog-filter-section-v123"><h3>Коллекция / капсула</h3><div className="catalog-filter-options-v123">{collectionOptions.map(value=>{const count=facetCount("collection",value,"collection"),checked=hasFacetValueV123(draft.collections,value);return <CatalogFilterOptionV123 key={`collection-${value}`} label={value} kind="Коллекция" count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("collections",value)}/>})}{capsuleOptions.map(value=>{const count=facetCount("collection",value,"capsule"),checked=hasFacetValueV123(draft.capsules,value);return <CatalogFilterOptionV123 key={`capsule-${value}`} label={value} kind="Капсула" count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("capsules",value)}/>})}</div></section>}
          {materialOptions.length>0&&<section className="catalog-filter-section-v123"><h3>Материал</h3><div className="catalog-filter-options-v123">{materialOptions.map(value=>{const count=facetCount("material",value),checked=hasFacetValueV123(draft.materials,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("materials",value)}/>})}</div></section>}
          {sizeOptions.length>0&&<section className="catalog-filter-section-v123"><h3>Размер</h3><div className="catalog-filter-options-v123">{sizeOptions.map(value=>{const count=facetCount("size",value),checked=hasFacetValueV123(draft.sizes,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} onChange={()=>changeDraft("sizes",value)}/>})}</div></section>}
          {colorOptions.length>0&&<section className="catalog-filter-section-v123"><h3>Цвет</h3><div className="catalog-filter-options-v123 catalog-filter-colors-v123">{colorOptions.map(value=>{const count=facetCount("color",value),checked=hasFacetValueV123(draft.colors,value);return <CatalogFilterOptionV123 key={value} label={value} count={count} checked={checked} disabled={count===0} swatch={colorHexes.get(facetNormV123(value))??"#e8e5df"} onChange={()=>changeDraft("colors",value)}/>})}</div></section>}
          {(minCatalogPrice>0||maxCatalogPrice>0)&&<section className="catalog-filter-section-v123"><h3>Цена</h3><div className="catalog-filter-price-v123"><label><span>От</span><div><input type="number" inputMode="numeric" min={0} placeholder={minCatalogPrice?catalogNumberV123(minCatalogPrice):"0"} value={draft.priceFrom} onChange={event=>setDraft(current=>({...current,priceFrom:event.target.value}))}/><b>₽</b></div></label><span className="catalog-filter-price-dash-v123">—</span><label><span>До</span><div><input type="number" inputMode="numeric" min={0} placeholder={maxCatalogPrice?catalogNumberV123(maxCatalogPrice):""} value={draft.priceTo} onChange={event=>setDraft(current=>({...current,priceTo:event.target.value}))}/><b>₽</b></div></label></div></section>}
        </div>
        <footer className="catalog-filter-footer-v123"><button className="catalog-filter-reset-v123" type="button" onClick={resetDraft}>Сбросить</button><button className="catalog-filter-apply-v123" type="button" onClick={applyDraft}>Показать {productCountLabel(draftCount)}</button></footer>
      </aside>
    </div>}
  </div>;
}

'''

page = PAGE.read_text(encoding="utf-8")
changed = False

if MARKER not in page:
    start = page.find("function CatalogView(")
    end = page.find("function ProductCard(", start)
    if start < 0 or end < 0:
        raise SystemExit("CATALOG_FILTERS_V123: CatalogView/ProductCard boundary not found")
    page = page[:start] + CATALOG_VIEW + page[end:]
    changed = True

variant_old = '''  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];\n  const [colorIndex, setColorIndex] = useState(0);\n  const chosen = variants[colorIndex];'''
variant_new = '''  const variants = product.colorVariants ?? [{ name: "Молочный", hex: "#eee", image: product.image, position: product.position }];\n  // CATALOG_FILTER_VARIANT_V123: start the card on the SKU/variant selected by catalog filters.\n  const initialColorIndex=Math.max(0,variants.findIndex(variant=>variant.name===product.selectedColor));\n  const [colorIndex, setColorIndex] = useState(initialColorIndex);\n  useEffect(()=>{const next=variants.findIndex(variant=>variant.name===product.selectedColor);if(next>=0)setColorIndex(next)},[product.selectedColor,variants.map(variant=>variant.name).join("|")]);\n  const chosen = variants[colorIndex]??variants[0];'''
if "CATALOG_FILTER_VARIANT_V123" not in page:
    if variant_old not in page:
        raise SystemExit("CATALOG_FILTERS_V123: ProductCard variant initializer not found")
    page = page.replace(variant_old, variant_new, 1)
    changed = True

sku_old = '''  const primarySkus=(product.skus??[]).filter(item=>skuPrimaryMatches(product,item,chosen.name));\n  const cardSkus=primarySkus.length?primarySkus:(product.skus??[]);'''
sku_new = '''  const allPrimarySkus=(product.skus??[]).filter(item=>skuPrimaryMatches(product,item,chosen.name));\n  const catalogFilterSkuIds=((product as Product&{catalogFilterSkuIds?:string[]}).catalogFilterSkuIds??[]);\n  const eligibleSkuSet=catalogFilterSkuIds.length?new Set(catalogFilterSkuIds):undefined;\n  const primarySkus=eligibleSkuSet?allPrimarySkus.filter(item=>eligibleSkuSet.has(item.id)):allPrimarySkus;\n  const eligibleSkus=eligibleSkuSet?(product.skus??[]).filter(item=>eligibleSkuSet.has(item.id)):(product.skus??[]);\n  const cardSkus=primarySkus.length?primarySkus:eligibleSkus.length?eligibleSkus:allPrimarySkus;'''
if "catalogFilterSkuIds=((product" not in page:
    if sku_old not in page:
        raise SystemExit("CATALOG_FILTERS_V123: ProductCard SKU pricing block not found")
    page = page.replace(sku_old, sku_new, 1)
    changed = True

if changed:
    PAGE.write_text(page, encoding="utf-8")

print(f"CATALOG_FILTERS_V123: dynamic filters, sorting, URL state and variant-aware PLP applied; page_changed={changed}")
