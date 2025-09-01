import { useEffect, useRef, useState } from "react";
import GraphViewWrapper from "./components/GraphView";
import ListView from "./components/ListView";
import SearchBar from "./components/SearchBar";
import type { GraphData, SearchResult } from "./types";

export default function App() {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [graphData, setGraphData] = useState<GraphData | undefined>(undefined);
  const [selectedPaper, setSelectedPaper] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const [darkMode, setDarkMode] = useState(true);

  const onSearch = async (query: string) => {
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    setIsLoading(true);
    try {
      const res = await fetch(`/api/search?query=${encodeURIComponent(query)}`, { signal: ctrl.signal });
      if (!res.ok) throw new Error(`Search failed: ${res.status} ${res.statusText}`);
      const data = await res.json();
      setSearchResults(data.results ?? []);
      setGraphData(data.graph ?? { nodes: [], edges: [] });
      setSelectedPaper(data.results?.[0]?.id ?? null);
    } catch (err) {
      if ((err as any)?.name !== "AbortError") console.error(err);
    } finally {
      if (abortRef.current === ctrl) abortRef.current = null;
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // onSearch("transformers");
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  return (
    <main className="min-h-dvh bg-[var(--bg)] text-[var(--text)]">
      <div className="mx-auto max-w-7xl p-6 space-y-4">
        <header className="flex items-center justify-between">
          <h1 className="text-3xl font-extrabold tracking-tight">
            GraphRAG <span className="underline decoration-4 decoration-[var(--accent)]">Search</span>
          </h1>

          <button
            onClick={() => setDarkMode((d) => !d)}
            className="text-sm px-3 py-1 border rounded border-[var(--border)] hover:bg-[var(--surface)]"
          >
            {darkMode ? "☀️ Light" : "🌙 Dark"}
          </button>
        </header>

        <SearchBar onSearch={onSearch} isLoading={isLoading} />

        {/* Two-pane: list (left), graph (right) */}
        <div className="grid gap-4 lg:grid-cols-[380px_1fr]">
          {/* List – light separation, sticky on desktop */}
          <aside className="self-start md:sticky md:top-4">
            <div className="rounded-md border border-[var(--border)]/60 bg-[--surface] h-[70vh] overflow-y-auto">
              <ListView
                results={searchResults}
                selectedPaper={selectedPaper}
                onPaperSelect={setSelectedPaper}
              />
            </div>
          </aside>
          <section className="rounded-none flex flex-col h-[70vh]">
            <GraphViewWrapper
              graphData={graphData}
              searchResults={searchResults}
              selectedPaper={selectedPaper}
              onPaperSelect={setSelectedPaper}
            />
          </section>
        </div>
      </div>
    </main>
  );
}
