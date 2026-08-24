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
    .map((group) => group.find((row) => row.type === "Основной") ?? group[0])
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
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решения"));
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
      const image = defaults
        .map((row) => imageIndex.get(String(row.offer_id))?.primary_image_url)
        .find((value): value is string => Boolean(value)) ?? "";
      const price = defaults.reduce((sum, row) => sum + toPrice(row.price_rub), 0);
      const copy = isConstructorScenarioId(scenarioId) ? SCENARIO_COPY[scenarioId] : undefined;
      return {
        id: scenarioId,
        name: summary.scenario_name,
        space: copy?.space ?? summary.space ?? "",
        occasion: summary.occasion,
        image,
        price,
        items: defaults.length,
      };
    }).filter(Boolean) as Array<{id:string;name:string;space:string;occasion:string;image:string;price:number;items:number}>;
  }, [data]);

  const spaces = useMemo(() => {
    const present = new Set(cards.map((card) => card.space));
    return ["Все", ...SPACE_TAXONOMY.filter((label) => present.has(label))];
  }, [cards]);

  const visible = cards.filter((card) => space === "Все" || card.space === space);

  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем готовые решения…</div></main>;

  return (
    <main className="solution-simple-shell">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/">КУЛЬТУРА ДОМА</Link>
          <span>ГОТОВЫЕ РЕШЕНИЯ</span>
        </nav>

        <header className="solution-simple-heading">
          <small>ГОТОВЫЕ КОМПЛЕКТЫ</small>
          <h1>Выберите готовое решение</h1>
          <p>Мы уже собрали совместимые предметы. Откройте комплект, при необходимости измените состав и добавьте всё в корзину одним действием.</p>
        </header>

        {spaces.length > 2 && <div className="solution-simple-filters" role="tablist" aria-label="Пространство">
          {spaces.map((item) => <button key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}
        </div>}

        <section className="solution-simple-grid" aria-label="Готовые решения">
          {visible.map((card, index) => (
            <Link className="solution-simple-card" href={`/constructor/${card.id}/`} key={card.id}>
              <div className="solution-simple-card-media">
                {card.image ? <RemoteImage src={card.image} alt={card.name} loading={index < 4 ? "eager" : "lazy"}/> : <span>Фото решения</span>}
              </div>
              <div className="solution-simple-card-copy">
                <small>{card.space}</small>
                <h2>{card.name}</h2>
                {card.occasion && <p>{card.occasion}</p>}
                <div className="solution-simple-card-meta"><span>{card.items} товаров</span><strong>{card.price ? `от ${formatRub(card.price)}` : "Цена уточняется"}</strong></div>
                <span className="solution-simple-card-cta">СМОТРЕТЬ КОМПЛЕКТ <b>→</b></span>
              </div>
            </Link>
          ))}
        </section>
      </div>
    </main>
  );
}
