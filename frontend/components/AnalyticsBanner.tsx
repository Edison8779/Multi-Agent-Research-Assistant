"use client";

import { ResearchResponse } from "@/types/research";
import { Globe, ShieldCheck, Zap, Search } from "lucide-react";

interface AnalyticsBannerProps {
  response: ResearchResponse;
}

export function AnalyticsBanner({ response }: AnalyticsBannerProps) {
  const sourcesCount = response.retrieved_documents?.length || response.search_results?.length || 0;
  const claimsCount = response.findings?.length || 0;
  const queriesCount = response.search_queries?.length || 1;

  const avgConfidence =
    claimsCount > 0
      ? Math.round(
          (response.findings.reduce((acc, f) => acc + (f.confidence || 0), 0) / claimsCount) * 100
        )
      : 0;

  const stats = [
    {
      label: "Sources Scraped",
      value: sourcesCount,
      icon: Globe,
      color: "text-blue-400",
      bg: "bg-blue-500/10 border-blue-500/20",
    },
    {
      label: "Claims Extracted",
      value: claimsCount,
      icon: ShieldCheck,
      color: "text-purple-400",
      bg: "bg-purple-500/10 border-purple-500/20",
    },
    {
      label: "Avg Confidence",
      value: `${avgConfidence}%`,
      icon: Zap,
      color: "text-emerald-400",
      bg: "bg-emerald-500/10 border-emerald-500/20",
    },
    {
      label: "Search Queries",
      value: queriesCount,
      icon: Search,
      color: "text-indigo-400",
      bg: "bg-indigo-500/10 border-indigo-500/20",
    },
  ];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 my-6">
      {stats.map((stat, idx) => {
        const Icon = stat.icon;
        return (
          <div
            key={idx}
            className={`p-4 rounded-2xl border ${stat.bg} backdrop-blur-md flex items-center space-x-3 shadow-md`}
          >
            <div className={`p-2.5 rounded-xl bg-slate-900/80 ${stat.color}`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xl sm:text-2xl font-extrabold text-slate-100 tracking-tight">
                {stat.value}
              </p>
              <p className="text-xs font-medium text-slate-400">{stat.label}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
