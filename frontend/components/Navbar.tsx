"use client";

import { useEffect, useState } from "react";
import { checkBackendHealth } from "@/lib/api";
import { Bot, History, Sparkles, Server, CheckCircle2, XCircle } from "lucide-react";

interface NavbarProps {
  onToggleHistory: () => void;
  historyCount: number;
}

export function Navbar({ onToggleHistory, historyCount }: NavbarProps) {
  const [isBackendOnline, setIsBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let isMounted = true;
    const check = async () => {
      const online = await checkBackendHealth();
      if (isMounted) setIsBackendOnline(online);
    };
    check();
    const interval = setInterval(check, 10000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <div className="flex items-center space-x-3">
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-500 shadow-lg shadow-indigo-500/20">
            <Bot className="w-5 h-5 text-white" />
            <div className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-emerald-400 ring-2 ring-slate-950 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg text-slate-100 tracking-tight">
                ResearchAI
              </span>
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                <Sparkles className="w-3 h-3 mr-1 text-indigo-400" />
                Multi-Agent
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Autonomous Deep Research Engine
            </p>
          </div>
        </div>

        {/* Status & Actions */}
        <div className="flex items-center space-x-4">
          {/* Backend Health Badge */}
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <Server className="w-3.5 h-3.5 text-slate-400" />
            <span className="hidden md:inline text-slate-400">API Status:</span>
            {isBackendOnline === null ? (
              <span className="text-slate-500 flex items-center">
                <span className="w-2 h-2 rounded-full bg-slate-500 mr-1.5 animate-pulse" />
                Checking...
              </span>
            ) : isBackendOnline ? (
              <span className="text-emerald-400 flex items-center font-medium">
                <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-400" />
                Online
              </span>
            ) : (
              <span className="text-rose-400 flex items-center font-medium">
                <XCircle className="w-3.5 h-3.5 mr-1 text-rose-400" />
                Offline
              </span>
            )}
          </div>

          {/* History Drawer Toggle Button */}
          <button
            onClick={onToggleHistory}
            className="relative flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 text-sm font-medium transition-all shadow-sm active:scale-95"
            title="Saved Research Sessions"
          >
            <History className="w-4 h-4 text-indigo-400" />
            <span className="hidden sm:inline">History</span>
            {historyCount > 0 && (
              <span className="ml-1 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-indigo-100 bg-indigo-600 rounded-full">
                {historyCount}
              </span>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
