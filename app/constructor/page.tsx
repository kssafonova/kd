import type { Metadata } from "next";
import { ReadySolutionsLandingV52 } from "./ready-solutions-v52";

export const metadata: Metadata = {
  title: "Готовые решения — Культура Дома",
  description: "Готовые сервировки и интерьерные решения внутри витрины Культура Дома — с покупкой отдельных предметов и настройкой всего состава.",
};

export default function ConstructorPage() {
  return <ReadySolutionsLandingV52 />;
}
