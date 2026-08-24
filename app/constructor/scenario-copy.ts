import type { LegacyConstructorScenarioId } from "./scenarios";

/**
 * Canonical, commercially-facing space taxonomy for the storefront —
 * independent of the raw `space` column in the scenarios CSV (which mixes
 * values like "Стол" and "Спальня / ванная" that don't read as retail
 * categories). Order matters: it's the display order of the landing
 * filter tabs. A tab only renders when at least one live scenario maps
 * to it — "Гостиная" and "Ванная" are part of the taxonomy so a future
 * scenario in either space slots in with no further code changes, but
 * neither has a live scenario yet, so neither tab shows today.
 */
export const SPACE_TAXONOMY = ["Кухня и столовая", "Спальня", "Кабинет", "Гостиная", "Ванная"] as const;
export type SpaceLabel = (typeof SPACE_TAXONOMY)[number];

export type ScenarioCopy = {
  space: SpaceLabel;
  mood: string;
  narrative: string;
};

/**
 * Short editorial framing per scenario, written from the real roles and
 * materials in kultura_doma_scenarios_full_variants.csv (not invented).
 * There is no narrative field in the data source itself, so this is
 * authored copy grounded in the actual products each scenario contains.
 */
export const SCENARIO_COPY: Record<LegacyConstructorScenarioId, ScenarioCopy> = {
  "retro-cabinet": {
    space: "Кабинет",
    mood: "Кожа, керамика цвета обожжённой глины и утро, которое не торопится.",
    narrative:
      "Стол для человека, у которого завтрак начинается с чтения, а не с телефона. Тёплая керамика «Юрма» и текстурная кожа «Текстура» держат одну гамму — от подставки под бокал до обложки ежедневника, — так рабочий уголок выглядит обжитым, а не составленным.",
  },
  "cloud-tenderness": {
    space: "Спальня",
    mood: "Белый на белом — сатин, вафельная ткань и фарфор одного дыхания.",
    narrative:
      "Сценарий для дома, где спальня продолжается в ванную без границы. Постельное бельё «Тихий сон», вафельный халат и бисквитный фарфор «Облачные фантазии» держат один и тот же мягкий белый — вещи не спорят друг с другом, а собираются в одно ровное утро.",
  },
  "winter-garden-breakfast": {
    space: "Кухня и столовая",
    mood: "Костяной фарфор, хрусталь и свет зимнего утра на белой скатерти.",
    narrative:
      "Сервировка для завтрака, который хочется продлить. Белый костяной фарфор «Камея», вышитая скатерть «Обереги» и хрустальная ваза «Росы» держат один прозрачный зимний свет — состав рассчитан на четверых и легко становится праздничным столом.",
  },
  "blue-velvet-night": {
    space: "Спальня",
    mood: "Глубокий синий, пуховый оренбургский платок и тишина позднего вечера.",
    narrative:
      "Сценарий для тех, кто заканчивает день медленно. Постельное бельё «Нити времени», пуховые носки из оренбургского платка и свеча «Поле» собраны в одну глубокую синюю палитру — от текстиля до чайной пары на прикроватном столике.",
  },
  "fairy-tea": {
    space: "Кухня и столовая",
    mood: "Фарфор с сюжетом — чаепитие, которое похоже на подарок.",
    narrative:
      "Праздничная сервировка на двоих или в подарок. Тарелка «Сказочный лес», чайная пара «Многоцвет» и фарфоровая ваза «Айсберг» держат одну повествовательную, слегка сказочную интонацию — стол, из-за которого не хочется вставать быстро.",
  },
};
