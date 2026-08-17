"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../../../remote-image";
import { ScenarioConstructor } from "../../../constructor/scenario-client";
import { loadConstructorData } from "../../../constructor/data-client";
import { getEditorialScenario } from "../../../editorial-scenario-config";
import type { CandidateRow, CatalogRow, ConstructorData, PresetRow, ScenarioMetaRow } from "../../../constructor/types";
import styles from "../../../editorial-scenarios.module.css";

const EVENT_LABELS: Record<string, string> = {
  tea: "Чаепитие",
  breakfast: "Завтрак",
  lunch: "Обед",
  dinner: "Ужин",
  celebration: "Праздник",
  gift: "Подарок",
  bedroom: "Спальня",
};

const unique = <T,>(values: T[]) => Array.from(new Set(values));

type StoryProduct = {
  offerId: string;
  name: string;
  collection: string;
  image: string;
  productType: string;
};

function fromPreset(row: PresetRow): StoryProduct {
  return {
    offerId: row.offer_id,
    name: row.product_name,
    collection: row.collection,
    image: row.primary_image_url,
    productType: row.product_type,
  };
}

function fromCandidate(row: CandidateRow): StoryProduct {
  return {
    offerId: row.offer_id,
    name: row.product_name,
    collection: row.collection,
    image: row.primary_image_url,
    productType: row.product_type,
  };
}

function fromCatalog(row: CatalogRow): StoryProduct {
  return {
    offerId: row.offer_id,
    name: row.product_name,
    collection: row.collection,
    image: row.primary_image_url,
    productType: row.product_type,
  };
}

function fallbackCatalog(data: ConstructorData, meta: ScenarioMetaRow[]) {
  const collections = unique(
    meta
      .flatMap((row) => `${row.entry_collection}|${row.allowed_collections}`.split("|"))
      .map((value) => value.trim())
      .filter(Boolean),
  );
  return data.catalog.filter((row) => collections.includes(row.collection)).slice(0, 8).map(fromCatalog);
}

function getStoryProducts(data: ConstructorData, scenarioId: string, meta: ScenarioMetaRow[]) {
  const presetProducts = data.presets.filter((row) => row.scenario_id === scenarioId).map(fromPreset);
  if (presetProducts.length) return presetProducts;

  const candidateProducts = data.candidates.filter((row) => row.scenario_id === scenarioId).map(fromCandidate);
  if (candidateProducts.length) {
    const seen = new Set<string>();
    return candidateProducts.filter((item) => {
      if (seen.has(item.offerId)) return false;
      seen.add(item.offerId);
      return true;
    }).slice(0, 8);
  }

  return fallbackCatalog(data, meta);
}

export function EditorialScenarioStory({ scenarioId }: { scenarioId: string }) {
  const config = getEditorialScenario(scenarioId);
  const [data, setData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    loadConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить данные сценария"));
    return () => {
      active = false;
    };
  }, [scenarioId]);

  const meta = useMemo(() => (data?.scenarios ?? []).filter((row) => row.scenario_id === scenarioId), [data, scenarioId]);
  const products = useMemo(() => (data ? getStoryProducts(data, scenarioId, meta) : []), [data, meta, scenarioId]);
  const hasPreset = Boolean(data?.presets.some((row) => row.scenario_id === scenarioId));
  const occasions = unique(meta.flatMap((row) => row.occasion.split("|")).map((value) => value.trim()).filter(Boolean));
  const styling = unique(meta.map((row) => row.styling_message).filter(Boolean)).join(". ");
  const heroImages = unique(products.map((product) => product.image).filter(Boolean)).slice(0, 3);

  if (!config) return null;

  return (
    <div className={styles.storyShell}>
      <header className={styles.storyTopbar}>
        <Link className={styles.storyBrand} href="/">КУЛЬТУРА ДОМА</Link>
        <Link className={styles.storyBack} href="/">← Вернуться к Editorial</Link>
      </header>

      <section className={styles.storyHero}>
        <div className={styles.storyHeroCopy}>
          <span className={styles.storyKicker}>{config.spaceLabel} · EDITORIAL STORY</span>
          <h1>{config.name}</h1>
          <p className={styles.storyHeroLead}>{config.lead}</p>
          <div className={styles.storyHeroMeta}>
            {occasions.map((occasion) => <span key={occasion}>{EVENT_LABELS[occasion] || occasion}</span>)}
            <span>{hasPreset ? "Готовый preset" : "Editorial selection"}</span>
          </div>
          {hasPreset && <a className={styles.storyPrimaryLink} href="#builder">Собрать свою капсулу</a>}
        </div>

        <div className={styles.storyHeroMedia}>
          {heroImages.length ? heroImages.map((image, index) => (
            <RemoteImage key={`${image}-${index}`} src={image} alt={`${config.name}, предмет ${index + 1}`} loading={index === 0 ? "eager" : "lazy"} />
          )) : <div className={styles.scenarioFallback}>Добавьте реальные изображения товаров в CSV</div>}
        </div>
      </section>

      <section className={styles.storySection}>
        <header className={styles.storySectionHead}>
          <h2>История пространства</h2>
          <p>{styling || config.lead} Сценарий строится вокруг конкретного пространства, повода и совместимого набора предметов — без перехода в общий каталог.</p>
        </header>
        <div className={styles.storyRules}>
          <article className={styles.storyRule}>
            <small>Что собираем</small>
            <p>{config.canInclude}</p>
          </article>
          <article className={styles.storyRule}>
            <small>Что не смешиваем</small>
            <p>{config.exclude}</p>
          </article>
        </div>
      </section>

      <section className={styles.storySection}>
        <header className={styles.storySectionHead}>
          <h2>Предметы истории</h2>
          <p>{hasPreset ? "Состав начинается с финального preset и дальше настраивается только совместимыми заменами." : "Ниже показаны реальные товары из разрешённых данных сценария. Они не объявляются готовым набором, пока для сценария не зафиксирован final preset."}</p>
        </header>
        <div className={styles.storyProducts}>
          {products.slice(0, 8).map((product) => (
            <article className={styles.storyProduct} key={`${product.offerId}-${product.name}`}>
              {product.image ? <RemoteImage src={product.image} alt={`${product.name}, ${product.collection}`} loading="lazy" /> : <div className={styles.scenarioFallback}>Фото недоступно</div>}
              <div>
                <small>{product.collection || product.productType}</small>
                <strong>{product.name}</strong>
              </div>
            </article>
          ))}
        </div>
      </section>

      {error && (
        <div className={styles.storyPending}>
          <small>ДАННЫЕ</small>
          <h2>Не удалось загрузить CSV</h2>
          <p>{error}</p>
        </div>
      )}

      {!error && hasPreset && (
        <section id="builder">
          <div className={styles.storySection}>
            <div className={styles.storyBuilderIntro}>
              <span className={styles.storyKicker}>НАСТРОИТЬ ПОД СЕБЯ</span>
              <h2>Соберите свою капсулу</h2>
              <p>Меняйте только совместимые позиции, выбирайте количество персон или размер и сразу видите состав и итоговую стоимость.</p>
            </div>
          </div>
          <ScenarioConstructor scenarioId={scenarioId} />
        </section>
      )}

      {!error && data && !hasPreset && (
        <div className={styles.storyPending}>
          <small>PRESET ЕЩЁ НЕ ЗАФИКСИРОВАН</small>
          <h2>Editorial-история готова, покупаемый набор — ещё нет</h2>
          <p>В текущем `kultura-doma-constructor-presets-final.csv` для «{config.name}» нет финального состава. Поэтому я не подменяю preset кандидатами и не формирую недостоверный cart payload. После добавления preset эта же страница автоматически сможет включить полноценный конструктор.</p>
          <Link className={styles.storyPrimaryLink} href="/constructor/">Посмотреть готовые сценарии</Link>
        </div>
      )}
    </div>
  );
}
