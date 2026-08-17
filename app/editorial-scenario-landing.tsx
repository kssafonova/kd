"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { assetUrl } from "./assets";
import { RemoteImage } from "./remote-image";
import { loadConstructorData } from "./constructor/data-client";
import { EDITORIAL_SCENARIOS } from "./editorial-scenario-config";
import type { ConstructorData, ScenarioMetaRow } from "./constructor/types";
import styles from "./editorial-scenarios.module.css";

type CollectionCard = {
  id: string;
  name: string;
  kind: string;
  description: string;
  images: string[];
};

type TabId = "collections" | "space" | "events";

type ScenarioCardData = {
  id: string;
  name: string;
  lead: string;
  spaceLabel: string;
  occasions: string[];
  images: string[];
  hasPreset: boolean;
};

const EVENT_LABELS: Record<string, string> = {
  tea: "Чаепитие",
  breakfast: "Завтрак",
  lunch: "Обед",
  dinner: "Ужин",
  celebration: "Праздник",
  gift: "Подарок",
  bedroom: "Ритуалы спальни",
};

const EVENT_ORDER = ["tea", "breakfast", "lunch", "dinner", "celebration", "gift", "bedroom"];

const unique = <T,>(values: T[]) => Array.from(new Set(values));

function scenarioImages(data: ConstructorData, scenarioId: string, metaRows: ScenarioMetaRow[]) {
  const presetImages = data.presets
    .filter((row) => row.scenario_id === scenarioId)
    .map((row) => row.primary_image_url)
    .filter(Boolean);

  if (presetImages.length) return unique(presetImages).slice(0, 3);

  const candidateImages = data.candidates
    .filter((row) => row.scenario_id === scenarioId)
    .map((row) => row.primary_image_url)
    .filter(Boolean);

  if (candidateImages.length) return unique(candidateImages).slice(0, 3);

  const collectionNames = unique(
    metaRows.flatMap((row) => `${row.entry_collection}|${row.allowed_collections}`.split("|")).map((value) => value.trim()).filter(Boolean),
  );
  const catalogImages = data.catalog
    .filter((row) => collectionNames.includes(row.collection))
    .map((row) => row.primary_image_url)
    .filter(Boolean);

  return unique(catalogImages).slice(0, 3);
}

function ScenarioCard({ scenario }: { scenario: ScenarioCardData }) {
  return (
    <article className={styles.scenarioCard}>
      <div className={styles.scenarioMedia}>
        {scenario.images.length ? (
          scenario.images.map((image, index) => (
            <RemoteImage key={`${scenario.id}-${image}-${index}`} src={image} alt={`${scenario.name}, предмет ${index + 1}`} loading={index === 0 ? "eager" : "lazy"} />
          ))
        ) : (
          <div className={styles.scenarioFallback}>РЕАЛЬНЫЕ ФОТО БУДУТ ЗАГРУЖЕНЫ ИЗ CSV</div>
        )}
      </div>
      <div className={styles.scenarioCopy}>
        <small>{scenario.spaceLabel}</small>
        <h2>{scenario.name}</h2>
        <p className={styles.scenarioLead}>{scenario.lead}</p>
        <div className={styles.scenarioMeta}>
          {scenario.occasions.slice(0, 3).map((occasion) => <span key={occasion}>{EVENT_LABELS[occasion] || occasion}</span>)}
        </div>
        <div className={styles.scenarioFooter}>
          <span className={styles.scenarioStatus}>{scenario.hasPreset ? "ГОТОВЫЙ PRESET · МОЖНО НАСТРОИТЬ" : "EDITORIAL · PRESET ЕЩЁ НЕ ЗАФИКСИРОВАН"}</span>
          <Link className={styles.scenarioCta} href={`/editorial/scenario/${scenario.id}/`}>Собери свою капсулу</Link>
        </div>
      </div>
    </article>
  );
}

export function EditorialScenarioLanding({
  collections,
  openCollection,
}: {
  collections: CollectionCard[];
  openCollection: (collection: CollectionCard) => void;
}) {
  const [tab, setTab] = useState<TabId>("collections");
  const [data, setData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    loadConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить сценарии"));
    return () => {
      active = false;
    };
  }, []);

  const scenarios = useMemo<ScenarioCardData[]>(() => {
    if (!data) return [];
    return EDITORIAL_SCENARIOS.map((config) => {
      const metaRows = data.scenarios.filter((row) => row.scenario_id === config.id);
      return {
        id: config.id,
        name: config.name,
        lead: config.lead,
        spaceLabel: config.spaceLabel,
        occasions: unique(metaRows.flatMap((row) => row.occasion.split("|")).map((value) => value.trim()).filter(Boolean)),
        images: scenarioImages(data, config.id, metaRows),
        hasPreset: data.presets.some((row) => row.scenario_id === config.id),
      };
    });
  }, [data]);

  const tableScenarios = scenarios.filter((item) => EDITORIAL_SCENARIOS.find((config) => config.id === item.id)?.spaceGroup === "table");
  const bedroomScenarios = scenarios.filter((item) => EDITORIAL_SCENARIOS.find((config) => config.id === item.id)?.spaceGroup === "bedroom");

  return (
    <div className={styles.shell}>
      <div className={styles.wrap}>
        <header className={styles.head}>
          <div>
            <p className={styles.eyebrow}>EDITORIAL</p>
            <h1 className={styles.title}>Истории для дома</h1>
          </div>
          <p className={styles.lead}>Коллекции задают настроение. Сценарии помогают перейти от вдохновения к готовому решению для конкретного пространства и повода.</p>
        </header>

        <div className={styles.tabs} role="tablist" aria-label="Editorial navigation">
          {([
            ["collections", "Все коллекции"],
            ["space", "По пространству"],
            ["events", "По событиям"],
          ] as const).map(([id, label]) => (
            <button key={id} type="button" role="tab" aria-selected={tab === id} className={`${styles.tab} ${tab === id ? styles.tabActive : ""}`} onClick={() => setTab(id)}>
              {label}
            </button>
          ))}
        </div>

        {tab === "collections" && (
          <div className={styles.collectionGrid}>
            {collections.map((item) => (
              <button key={item.id} type="button" className={styles.collectionCard} onClick={() => openCollection(item)}>
                <RemoteImage src={assetUrl(item.images[1] || item.images[0] || "")} alt={item.name} loading="lazy" />
                <span className={styles.collectionShade} />
                <span className={styles.collectionCopy}>
                  <small>{item.kind}</small>
                  <h2>{item.name}</h2>
                  <p>{item.description}</p>
                  <span>Смотреть историю →</span>
                </span>
              </button>
            ))}
          </div>
        )}

        {tab !== "collections" && error && (
          <div className={styles.eventIntro}>
            <h2>Не удалось загрузить сценарии</h2>
            <p>{error}</p>
          </div>
        )}

        {tab !== "collections" && !data && !error && (
          <div className={styles.eventIntro}><h2>Загружаем сценарии…</h2></div>
        )}

        {tab === "space" && data && (
          <>
            <section className={styles.group}>
              <header className={styles.groupHead}>
                <h2>Накрыть стол</h2>
                <span>Чаепитие, завтрак, семейный обед, праздничный стол и вечерняя сервировка.</span>
              </header>
              <div className={styles.scenarioGrid}>{tableScenarios.map((scenario) => <ScenarioCard key={scenario.id} scenario={scenario} />)}</div>
            </section>
            <section className={styles.group}>
              <header className={styles.groupHead}>
                <h2>Оформить спальню</h2>
                <span>Готовые текстильные истории для медленного утра и спокойного вечера.</span>
              </header>
              <div className={styles.scenarioGrid}>{bedroomScenarios.map((scenario) => <ScenarioCard key={scenario.id} scenario={scenario} />)}</div>
            </section>
          </>
        )}

        {tab === "events" && data && (
          <>
            <div className={styles.eventIntro}>
              <h2>Выберите повод</h2>
              <p>Один сценарий может появляться в нескольких поводах — это намеренно: пользователь выбирает не структуру каталога, а ситуацию, для которой оформляет дом.</p>
            </div>
            {EVENT_ORDER.map((eventId) => {
              const items = scenarios.filter((scenario) => scenario.occasions.includes(eventId));
              if (!items.length) return null;
              return (
                <section className={styles.group} key={eventId}>
                  <header className={styles.groupHead}><h2>{EVENT_LABELS[eventId]}</h2></header>
                  <div className={styles.scenarioGrid}>{items.map((scenario) => <ScenarioCard key={`${eventId}-${scenario.id}`} scenario={scenario} />)}</div>
                </section>
              );
            })}
          </>
        )}
      </div>
    </div>
  );
}
