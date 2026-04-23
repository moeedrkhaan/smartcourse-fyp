import { cn } from "@/lib/utils";
import { Cpu, Brain } from "lucide-react";

type ModelType = "tfidf" | "neural";

interface ModelToggleProps {
  value: ModelType;
  onChange: (value: ModelType) => void;
  disabled?: boolean;
}

export function ModelToggle({ value, onChange, disabled = false }: ModelToggleProps) {
  return (
    <div className="flex items-center gap-2 p-1 bg-secondary rounded-xl">
      <button
        onClick={() => !disabled && onChange("tfidf")}
        disabled={disabled}
        className={cn(
          "flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200",
          value === "tfidf"
            ? "bg-card text-foreground shadow-sm"
            : "text-muted-foreground hover:text-foreground",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      >
        <Cpu className="h-4 w-4" />
        <span>TF-IDF Model</span>
      </button>
      <button
        onClick={() => !disabled && onChange("neural")}
        disabled={disabled}
        className={cn(
          "flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200",
          value === "neural"
            ? "bg-card text-foreground shadow-sm"
            : "text-muted-foreground hover:text-foreground",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      >
        <Brain className="h-4 w-4" />
        <span>Neural Model</span>
      </button>
    </div>
  );
}
