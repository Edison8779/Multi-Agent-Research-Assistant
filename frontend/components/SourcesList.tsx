"use client";

import { RetrievedDocument, SearchResult } from "@/types/research";
import { Globe, ExternalLink, FileText, Calendar } from "lucide-react";

interface SourcesListProps {
  documents: RetrievedDocument[];
  searchResults: SearchResult[];
}

export function SourcesList({ documents, searchResults }: SourcesListProps) {
  // Combine documents and search results if any
  const hasDocuments = documents && documents.length > 0;
  const hasSearchResults = searchResults && searchResults.length > 0;

  if (!hasDocuments && !hasSearchResults) {
    return (
      <div className="p-8 rounded-2xl bg-slate-900/60 border border-slate-800 text-center text-slate-400">
        No web sources retrieved for this search.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Retrieved Documents Section */}
      {hasDocuments && (
        <div className="space-y-3">
          <h3 className="text-base font-bold text-slate-100 flex items-center">
            <Globe className="w-5 h-5 text-indigo-400 mr-2" />
            Scraped Web Documents ({documents.length})
          </h3>

          <div className="space-y-3">
            {documents.map((doc, idx) => {
              let domain = "";
              try {
                domain = new URL(doc.url).hostname;
              } catch {
                domain = doc.url;
              }

              return (
                <div
                  key={idx}
                  className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 hover:border-indigo-500/40 transition-all shadow-md backdrop-blur-md"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-800 text-indigo-300 font-mono border border-slate-700">
                      {domain}
                    </span>

                    {doc.published_date && (
                      <span className="text-xs text-slate-400 flex items-center">
                        <Calendar className="w-3 h-3 mr-1" />
                        {doc.published_date}
                      </span>
                    )}
                  </div>

                  <h4 className="text-base font-bold text-slate-100 hover:text-indigo-300 transition-colors mb-2">
                    <a href={doc.url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5">
                      {doc.title || "Untitled Source"}
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400" />
                    </a>
                  </h4>

                  <p className="text-xs text-slate-300 line-clamp-3 bg-slate-950/40 p-3 rounded-xl border border-slate-850 font-sans">
                    {doc.content}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Raw Search Results fallback if no scraped docs */}
      {!hasDocuments && hasSearchResults && (
        <div className="space-y-3">
          <h3 className="text-base font-bold text-slate-100 flex items-center">
            <FileText className="w-5 h-5 text-indigo-400 mr-2" />
            Web Search Hits ({searchResults.length})
          </h3>

          <div className="space-y-3">
            {searchResults.map((res, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl bg-slate-900/80 border border-slate-800"
              >
                <h4 className="text-sm font-bold text-slate-100 mb-1">
                  <a href={res.url} target="_blank" rel="noopener noreferrer" className="hover:text-indigo-400 inline-flex items-center gap-1">
                    {res.title}
                    <ExternalLink className="w-3 h-3 text-slate-400" />
                  </a>
                </h4>
                <p className="text-xs text-slate-400">{res.snippet}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
