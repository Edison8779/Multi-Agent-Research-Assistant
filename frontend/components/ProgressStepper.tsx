"use client";

import { CheckCircle2, Loader2, Search, Globe, Dna, FileText } from "lucide-react";

export type ResearchStage = "search" | "retrieve" | "extract" | "answer" | "completed" | "idle";

interface ProgressStepperProps {
  currentStage: ResearchStage;
  searchQueries?: string[];
  findingsCount?: number;
  sourcesCount?: number;
}

const STAGES = [
  {
    id: "search",
    title: "Search & Query Expansion",
    description: "Generating expanded queries & retrieving Tavily/Wiki search hits",
    icon: Search,
  },
  {
    id: "retrieve",
    title: "Document Retrieval",
    description: "Fetching web page contents concurrently via httpx scraper",
    icon: Globe,
  },
  {
    id: "extract",
    title: "Factual Claim Extraction",
    description: "Using LLM structured output to extract claims, evidence & confidence",
    icon: Dna,
  },
  {
    id: "answer",
    title: "Citation Synthesis",
    description: "Synthesizing citations into a structured Markdown research report",
    icon: FileText,
  },
];

export function ProgressStepper({
  currentStage,
  searchQueries = [],
  findingsCount = 0,
  sourcesCount = 0,
}: ProgressStepperProps) {
  if (currentStage === "idle") return null;

  const stageOrder = ["search", "retrieve", "extract", "answer", "completed"];
  const currentIdx = stageOrder.indexOf(currentStage);

  return (
    <div className="w-full max-w-4xl mx-auto my-6 p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-semibold text-indigo-400 tracking-wide uppercase flex items-center">
          <span className="w-2 h-2 rounded-full bg-indigo-500 mr-2 animate-ping" />
          Agent Pipeline Execution
        </h3>
        {currentStage === "completed" ? (
          <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium flex items-center">
            <CheckCircle2 className="w-3.5 h-3.5 mr-1" /> Workflow Complete
          </span>
        ) : (
          <span className="text-xs px-2.5 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 font-medium flex items-center">
            <Loader2 className="w-3.5 h-3.5 mr-1 animate-spin text-indigo-400" /> In Progress
          </span>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {STAGES.map((stage, idx) => {
          const Icon = stage.icon;
          const isDone = currentIdx > idx || currentStage === "completed";
          const isCurrent = stageOrder[idx] === currentStage;

          return (
            <div
              key={stage.id}
              className={`p-4 rounded-xl border transition-all ${
                isCurrent
                  ? "bg-indigo-950/40 border-indigo-500/60 shadow-lg shadow-indigo-500/10"
                  : isDone
                  ? "bg-slate-900/60 border-emerald-500/30 text-slate-300"
                  : "bg-slate-950/40 border-slate-850 opacity-50"
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div
                  className={`w-8 h-8 rounded-lg flex items-center justify-center ${
                    isDone
                      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                      : isCurrent
                      ? "bg-indigo-500/20 text-indigo-400 border border-indigo-500/40 animate-pulse"
                      : "bg-slate-800 text-slate-500"
                  }`}
                >
                  {isDone ? (
                    <CheckCircle2 className="w-4 h-4" />
                  ) : isCurrent ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Icon className="w-4 h-4" />
                  )}
                </div>
                <span className="text-xs font-mono text-slate-500">0{idx + 1}</span>
              </div>

              <h4 className="text-xs font-bold text-slate-200 mb-1">{stage.title}</h4>
              <p className="text-[11px] text-slate-400 leading-tight line-clamp-2">
                {stage.description}
              </p>

              {/* Dynamic Metadata badges */}
              {isDone && stage.id === "search" && searchQueries.length > 0 && (
                <div className="mt-2 text-[10px] text-indigo-300 bg-indigo-950/60 px-2 py-0.5 rounded border border-indigo-800/40 font-mono truncate">
                  {searchQueries.length} query generated
                </div>
              )}
              {isDone && stage.id === "retrieve" && sourcesCount > 0 && (
                <div className="mt-2 text-[10px] text-emerald-300 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40 font-mono truncate">
                  {sourcesCount} sources retrieved
                </div>
              )}
              {isDone && stage.id === "extract" && findingsCount > 0 && (
                <div className="mt-2 text-[10px] text-purple-300 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-800/40 font-mono truncate">
                  {findingsCount} claims extracted
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
