"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadFinalConstructorData } from "./data-client";
import { SCENARIO_COPY, SPACE_TAXONOMY } from "./scenario-copy";
import { CONSTRUCTOR_SCENARIO_IDS, isConstructorScenarioId } from "./scenarios";
import type { CatalogRow, FinalConstructorData, FinalScenarioVariantRow } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;

const catalogByOffer = (catalog: CatalogRow[]) => {
  const map = new Map<string, CatalogRow>();
  catalog.forEach((row) => {
    if (row.offer_id && !map.has(String(row.offer_id))) map.set(String(row.offer_id), row);
  });
  return map;
};

const defaultRows = (rows: FinalScenarioVariantRow[]) => {
  const groups = new Map<string, FinalScenarioVariantRow[]>();
  rows.forEach((row) => groups.set(row.role, [...(groups.get(row.role) ?? []), row]));
  return Array.from(groups.values())
    .map((group) => group.find((row) => row.type === "Основной"))
    .filter((row): row is FinalScenarioVariantRow => Boolean(row));
};

export function ConstructorLanding() {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [error, setError] = useState("");
  const [space, setSpace] = useState("Все");

  useEffect(() => {
    let active = true;
    loadFinalConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить сценарии"));
    return () => { active = false; };
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    const imageIndex = catalogByOffer(data.catalog);
    return CONSTRUCTOR_SCENARIO_IDS.map((scenarioId) => {
      const summary = data.summaries.find((row) => row.scenario_id === scenarioId);
      if (!summary) return null;
      const rows = data.variants.filter((row) => row.scenario_name === summary.scenario_name);
      const defaults = defaultRows(rows);
      const images = Array.from(new Set(defaults
        .map((row) => imageIndex.get(String(row.offer_id))?.primary_image_url)
        .filter((value): value is string => Boolean(value)))).slice(0, 3);
      const price = defaults.reduce((sum, row) => sum + toPrice(row.price_rub), 0);
      const savings = defaults.reduce((sum, row) => {
        const oldPrice = toPrice(imageIndex.get(String(row.offer_id))?.old_price);
        const rowPrice = toPrice(row.price_rub);
        return oldPrice > rowPrice ? sum + (oldPrice - rowPrice) : sum;
      }, 0);
      const copy = isConstructorScenarioId(scenarioId) ? SCENARIO_COPY[scenarioId] : undefined;
      return {
        id: scenarioId,
        name: summary.scenario_name,
        space: copy?.space ?? "",
        occasion: summary.occasion,
        mood: copy?.mood ?? "",
        images,
        price,
        savings,
        roles: new Set(rows.map((row) => row.role)).size,
        alternatives: rows.filter((row) => row.type === "Альтернатива").length,
      };
    }).filter(Boolean) as Array<{id:string;name:string;space:string;occasion:string;mood:string;images:string[];price:number;savings:number;roles:number;alternatives:number}>;
  }, [data]);

  // Only offer a filter tab for a space that at least one live scenario
  // actually belongs to — "Гостиная"/"Ванная" join automatically the day a
  // scenario is added there, no empty dead-end tabs in the meantime.
  const spaces = useMemo(() => {
    const present = new Set(cards.map((card) => card.space));
    return ["Все", ...SPACE_TAXONOMY.filter((label) => present.has(label))];
  }, [cards]);

  const visible = cards.filter((card) => space === "Все" || card.space === space);

  if (error) return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Не удалось загрузить сценарии</h1><p>{error}</p></div></main>;
  if (!data) return <main className="constructor-shell"><div className="constructor-wrap constructor-empty">Загружаем готовые решения…</div></main>;

  return (
    <main className="constructor-shell constructor-landing">
      <div className="constructor-wrap">
        <nav className="constructor-topline">
          <Link className="constructor-back" href="/">КУЛЬТУРА ДОМА</Link>
          <span>ГОТОВЫЕ РЕШЕНИЯ</span>
        </nav>

        <header className="constructor-landing-head">
          <p className="constructor-kicker">EDITORIAL · ГОТОВЫЕ РЕШЕНИЯ</p>
          <h1 className="constructor-title">Соберите атмосферу дома</h1>
          <p className="constructor-lead">Каждое решение — реальная сервировка или спальный сценарий, собранный куратором. Оставьте состав как есть или замените отдельные предметы на совместимые альтернативы.</p>
        </header>

        <div className="constructor-filter" role="tablist" aria-label="Фильтр по пространству">
          {spaces.map((item) => <button key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item.toUpperCase()}</button>)}
        </div>

        <section className="constructor-scenario-grid" aria-label="Готовые решения">
          {visible.map((card, index) => (
            <article className="constructor-scenario-card" key={card.id}>
              <Link className="constructor-scenario-media" href={`/constructor/${card.id}/`} aria-label={`Открыть ${card.name}`}>
                <div className="constructor-scenario-collage">
                  {Array.from({ length: 3 }, (_, imageIndex) => {
                    const image = card.images[imageIndex];
                    return image ? <div key={image}><RemoteImage src={image} alt={`${card.name}: предмет ${imageIndex + 1}`} loading={index < 2 ? "eager" : "lazy"}/></div> : <div className="constructor-image-fallback" key={imageIndex}>Фото товара</div>;
                  })}
                </div>
              </Link>
              <div className="constructor-scenario-copy">
                <div className="constructor-card-labels"><span>{card.space}</span><span>{card.occasion}</span></div>
                <h2>{card.name}</h2>
                {card.mood && <p className="constructor-card-mood">{card.mood}</p>}
                <div className="constructor-scenario-meta">
                  <div>
                    <small>{card.roles} групп · {card.alternatives} альтернатив</small>
                    <strong>{card.price ? `от ${formatRub(card.price)}` : "Цена уточняется"}</strong>
                    {card.savings > 0 && <em className="constructor-card-savings">Экономия от {formatRub(card.savings)}</em>}
                  </div>
                  <Link className="constructor-primary-link" href={`/constructor/${card.id}/`}>СОБРАТЬ РЕШЕНИЕ <span>→</span></Link>
                </div>
              </div>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
