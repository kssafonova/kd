import type { Metadata } from "next";
import { ReadySolutionsLandingV47 } from "./ready-solutions-v47";

export const metadata: Metadata = {
  title: "Готовые решения — Культура Дома",
  description: "Готовые сервировки и интерьерные решения, которые можно настроить по составу, цвету, размеру и количеству.",
};

export default function ConstructorPage() {
  return <ReadySolutionsLandingV47 />;
}
