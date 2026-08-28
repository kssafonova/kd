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
] as const;

export const FINAL_CONSTRUCTOR_DATA_FILES = [
  "kultura_doma_scenarios_summary.csv",
  "kultura_doma_scenarios_full_variants.csv",
] as const;

export const EDITORIAL_EXPANSION_FILES = [
  "kultura_doma_scenario_expansion_rules.csv",
  "kultura_doma_scenario_expansion_patch.csv",
] as const;

export const constructorDataUrl = (fileName: string) => `${BASE_PATH}/data/${fileName}`;
export const isConstructorCatalogProductVisible = (_productName: string) => true;
const filterCatalogRows = (rows: CatalogRow[]) => rows;

function parseCsv<T extends Record<string, string>>(source: string): T[] {
  const text = source.replace(/^\uFEFF/, "");
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        cell += char;
      }
      continue;
    }

    if (char === '"') quoted = true;
    else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell.replace(/\r$/, ""));
      if (row.some((value) => value !== "")) rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }

  if (cell.length || row.length) {
    row.push(cell.replace(/\r$/, ""));
    if (row.some((value) => value !== "")) rows.push(row);
  }

  const [headers = [], ...body] = rows;
  return body.map((values) => {
    const result: Record<string, string> = {};
    headers.forEach((header, index) => {
      result[header.trim()] = values[index] ?? "";
    });
    return result as T;
  });
}

async function loadCsv<T extends Record<string, string>>(fileName: string): Promise<T[]> {
  let response: Response;
  try {
    response = await fetch(constructorDataUrl(fileName), { cache: "no-store" });
  } catch {
    throw new Error(`Не удалось загрузить ${fileName}`);
  }
  if (!response.ok) throw new Error(`Не удалось загрузить ${fileName}: ${response.status}`);
  const rows = parseCsv<T>(await response.text());
  if (!rows.length) throw new Error(`CSV-файл ${fileName} пуст или не распознан`);
  return rows;
}

async function loadOptionalCsv<T extends Record<string, string>>(fileName: string): Promise<T[]> {
  try {
    const response = await fetch(constructorDataUrl(fileName), { cache: "force-cache" });
    if (!response.ok) return [];
    return parseCsv<T>(await response.text());
  } catch {
    return [];
  }
}

const norm = (value: string) =>
  String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е");

const truthImage = (value?: string) => {
  const source = String(value || "").trim();
  if (!source || source.toLowerCase() === "null") return "";
  if (/^https?:\/\//i.test(source)) return source;
  if (source.startsWith("/kd/")) return source.slice(3);
  if (source.startsWith("/")) return source;
  return `/images/imported-products/${source}`;
};

const xlsxProductType = (row: Record<string, string>) => {
  const name = norm(row["Название товара"]);
  const category = norm(row["Категория"]);
  const subcategory = norm(row["Подкатегория"]);
  if (name.includes("тарелка глубок") || subcategory.includes("глубок")) return "deep_plate";
  if (name.includes("тарел")) return "plate";
  if (name.includes("салатник")) return "salad_bowl";
  if (name.includes("супниц")) return "tureen";
  if (name.includes("чайная пара")) return "tea_pair";
  if (name.includes("кофейная пара")) return "coffee_pair";
  if (name.includes("круж")) return "mug";
  if (name.includes("чайник")) return "teapot";
  if (name.includes("молочник") || name.includes("сливочник")) return "milk_jug";
  if (name.includes("сахарниц")) return "sugar_bowl";
  if (name.includes("скатерт")) return "tablecloth";
  if (name.includes("плейсмат")) return "placemat";
  if (name.includes("салфет")) return "napkin";
  if (name.includes("дорожк")) return "table_runner";
  if (name.includes("подушка")) return "decorative_pillow";
  if (name.includes("плед")) return "throw";
  if (name.includes("покрывал")) return "coverlet";
  if (name.includes("пододеяль")) return "duvet";
  if (name.includes("простын")) return "sheet";
  if (name.includes("наволоч")) return "pillowcase";
  if (name.includes("постель") || category.includes("постель")) return "bedding_set";
  if (name.includes("свеч")) return "candle";
  if (name.includes("диффуз")) return "diffuser";
  if (name.includes("ваза")) return "vase";
  if (name.includes("поднос")) return "tray";
  if (name.includes("корзин")) return "basket";
  if (name.includes("домино") || name.includes("шаш") || name.includes("крестики") || name.includes("игра")) return "board_game";
  if (name.includes("прибор") || name.includes("ложк") || name.includes("вилк") || name.includes("нож")) return "cutlery";
  if (name.includes("графин")) return "decanter";
  return "other";
};

const domainFor = (categoryValue: string) => {
  const category = norm(categoryValue);
  if (category.includes("посуда") || category.includes("столовый текстиль")) return "table";
  if (category.includes("постель") || category.includes("плед")) return "bedroom";
  return "decor";
};

type TruthVariant = {
  id: string;
  variantKey: string;
  offerId: string;
  article: string;
  name: string;
  color: string;
  aroma: string;
  size: string;
  price: number;
  oldPrice?: number | null;
  height: string;
  width: string;
  volume: string;
  diameter: string;
  packageInfo: string;
  material: string;
  composition: string;
  details: string;
  collection: string;
  capsule: string;
  category: string;
  subcategory: string;
  readyRequired: string[];
  readyOptional: string[];
  photos: string[];
};

type TruthProduct = {
  key: string;
  id: number;
  article: string;
  name: string;
  category: string;
  subcategory: string;
  collections: string[];
  capsules: string[];
  variants: TruthVariant[];
};

type TruthData = { products: TruthProduct[] };

async function loadTruthData(): Promise<TruthData> {
  const response = await fetch(constructorDataUrl("catalog_truth.json.gz.b64"), { cache: "no-store" });
  if (!response.ok || typeof DecompressionStream === "undefined") {
    throw new Error(`Не удалось загрузить canonical XLSX truth: ${response.status}`);
  }
  const encoded = (await response.text()).trim();
  const bytes = Uint8Array.from(atob(encoded), (char) => char.charCodeAt(0));
  const stream = new Blob([bytes]).stream().pipeThrough(new DecompressionStream("gzip"));
  return JSON.parse(await new Response(stream).text()) as TruthData;
}

async function loadTruthCatalog(): Promise<CatalogRow[]> {
  const truth = await loadTruthData();
  return truth.products.flatMap((product) =>
    product.variants.map((variant, index) => {
      const photos = variant.photos.map(truthImage).filter(Boolean);
      const relationTags = [
        ...variant.readyRequired.map((value) => `required:${value}`),
        ...variant.readyOptional.map((value) => `optional:${value}`),
        variant.capsule ? `capsule:${variant.capsule}` : "",
        variant.aroma ? `aroma:${variant.aroma}` : "",
      ]
        .filter(Boolean)
        .join("|");

      return {
        offer_id: String(variant.offerId || variant.id || `${product.id}-${index + 1}`),
        group_id: product.key,
        vendor_code: variant.article || product.article,
        collection: variant.collection || variant.capsule || product.collections[0] || product.capsules[0] || "",
        product_name: variant.name || product.name,
        product_url: "",
        product_type: xlsxProductType({
          "Название товара": variant.name || product.name,
          Категория: variant.category || product.category,
          Подкатегория: variant.subcategory || product.subcategory,
        }),
        constructor_role: variant.subcategory || variant.category || product.subcategory || product.category,
        mix_role: variant.readyOptional.length && !variant.readyRequired.length ? "optional" : "required",
        builder_domain: domainFor(variant.category || product.category),
        palette: variant.color,
        style_tags: relationTags,
        price: String(variant.price || 0),
        old_price: variant.oldPrice ? String(variant.oldPrice) : "",
        color: variant.aroma || variant.color,
        size: variant.size,
        material: variant.material,
        volume: variant.volume,
        availability_status: "available",
        primary_image_url: photos[0] || "/images/image-placeholder.svg",
        all_image_urls: photos.join("|"),
      } satisfies CatalogRow;
    }),
  );
}

let constructorDataPromise: Promise<ConstructorData> | null = null;

export const loadConstructorData = () => {
  if (!constructorDataPromise) {
    constructorDataPromise = Promise.all([
      loadCsv<PresetRow>(CONSTRUCTOR_DATA_FILES[0]),
      loadCsv<CandidateRow>(CONSTRUCTOR_DATA_FILES[1]),
      loadCsv<ScenarioMetaRow>(CONSTRUCTOR_DATA_FILES[2]),
      loadOptionalCsv<ExpansionRuleRow>(EDITORIAL_EXPANSION_FILES[0]),
      loadOptionalCsv<ExpansionPatchRow>(EDITORIAL_EXPANSION_FILES[1]),
      loadTruthCatalog(),
    ])
      .then(([presets, candidates, scenarios, expansionRules, expansionPatches, truthCatalog]) => ({
        presets,
        candidates,
        scenarios,
        catalog: filterCatalogRows(truthCatalog),
        expansionRules,
        expansionPatches,
      }))
      .catch((error) => {
        constructorDataPromise = null;
        throw error;
      });
  }
  return constructorDataPromise;
};

let finalConstructorDataPromise: Promise<FinalConstructorData> | null = null;

export const loadFinalConstructorData = () => {
  if (!finalConstructorDataPromise) {
    finalConstructorDataPromise = Promise.all([
      loadCsv<Record<string, string>>(FINAL_CONSTRUCTOR_DATA_FILES[0]),
      loadCsv<Record<string, string>>(FINAL_CONSTRUCTOR_DATA_FILES[1]),
      loadTruthCatalog(),
    ])
      .then(([summaryRaw, variantRaw, truthCatalog]) => {
        const summaries: FinalScenarioSummaryRow[] = summaryRaw.map((row) => ({
          scenario_id: row.scenario_id ?? "",
          scenario_name: row.scenario_name ?? "",
          space: row.space ?? "",
          occasion: row.occasion ?? "",
          total_items: row.total_items ?? "",
          required_items: row.required_items ?? "",
          status: row.status ?? "",
        }));
        const variants: FinalScenarioVariantRow[] = variantRaw.map((row) => ({
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
        }));
        return { summaries, variants, catalog: filterCatalogRows(truthCatalog) };
      })
      .catch((error) => {
        finalConstructorDataPromise = null;
        throw error;
      });
  }
  return finalConstructorDataPromise;
};
