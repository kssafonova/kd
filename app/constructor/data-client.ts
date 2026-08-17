"use client";

import type {
  CandidateRow,
  CatalogRow,
  ConstructorData,
  PresetRow,
  ScenarioMetaRow,
} from "./types";

const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

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
  const response = await fetch(constructorDataUrl(fileName), { cache: "force-cache" });
  if (!response.ok) {
    throw new Error(`Не удалось загрузить ${fileName}: ${response.status}`);
  }
  return parseCsv<T>(await response.text());
};

let constructorDataPromise: Promise<ConstructorData> | null = null;

export const loadConstructorData = () => {
  if (!constructorDataPromise) {
    constructorDataPromise = Promise.all([
      loadCsv<PresetRow>("kultura-doma-constructor-presets-final.csv"),
      loadCsv<CandidateRow>("kultura_doma_scenario_candidates.csv"),
      loadCsv<ScenarioMetaRow>("kultura_doma_constructor_scenarios.csv"),
      loadCsv<CatalogRow>("kultura_doma_full_constructor_eligible_catalog.csv"),
    ]).then(([presets, candidates, scenarios, catalog]) => ({
      presets,
      candidates,
      scenarios,
      catalog,
    }));
  }
  return constructorDataPromise;
};
