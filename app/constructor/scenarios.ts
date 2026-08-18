export const CONSTRUCTOR_SCENARIO_IDS = [
  "winter-garden-breakfast",
  "earth-breath",
  "northern-dreams-bedroom",
  "fairy-tea",
  "botanical-garden",
  "retro-cabinet",
  "blue-velvet-night",
  "cloud-tenderness",
  "mokoshi-morning",
  "kokoshnik-gift",
  "forest-fairytale-obereg",
] as const;

export type ConstructorScenarioId = (typeof CONSTRUCTOR_SCENARIO_IDS)[number];

export const isConstructorScenarioId = (value: string): value is ConstructorScenarioId =>
  CONSTRUCTOR_SCENARIO_IDS.includes(value as ConstructorScenarioId);
