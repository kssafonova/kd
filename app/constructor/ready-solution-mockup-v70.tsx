"use client";

import { useEffect } from "react";

const STEP_LABELS = ["Параметры", "Состав", "Результат"] as const;

export function ReadySolutionMockupV70() {
  useEffect(() => {
    const page = document.querySelector<HTMLElement>(".v54-ready-page");
    const hero = page?.querySelector<HTMLElement>(".v54-hero");
    const person = page?.querySelector<HTMLElement>(".v54-person-step");
    const groups = page?.querySelector<HTMLElement>(".v54-groups");
    const categoryNav = page?.querySelector<HTMLElement>(".v54-category-nav");
    const summary = page?.querySelector<HTMLElement>(".v54-summary");
    if (!page || !hero || !person || !groups || !summary || page.classList.contains("v70-ready")) return;

    const readyPage = page;
    const readyGroups = groups;
    readyPage.classList.add("v70-ready");
    let step = 1;

    const nav = document.createElement("nav");
    nav.className = "v70-steps";
    nav.setAttribute("aria-label", "Шаги готового решения");
    STEP_LABELS.forEach((label, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.step = String(index + 1);
      button.innerHTML = `<span>0${index + 1}</span><b>${label}</b>`;
      button.addEventListener("click", () => setStep(index + 1));
      nav.appendChild(button);
    });
    hero.insertAdjacentElement("afterend", nav);

    const result = document.createElement("section");
    result.className = "v70-result";
    result.innerHTML = `
      <header class="v70-result-head">
        <small>ВАШЕ РЕШЕНИЕ</small>
        <h1></h1>
        <p>Собранные предметы показаны вместе. Нажмите на категорию, чтобы посмотреть её состав.</p>
      </header>
      <div class="v70-moodboard" aria-live="polite"></div>
      <div class="v70-result-groups" aria-label="Состав решения по категориям"></div>
      <button type="button" class="v70-edit">Изменить состав</button>
    `;
    readyGroups.insertAdjacentElement("afterend", result);
    const resultTitle = result.querySelector("h1")!;
    resultTitle.textContent = hero.querySelector("h1")?.textContent || "Готовое решение";
    result.querySelector<HTMLButtonElement>(".v70-edit")?.addEventListener("click", () => setStep(2));

    const flowbar = document.createElement("div");
    flowbar.className = "v70-flowbar";
    flowbar.innerHTML = `
      <div class="v70-flowbar-copy"><small></small><strong></strong></div>
      <button type="button"></button>
    `;
    readyPage.appendChild(flowbar);
    const flowbarSmall = flowbar.querySelector("small")!;
    const flowbarStrong = flowbar.querySelector("strong")!;
    const flowbarButton = flowbar.querySelector<HTMLButtonElement>("button")!;
    flowbarButton.addEventListener("click", () => setStep(step === 1 ? 2 : 3));

    const nativeSummaryButton = summary.querySelector<HTMLButtonElement>("button");
    if (nativeSummaryButton) nativeSummaryButton.textContent = "ДОБАВИТЬ В КОРЗИНУ";

    function selectedCards() {
      return Array.from(readyGroups.querySelectorAll<HTMLElement>(".v54-product-card.is-selected"));
    }

    function productMeta(card: HTMLElement) {
      const name = card.querySelector<HTMLElement>(".v54-product-info strong")?.textContent?.trim() || "Товар";
      const subtitle = card.querySelector<HTMLElement>(".v54-product-info small")?.textContent?.trim() || "";
      const price = card.querySelector<HTMLElement>(".v54-product-info > span")?.textContent?.trim() || "";
      const color = card.querySelector<HTMLButtonElement>(".v54-color-options button.is-active")?.textContent?.trim() || "";
      const size = card.querySelector<HTMLSelectElement>(".v54-size-control select")?.value || "";
      const qtySpans = card.querySelectorAll<HTMLElement>(".v54-qty-control > div:last-child span");
      const quantity = qtySpans.length ? qtySpans[qtySpans.length - 1]?.textContent?.trim() || "1" : "1";
      return { name, subtitle, price, color, size, quantity };
    }

    function makeResultItem(card: HTMLElement) {
      const item = document.createElement("div");
      item.className = "v70-result-item";

      const media = document.createElement("div");
      media.className = "v70-result-item-media";
      const image = card.querySelector(".v54-product-media img")?.cloneNode(true);
      if (image) media.appendChild(image);

      const copy = document.createElement("div");
      copy.className = "v70-result-item-copy";
      const meta = productMeta(card);
      const details = [meta.subtitle, meta.color, meta.size, `${meta.quantity} шт.`].filter(Boolean).join(" · ");
      copy.innerHTML = `<strong>${meta.name}</strong><small>${details}</small>`;

      const price = document.createElement("span");
      price.className = "v70-result-item-price";
      price.textContent = meta.price;

      item.append(media, copy, price);
      return item;
    }

    function syncResult() {
      const mood = result.querySelector<HTMLElement>(".v70-moodboard")!;
      const resultGroups = result.querySelector<HTMLElement>(".v70-result-groups")!;
      mood.replaceChildren();
      resultGroups.replaceChildren();

      const cards = selectedCards();
      cards.forEach((card, index) => {
        const media = card.querySelector<HTMLElement>(".v54-product-media");
        if (!media) return;
        const tile = document.createElement("div");
        tile.className = `v70-mood-tile v70-tile-${(index % 7) + 1}`;
        const image = media.querySelector("img")?.cloneNode(true);
        if (image) tile.appendChild(image);
        mood.appendChild(tile);
      });

      Array.from(readyGroups.querySelectorAll<HTMLElement>(".v54-group")).forEach((group) => {
        const selectedInGroup = Array.from(group.querySelectorAll<HTMLElement>(".v54-product-card.is-selected"));
        if (!selectedInGroup.length) return;

        const title = group.querySelector("h2")?.textContent?.trim() || "Категория";
        const details = document.createElement("details");
        details.className = "v70-result-category";

        const heading = document.createElement("summary");
        heading.innerHTML = `
          <span>${title}</span>
          <small>${selectedInGroup.length} ${selectedInGroup.length === 1 ? "предмет" : selectedInGroup.length < 5 ? "предмета" : "предметов"}</small>
          <b aria-hidden="true">+</b>
        `;

        const panel = document.createElement("div");
        panel.className = "v70-result-category-panel";
        selectedInGroup.forEach((card) => panel.appendChild(makeResultItem(card)));

        details.append(heading, panel);
        resultGroups.appendChild(details);
      });

      updateFlowbar();
    }

    function updateFlowbar() {
      const count = selectedCards().length;
      if (step === 1) {
        flowbarSmall.textContent = "ШАГ 1 ИЗ 3";
        flowbarStrong.textContent = "Параметры решения";
        flowbarButton.textContent = "К СОСТАВУ";
      } else if (step === 2) {
        flowbarSmall.textContent = count ? `ВЫБРАНО ${count}` : "ВЫБЕРИТЕ ПРЕДМЕТЫ";
        flowbarStrong.textContent = "Состав решения";
        flowbarButton.textContent = "К РЕЗУЛЬТАТУ";
        flowbarButton.disabled = count === 0;
      }
      if (step !== 2) flowbarButton.disabled = false;

      const resultTab = nav.querySelector<HTMLButtonElement>('button[data-step="3"]');
      if (resultTab) resultTab.disabled = count === 0 && step !== 3;
    }

    const observer = new MutationObserver(() => syncResult());
    observer.observe(readyGroups, { attributes: true, subtree: true, attributeFilter: ["class"] });

    function setStep(next: number) {
      if (next === 3 && selectedCards().length === 0) return;
      step = next;
      readyPage.dataset.v70Step = String(step);
      nav.querySelectorAll<HTMLButtonElement>("button").forEach((button) => {
        button.classList.toggle("is-active", Number(button.dataset.step) === step);
      });

      person.hidden = step !== 1;
      readyGroups.hidden = step !== 2;
      if (categoryNav) categoryNav.hidden = true;
      result.hidden = step !== 3;
      hero.hidden = step === 3;
      hero.classList.toggle("is-compact", step === 2);

      flowbar.hidden = step === 3;
      summary.hidden = step !== 3;
      if (nativeSummaryButton) nativeSummaryButton.textContent = "ДОБАВИТЬ В КОРЗИНУ";

      syncResult();
      updateFlowbar();
      if (step > 1) nav.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    setStep(1);
    return () => observer.disconnect();
  }, []);

  return null;
}
