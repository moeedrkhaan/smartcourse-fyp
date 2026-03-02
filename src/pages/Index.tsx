import { Layout } from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Link } from "react-router-dom";
import {
  Brain,
  Sparkles,
  Zap,
  Target,
  BarChart3,
  Shield,
  ArrowRight,
  Search,
  CheckCircle,
} from "lucide-react";

const features = [
  {
    icon: Brain,
    title: "Neural Semantic Search",
    description:
      "State-of-the-art sentence transformers understand context, not just keywords.",
  },
  {
    icon: Target,
    title: "TF-IDF Precision",
    description:
      "Classic keyword matching with optimized term frequency analysis for exact matches.",
  },
  {
    icon: BarChart3,
    title: "Model Comparison",
    description:
      "Compare results from different models side-by-side to find your perfect course.",
  },
  {
    icon: Zap,
    title: "Real-time Results",
    description:
      "Get instant recommendations as you type with our optimized inference pipeline.",
  },
  {
    icon: Shield,
    title: "Curated Dataset",
    description:
      "Carefully preprocessed corpus from top educational platforms worldwide.",
  },
  {
    icon: Sparkles,
    title: "Personalized Learning",
    description:
      "Save favorites and track your learning journey with intelligent dashboards.",
  },
];

const stats = [
  { value: "20", label: "Courses Available" },
  { value: "2 Models", label: "AI Algorithms" },
  { value: "High", label: "Accuracy" },
  { value: "< 200ms", label: "Response Time" },
];

export default function Index() {
  return (
    <Layout>
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-hero -z-10" />
        <div className="absolute top-20 left-1/4 w-72 h-72 bg-primary/10 rounded-full blur-3xl -z-10" />
        <div className="absolute bottom-20 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl -z-10" />

        <div className="container max-w-7xl mx-auto px-4 relative py-24 md:py-32">
          <div className="max-w-3xl mx-auto text-center space-y-8 animate-fade-up">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium">
              <Sparkles className="h-4 w-4" />
              AI-Powered Course Discovery
            </div>

            <h1 className="font-display text-4xl md:text-6xl font-bold text-foreground tracking-tight">
              Find Your Perfect Course with{" "}
              <span className="text-gradient-primary">Intelligent</span> Search
            </h1>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
              SmartCourse uses advanced NLP models to understand what you want to
              learn and recommends the most relevant courses from our curated
              collection.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
              <Link to="/recommendations">
                <Button variant="hero" size="xl" className="gap-2">
                  Start Exploring
                  <ArrowRight className="h-5 w-5" />
                </Button>
              </Link>
              <Link to="/about">
                <Button variant="outline" size="xl">
                  Learn How It Works
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y border-border bg-secondary/30 overflow-hidden">
        <div className="container max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div
                key={stat.label}
                className="text-center animate-fade-up"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="font-display text-3xl md:text-4xl font-bold text-primary">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 md:py-32 overflow-hidden">
        <div className="container max-w-7xl mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              Powered by Advanced AI
            </h2>
            <p className="text-lg text-muted-foreground">
              Two complementary models work together to deliver precise,
              context-aware course recommendations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <Card
                key={feature.title}
                className="group border border-border/50 bg-card hover-lift animate-fade-up"
                style={{ animationDelay: `${index * 80}ms` }}
              >
                <CardContent className="p-6">
                  <div className="h-12 w-12 rounded-xl gradient-primary flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                    <feature.icon className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <h3 className="font-display font-semibold text-lg text-foreground mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 bg-secondary/30 overflow-hidden">
        <div className="container max-w-7xl mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
              How SmartCourse Works
            </h2>
            <p className="text-lg text-muted-foreground">
              Three simple steps to discover courses tailored to your learning goals.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {[
              {
                step: "01",
                title: "Describe Your Goals",
                description:
                  "Use natural language to tell us what you want to learn. No keywords needed.",
              },
              {
                step: "02",
                title: "Choose Your Model",
                description:
                  "Select TF-IDF for keyword precision or Neural for semantic understanding.",
              },
              {
                step: "03",
                title: "Get Recommendations",
                description:
                  "Receive top-10 courses ranked by relevance with detailed insights.",
              },
            ].map((item, index) => (
              <div
                key={item.step}
                className="relative text-center animate-fade-up"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="text-6xl font-display font-bold text-primary/20 mb-4">
                  {item.step}
                </div>
                <h3 className="font-display font-semibold text-xl text-foreground mb-2">
                  {item.title}
                </h3>
                <p className="text-muted-foreground">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 overflow-hidden">
        <div className="container max-w-7xl mx-auto px-4">
          <Card className="gradient-primary border-0 overflow-hidden">
            <CardContent className="p-8 md:p-12 text-center">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-primary-foreground mb-4">
                Ready to Find Your Next Course?
              </h2>
              <p className="text-primary-foreground/80 text-lg max-w-xl mx-auto mb-8">
                Start exploring thousands of courses with our AI-powered
                recommendation engine.
              </p>
              <Link to="/recommendations">
                <Button
                  variant="secondary"
                  size="xl"
                  className="gap-2 bg-card text-foreground hover:bg-card/90"
                >
                  <Search className="h-5 w-5" />
                  Try It Now — It's Free
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>
    </Layout>
  );
}
