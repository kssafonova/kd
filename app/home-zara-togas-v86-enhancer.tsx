"use client";

import { useEffect } from "react";

const BANNERS = [
  {
    eyebrow: "КУЛЬТУРА ДОМА",
    title: "Традиции в современном доме",
    text: "Текстиль, сервировка и декор, собранные в спокойную цельную композицию.",
    image: "/assets/images/caps_luna_postel2.png",
    mobile: "/assets/images/caps_luna_postel.png",
    cta: "Смотреть коллекции",
    action: "collections",
  },
  {
    eyebrow: "ГОТОВЫЕ РЕШЕНИЯ",
    title: "Дом, который уже собран",
    text: "Выберите настроение и настройте состав, количество и коллекции под своё пространство.",
    image: "/assets/images/green.jpeg",
    mobile: "/assets/images/green.jpeg",
    cta: "Выбрать решение",
    action: "solutions",
  },
  {
    eyebrow: "СЕРВИРОВКА",
    title: "Предметы для ежедневных ритуалов",
    text: "Фарфор, стекло и текстиль работают вместе — как интерьер, а не как отдельные товары.",
    image: "/assets/images/time-table.png",
    mobile: "/assets/images/russian-service-blue.png",
    cta: "Смотреть посуду",
    action: "tableware",
  },
];

const CAPSULE_IMAGES: Record<string, string[]> = {
  "Ледяные узоры": [
    "/assets/images/caps_led_podyshka.png",
    "/assets/images/caps_led_podyshka2.png",
    "/assets/images/caps_led_serviz.png",
    "/assets/images/caps_led.png",
  ],
  "Лунная сказка": [
    "/assets/images/caps_luna_postel.png",
    "/assets/images/caps_luna_postel2.png",
    "/assets/images/caps_luna_postel3.png",
    "/assets/images/caps_luna_serviz.png",
    "/assets/images/caps_luna_serviz2.png",
    "/assets/images/caps_luna_serviz3.png",
  ],
  "Тайна": [
    "/assets/images/tayna0.jpg",
    "/assets/images/tayna1.jpg",
    "/assets/images/tayna2.jpg",
  ],
  "Нити": [
    "/assets/images/niti0.jpg",
    "/assets/images/niti1.jpg",
  ],
  "Феникс": [
    "/assets/images/feniks0.jpg",
    "/assets/images/feniks1.jpg",
    "/assets/images/feniks2.jpg",
  ],
};

function asset(path: string) {
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  return `${base}${path}`;
}

function homeRoot() {
  return document.querySelector<HTMLElement>(".home-v81");
}

function triggerHomeAction(action: string) {
  if (action === "solutions") {
    window.location.href = `${process.env.NEXT_PUBLIC_BASE_PATH ?? ""}/ready-solutions/`;
    return;
  }
  const home = homeRoot();
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

function scrollRail(rail: HTMLElement, direction: -1 | 1) {
  const card = rail.firstElementChild as HTMLElement | null;
  const amount = card ? Math.max(card.getBoundingClientRect().width + 16, rail.clientWidth * 0.72) : rail.clientWidth * 0.8;
  rail.scrollBy({ left: amount * direction, behavior: "smooth" });
}

function installRailControls(container: HTMLElement, rail: HTMLElement, label: string) {
  if (container.querySelector(".home87-rail-controls")) return;
  const controls = document.createElement("div");
  controls.className = "home87-rail-controls";
  controls.innerHTML = `<button type="button" aria-label="Назад: ${label}">←</button><button type="button" aria-label="Вперёд: ${label}">→</button>`;
  const [prev, next] = Array.from(controls.querySelectorAll<HTMLButtonElement>("button"));
  prev?.addEventListener("click", () => scrollRail(rail, -1));
  next?.addEventListener("click", () => scrollRail(rail, 1));
  container.appendChild(controls);
}

function installCapsuleStyles() {
  if (document.getElementById("home125-capsule-images")) return;
  const style = document.createElement("style");
  style.id = "home125-capsule-images";
  style.textContent = `
    .home-v113 .home117-capsule-media.home125-capsule-media{
      position:relative!important;
      display:block!important;
      width:100%!important;
      aspect-ratio:4/5!important;
      padding:0!important;
      overflow:hidden!important;
      background:#f0eee9!important;
    }
    .home-v113 .home125-capsule-image-grid{
      display:grid!important;
      width:100%!important;
      height:100%!important;
      min-height:100%!important;
      gap:2px!important;
      overflow:hidden!important;
      background:#fff!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="2"]{
      grid-template-columns:1fr 1fr!important;
      grid-template-rows:1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="3"]{
      grid-template-columns:1.35fr .65fr!important;
      grid-template-rows:1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="3"] img:first-child{
      grid-row:1 / 3!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="4"]{
      grid-template-columns:1fr 1fr!important;
      grid-template-rows:1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="6"]{
      grid-template-columns:1fr 1fr 1fr!important;
      grid-template-rows:1fr 1fr 1fr!important;
    }
    .home-v113 .home125-capsule-image-grid[data-count="6"] img:first-child{
      grid-column:1 / 3!important;
      grid-row:1 / 3!important;
    }
    .home-v113 .home125-capsule-image-grid img{
      display:block!important;
      width:100%!important;
      height:100%!important;
      min-width:0!important;
      min-height:0!important;
      object-fit:cover!important;
      object-position:center!important;
      background:#ece9e2!important;
      transform:scale(1.001);
      transition:transform .55s ease,opacity .3s ease!important;
    }
    @media(hover:hover){
      .home-v113 .home117-capsule-card:hover .home125-capsule-image-grid img{
        transform:scale(1.018);
      }
    }
    @media(max-width:700px){
      .home-v113 .home117-capsule-media.home125-capsule-media{
        aspect-ratio:3/4!important;
      }
      .home-v113 .home125-capsule-image-grid{
        gap:1px!important;
      }
    }
  `;
  document.head.appendChild(style);
}

function installCurrentCapsuleImages() {
  const section = document.querySelector<HTMLElement>(".home-v113 .home117-capsules");
  if (!section) return;
  installCapsuleStyles();

  section.querySelectorAll<HTMLElement>(".home117-capsule-card").forEach((card) => {
    const title = card.querySelector<HTMLElement>("h3")?.textContent?.trim() || "";
    const images = CAPSULE_IMAGES[title];
    const media = card.querySelector<HTMLButtonElement>(".home117-capsule-media");
    if (!images?.length || !media) return;

    const signature = images.join("|");
    if (media.dataset.home125Images === signature) return;

    const grid = document.createElement("span");
    grid.className = "home125-capsule-image-grid";
    grid.dataset.count = String(images.length);
    grid.setAttribute("aria-hidden", "true");

    images.forEach((src, index) => {
      const image = document.createElement("img");
      image.src = asset(src);
      image.alt = "";
      image.loading = "lazy";
      image.decoding = "async";
      image.dataset.capsuleImage = `${title}-${index + 1}`;
      grid.appendChild(image);
    });

    media.replaceChildren(grid);
    media.classList.add("home125-capsule-media");
    media.dataset.home125Images = signature;
  });
}

function installHero(home: HTMLElement) {
  const originalHero = home.querySelector<HTMLElement>(".home81-hero");
  if (!originalHero || home.querySelector(".home87-hero")) return;

  home.querySelector(".home86-banner-section")?.remove();

  const section = document.createElement("section");
  section.className = "home87-hero";
  section.setAttribute("aria-label", "Главные истории Культура Дома");

  const rail = document.createElement("div");
  rail.className = "home87-hero-rail";

  BANNERS.forEach((banner, index) => {
    const article = document.createElement("article");
    article.className = "home87-hero-slide";
    article.innerHTML = `
      <picture>
        <source media="(max-width: 700px)" srcset="${asset(banner.mobile)}" />
        <img src="${asset(banner.image)}" alt="${banner.title}" loading="${index === 0 ? "eager" : "lazy"}" />
      </picture>
      <div class="home87-hero-shade"></div>
      <div class="home87-hero-copy">
        <small>${banner.eyebrow}</small>
        <h1>${banner.title}</h1>
        <p>${banner.text}</p>
        <button type="button" data-home87-action="${banner.action}">${banner.cta}</button>
      </div>`;
    rail.appendChild(article);
  });

  const footer = document.createElement("div");
  footer.className = "home87-hero-footer";
  footer.innerHTML = `<div class="home87-hero-progress">${BANNERS.map((banner, index) => `<button type="button" aria-label="${banner.title}" data-home87-slide="${index}" class="${index === 0 ? "is-active" : ""}"></button>`).join("")}</div><div class="home87-hero-arrows"><button type="button" aria-label="Предыдущий баннер">←</button><button type="button" aria-label="Следующий баннер">→</button></div>`;

  section.appendChild(rail);
  section.appendChild(footer);
  originalHero.before(section);
  originalHero.hidden = true;

  section.querySelectorAll<HTMLButtonElement>("[data-home87-action]").forEach((button) => {
    button.addEventListener("click", () => triggerHomeAction(button.dataset.home87Action || ""));
  });

  const progress = Array.from(section.querySelectorAll<HTMLButtonElement>("[data-home87-slide]"));
  const syncProgress = () => {
    const index = Math.max(0, Math.min(BANNERS.length - 1, Math.round(rail.scrollLeft / Math.max(1, rail.clientWidth))));
    progress.forEach((button, buttonIndex) => button.classList.toggle("is-active", buttonIndex === index));
  };
  rail.addEventListener("scroll", syncProgress, { passive: true });
  progress.forEach((button) => button.addEventListener("click", () => {
    const index = Number(button.dataset.home87Slide || 0);
    rail.scrollTo({ left: rail.clientWidth * index, behavior: "smooth" });
  }));
  const arrows = Array.from(section.querySelectorAll<HTMLButtonElement>(".home87-hero-arrows button"));
  arrows[0]?.addEventListener("click", () => scrollRail(rail, -1));
  arrows[1]?.addEventListener("click", () => scrollRail(rail, 1));
}

function installBrandStory(home: HTMLElement) {
  const collections = home.querySelector<HTMLElement>(".home81-collections");
  if (!collections || home.querySelector(".home87-brand-story")) return;

  const story = document.createElement("section");
  story.className = "home87-brand-story";
  story.innerHTML = `
    <div class="home87-brand-media"><img src="${asset("/assets/images/russian-bedroom.png")}" alt="Современная интерпретация русских традиций в интерьере" loading="lazy" /></div>
    <div class="home87-brand-copy">
      <small>О БРЕНДЕ</small>
      <h2>Традиции познаются в доме</h2>
      <p>Культура Дома переводит русские художественные традиции в современный интерьер — через материал, орнамент, цвет и домашние ритуалы.</p>
      <button type="button" data-home87-action="collections">Смотреть истории</button>
    </div>`;
  collections.before(story);
  story.querySelector<HTMLButtonElement>("[data-home87-action]")?.addEventListener("click", () => triggerHomeAction("collections"));
}

function enhanceSections(home: HTMLElement) {
  const categories = home.querySelector<HTMLElement>(".home81-categories");
  if (categories) {
    const small = categories.querySelector("header small");
    const title = categories.querySelector("header h2");
    const text = categories.querySelector("header p");
    if (small) small.textContent = "КАТАЛОГ";
    if (title) title.textContent = "Для каждой зоны дома";
    if (text) text.textContent = "Быстрый вход в основные категории — без перегруженной навигации.";
  }

  const collections = home.querySelector<HTMLElement>(".home81-collections");
  if (collections) {
    const copy = collections.querySelector<HTMLElement>(".home81-collections-hero > div");
    const small = collections.querySelector(".home81-collections-hero small");
    const title = collections.querySelector(".home81-collections-hero h2");
    const text = collections.querySelector(".home81-collections-hero p");
    const rail = collections.querySelector<HTMLElement>(".home81-collection-rail");
    if (small) small.textContent = "КОЛЛЕКЦИИ";
    if (title) title.textContent = "Коллекции для дома";
    if (text) text.textContent = "Редакционные истории, где цвет, орнамент и материал продолжаются от одного предмета к другому.";
    if (copy && rail) installRailControls(copy, rail, "Коллекции");
  }

  const solutions = home.querySelector<HTMLElement>(".home81-solutions");
  if (solutions) {
    const header = solutions.querySelector<HTMLElement>("header");
    const small = solutions.querySelector("header small");
    const title = solutions.querySelector("header h2");
    const text = solutions.querySelector("header p");
    const rail = solutions.querySelector<HTMLElement>(":scope > div");
    if (small) small.textContent = "ГОТОВЫЕ РЕШЕНИЯ";
    if (title) title.textContent = "Готовые решения для вашего дома";
    if (text) text.textContent = "Выберите готовую композицию как отправную точку, а затем адаптируйте её под своё пространство.";
    if (header && rail) installRailControls(header, rail, "Готовые решения");
  }
}

function enhanceHome() {
  const home = homeRoot();
  if (!home) return;
  if (home.dataset.home87 === "1" && home.querySelector(".home87-hero") && home.querySelector(".home87-brand-story")) return;
  home.dataset.home87 = "1";
  installHero(home);
  installBrandStory(home);
  enhanceSections(home);
}

export function HomeZaraTogasV86Enhancer() {
  useEffect(() => {
    enhanceHome();
    installCurrentCapsuleImages();
    const observer = new MutationObserver(() => {
      enhanceHome();
      installCurrentCapsuleImages();
    });
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);
  return null;
}
