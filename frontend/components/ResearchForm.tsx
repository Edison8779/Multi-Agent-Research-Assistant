"use client";

import { useState } from "react";
import { Search, Loader2, Sparkles, X, ArrowRight } from "lucide-react";

interface ResearchFormProps {
  onSearch: (question: string) => void;
  isLoading: boolean;
}

const SAMPLE_PROMPTS = [
  "What are the advantages of PostgreSQL in 2026?",
  "Latest breakthroughs in Quantum Computing",
  "Compare Rust and Go for microservice architectures",
  "Key design patterns in LangGraph multi-agent systems",
];

export function ResearchForm({ onSearch, isLoading }: ResearchFormProps) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (question.trim() && !isLoading) {
      onSearch(question.trim());
    }
  };

  const handleChipClick = (prompt: string) => {
    setQuestion(prompt);
    if (!isLoading) {
      onSearch(prompt);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto space-y-4">
      <form onSubmit={handleSubmit} className="relative group">
        {/* Glow backdrop effect */}
        <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-2xl blur-md opacity-25 group-hover:opacity-40 transition duration-500" />

        <div className="relative flex items-center rounded-2xl bg-slate-900/90 border border-slate-700/60 shadow-2xl backdrop-blur-xl p-2 transition-all group-focus-within:border-indigo-500/80">
          <div className="flex items-center justify-center pl-4 pr-2 text-indigo-400">
            <Search className="w-5 h-5" />
          </div>

          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={isLoading}
            placeholder="Ask any research topic or question (e.g., PostgreSQL advantages, AI trends)..."
            className="w-full bg-transparent px-2 py-3 text-slate-100 placeholder-slate-400 focus:outline-none text-base sm:text-lg font-normal disabled:opacity-50"
          />

          {question && !isLoading && (
            <button
              type="button"
              onClick={() => setQuestion("")}
              className="p-1.5 text-slate-400 hover:text-slate-200 transition-colors mr-2"
            >
              <X className="w-4 h-4" />
            </button>
          )}

          <button
            type="submit"
            disabled={!question.trim() || isLoading}
            className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-medium text-sm transition-all shadow-md shadow-indigo-600/30 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none shrink-0"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Researching...</span>
              </>
            ) : (
              <>
                <span>Start Research</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Suggestion Chips */}
      <div className="flex flex-wrap items-center gap-2 justify-center sm:justify-start pt-1">
        <span className="text-xs text-slate-400 font-medium flex items-center mr-1">
          <Sparkles className="w-3 h-3 text-indigo-400 mr-1" />
          Suggested:
        </span>
        {SAMPLE_PROMPTS.map((prompt, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleChipClick(prompt)}
            disabled={isLoading}
            className="text-xs px-3 py-1.5 rounded-lg bg-slate-900/80 hover:bg-indigo-950/60 border border-slate-800 hover:border-indigo-500/40 text-slate-300 hover:text-indigo-300 transition-all font-medium disabled:opacity-50"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
