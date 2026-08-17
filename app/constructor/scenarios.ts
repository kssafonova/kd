export const CONSTRUCTOR_SCENARIO_IDS = [
  "red-thread-tea",
  "quiet-obereg",
  "sky-celebration",
  "green-salon",
  "blue-hour-bedroom",
] as const;

export type ConstructorScenarioId = (typeof CONSTRUCTOR_SCENARIO_IDS)[number];

export const isConstructorScenarioId = (value: string): value is ConstructorScenarioId =>
  CONSTRUCTOR_SCENARIO_IDS.includes(value as ConstructorScenarioId);
