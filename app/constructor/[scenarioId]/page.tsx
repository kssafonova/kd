import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ScenarioConstructor } from "../scenario-client";
import { TableSolutionDetail } from "../table-solution-client";
import { CONSTRUCTOR_SCENARIO_IDS, isRoutableConstructorScenarioId } from "../scenarios";
import { findTableSolution } from "../table-solutions";

export const dynamicParams = false;

export function generateStaticParams() {
  return CONSTRUCTOR_SCENARIO_IDS.map((scenarioId) => ({ scenarioId }));
}

export async function generateMetadata({ params }: { params: Promise<{ scenarioId: string }> }): Promise<Metadata> {
  const { scenarioId } = await params;
  const solution = findTableSolution(scenarioId);
  return {
    title: `${solution?.name ?? scenarioId} — Готовые решения Культура Дома`,
    description: solution
      ? `${solution.space}. Готовое решение из коллекций ${solution.collections.join(", ")}.`
      : "Соберите готовый сценарий из совместимых товаров Культуры Дома.",
  };
}

export default async function ScenarioPage({ params }: { params: Promise<{ scenarioId: string }> }) {
  const { scenarioId } = await params;
  if (!isRoutableConstructorScenarioId(scenarioId)) notFound();
  if (findTableSolution(scenarioId)) return <TableSolutionDetail scenarioId={scenarioId} />;
  return <ScenarioConstructor scenarioId={scenarioId} />;
}
