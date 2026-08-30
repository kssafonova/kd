"use client";

import { useEffect } from "react";

const setText = (node: Element | null, value: string) => {
  if (node && node.textContent !== value) node.textContent = value;
};

function enhanceCart(root: HTMLElement) {
  root.classList.add("kd-cart-v136");

  const titleCopy = root.querySelector<HTMLElement>(".cart-v43-title p");
  setText(titleCopy, "Проверьте товары перед оформлением. Количество и упаковку можно изменить здесь.");

  const summary = root.querySelector<HTMLElement>(".cart-v43-summary-inner");
  if (!summary) return;
  summary.setAttribute("aria-live", "polite");

  setText(summary.querySelector(":scope > small"), "ВАШ ЗАКАЗ");

  const dl = summary.querySelector<HTMLElement>("dl");
  const rows = Array.from(summary.querySelectorAll<HTMLElement>("dl > div"));
  const goodsRow = rows.find((row) => row.querySelector("dt")?.textContent?.trim() === "Товары");
  const goodsValue = goodsRow?.querySelector("dd")?.textContent?.trim() || "";

  rows.forEach((row) => {
    const label = row.querySelector("dt")?.textContent?.trim();
    if (label === "Курьер" || label === "Пункт выдачи") row.classList.add("kd-v136-hide-delivery-row");
  });

  if (dl && !summary.querySelector(".kd-cart-delivery-line")) {
    const line = document.createElement("div");
    line.className = "kd-cart-delivery-line";
    const label = document.createElement("span");
    label.textContent = "Доставка";
    const value = document.createElement("b");
    value.textContent = "Выберете на следующем шаге";
    line.append(label, value);
    dl.insertAdjacentElement("afterend", line);
  }

  const total = summary.querySelector<HTMLElement>(".cart-v43-total");
  if (total) {
    setText(total.querySelector("span"), "Итого без доставки");
    if (goodsValue) setText(total.querySelector("b"), goodsValue);
  }

  const note = summary.querySelector<HTMLElement>(":scope > p");
  setText(note, "Способ и стоимость доставки выберете на следующем шаге. Итог обновится до подтверждения заказа.");
}

const stepNames = ["Контакты", "Получение", "Оплата", "Проверка"];

function addSectionError(section: HTMLElement | undefined, text: string, show: boolean) {
  if (!section) return;
  let error = section.querySelector<HTMLElement>(":scope > .kd-checkout-inline-error");
  if (!show) {
    error?.remove();
    return;
  }
  if (!error) {
    error = document.createElement("div");
    error.className = "kd-checkout-inline-error";
    error.setAttribute("role", "alert");
    section.appendChild(error);
  }
  setText(error, text);
}

function syncInlineErrors(root: HTMLElement, sections: HTMLElement[]) {
  const aggregate = root.querySelector<HTMLElement>(".checkout-v69-errors");
  const text = aggregate?.textContent?.toLocaleLowerCase("ru-RU") || "";
  const hasErrors = Boolean(text.trim());

  addSectionError(
    sections[0],
    "Проверьте обязательные контактные данные и подтверждение телефона.",
    hasErrors && /(имя|телефон|email)/i.test(text),
  );
  addSectionError(
    sections[1],
    "Заполните данные получения заказа.",
    hasErrors && /достав/i.test(text),
  );
  addSectionError(
    sections[3],
    "Подтвердите согласие с условиями перед оформлением.",
    hasErrors && /соглас/i.test(text),
  );
}

function enhanceCheckout(root: HTMLElement) {
  root.classList.add("kd-checkout-v136");

  const main = root.querySelector<HTMLElement>(".checkout-v69-main");
  const title = root.querySelector<HTMLElement>(".checkout-v69-title");
  if (!main || !title) return;

  if (!title.querySelector(".kd-checkout-intro")) {
    const intro = document.createElement("p");
    intro.className = "kd-checkout-intro";
    intro.textContent = "Контакты, получение, оплата и проверка — на одном экране. Регистрация не нужна для оформления заказа.";
    title.appendChild(intro);
  }

  const sections = Array.from(main.querySelectorAll<HTMLElement>(":scope > .checkout-v69-section"));
  sections.slice(0, 4).forEach((section, index) => {
    section.dataset.kdStep = `${String(index + 1).padStart(2, "0")} · ${stepNames[index]}`;
    section.id ||= `kd-checkout-step-${index + 1}`;
  });

  if (!main.querySelector(":scope > .kd-checkout-progress")) {
    const nav = document.createElement("nav");
    nav.className = "kd-checkout-progress";
    nav.setAttribute("aria-label", "Этапы оформления заказа");

    stepNames.forEach((name, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.kdStepTarget = String(index);
      button.className = index === 0 ? "is-active" : "";
      button.setAttribute("aria-label", `Перейти к этапу ${index + 1}: ${name}`);
      const number = document.createElement("span");
      number.textContent = String(index + 1).padStart(2, "0");
      const label = document.createElement("b");
      label.textContent = name;
      button.append(number, label);
      button.addEventListener("click", () => {
        const target = sections[index];
        if (!target) return;
        const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
        target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
      });
      nav.appendChild(button);
    });
    title.insertAdjacentElement("afterend", nav);
  }

  syncInlineErrors(root, sections);
}

function enhanceAll() {
  document.querySelectorAll<HTMLElement>(".cart-v43.cart-v69").forEach(enhanceCart);
  document.querySelectorAll<HTMLElement>(".checkout-v69").forEach(enhanceCheckout);
}

function syncProgress() {
  const root = document.querySelector<HTMLElement>(".kd-checkout-v136");
  if (!root) return;
  const sections = Array.from(root.querySelectorAll<HTMLElement>(".checkout-v69-main > .checkout-v69-section")).slice(0, 4);
  const buttons = Array.from(root.querySelectorAll<HTMLElement>(".kd-checkout-progress button"));
  if (!sections.length || !buttons.length) return;

  const headerOffset = window.innerWidth <= 760 ? 120 : 132;
  let active = 0;
  sections.forEach((section, index) => {
    if (section.getBoundingClientRect().top <= headerOffset + 24) active = index;
  });
  buttons.forEach((button, index) => {
    button.classList.toggle("is-active", index === active);
    if (index === active) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
  });
}

export function CartCheckoutHumanEyeV136Enhancer() {
  useEffect(() => {
    let frame = 0;
    const run = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        enhanceAll();
        syncProgress();
      });
    };

    run();
    const observer = new MutationObserver(run);
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    window.addEventListener("scroll", syncProgress, { passive: true });
    window.addEventListener("resize", syncProgress);

    return () => {
      cancelAnimationFrame(frame);
      observer.disconnect();
      window.removeEventListener("scroll", syncProgress);
      window.removeEventListener("resize", syncProgress);
    };
  }, []);

  return null;
}
