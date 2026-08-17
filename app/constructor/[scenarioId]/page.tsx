import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ScenarioConstructor } from "../scenario-client";
import { CONSTRUCTOR_SCENARIO_IDS, isConstructorScenarioId } from "../scenarios";

export const dynamicParams = false;

export function generateStaticParams() {
  return CONSTRUCTOR_SCENARIO_IDS.map((scenarioId) => ({ scenarioId }));
}

export async function generateMetadata({ params }: { params: Promise<{ scenarioId: string }> }): Promise<Metadata> {
  const { scenarioId } = await params;
  return {
    title: `${scenarioId} — Конструктор Культура Дома`,
    description: "Соберите готовый сценарий из совместимых товаров Культуры Дома.",
  };
}

export default async function ScenarioPage({ params }: { params: Promise<{ scenarioId: string }> }) {
  const { scenarioId } = await params;
  if (!isConstructorScenarioId(scenarioId)) notFound();
  return <ScenarioConstructor scenarioId={scenarioId} />;
}
