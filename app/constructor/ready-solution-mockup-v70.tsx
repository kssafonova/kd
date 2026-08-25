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

    // Preserve the successful null guard for nested callbacks/functions.
    const pageRoot = page;
    const heroRoot = hero;
    const personRoot = person;
    const groupsRoot = groups;
    const summaryRoot = summary;

    pageRoot.classList.add("v70-ready");
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
    heroRoot.insertAdjacentElement("afterend", nav);

    const result = document.createElement("section");
    result.className = "v70-result";
    result.innerHTML = `
      <header class="v70-result-head"><small>ВАШЕ РЕШЕНИЕ</small><h1></h1></header>
      <div class="v70-moodboard" aria-live="polite"></div>
      <div class="v70-result-groups"></div>
      <button type="button" class="v70-edit">Изменить состав</button>
    `;
    groupsRoot.insertAdjacentElement("afterend", result);
    const resultTitle = result.querySelector("h1")!;
    resultTitle.textContent = heroRoot.querySelector("h1")?.textContent || "Готовое решение";
    result.querySelector<HTMLButtonElement>(".v70-edit")?.addEventListener("click", () => setStep(2));

    const nextFromParams = document.createElement("button");
    nextFromParams.type = "button";
    nextFromParams.className = "v70-inline-next";
    nextFromParams.textContent = "К СОСТАВУ";
    nextFromParams.addEventListener("click", () => setStep(2));
    personRoot.appendChild(nextFromParams);

    const toResult = document.createElement("button");
    toResult.type = "button";
    toResult.className = "v70-inline-next v70-to-result";
    toResult.textContent = "ПЕРЕЙТИ К РЕЗУЛЬТАТУ";
    toResult.addEventListener("click", () => setStep(3));
    groupsRoot.appendChild(toResult);

    function selectedCards() {
      return Array.from(groupsRoot.querySelectorAll<HTMLElement>(".v54-product-card.is-selected"));
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
      Array.from(groupsRoot.querySelectorAll<HTMLElement>(".v54-group")).forEach((group) => {
        const count = group.querySelectorAll(".v54-product-card.is-selected").length;
        if (!count) return;
        const row = document.createElement("button");
        row.type = "button";
        row.innerHTML = `<span>${group.querySelector("h2")?.textContent || "Категория"} · ${count}</span><b>›</b>`;
        row.addEventListener("click", () => setStep(2));
        resultGroups.appendChild(row);
      });
    }

    const observer = new MutationObserver(() => syncResult());
    observer.observe(groupsRoot, { attributes: true, subtree: true, attributeFilter: ["class"] });

    function setStep(next: number) {
      step = next;
      pageRoot.dataset.v70Step = String(step);
      nav.querySelectorAll<HTMLButtonElement>("button").forEach((button) => {
        button.classList.toggle("is-active", Number(button.dataset.step) === step);
      });
      personRoot.hidden = step !== 1;
      groupsRoot.hidden = step !== 2;
      if (categoryNav) categoryNav.hidden = true;
      result.hidden = step !== 3;
      heroRoot.classList.toggle("is-compact", step !== 1);
      summaryRoot.classList.toggle("is-result", step === 3);
      syncResult();
      if (step > 1) nav.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    setStep(1);
    return () => observer.disconnect();
  }, []);

  return null;
}
