import { Loader2, Search, X } from "lucide-react";
import React, { useEffect, useRef, useState } from "react";

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const q = query.trim();
    if (q) onSearch(q);
  };

  // Quick focus via "/" key (Jakob’s Law: familiar pattern)
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "/" && document.activeElement !== inputRef.current) {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <form onSubmit={handleSubmit} className="relative">
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[var(--muted)]" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search papers…  (press / to focus)"
          className="w-full pl-11 pr-16 py-3 rounded-lg border-2 border-[var(--border)] bg-[--surface] text-[--text] placeholder-[--muted] focus:outline-none focus:ring-0 focus:border-[--accent] font-mono"
          disabled={isLoading}
        />
        {query && !isLoading && (
          <button
            type="button"
            onClick={() => setQuery("")}
            className="absolute right-10 top-1/2 -translate-y-1/2 p-1 text-[var(--muted)] hover:text-[--text]"
            aria-label="Clear"
          >
            <X className="w-4 h-4" />
          </button>
        )}
        {isLoading && (
          <Loader2 className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-[--accent] animate-spin" />
        )}
      </div>
    </form>
  );
}
