"use client";

import { ResearchFinding } from "@/types/research";
import { CheckCircle, ExternalLink, Quote, ShieldCheck, AlertTriangle } from "lucide-react";

interface FindingsGridProps {
  findings: ResearchFinding[];
}

export function FindingsGrid({ findings }: FindingsGridProps) {
  if (!findings || findings.length === 0) {
    return (
      <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 text-center text-slate-400">
        No structured factual claims extracted yet.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-base font-bold text-slate-100 flex items-center">
          <ShieldCheck className="w-5 h-5 text-indigo-400 mr-2" />
          Extracted Factual Claims ({findings.length})
        </h3>
        <span className="text-xs text-slate-400">
          Ranked by confidence score
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {findings.map((finding, idx) => {
          const confidencePct = Math.round(finding.confidence * 100);
          const isHighConfidence = finding.confidence >= 0.8;
          const isMedConfidence = finding.confidence >= 0.5;

          return (
            <div
              key={idx}
              className="flex flex-col justify-between p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/40 transition-all shadow-lg backdrop-blur-md group"
            >
              <div>
                {/* Header with confidence meter */}
                <div className="flex items-start justify-between gap-3 mb-3">
                  <h4 className="text-sm font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors leading-snug">
                    {finding.claim}
                  </h4>

                  {/* Confidence Badge */}
                  <div
                    className={`shrink-0 px-2.5 py-1 rounded-full text-xs font-mono font-bold flex items-center border ${
                      isHighConfidence
                        ? "bg-emerald-950/60 text-emerald-400 border-emerald-500/30"
                        : isMedConfidence
                        ? "bg-amber-950/60 text-amber-400 border-amber-500/30"
                        : "bg-rose-950/60 text-rose-400 border-rose-500/30"
                    }`}
                  >
                    {isHighConfidence ? (
                      <CheckCircle className="w-3 h-3 mr-1 text-emerald-400" />
                    ) : (
                      <AlertTriangle className="w-3 h-3 mr-1 text-amber-400" />
                    )}
                    {confidencePct}%
                  </div>
                </div>

                {/* Evidence snippet */}
                {finding.evidence && (
                  <div className="mb-4 p-3 rounded-xl bg-slate-950/60 border border-slate-850 text-xs text-slate-300 italic flex items-start space-x-2">
                    <Quote className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                    <span className="line-clamp-3">"{finding.evidence}"</span>
                  </div>
                )}
              </div>

              {/* Source Link */}
              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium truncate max-w-[200px]">
                  {finding.source_title || "Web Source"}
                </span>

                {finding.source_url && (
                  <a
                    href={finding.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center space-x-1 text-indigo-400 hover:text-indigo-300 font-medium transition-colors"
                  >
                    <span>View Source</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
