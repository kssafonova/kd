"use client";

import type {
  CandidateRow,
  CatalogRow,
  ConstructorData,
  ExpansionPatchRow,
  ExpansionRuleRow,
  FinalConstructorData,
  FinalScenarioSummaryRow,
  FinalScenarioVariantRow,
  PresetRow,
  ScenarioMetaRow,
} from "./types";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
const XLSX_ENTITY_FILES = Array.from({length:5},(_,index)=>`kultura_doma_product_entities_xlsx_${index+1}.csv`);

export const CONSTRUCTOR_DATA_FILES = [
  "kultura-doma-constructor-presets-final.csv",
  "kultura_doma_scenario_candidates.csv",
  "kultura_doma_constructor_scenarios.csv",
  "kultura_doma_full_constructor_eligible_catalog.csv",
] as const;

export const FINAL_CONSTRUCTOR_DATA_FILES = [
  "kultura_doma_scenarios_summary.csv",
  "kultura_doma_scenarios_full_variants.csv",
  "kultura_doma_full_constructor_eligible_catalog.csv",
] as const;

export const EDITORIAL_EXPANSION_FILES = [
  "kultura_doma_scenario_expansion_rules.csv",
  "kultura_doma_scenario_expansion_patch.csv",
] as const;

export const constructorDataUrl = (fileName: string) => `${BASE_PATH}/data/${fileName}`;

// Products from these discontinued lines must not surface anywhere in the
// storefront constructor, even if an old preset or scenario still references
// their offer ids. Match the product display name rather than collection so
// unrelated products assigned to the same merchandising collection stay intact.
const REMOVED_CATALOG_NAME_TOKENS = [] as const;

const normalizeCatalogProductName = (value: string) =>
  String(value || "")
    .trim()
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/[‐‑‒–—]/g, "-")
    .replace(/\s+/g, " ");

export const isConstructorCatalogProductVisible = (productName: string) => {
  const name = normalizeCatalogProductName(productName);
  return !REMOVED_CATALOG_NAME_TOKENS.some((token) => name.includes(token));
};

const filterCatalogRows = (rows: CatalogRow[]) =>
  rows.filter((row) => isConstructorCatalogProductVisible(row.product_name));

const parseCsv = <T extends Record<string, string>>(source: string): T[] => {
  const text = source.replace(/^\uFEFF/, "");
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') { cell += '"'; index += 1; }
      else if (char === '"') quoted = false;
      else cell += char;
      continue;
    }
    if (char === '"') quoted = true;
    else if (char === ",") { row.push(cell); cell = ""; }
    else if (char === "\n") { row.push(cell.replace(/\r$/, "")); if (row.some((value) => value !== "")) rows.push(row); row = []; cell = ""; }
    else cell += char;
  }
  if (cell.length || row.length) { row.push(cell.replace(/\r$/, "")); if (row.some((value) => value !== "")) rows.push(row); }
  const [headers = [], ...body] = rows;
  return body.map((values) => {
    const result: Record<string, string> = {};
    headers.forEach((header, index) => { result[header.trim()] = values[index] ?? ""; });
    return result as T;
  });
};

const loadCsv = async <T extends Record<string, string>>(fileName: string): Promise<T[]> => {
  let response: Response;
  try { response = await fetch(constructorDataUrl(fileName), { cache: "force-cache" }); }
  catch { throw new Error("Добавьте CSV-файлы в public/data"); }
  if (!response.ok) {
    if (response.status === 404) throw new Error("Добавьте CSV-файлы в public/data");
    throw new Error(`Не удалось загрузить ${fileName}: ${response.status}`);
  }
  const rows = parseCsv<T>(await response.text());
  if (!rows.length) throw new Error(`CSV-файл ${fileName} пуст или не распознан`);
  return rows;
};

const loadCompressedXlsxEntities=async()=>{
  try{
    const response=await fetch(constructorDataUrl("kultura_doma_product_entities_xlsx_extra.b64"),{cache:"no-store"});
    if(!response.ok||typeof DecompressionStream==="undefined")return [];
    const encoded=(await response.text()).trim();
    const bytes=Uint8Array.from(atob(encoded),char=>char.charCodeAt(0));
    const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
    return parseCsv<Record<string,string>>(await new Response(stream).text());
  }catch{return []}
};
const xlsxProductType=(row:Record<string,string>)=>{
  const name=String(row["Название товара"]||"").toLocaleLowerCase("ru-RU");
  if(name.includes("тарел"))return "plate"; if(name.includes("салатник")||name.includes("супниц"))return "salad_bowl";
  if(name.includes("чайная пара"))return "tea_pair"; if(name.includes("кофейная пара"))return "coffee_pair"; if(name.includes("круж"))return "mug";
  if(name.includes("чайник"))return "teapot"; if(name.includes("молочник")||name.includes("сливочник"))return "milk_jug"; if(name.includes("сахарниц"))return "sugar_bowl";
  if(name.includes("скатерт"))return "tablecloth"; if(name.includes("плейсмат"))return "placemat"; if(name.includes("салфет"))return "napkin"; if(name.includes("дорожк"))return "table_runner";
  if(name.includes("подушка"))return "decorative_pillow"; if(name.includes("плед"))return "throw"; if(name.includes("покрывал"))return "coverlet";
  if(name.includes("постель")||name.includes("простын")||name.includes("пододеяль")||name.includes("наволоч"))return "bedding_set";
  if(name.includes("свеч"))return "candle"; if(name.includes("диффуз"))return "diffuser"; if(name.includes("ваза"))return "vase"; if(name.includes("поднос"))return "tray";
  if(name.includes("прибор")||name.includes("ложк")||name.includes("вилк"))return "cutlery"; return "other";
};
const loadXlsxCatalog = async (): Promise<CatalogRow[]> => {
  const parts=await Promise.all(XLSX_ENTITY_FILES.map(async fileName=>{
    try{const response=await fetch(constructorDataUrl(fileName),{cache:"no-store"});if(!response.ok)return [];return parseCsv<Record<string,string>>(await response.text())}catch{return []}
  }));
  const extra=await loadCompressedXlsxEntities();
  return [...parts.flat(),...extra].filter(row=>row["Артикул"]&&row["Название товара"]).map((row,index)=>{
    const images=[row["Превью фотография товара"],row["Вторая фотография товара в скролле"],row["Третья фотография в стролле"]].filter(Boolean);
    return {offer_id:`xlsx-${index+1}`,group_id:`xlsx-${row["Артикул"]}`,vendor_code:row["Артикул"]||"",collection:row["Коллекция"]||"",product_name:row["Название товара"]||"",product_url:"",product_type:xlsxProductType(row),constructor_role:"",mix_role:"",builder_domain:"",palette:"",style_tags:"",price:"0",old_price:"",color:row["Цвет"]||"",size:row["Размер"]||"",material:row["Материал"]||"",volume:row["Объем"]||"",availability_status:"available",primary_image_url:images[0]||"/images/image-placeholder.svg",all_image_urls:images.join("|")} satisfies CatalogRow;
  });
};
const mergeCatalog=(base:CatalogRow[],xlsx:CatalogRow[])=>{
  const key=(row:CatalogRow)=>[row.vendor_code,row.product_name,row.color,row.size,row.volume].map(value=>String(value||"").trim().toLocaleLowerCase("ru-RU")).join("|");
  const xkeys=new Set(xlsx.map(key));
  return [...xlsx,...base.filter(row=>!xkeys.has(key(row)))];
};

const loadOptionalCsv = async <T extends Record<string, string>>(fileName: string): Promise<T[]> => {
  try {
    const response = await fetch(constructorDataUrl(fileName), { cache: "force-cache" });
    if (!response.ok) return [];
    return parseCsv<T>(await response.text());
  } catch { return []; }
};

let constructorDataPromise: Promise<ConstructorData> | null = null;

export const loadConstructorData = () => {
  if (!constructorDataPromise) {
    constructorDataPromise = Promise.all([
      loadCsv<PresetRow>(CONSTRUCTOR_DATA_FILES[0]),
      loadCsv<CandidateRow>(CONSTRUCTOR_DATA_FILES[1]),
      loadCsv<ScenarioMetaRow>(CONSTRUCTOR_DATA_FILES[2]),
      loadCsv<CatalogRow>(CONSTRUCTOR_DATA_FILES[3]),
      loadOptionalCsv<ExpansionRuleRow>(EDITORIAL_EXPANSION_FILES[0]),
      loadOptionalCsv<ExpansionPatchRow>(EDITORIAL_EXPANSION_FILES[1]),
      loadXlsxCatalog(),
    ])
      .then(([presets, candidates, scenarios, catalog, expansionRules, expansionPatches, xlsxCatalog]) => ({
        presets,
        candidates,
        scenarios,
        catalog: filterCatalogRows(mergeCatalog(catalog,xlsxCatalog)),
        expansionRules,
        expansionPatches,
      }))
      .catch((error) => { constructorDataPromise = null; throw error; });
  }
  return constructorDataPromise;
};

let finalConstructorDataPromise: Promise<FinalConstructorData> | null = null;

export const loadFinalConstructorData = () => {
  if (!finalConstructorDataPromise) {
    finalConstructorDataPromise = Promise.all([
      loadCsv<Record<string, string>>(FINAL_CONSTRUCTOR_DATA_FILES[0]),
      loadCsv<Record<string, string>>(FINAL_CONSTRUCTOR_DATA_FILES[1]),
      loadCsv<CatalogRow>(FINAL_CONSTRUCTOR_DATA_FILES[2]),
      loadXlsxCatalog(),
    ])
      .then(([summaryRaw, variantRaw, catalog, xlsxCatalog]) => {
        const summaries: FinalScenarioSummaryRow[] = summaryRaw.map((row) => ({
          scenario_id: row.scenario_id ?? "",
          scenario_name: row.scenario_name ?? "",
          space: row.space ?? "",
          occasion: row.occasion ?? "",
          total_items: row.total_items ?? "",
          required_items: row.required_items ?? "",
          status: row.status ?? "",
        }));
        const variants: FinalScenarioVariantRow[] = variantRaw
          .map((row) => ({
            scenario_name: row["Сценарий"] ?? "",
            space: row["Пространство"] ?? "",
            occasion: row["Повод"] ?? "",
            role: row["Роль"] ?? "",
            type: row["Тип"] ?? "",
            offer_id: row.offer_id ?? "",
            product_name: row["Название товара"] ?? "",
            price_rub: row["Цена"] ?? "",
            material: row["Материал"] ?? "",
            color: row["Цвет"] ?? "",
            product_url: row.URL ?? "",
            note: row["Примечание"] ?? "",
          }))
          .filter((row) => isConstructorCatalogProductVisible(row.product_name));
        return { summaries, variants, catalog: filterCatalogRows(mergeCatalog(catalog,xlsxCatalog)) };
      })
      .catch((error) => { finalConstructorDataPromise = null; throw error; });
  }
  return finalConstructorDataPromise;
};
