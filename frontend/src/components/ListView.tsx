import { ExternalLink, Network, Star, Users } from "lucide-react";
import type { SearchResult } from "../types";

interface ListViewProps {
  results: SearchResult[];
  selectedPaper: string | null;
  onPaperSelect: (paperId: string) => void;
}

export default function ListView({ results, selectedPaper, onPaperSelect }: ListViewProps) {
  if (results.length === 0) {
    return (
      <div className="p-10 text-center text-[var(--muted)]">
        <div className="w-16 h-16 rounded-md border-2 border-[var(--border)] bg-[--surface] flex items-center justify-center mx-auto mb-4">
          <Network className="w-8 h-8 text-[var(--muted)]" />
        </div>
        <p>No papers found</p>
        <p className="text-sm mt-1">Try a different query</p>
      </div>
    );
  }

  return (
    <div className="divide-y divide-[--border]">
      {results.map((paper) => {
        const selected = selectedPaper === paper.id;
        return (
          <div key={paper.id} className="relative">
            {/* Accent bar for selected */}
            {selected && (
              <div className="absolute left-0 top-0 h-full w-1 bg-[var(--accent)] rounded-r-sm" />
            )}

            <button
              onClick={() => onPaperSelect(paper.id)}
              className={[
                "w-full text-left p-3 pl-4 transition-colors font-sans relative",
                selected ? "bg-black/30" : "hover:bg-black/20",
              ].join(" ")}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1.5">
                    {/* Title truncates instead of overflowing */}
                    <h3 className="text-base font-semibold leading-tight truncate">
                      {paper.title}
                    </h3>
                    {paper.score && paper.score > 0.5 && (
                      <Star className="w-4 h-4 text-[--accent] shrink-0" />
                    )}
                  </div>

                  <div className="flex items-center text-[var(--muted)] mb-2 overflow-hidden">
                    <Users className="w-4 h-4 mr-2 shrink-0" />
                    <span className="text-xs truncate">
                      {paper.authors.length > 3
                        ? `${paper.authors.slice(0, 3).join(", ")} +${paper.authors.length - 3}`
                        : paper.authors.join(", ")}
                    </span>
                  </div>

                  <div className="flex flex-wrap gap-4 text-xs text-[var(--muted)] font-mono break-all">
                    {paper.score !== undefined && (
                      <span className="flex items-center">
                        score:<span className="ml-1">{paper.score.toFixed(3)}</span>
                      </span>
                    )}
                    {!!paper.related_ids?.length && (
                      <span className="flex items-center">
                        <Network className="w-3 h-3 mr-1" />
                        {paper.related_ids.length} related
                      </span>
                    )}
                    {/* Force IDs to break instead of overflow */}
                    <span className="opacity-70 break-all">id: {paper.id}</span>
                  </div>
                </div>

                <div className="ml-2 shrink-0">
                  <a
                    href={`https://arxiv.org/abs/${paper.id}`}
                    target="_blank"
                    rel="noreferrer"
                    className="p-2 text-[var(--muted)] hover:text-[var(--text)]"
                    title="View on arXiv"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>

              {!!paper.related_ids?.length && selected && (
                <div className="mt-3 pt-3 border-t border-[var(--border)]">
                  <div className="flex flex-wrap gap-2">
                    {paper.related_ids.slice(0, 5).map((relatedId) => (
                      <span
                        key={relatedId}
                        className="px-2 py-0.5 border-2 border-[var(--border)] rounded-md text-xs text-[var(--muted)] bg-transparent break-all"
                      >
                        {relatedId}
                      </span>
                    ))}
                    {paper.related_ids.length > 5 && (
                      <span className="px-2 py-0.5 border-2 border-[var(--border)] rounded-md text-xs text-[var(--muted)]">
                        +{paper.related_ids.length - 5} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </button>
          </div>
        );
      })}
    </div>
  );
}
