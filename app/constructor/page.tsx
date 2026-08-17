import type { Metadata } from "next";
import { ConstructorLanding } from "./constructor-client";

export const metadata: Metadata = {
  title: "Конструктор сценариев — Культура Дома",
  description: "Готовые сервировки и интерьерные сценарии из реальных товаров Культуры Дома.",
};

export default function ConstructorPage() {
  return <ConstructorLanding />;
}
