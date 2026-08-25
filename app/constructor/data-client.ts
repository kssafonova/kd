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
const REMOVED_CATALOG_NAME_TOKENS = [
  "мокоши",
  "жар-птица",
  "жар птица",
  "жарптица",
  "овация",
] as const;

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
    ])
      .then(([presets, candidates, scenarios, catalog, expansionRules, expansionPatches]) => ({
        presets,
        candidates,
        scenarios,
        catalog: filterCatalogRows(catalog),
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
    ])
      .then(([summaryRaw, variantRaw, catalog]) => {
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
        return { summaries, variants, catalog: filterCatalogRows(catalog) };
      })
      .catch((error) => { finalConstructorDataPromise = null; throw error; });
  }
  return finalConstructorDataPromise;
};
