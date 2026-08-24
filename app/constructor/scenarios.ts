export const LEGACY_CONSTRUCTOR_SCENARIO_IDS = [
  "retro-cabinet",
  "cloud-tenderness",
  "winter-garden-breakfast",
  "blue-velvet-night",
  "fairy-tea",
] as const;

export const TABLE_SOLUTION_IDS = [
  "table-1",
  "table-2",
  "table-3",
] as const;

export const CONSTRUCTOR_SCENARIO_IDS = [
  ...LEGACY_CONSTRUCTOR_SCENARIO_IDS,
  ...TABLE_SOLUTION_IDS,
] as const;

export type LegacyConstructorScenarioId = (typeof LEGACY_CONSTRUCTOR_SCENARIO_IDS)[number];
export type ConstructorScenarioId = (typeof CONSTRUCTOR_SCENARIO_IDS)[number];

// Kept as the legacy guard because SCENARIO_COPY contains copy only for the
// original five scenarios. New table-driven solutions use their own metadata.
export const isConstructorScenarioId = (value: string): value is LegacyConstructorScenarioId =>
  LEGACY_CONSTRUCTOR_SCENARIO_IDS.includes(value as LegacyConstructorScenarioId);

export const isRoutableConstructorScenarioId = (value: string): value is ConstructorScenarioId =>
  CONSTRUCTOR_SCENARIO_IDS.includes(value as ConstructorScenarioId);
