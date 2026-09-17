export interface ResearchFinding {
  claim: string;
  evidence: string;
  source_url: string;
  source_title: string;
  confidence: number;
}

export interface SearchResult {
  title: string;
  url: string;
  snippet: string;
}

export interface RetrievedDocument {
  title: string;
  url: string;
  content: string;
  published_date?: string;
}

export interface ResearchResponse {
  question: string;
  search_queries: string[];
  search_results: SearchResult[];
  retrieved_documents: RetrievedDocument[];
  findings: ResearchFinding[];
  final_answer: string;
}

export interface ResearchRequest {
  question: string;
}

export interface ResearchHistoryItem {
  id: string;
  timestamp: string;
  question: string;
  response: ResearchResponse;
}
