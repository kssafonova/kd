import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ReadySolutionWizard } from "../ready-solutions-client";
import { TABLE_SOLUTIONS, findTableSolution } from "../../constructor/table-solutions";

export const dynamicParams = false;

export function generateStaticParams() {
  return TABLE_SOLUTIONS.map((solution) => ({ scenarioId: solution.id }));
}

export async function generateMetadata({ params }: { params: Promise<{ scenarioId: string }> }): Promise<Metadata> {
  const { scenarioId } = await params;
  const solution = findTableSolution(scenarioId);
  return {
    title: `${solution?.name ?? "Готовое решение"} — Культура Дома`,
    description: solution ? `Настройте готовое решение «${solution.name}»: количество персон, категории, товары, размеры и цвета.` : "Конструктор готового решения Культура Дома.",
  };
}

export default async function ReadySolutionPage({ params }: { params: Promise<{ scenarioId: string }> }) {
  const { scenarioId } = await params;
  if (!findTableSolution(scenarioId)) notFound();
  return <ReadySolutionWizard scenarioId={scenarioId} />;
}
