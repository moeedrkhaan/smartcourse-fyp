import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Search, Sparkles, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface SearchInputProps {
  onSearch: (query: string) => void;
  isLoading?: boolean;
  placeholder?: string;
}

export function SearchInput({
  onSearch,
  isLoading = false,
  placeholder = "Describe what you want to learn... e.g., 'machine learning for beginners with Python focus'",
}: SearchInputProps) {
  const [query, setQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const exampleQueries = [
    "Introduction to web development",
    "Data science with Python",
    "Mobile app development for beginners",
  ];

  return (
    <div className="w-full space-y-4">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative group">
          <div className="absolute inset-0 rounded-xl gradient-primary opacity-0 group-focus-within:opacity-10 transition-opacity duration-300 blur-xl" />
          <div className="relative bg-card border border-border rounded-xl shadow-card overflow-hidden">
            <Textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={placeholder}
              className="min-h-[120px] resize-none border-0 bg-transparent focus-visible:ring-0 text-base placeholder:text-muted-foreground/60 p-4"
            />
            <div className="flex items-center justify-between p-3 pt-0 border-t border-border/50 bg-secondary/30">
              <div className="flex items-center gap-2 text-sm text-muted-foreground">
                <Sparkles className="h-4 w-4" />
                <span>Natural language powered</span>
              </div>
              <Button
                type="submit"
                variant="hero"
                disabled={!query.trim() || isLoading}
                className="gap-2"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Searching...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    Find Courses
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      </form>

      <div className="flex flex-wrap items-center gap-2">
        <span className="text-sm text-muted-foreground">Try:</span>
        {exampleQueries.map((example) => (
          <Button
            key={example}
            variant="secondary"
            size="sm"
            className="text-xs"
            onClick={() => setQuery(example)}
          >
            {example}
          </Button>
        ))}
      </div>
    </div>
  );
}
