"use client";

import { useEffect, useState } from "react";
import { runResearch } from "@/lib/api";
import { ResearchResponse, ResearchHistoryItem } from "@/types/research";
import { Navbar } from "@/components/Navbar";
import { ResearchForm } from "@/components/ResearchForm";
import { ProgressStepper, ResearchStage } from "@/components/ProgressStepper";
import { ReportViewer } from "@/components/ReportViewer";
import { FindingsGrid } from "@/components/FindingsGrid";
import { SourcesList } from "@/components/SourcesList";
import { AnalyticsBanner } from "@/components/AnalyticsBanner";
import { HistoryDrawer } from "@/components/HistoryDrawer";
import { Sparkles, FileText, ShieldCheck, Globe, AlertCircle, RefreshCw } from "lucide-react";

export default function Home() {
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState<ResearchStage>("idle");
  const [researchResponse, setResearchResponse] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Active tab state: "report" | "claims" | "sources"
  const [activeTab, setActiveTab] = useState<"report" | "claims" | "sources">("report");

  // History state
  const [isHistoryOpen, setIsHistoryOpen] = useState(false);
  const [history, setHistory] = useState<ResearchHistoryItem[]>([]);

  // Load history from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem("research_history");
      if (saved) {
        setHistory(JSON.parse(saved));
      }
    } catch (e) {
      console.error("Failed to load history from localStorage:", e);
    }
  }, []);

  // Save history item
  const saveToHistory = (res: ResearchResponse) => {
    const newItem: ResearchHistoryItem = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      question: res.question,
      response: res,
    };
    const updated = [newItem, ...history.filter((h) => h.question !== res.question)].slice(0, 20);
    setHistory(updated);
    try {
      localStorage.setItem("research_history", JSON.stringify(updated));
    } catch (e) {
      console.error("Failed to save history to localStorage:", e);
    }
  };

  const handleClearHistory = () => {
    setHistory([]);
    try {
      localStorage.removeItem("research_history");
    } catch (e) {
      console.error("Failed to clear history from localStorage:", e);
    }
  };

  const handleSelectHistory = (item: ResearchHistoryItem) => {
    setCurrentQuestion(item.question);
    setResearchResponse(item.response);
    setCurrentStage("completed");
    setError(null);
    setActiveTab("report");
  };

  const handleStartResearch = async (question: string) => {
    setCurrentQuestion(question);
    setIsLoading(true);
    setError(null);
    setResearchResponse(null);
    setActiveTab("report");

    // Stage progression animation
    setCurrentStage("search");
    const timer1 = setTimeout(() => setCurrentStage("retrieve"), 2500);
    const timer2 = setTimeout(() => setCurrentStage("extract"), 5500);
    const timer3 = setTimeout(() => setCurrentStage("answer"), 8500);

    try {
      const result = await runResearch(question);
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);

      setResearchResponse(result);
      setCurrentStage("completed");
      saveToHistory(result);
    } catch (err: any) {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
      setCurrentStage("idle");
      setError(err.message || "An unexpected error occurred during research execution.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#090d16] text-slate-100 selection:bg-indigo-500 selection:text-white">
      {/* Navigation Bar */}
      <Navbar
        onToggleHistory={() => setIsHistoryOpen(true)}
        historyCount={history.length}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Banner Header */}
        <div className="text-center space-y-3 pt-4 pb-2">
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold tracking-wide">
            <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
            <span>Autonomous Factual Research Assistant</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white max-w-3xl mx-auto leading-tight">
            Deep Research with <span className="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">Multi-Agent Intelligence</span>
          </h1>

          <p className="text-sm sm:text-base text-slate-400 max-w-2xl mx-auto font-normal">
            Searches the web, extracts verified factual claims with confidence metrics, and synthesizes cited research reports automatically.
          </p>
        </div>

        {/* Search Input Box */}
        <ResearchForm onSearch={handleStartResearch} isLoading={isLoading} />

        {/* Live Workflow Stepper */}
        {currentStage !== "idle" && (
          <ProgressStepper
            currentStage={currentStage}
            searchQueries={researchResponse?.search_queries}
            findingsCount={researchResponse?.findings?.length}
            sourcesCount={researchResponse?.retrieved_documents?.length}
          />
        )}

        {/* Error Alert Box */}
        {error && (
          <div className="max-w-4xl mx-auto p-4 rounded-2xl bg-rose-950/40 border border-rose-800/80 text-rose-300 flex items-start space-x-3 shadow-xl">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
            <div className="flex-1">
              <h4 className="text-sm font-bold text-rose-200">Research Failed</h4>
              <p className="text-xs text-rose-300/90 mt-1">{error}</p>
              <p className="text-[11px] text-rose-400/80 mt-2 font-mono">
                Make sure your FastAPI backend server is running on <code className="bg-rose-900/40 px-1 py-0.5 rounded">http://localhost:8000</code> with your GROQ_API_KEY / SEARCH_API_KEY configured.
              </p>
            </div>
            <button
              onClick={() => handleStartResearch(currentQuestion)}
              className="px-3 py-1.5 rounded-lg bg-rose-900/60 hover:bg-rose-800 text-rose-100 text-xs font-medium border border-rose-700 shrink-0 flex items-center space-x-1"
            >
              <RefreshCw className="w-3.5 h-3.5 mr-1" /> Retry
            </button>
          </div>
        )}

        {/* Results Dashboard */}
        {researchResponse && (
          <div className="w-full max-w-5xl mx-auto space-y-6 pt-4 animate-fade-in">
            {/* Analytics KPI Header */}
            <AnalyticsBanner response={researchResponse} />

            {/* Navigation Tabs */}
            <div className="flex border-b border-slate-800 space-x-2 sm:space-x-4">
              <button
                onClick={() => setActiveTab("report")}
                className={`flex items-center space-x-2 px-4 py-3 text-sm font-semibold border-b-2 transition-all ${
                  activeTab === "report"
                    ? "border-indigo-500 text-indigo-400 bg-indigo-500/5"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <FileText className="w-4 h-4" />
                <span>Synthesized Report</span>
              </button>

              <button
                onClick={() => setActiveTab("claims")}
                className={`flex items-center space-x-2 px-4 py-3 text-sm font-semibold border-b-2 transition-all ${
                  activeTab === "claims"
                    ? "border-indigo-500 text-indigo-400 bg-indigo-500/5"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <ShieldCheck className="w-4 h-4" />
                <span>Factual Claims ({researchResponse.findings?.length || 0})</span>
              </button>

              <button
                onClick={() => setActiveTab("sources")}
                className={`flex items-center space-x-2 px-4 py-3 text-sm font-semibold border-b-2 transition-all ${
                  activeTab === "sources"
                    ? "border-indigo-500 text-indigo-400 bg-indigo-500/5"
                    : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Globe className="w-4 h-4" />
                <span>Sources ({researchResponse.retrieved_documents?.length || 0})</span>
              </button>
            </div>

            {/* Tab Views */}
            {activeTab === "report" && (
              <ReportViewer
                answer={researchResponse.final_answer}
                question={researchResponse.question}
              />
            )}

            {activeTab === "claims" && (
              <FindingsGrid findings={researchResponse.findings} />
            )}

            {activeTab === "sources" && (
              <SourcesList
                documents={researchResponse.retrieved_documents}
                searchResults={researchResponse.search_results}
              />
            )}
          </div>
        )}
      </main>

      {/* History Drawer */}
      <HistoryDrawer
        isOpen={isHistoryOpen}
        onClose={() => setIsHistoryOpen(false)}
        history={history}
        onSelectHistory={handleSelectHistory}
        onClearHistory={handleClearHistory}
      />

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-slate-950/60 py-6 text-center text-xs text-slate-500">
        <p>Multi-Agent Research Assistant • Powered by LangGraph, FastAPI & React</p>
      </footer>
    </div>
  );
}
