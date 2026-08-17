"use client";

import { useMemo, useState } from "react";
import { RemoteImage } from "../../../remote-image";
import type { CatalogRow, ExpansionRuleRow } from "../../../constructor/types";
import builderStyles from "../../../editorial-expansion-builder.module.css";

const splitPipe = (value: string) => value.split("|").map((item) => item.trim()).filter(Boolean);
const toPrice = (value: string) => {
  const parsed = Number(String(value ?? "").replace(/\s/g, "").replace(",", "."));
  return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
};
const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(Math.round(value))} ₽`;
const isUnavailable = (value: string) => {
  const normalized = String(value ?? "").trim().toLowerCase();
  if (!normalized || normalized === "unknown_from_feed") return false;
  return ["out_of_stock", "unavailable", "not_available", "sold_out", "нет в наличии"].some((token) => normalized.includes(token));
};
const unique = <T,>(values: T[]) => Array.from(new Set(values));

function roleCandidates(rule: ExpansionRuleRow, catalog: CatalogRow[]) {
  const collections = splitPipe(rule.allowed_collections);
  const productTypes = splitPipe(rule.allowed_product_types).filter((item) => item !== "required");
  const seen = new Set<string>();
  return catalog.filter((row) => {
    if (!collections.includes(row.collection) || !productTypes.includes(row.product_type) || !row.offer_id) return false;
    if (seen.has(row.offer_id)) return false;
    seen.add(row.offer_id);
    return true;
  });
}

export function ExpansionScenarioBuilder({ scenarioId, rules, catalog }: { scenarioId: string; rules: ExpansionRuleRow[]; catalog: CatalogRow[] }) {
  const guestOptions = useMemo(
    () => unique(rules.flatMap((rule) => splitPipe(rule.guests_supported)).map(Number).filter((value) => Number.isFinite(value))).sort((a, b) => a - b),
    [rules],
  );
  const [guests, setGuests] = useState(guestOptions[0] || 2);
  const [selected, setSelected] = useState<Record<string, string>>({});
  const [enabled, setEnabled] = useState<Record<string, boolean>>(() => Object.fromEntries(rules.map((rule) => [rule.role, rule.preset_status !== "optional"])));
  const [manualQuantity, setManualQuantity] = useState<Record<string, number>>({});
  const [payload, setPayload] = useState<Array<{ offer_id: string; quantity: number }> | null>(null);

  const pools = useMemo(() => Object.fromEntries(rules.map((rule) => [rule.role, roleCandidates(rule, catalog)])) as Record<string, CatalogRow[]>, [rules, catalog]);
  const selectedRows = rules.map((rule) => ({ rule, product: pools[rule.role]?.find((row) => row.offer_id === selected[rule.role]), enabled: enabled[rule.role] !== false }));
  const quantityFor = (rule: ExpansionRuleRow) => rule.quantity_rule === "per_guest" ? guests : Math.max(1, manualQuantity[rule.role] || 1);

  const problems = selectedRows.flatMap(({ rule, product, enabled: roleEnabled }) => {
    if (!roleEnabled) return [];
    if (!product) {
      if (rule.preset_status === "required") return [`Выберите обязательную позицию: ${rule.flow_step}`];
      return [];
    }
    if (isUnavailable(product.availability_status)) return [`«${product.product_name}» нет в наличии`];
    if (!toPrice(product.price)) return [`Для «${product.product_name}» цена уточняется`];
    return [];
  });

  const activeRows = selectedRows.filter(({ product, enabled: roleEnabled }) => roleEnabled && product);
  const total = activeRows.reduce((sum, { rule, product }) => sum + (toPrice(product!.price) || 0) * quantityFor(rule), 0);
  const totalUnits = activeRows.reduce((sum, { rule }) => sum + quantityFor(rule), 0);

  const addToCart = () => {
    if (problems.length) return;
    const nextPayload = activeRows
      .filter(({ product }) => product && toPrice(product.price) && !isUnavailable(product.availability_status))
      .map(({ rule, product }) => ({ offer_id: product!.offer_id, quantity: quantityFor(rule) }));
    console.log("EDITORIAL_SCENARIO_CART", { scenario_id: scenarioId, items: nextPayload });
    setPayload(nextPayload);
  };

  return (
    <div className={builderStyles.expansionBuilder}>
      <div className={builderStyles.expansionBuilderMain}>
        {guestOptions.length > 1 && <div className={builderStyles.expansionGuests}><small>КОЛИЧЕСТВО ПЕРСОН</small><div>{guestOptions.map((value) => <button key={value} type="button" className={guests === value ? builderStyles.expansionGuestActive : ""} onClick={() => setGuests(value)}>{value}</button>)}</div><p>Автоматически пересчитываются только позиции с quantity_rule = per_guest.</p></div>}
        {rules.map((rule) => {
          const candidates = pools[rule.role] || [];
          const roleEnabled = enabled[rule.role] !== false;
          const product = candidates.find((row) => row.offer_id === selected[rule.role]);
          const images = product ? unique([product.primary_image_url, ...splitPipe(product.all_image_urls)].filter(Boolean)).slice(0, 5) : [];
          const quantity = quantityFor(rule);
          const price = product ? toPrice(product.price) : null;
          return <section className={builderStyles.expansionRole} key={rule.role}><header className={builderStyles.expansionRoleHead}><div><small>{rule.preset_status === "required" ? "ОБЯЗАТЕЛЬНО" : rule.preset_status === "default" ? "ОСНОВА СЦЕНАРИЯ" : "ПО ЖЕЛАНИЮ"}</small><h3>{rule.flow_step}</h3><p>{rule.styling_message}</p></div>{rule.preset_status === "optional" && <button type="button" className={roleEnabled ? builderStyles.expansionToggleActive : builderStyles.expansionToggle} onClick={() => setEnabled((current) => ({ ...current, [rule.role]: !roleEnabled }))}>{roleEnabled ? "Добавлено" : "Добавить"}</button>}</header>{roleEnabled && <>{!candidates.length ? <div className={builderStyles.expansionGap}>В master catalog нет реального товара, одновременно подходящего по allowed_collections и allowed_product_types этой роли. Позиция не подменяется похожим товаром.</div> : <div className={builderStyles.expansionRoleBody}><label className={builderStyles.expansionSelectLabel}><span>Выберите товар</span><select value={selected[rule.role] || ""} onChange={(event) => setSelected((current) => ({ ...current, [rule.role]: event.target.value }))}><option value="">Не выбран</option>{candidates.map((candidate) => { const candidatePrice = toPrice(candidate.price); const unavailable = isUnavailable(candidate.availability_status); return <option key={candidate.offer_id} value={candidate.offer_id} disabled={unavailable}>{candidate.product_name} · {candidate.collection}{candidate.size ? ` · ${candidate.size}` : ""} · {candidatePrice ? formatRub(candidatePrice) : "Цена уточняется"}{unavailable ? " · нет в наличии" : ""}</option> })}</select></label>{product && <div className={builderStyles.expansionSelected}><div className={builderStyles.expansionSelectedGallery}>{images.map((image, index) => <RemoteImage key={`${product.offer_id}-${image}`} src={image} alt={`${product.product_name}, фото ${index + 1}`} loading={index ? "lazy" : "eager"} />)}</div><div className={builderStyles.expansionSelectedCopy}><small>{product.collection} · {product.product_type}</small><h4>{product.product_name}</h4><p>{[product.color, product.size, product.material].filter(Boolean).join(" · ")}</p><strong>{price ? formatRub(price) : "Цена уточняется"}</strong>{isUnavailable(product.availability_status) && <em>Нет в наличии — выберите замену</em>}{!price && <em>Позиция не попадёт в total и payload, пока цена не будет определена.</em>}<div className={builderStyles.expansionQuantity}><span>Количество</span>{rule.quantity_rule === "per_guest" ? <b>{quantity}</b> : <div><button type="button" onClick={() => setManualQuantity((current) => ({ ...current, [rule.role]: Math.max(1, quantity - 1) }))} aria-label="Уменьшить количество">−</button><b>{quantity}</b><button type="button" onClick={() => setManualQuantity((current) => ({ ...current, [rule.role]: quantity + 1 }))} aria-label="Увеличить количество">+</button></div>}</div></div></div>}</div>}</>}</section>
        })}
      </div>
      <aside className={builderStyles.expansionSummary}><small>ВАША КАПСУЛА</small><h3>{activeRows.length} позиций · {totalUnits} шт.</h3><div className={builderStyles.expansionSummaryList}>{activeRows.map(({ rule, product }) => <div key={rule.role}><span>{product!.product_name}</span><b>{quantityFor(rule)} × {toPrice(product!.price) ? formatRub(toPrice(product!.price)!) : "Цена уточняется"}</b></div>)}</div><div className={builderStyles.expansionTotal}><span>Итого</span><strong>{formatRub(total)}</strong></div>{problems.length > 0 && <div className={builderStyles.expansionProblems}>{problems.map((problem) => <p key={problem}>{problem}</p>)}</div>}<button type="button" className={builderStyles.expansionAdd} disabled={problems.length > 0 || !activeRows.length} onClick={addToCart}>{problems.length ? "Завершите настройку" : `Добавить всё · ${formatRub(total)}`}</button></aside>
      {payload && <div className={builderStyles.expansionModalBackdrop} role="presentation" onClick={() => setPayload(null)}><div className={builderStyles.expansionModal} role="dialog" aria-modal="true" aria-label="Состав капсулы" onClick={(event) => event.stopPropagation()}><button type="button" className={builderStyles.expansionModalClose} onClick={() => setPayload(null)} aria-label="Закрыть">×</button><small>MVP CART PAYLOAD</small><h3>Капсула готова</h3><p>В корзину передаются отдельные реальные offer_id и количество.</p><pre>{JSON.stringify(payload, null, 2)}</pre><button type="button" className={builderStyles.expansionAdd} onClick={() => setPayload(null)}>Продолжить</button></div></div>}
    </div>
  );
}
