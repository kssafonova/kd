"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadFinalConstructorData } from "./data-client";
import { trackConstructorEvent } from "./logic";
import { SCENARIO_COPY } from "./scenario-copy";
import { isConstructorScenarioId } from "./scenarios";
import type { CatalogRow, FinalConstructorData, FinalScenarioVariantRow } from "./types";

const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const CART_STORAGE_KEY = "kultura-cart";
const CART_ID_OFFSET = 900000;

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

type SharedCartItem = {
  id: number;
  name: string;
  note: string;
  price: number;
  image: string;
  gallery: string[];
  selectedColor: string;
  selectedSize: string;
  selectedSkuId: string;
  quantity: number;
  skus: Array<{
    id: string;
    article: string;
    productId: number;
    color: string;
    colorHex: string;
    size: string;
    material: string;
    composition: string;
    price: number;
    image: string;
    gallery: string[];
  }>;
};

const mergeIntoSharedCart = (items: SharedCartItem[]) => {
  let existing: SharedCartItem[] = [];
  try {
    const raw = localStorage.getItem(CART_STORAGE_KEY);
    if (raw) existing = JSON.parse(raw);
  } catch { existing = []; }
  const merged = [...existing];
  items.forEach((item) => {
    const matchIndex = merged.findIndex((entry) => entry.id === item.id && entry.selectedColor === item.selectedColor);
    if (matchIndex >= 0) merged[matchIndex] = { ...merged[matchIndex], quantity: merged[matchIndex].quantity + item.quantity };
    else merged.push(item);
  });
  try { localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(merged)); } catch {}
};

export function ScenarioConstructor({ scenarioId }: { scenarioId: string }) {
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [error, setError] = useState("");
  const [selected, setSelected] = useState<Record<string, string>>({});
  const [enabled, setEnabled] = useState<Record<string, boolean>>({});
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [expandedRole, setExpandedRole] = useState<string | null>(null);
  const [redirecting, setRedirecting] = useState(false);

  useEffect(() => {
    let active = true;
    loadFinalConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решение"));
    return () => { active = false; };
  }, []);

  const summary = useMemo(() => data?.summaries.find((row) => row.scenario_id === scenarioId), [data, scenarioId]);
  const rows = useMemo(() => summary ? (data?.variants ?? []).filter((row) => row.scenario_name === summary.scenario_name) : [], [data, summary]);
  const catalogIndex = useMemo(() => makeCatalogIndex(data?.catalog ?? []), [data]);
  const copy = isConstructorScenarioId(scenarioId) ? SCENARIO_COPY[scenarioId] : undefined;

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
    setRedirecting(false);
  }, [scenarioId, groups.length]);

  const selectedRows = useMemo(() => groups.map(({ role, options }) => {
    const row = options.find((option) => option.offer_id === selected[role]) ?? options.find((option) => option.type === "Основной") ?? options[0];
    return row ? { role, row, enabled: enabled[role] !== false, quantity: quantity[role] || 1, options } : null;
  }).filter(Boolean) as Array<{ role: string; row: FinalScenarioVariantRow; enabled: boolean; quantity: number; options: FinalScenarioVariantRow[] }>, [groups, selected, enabled, quantity]);

  const activeRows = selectedRows.filter((item) => item.enabled);
  const total = activeRows.reduce((sum, item) => sum + toPrice(item.row.price_rub) * item.quantity, 0);
  const heroImage = activeRows
    .map((item) => catalogIndex.get(String(item.row.offer_id))?.primary_image_url)
    .find((value): value is string => Boolean(value)) ?? "";

  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;
  if (!summary) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;

  const addSolution = () => {
    const items: SharedCartItem[] = activeRows.map((item) => {
      const catalog = catalogIndex.get(String(item.row.offer_id));
      const unitPrice = toPrice(item.row.price_rub);
      const image = catalog?.primary_image_url || "";
      const gallery = splitImages(catalog);
      const skuId = `solution-${item.row.offer_id}`;
      const numericId = CART_ID_OFFSET + (Number(item.row.offer_id) || 0);
      return {
        id: numericId,
        name: item.row.product_name,
        note: `Из готового решения «${summary.scenario_name}»`,
        price: unitPrice,
        image,
        gallery,
        selectedColor: item.row.color || "",
        selectedSize: "1 шт",
        selectedSkuId: skuId,
        quantity: item.quantity,
        skus: [{
          id: skuId,
          article: String(item.row.offer_id),
          productId: numericId,
          color: item.row.color || "",
          colorHex: "#d8d5cf",
          size: "1 шт",
          material: item.row.material || "",
          composition: "",
          price: unitPrice,
          image,
          gallery,
        }],
      };
    });

    mergeIntoSharedCart(items);
    trackConstructorEvent("constructor:add_solution", { scenario_id: scenarioId, items: items.length, total });
    setRedirecting(true);
    window.setTimeout(() => {
      const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
      window.location.href = `${base}/?cart=open`;
    }, 500);
  };

  return (
    <main className="solution-simple-shell solution-detail-shell">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/constructor/">← ГОТОВЫЕ РЕШЕНИЯ</Link>
          <span>{copy?.space ?? summary.space}</span>
        </nav>

        <section className="solution-detail-hero">
          <div className="solution-detail-hero-media">
            {heroImage ? <RemoteImage src={heroImage} alt={summary.scenario_name} loading="eager"/> : <span>Фото решения</span>}
          </div>
          <div className="solution-detail-hero-copy">
            <small>ГОТОВОЕ РЕШЕНИЕ · {(copy?.space ?? summary.space).toUpperCase()}</small>
            <h1>{summary.scenario_name}</h1>
            {summary.occasion && <p className="solution-detail-occasion">{summary.occasion}</p>}
            <p>{copy?.narrative ?? "Все предметы уже подобраны друг к другу. Оставьте комплект как есть или измените только нужные позиции."}</p>
            <div className="solution-detail-hero-meta"><span>{activeRows.length} товаров выбрано</span><strong>{formatRub(total)}</strong></div>
            <a className="solution-detail-anchor" href="#solution-products">СМОТРЕТЬ СОСТАВ ↓</a>
          </div>
        </section>

        <div className="solution-detail-layout" id="solution-products">
          <section className="solution-detail-products">
            <header className="solution-detail-section-head">
              <div><small>СОСТАВ</small><h2>Что входит в комплект</h2></div>
              <p>Снимите галочку, если товар не нужен. Количество и замену можно изменить прямо здесь.</p>
            </header>

            <div className="solution-product-list">
              {selectedRows.map(({ role, row, enabled: isEnabled, quantity: q, options }) => {
                const catalog = catalogIndex.get(String(row.offer_id));
                const image = catalog?.primary_image_url;
                const hasAlternatives = options.length > 1;
                return (
                  <article className={`solution-product-row ${isEnabled ? "selected" : "disabled"}`} key={role}>
                    <label className="solution-product-check" aria-label={isEnabled ? `Убрать ${row.product_name}` : `Добавить ${row.product_name}`}>
                      <input type="checkbox" checked={isEnabled} onChange={(event) => setEnabled((state) => ({ ...state, [role]: event.target.checked }))}/>
                      <span/>
                    </label>
                    <div className="solution-product-image">
                      {image ? <RemoteImage src={image} alt={row.product_name}/> : <span>Фото</span>}
                    </div>
                    <div className="solution-product-copy">
                      <small>{role}</small>
                      <h3>{row.product_name}</h3>
                      <div className="solution-product-facts">
                        {row.color && <span>Цвет: {row.color}</span>}
                        {row.material && <span>{row.material}</span>}
                        <span>Арт. {row.offer_id}</span>
                      </div>
                      <div className="solution-product-controls">
                        <strong>{toPrice(row.price_rub) ? formatRub(toPrice(row.price_rub)) : "Цена уточняется"}</strong>
                        {isEnabled && <div className="solution-product-qty"><button type="button" onClick={() => setQuantity((state) => ({ ...state, [role]: Math.max(1, q - 1) }))} aria-label="Уменьшить количество">−</button><span>{q}</span><button type="button" onClick={() => setQuantity((state) => ({ ...state, [role]: q + 1 }))} aria-label="Увеличить количество">+</button></div>}
                        {hasAlternatives && <button className="solution-replace-button" type="button" onClick={() => setExpandedRole(expandedRole === role ? null : role)}>{expandedRole === role ? "СКРЫТЬ" : "ЗАМЕНИТЬ"}</button>}
                      </div>
                    </div>

                    {expandedRole === role && <div className="solution-replacements">
                      <p>Выберите другой вариант</p>
                      <div>{options.map((option) => {
                        const optionCatalog = catalogIndex.get(String(option.offer_id));
                        const optionImage = optionCatalog?.primary_image_url;
                        const active = option.offer_id === row.offer_id;
                        return <button type="button" className={active ? "active" : ""} key={option.offer_id} onClick={() => { setSelected((state) => ({ ...state, [role]: option.offer_id })); setEnabled((state) => ({ ...state, [role]: true })); setExpandedRole(null); }}>
                          <span className="solution-replacement-image">{optionImage ? <RemoteImage src={optionImage} alt={option.product_name}/> : <i>Фото</i>}</span>
                          <span><b>{option.product_name}</b><small>{option.color || option.material || `Арт. ${option.offer_id}`}</small><strong>{toPrice(option.price_rub) ? formatRub(toPrice(option.price_rub)) : "Цена уточняется"}</strong></span>
                        </button>;
                      })}</div>
                    </div>}
                  </article>
                );
              })}
            </div>
          </section>

          <aside className="solution-purchase-card">
            <small>ВАШ КОМПЛЕКТ</small>
            <h2>{summary.scenario_name}</h2>
            <div className="solution-purchase-count"><span>Выбрано</span><b>{activeRows.length} из {selectedRows.length}</b></div>
            <div className="solution-purchase-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong></div>
            <button type="button" disabled={!activeRows.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ КОМПЛЕКТ В КОРЗИНУ"}</button>
            <p>Все выбранные товары попадут в обычную корзину отдельными позициями.</p>
          </aside>
        </div>
      </div>
    </main>
  );
}
