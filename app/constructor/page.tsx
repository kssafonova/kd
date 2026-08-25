import type { Metadata } from "next";
import { ReadySolutionsLandingV54 } from "./ready-solutions-v54";

export const metadata: Metadata = {
  title: "Готовые решения — Культура Дома",
  description: "Готовые сервировки и интерьерные решения Культура Дома: выберите количество персон, настройте категории и добавьте выбранный состав в корзину.",
};

export default function ConstructorPage() {
  return <ReadySolutionsLandingV54 />;
}
