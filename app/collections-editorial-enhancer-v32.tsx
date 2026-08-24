"use client";

import { useEffect } from "react";

const normalize = (value: string) => value.trim().toLocaleUpperCase("ru-RU");

export function CollectionsEditorialEnhancerV32() {
  useEffect(() => {
    const enhance = (root: HTMLElement) => {
      if (root.dataset.kdCollectionsV32 === "true") return;
      const grid = root.querySelector<HTMLElement>(".collections-v23-grid");
      const head = root.querySelector<HTMLElement>(".collections-v23-head");
      if (!grid || !head) return;

      const cards = Array.from(grid.querySelectorAll<HTMLElement>(".collections-v23-card"));
      if (!cards.length) return;

      root.dataset.kdCollectionsV32 = "true";
      cards.forEach((card) => {
        const kind = normalize(card.querySelector(".collections-v23-card-copy small")?.textContent || "");
        card.dataset.editorialKind = kind.includes("КАПСУЛ") ? "capsule" : "collection";
      });

      const tabs = document.createElement("nav");
      tabs.className = "collections-v32-tabs";
      tabs.setAttribute("aria-label", "Фильтр капсул и коллекций");

      const count = document.createElement("span");
      count.className = "collections-v32-count";

      const controls = document.createElement("div");
      controls.className = "collections-v32-tab-controls";

      const definitions = [
        { id: "all", label: "Все" },
        { id: "capsule", label: "Капсулы" },
        { id: "collection", label: "Коллекции" },
      ];

      const apply = (filter: string) => {
        let visibleCount = 0;
        let featuredAssigned = false;
        cards.forEach((card) => {
          const visible = filter === "all" || card.dataset.editorialKind === filter;
          card.hidden = !visible;
          card.classList.remove("collections-v32-feature");
          if (visible) {
            visibleCount += 1;
            if (!featuredAssigned) {
              card.classList.add("collections-v32-feature");
              featuredAssigned = true;
            }
          }
        });
        count.textContent = `${visibleCount} ${visibleCount === 1 ? "история" : visibleCount > 1 && visibleCount < 5 ? "истории" : "историй"}`;
        controls.querySelectorAll("button").forEach((button) => button.classList.toggle("active", (button as HTMLButtonElement).dataset.filter === filter));
      };

      definitions.forEach(({ id, label }) => {
        const button = document.createElement("button");
        button.type = "button";
        button.dataset.filter = id;
        button.textContent = label;
        button.addEventListener("click", () => apply(id));
        controls.appendChild(button);
      });

      tabs.append(controls, count);
      head.insertAdjacentElement("afterend", tabs);
      apply("all");
    };

    const scan = () => document.querySelectorAll<HTMLElement>(".collections-v23").forEach(enhance);
    scan();
    const observer = new MutationObserver(scan);
    observer.observe(document.body, { childList: true, subtree: true });
    return () => observer.disconnect();
  }, []);

  return null;
}
