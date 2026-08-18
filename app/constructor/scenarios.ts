export const CONSTRUCTOR_SCENARIO_IDS = [
  "retro-cabinet",
  "cloud-tenderness",
  "winter-garden-breakfast",
  "blue-velvet-night",
  "fairy-tea",
] as const;

export type ConstructorScenarioId = (typeof CONSTRUCTOR_SCENARIO_IDS)[number];

export const isConstructorScenarioId = (value: string): value is ConstructorScenarioId =>
  CONSTRUCTOR_SCENARIO_IDS.includes(value as ConstructorScenarioId);
