"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData } from "./data-client";
import {
  buildCartPayload,
  calculateSummary,
  createIndexes,
  deriveProductView,
  formatRub,
  getBlockingReasons,
  getReplacementCandidates,
  getVariantOptions,
  isUnavailable,
  toNumber,
  trackConstructorEvent,
} from "./logic";
import type {
  CandidateRow,
  CatalogRow,
  CartPayloadItem,
  ConstructorData,
  PresetRow,
  ProductView,
  SlotState,
} from "./types";

const GUEST_OPTIONS = [2, 4, 6, 8] as const;

const humanProductType = (value: string) => {
  const labels: Record<string, string> = {
    tea_pair: "Чайная пара",
    coffee_pair: "Кофейная пара",
    dessert_plate: "Десертная тарелка",
    dinner_plate: "Обеденная тарелка",
    snack_plate: "Закусочная тарелка",
    napkin: "Салфетка",
    placemat: "Плейсмат",
    table_runner: "Дорожка",
    tablecloth: "Скатерть",
    milk_jug: "Молочник",
    sugar_bowl: "Сахарница",
    teapot: "Чайник",
    decorative_pillow: "Декоративная подушка",
    throw: "Плед",
    candle: "Свеча",
    bedding_set: "Постельное бельё",
  };
  return labels[value] || value.replaceAll("_", " ");
};

function ProductImage({ view, eager = false }: { view: ProductView; eager?: boolean }) {
  if (!view.primaryImageUrl) return <div className="constructor-image-fallback">Фото товара недоступно</div>;
  return <RemoteImage src={view.primaryImageUrl} alt={`${view.name}, ${view.collection}`} loading={eager ? "eager" : "lazy"} />;
}

export function ScenarioConstructor({ scenarioId }: { scenarioId: string }) {
  const [data, setData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [guests, setGuests] = useState(2);
  const [slots, setSlots] = useState<SlotState[]>([]);
  const [replacementKey, setReplacementKey] = useState<string | null>(null);
  const [galleryKey, setGalleryKey] = useState<string | null>(null);
  const [payload, setPayload] = useState<CartPayloadItem[] | null>(null);

  useEffect(() => {
    let active = true;
    loadConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Ошибка загрузки CSV"));
    trackConstructorEvent("constructor_opened", { scenario_id: scenarioId });
    return () => {
      active = false;
    };
  }, [scenarioId]);

  const presets = useMemo(
    () => (data?.presets ?? []).filter((row) => row.scenario_id === scenarioId).sort((a, b) => Number(a.sort_order) - Number(b.sort_order)),
    [data, scenarioId],
  );

  const indexes = useMemo(() => (data ? createIndexes(data) : null), [data]);

  useEffect(() => {
    if (!presets.length) return;
    const first = presets[0];
    setGuests(first.domain === "table" ? Number(first.default_guests) || 2 : 1);
    setSlots(
      presets.map((preset) => ({
        key: `${preset.scenario_id}:${preset.sort_order}:${preset.offer_id}`,
        enabled: preset.preset_status !== "optional",
      })),
    );
    setReplacementKey(null);
    setGalleryKey(null);
    setPayload(null);
  }, [scenarioId, presets.length]);

  const presetByKey = useMemo(() => {
    const map = new Map<string, PresetRow>();
    presets.forEach((preset) => map.set(`${preset.scenario_id}:${preset.sort_order}:${preset.offer_id}`, preset));
    return map;
  }, [presets]);

  const views = useMemo(() => {
    if (!indexes) return [];
    return slots
      .map((slot) => {
        const preset = presetByKey.get(slot.key);
        return preset ? deriveProductView(preset, slot, guests, indexes) : null;
      })
      .filter((view): view is ProductView => Boolean(view));
  }, [guests, indexes, presetByKey, slots]);

  const meta = useMemo(() => (data?.scenarios ?? []).filter((row) => row.scenario_id === scenarioId), [data, scenarioId]);
  const firstPreset = presets[0];
  const summary = calculateSummary(views);
  const blockers = getBlockingReasons(views);
  const galleryView = galleryKey ? views.find((view) => view.key === galleryKey) : undefined;
  const replacementView = replacementKey ? views.find((view) => view.key === replacementKey) : undefined;
  const replacementPreset = replacementKey ? presetByKey.get(replacementKey) : undefined;
  const replacementCandidates = replacementView && replacementPreset && data
    ? getReplacementCandidates(scenarioId, replacementPreset.product_type, replacementView.offerId, data)
    : [];

  if (error) {
    return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Не удалось загрузить сценарий</h1><p>{error}</p></div></main>;
  }

  if (!data || !indexes) {
    return <main className="constructor-shell"><div className="constructor-wrap constructor-empty">Загружаем сценарий…</div></main>;
  }

  if (!firstPreset) {
    return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Сценарий не найден</h1><Link href="/constructor/">Вернуться к сценариям</Link></div></main>;
  }

  const description = Array.from(new Set(meta.map((row) => row.styling_message).filter(Boolean))).join(". ") || firstPreset.selection_reason;
  const isTable = firstPreset.domain === "table";

  const updateSlot = (key: string, patch: Partial<SlotState>) => {
    setSlots((current) => current.map((slot) => (slot.key === key ? { ...slot, ...patch } : slot)));
    setPayload(null);
  };

  const addAll = () => {
    const currentBlockers = getBlockingReasons(views);
    if (currentBlockers.length) return;
    const nextPayload = buildCartPayload(views);
    console.log("ADD_ALL_TO_CART", nextPayload);
    setPayload(nextPayload);
    trackConstructorEvent("add_all_to_cart_clicked", { scenario_id: scenarioId, payload: nextPayload });
    trackConstructorEvent("add_all_to_cart_success", { scenario_id: scenarioId, items: nextPayload.length });
  };

  return (
    <main className="constructor-shell">
      <div className="constructor-wrap">
        <Link className="constructor-back" href="/constructor/">← ВСЕ СЦЕНАРИИ</Link>

        <header className="constructor-page-head">
          <div>
            <p className="constructor-kicker">{isTable ? "СЕРВИРОВКА" : "СПАЛЬНЯ"}</p>
            <h1 className="constructor-title">{meta[0]?.scenario_name || firstPreset.scenario_name}</h1>
            <p className="constructor-lead">{description}</p>
          </div>
          {isTable && (
            <div className="constructor-guests">
              <p>КОЛИЧЕСТВО ПЕРСОН</p>
              <div className="constructor-guest-buttons" role="group" aria-label="Количество персон">
                {GUEST_OPTIONS.map((value) => (
                  <button
                    key={value}
                    type="button"
                    className={guests === value ? "active" : ""}
                    aria-pressed={guests === value}
                    onClick={() => {
                      setGuests(value);
                      setPayload(null);
                      trackConstructorEvent("guest_count_changed", { scenario_id: scenarioId, guests: value });
                    }}
                  >
                    {value}
                  </button>
                ))}
              </div>
            </div>
          )}
        </header>

        <div className="constructor-layout">
          <div>
            <section className="constructor-hero-collage" aria-label="Предметы сценария">
              {views.filter((view) => view.enabled).slice(0, 5).map((view, index) => (
                <button key={view.key} type="button" onClick={() => setGalleryKey(view.key)} aria-label={`Открыть фотографии ${view.name}`}>
                  <ProductImage view={view} eager={index < 4} />
                </button>
              ))}
            </section>

            <section>
              <header className="constructor-section-head">
                <div>
                  <p className="constructor-kicker">СОСТАВ</p>
                  <h2>Настройте образ</h2>
                </div>
                <span>Обязательные позиции нельзя отключить. Default можно убрать, optional — добавить. Замены показываются только внутри того же типа товара.</span>
              </header>

              <div className="constructor-products">
                {views.map((view) => {
                  const preset = presetByKey.get(view.key)!;
                  const slot = slots.find((item) => item.key === view.key)!;
                  const variants = getVariantOptions(preset, slot, indexes);
                  const replacements = getReplacementCandidates(scenarioId, preset.product_type, view.offerId, data);
                  const priceMissing = !view.price && !(view.variantRequired && !view.variantSelected);
                  const unavailable = isUnavailable(view.availabilityStatus);

                  return (
                    <article className={`constructor-product ${view.enabled ? "" : "is-off"}`} key={view.key}>
                      <div className="constructor-product-media">
                        <button type="button" onClick={() => setGalleryKey(view.key)} aria-label={`Галерея ${view.name}`}>
                          <ProductImage view={view} />
                        </button>
                        <div className="constructor-product-badges">
                          <span className="constructor-chip">{humanProductType(view.productType)}</span>
                          {view.status === "required" && <span className="constructor-chip required">ОБЯЗАТЕЛЬНО</span>}
                        </div>
                        {view.status !== "required" && (
                          <button
                            className={`constructor-toggle ${view.enabled ? "active" : ""}`}
                            type="button"
                            aria-pressed={view.enabled}
                            onClick={() => {
                              updateSlot(view.key, { enabled: !view.enabled });
                              trackConstructorEvent("item_toggled", { scenario_id: scenarioId, offer_id: view.offerId, enabled: !view.enabled });
                            }}
                          >
                            {view.enabled ? "✓ В НАБОРЕ" : "+ ДОБАВИТЬ"}
                          </button>
                        )}
                      </div>

                      <div className="constructor-product-copy">
                        <p>{view.collection || "КУЛЬТУРА ДОМА"}</p>
                        <h3>{view.name}</h3>
                        <div className="constructor-product-facts">
                          {view.color && <span>Цвет: {view.color}</span>}
                          {view.material && <span>{view.material}</span>}
                          {view.size && <span>{view.size}</span>}
                          <span>{view.quantity} шт.</span>
                        </div>

                        {view.variantRequired && (
                          <div className="constructor-variant">
                            <label htmlFor={`variant-${view.key}`}>ВЫБЕРИТЕ РАЗМЕР</label>
                            <select
                              id={`variant-${view.key}`}
                              value={view.variantSelected ? view.offerId : ""}
                              onChange={(event) => {
                                updateSlot(view.key, { selectedVariantOfferId: event.target.value || undefined, enabled: true });
                                if (event.target.value) trackConstructorEvent("variant_selected", { scenario_id: scenarioId, offer_id: event.target.value });
                              }}
                            >
                              <option value="">Размер не выбран</option>
                              {variants.map((variant) => {
                                const variantPrice = toNumber(variant.price);
                                return (
                                  <option key={variant.offer_id} value={variant.offer_id} disabled={isUnavailable(variant.availability_status) || !variantPrice}>
                                    {variant.size || variant.product_name} · {variantPrice ? formatRub(variantPrice) : "Цена уточняется"}{isUnavailable(variant.availability_status) ? " · Нет в наличии" : ""}
                                  </option>
                                );
                              })}
                            </select>
                            {!view.variantSelected && <p className="constructor-warning">Без выбора размера сценарий нельзя добавить в корзину.</p>}
                          </div>
                        )}

                        <div className="constructor-price-row">
                          <div className="constructor-price">
                            {view.variantRequired && !view.variantSelected ? (
                              <><span>{view.displayPrice ? `от ${formatRub(view.displayPrice)}` : "Цена уточняется"}</span><small>В итог попадёт после выбора размера</small></>
                            ) : view.price ? (
                              <><span>{formatRub(view.price)}</span>{view.oldPrice && <del>{formatRub(view.oldPrice)}</del>}</>
                            ) : (
                              <><span>Цена уточняется</span><small>Позиция не войдёт в корзину</small></>
                            )}
                          </div>
                          <div className="constructor-actions">
                            {replacements.length > 0 && <button type="button" onClick={() => setReplacementKey(view.key)}>ЗАМЕНИТЬ ТОВАР</button>}
                            {view.productUrl && <a href={view.productUrl} target="_blank" rel="noreferrer">КАРТОЧКА ТОВАРА ↗</a>}
                          </div>
                        </div>
                        {priceMissing && <p className="constructor-warning">Цена не получена: выберите другую позицию или дождитесь обновления данных.</p>}
                        {unavailable && <p className="constructor-warning">Нет в наличии. {view.status === "required" ? "Выберите совместимую замену." : "Замените или отключите позицию."}</p>}
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          </div>

          <aside className="constructor-summary" aria-label="Итог сценария">
            <p>ВАШ СЦЕНАРИЙ</p>
            <h2>Состав набора</h2>
            <div className="constructor-summary-list">
              {views.filter((view) => view.enabled).map((view) => (
                <div className="constructor-summary-item" key={view.key}>
                  <div>{view.primaryImageUrl ? <RemoteImage src={view.primaryImageUrl} alt={`${view.name}, ${view.collection}`} loading="lazy" /> : <div className="constructor-image-fallback" />}</div>
                  <div><strong>{view.name}</strong><span>{view.variantRequired && !view.variantSelected ? "Выберите размер" : `${view.quantity} шт.${view.size ? ` · ${view.size}` : ""}`}</span></div>
                  <b>{view.price && !isUnavailable(view.availabilityStatus) ? formatRub(view.price * view.quantity) : "—"}</b>
                </div>
              ))}
            </div>
            <div className="constructor-summary-total">
              <div><span>ИТОГО</span><strong>{formatRub(summary.total)}</strong></div>
              <small>{summary.positions} поз. · {summary.units} шт.</small>
              {summary.savings > 0 && <small className="constructor-saving">Выгода {formatRub(summary.savings)}</small>}
              {blockers.length > 0 && <div className="constructor-blockers">{blockers.map((reason) => <div key={reason}>{reason}</div>)}</div>}
              <button className="constructor-primary" type="button" disabled={blockers.length > 0} onClick={addAll}>
                {blockers.some((reason) => reason.startsWith("Выберите размер")) ? "ВЫБЕРИТЕ РАЗМЕР" : blockers.length ? "ПРОВЕРЬТЕ СОСТАВ" : "ДОБАВИТЬ ВСЁ В КОРЗИНУ"}
              </button>
            </div>
          </aside>
        </div>
      </div>

      <ReplacementDrawer
        open={Boolean(replacementKey)}
        source={replacementView}
        candidates={replacementCandidates}
        catalog={data.catalog}
        onClose={() => setReplacementKey(null)}
        onChoose={(candidate) => {
          if (!replacementKey) return;
          updateSlot(replacementKey, { replacementOfferId: String(candidate.offer_id), selectedVariantOfferId: undefined, enabled: true });
          setReplacementKey(null);
          trackConstructorEvent("item_replaced", { scenario_id: scenarioId, offer_id: candidate.offer_id, product_type: candidate.product_type });
        }}
      />

      <GalleryModal view={galleryView} onClose={() => setGalleryKey(null)} />
      <PayloadModal payload={payload} onClose={() => setPayload(null)} />
    </main>
  );
}

function ReplacementDrawer({
  open,
  source,
  candidates,
  catalog,
  onClose,
  onChoose,
}: {
  open: boolean;
  source?: ProductView;
  candidates: CandidateRow[];
  catalog: CatalogRow[];
  onClose: () => void;
  onChoose: (candidate: CandidateRow) => void;
}) {
  useEffect(() => {
    if (!open) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const keydown = (event: KeyboardEvent) => event.key === "Escape" && onClose();
    document.addEventListener("keydown", keydown);
    return () => {
      document.body.style.overflow = previous;
      document.removeEventListener("keydown", keydown);
    };
  }, [open, onClose]);

  if (!open || !source) return null;
  const catalogByOffer = new Map(catalog.map((row) => [String(row.offer_id), row]));

  return (
    <div className="constructor-overlay" role="dialog" aria-modal="true" aria-label={`Заменить ${source.name}`}>
      <button className="constructor-overlay-bg" type="button" onClick={onClose} aria-label="Закрыть окно замен" />
      <aside className="constructor-drawer constructor-panel-content">
        <header className="constructor-panel-head">
          <div><p className="constructor-kicker">СОВМЕСТИМЫЕ ЗАМЕНЫ</p><h2>{humanProductType(source.productType)}</h2></div>
          <button className="constructor-panel-close" type="button" onClick={onClose} aria-label="Закрыть">×</button>
        </header>
        <div className="constructor-candidates">
          {candidates.length === 0 && <div className="constructor-empty">Для этого типа товара нет разрешённых замен.</div>}
          {candidates.map((candidate) => {
            const master = catalogByOffer.get(String(candidate.offer_id));
            const price = toNumber(master?.price || candidate.price_rub);
            const oldPrice = toNumber(master?.old_price || candidate.old_price_rub);
            const image = master?.primary_image_url || candidate.primary_image_url;
            const unavailable = isUnavailable(master?.availability_status);
            return (
              <article className="constructor-candidate" key={candidate.offer_id}>
                <div>{image ? <RemoteImage src={image} alt={`${master?.product_name || candidate.product_name}, ${master?.collection || candidate.collection}`} loading="lazy" /> : <div className="constructor-image-fallback" />}</div>
                <div>
                  <p>{master?.collection || candidate.collection || "КУЛЬТУРА ДОМА"}</p>
                  <h3>{master?.product_name || candidate.product_name}</h3>
                  <span>{master?.material || candidate.material}{(master?.size || candidate.size) ? ` · ${master?.size || candidate.size}` : ""}</span>
                  <strong>{price ? formatRub(price) : "Цена уточняется"}{oldPrice && price && oldPrice > price ? ` · ранее ${formatRub(oldPrice)}` : ""}</strong>
                  {unavailable && <span style={{ color: "#8b5d3c", marginTop: 5 }}>Нет в наличии</span>}
                  <div className="constructor-candidate-actions">
                    <button type="button" disabled={!price || unavailable} onClick={() => onChoose(candidate)}>{!price ? "ЦЕНА УТОЧНЯЕТСЯ" : unavailable ? "НЕТ В НАЛИЧИИ" : "ВЫБРАТЬ"}</button>
                    {(master?.product_url || candidate.product_url)?.startsWith("https://") && <a href={master?.product_url || candidate.product_url} target="_blank" rel="noreferrer">Открыть товар ↗</a>}
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      </aside>
    </div>
  );
}

function GalleryModal({ view, onClose }: { view?: ProductView; onClose: () => void }) {
  const [index, setIndex] = useState(0);
  useEffect(() => {
    if (!view) return;
    setIndex(0);
    const previous = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const keydown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
      if (event.key === "ArrowRight") setIndex((current) => Math.min(view.images.length - 1, current + 1));
      if (event.key === "ArrowLeft") setIndex((current) => Math.max(0, current - 1));
    };
    document.addEventListener("keydown", keydown);
    return () => {
      document.body.style.overflow = previous;
      document.removeEventListener("keydown", keydown);
    };
  }, [view, onClose]);

  if (!view) return null;
  const images = view.images.length ? view.images : [view.primaryImageUrl].filter(Boolean);

  return (
    <div className="constructor-overlay center" role="dialog" aria-modal="true" aria-label={`Галерея ${view.name}`}>
      <button className="constructor-overlay-bg" type="button" onClick={onClose} aria-label="Закрыть галерею" />
      <section className="constructor-modal constructor-panel-content">
        <header className="constructor-panel-head">
          <div><p className="constructor-kicker">{view.collection}</p><h2>{view.name}</h2></div>
          <button className="constructor-panel-close" type="button" onClick={onClose} aria-label="Закрыть">×</button>
        </header>
        <div className="constructor-gallery-body">
          <div className="constructor-gallery-main">{images[index] ? <RemoteImage src={images[index]} alt={`${view.name}, фото ${index + 1}`} loading="eager" /> : <div className="constructor-image-fallback" />}</div>
        </div>
        {images.length > 1 && <div className="constructor-gallery-thumbs">{images.map((image, imageIndex) => <button type="button" className={index === imageIndex ? "active" : ""} key={`${image}-${imageIndex}`} onClick={() => setIndex(imageIndex)} aria-label={`Фото ${imageIndex + 1}`}><RemoteImage src={image} alt={`${view.name}, миниатюра ${imageIndex + 1}`} loading="lazy" /></button>)}</div>}
      </section>
    </div>
  );
}

function PayloadModal({ payload, onClose }: { payload: CartPayloadItem[] | null; onClose: () => void }) {
  useEffect(() => {
    if (!payload) return;
    const keydown = (event: KeyboardEvent) => event.key === "Escape" && onClose();
    document.addEventListener("keydown", keydown);
    return () => document.removeEventListener("keydown", keydown);
  }, [payload, onClose]);

  if (!payload) return null;
  return (
    <div className="constructor-overlay center" role="dialog" aria-modal="true" aria-label="Payload корзины">
      <button className="constructor-overlay-bg" type="button" onClick={onClose} aria-label="Закрыть" />
      <section className="constructor-modal constructor-panel-content" style={{ maxWidth: 620 }}>
        <header className="constructor-panel-head">
          <div><p className="constructor-kicker">MVP КОРЗИНА</p><h2>Сценарий готов</h2></div>
          <button className="constructor-panel-close" type="button" onClick={onClose} aria-label="Закрыть">×</button>
        </header>
        <div className="constructor-json">
          <p>Массив также выведен в console.log с меткой <code>ADD_ALL_TO_CART</code>.</p>
          <pre>{JSON.stringify(payload, null, 2)}</pre>
        </div>
      </section>
    </div>
  );
}
