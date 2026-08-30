"use client";

import { useEffect } from "react";

const CATALOG_RESOURCE = "/data/catalog_master.csv";

export function CatalogLoadingStateV127() {
  useEffect(() => {
    const shell = document.querySelector<HTMLElement>(".view-catalog .catalog-v123");
    if (!shell) return;

    const hasProducts = () => Boolean(shell.querySelector(".product-grid .product-card"));
    const looksLikeInitialEmpty = () => {
      const count = shell.querySelector<HTMLElement>(".title-line > span")?.textContent?.trim() ?? "";
      return Boolean(shell.querySelector(".catalog-empty-v123")) && /^0\s/.test(count);
    };

    if (hasProducts() || !looksLikeInitialEmpty()) return;

    shell.classList.add("catalog-data-loading-v127");
    let settled = false;
    let settleTimer = 0;

    const finish = () => {
      if (settled) return;
      settled = true;
      shell.classList.remove("catalog-data-loading-v127");
      observer.disconnect();
      resourceObserver?.disconnect();
      window.clearTimeout(settleTimer);
    };

    const scheduleFinishAfterResource = () => {
      if (settled) return;
      window.clearTimeout(settleTimer);
      // Give the catalog's own React state update one paint after the CSV request settles.
      settleTimer = window.setTimeout(finish, 450);
    };

    const observer = new MutationObserver(() => {
      if (hasProducts() || !shell.querySelector(".catalog-empty-v123")) finish();
    });
    observer.observe(shell, { childList: true, subtree: true, characterData: true });

    const alreadyLoaded = performance
      .getEntriesByType("resource")
      .some((entry) => entry.name.includes(CATALOG_RESOURCE));

    let resourceObserver: PerformanceObserver | null = null;
    if (alreadyLoaded) {
      scheduleFinishAfterResource();
    } else if ("PerformanceObserver" in window) {
      resourceObserver = new PerformanceObserver((list) => {
        if (list.getEntries().some((entry) => entry.name.includes(CATALOG_RESOURCE))) {
          scheduleFinishAfterResource();
        }
      });
      try {
        resourceObserver.observe({ type: "resource", buffered: true });
      } catch {
        resourceObserver = null;
      }
    }

    // Safety valve: never leave the user in a permanent loading state if loading fails.
    const safetyTimer = window.setTimeout(finish, 7000);

    return () => {
      settled = true;
      shell.classList.remove("catalog-data-loading-v127");
      observer.disconnect();
      resourceObserver?.disconnect();
      window.clearTimeout(settleTimer);
      window.clearTimeout(safetyTimer);
    };
  }, []);

  return null;
}
