import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, Users, Star, Bookmark, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

interface CourseCardProps {
  title: string;
  provider: string;
  description: string;
  level: string;
  duration: string;
  students: string;
  rating: number;
  relevanceScore: number;
  tags: string[];
  modelType: "tfidf" | "neural";
  index: number;
  onSave?: () => void;
  isSaved?: boolean;
}

export function CourseCard({
  title,
  provider,
  description,
  level,
  duration,
  students,
  rating,
  relevanceScore,
  tags,
  modelType,
  index,
  onSave,
  isSaved = false,
}: CourseCardProps) {
  return (
    <Card
      className={cn(
        "group border border-border/50 bg-card hover-lift",
        "animate-fade-up flex flex-col"
      )}
      style={{ animationDelay: `${index * 80}ms` }}
    >
      <CardHeader className="pb-3 px-6">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-3">
              <Badge
                variant="secondary"
                className={cn(
                  "text-[10px] font-semibold px-2 py-0.5",
                  modelType === "neural"
                    ? "bg-primary/10 text-primary border-primary/20"
                    : "bg-accent/10 text-accent border-accent/20"
                )}
              >
                {modelType === "neural" ? "Neural" : "TF-IDF"}
              </Badge>
              <span className="text-xs text-muted-foreground truncate">{provider}</span>
            </div>
            <h3 className="font-display font-semibold text-base leading-tight text-foreground group-hover:text-primary transition-colors line-clamp-2 mb-0 h-[44px]">
              {title}
            </h3>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className={cn(
              "shrink-0 -mt-1",
              isSaved ? "text-primary" : "text-muted-foreground"
            )}
            onClick={onSave}
          >
            <Bookmark className={cn("h-4 w-4", isSaved && "fill-current")} />
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-3.5 px-6">
        <p className="text-sm text-muted-foreground leading-relaxed line-clamp-2 h-[42px]">{description}</p>

        {/* Relevance Score Bar */}
        <div className="space-y-1.5 w-full">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Relevance Score</span>
            <span className="font-semibold text-foreground">{relevanceScore}%</span>
          </div>
          <div className="h-2 w-full bg-secondary rounded-full overflow-hidden">
            <div
              className={cn(
                "h-full rounded-full transition-all duration-1000 ease-out",
                modelType === "neural" ? "gradient-primary" : "gradient-accent"
              )}
              style={{ width: `${relevanceScore}%` }}
            />
          </div>
        </div>

        {/* Metadata */}
        <div className="flex flex-wrap gap-4 text-sm text-muted-foreground min-h-[24px]">
          <div className="flex items-center gap-1.5">
            <Clock className="h-4 w-4" />
            <span>{duration}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Users className="h-4 w-4" />
            <span>{students}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Star className="h-4 w-4 text-amber-500 fill-amber-500" />
            <span>{rating.toFixed(1)}</span>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 min-h-[28px]">
          <Badge variant="outline" className="text-xs">
            {level}
          </Badge>
          {tags.slice(0, 2).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        {/* Action */}
        <Button variant="outline" className="w-full group/btn" size="sm">
          View Course
          <ExternalLink className="h-4 w-4 ml-2 group-hover/btn:translate-x-0.5 transition-transform" />
        </Button>
      </CardContent>
    </Card>
  );
}
