"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { useEffect } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { findTableSolution } from "./table-solutions";
import { resolveTableSolutionProducts } from "./table-solution-resolver";
import {
  SOLUTION_PRESETS,
  buildSolutionGroups,
  deriveGuestOptions,
  isPerPersonProduct,
  recommendedProductQuantity,
  selectionForPreset,
  type SolutionPreset,
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
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [quantity, setQuantity] = useState<Record<string, number>>({});
  const [guests, setGuests] = useState(2);
  const [preset, setPreset] = useState<SolutionPreset>("balanced");
  const [redirecting, setRedirecting] = useState(false);

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
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Не удалось загрузить решение"));
    return () => { active = false; };
  }, []);

  const productRows = useMemo(() => {
    if (!data || !solution) return [];
    return resolveTableSolutionProducts(data.catalog, solution);
  }, [data, solution]);

  const groups = useMemo(() => solution ? buildSolutionGroups(productRows, solution.space) : [], [productRows, solution]);
  const guestOptions = useMemo(() => solution ? deriveGuestOptions(solution, ruleData) : [1, 2], [solution, ruleData]);
  const defaultSelection = useMemo(() => selectionForPreset(groups, preset), [groups, preset]);

  useEffect(() => {
    if (!guestOptions.length) return;
    if (!guestOptions.includes(guests)) setGuests(guestOptions[0]);
  }, [guestOptions, guests]);

  useEffect(() => {
    setSelected({});
    setQuantity({});
    setPreset("balanced");
  }, [scenarioId]);

  if (!solution) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Решение не найдено</h1><Link href="/constructor/">Вернуться к готовым решениям</Link></div></main>;
  if (error) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty"><h1>Не удалось загрузить решение</h1><p>{error}</p></div></main>;
  if (!data) return <main className="solution-simple-shell"><div className="solution-simple-wrap solution-simple-empty">Загружаем решение…</div></main>;

  const isSelected = (row: CatalogRow) => selected[row.offer_id] ?? defaultSelection.has(row.offer_id);
  const itemQuantity = (row: CatalogRow) => quantity[row.offer_id] ?? recommendedProductQuantity(row, solution.space, guests);
  const activeRows = productRows.filter(isSelected);
  const totalUnits = activeRows.reduce((sum, row) => sum + itemQuantity(row), 0);
  const total = activeRows.reduce((sum, row) => sum + toPrice(row.price) * itemQuantity(row), 0);
  const previewFallback = productRows[0]?.primary_image_url || "/images/image-placeholder.svg";
  const scrollFallback = productRows[1]?.primary_image_url || productRows[0]?.all_image_urls?.split("|")[1] || previewFallback;
  const previewSrc = solution.previewFile ? `/images/constructor/${solution.previewFile}` : previewFallback;
  const scrollSrc = solution.scrollFile ? `/images/constructor/${solution.scrollFile}` : scrollFallback;

  const applyPreset = (nextPreset: SolutionPreset) => {
    const nextSelection = selectionForPreset(groups, nextPreset);
    setPreset(nextPreset);
    setSelected(Object.fromEntries(productRows.map((row) => [row.offer_id, nextSelection.has(row.offer_id)])));
    setQuantity({});
  };

  const changeGuests = (value: number) => {
    setGuests(value);
    setQuantity({});
  };

  const toggleGroup = (rows: CatalogRow[]) => {
    const allChecked = rows.every(isSelected);
    setSelected((state) => ({
      ...state,
      ...Object.fromEntries(rows.map((row) => [row.offer_id, !allChecked])),
    }));
  };

  const presetCards = SOLUTION_PRESETS.map((option) => {
    const ids = selectionForPreset(groups, option.id);
    const rows = productRows.filter((row) => ids.has(row.offer_id));
    const scenarioTotal = rows.reduce((sum, row) => sum + toPrice(row.price) * recommendedProductQuantity(row, solution.space, guests), 0);
    return { ...option, count: rows.length, total: scenarioTotal };
  });

  const addSolution = () => {
    const items: SharedCartItem[] = activeRows.map((row, index) => {
      const numericOffer = Number(String(row.offer_id).split("-")[0]) || index + 1;
      const productId = CART_ID_OFFSET + numericOffer;
      const skuId = `table-solution-${solution.sourceId}-${row.offer_id}`;
      const image = row.primary_image_url || "/images/image-placeholder.svg";
      const gallery = splitImages(row);
      const size = row.size || row.volume || "Стандартный";
      const price = toPrice(row.price);
      return {
        id: productId,
        name: row.product_name,
        note: `Из готового решения «${solution.name}» · ${guests} персон`,
        price,
        image,
        gallery,
        selectedColor: row.color || "",
        selectedSize: size,
        selectedSkuId: skuId,
        quantity: itemQuantity(row),
        skus: [{
          id: skuId,
          article: row.vendor_code || String(row.offer_id),
          productId,
          color: row.color || "",
          colorHex: "#d8d5cf",
          size,
          material: row.material || "",
          composition: "",
          price,
          image,
          gallery,
        }],
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
    <main className="solution-simple-shell table-solution-detail-shell table-builder-v25">
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
            {solution.collections.length > 0 && <div className="table-solution-collection-list">
              {solution.collections.map((collection) => <span key={collection}>{collection}</span>)}
            </div>}
            <p>Настройте решение под себя: укажите количество персон, выберите готовый сценарий комплектации и затем скорректируйте товары внутри каждой категории.</p>
            <div className="table-solution-hero-total"><span>{activeRows.length} товаров · {totalUnits} шт.</span><strong>{formatRub(total)}</strong></div>
          </div>
        </section>

        {productRows.length === 0 ? (
          <section className="table-solution-pending-composition">
            <div><small>СОСТАВ</small><h2>Товары не найдены в CSV</h2><p>Для этого решения в текущем каталоге не удалось найти позиции по указанным коллекциям или названиям.</p></div>
          </section>
        ) : (
          <>
            <section className="table-builder-config" aria-label="Настройка готового решения">
              <div className="table-builder-step">
                <div className="table-builder-step-number">01</div>
                <div className="table-builder-step-copy"><small>КОЛИЧЕСТВО ПЕРСОН</small><h2>На сколько человек?</h2><p>Для индивидуальной посуды и текстиля количество пересчитается автоматически.</p></div>
                <div className="table-builder-guests" role="group" aria-label="Количество персон">
                  {guestOptions.map((value) => <button type="button" key={value} className={guests === value ? "active" : ""} onClick={() => changeGuests(value)}><strong>{value}</strong><span>{value === 1 ? "персона" : value < 5 ? "персоны" : "персон"}</span></button>)}
                </div>
              </div>

              <div className="table-builder-step table-builder-step-scenarios">
                <div className="table-builder-step-number">02</div>
                <div className="table-builder-step-copy"><small>ГОТОВЫЙ СЦЕНАРИЙ</small><h2>Выберите уровень комплектации</h2><p>Можно начать с готового набора, а затем изменить любой товар вручную.</p></div>
                <div className="table-builder-presets">
                  {presetCards.map((option) => <button type="button" key={option.id} className={preset === option.id ? "active" : ""} onClick={() => applyPreset(option.id)}>
                    <span className="table-builder-preset-check"/>
                    <small>{option.id === "basic" ? "БЫСТРО" : option.id === "balanced" ? "РЕКОМЕНДУЕМ" : "МАКСИМУМ"}</small>
                    <strong>{option.title}</strong>
                    <p>{option.description}</p>
                    <div><span>{option.count} товаров</span><b>{formatRub(option.total)}</b></div>
                  </button>)}
                </div>
              </div>

              <div className="table-builder-step table-builder-step-categories">
                <div className="table-builder-step-number">03</div>
                <div className="table-builder-step-copy"><small>СОСТАВ</small><h2>Настройте по категориям</h2><p>Товары разделены по назначению, чтобы решение собиралось последовательно как конструктор.</p></div>
                <nav className="table-builder-category-nav" aria-label="Категории решения">
                  {groups.map((group) => {
                    const checked = group.rows.filter(isSelected).length;
                    return <a href={`#solution-group-${group.id}`} key={group.id}><span>{group.title}</span><b>{checked}/{group.rows.length}</b></a>;
                  })}
                </nav>
              </div>
            </section>

            <div className="table-solution-buy-layout table-builder-buy-layout">
              <section className="table-solution-product-list table-builder-product-list">
                {groups.map((group) => {
                  const selectedInGroup = group.rows.filter(isSelected).length;
                  const allChecked = selectedInGroup === group.rows.length;
                  return <section className="table-builder-group" id={`solution-group-${group.id}`} key={group.id}>
                    <header className="table-builder-group-header">
                      <div><small>{String(groups.indexOf(group) + 1).padStart(2, "0")} · КАТЕГОРИЯ</small><h2>{group.title}</h2><p>{group.description}</p></div>
                      <div className="table-builder-group-actions"><span>{selectedInGroup} из {group.rows.length}</span><button type="button" onClick={() => toggleGroup(group.rows)}>{allChecked ? "УБРАТЬ ВСЕ" : "ВЫБРАТЬ ВСЕ"}</button></div>
                    </header>

                    <div className="table-builder-products-grid">
                      {group.rows.map((row) => {
                        const checked = isSelected(row);
                        const q = itemQuantity(row);
                        const perPerson = isPerPersonProduct(row, solution.space);
                        return <article className={`table-solution-product table-builder-product ${checked ? "selected" : "disabled"}`} key={row.offer_id}>
                          <div className="table-builder-product-top">
                            <label className="table-solution-product-check"><input type="checkbox" checked={checked} onChange={(event) => setSelected((state) => ({ ...state, [row.offer_id]: event.target.checked }))}/><span/></label>
                            {perPerson && <span className="table-builder-person-badge">НА {guests} ПЕРСОН</span>}
                          </div>
                          <div className="table-solution-product-media"><RemoteImage src={row.primary_image_url || "/images/image-placeholder.svg"} alt={row.product_name}/></div>
                          <div className="table-solution-product-copy">
                            <small>{row.collection || "Культура Дома"}</small>
                            <h3>{row.product_name}</h3>
                            <p>{[row.color && `Цвет: ${row.color}`, row.size && `Размер: ${row.size}`, row.volume && row.volume, row.material].filter(Boolean).join(" · ")}</p>
                            <div className="table-builder-product-bottom">
                              <div className="table-builder-price"><strong>{toPrice(row.price) ? formatRub(toPrice(row.price)) : "Цена уточняется"}</strong>{checked && q > 1 && <small>{formatRub(toPrice(row.price) * q)} за {q} шт.</small>}</div>
                              {checked && <div className="table-solution-qty"><button type="button" aria-label="Уменьшить количество" onClick={() => setQuantity((state) => ({ ...state, [row.offer_id]: Math.max(1, q - 1) }))}>−</button><span>{q}</span><button type="button" aria-label="Увеличить количество" onClick={() => setQuantity((state) => ({ ...state, [row.offer_id]: q + 1 }))}>+</button></div>}
                            </div>
                          </div>
                        </article>;
                      })}
                    </div>
                  </section>;
                })}
              </section>

              <aside className="table-solution-purchase-card table-builder-summary">
                <small>ВАШЕ РЕШЕНИЕ</small>
                <h2>{solution.name}</h2>
                <div><span>Персоны</span><b>{guests}</b></div>
                <div><span>Сценарий</span><b>{SOLUTION_PRESETS.find((item) => item.id === preset)?.title}</b></div>
                <div><span>Выбрано</span><b>{activeRows.length} из {productRows.length}</b></div>
                <div><span>Количество</span><b>{totalUnits} шт.</b></div>
                <div className="table-solution-purchase-total"><span>ИТОГО</span><strong>{formatRub(total)}</strong></div>
                <button type="button" disabled={!activeRows.length || redirecting} onClick={addSolution}>{redirecting ? "ДОБАВЛЯЕМ…" : "ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ"}</button>
                <p>В корзину попадут только выбранные товары и рассчитанное количество на {guests} персон.</p>
              </aside>
            </div>
          </>
        )}
      </div>
    </main>
  );
}
