"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { findTableSolution } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedSlotQuantity,
  type SolutionProductOption,
  type SolutionSlot,
} from "./table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "./types";

const CART_STORAGE_KEY = "kultura-cart";
const CART_ID_OFFSET = 920000;
const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;

const splitImages = (row?: CatalogRow) => Array.from(new Set([
  row?.primary_image_url,
  ...(row?.all_image_urls || "").split("|"),
].filter((value): value is string => Boolean(value))));

const colorCss = (value: string) => {
  const color = value.toLocaleLowerCase("ru-RU");
  if (color.includes("бел") || color.includes("молоч") || color.includes("айвори")) return "#f1efe8";
  if (color.includes("черн")) return "#181818";
  if (color.includes("темно-син") || color.includes("ночн")) return "#24364a";
  if (color.includes("син")) return "#49657b";
  if (color.includes("голуб")) return "#9db8c7";
  if (color.includes("зелен")) return "#56735d";
  if (color.includes("красн") || color.includes("бордо")) return "#8f3c39";
  if (color.includes("роз") || color.includes("пудр")) return "#d5aaa7";
  if (color.includes("беж") || color.includes("льнян") || color.includes("песоч")) return "#c7b59d";
  if (color.includes("сер")) return "#9b9b96";
  if (color.includes("золот")) return "#b99a5f";
  return "#d8d5cf";
};

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
    if (raw) existing = JSON.parse(raw) as SharedCartItem[];
  } catch { existing = []; }

  const merged = [...existing];
  items.forEach((item) => {
    const index = merged.findIndex((entry) => entry.id === item.id && entry.selectedSize === item.selectedSize && entry.selectedColor === item.selectedColor);
    if (index >= 0) merged[index] = { ...merged[index], quantity: merged[index].quantity + item.quantity };
    else merged.push(item);
  });
  try { localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(merged)); } catch {}
};

export function TableSolutionDetail({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [ruleData, setRuleData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [guests, setGuests] = useState(2);
  const [enabledSlots, setEnabledSlots] = useState<Record<string, boolean>>({});
  const [optionChoice, setOptionChoice] = useState<Record<string, string>>({});
  const [colorChoice, setColorChoice] = useState<Record<string, string>>({});
  const [sizeChoice, setSizeChoice] = useState<Record<string, string>>({});
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [redirecting, setRedirecting] = useState(false);

  useEffect(() => {
    let active = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([loaded, rules]) => {
        if (!active) return;
        setData(loaded);
        setRuleData(rules);
      })
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решение"));
    return () => { active = false; };
  }, []);

  const catalogRows = useMemo(() => {
    if (!data || !solution) return [];
    return resolveTableSolutionCatalogRows(data.catalog, solution);
  }, [data, solution]);

  const categories = useMemo(() => solution ? buildSolutionCategories(catalogRows, solution.space) : [], [catalogRows, solution]);
  const allSlots = useMemo(() => categories.flatMap((category) => category.slots), [categories]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, ruleData) : [1, 2], [solution, ruleData]);

  useEffect(() => {
    if (guestOptions.length && !guestOptions.includes(guests)) setGuests(guestOptions[0]);
  }, [guestOptions, guests]);

  useEffect(() => {
    setEnabledSlots({});
    setOptionChoice({});
    setColorChoice({});
    setSizeChoice({});
    setQuantity({});
  }, [scenarioId]);

  if (!solution) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;
  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;

  const isSlotEnabled = (slot: SolutionSlot) => enabledSlots[slot.id] !== false;
  const selectedOption = (slot: SolutionSlot) => slot.options.find((option) => option.id === optionChoice[slot.id]) || slot.options[0];
  const selectedRow = (slot: SolutionSlot) => {
    const option = selectedOption(slot);
    if (!option) return undefined;
    const colors = optionColors(option);
    const color = colorChoice[option.id] || colors[0] || "";
    const sizes = optionSizes(option, color);
    const size = sizeChoice[option.id] || sizes[0] || "";
    return pickOptionVariant(option, color, size);
  };
  const slotQuantity = (slot: SolutionSlot) => quantity[slot.id] ?? recommendedSlotQuantity(slot, guests);

  const activeSelections = allSlots
    .filter(isSlotEnabled)
    .map((slot) => ({ slot, option: selectedOption(slot), row: selectedRow(slot), quantity: slotQuantity(slot) }))
    .filter((item): item is { slot: SolutionSlot; option: SolutionProductOption; row: CatalogRow; quantity: number } => Boolean(item.option && item.row));

  const totalUnits = activeSelections.reduce((sum, item) => sum + item.quantity, 0);
  const total = activeSelections.reduce((sum, item) => sum + toPrice(item.row.price) * item.quantity, 0);
  const previewFallback = catalogRows[0]?.primary_image_url || "/images/image-placeholder.svg";
  const scrollFallback = catalogRows[1]?.primary_image_url || catalogRows[0]?.all_image_urls?.split("|")[1] || previewFallback;
  const previewSrc = solution.previewFile ? `/images/constructor/${solution.previewFile}` : previewFallback;
  const scrollSrc = solution.scrollFile ? `/images/constructor/${solution.scrollFile}` : scrollFallback;

  const chooseOption = (slot: SolutionSlot, option: SolutionProductOption) => {
    setOptionChoice((state) => ({ ...state, [slot.id]: option.id }));
    setEnabledSlots((state) => ({ ...state, [slot.id]: true }));
    setQuantity((state) => { const next = { ...state }; delete next[slot.id]; return next; });
  };

  const addSolution = () => {
    const items: SharedCartItem[] = activeSelections.map(({ slot, option, row, quantity: itemQty }, index) => {
      const numericOffer = Number(String(row.offer_id).split("-")[0]) || index + 1;
      const productId = CART_ID_OFFSET + numericOffer;
      const skuId = `table-solution-${solution.sourceId}-${row.offer_id}`;
      const image = row.primary_image_url || "/images/image-placeholder.svg";
      const gallery = splitImages(row);
      const size = row.size || row.volume || "Стандартный";
      const price = toPrice(row.price);
      const skus = option.variants.map((variant, variantIndex) => {
        const variantNumeric = Number(String(variant.offer_id).split("-")[0]) || numericOffer + variantIndex;
        const variantProductId = CART_ID_OFFSET + variantNumeric;
        const variantImage = variant.primary_image_url || image;
        return {
          id: `table-solution-${solution.sourceId}-${variant.offer_id}`,
          article: variant.vendor_code || String(variant.offer_id),
          productId: variantProductId,
          color: variant.color || "",
          colorHex: colorCss(variant.color || ""),
          size: variant.size || variant.volume || "Стандартный",
          material: variant.material || "",
          composition: "",
          price: toPrice(variant.price),
          image: variantImage,
          gallery: splitImages(variant),
        };
      });
      return {
        id: productId,
        name: row.product_name,
        note: `Из готового решения «${solution.name}» · ${slot.title} · ${guests} персон`,
        price,
        image,
        gallery,
        selectedColor: row.color || "",
        selectedSize: size,
        selectedSkuId: skuId,
        quantity: itemQty,
        skus,
      };
    });

    if (!items.length) return;
    mergeIntoSharedCart(items);
    setRedirecting(true);
    window.setTimeout(() => {
      const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
      window.location.href = `${base}/?cart=open`;
    }, 450);
  };

  return (
    <main className="solution-simple-shell table-solution-detail-shell table-builder-v27">
      <div className="solution-simple-wrap">
        <nav className="solution-simple-topbar">
          <Link href="/constructor/">← ГОТОВЫЕ РЕШЕНИЯ</Link>
          <span>{solution.space}</span>
        </nav>

        <section className="table-solution-detail-hero">
          <div className="table-solution-hero-media">
            <RemoteImage src={previewSrc} fallbackSrc={previewFallback} alt={`${solution.name}: превью`} loading="eager"/>
            <RemoteImage src={scrollSrc} fallbackSrc={scrollFallback} alt={`${solution.name}: второй кадр`} loading="eager"/>
          </div>
          <div className="table-solution-hero-copy">
            <small>ГОТОВОЕ РЕШЕНИЕ · {solution.space.toUpperCase()}</small>
            <h1>{solution.name}</h1>
            {solution.collections.length > 0 && <div className="table-solution-collection-list">{solution.collections.map((collection) => <span key={collection}>{collection}</span>)}</div>}
            <p>Соберите решение по типам товаров: сначала выберите, какие предметы нужны, затем сравните варианты из разных коллекций и настройте цвет, размер и количество.</p>
            <div className="table-solution-hero-total"><span>{activeSelections.length} позиций · {totalUnits} шт.</span><strong>{formatRub(total)}</strong></div>
          </div>
        </section>

        {catalogRows.length === 0 ? (
          <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены в CSV</h2><p>Для этого решения не удалось найти позиции по указанным коллекциям или названиям.</p></div></section>
        ) : (
          <>
            <section className="table-builder-config table-builder-config-v27" aria-label="Настройка готового решения">
              <div className="table-builder-step table-builder-step-v27">
                <div className="table-builder-step-number">01</div>
                <div className="table-builder-step-copy"><small>КОЛИЧЕСТВО ПЕРСОН</small><h2>На сколько человек?</h2><p>Количество тарелок, пар, бокалов, плейсматов и других индивидуальных предметов пересчитывается автоматически.</p></div>
                <div className="table-builder-guests" role="group" aria-label="Количество персон">
                  {guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQuantity({}); }}><strong>{value}</strong><span>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</span></button>)}
                </div>
              </div>
              <div className="table-builder-step table-builder-step-v27">
                <div className="table-builder-step-number">02</div>
                <div className="table-builder-step-copy"><small>КОНСТРУКТОР</small><h2>Выберите категории</h2><p>Товары сгруппированы по типу, а не по коллекции. Например, все тарелки находятся вместе, все корзины — вместе.</p></div>
                <nav className="table-builder-category-nav" aria-label="Категории решения">
                  {categories.map((category) => <a href={`#solution-category-${category.id}`} key={category.id}><span>{category.title}</span><b>{category.slots.length}</b></a>)}
                </nav>
              </div>
            </section>

            <div className="table-solution-buy-layout table-builder-buy-layout table-builder-buy-layout-v27">
              <section className="table-builder-category-list">
                {categories.map((category, categoryIndex) => (
                  <section className="table-builder-category-v27" id={`solution-category-${category.id}`} key={category.id}>
                    <header className="table-builder-category-header-v27">
                      <div><small>{String(categoryIndex + 1).padStart(2, "0")} · КАТЕГОРИЯ</small><h2>{category.title}</h2><p>{category.description}</p></div>
                      <span>{category.slots.length} {category.slots.length === 1 ? "тип" : "типа"}</span>
                    </header>

                    <div className="table-builder-slot-list">
                      {category.slots.map((slot) => {
                        const enabled = isSlotEnabled(slot);
                        const option = selectedOption(slot);
                        const row = selectedRow(slot);
                        const colors = option ? optionColors(option) : [];
                        const activeColor = option ? (colorChoice[option.id] || colors[0] || "") : "";
                        const sizes = option ? optionSizes(option, activeColor) : [];
                        const activeSize = option ? (sizeChoice[option.id] || sizes[0] || "") : "";
                        const q = slotQuantity(slot);
                        return (
                          <article className={`table-builder-slot ${enabled ? "enabled" : "disabled"}`} key={slot.id}>
                            <header className="table-builder-slot-header">
                              <label className="table-builder-slot-toggle">
                                <input type="checkbox" checked={enabled} onChange={(event) => setEnabledSlots((state) => ({ ...state, [slot.id]: event.target.checked }))}/>
                                <span/>
                              </label>
                              <div><h3>{slot.title}</h3><p>{slot.description}</p></div>
                              <div className="table-builder-slot-status"><small>{enabled ? "В РЕШЕНИИ" : "НЕ ДОБАВЛЯТЬ"}</small>{slot.perPerson && enabled && <b>{q} шт. на {guests} персон</b>}</div>
                            </header>

                            {enabled && option && row && <div className="table-builder-slot-body">
                              <div className="table-builder-option-grid" role="radiogroup" aria-label={`Выбор: ${slot.title}`}>
                                {slot.options.map((candidate) => {
                                  const candidateSelected = candidate.id === option.id;
                                  const candidateRow = candidateSelected ? row : candidate.variants[0];
                                  return <button type="button" role="radio" aria-checked={candidateSelected} className={candidateSelected ? "active" : ""} key={candidate.id} onClick={() => chooseOption(slot, candidate)}>
                                    <span className="table-builder-option-media"><RemoteImage src={candidateRow?.primary_image_url || "/images/image-placeholder.svg"} alt={candidate.title}/></span>
                                    <span className="table-builder-option-copy"><small>{candidate.collection}</small><strong>{candidate.title}</strong><b>{toPrice(candidateRow?.price) ? formatRub(toPrice(candidateRow?.price)) : "Цена уточняется"}</b></span>
                                    <i aria-hidden="true"/>
                                  </button>;
                                })}
                              </div>

                              <div className="table-builder-variant-panel">
                                {colors.length > 1 && <div className="table-builder-variant-row"><span>Цвет</span><div className="table-builder-color-options">{colors.map((color) => <button type="button" className={activeColor === color ? "active" : ""} key={color} onClick={() => { setColorChoice((state) => ({ ...state, [option.id]: color })); setSizeChoice((state) => { const next = { ...state }; delete next[option.id]; return next; }); }}><i style={{ backgroundColor: colorCss(color) }}/><b>{color}</b></button>)}</div></div>}
                                {sizes.length > 1 && <div className="table-builder-variant-row"><span>Размер</span><div className="table-builder-size-options">{sizes.map((size) => <button type="button" className={activeSize === size ? "active" : ""} key={size} onClick={() => setSizeChoice((state) => ({ ...state, [option.id]: size }))}>{size}</button>)}</div></div>}
                                <div className="table-builder-variant-row table-builder-quantity-row"><span>Количество</span><div className="table-solution-qty"><button type="button" onClick={() => setQuantity((state) => ({ ...state, [slot.id]: Math.max(1, q - 1) }))}>−</button><span>{q}</span><button type="button" onClick={() => setQuantity((state) => ({ ...state, [slot.id]: q + 1 }))}>+</button></div>{slot.perPerson && <small>Рекомендовано: {guests} шт.</small>}</div>
                              </div>
                            </div>}
                          </article>
                        );
                      })}
                    </div>
                  </section>
                ))}
              </section>

              <aside className="table-solution-purchase-card table-builder-summary table-builder-summary-v27">
                <small>ВАШЕ РЕШЕНИЕ</small>
                <h2>{solution.name}</h2>
                <div><span>Персон</span><b>{guests}</b></div>
                <div><span>Категорий</span><b>{categories.length}</b></div>
                <div><span>Выбрано</span><b>{activeSelections.length} позиций · {totalUnits} шт.</b></div>
                <div className="table-solution-purchase-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong></div>
                <button type="button" disabled={!activeSelections.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ"}</button>
                <p>В корзину попадут выбранные товары с указанными цветами, размерами и количеством.</p>
              </aside>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
