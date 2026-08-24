"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS } from "./table-solutions";
import { resolveTableSolutionProducts } from "./table-solution-resolver";
import {
  buildSolutionGroups,
  deriveGuestOptions,
  recommendedProductQuantity,
  selectionForPreset,
} from "./table-solution-builder";
import type { ConstructorData, FinalConstructorData } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;

export function ConstructorLanding() {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [ruleData, setRuleData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [space, setSpace] = useState("Все");
  const [people, setPeople] = useState(0);

  useEffect(() => {
    let active = true;
    Promise.all([
      loadFinalConstructorData(),
      loadConstructorData().catch(() => null),
    ])
      .then(([loaded, rules]) => {
        if (!active) return;
        setData(loaded);
        setRuleData(rules);
      })
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решения"));
    return () => { active = false; };
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    return TABLE_SOLUTIONS.map((solution) => {
      const rows = resolveTableSolutionProducts(data.catalog, solution);
      const guestOptions = deriveGuestOptions(solution, ruleData);
      const targetPeople = people && guestOptions.includes(people) ? people : guestOptions[0] || 1;
      const groups = buildSolutionGroups(rows, solution.space);
      const balanced = selectionForPreset(groups, "balanced");
      const scenarioRows = rows.filter((row) => balanced.has(row.offer_id));
      const price = scenarioRows.reduce((sum, row) => sum + toPrice(row.price) * recommendedProductQuantity(row, solution.space, targetPeople), 0);
      return {
        ...solution,
        rows,
        scenarioRows,
        guestOptions,
        targetPeople,
        fallbackImage: rows[0]?.primary_image_url || "/images/image-placeholder.svg",
        price,
      };
    });
  }, [data, ruleData, people]);

  const spaces = useMemo(() => ["Все", ...Array.from(new Set(TABLE_SOLUTIONS.map((item) => item.space)))], []);
  const availablePeople = useMemo(() => Array.from(new Set(cards.flatMap((card) => card.guestOptions))).sort((a, b) => a - b), [cards]);
  const visible = cards.filter((card) => (space === "Все" || card.space === space) && (!people || card.guestOptions.includes(people)));

  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем готовые решения…</div></main>;

  return (
    <main className="solution-simple-shell table-solutions-shell table-solutions-finder-v25">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/">КУЛЬТУРА ДОМА</Link>
          <span>ГОТОВЫЕ РЕШЕНИЯ</span>
        </nav>

        <header className="solution-simple-heading table-solutions-heading">
          <small>ГОТОВЫЕ РЕШЕНИЯ</small>
          <h1>Соберите пространство под свой сценарий</h1>
          <p>Выберите пространство и количество персон. Мы покажем подходящие решения, а внутри предложим базовую, оптимальную и полную комплектацию из реальных товаров каталога.</p>
        </header>

        <section className="table-solution-finder" aria-label="Подбор готового решения">
          <div className="table-solution-finder-block">
            <small>01 · ПРОСТРАНСТВО</small>
            <div className="table-solution-finder-options">
              {spaces.map((item) => <button type="button" key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}
            </div>
          </div>
          <div className="table-solution-finder-block">
            <small>02 · КОЛИЧЕСТВО ПЕРСОН</small>
            <div className="table-solution-finder-options table-solution-finder-people">
              <button type="button" className={people === 0 ? "active" : ""} onClick={() => setPeople(0)}>Любое</button>
              {availablePeople.map((value) => <button type="button" key={value} className={people === value ? "active" : ""} onClick={() => setPeople(value)}>{value}</button>)}
            </div>
          </div>
          <div className="table-solution-finder-result"><strong>{visible.length}</strong><span>{visible.length === 1 ? "подходящее решение" : "подходящих решений"}</span></div>
        </section>

        <section className="solution-simple-grid table-solution-grid" aria-label="Готовые решения">
          {visible.map((card, index) => {
            const source = card.previewFile ? `/images/constructor/${card.previewFile}` : card.fallbackImage;
            return (
              <Link className="solution-simple-card table-solution-card table-solution-finder-card" href={`/constructor/${card.id}/`} key={card.id}>
                <div className="solution-simple-card-media table-solution-card-media">
                  <RemoteImage src={source} fallbackSrc={card.fallbackImage} alt={card.name} loading={index < 4 ? "eager" : "lazy"}/>
                  <span className="table-solution-number">{String(card.sourceId).padStart(2, "0")}</span>
                  <span className="table-solution-card-scenario">ОПТИМАЛЬНЫЙ СЦЕНАРИЙ</span>
                </div>
                <div className="solution-simple-card-copy table-solution-card-copy">
                  <small>{card.space}</small>
                  <h2>{card.name}</h2>
                  <div className="table-solution-card-guests" aria-label="Количество персон">
                    {card.guestOptions.map((value) => <span className={people === value ? "active" : ""} key={value}>{value} {value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</span>)}
                  </div>
                  {card.collections.length > 0 && <div className="table-solution-collections" aria-label="Коллекции">
                    {card.collections.map((collection) => <span key={collection}>{collection}</span>)}
                  </div>}
                  <div className="table-solution-finder-card-summary">
                    <div><small>РЕКОМЕНДУЕМ</small><span>{card.scenarioRows.length} из {card.rows.length} товаров</span></div>
                    <strong>{card.price ? `от ${formatRub(card.price)}` : "—"}</strong>
                  </div>
                  <span className="solution-simple-card-cta">НАСТРОИТЬ РЕШЕНИЕ <b>→</b></span>
                </div>
              </Link>
            );
          })}
        </section>

        {visible.length === 0 && <section className="table-solution-finder-empty"><h2>Нет точного совпадения</h2><p>Измените количество персон или пространство — состав любого решения всё равно можно настроить вручную внутри конструктора.</p><button type="button" onClick={() => { setSpace("Все"); setPeople(0); }}>ПОКАЗАТЬ ВСЕ РЕШЕНИЯ</button></section>}
      </div>
    </main>
  );
}
