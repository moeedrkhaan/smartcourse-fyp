import { useState } from "react";
import { Layout } from "@/components/layout/Layout";
import { SearchInput } from "@/components/recommendation/SearchInput";
import { ModelToggle } from "@/components/recommendation/ModelToggle";
import { CourseCard } from "@/components/course/CourseCard";
import { Sparkles, Info, AlertCircle, GitCompare } from "lucide-react";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { apiService, Course } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

type ModelType = "tfidf" | "neural";

export default function Recommendations() {
  const [modelType, setModelType] = useState<ModelType>("neural");
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [savedCourses, setSavedCourses] = useState<Set<string>>(new Set());
  const [results, setResults] = useState<Course[]>([]);
  const [compareMode, setCompareMode] = useState(false);
  const [tfidfResults, setTfidfResults] = useState<Course[]>([]);
  const [neuralResults, setNeuralResults] = useState<Course[]>([]);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setSearchQuery(query);
    setError(null);
    
    try {
      if (compareMode) {
        // Compare both models side-by-side
        const response = await apiService.compareModels(query);
        setTfidfResults(response.tfidf.results);
        setNeuralResults(response.neural.results);
        setHasSearched(true);
        
        toast({
          title: "Comparison loaded",
          description: `Comparing ${response.tfidf.results.length} courses from both models`,
        });
      } else {
        // Single model search
        const response = await apiService.getRecommendations(query, modelType);
        setResults(response.results);
        setHasSearched(true);
        
        toast({
          title: "Recommendations loaded",
          description: `Found ${response.results.length} courses using ${response.model.type} model`,
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get recommendations");
      toast({
        title: "Error",
        description: "Failed to get recommendations. Please make sure the backend server is running.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleSaveCourse = async (courseId: string, courseTitle?: string) => {
    if (savedCourses.has(courseId)) {
      // Remove from saved
      setSavedCourses((prev) => {
        const next = new Set(prev);
        next.delete(courseId);
        return next;
      });
      
      toast({
        title: "Removed from saved",
        description: "Course removed from your saved list",
      });
    } else {
      // Add to saved
      setSavedCourses((prev) => new Set(prev).add(courseId));
      
      try {
        await apiService.saveRecommendation(courseId, searchQuery, modelType);
        toast({
          title: "Course saved",
          description: courseTitle || "Course added to your saved list",
        });
      } catch (err) {
        // Revert on error
        setSavedCourses((prev) => {
          const next = new Set(prev);
          next.delete(courseId);
          return next;
        });
        
        toast({
          title: "Error saving course",
          description: "Failed to save course. Please try again.",
          variant: "destructive",
        });
      }
    }
  };

  return (
    <Layout>
      <div className="container max-w-7xl mx-auto px-4 py-8 md:py-12 overflow-hidden">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-2">
            Recommendations
          </h1>
          <p className="text-base text-muted-foreground">
            Describe what you want to learn in natural language, and let our AI find the most relevant courses for you.
          </p>
        </div>

        {/* Search and Controls */}
        <div className="space-y-4 mb-8">
          <SearchInput onSearch={handleSearch} isLoading={isLoading} />
          
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <ModelToggle value={modelType} onChange={setModelType} disabled={isLoading || compareMode} />
              
              <Button
                variant={compareMode ? "default" : "outline"}
                size="sm"
                onClick={() => setCompareMode(!compareMode)}
                disabled={isLoading}
                className="gap-2"
              >
                <GitCompare className="h-4 w-4" />
                Compare Models
              </Button>
            </div>
            
            <Alert className="bg-secondary/50 border-border/50 py-2 px-4 w-auto">
              <Info className="h-4 w-4" />
              <AlertDescription className="text-xs">
                {compareMode
                  ? "Comparing both TF-IDF and Neural models side-by-side"
                  : modelType === "neural"
                  ? "Neural model uses sentence transformers for semantic understanding"
                  : "TF-IDF model uses keyword frequency for precise matching"}
              </AlertDescription>
            </Alert>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              {error}. Make sure the Flask backend is running at http://localhost:5000
            </AlertDescription>
          </Alert>
        )}

        {/* Results */}
        {hasSearched && (
          <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-border">
              <div>
                <p className="text-sm text-muted-foreground">
                  Results for: <span className="font-medium text-foreground">"{searchQuery}"</span>
                </p>
              </div>
              <span className="text-sm font-medium text-foreground">
                {compareMode 
                  ? `${tfidfResults.length} courses per model` 
                  : `${results.length} courses found`}
              </span>
            </div>

            {compareMode ? (
              /* Side-by-Side Comparison */
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* TF-IDF Results */}
                <div>
                  <div className="mb-4 p-3 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                    <h3 className="font-semibold text-blue-600 dark:text-blue-400">
                      TF-IDF Model
                    </h3>
                    <p className="text-xs text-muted-foreground mt-1">
                      Keyword frequency-based matching
                    </p>
                  </div>
                  <div className="space-y-4">
                    {tfidfResults.map((course, index) => (
                      <CourseCard
                        key={course.id}
                        {...course}
                        modelType="tfidf"
                        index={index}
                        isSaved={savedCourses.has(course.id)}
                        onSave={() => toggleSaveCourse(course.id, course.title)}
                      />
                    ))}
                  </div>
                </div>

                {/* Neural Results */}
                <div>
                  <div className="mb-4 p-3 bg-purple-500/10 border border-purple-500/20 rounded-lg">
                    <h3 className="font-semibold text-purple-600 dark:text-purple-400">
                      Neural Model (Sentence-BERT)
                    </h3>
                    <p className="text-xs text-muted-foreground mt-1">
                      Semantic understanding using transformers
                    </p>
                  </div>
                  <div className="space-y-4">
                    {neuralResults.map((course, index) => (
                      <CourseCard
                        key={course.id}
                        {...course}
                        modelType="neural"
                        index={index}
                        isSaved={savedCourses.has(course.id)}
                        onSave={() => toggleSaveCourse(course.id, course.title)}
                      />
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              /* Single Model Results */
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.map((course, index) => (
                  <CourseCard
                    key={course.id}
                    {...course}
                    modelType={modelType}
                    index={index}
                    isSaved={savedCourses.has(course.id)}
                    onSave={() => toggleSaveCourse(course.id, course.title)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!hasSearched && !isLoading && (
          <div className="text-center py-16">
            <div className="inline-flex h-20 w-20 items-center justify-center rounded-full bg-secondary mb-6">
              <Sparkles className="h-10 w-10 text-primary" />
            </div>
            <h3 className="font-display text-xl font-semibold text-foreground mb-2">
              Start Your Search
            </h3>
            <p className="text-muted-foreground max-w-md mx-auto">
              Enter a description of what you'd like to learn, and we'll find
              the best courses for you using advanced AI models.
            </p>
          </div>
        )}
      </div>
    </Layout>
  );
}
