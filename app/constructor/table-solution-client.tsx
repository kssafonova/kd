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

const CART_KEY = "kultura-cart";
const CART_OFFSET = 920000;
const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const price = (value?: string) => Number(String(value || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const norm = (value: string) => String(value || "").trim().toLocaleLowerCase("ru-RU").replace(/ё/g, "е").replace(/[«»"']/g, "").replace(/\s+/g, " ");
const images = (row?: CatalogRow) => Array.from(new Set([row?.primary_image_url, ...(row?.all_image_urls || "").split("|")].filter((v): v is string => Boolean(v))));

const swatch = (value: string) => {
  const v = value.toLocaleLowerCase("ru-RU");
  if (v.includes("бел") || v.includes("молоч") || v.includes("айвори")) return "#f1efe8";
  if (v.includes("черн")) return "#181818";
  if (v.includes("темно-син") || v.includes("ночн")) return "#24364a";
  if (v.includes("син")) return "#49657b";
  if (v.includes("голуб")) return "#9db8c7";
  if (v.includes("зелен")) return "#56735d";
  if (v.includes("красн") || v.includes("бордо")) return "#8f3c39";
  if (v.includes("роз") || v.includes("пудр")) return "#d5aaa7";
  if (v.includes("беж") || v.includes("льнян") || v.includes("песоч")) return "#c7b59d";
  if (v.includes("сер")) return "#9b9b96";
  if (v.includes("золот")) return "#b99a5f";
  return "#d8d5cf";
};

type CartItem = {
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
  skus: Array<{ id: string; article: string; productId: number; color: string; colorHex: string; size: string; material: string; composition: string; price: number; image: string; gallery: string[] }>;
};

const putInCart = (items: CartItem[]) => {
  let current: CartItem[] = [];
  try { current = JSON.parse(localStorage.getItem(CART_KEY) || "[]") as CartItem[]; } catch { current = []; }
  const next = [...current];
  items.forEach((item) => {
    const i = next.findIndex((x) => x.id === item.id && x.selectedColor === item.selectedColor && x.selectedSize === item.selectedSize);
    if (i >= 0) next[i] = { ...next[i], quantity: next[i].quantity + item.quantity };
    else next.push(item);
  });
  try { localStorage.setItem(CART_KEY, JSON.stringify(next)); } catch {}
};

export function TableSolutionDetail({ scenarioId }: { scenarioId: string }) {
  const solution = findTableSolution(scenarioId);
  const [data, setData] = useState<FinalConstructorData | null>(null);
  const [rules, setRules] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  const [guests, setGuests] = useState(2);
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [open, setOpen] = useState<Record<string, boolean>>({});
  const [saved, setSaved] = useState(false);
  const [adding, setAdding] = useState(false);

  useEffect(() => {
    let alive = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([catalog, ruleData]) => { if (alive) { setData(catalog); setRules(ruleData); } })
      .catch((e: unknown) => alive && setError(e instanceof Error ? e.message : "Не удалось загрузить решение"));
    return () => { alive = false; };
  }, []);

  const rows = useMemo(() => data && solution ? resolveTableSolutionCatalogRows(data.catalog, solution) : [], [data, solution]);
  const categories = useMemo(() => solution ? buildSolutionCategories(rows, solution.space) : [], [rows, solution]);
  const options = useMemo(() => categories.flatMap((c) => c.slots.flatMap((s) => s.options)), [categories]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, rules) : [1, 2], [solution, rules]);

  useEffect(() => {
    if (guestOptions.length && !guestOptions.includes(guests)) setGuests(guestOptions[0]);
  }, [guestOptions, guests]);

  useEffect(() => {
    setSelected({}); setColors({}); setSizes({}); setQty({}); setOpen({}); setSaved(false);
  }, [scenarioId]);

  useEffect(() => {
    if (!categories.length || !solution) return;
    setOpen((state) => Object.keys(state).length ? state : { [categories[0].id]: true });
    setSelected((state) => {
      if (Object.keys(state).length) return state;
      const explicit = solution.productNames.map(norm).filter(Boolean);
      const next: Record<string, boolean> = {};
      categories.forEach((category) => {
        const list = category.slots.flatMap((slot) => slot.options);
        const matches = list.filter((option) => explicit.some((target) => {
          const title = norm(option.title);
          return title === target || title.includes(target) || target.includes(title);
        }));
        if (matches.length) matches.forEach((option) => { next[option.id] = true; });
        else if (!["atmosphere", "vases", "games", "other"].includes(category.id) && list[0]) next[list[0].id] = true;
      });
      return next;
    });
  }, [categories, solution]);

  if (!solution) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться</Link></div></main>;
  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;

  const checked = (option: SolutionProductOption) => Boolean(selected[option.id]);
  const chosenRow = (option: SolutionProductOption) => {
    const colorList = optionColors(option);
    const color = colors[option.id] || colorList[0] || "";
    const sizeList = optionSizes(option, color);
    const size = sizes[option.id] || sizeList[0] || "";
    return pickOptionVariant(option, color, size);
  };
  const count = (option: SolutionProductOption) => qty[option.id] ?? recommendedOptionQuantity(option, guests);
  const active = options.filter(checked).map((option) => ({ option, row: chosenRow(option), quantity: count(option) })).filter((x): x is { option: SolutionProductOption; row: CatalogRow; quantity: number } => Boolean(x.row));
  const units = active.reduce((sum, x) => sum + x.quantity, 0);
  const total = active.reduce((sum, x) => sum + price(x.row.price) * x.quantity, 0);
  const fallback = rows[0]?.primary_image_url || "/assets/images/image-placeholder.svg";
  const hero = solution.previewFile ? `/assets/images/constructor/${solution.previewFile}` : fallback;

  const toggleCategory = (list: SolutionProductOption[]) => {
    const all = list.every(checked);
    setSelected((state) => ({ ...state, ...Object.fromEntries(list.map((item) => [item.id, !all])) }));
  };

  const save = () => {
    try {
      localStorage.setItem(`kultura-ready-solution-${scenarioId}`, JSON.stringify({ guests, items: active.map((x) => ({ optionId: x.option.id, offerId: x.row.offer_id, quantity: x.quantity })) }));
      setSaved(true);
    } catch {}
  };

  const add = () => {
    const items: CartItem[] = active.map(({ option, row, quantity }, index) => {
      const numeric = Number(String(row.offer_id).split("-")[0]) || index + 1;
      const productId = CART_OFFSET + numeric;
      const image = row.primary_image_url || "/assets/images/image-placeholder.svg";
      const selectedSize = row.size || row.volume || "Стандартный";
      return {
        id: productId,
        name: option.title,
        note: `Из готового решения «${solution.name}» · ${option.collection || "Культура Дома"} · ${guests} персон`,
        price: price(row.price),
        image,
        gallery: images(row),
        selectedColor: row.color || "",
        selectedSize,
        selectedSkuId: `table-solution-${solution.sourceId}-${row.offer_id}`,
        quantity,
        skus: option.variants.map((variant, i) => ({
          id: `table-solution-${solution.sourceId}-${variant.offer_id}`,
          article: variant.vendor_code || String(variant.offer_id),
          productId: CART_OFFSET + (Number(String(variant.offer_id).split("-")[0]) || numeric + i),
          color: variant.color || "",
          colorHex: swatch(variant.color || ""),
          size: variant.size || variant.volume || "Стандартный",
          material: variant.material || "",
          composition: "",
          price: price(variant.price),
          image: variant.primary_image_url || image,
          gallery: images(variant),
        })),
      };
    });
    if (!items.length) return;
    putInCart(items);
    setAdding(true);
    window.setTimeout(() => { window.location.href = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/?cart=open`; }, 350);
  };

  return <main className="solution-simple-shell kd-ready-v29">
    <div className="solution-simple-wrap kd-ready-wrap-v29">
      <nav className="kd-ready-breadcrumb-v29"><Link href="/constructor/">← Готовые решения</Link><span>{solution.space}</span></nav>

      <section className="kd-ready-hero-v29">
        <div className="kd-ready-hero-copy-v29"><small>{solution.name} · {solution.space}</small><h1>ГОТОВЫЕ РЕШЕНИЯ</h1><p>Соберите идеальное пространство за несколько кликов — выберите нужные предметы, цвет и количество.</p>{solution.collections.length > 0 && <div className="kd-ready-collections-v29">{solution.collections.map((x) => <span key={x}>{x}</span>)}</div>}</div>
        <div className="kd-ready-hero-media-v29"><RemoteImage src={hero} fallbackSrc={fallback} alt={solution.name} loading="eager"/></div>
      </section>

      <section className="kd-ready-guests-v29"><span>Сколько персон будет за столом?</span><div role="group">{guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => { setGuests(value); setQty({}); }}><b>{value}</b><em>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</em></button>)}</div></section>

      {!rows.length ? <section className="table-solution-pending-composition"><div><small>СОСТАВ</small><h2>Товары не найдены</h2></div></section> : <div className="kd-ready-commerce-v29">
        <section className="kd-ready-groups-v29">
          {categories.map((category) => {
            const list = category.slots.flatMap((slot) => slot.options);
            const selectedCount = list.filter(checked).length;
            const all = selectedCount === list.length && list.length > 0;
            const perPerson = list.some((item) => item.perPerson);
            const isOpen = Boolean(open[category.id]);
            return <section className={`kd-ready-group-v29 ${isOpen ? "open" : "collapsed"}`} id={`solution-category-${category.id}`} key={category.id}>
              <header className="kd-ready-group-header-v29">
                <button className="kd-ready-group-toggle-v29" type="button" aria-expanded={isOpen} onClick={() => setOpen((state) => ({ ...state, [category.id]: !isOpen }))}><span><h2>{category.title}</h2><small>{perPerson ? `Рекомендуем ${guests} шт.` : `${selectedCount} выбрано`}</small></span><i aria-hidden="true">⌄</i></button>
                <label className="kd-ready-select-all-v29"><input type="checkbox" checked={all} onChange={() => toggleCategory(list)}/><span>Выбрать все</span></label>
              </header>
              <div className="kd-ready-group-body-v29"><div className="kd-ready-products-v29">{list.map((option) => {
                const isChecked = checked(option);
                const row = chosenRow(option) || option.variants[0];
                const colorList = optionColors(option);
                const activeColor = colors[option.id] || colorList[0] || "";
                const sizeList = optionSizes(option, activeColor);
                const activeSize = sizes[option.id] || sizeList[0] || "";
                const q = count(option);
                return <article className={`kd-ready-product-v29 ${isChecked ? "selected" : ""}`} key={option.id}>
                  <button className="kd-ready-product-check-v29" type="button" aria-pressed={isChecked} onClick={() => setSelected((state) => ({ ...state, [option.id]: !isChecked }))}><span>{isChecked ? "✓" : ""}</span></button>
                  <div className="kd-ready-product-media-v29"><RemoteImage src={row?.primary_image_url || "/assets/images/image-placeholder.svg"} alt={option.title}/></div>
                  <div className="kd-ready-product-copy-v29"><small>{option.collection || "Культура Дома"}</small><h3>{option.title}</h3><strong>{price(row?.price) ? money(price(row?.price)) : "Цена уточняется"}</strong></div>
                  {isChecked && <div className="kd-ready-product-controls-v29">
                    {colorList.length > 1 && <div className="kd-ready-swatches-v29">{colorList.map((color) => <button type="button" key={color} className={activeColor === color ? "active" : ""} title={color} onClick={() => { setColors((state) => ({ ...state, [option.id]: color })); setSizes((state) => { const next = { ...state }; delete next[option.id]; return next; }); }}><i style={{ background: swatch(color) }}/></button>)}</div>}
                    {sizeList.length > 1 && <select className="kd-ready-size-v29" value={activeSize} onChange={(e) => setSizes((state) => ({ ...state, [option.id]: e.target.value }))}>{sizeList.map((size) => <option key={size}>{size}</option>)}</select>}
                    <div className="kd-ready-qty-v29"><button type="button" onClick={() => setQty((state) => ({ ...state, [option.id]: Math.max(1, q - 1) }))}>−</button><b>{q}</b><button type="button" onClick={() => setQty((state) => ({ ...state, [option.id]: q + 1 }))}>+</button></div>
                  </div>}
                </article>;
              })}</div></div>
            </section>;
          })}
        </section>

        <aside className="kd-ready-summary-v29">
          <div className="kd-ready-summary-title-v29"><div><small>Ваше решение</small><h2>{solution.name}</h2></div><a href={categories[0] ? `#solution-category-${categories[0].id}` : "#"}>Изменить</a></div>
          <dl className="kd-ready-summary-meta-v29"><div><dt>Персон</dt><dd>{guests}</dd></div><div><dt>Предметов</dt><dd>{units}</dd></div></dl>
          <h3>Состав решения</h3>
          <div className="kd-ready-summary-items-v29">{active.slice(0, 7).map(({ option, row, quantity }) => <div className="kd-ready-summary-item-v29" key={option.id}><span className="kd-ready-summary-thumb-v29"><RemoteImage src={row.primary_image_url || "/assets/images/image-placeholder.svg"} alt={option.title}/></span><span className="kd-ready-summary-copy-v29"><b>{option.title}</b><small>{option.collection || "Культура Дома"}</small><em>{quantity} шт.</em></span><strong>{money(price(row.price) * quantity)}</strong></div>)}{active.length > 7 && <p>+ ещё {active.length - 7} товаров</p>}</div>
          <div className="kd-ready-summary-total-v29"><span><b>Итого</b><small>Включая НДС</small></span><strong>{money(total)}</strong></div>
          <button type="button" className="kd-ready-add-v29" disabled={!active.length || adding} onClick={add}>{adding ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ В КОРЗИНУ"}</button>
          <button type="button" className={`kd-ready-save-v29 ${saved ? "saved" : ""}`} onClick={save}>{saved ? "✓ РЕШЕНИЕ СОХРАНЕНО" : "♡ СОХРАНИТЬ РЕШЕНИЕ"}</button>
          <div className="kd-ready-benefits-v29"><p>◇ Бесплатная доставка от 15 000 ₽</p><p>↺ Лёгкий возврат в течение 30 дней</p></div>
        </aside>
      </div>}
    </div>

    {active.length > 0 && <div className="kd-ready-mobile-total-v29"><div><span>{active.length} товаров · {units} шт.</span><strong>{money(total)}</strong></div><button type="button" disabled={adding} onClick={add}>{adding ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ В КОРЗИНУ"}</button></div>}
  </main>;
}
