"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Copy, Check, FileText, Share2, Sparkles, BookOpen } from "lucide-react";

interface ReportViewerProps {
  answer: string;
  question: string;
}

export function ReportViewer({ answer, question }: ReportViewerProps) {
  const [copied, setCopied] = useState(false);
  const [showRaw, setShowRaw] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!answer) {
    return (
      <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 text-center text-slate-400">
        No report generated yet.
      </div>
    );
  }

  return (
    <div className="w-full rounded-2xl bg-slate-900/80 border border-slate-800 shadow-2xl overflow-hidden backdrop-blur-md">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 px-6 py-4 bg-slate-950/60 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <div className="p-2 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center">
              Synthesized Research Report
            </h2>
            <p className="text-xs text-slate-400">
              Verified & Cited by Autonomous Agent
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowRaw(!showRaw)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition-colors"
          >
            {showRaw ? "Formatted View" : "Raw Markdown"}
          </button>

          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-medium transition-colors shadow-sm"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-300" />
                <span>Copied!</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5" />
                <span>Copy Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="p-6 sm:p-8">
        <div className="mb-6 p-4 rounded-xl bg-slate-950/40 border border-slate-800/80">
          <span className="text-xs font-semibold uppercase tracking-wider text-indigo-400 block mb-1">
            Research Prompt
          </span>
          <h3 className="text-lg font-semibold text-slate-100">{question}</h3>
        </div>

        {showRaw ? (
          <pre className="p-4 rounded-xl bg-slate-950 text-slate-300 text-xs font-mono overflow-x-auto whitespace-pre-wrap border border-slate-800">
            {answer}
          </pre>
        ) : (
          <div className="prose prose-invert prose-indigo max-w-none text-slate-200 text-sm sm:text-base leading-relaxed space-y-4">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => (
                  <h1 className="text-2xl font-bold text-slate-100 border-b border-slate-800 pb-2 mt-6 mb-4">
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-xl font-semibold text-indigo-300 mt-6 mb-3">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-lg font-medium text-slate-200 mt-4 mb-2">
                    {children}
                  </h3>
                ),
                ul: ({ children }) => (
                  <ul className="list-disc list-inside space-y-1 my-2 text-slate-300">
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="list-decimal list-inside space-y-1 my-2 text-slate-300">
                    {children}
                  </ol>
                ),
                code: ({ children }) => (
                  <code className="px-1.5 py-0.5 rounded bg-slate-950 text-indigo-300 font-mono text-xs border border-slate-800">
                    {children}
                  </code>
                ),
                blockquote: ({ children }) => (
                  <blockquote className="border-l-4 border-indigo-500 pl-4 italic text-slate-400 my-4 bg-indigo-950/20 py-2 rounded-r">
                    {children}
                  </blockquote>
                ),
                a: ({ href, children }) => (
                  <a
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-indigo-400 hover:text-indigo-300 underline font-medium inline-flex items-center gap-1"
                  >
                    {children}
                  </a>
                ),
              }}
            >
              {answer}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  );
}
