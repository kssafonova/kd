import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { EDITORIAL_SCENARIOS, EDITORIAL_SCENARIO_IDS, getEditorialScenario } from "../../../editorial-scenario-config";
import { EditorialScenarioStory } from "./story-client";

export const dynamicParams = false;

export function generateStaticParams() {
  return EDITORIAL_SCENARIO_IDS.map((scenarioId) => ({ scenarioId }));
}

export async function generateMetadata({ params }: { params: Promise<{ scenarioId: string }> }): Promise<Metadata> {
  const { scenarioId } = await params;
  const scenario = getEditorialScenario(scenarioId);
  return {
    title: scenario ? `${scenario.name} — Editorial | Культура Дома` : "Editorial | Культура Дома",
    description: scenario?.lead ?? "Editorial-сценарий Культура Дома.",
  };
}

export default async function EditorialScenarioPage({ params }: { params: Promise<{ scenarioId: string }> }) {
  const { scenarioId } = await params;
  if (!EDITORIAL_SCENARIOS.some((item) => item.id === scenarioId)) notFound();
  return <EditorialScenarioStory scenarioId={scenarioId} />;
}
