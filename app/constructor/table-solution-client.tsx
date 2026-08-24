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
  const [openCategories, setOpenCategories] = useState<Record<string, boolean>>({});
  const [redirecting, setRedirecting] = useState(false);
  const [saved, setSaved] = useState(false);

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
    setOpenCategories({});
    setSaved(false);
  }, [scenarioId]);

  useEffect(() => {
    if (!categories.length) return;
    setOpenCategories((state) => Object.keys(state).length ? state : { [categories[0].id]: true });
  }, [categories]);

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
  const previewFallback = catalogRows[0]?.primary_image_url || "/images/image-placeholder.svg";
  const previewSrc = solution.previewFile ? `/images/constructor/${solution.previewFile}` : previewFallback;

  const toggleOption = (option: SolutionProductOption) => {
    const next = !isOptionSelected(option);
    setSelectedOptions((state) => ({ ...state, [option.id]: next }));
  };

  const toggleCategory = (options: SolutionProductOption[]) => {
    const allSelected = options.every(isOptionSelected);
    setSelectedOptions((state) => ({ ...state, ...Object.fromEntries(options.map((option) => [option.id, !allSelected])) }));
  };

  const saveSolution = () => {
    try {
      localStorage.setItem(`kultura-ready-solution-${scenarioId}`, JSON.stringify({ guests, selected: activeSelections.map(({ option, row, quantity: itemQty }) => ({ optionId: option.id, offerId: row.offer_id, quantity: itemQty })) }));
      setSaved(true);
    } catch {}
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
    <main className="solution-simple-shell kd-ready-v29">
      <div className="solution-simple-wrap kd-ready-wrap-v29">
        <nav className="kd-ready-breadcrumb-v29">
          <Link href="/constructor/">← Готовые решения</Link>
          <span>{solution.space}</span>
        </nav>

        <section className="kd-ready-hero-v29">
          <div className="kd-ready-hero-copy-v29">
            <small>{solution.name} · {solution.space}</small>
            <h1>ГОТОВЫЕ РЕШЕНИЯ</h1>
            <p>Соберите идеальное пространство за несколько кликов — выберите нужные предметы, цвет и количество.</p>
            {solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((collection) => <span key={collection}>{collection}</span>)}</div>}
          </div>
          <div className="kd-ready-hero-media-v29"><RemoteImage src={previewSrc} fallbackSrc={previewFallback} alt={solution.name} loading="eager"/></div>
        </section>

        <section className="kd-ready-guests-v29" aria-label="Количество персон">
          <span>Сколько персон будет за столом?</span>
          <div role="group">
            {guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQuantity({}); }}><b>{value}</b><em>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</em></button>)}
          </div>
        </section>

        {catalogRows.length === 0 ? (
          <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены в CSV</h2><p>Для этого решения не удалось найти позиции по указанным коллекциям или названиям.</p></div></section>
        ) : (
          <div className="kd-ready-commerce-v29">
            <section className="kd-ready-groups-v29">
              {categories.map((category) => {
                const options = category.slots.flatMap((slot) => slot.options);
                const selectedCount = options.filter(isOptionSelected).length;
                const allSelected = selectedCount === options.length && options.length > 0;
                const hasPerPerson = options.some((option) => option.perPerson);
                const isOpen = openCategories[category.id] ?? false;
                return (
                  <section className={`kd-ready-group-v29 ${isOpen ? "open" : "collapsed"}`} id={`solution-category-${category.id}`} key={category.id}>
                    <header className="kd-ready-group-header-v29">
                      <button className="kd-ready-group-toggle-v29" type="button" aria-expanded={isOpen} onClick={() => setOpenCategories((state) => ({ ...state, [category.id]: !isOpen }))}>
                        <span><h2>{category.title}</h2><small>{hasPerPerson ? `Рекомендуем ${guests} шт.` : `${selectedCount} выбрано`}</small></span>
                        <i aria-hidden="true">⌄</i>
                      </button>
                      <label className="kd-ready-select-all-v29"><input type="checkbox" checked={allSelected} onChange={() => toggleCategory(options)}/><span>Выбрать все</span></label>
                    </header>

                    <div className="kd-ready-group-body-v29">
                      <div className="kd-ready-products-v29">
                        {options.map((option) => {
                          const checked = isOptionSelected(option);
                          const row = selectedRow(option) || option.variants[0];
                          const colors = optionColors(option);
                          const activeColor = colorChoice[option.id] || colors[0] || "";
                          const sizes = optionSizes(option, activeColor);
                          const activeSize = sizeChoice[option.id] || sizes[0] || "";
                          const q = optionQuantity(option);
                          return (
                            <article className={`kd-ready-product-v29 ${checked ? "selected" : ""}`} key={option.id}>
                              <button type="button" className="kd-ready-product-check-v29" aria-pressed={checked} aria-label={checked ? `Убрать ${option.title}` : `Добавить ${option.title}`} onClick={() => toggleOption(option)}><span>{checked ? "✓" : ""}</span></button>
                              <div className="kd-ready-product-media-v29"><RemoteImage src={row?.primary_image_url || "/images/image-placeholder.svg"} alt={option.title}/></div>
                              <div className="kd-ready-product-copy-v29">
                                <small>{option.collection || "Культура Дома"}</small>
                                <h3>{option.title}</h3>
                                <strong>{toPrice(row?.price) ? formatRub(toPrice(row?.price)) : "Цена уточняется"}</strong>
                              </div>

                              {checked && <div className="kd-ready-product-controls-v29">
                                {colors.length > 1 && <div className="kd-ready-swatches-v29" aria-label="Цвет">
                                  {colors.map((color) => <button type="button" key={color} className={activeColor === color ? "active" : ""} title={color} aria-label={`Цвет ${color}`} onClick={() => {
                                    setColorChoice((state) => ({ ...state, [option.id]: color }));
                                    setSizeChoice((state) => { const next = { ...state }; delete next[option.id]; return next; });
                                  }}><i style={{ background: colorCss(color) }}/></button>)}
                                </div>}
                                {sizes.length > 1 && <select className="kd-ready-size-v29" value={activeSize} onChange={(event) => setSizeChoice((state) => ({ ...state, [option.id]: event.target.value }))} aria-label={`Размер ${option.title}`}>
                                  {sizes.map((size) => <option value={size} key={size}>{size}</option>)}
                                </select>}
                                <div className="kd-ready-qty-v29"><button type="button" aria-label="Уменьшить" onClick={() => setQuantity((state) => ({ ...state, [option.id]: Math.max(1, q - 1) }))}>−</button><b>{q}</b><button type="button" aria-label="Увеличить" onClick={() => setQuantity((state) => ({ ...state, [option.id]: q + 1 }))}>+</button></div>
                              </div>}
                            </article>
                          );
                        })}
                      </div>
                    </div>
                  </section>
                );
              })}
            </section>

            <aside className="kd-ready-summary-v29">
              <div className="kd-ready-summary-title-v29"><div><small>Ваше решение</small><h2>{solution.name}</h2></div><a href="#solution-category-${categories[0]?.id || ""}">Изменить</a></div>
              <dl className="kd-ready-summary-meta-v29"><div><dt>Персон</dt><dd>{guests}</dd></div><div><dt>Предметов</dt><dd>{totalUnits}</dd></div></dl>
              <h3>Состав решения</h3>
              <div className="kd-ready-summary-items-v29">
                {activeSelections.slice(0, 7).map(({ option, row, quantity: itemQty }) => <div className="kd-ready-summary-item-v29" key={option.id}>
                  <span className="kd-ready-summary-thumb-v29"><RemoteImage src={row.primary_image_url || "/images/image-placeholder.svg"} alt={option.title}/></span>
                  <span className="kd-ready-summary-copy-v29"><b>{option.title}</b><small>{option.collection || "Культура Дома"}</small><em>{itemQty} шт.</em></span>
                  <strong>{formatRub(toPrice(row.price) * itemQty)}</strong>
                </div>)}
                {activeSelections.length > 7 && <p>+ ещё {activeSelections.length - 7} товаров</p>}
              </div>
              <div className="kd-ready-summary-total-v29"><span><b>Итого</b><small>Включая НДС</small></span><strong>{formatRub(total)}</strong></div>
              <button type="button" className="kd-ready-add-v29" disabled={!activeSelections.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ В КОРЗИНУ"}</button>
              <button type="button" className={`kd-ready-save-v29 ${saved ? "saved" : ""}`} onClick={saveSolution}>{saved ? "✓ РЕШЕНИЕ СОХРАНЕНО" : "♡ СОХРАНИТЬ РЕШЕНИЕ"}</button>
              <div className="kd-ready-benefits-v29"><p>◇ Бесплатная доставка от 15 000 ₽</p><p>↺ Лёгкий возврат в течение 30 дней</p></div>
            </aside>
          </div>
        )}
      </div>

      {activeSelections.length > 0 && <div className="kd-ready-mobile-total-v29"><div><span>{activeSelections.length} товаров · {totalUnits} шт.</span><strong>{formatRub(total)}</strong></div><button type="button" disabled={redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ В КОРЗИНУ"}</button></div>}
    </main>
  );
}
