import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  History,
  Bookmark,
  GitCompare,
  Clock,
  Trash2,
  ExternalLink,
  Brain,
  Cpu,
  Loader2,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/contexts/AuthContext";
import { apiService } from "@/services/api";
import { toast } from "sonner";

interface SearchHistoryItem {
  id: number;
  query: string;
  model: "tfidf" | "neural";
  timestamp: string;
  results_count: number;
}

interface SavedCourse {
  id: number;
  course_id: string;
  course_title: string;
  course_provider: string;
  query: string;
  model: "tfidf" | "neural";
  relevance_score: number;
  timestamp: string;
}

export default function Dashboard() {
  const { user, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [history, setHistory] = useState<SearchHistoryItem[]>([]);
  const [saved, setSaved] = useState<SavedCourse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Redirect to auth if not logged in
    if (!authLoading && !user) {
      toast.error("Please login to view your dashboard");
      navigate("/auth");
      return;
    }

    // Fetch data if user is authenticated
    if (user) {
      fetchData();
    }
  }, [user, authLoading, navigate]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [historyData, savedData] = await Promise.all([
        apiService.getSearchHistory(50),
        apiService.getSavedRecommendations(100),
      ]);
      setHistory(historyData);
      setSaved(savedData);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
      toast.error("Failed to load dashboard data");
    } finally {
      setLoading(false);
    }
  };

  const removeFromHistory = async (id: number) => {
    try {
      await apiService.deleteSearchHistory(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      toast.success("Search history item removed");
    } catch (error) {
      console.error("Error deleting history:", error);
      toast.error("Failed to delete history item");
    }
  };

  const removeFromSaved = async (id: number) => {
    try {
      await apiService.deleteSavedRecommendation(id);
      setSaved((prev) => prev.filter((item) => item.id !== id));
      toast.success("Saved course removed");
    } catch (error) {
      console.error("Error deleting saved course:", error);
      toast.error("Failed to delete saved course");
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? "s" : ""} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? "s" : ""} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? "s" : ""} ago`;
    return date.toLocaleDateString();
  };

  if (authLoading || loading) {
    return (
      <Layout>
        <div className="container max-w-7xl mx-auto px-4 py-12 flex items-center justify-center min-h-[60vh]">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="container max-w-7xl mx-auto px-4 py-12 md:py-16 overflow-hidden">
        <div className="mb-8">
          <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">
            Your Dashboard
          </h1>
          <p className="text-lg text-muted-foreground">
            Track your search history, saved courses, and more.
          </p>
        </div>

        <Tabs defaultValue="history" className="space-y-8">
          <TabsList className="bg-secondary/50 p-1">
            <TabsTrigger value="history" className="gap-2">
              <History className="h-4 w-4" />
              Search History
            </TabsTrigger>
            <TabsTrigger value="saved" className="gap-2">
              <Bookmark className="h-4 w-4" />
              Saved Courses
            </TabsTrigger>
          </TabsList>

          {/* Search History Tab */}
          <TabsContent value="history" className="space-y-4">
            {history.length === 0 ? (
              <Card className="border-dashed">
                <CardContent className="py-12 text-center">
                  <History className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-2">No search history yet</p>
                  <p className="text-sm text-muted-foreground">
                    Start searching for courses to see your history here
                  </p>
                </CardContent>
              </Card>
            ) : (
              history.map((item, index) => (
                <Card
                  key={item.id}
                  className="group hover-lift animate-fade-up"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <CardContent className="p-4 flex items-center justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge
                          variant="secondary"
                          className={cn(
                            "text-xs",
                            item.model === "neural"
                              ? "bg-primary/10 text-primary"
                              : "bg-accent/10 text-accent"
                          )}
                        >
                          {item.model === "neural" ? (
                            <Brain className="h-3 w-3 mr-1" />
                          ) : (
                            <Cpu className="h-3 w-3 mr-1" />
                          )}
                          {item.model.toUpperCase()}
                        </Badge>
                        <span className="text-xs text-muted-foreground flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {formatTimestamp(item.timestamp)}
                        </span>
                      </div>
                      <p className="font-medium text-foreground truncate">
                        "{item.query}"
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {item.results_count} results found
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-muted-foreground hover:text-destructive"
                        onClick={() => removeFromHistory(item.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>

          {/* Saved Courses Tab */}
          <TabsContent value="saved" className="space-y-4">
            {saved.length === 0 ? (
              <Card className="border-dashed">
                <CardContent className="py-12 text-center">
                  <Bookmark className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <p className="text-muted-foreground mb-2">No saved courses yet</p>
                  <p className="text-sm text-muted-foreground">
                    Save courses from recommendations to access them here
                  </p>
                </CardContent>
              </Card>
            ) : (
              saved.map((course, index) => (
                <Card
                  key={course.id}
                  className="group hover-lift animate-fade-up"
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <CardContent className="p-4 flex items-center justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge
                          variant="secondary"
                          className={cn(
                            "text-xs",
                            course.model === "neural"
                              ? "bg-primary/10 text-primary"
                              : "bg-accent/10 text-accent"
                          )}
                        >
                          {course.model.toUpperCase()}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {course.course_provider}
                        </span>
                      </div>
                      <p className="font-medium text-foreground truncate">
                        {course.course_title}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        From search: "{course.query}"
                      </p>
                      <span className="text-xs text-muted-foreground">
                        Saved {formatTimestamp(course.timestamp)}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-muted-foreground hover:text-destructive"
                        onClick={() => removeFromSaved(course.id)}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </TabsContent>
        </Tabs>
      </div>
    </Layout>
  );
}
