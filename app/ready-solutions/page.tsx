import type { Metadata } from "next";
import { ReadySolutionsLanding } from "./ready-solutions-client";

export const metadata: Metadata = {
  title: "Готовые решения — Культура Дома",
  description: "Готовые интерьерные и сервировочные решения Культура Дома: выберите сценарий и настройте состав под своё пространство.",
};

export default function ReadySolutionsPage() {
  return <ReadySolutionsLanding />;
}
