"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import { buildSolutionCategories, deriveGuestOptions, pickOptionVariant, recommendedSlotQuantity } from "./table-solution-builder";
import type { ConstructorData, FinalConstructorData } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const peopleLabel = (value: number) => `${value} ${value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}`;

export function ConstructorLanding() {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [ruleData, setRuleData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [space, setSpace] = useState("Все");
  const [people, setPeople] = useState(0);

  useEffect(() => {
    let active = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
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
      const catalogRows = resolveTableSolutionCatalogRows(data.catalog, solution);
      const guestOptions = deriveGuestOptions(solution, ruleData);
      const targetPeople = people && guestOptions.includes(people) ? people : guestOptions[0] || 1;
      const categories = buildSolutionCategories(catalogRows, solution.space);
      const slots = categories.flatMap((category) => category.slots);
      const defaultRows = slots
        .map((slot) => {
          const option = slot.options[0];
          const row = option ? pickOptionVariant(option) : undefined;
          return row ? { row, quantity: recommendedSlotQuantity(slot, targetPeople) } : null;
        })
        .filter((item): item is { row: NonNullable<typeof item> extends { row: infer R } ? R : never; quantity: number } => Boolean(item));
      const price = defaultRows.reduce((sum, item) => sum + toPrice(item.row.price) * item.quantity, 0);
      const productCount = Array.from(new Set(catalogRows.map((row) => row.product_name))).length;
      return {
        ...solution,
        catalogRows,
        categories,
        slots,
        guestOptions,
        targetPeople,
        fallbackImage: catalogRows[0]?.primary_image_url || "/images/image-placeholder.svg",
        price,
        productCount,
      };
    });
  }, [data, ruleData, people]);

  const spaces = useMemo(() => ["Все", ...Array.from(new Set(TABLE_SOLUTIONS.map((item) => item.space)))], []);
  const availablePeople = useMemo(() => Array.from(new Set(cards.flatMap((card) => card.guestOptions))).sort((a, b) => a - b), [cards]);
  const visible = cards.filter((card) => (space === "Все" || card.space === space) && (!people || card.guestOptions.includes(people)));
  const featured = visible[0];
  const rest = visible.slice(1);

  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить готовые решения</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем готовые решения…</div></main>;

  return (
    <main className="kd-solutions-v30">
      <div className="kd-solutions-wrap-v30">
        <nav className="kd-solutions-top-v30">
          <Link href="/">КУЛЬТУРА ДОМА</Link>
          <span>ГОТОВЫЕ РЕШЕНИЯ</span>
        </nav>

        <header className="kd-solutions-intro-v30">
          <small>ГОТОВЫЕ РЕШЕНИЯ</small>
          <h1>Пространство, собранное за вас</h1>
          <p>Готовые сочетания предметов из разных коллекций. Выберите сценарий, количество персон и настройте состав под себя уже внутри решения.</p>
        </header>

        <section className="kd-solutions-filters-v30" aria-label="Фильтры готовых решений">
          <div className="kd-solutions-filter-v30">
            <span>Пространство</span>
            <div className="kd-solutions-space-tabs-v30">
              {spaces.map((item) => <button type="button" key={item} className={space === item ? "active" : ""} onClick={() => setSpace(item)}>{item}</button>)}
            </div>
          </div>
          <div className="kd-solutions-filter-v30 kd-solutions-people-v30">
            <span>Количество персон</span>
            <div>
              <button type="button" className={people === 0 ? "active" : ""} onClick={() => setPeople(0)}>Любое</button>
              {availablePeople.map((value) => <button type="button" key={value} className={people === value ? "active" : ""} onClick={() => setPeople(value)}>{value}</button>)}
            </div>
          </div>
        </section>

        {featured ? (
          <>
            <Link className="kd-solutions-feature-v30" href={`/constructor/${featured.id}/`}>
              <div className="kd-solutions-feature-media-v30">
                <RemoteImage src={featured.previewFile ? `/images/constructor/${featured.previewFile}` : featured.fallbackImage} fallbackSrc={featured.fallbackImage} alt={featured.name} loading="eager"/>
              </div>
              <div className="kd-solutions-feature-copy-v30">
                <div>
                  <small>{featured.space}</small>
                  <h2>{featured.name}</h2>
                  <p>{featured.collections.length ? featured.collections.join(" · ") : "Готовое сочетание предметов для дома"}</p>
                </div>
                <dl>
                  <div><dt>Персон</dt><dd>{featured.guestOptions.map((value) => value).join(" / ")}</dd></div>
                  <div><dt>Товаров</dt><dd>{featured.productCount}</dd></div>
                  <div><dt>Стоимость</dt><dd>{featured.price ? `от ${formatRub(featured.price)}` : "Соберите состав"}</dd></div>
                </dl>
                <span>СОБРАТЬ РЕШЕНИЕ <b>→</b></span>
              </div>
            </Link>

            {rest.length > 0 && <section className="kd-solutions-list-head-v30"><h2>Ещё решения</h2><span>{visible.length} {visible.length === 1 ? "сценарий" : "сценариев"}</span></section>}

            <section className="kd-solutions-grid-v30" aria-label="Готовые решения">
              {rest.map((card, index) => (
                <Link className="kd-solutions-card-v30" href={`/constructor/${card.id}/`} key={card.id}>
                  <div className="kd-solutions-card-media-v30">
                    <RemoteImage src={card.previewFile ? `/images/constructor/${card.previewFile}` : card.fallbackImage} fallbackSrc={card.fallbackImage} alt={card.name} loading={index < 3 ? "eager" : "lazy"}/>
                  </div>
                  <div className="kd-solutions-card-copy-v30">
                    <small>{card.space}</small>
                    <h3>{card.name}</h3>
                    <p>{card.collections.length ? card.collections.join(" · ") : "Готовое решение"}</p>
                    <div className="kd-solutions-card-meta-v30">
                      <span>{card.guestOptions.map(peopleLabel).join(" · ")}</span>
                      <strong>{card.price ? `от ${formatRub(card.price)}` : "Собрать"}</strong>
                    </div>
                    <span className="kd-solutions-card-cta-v30">СМОТРЕТЬ РЕШЕНИЕ <b>→</b></span>
                  </div>
                </Link>
              ))}
            </section>
          </>
        ) : (
          <section className="kd-solutions-empty-v30">
            <h2>Нет точного совпадения</h2>
            <p>Попробуйте изменить пространство или количество персон. Состав любого готового решения можно настроить вручную.</p>
            <button type="button" onClick={() => { setSpace("Все"); setPeople(0); }}>ПОКАЗАТЬ ВСЕ</button>
          </section>
        )}
      </div>
    </main>
  );
}
