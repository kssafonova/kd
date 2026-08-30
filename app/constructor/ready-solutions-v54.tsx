"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData, loadFinalConstructorData } from "./data-client";
import { TABLE_SOLUTIONS, findTableSolution, type TableSolution } from "./table-solutions";
import { resolveTableSolutionCatalogRows } from "./table-solution-resolver";
import {
  buildSolutionCategories,
  deriveGuestOptions,
  optionColors,
  optionSizes,
  pickOptionVariant,
  recommendedOptionQuantity,
  type SolutionCategory,
  type SolutionProductOption,
} from "./table-solution-builder";
import type { CatalogRow, ConstructorData, FinalConstructorData } from "./types";

const CART_KEY = "kultura-cart";
const CART_OFFSET = 985000;
const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const money = (value: number) => `${new Intl.NumberFormat("ru-RU").format(value)} ₽`;
const priceOf = (row?: CatalogRow) =>
  Number(String(row?.price || "").replace(/[^\d.,-]/g, "").replace(",", ".")) || 0;
const norm = (value: string) =>
  String(value || "")
    .trim()
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/[«»"']/g, "")
    .replace(/\s+/g, " ");
const rowImages = (row?: CatalogRow) =>
  Array.from(
    new Set(
      [row?.primary_image_url, ...(row?.all_image_urls || "").split("|")].filter(
        (value): value is string => Boolean(value),
      ),
    ),
  );
const rowId = (row: CatalogRow) => {
  const numeric = Number(String(row.offer_id || row.group_id || "").replace(/\D/g, ""));
  if (Number.isFinite(numeric) && numeric > 0) return CART_OFFSET + numeric;
  return CART_OFFSET + Array.from(row.product_name).reduce((sum, char) => sum + char.charCodeAt(0), 0);
};

function SiteIcon({ name }: { name: "search" | "user" | "heart" | "bag" | "pin" }) {
  const common = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.6,
    strokeLinecap: "round" as const,
    strokeLinejoin: "round" as const,
  };
  if (name === "search")
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" {...common}>
        <circle cx="10.5" cy="10.5" r="6.5" />
        <path d="m15.3 15.3 5.2 5.2" />
      </svg>
    );
  if (name === "user")
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" {...common}>
        <circle cx="12" cy="7.2" r="4" />
        <path d="M4.2 21c.8-4.4 3.4-6.6 7.8-6.6s7 2.2 7.8 6.6" />
      </svg>
    );
  if (name === "heart")
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" {...common}>
        <path d="M20.8 5.8c-2.2-2.4-6.1-1.8-8.8 1.4-2.7-3.2-6.6-3.8-8.8-1.4-2.4 2.7-1.5 7 1 9.5C6.4 17.6 9.1 20 12 22c2.9-2 5.6-4.4 7.8-6.7 2.5-2.5 3.4-6.8 1-9.5Z" />
      </svg>
    );
  if (name === "pin")
    return (
      <svg viewBox="0 0 24 24" aria-hidden="true" {...common}>
        <path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z" />
        <circle cx="12" cy="10" r="2.6" />
      </svg>
    );
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" {...common}>
      <path d="M4.3 7.5h15.4l-1.2 14H5.5l-1.2-14Z" />
      <path d="M8.5 8V5.7a3.5 3.5 0 0 1 7 0V8" />
    </svg>
  );
}

function IntegratedHeaderV54() {
  return (
    <>
      <div className="promo">
        БЕСПЛАТНАЯ ДОСТАВКА ОТ 15 000 ₽ <Link href={`${basePath}/`}>ПОДРОБНЕЕ</Link>
      </div>
      <header className="header v54-integrated-header">
        <div className="header-left">
          <Link className="icon-btn hamburger" href={`${basePath}/`} aria-label="Каталог">
            <i />
            <i />
            <i />
          </Link>
          <Link className="boutiques" href={`${basePath}/?open=boutiques`}>
            <SiteIcon name="pin" /> Бутики
          </Link>
        </div>
        <Link className="logo" href={`${basePath}/`}>
          КУЛЬТУРА ДОМА
        </Link>
        <div className="header-actions">
          <Link href={`${basePath}/?open=search`} aria-label="Поиск">
            <SiteIcon name="search" />
          </Link>
          <Link href={`${basePath}/?open=account`} aria-label="Профиль">
            <SiteIcon name="user" />
          </Link>
          <Link href={`${basePath}/?open=favorites`} aria-label="Избранное">
            <SiteIcon name="heart" />
          </Link>
          <Link className="bag" href={`${basePath}/?open=cart`} aria-label="Корзина">
            <SiteIcon name="bag" />
          </Link>
        </div>
      </header>
    </>
  );
}

function useConstructorData() {
  const [catalog, setCatalog] = useState<FinalConstructorData | null>(null);
  const [rules, setRules] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    let alive = true;
    Promise.all([loadFinalConstructorData(), loadConstructorData().catch(() => null)])
      .then(([nextCatalog, nextRules]) => {
        if (alive) {
          setCatalog(nextCatalog);
          setRules(nextRules);
        }
      })
      .catch((reason: unknown) => {
        if (alive) setError(reason instanceof Error ? reason.message : "Не удалось загрузить данные");
      });
    return () => {
      alive = false;
    };
  }, []);
  return { catalog, rules, error };
}

function solutionImage(solution: TableSolution, rows: CatalogRow[]) {
  return (
    solution.heroImage ||
    (solution.previewFile ? `/assets/images/constructor/${solution.previewFile}` : rows[0]?.primary_image_url) ||
    "/assets/images/image-placeholder.svg"
  );
}

function orderedCategories(categories: SolutionCategory[], solution: TableSolution) {
  const order = solution.productOrder?.map(norm) ?? [];
  if (!order.length) return categories;
  return categories.map((category) => ({
    ...category,
    slots: category.slots.map((slot) => ({
      ...slot,
      options: [...slot.options].sort((a, b) => {
        const ai = order.indexOf(norm(a.title));
        const bi = order.indexOf(norm(b.title));
        return (ai < 0 ? 9999 : ai) - (bi < 0 ? 9999 : bi);
      }),
    })),
  }));
}

function cartItemFromRow(row: CatalogRow, quantity = 1) {
  const images = rowImages(row);
  const price = priceOf(row);
  const color = row.color || "Без цвета";
  const size = row.size || row.volume || "Единый размер";
  const id = rowId(row);
  return {
    id,
    name: row.product_name,
    note: [row.collection, row.material].filter(Boolean).join(" · "),
    price,
    image: images[0] || "/assets/images/image-placeholder.svg",
    gallery: images.slice(1),
    selectedColor: color,
    selectedSize: size,
    selectedSkuId: `constructor-${row.offer_id || id}`,
    quantity,
    skus: [
      {
        id: `constructor-${row.offer_id || id}`,
        article: row.vendor_code || String(row.offer_id),
        productId: id,
        color,
        colorHex: "#d8d5cf",
        size,
        material: row.material || "",
        composition: row.material || "",
        price,
        image: images[0] || "/assets/images/image-placeholder.svg",
        gallery: images.slice(1),
      },
    ],
  };
}

function addRowsToSharedCart(rows: Array<{ row: CatalogRow; quantity: number }>) {
  let current: any[] = [];
  try {
    current = JSON.parse(localStorage.getItem(CART_KEY) || "[]");
  } catch {}
  const next = [...current];
  rows.forEach(({ row, quantity }) => {
    const item = cartItemFromRow(row, quantity);
    const index = next.findIndex(
      (existing) =>
        existing.id === item.id &&
        existing.selectedColor === item.selectedColor &&
        existing.selectedSize === item.selectedSize,
    );
    if (index >= 0) next[index] = { ...next[index], quantity: (next[index].quantity || 1) + quantity };
    else next.push(item);
  });
  try {
    localStorage.setItem(CART_KEY, JSON.stringify(next));
  } catch {}
}

type BroadGroupId =
  | "tableware"
  | "tableTextile"
  | "bedding"
  | "homeDecor"
  | "atmosphere"
  | "bath";

type BroadItem = {
  option: SolutionProductOption;
  subcategoryId: string;
  subcategoryTitle: string;
};

type BroadGroup = {
  id: BroadGroupId;
  title: string;
  description: string;
  items: BroadItem[];
};

const BROAD_META: Record<
  BroadGroupId,
  { title: string; description: string; categories: string[] }
> = {
  tableware: {
    title: "Посуда и сервировка",
    description:
      "Тарелки, чашки, чайные пары, блюда, чайники, стекло и приборы. Выбирайте только те предметы, которые нужны вашему сценарию.",
    categories: [
      "plates",
      "bowls",
      "cupsPairs",
      "greenSalonTeaService",
      "sugarBowls",
      "milkJugs",
      "teapots",
      "serving",
      "drinkware",
      "cutlery",
    ],
  },
  tableTextile: {
    title: "Столовый текстиль",
    description:
      "Скатерти, дорожки, плейсматы и тканевые салфетки. Количество предметов автоматически учитывает выбранное число персон.",
    categories: ["tableTextile"],
  },
  bedding: {
    title: "Постельное бельё",
    description:
      "Комплекты постельного белья, пледы, покрывала и декоративные подушки для цельной композиции спальни.",
    categories: ["bedding", "throwsCoverlets", "decorativePillows"],
  },
  homeDecor: {
    title: "Декор для дома",
    description:
      "Вазы, корзины, игры, хранение и интерьерные акценты — необязательные элементы, которыми можно завершить решение.",
    categories: ["vases", "baskets", "games", "storage", "other"],
  },
  atmosphere: {
    title: "Свечи и диффузоры",
    description:
      "Свечи, подсвечники и ароматы для дома. Добавьте один или несколько атмосферных акцентов.",
    categories: ["atmosphere"],
  },
  bath: {
    title: "Для ванной",
    description:
      "Халаты, полотенца и текстиль для ванной, если они входят в выбранный сценарий.",
    categories: ["bath"],
  },
};

const BROAD_ORDER: BroadGroupId[] = [
  "tableware",
  "tableTextile",
  "bedding",
  "homeDecor",
  "atmosphere",
  "bath",
];

function buildBroadGroups(categories: SolutionCategory[]): BroadGroup[] {
  return BROAD_ORDER.map((groupId) => {
    const meta = BROAD_META[groupId];
    const source = categories.filter((category) => meta.categories.includes(category.id));
    const items = source.flatMap((category) =>
      category.slots.flatMap((slot) =>
        slot.options.map((option) => ({
          option,
          subcategoryId: category.id,
          subcategoryTitle: category.title,
        })),
      ),
    );
    return { id: groupId, title: meta.title, description: meta.description, items };
  }).filter((group) => group.items.length > 0);
}

function ReadyProductCardV54({
  item,
  selected,
  editing,
  guests,
  color,
  size,
  quantity,
  onToggle,
  onColor,
  onSize,
  onQuantity,
}: {
  item: BroadItem;
  selected: boolean;
  editing: boolean;
  guests: number;
  color: string;
  size: string;
  quantity: number;
  onToggle: () => void;
  onColor: (value: string) => void;
  onSize: (value: string) => void;
  onQuantity: (value: number) => void;
}) {
  const { option } = item;
  const colors = optionColors(option);
  const sizes = optionSizes(option, color);
  const row = pickOptionVariant(option, color, size);
  const image = rowImages(row)[0] || "/assets/images/image-placeholder.svg";

  return (
    <article className={`v54-product-card ${selected ? "is-selected" : ""}`}>
      <div className="v54-product-media">
        <button type="button" className="v54-product-image" onClick={onToggle}>
          <RemoteImage src={image} fallbackSrc="/assets/images/image-placeholder.svg" alt={option.title} />
        </button>
        <button
          type="button"
          className={`v54-checkbox ${selected ? "is-selected" : ""}`}
          onClick={onToggle}
          aria-pressed={selected}
          aria-label={selected ? `Убрать ${option.title}` : `Выбрать ${option.title}`}
        >
          {selected ? "✓" : ""}
        </button>
      </div>

      <div className="v54-product-info">
        <strong>{option.title}</strong>
        <small>{option.collection || row?.material || "Культура Дома"}</small>
        <span>{money(priceOf(row))}</span>
      </div>

      {editing && selected && (
        <div className="v54-product-controls">
          {colors.length > 1 && (
            <div className="v54-control-block">
              <label>Цвет</label>
              <div className="v54-color-options">
                {colors.map((itemColor) => (
                  <button
                    type="button"
                    key={itemColor}
                    className={color === itemColor ? "is-active" : ""}
                    onClick={() => onColor(itemColor)}
                  >
                    {itemColor}
                  </button>
                ))}
              </div>
            </div>
          )}

          {sizes.length > 1 && (
            <label className="v54-size-control">
              <span>Размер</span>
              <select value={size} onChange={(event) => onSize(event.target.value)}>
                <option value="">Выбрать размер</option>
                {sizes.map((itemSize) => (
                  <option value={itemSize} key={itemSize}>
                    {itemSize}
                  </option>
                ))}
              </select>
            </label>
          )}

          <div className="v54-qty-control">
            <div>
              <span>Количество</span>
              {option.perPerson && <small>на {guests} персон</small>}
            </div>
            <div>
              <button type="button" onClick={() => onQuantity(Math.max(1, quantity - 1))}>
                −
              </button>
              <span>{quantity}</span>
              <button type="button" onClick={() => onQuantity(quantity + 1)}>
                +
              </button>
            </div>
          </div>
        </div>
      )}
    </article>
  );
}

function ReadySolutionPageV54({
  solution,
  catalog,
  rules,
}: {
  solution: TableSolution;
  catalog: FinalConstructorData;
  rules: ConstructorData | null;
}) {
  const rows = useMemo(
    () => resolveTableSolutionCatalogRows(catalog.catalog, solution),
    [catalog, solution],
  );
  const legacyCategories = useMemo(
    () => orderedCategories(buildSolutionCategories(rows, solution.space), solution),
    [rows, solution],
  );
  const groups = useMemo(() => buildBroadGroups(legacyCategories), [legacyCategories]);
  const options = useMemo(
    () => groups.flatMap((group) => group.items.map((item) => item.option)),
    [groups],
  );
  const guestOptions = useMemo(() => deriveGuestOptions(solution, rules), [solution, rules]);
  const [guests, setGuests] = useState(guestOptions[0] || 2);
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const [colors, setColors] = useState<Record<string, string>>({});
  const [sizes, setSizes] = useState<Record<string, string>>({});
  const [qty, setQty] = useState<Record<string, number>>({});
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [editingGroup, setEditingGroup] = useState<string>("");

  useEffect(() => {
    if (!guestOptions.includes(guests)) setGuests(guestOptions[0] || 2);
  }, [guestOptions, guests]);

  useEffect(() => {
    const defaults = (solution.defaultProductNames ?? solution.productNames).map(norm);
    const nextSelected: Record<string, boolean> = {};
    const nextColors: Record<string, string> = {};
    const nextSizes: Record<string, string> = {};
    const nextQty: Record<string, number> = {};

    options.forEach((option) => {
      const title = norm(option.title);
      nextSelected[option.id] = defaults.some(
        (target) => target === title || target.includes(title) || title.includes(target),
      );

      const defaultColor =
        Object.entries(solution.defaultColors ?? {}).find(([name]) => norm(name) === title)?.[1] ??
        optionColors(option)[0] ??
        "";
      const availableSizes = optionSizes(option, defaultColor);
      const configuredSize = Object.entries(solution.defaultSizes ?? {}).find(
        ([name]) => norm(name) === title,
      )?.[1];

      nextColors[option.id] = defaultColor;
      if (configuredSize) nextSizes[option.id] = configuredSize;
      else if (availableSizes.length === 1) nextSizes[option.id] = availableSizes[0];

      nextQty[option.id] =
        Object.entries(solution.defaultQuantities ?? {}).find(([name]) => norm(name) === title)?.[1] ??
        recommendedOptionQuantity(option, guestOptions[0] || 2);
    });

    setSelected(nextSelected);
    setColors(nextColors);
    setSizes(nextSizes);
    setQty(nextQty);
    setFilters({});
    setEditingGroup("");
  }, [options, solution, guestOptions]);

  useEffect(() => {
    setQty((current) => {
      const next = { ...current };
      options.forEach((option) => {
        if (option.perPerson) next[option.id] = recommendedOptionQuantity(option, guests);
      });
      return next;
    });
  }, [guests, options]);

  const selectedRows = options
    .filter((option) => selected[option.id])
    .map((option) => {
      const color = colors[option.id] ?? optionColors(option)[0] ?? "";
      const size = sizes[option.id] ?? "";
      const availableSizes = optionSizes(option, color);
      const missingSize = availableSizes.length > 1 && !size;
      const row = pickOptionVariant(option, color, size);
      return {
        option,
        row,
        missingSize,
        quantity: qty[option.id] ?? recommendedOptionQuantity(option, guests),
      };
    });

  const pending = selectedRows.filter((item) => item.missingSize).length;
  const total = selectedRows.reduce(
    (sum, item) => sum + priceOf(item.row) * item.quantity,
    0,
  );
  const units = selectedRows.reduce((sum, item) => sum + item.quantity, 0);

  const addSolution = () => {
    if (!selectedRows.length || pending > 0) return;
    addRowsToSharedCart(
      selectedRows.map((item) => ({ row: item.row, quantity: item.quantity })),
    );
    window.location.assign(`${basePath}/?open=cart`);
  };

  const toggleWholeGroup = (group: BroadGroup, value: boolean) => {
    setSelected((current) => {
      const next = { ...current };
      group.items.forEach(({ option }) => {
        next[option.id] = value;
      });
      return next;
    });
  };

  const hero = solutionImage(solution, rows);

  return (
    <div className="v54-ready-page">
      <IntegratedHeaderV54 />

      <main>
        <section className="v54-hero">
          <div className="v54-hero-media">
            <RemoteImage
              src={hero}
              fallbackSrc={rows[0]?.primary_image_url || "/assets/images/image-placeholder.svg"}
              alt={solution.name}
            />
          </div>
          <div className="v54-hero-copy">
            <Link href={`${basePath}/constructor/`}>← Все готовые решения</Link>
            <small>ГОТОВОЕ РЕШЕНИЕ · {solution.space}</small>
            <h1>{solution.name}</h1>
            <p>
              Выберите количество персон, затем соберите решение по крупным категориям.
              Внутри каждого блока можно сравнить товары, отметить нужные и настроить
              цвет, размер и количество.
            </p>
            <span>{solution.collections.join(" · ")}</span>
          </div>
        </section>

        <section className="v54-person-step" aria-labelledby="v54-person-title">
          <div>
            <small>ШАГ 1</small>
            <h2 id="v54-person-title">Количество персон</h2>
            <p>
              Мы пересчитаем количество тарелок, пар, приборов, плейсматов и других
              персональных предметов. Декор и крупный текстиль останутся без изменений.
            </p>
          </div>
          <div className="v54-person-options" role="group" aria-label="Количество персон">
            {guestOptions.map((value) => (
              <button
                type="button"
                key={value}
                className={guests === value ? "is-active" : ""}
                onClick={() => setGuests(value)}
              >
                {value}
              </button>
            ))}
          </div>
        </section>

        <nav className="v54-category-nav" aria-label="Категории решения">
          {groups.map((group) => (
            <a href={`#v54-${group.id}`} key={group.id}>
              {group.title}
            </a>
          ))}
        </nav>

        <section className="v54-groups">
          {groups.map((group) => {
            const subcategories = Array.from(
              new Map(
                group.items.map((item) => [
                  item.subcategoryId,
                  { id: item.subcategoryId, title: item.subcategoryTitle },
                ]),
              ).values(),
            );
            const activeFilter = filters[group.id] || "all";
            const visibleItems =
              activeFilter === "all"
                ? group.items
                : group.items.filter((item) => item.subcategoryId === activeFilter);
            const selectedInGroup = group.items.filter(({ option }) => selected[option.id]).length;
            const allSelected = selectedInGroup === group.items.length && group.items.length > 0;
            const editing = editingGroup === group.id;

            return (
              <section className="v54-group" id={`v54-${group.id}`} key={group.id}>
                <header className="v54-group-head">
                  <div>
                    <small>ШАГ 2 · {selectedInGroup} ИЗ {group.items.length} ВЫБРАНО</small>
                    <h2>{group.title}</h2>
                    <p>{group.description}</p>
                  </div>
                  <button
                    type="button"
                    className="v54-select-all"
                    onClick={() => toggleWholeGroup(group, !allSelected)}
                  >
                    {allSelected ? "Снять всё" : "Выбрать всё"}
                  </button>
                </header>

                {subcategories.length > 1 && (
                  <div className="v54-filter-row" role="group" aria-label={`Фильтры: ${group.title}`}>
                    <button
                      type="button"
                      className={activeFilter === "all" ? "is-active" : ""}
                      onClick={() =>
                        setFilters((current) => ({ ...current, [group.id]: "all" }))
                      }
                    >
                      Все
                    </button>
                    {subcategories.map((subcategory) => (
                      <button
                        type="button"
                        key={subcategory.id}
                        className={activeFilter === subcategory.id ? "is-active" : ""}
                        onClick={() =>
                          setFilters((current) => ({
                            ...current,
                            [group.id]: subcategory.id,
                          }))
                        }
                      >
                        {subcategory.title}
                      </button>
                    ))}
                  </div>
                )}

                <div className="v54-product-grid">
                  {visibleItems.map((item) => {
                    const option = item.option;
                    const color = colors[option.id] ?? optionColors(option)[0] ?? "";
                    const size = sizes[option.id] ?? "";
                    return (
                      <ReadyProductCardV54
                        key={option.id}
                        item={item}
                        selected={Boolean(selected[option.id])}
                        editing={editing}
                        guests={guests}
                        color={color}
                        size={size}
                        quantity={qty[option.id] ?? recommendedOptionQuantity(option, guests)}
                        onToggle={() =>
                          setSelected((current) => ({
                            ...current,
                            [option.id]: !current[option.id],
                          }))
                        }
                        onColor={(value) => {
                          setColors((current) => ({ ...current, [option.id]: value }));
                          const nextSizes = optionSizes(option, value);
                          setSizes((current) => ({
                            ...current,
                            [option.id]: nextSizes.length === 1 ? nextSizes[0] : "",
                          }));
                        }}
                        onSize={(value) =>
                          setSizes((current) => ({ ...current, [option.id]: value }))
                        }
                        onQuantity={(value) =>
                          setQty((current) => ({ ...current, [option.id]: value }))
                        }
                      />
                    );
                  })}
                </div>

                <button
                  type="button"
                  className={`v54-configure-group ${editing ? "is-active" : ""}`}
                  onClick={() => setEditingGroup(editing ? "" : group.id)}
                >
                  {editing ? "ГОТОВО" : "НАСТРОИТЬ РЕШЕНИЕ"}
                </button>
              </section>
            );
          })}
        </section>
      </main>

      <aside className="v54-summary" aria-live="polite">
        <div>
          <small>
            {pending > 0
              ? `Нужно выбрать размер · ${pending}`
              : selectedRows.length
                ? `Выбрано ${selectedRows.length} позиций · ${units} шт.`
                : "Выберите товары"}
          </small>
          <strong>{money(total)}</strong>
        </div>
        <button
          type="button"
          disabled={!selectedRows.length || pending > 0}
          onClick={addSolution}
        >
          ДОБАВИТЬ РЕШЕНИЕ В КОРЗИНУ
        </button>
      </aside>
    </div>
  );
}

export function ReadySolutionsLandingV54() {
  const { catalog, error } = useConstructorData();

  const cards = useMemo(
    () =>
      !catalog
        ? []
        : TABLE_SOLUTIONS.map((solution) => {
            const rows = resolveTableSolutionCatalogRows(catalog.catalog, solution);
            return {
              solution,
              rows,
              image: solutionImage(solution, rows),
              count: Array.from(new Set(rows.map((row) => norm(row.product_name)))).length,
            };
          }),
    [catalog],
  );

  return (
    <div className="v54-ready-page">
      <IntegratedHeaderV54 />
      <main className="v54-landing">
        <header className="v54-landing-intro">
          <small>КУЛЬТУРА ДОМА · ГОТОВЫЕ РЕШЕНИЯ</small>
          <h1>Готовые решения</h1>
          <p>
            Выберите готовый сценарий, укажите количество персон и настройте только
            нужные категории. Товары, цвета, размеры и количество можно изменить
            внутри каждого блока.
          </p>
        </header>

        {error ? (
          <div className="v54-state">{error}</div>
        ) : !catalog ? (
          <div className="v54-state">Загружаем решения…</div>
        ) : (
          <section className="v54-landing-grid">
            {cards.map(({ solution, rows, image, count }) => (
              <article key={solution.id} className="v54-landing-card">
                <Link href={`${basePath}/constructor/${solution.id}/`}>
                  <span>
                    <RemoteImage
                      src={image}
                      fallbackSrc={rows[0]?.primary_image_url}
                      alt={solution.name}
                    />
                  </span>
                  <small>{solution.space}</small>
                  <h2>{solution.name}</h2>
                  <p>{solution.collections.join(" · ")}</p>
                  <div>
                    <em>{count} позиций</em>
                    <b>Собрать →</b>
                  </div>
                </Link>
              </article>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export function ReadySolutionDetailV54({ scenarioId }: { scenarioId: string }) {
  const { catalog, rules, error } = useConstructorData();
  const solution = findTableSolution(scenarioId);

  if (!solution) return null;

  if (error) {
    return (
      <div className="v54-ready-page">
        <IntegratedHeaderV54 />
        <div className="v54-state">{error}</div>
      </div>
    );
  }

  if (!catalog) {
    return (
      <div className="v54-ready-page">
        <IntegratedHeaderV54 />
        <div className="v54-state">Загружаем решение…</div>
      </div>
    );
  }

  return <ReadySolutionPageV54 solution={solution} catalog={catalog} rules={rules} />;
}
