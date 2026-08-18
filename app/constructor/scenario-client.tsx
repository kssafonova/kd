"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadFinalConstructorData } from "./data-client";
import type { CatalogRow, FinalConstructorData, FinalScenarioVariantRow } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;

const makeCatalogIndex = (rows: CatalogRow[]) => {
  const map = new Map<string, CatalogRow>();
  rows.forEach((row) => {
    const key = String(row.offer_id || "");
    if (key && !map.has(key)) map.set(key, row);
  });
  return map;
};

const splitImages = (catalog?: CatalogRow) => Array.from(new Set([
  catalog?.primary_image_url,
  ...(catalog?.all_image_urls || "").split("|")
].filter((value): value is string => Boolean(value))));

const cleanRole = (role: string) => role.replace(/\s+/g, " ").trim();

export function ScenarioConstructor({ scenarioId }: { scenarioId: string }) {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Record<string, string>>({});
  const [enabled, setEnabled] = useState<Record<string, boolean>>({});
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [expandedRole, setExpandedRole] = useState<string | null>(null);
  const [galleryOffer, setGalleryOffer] = useState<string | null>(null);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    let active = true;
    loadFinalConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить сценарий"));
    return () => { active = false; };
  }, []);

  const summary = useMemo(() => data?.summaries.find((row) => row.scenario_id === scenarioId), [data, scenarioId]);
  const rows = useMemo(() => summary ? (data?.variants ?? []).filter((row) => row.scenario_name === summary.scenario_name) : [], [data, summary]);
  const catalogIndex = useMemo(() => makeCatalogIndex(data?.catalog ?? []), [data]);

  const groups = useMemo(() => {
    const order: string[] = [];
    const map = new Map<string, FinalScenarioVariantRow[]>();
    rows.forEach((row) => {
      const role = cleanRole(row.role);
      if (!map.has(role)) order.push(role);
      map.set(role, [...(map.get(role) ?? []), row]);
    });
    return order.map((role) => ({ role, options: map.get(role) ?? [] }));
  }, [rows]);

  useEffect(() => {
    if (!groups.length) return;
    const nextSelected: Record<string, string> = {};
    const nextEnabled: Record<string, boolean> = {};
    const nextQuantity: Record<string, number> = {};
    groups.forEach(({ role, options }) => {
      const main = options.find((row) => row.type === "Основной");
      const initial = main ?? options[0];
      if (!initial) return;
      nextSelected[role] = initial.offer_id;
      nextEnabled[role] = Boolean(main);
      nextQuantity[role] = 1;
    });
    setSelected(nextSelected);
    setEnabled(nextEnabled);
    setQuantity(nextQuantity);
    setExpandedRole(null);
    setGalleryOffer(null);
    setAdded(false);
  }, [scenarioId, groups.length]);

  const selectedRows = useMemo(() => groups.map(({ role, options }) => {
    const row = options.find((option) => option.offer_id === selected[role]) ?? options.find((option) => option.type === "Основной") ?? options[0];
    return row ? { role, row, enabled: enabled[role] !== false, quantity: quantity[role] || 1 } : null;
  }).filter(Boolean) as Array<{role:string;row:FinalScenarioVariantRow;enabled:boolean;quantity:number}>, [groups, selected, enabled, quantity]);

  const activeRows = selectedRows.filter((item) => item.enabled);
  const total = activeRows.reduce((sum, item) => sum + toPrice(item.row.price_rub) * item.quantity, 0);
  const mainImages = activeRows.map((item) => catalogIndex.get(String(item.row.offer_id))?.primary_image_url).filter((value): value is string => Boolean(value)).slice(0, 5);
  const galleryRow = rows.find((row) => row.offer_id === galleryOffer);
  const galleryCatalog = galleryRow ? catalogIndex.get(String(galleryRow.offer_id)) : undefined;
  const galleryImages = splitImages(galleryCatalog);

  if (error) return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Не удалось загрузить сценарий</h1><p>{error}</p></div></main>;
  if (!data) return <main className="constructor-shell"><div className="constructor-wrap constructor-empty">Загружаем решение…</div></main>;
  if (!summary) return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Сценарий не найден</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;

  const addSolution = () => {
    const payload = activeRows.map((item) => ({
      scenario_id: scenarioId,
      scenario_name: summary.scenario_name,
      offer_id: item.row.offer_id,
      product_name: item.row.product_name,
      quantity: item.quantity,
      unit_price: toPrice(item.row.price_rub),
    }));
    try { localStorage.setItem("kultura-constructor-cart", JSON.stringify(payload)); } catch {}
    setAdded(true);
  };

  return (
    <main className="constructor-shell constructor-detail">
      <div className="constructor-wrap">
        <nav className="constructor-topline">
          <Link className="constructor-back" href="/constructor/">← ВСЕ ГОТОВЫЕ РЕШЕНИЯ</Link>
          <span>{summary.space}</span>
        </nav>

        <header className="constructor-page-head">
          <div>
            <p className="constructor-kicker">ГОТОВОЕ РЕШЕНИЕ · {summary.space.toUpperCase()}</p>
            <h1 className="constructor-title">{summary.scenario_name}</h1>
            <p className="constructor-lead">{summary.occasion}. Основная сборка уже выбрана — меняйте только те предметы, для которых в сценарии предусмотрены альтернативы.</p>
          </div>
          <div className="constructor-head-stat"><span>СОСТАВ</span><strong>{groups.length}</strong><small>групп предметов</small></div>
        </header>

        <section className="constructor-hero-collage" aria-label="Выбранные предметы сценария">
          {Array.from({ length: Math.max(4, Math.min(5, mainImages.length)) }, (_, index) => {
            const image = mainImages[index];
            return image ? <div key={`${image}-${index}`}><RemoteImage src={image} alt={`${summary.scenario_name}: выбранный предмет ${index + 1}`} loading={index < 3 ? "eager" : "lazy"}/></div> : <div className="constructor-image-fallback" key={index}>Фото товара</div>;
          })}
        </section>

        <div className="constructor-layout">
          <section className="constructor-builder">
            <header className="constructor-section-head">
              <div><p className="constructor-kicker">СОСТАВ РЕШЕНИЯ</p><h2>Настройте под себя</h2></div>
              <p>Основной предмет выбран автоматически. Нажмите «Другой вариант», чтобы заменить его на альтернативу из финального сценария.</p>
            </header>

            <div className="constructor-role-list">
              {groups.map(({ role, options }, index) => {
                const current = options.find((option) => option.offer_id === selected[role]) ?? options.find((option) => option.type === "Основной") ?? options[0];
                if (!current) return null;
                const catalog = catalogIndex.get(String(current.offer_id));
                const image = catalog?.primary_image_url;
                const isEnabled = enabled[role] !== false;
                const hasMain = options.some((option) => option.type === "Основной");
                const hasAlternatives = options.length > 1;
                const q = quantity[role] || 1;
                return <article className={`constructor-role ${isEnabled ? "active" : "inactive"}`} key={role}>
                  <div className="constructor-role-number">{String(index + 1).padStart(2, "0")}</div>
                  <button className="constructor-role-image" onClick={() => setGalleryOffer(current.offer_id)} aria-label={`Открыть изображения ${current.product_name}`}>
                    {image ? <RemoteImage src={image} alt={current.product_name}/> : <span className="constructor-image-fallback">Фото товара</span>}
                  </button>
                  <div className="constructor-role-copy">
                    <div className="constructor-role-heading"><div><p>{role}</p><h3>{current.product_name}</h3></div><button className={`constructor-inclusion ${isEnabled ? "active" : ""}`} onClick={() => setEnabled((state) => ({ ...state, [role]: !isEnabled }))}>{isEnabled ? "В РЕШЕНИИ ✓" : "+ ДОБАВИТЬ"}</button></div>
                    <div className="constructor-product-facts">
                      {current.material && <span>{current.material}</span>}
                      {current.color && <span>Цвет: {current.color}</span>}
                      <span>Арт. {current.offer_id}</span>
                      {!hasMain && <span className="constructor-optional-label">Дополнение</span>}
                    </div>
                    {current.note && <p className="constructor-note">{current.note}</p>}
                    <div className="constructor-role-bottom">
                      <div className="constructor-price">{toPrice(current.price_rub) ? formatRub(toPrice(current.price_rub)) : "Цена уточняется"}</div>
                      <div className="constructor-qty" aria-label="Количество"><button onClick={() => setQuantity((state) => ({ ...state, [role]: Math.max(1, q - 1) }))}>−</button><span>{q}</span><button onClick={() => setQuantity((state) => ({ ...state, [role]: q + 1 }))}>+</button></div>
                      {hasAlternatives && <button className="constructor-change" onClick={() => setExpandedRole(expandedRole === role ? null : role)}>{expandedRole === role ? "СКРЫТЬ ВАРИАНТЫ" : `ДРУГОЙ ВАРИАНТ · ${options.length - 1}`}</button>}
                    </div>

                    {expandedRole === role && <div className="constructor-alternatives">
                      {options.map((option) => {
                        const optionCatalog = catalogIndex.get(String(option.offer_id));
                        const optionImage = optionCatalog?.primary_image_url;
                        const picked = current.offer_id === option.offer_id;
                        return <button key={option.offer_id} className={picked ? "selected" : ""} onClick={() => { setSelected((state) => ({ ...state, [role]: option.offer_id })); setEnabled((state) => ({ ...state, [role]: true })); setAdded(false); }}>
                          <span className="constructor-alt-image">{optionImage ? <RemoteImage src={optionImage} alt={option.product_name}/> : <i/>}</span>
                          <span className="constructor-alt-copy"><small>{option.type === "Основной" ? "ОСНОВНОЙ" : "АЛЬТЕРНАТИВА"}</small><strong>{option.product_name}</strong><em>{formatRub(toPrice(option.price_rub))}</em></span>
                          <b>{picked ? "✓" : ""}</b>
                        </button>;
                      })}
                    </div>}
                  </div>
                </article>;
              })}
            </div>
          </section>

          <aside className="constructor-summary">
            <p>ВАШЕ РЕШЕНИЕ</p>
            <h2>{summary.scenario_name}</h2>
            <div className="constructor-summary-list">
              {activeRows.map((item) => <div className="constructor-summary-item" key={item.role}><span>{item.row.product_name}<small>{item.quantity} шт.</small></span><b>{formatRub(toPrice(item.row.price_rub) * item.quantity)}</b></div>)}
            </div>
            <div className="constructor-summary-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong><small>{activeRows.length} позиций в выбранной сборке</small></div>
            <button className="constructor-primary" disabled={!activeRows.length} onClick={addSolution}>ДОБАВИТЬ РЕШЕНИЕ · {formatRub(total)}</button>
            <p className="constructor-summary-hint">Вы можете изменить состав до оформления заказа.</p>
            {added && <div className="constructor-success"><b>Решение сохранено</b><span>{activeRows.length} позиций добавлены в выбранный комплект.</span></div>}
          </aside>
        </div>
      </div>

      {galleryRow && galleryImages.length > 0 && <div className="constructor-overlay center" role="dialog" aria-modal="true" aria-label={`Галерея ${galleryRow.product_name}`}>
        <button className="constructor-overlay-bg" onClick={() => setGalleryOffer(null)} aria-label="Закрыть"/>
        <div className="constructor-modal constructor-gallery-modal">
          <div className="constructor-panel-head"><div><p className="constructor-kicker">{galleryRow.role}</p><h2>{galleryRow.product_name}</h2></div><button className="constructor-panel-close" onClick={() => setGalleryOffer(null)}>×</button></div>
          <div className="constructor-gallery-grid">{galleryImages.map((image, index) => <div key={`${image}-${index}`}><RemoteImage src={image} alt={`${galleryRow.product_name}, фото ${index + 1}`}/></div>)}</div>
        </div>
      </div>}
    </main>
  );
}
