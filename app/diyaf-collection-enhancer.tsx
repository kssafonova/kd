"use client";

import { useEffect } from "react";

const DIYAF_PRODUCTS = new Set([
  "Блюдо Дияф",
  "Дорожка Дияф",
  "Пиала Дияф",
  "Плейсмат Дияф",
  "Салфетка Дияф",
  "Сахарница Дияф",
  "Скатерть Дияф",
  "Тарелка десертная Дияф",
  "Тарелка закусочная Дияф",
  "Тарелка обеденная Дияф",
  "Чайная пара Дияф",
  "Чайник Дияф",
]);

const DIYAF_TEXTILE = new Set([
  "Дорожка Дияф",
  "Плейсмат Дияф",
  "Салфетка Дияф",
  "Скатерть Дияф",
]);

const COLLECTION_LEAD =
  "Белый фарфор с голубой графикой и столовый текстиль с золотыми деталями — цельная сервировка для спокойного, собранного стола.";

const COLLECTION_DESCRIPTION =
  "«Дияф» соединяет холодный голубой рисунок фарфора с тёплым блеском золотой отделки текстиля. Предметы можно собирать по одному или объединить в полный сценарий сервировки: от скатерти и плейсматов до чайной пары, чайника и посуды для подачи.";

const COMMERCE_COPY =
  "Все 12 предметов коллекции собраны в одной витрине. Фарфор показываем целиком, без жёсткого кропа; текстиль — с сохранением пропорций и фактуры.";

const normalize = (value: string | null | undefined) =>
  String(value ?? "")
    .trim()
    .toLocaleLowerCase("ru-RU")
    .replace(/ё/g, "е")
    .replace(/\s+/g, " ");

const isDiyafName = (value: string | null | undefined) =>
  DIYAF_PRODUCTS.has(String(value ?? "").trim());

const setText = (node: Element | null, text: string) => {
  if (node && node.textContent !== text) node.textContent = text;
};

const markProductSurface = (surface: HTMLElement, name: string) => {
  surface.classList.add("diyaf-product-surface");
  surface.classList.toggle("diyaf-product-textile", DIYAF_TEXTILE.has(name));
  surface.classList.toggle("diyaf-product-porcelain", !DIYAF_TEXTILE.has(name));
  surface.dataset.diyafProduct = name;
};

function enhanceDiyaf() {
  document.querySelectorAll<HTMLElement>(".product-card").forEach((card) => {
    const name = card.querySelector(".product-copy strong")?.textContent?.trim() ?? "";
    if (isDiyafName(name)) markProductSurface(card, name);
  });

  document.querySelectorAll<HTMLElement>(".collections-v52-card").forEach((card) => {
    const title = card.querySelector("h2")?.textContent;
    if (normalize(title) !== "дияф") return;
    card.classList.add("diyaf-collection-card");
    setText(card.querySelector(".collections-v52-card-copy > small"), "КОЛЛЕКЦИЯ");
    setText(card.querySelector(".collections-v52-card-copy > p"), COLLECTION_LEAD);
  });

  document.querySelectorAll<HTMLElement>(".v52-story-modal").forEach((modal) => {
    const title = modal.querySelector(".v52-story-title h1")?.textContent;
    if (normalize(title) !== "дияф") return;

    modal.classList.add("diyaf-story-modal");
    setText(modal.querySelector(".v52-story-title > small"), "КОЛЛЕКЦИЯ");
    setText(modal.querySelector(".v52-story-title > p"), COLLECTION_LEAD);
    setText(modal.querySelector(".v52-story-note > small"), "О КОЛЛЕКЦИИ");
    setText(modal.querySelector(".v52-story-note > p"), COLLECTION_DESCRIPTION);

    const commerce = modal.querySelector<HTMLElement>(".v52-story-commerce");
    if (commerce && !commerce.classList.contains("is-selection-mode")) {
      setText(commerce.querySelector(".v52-commerce-head small"), "ДИЯФ · 12 ПРЕДМЕТОВ");
      setText(commerce.querySelector(".v52-commerce-head h2"), "Сервировка Дияф");
      setText(commerce.querySelector(".v52-commerce-head p"), COMMERCE_COPY);
    }

    modal.querySelectorAll<HTMLElement>(".v52-story-product").forEach((product) => {
      const name = product.querySelector(".product-copy strong")?.textContent?.trim() ?? "";
      if (isDiyafName(name)) markProductSurface(product, name);
    });
  });

  document.querySelectorAll<HTMLElement>(".product-page").forEach((page) => {
    const name = page.querySelector(".pdp-title h1")?.textContent?.trim() ?? "";
    if (isDiyafName(name)) markProductSurface(page, name);
  });
}

export function DiyafCollectionEnhancer() {
  useEffect(() => {
    let frame = 0;
    const schedule = () => {
      if (frame) return;
      frame = window.requestAnimationFrame(() => {
        frame = 0;
        enhanceDiyaf();
      });
    };

    schedule();
    const observer = new MutationObserver(schedule);
    observer.observe(document.body, { childList: true, subtree: true });

    return () => {
      observer.disconnect();
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, []);

  return null;
}
