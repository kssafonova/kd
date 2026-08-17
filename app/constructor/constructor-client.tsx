"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { RemoteImage } from "../remote-image";
import { loadConstructorData } from "./data-client";
import {
  computeQuantity,
  createIndexes,
  formatRub,
  toNumber,
  trackConstructorEvent,
} from "./logic";
import { CONSTRUCTOR_SCENARIO_IDS } from "./scenarios";
import type { ConstructorData } from "./types";

const paletteColors: Record<string, string> = {
  red: "#9a3f3a",
  milk: "#eee8dc",
  white: "#f7f7f4",
  blue: "#7f9ab1",
  sky_blue: "#9db8cf",
  navy: "#243b59",
  gold: "#b49a65",
  green: "#647b67",
  beige: "#c8b49a",
  grey: "#999b98",
  pink: "#d6aaa5",
  black: "#262626",
  multicolor: "#9b7772",
};

export function ConstructorLanding() {
  const [data, setData] = useState<ConstructorData | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    loadConstructorData()
      .then((loaded) => active && setData(loaded))
      .catch((reason: unknown) => active && setError(reason instanceof Error ? reason.message : "Ошибка загрузки CSV"));
    trackConstructorEvent("constructor_opened");
    return () => {
      active = false;
    };
  }, []);

  const cards = useMemo(() => {
    if (!data) return [];
    const indexes = createIndexes(data);

    return CONSTRUCTOR_SCENARIO_IDS.map((scenarioId) => {
      const presets = data.presets
        .filter((row) => row.scenario_id === scenarioId)
        .sort((a, b) => Number(a.sort_order) - Number(b.sort_order));
      const meta = data.scenarios.filter((row) => row.scenario_id === scenarioId);
      if (!presets.length) return null;

      const defaultGuests = Number(presets[0].default_guests) || (presets[0].domain === "table" ? 2 : 1);
      const defaultRows = presets.filter((row) => row.preset_status !== "optional");
      const startPrice = defaultRows.reduce((sum, preset) => {
        const catalog = indexes.catalogByOffer.get(String(preset.offer_id));
        const price = toNumber(catalog?.price || preset.price_rub);
        return sum + (price ? price * computeQuantity(preset, defaultGuests) : 0);
      }, 0);

      const images = presets
        .map((preset) => indexes.catalogByOffer.get(String(preset.offer_id))?.primary_image_url || preset.primary_image_url)
        .filter((url) => url.startsWith("https://"))
        .slice(0, 4);

      const paletteTokens = Array.from(
        new Set(
          data.candidates
            .filter((row) => row.scenario_id === scenarioId)
            .flatMap((row) => row.palette.split("|"))
            .map((value) => value.trim().toLowerCase())
            .filter(Boolean),
        ),
      ).slice(0, 5);

      const description = Array.from(new Set(meta.map((row) => row.styling_message).filter(Boolean))).slice(0, 2).join(". ");

      return {
        scenarioId,
        name: meta[0]?.scenario_name || presets[0].scenario_name,
        description: description || presets[0].selection_reason,
        images,
        startPrice,
        itemCount: defaultRows.length,
        paletteTokens,
      };
    }).filter(Boolean) as Array<{
      scenarioId: string;
      name: string;
      description: string;
      images: string[];
      startPrice: number;
      itemCount: number;
      paletteTokens: string[];
    }>;
  }, [data]);

  if (error) {
    return <main className="constructor-shell"><div className="constructor-wrap constructor-empty"><h1>Не удалось загрузить данные конструктора</h1><p>{error}</p></div></main>;
  }

  if (!data) {
    return <main className="constructor-shell"><div className="constructor-wrap constructor-empty">Загружаем сценарии…</div></main>;
  }

  return (
    <main className="constructor-shell">
      <div className="constructor-wrap">
        <Link className="constructor-back" href="/">← КУЛЬТУРА ДОМА</Link>
        <header className="constructor-landing-head">
          <p className="constructor-kicker">EDITORIAL CONSTRUCTOR</p>
          <h1 className="constructor-title">Соберите сценарий</h1>
          <p className="constructor-lead">Пять готовых историй для сервировки и спальни. Выберите образ, настройте количество и заменяйте только совместимые предметы.</p>
        </header>

        <section className="constructor-scenario-grid" aria-label="Сценарии конструктора">
          {cards.map((card) => (
            <article className="constructor-scenario-card" key={card.scenarioId}>
              <div className="constructor-scenario-collage">
                {Array.from({ length: 3 }, (_, index) => {
                  const image = card.images[index];
                  return image ? (
                    <div key={`${image}-${index}`}>
                      <RemoteImage
                        src={image}
                        alt={`${card.name}, предмет сценария ${index + 1}`}
                        loading={index === 0 ? "eager" : "lazy"}
                      />
                    </div>
                  ) : (
                    <div className="constructor-image-fallback" key={`fallback-${index}`}>Фото товара недоступно</div>
                  );
                })}
              </div>
              <div className="constructor-scenario-copy">
                <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "flex-start" }}>
                  <div>
                    <p className="constructor-kicker">СЦЕНАРИЙ</p>
                    <h2>{card.name}</h2>
                  </div>
                  <div aria-label="Палитра" style={{ display: "flex", gap: 5, paddingTop: 5 }}>
                    {card.paletteTokens.map((token) => (
                      <i key={token} title={token} style={{ width: 15, height: 15, borderRadius: "50%", border: "1px solid #ddd", background: paletteColors[token] || "#9b9c99" }} />
                    ))}
                  </div>
                </div>
                <p>{card.description}</p>
                <div className="constructor-scenario-meta">
                  <div>
                    <span>{card.itemCount} позиций по умолчанию</span>
                    <strong>{card.startPrice > 0 ? `от ${formatRub(card.startPrice)}` : "Цена уточняется"}</strong>
                  </div>
                  <Link
                    className="constructor-primary-link"
                    href={`/constructor/${card.scenarioId}/`}
                    onClick={() => trackConstructorEvent("scenario_selected", { scenario_id: card.scenarioId })}
                  >
                    СОБРАТЬ ОБРАЗ →
                  </Link>
                </div>
              </div>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
