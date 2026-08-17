"use client";

import type {
  CandidateRow,
  CatalogRow,
  ConstructorData,
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

export const constructorDataUrl = (fileName: string) => `${BASE_PATH}/data/${fileName}`;

const parseCsv = <T extends Record<string, string>>(source: string): T[] => {
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

    if (char === '"') {
      quoted = true;
    } else if (char === ",") {
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
};

const loadCsv = async <T extends Record<string, string>>(fileName: string): Promise<T[]> => {
  let response: Response;
  try {
    response = await fetch(constructorDataUrl(fileName), { cache: "force-cache" });
  } catch {
    throw new Error("Добавьте CSV-файлы в public/data");
  }

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Добавьте CSV-файлы в public/data");
    }
    throw new Error(`Не удалось загрузить ${fileName}: ${response.status}`);
  }

  const rows = parseCsv<T>(await response.text());
  if (!rows.length) {
    throw new Error(`CSV-файл ${fileName} пуст или не распознан`);
  }
  return rows;
};

let constructorDataPromise: Promise<ConstructorData> | null = null;

export const loadConstructorData = () => {
  if (!constructorDataPromise) {
    constructorDataPromise = Promise.all([
      loadCsv<PresetRow>(CONSTRUCTOR_DATA_FILES[0]),
      loadCsv<CandidateRow>(CONSTRUCTOR_DATA_FILES[1]),
      loadCsv<ScenarioMetaRow>(CONSTRUCTOR_DATA_FILES[2]),
      loadCsv<CatalogRow>(CONSTRUCTOR_DATA_FILES[3]),
    ])
      .then(([presets, candidates, scenarios, catalog]) => ({ presets, candidates, scenarios, catalog }))
      .catch((error) => {
        constructorDataPromise = null;
        throw error;
      });
  }
  return constructorDataPromise;
};
