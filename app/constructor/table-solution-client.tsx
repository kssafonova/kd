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
  recommendedOptionQuantity,
  type SolutionProductOption,
} from "./table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "./types";

const CART_STORAGE_KEY = "kultura-cart";
const CART_ID_OFFSET = 920000;
const formatRub = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const toPrice = (value: string | undefined) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const normalize = (value: string) => String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/[«»"']/g, "").replace(/\s+/g, " ");

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
  const [selectedOptions, setSelectedOptions] = useState<Record<string, boolean>>({});
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
  const allOptions = useMemo(() => categories.flatMap((category) => category.slots.flatMap((slot) => slot.options)), [categories]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, ruleData) : [1, 2], [solution, ruleData]);

  const defaultSelected = useMemo(() => {
    const selected = new Set<string>();
    if (!solution) return selected;
    const explicitTargets = solution.productNames.map(normalize).filter(Boolean);
    categories.forEach((category) => {
      const options = category.slots.flatMap((slot) => slot.options);
      const explicit = options.filter((option) => explicitTargets.some((target) => {
        const title = normalize(option.title);
        return title === target || title.includes(target) || target.includes(title);
      }));
      if (explicit.length) {
        explicit.forEach((option) => selected.add(option.id));
        return;
      }
      // Ready solution starts with one sensible product in core categories.
      if (!["atmosphere", "vases", "games", "other"].includes(category.id) && options[0]) selected.add(options[0].id);
    });
    return selected;
  }, [categories, solution]);

  useEffect(() => {
    if (guestOptions.length && !guestOptions.includes(guests)) setGuests(guestOptions[0]);
  }, [guestOptions, guests]);

  useEffect(() => {
    setSelectedOptions({});
    setColorChoice({});
    setSizeChoice({});
    setQuantity({});
  }, [scenarioId]);

  if (!solution) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;
  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;

  const isOptionSelected = (option: SolutionProductOption) => selectedOptions[option.id] ?? defaultSelected.has(option.id);
  const selectedRow = (option: SolutionProductOption) => {
    const colors = optionColors(option);
    const color = colorChoice[option.id] || colors[0] || "";
    const sizes = optionSizes(option, color);
    const size = sizeChoice[option.id] || sizes[0] || "";
    return pickOptionVariant(option, color, size);
  };
  const optionQuantity = (option: SolutionProductOption) => quantity[option.id] ?? recommendedOptionQuantity(option, guests);

  const activeSelections = allOptions
    .filter(isOptionSelected)
    .map((option) => ({ option, row: selectedRow(option), quantity: optionQuantity(option) }))
    .filter((item): item is { option: SolutionProductOption; row: CatalogRow; quantity: number } => Boolean(item.row));

  const totalUnits = activeSelections.reduce((sum, item) => sum + item.quantity, 0);
  const total = activeSelections.reduce((sum, item) => sum + toPrice(item.row.price) * item.quantity, 0);
  const selectedCategoryCount = categories.filter((category) => category.slots.some((slot) => slot.options.some(isOptionSelected))).length;

  const previewFallback = catalogRows[0]?.primary_image_url || "/images/image-placeholder.svg";
  const scrollFallback = catalogRows[1]?.primary_image_url || catalogRows[0]?.all_image_urls?.split("|")[1] || previewFallback;
  const previewSrc = solution.previewFile ? `/images/constructor/${solution.previewFile}` : previewFallback;
  const scrollSrc = solution.scrollFile ? `/images/constructor/${solution.scrollFile}` : scrollFallback;

  const toggleOption = (option: SolutionProductOption) => {
    const next = !isOptionSelected(option);
    setSelectedOptions((state) => ({ ...state, [option.id]: next }));
  };

  const toggleCategory = (options: SolutionProductOption[]) => {
    const allSelected = options.every(isOptionSelected);
    setSelectedOptions((state) => ({
      ...state,
      ...Object.fromEntries(options.map((option) => [option.id, !allSelected])),
    }));
  };

  const addSolution = () => {
    const items: SharedCartItem[] = activeSelections.map(({ option, row, quantity: itemQty }, index) => {
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
        name: option.title,
        note: `Из готового решения «${solution.name}» · ${option.collection || "Культура Дома"} · ${guests} персон`,
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
    <main className="solution-simple-shell table-solution-detail-shell table-builder-v28">
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
            <p>Соберите решение по понятным товарным группам. В каждой группе можно выбрать несколько товаров из разных коллекций, а цвет и размер настроить внутри одной карточки.</p>
            <div className="table-solution-hero-total"><span>{activeSelections.length} товаров · {totalUnits} шт.</span><strong>{formatRub(total)}</strong></div>
          </div>
        </section>

        {catalogRows.length === 0 ? (
          <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены в CSV</h2><p>Для этого решения не удалось найти позиции по указанным коллекциям или названиям.</p></div></section>
        ) : (
          <>
            <section className="table-builder-config table-builder-config-v28" aria-label="Настройка готового решения">
              <div className="table-builder-step table-builder-step-v28">
                <div className="table-builder-step-number">01</div>
                <div className="table-builder-step-copy"><small>КОЛИЧЕСТВО ПЕРСОН</small><h2>На сколько человек?</h2><p>Для тарелок, кружек, пар, бокалов, плейсматов и салфеток рекомендуемое количество пересчитывается автоматически.</p></div>
                <div className="table-builder-guests" role="group" aria-label="Количество персон">
                  {guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQuantity({}); }}><strong>{value}</strong><span>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</span></button>)}
                </div>
              </div>

              <div className="table-builder-step table-builder-step-v28">
                <div className="table-builder-step-number">02</div>
                <div className="table-builder-step-copy"><small>СОСТАВ РЕШЕНИЯ</small><h2>Выберите нужные группы</h2><p>Внутри каждой группы можно отметить несколько товаров. Коллекция больше не определяет структуру конструктора.</p></div>
                <nav className="table-builder-category-nav" aria-label="Группы товаров">
                  {categories.map((category) => {
                    const options = category.slots.flatMap((slot) => slot.options);
                    const selectedCount = options.filter(isOptionSelected).length;
                    return <a href={`#solution-category-${category.id}`} key={category.id}><span>{category.title}</span><b>{selectedCount}/{options.length}</b></a>;
                  })}
                </nav>
              </div>
            </section>

            <div className="table-solution-buy-layout table-builder-buy-layout table-builder-buy-layout-v28">
              <section className="table-builder-category-list table-builder-category-list-v28">
                {categories.map((category, categoryIndex) => {
                  const options = category.slots.flatMap((slot) => slot.options);
                  const selectedCount = options.filter(isOptionSelected).length;
                  const allSelected = selectedCount === options.length && options.length > 0;
                  return (
                    <section className="table-builder-category-v28" id={`solution-category-${category.id}`} key={category.id}>
                      <header className="table-builder-category-header-v28">
                        <div>
                          <small>{String(categoryIndex + 1).padStart(2, "0")} · ГРУППА</small>
                          <h2>{category.title}</h2>
                          <p>{category.description}</p>
                        </div>
                        <div className="table-builder-category-actions-v28">
                          <span>{selectedCount} из {options.length}</span>
                          <button type="button" onClick={() => toggleCategory(options)}>{allSelected ? "УБРАТЬ ВСЕ" : "ВЫБРАТЬ ВСЕ"}</button>
                        </div>
                      </header>

                      <div className="table-builder-multi-grid">
                        {options.map((option) => {
                          const checked = isOptionSelected(option);
                          const row = selectedRow(option) || option.variants[0];
                          const colors = optionColors(option);
                          const activeColor = colorChoice[option.id] || colors[0] || "";
                          const sizes = optionSizes(option, activeColor);
                          const activeSize = sizeChoice[option.id] || sizes[0] || "";
                          const q = optionQuantity(option);
                          return (
                            <article className={`table-builder-multi-card ${checked ? "selected" : ""}`} key={option.id}>
                              <button className="table-builder-multi-select" type="button" aria-pressed={checked} onClick={() => toggleOption(option)}>
                                <span className="table-builder-multi-check" aria-hidden="true">{checked ? "✓" : ""}</span>
                                <span>{checked ? "В РЕШЕНИИ" : "ДОБАВИТЬ"}</span>
                              </button>

                              <div className="table-builder-multi-media">
                                <RemoteImage src={row?.primary_image_url || "/images/image-placeholder.svg"} alt={option.title}/>
                              </div>

                              <div className="table-builder-multi-copy">
                                <small>{option.collection || "Культура Дома"}</small>
                                <h3>{option.title}</h3>
                                <strong>{toPrice(row?.price) ? formatRub(toPrice(row?.price)) : "Цена уточняется"}</strong>
                                {option.perPerson && <span className="table-builder-person-note">Рекомендуем {guests} шт. · по одной на персону</span>}
                              </div>

                              {checked && <div className="table-builder-multi-controls">
                                {colors.length > 1 && <div className="table-builder-control-row">
                                  <span>Цвет</span>
                                  <div className="table-builder-color-options">
                                    {colors.map((color) => <button type="button" key={color} className={activeColor === color ? "active" : ""} title={color} aria-label={`Цвет ${color}`} onClick={() => {
                                      setColorChoice((state) => ({ ...state, [option.id]: color }));
                                      setSizeChoice((state) => { const next = { ...state }; delete next[option.id]; return next; });
                                    }}><i style={{ background: colorCss(color) }}/><b>{color}</b></button>)}
                                  </div>
                                </div>}

                                {sizes.length > 1 && <div className="table-builder-control-row">
                                  <span>Размер</span>
                                  <div className="table-builder-size-options">
                                    {sizes.map((size) => <button type="button" key={size} className={activeSize === size ? "active" : ""} onClick={() => setSizeChoice((state) => ({ ...state, [option.id]: size }))}>{size}</button>)}
                                  </div>
                                </div>}

                                <div className="table-builder-control-row table-builder-qty-row">
                                  <span>Количество</span>
                                  <div className="table-builder-qty-control">
                                    <button type="button" aria-label="Уменьшить количество" onClick={() => setQuantity((state) => ({ ...state, [option.id]: Math.max(1, q - 1) }))}>−</button>
                                    <b>{q}</b>
                                    <button type="button" aria-label="Увеличить количество" onClick={() => setQuantity((state) => ({ ...state, [option.id]: q + 1 }))}>+</button>
                                  </div>
                                </div>
                              </div>}
                            </article>
                          );
                        })}
                      </div>
                    </section>
                  );
                })}
              </section>

              <aside className="table-solution-summary table-builder-summary table-builder-summary-v28">
                <small>ВАШЕ РЕШЕНИЕ</small>
                <h2>{solution.name}</h2>
                <div className="table-builder-summary-meta-v28">
                  <div><span>Персон</span><b>{guests}</b></div>
                  <div><span>Групп</span><b>{selectedCategoryCount}</b></div>
                  <div><span>Товаров</span><b>{activeSelections.length}</b></div>
                  <div><span>Единиц</span><b>{totalUnits}</b></div>
                </div>
                <div className="table-builder-summary-lines-v28">
                  {activeSelections.slice(0, 8).map(({ option, row, quantity: itemQty }) => <div key={option.id}><span>{option.title}<small>{row.color ? ` · ${row.color}` : ""}</small></span><b>{itemQty} × {formatRub(toPrice(row.price))}</b></div>)}
                  {activeSelections.length > 8 && <p>+ ещё {activeSelections.length - 8} товаров</p>}
                </div>
                <div className="table-solution-summary-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong></div>
                <button type="button" className="table-solution-add-all" disabled={!activeSelections.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : `ДОБАВИТЬ В КОРЗИНУ · ${activeSelections.length}`}</button>
                <p className="table-builder-summary-help-v28">Все выбранные товары попадут в корзину отдельными позициями с выбранными цветами, размерами и количеством.</p>
              </aside>
            </div>
          </>
        )}
      </div>

      {activeSelections.length > 0 && <div className="table-builder-mobile-bar-v28">
        <div><span>{activeSelections.length} товаров · {totalUnits} шт.</span><strong>{formatRub(total)}</strong></div>
        <button type="button" disabled={redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "В КОРЗИНУ"}</button>
      </div>}
    </main>
  );
}
