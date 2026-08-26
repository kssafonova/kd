"use client";

import { useEffect } from "react";

const BANNERS = [
  {
    eyebrow: "НОВАЯ ИСТОРИЯ",
    title: "Дом как единая композиция",
    text: "Текстиль, сервировка и декор в современном русском прочтении.",
    image: "/images/editorial/caps_luna_postel2.png",
    mobile: "/images/editorial/caps_luna_postel.png",
    cta: "Смотреть коллекции",
    action: "collections",
  },
  {
    eyebrow: "ГОТОВЫЕ РЕШЕНИЯ",
    title: "Соберите пространство целиком",
    text: "Выберите готовую основу и измените только нужные предметы.",
    image: "/images/constructor/green.jpeg",
    mobile: "/images/constructor/green.jpeg",
    cta: "Выбрать решение",
    action: "solutions",
  },
  {
    eyebrow: "СЕРВИРОВКА",
    title: "Предметы для ежедневных ритуалов",
    text: "Фарфор, стекло и текстиль, которые работают вместе.",
    image: "/images/time-table.png",
    mobile: "/images/russian-service-blue.png",
    cta: "Смотреть каталог",
    action: "tableware",
  },
];

function asset(path: string) {
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  return `${base}${path}`;
}

function triggerHomeAction(action: string) {
  if (action === "solutions") {
    window.location.href = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;
    return;
  }
  const home = document.querySelector<HTMLElement>(".home-v81");
  if (!home) return;
  if (action === "collections") {
    const button = Array.from(home.querySelectorAll<HTMLButtonElement>(".home81-nav button")).find((item) => item.textContent?.trim() === "Коллекции");
    button?.click();
    return;
  }
  if (action === "tableware") {
    const button = Array.from(home.querySelectorAll<HTMLButtonElement>(".home81-categories button")).find((item) => item.textContent?.includes("Посуда и сервировка"));
    button?.click();
  }
}

function enhanceHome() {
  const home = document.querySelector<HTMLElement>(".home-v81");
  if (!home || home.dataset.home86 === "1") return;
  home.dataset.home86 = "1";

  const originalHero = home.querySelector<HTMLElement>(".home81-hero");
  if (originalHero && !home.querySelector(".home86-banner-section")) {
    const section = document.createElement("section");
    section.className = "home86-banner-section";
    section.setAttribute("aria-label", "Главные истории");
    const rail = document.createElement("div");
    rail.className = "home86-banner-rail";

    BANNERS.forEach((banner, index) => {
      const article = document.createElement("article");
      article.className = "home86-banner";
      article.innerHTML = `
        <picture>
          <source media="(max-width: 700px)" srcset="${asset(banner.mobile)}" />
          <img src="${asset(banner.image)}" alt="${banner.title}" loading="${index === 0 ? "eager" : "lazy"}" />
        </picture>
        <div class="home86-banner-shade"></div>
        <div class="home86-banner-copy">
          <small>${banner.eyebrow}</small>
          <h1>${banner.title}</h1>
          <p>${banner.text}</p>
          <button type="button" data-home86-action="${banner.action}">${banner.cta}</button>
        </div>`;
      rail.appendChild(article);
    });

    section.appendChild(rail);
    originalHero.before(section);
    originalHero.hidden = true;
    section.querySelectorAll<HTMLButtonElement>("[data-home86-action]").forEach((button) => {
      button.addEventListener("click", () => triggerHomeAction(button.dataset.home86Action || ""));
    });
  }

  const categories = home.querySelector<HTMLElement>(".home81-categories");
  if (categories) {
    const small = categories.querySelector("header small");
    const title = categories.querySelector("header h2");
    const text = categories.querySelector("header p");
    if (small) small.textContent = "КАТЕГОРИИ";
    if (title) title.textContent = "Выберите категорию";
    if (text) text.textContent = "Быстрый переход к основным разделам каталога.";
  }

  const collections = home.querySelector<HTMLElement>(".home81-collections");
  if (collections) {
    const small = collections.querySelector(".home81-collections-hero small");
    const title = collections.querySelector(".home81-collections-hero h2");
    const text = collections.querySelector(".home81-collections-hero p");
    if (small) small.textContent = "КАПСУЛЫ И КОЛЛЕКЦИИ";
    if (title) title.textContent = "Истории для дома";
    if (text) text.textContent = "Готовые сочетания цвета, орнамента и материалов — от сервировки до текстиля.";
  }

  const solutions = home.querySelector<HTMLElement>(".home81-solutions");
  if (solutions) {
    const title = solutions.querySelector("header h2");
    const text = solutions.querySelector("header p");
    if (title) title.textContent = "Готовые решения для пространства";
    if (text) text.textContent = "Выберите настроение, а состав и количество предметов настройте под себя.";
  }
}

export function HomeZaraTogasV86Enhancer() {
  useEffect(() => {
    enhanceHome();
    const observer = new MutationObserver(() => enhanceHome());
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);
  return null;
}
