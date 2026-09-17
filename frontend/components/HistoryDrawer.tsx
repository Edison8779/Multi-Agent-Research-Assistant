"use client";

import { ResearchHistoryItem } from "@/types/research";
import { X, Trash2, Clock, ChevronRight, FileText } from "lucide-react";

interface HistoryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  history: ResearchHistoryItem[];
  onSelectHistory: (item: ResearchHistoryItem) => void;
  onClearHistory: () => void;
}

export function HistoryDrawer({
  isOpen,
  onClose,
  history,
  onSelectHistory,
  onClearHistory,
}: HistoryDrawerProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        onClick={onClose}
        className="fixed inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity"
      />

      {/* Drawer Panel */}
      <div className="relative w-full max-w-md bg-slate-900 border-l border-slate-800 h-full flex flex-col shadow-2xl z-10">
        {/* Drawer Header */}
        <div className="p-5 border-b border-slate-800 flex items-center justify-between bg-slate-950/40">
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-slate-100">Research History</h2>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Drawer Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {history.length === 0 ? (
            <div className="text-center py-12 text-slate-500 space-y-2">
              <FileText className="w-10 h-10 mx-auto opacity-40 text-indigo-400" />
              <p className="text-sm">No research history saved yet.</p>
              <p className="text-xs text-slate-600">
                Your completed research prompts will appear here.
              </p>
            </div>
          ) : (
            history.map((item) => (
              <div
                key={item.id}
                onClick={() => {
                  onSelectHistory(item);
                  onClose();
                }}
                className="group p-4 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-indigo-500/50 hover:bg-indigo-950/20 cursor-pointer transition-all space-y-2"
              >
                <div className="flex items-center justify-between text-[11px] text-slate-400 font-mono">
                  <span>{new Date(item.timestamp).toLocaleString()}</span>
                  <span className="text-indigo-400 group-hover:translate-x-0.5 transition-transform">
                    <ChevronRight className="w-3.5 h-3.5" />
                  </span>
                </div>

                <h3 className="text-sm font-semibold text-slate-200 group-hover:text-indigo-300 transition-colors line-clamp-2">
                  {item.question}
                </h3>

                <div className="flex items-center space-x-3 text-[11px] text-slate-400 font-medium">
                  <span>{item.response.findings?.length || 0} claims</span>
                  <span>•</span>
                  <span>{item.response.retrieved_documents?.length || 0} sources</span>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Drawer Footer */}
        {history.length > 0 && (
          <div className="p-4 border-t border-slate-800 bg-slate-950/40">
            <button
              onClick={onClearHistory}
              className="w-full flex items-center justify-center space-x-2 px-4 py-2.5 rounded-xl bg-rose-950/30 hover:bg-rose-900/40 border border-rose-800/40 text-rose-400 text-xs font-medium transition-colors"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear History</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
