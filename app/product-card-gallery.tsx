"use client";

import { useEffect } from "react";

const TRACK_SELECTOR = ".product-card .product-image .product-media-scroll.horizontal-media.is-scrollable";

export function ProductCardGalleryEnhancer() {
  useEffect(() => {
    const enhanceTrack = (track: HTMLElement) => {
      if (track.dataset.cardGalleryEnhanced === "true") return;

      const shell = track.closest<HTMLElement>(".product-image");
      if (!shell) return;

      const getSlides = () => Array.from(track.querySelectorAll<HTMLImageElement>(":scope > img"));
      if (getSlides().length < 2) return;

      track.dataset.cardGalleryEnhanced = "true";
      shell.classList.add("product-image-gallery");

      const previous = document.createElement("div");
      previous.className = "product-card-gallery-nav product-card-gallery-prev";
      previous.setAttribute("aria-hidden", "true");

      const next = document.createElement("div");
      next.className = "product-card-gallery-nav product-card-gallery-next";
      next.setAttribute("aria-hidden", "true");

      const dots = document.createElement("div");
      dots.className = "product-card-gallery-dots";
      dots.setAttribute("aria-hidden", "true");

      shell.append(previous, next, dots);

      let currentIndex = 0;
      let scrollFrame = 0;
      let dragging = false;
      let moved = false;
      let startX = 0;
      let startScrollLeft = 0;
      let suppressClickUntil = 0;

      const clampIndex = (index: number) => {
        const total = getSlides().length;
        return Math.max(0, Math.min(total - 1, index));
      };

      const renderDots = () => {
        const total = getSlides().length;
        dots.replaceChildren(
          ...Array.from({ length: total }, (_, index) => {
            const dot = document.createElement("i");
            dot.className = `product-card-gallery-dot${index === currentIndex ? " active" : ""}`;
            return dot;
          }),
        );
        previous.classList.toggle("is-disabled", currentIndex <= 0);
        next.classList.toggle("is-disabled", currentIndex >= total - 1);
      };

      const syncIndexFromScroll = () => {
        const width = track.clientWidth || 1;
        const nextIndex = clampIndex(Math.round(track.scrollLeft / width));
        if (nextIndex !== currentIndex) {
          currentIndex = nextIndex;
          renderDots();
        }
      };

      const scheduleSync = () => {
        if (scrollFrame) cancelAnimationFrame(scrollFrame);
        scrollFrame = requestAnimationFrame(syncIndexFromScroll);
      };

      const scrollToIndex = (index: number, behavior: ScrollBehavior = "smooth") => {
        const slides = getSlides();
        const nextIndex = clampIndex(index);
        const target = slides[nextIndex];
        if (!target) return;
        currentIndex = nextIndex;
        renderDots();
        track.scrollTo({ left: target.offsetLeft, top: 0, behavior });
      };

      const stopCardOpen = (event: Event) => {
        event.preventDefault();
        event.stopPropagation();
      };

      const onPrevious = (event: Event) => {
        stopCardOpen(event);
        scrollToIndex(currentIndex - 1);
      };

      const onNext = (event: Event) => {
        stopCardOpen(event);
        scrollToIndex(currentIndex + 1);
      };

      const onKeyDown = (event: KeyboardEvent) => {
        if (event.key === "ArrowLeft") {
          event.preventDefault();
          event.stopPropagation();
          scrollToIndex(currentIndex - 1);
        }
        if (event.key === "ArrowRight") {
          event.preventDefault();
          event.stopPropagation();
          scrollToIndex(currentIndex + 1);
        }
      };

      const onPointerDown = (event: PointerEvent) => {
        if (event.pointerType !== "mouse" || event.button !== 0) return;
        dragging = true;
        moved = false;
        startX = event.clientX;
        startScrollLeft = track.scrollLeft;
        track.setPointerCapture?.(event.pointerId);
        shell.classList.add("is-dragging");
      };

      const onPointerMove = (event: PointerEvent) => {
        if (!dragging) return;
        const delta = event.clientX - startX;
        if (Math.abs(delta) > 4) moved = true;
        if (!moved) return;
        event.preventDefault();
        track.scrollLeft = startScrollLeft - delta;
      };

      const finishDrag = (event: PointerEvent) => {
        if (!dragging) return;
        dragging = false;
        shell.classList.remove("is-dragging");
        try {
          track.releasePointerCapture?.(event.pointerId);
        } catch {
          // Pointer can already be released by the browser.
        }
        if (moved) {
          suppressClickUntil = Date.now() + 350;
          const width = track.clientWidth || 1;
          scrollToIndex(Math.round(track.scrollLeft / width));
        }
      };

      const onTrackClickCapture = (event: MouseEvent) => {
        if (Date.now() < suppressClickUntil) stopCardOpen(event);
      };

      const childObserver = new MutationObserver(() => {
        currentIndex = clampIndex(currentIndex);
        renderDots();
        scheduleSync();
      });

      previous.addEventListener("pointerdown", stopCardOpen);
      next.addEventListener("pointerdown", stopCardOpen);
      previous.addEventListener("click", onPrevious);
      next.addEventListener("click", onNext);
      shell.addEventListener("keydown", onKeyDown);
      track.addEventListener("scroll", scheduleSync, { passive: true });
      track.addEventListener("pointerdown", onPointerDown);
      track.addEventListener("pointermove", onPointerMove);
      track.addEventListener("pointerup", finishDrag);
      track.addEventListener("pointercancel", finishDrag);
      track.addEventListener("click", onTrackClickCapture, true);
      childObserver.observe(track, { childList: true });

      const resizeObserver = typeof ResizeObserver !== "undefined" ? new ResizeObserver(scheduleSync) : null;
      resizeObserver?.observe(track);

      renderDots();
      scheduleSync();
    };

    const scan = () => {
      document.querySelectorAll<HTMLElement>(TRACK_SELECTOR).forEach(enhanceTrack);
    };

    scan();
    const observer = new MutationObserver(scan);
    observer.observe(document.body, { childList: true, subtree: true });

    return () => {
      observer.disconnect();
    };
  }, []);

  return null;
}
