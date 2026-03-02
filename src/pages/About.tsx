import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Database,
  FileText,
  Cpu,
  Brain,
  ArrowRight,
  Code,
  Layers,
  Zap,
} from "lucide-react";

const pipelineSteps = [
  {
    icon: Database,
    title: "Data Collection",
    description:
      "Curated dataset of 20 courses from leading platforms including Coursera, edX, Udemy, and more for prototype demonstration.",
  },
  {
    icon: FileText,
    title: "Text Preprocessing",
    description:
      "Tokenization, lowercasing, stop-word removal, lemmatization, and special character handling.",
  },
  {
    icon: Layers,
    title: "Feature Extraction",
    description:
      "TF-IDF vectorization for keyword-based features and sentence embeddings for semantic features.",
  },
  {
    icon: Zap,
    title: "Model Training",
    description:
      "Trained both TF-IDF sparse matrix similarity and neural sentence transformer models.",
  },
];

const models = [
  {
    icon: Cpu,
    name: "TF-IDF Model",
    color: "accent",
    description:
      "Term Frequency-Inverse Document Frequency (TF-IDF) is a statistical measure that evaluates how relevant a word is to a document in a collection.",
    features: [
      "Fast keyword-based matching",
      "Precise term frequency analysis",
      "Cosine similarity for ranking",
      "Sparse matrix representation",
      "Great for exact phrase matching",
    ],
    techStack: ["scikit-learn", "NumPy", "SciPy"],
  },
  {
    icon: Brain,
    name: "Neural Semantic Model",
    color: "primary",
    description:
      "Sentence Transformers use deep neural networks to encode sentences into dense vector embeddings that capture semantic meaning.",
    features: [
      "Deep semantic understanding",
      "Context-aware embeddings",
      "Handles synonyms and paraphrases",
      "768-dimensional dense vectors",
      "State-of-the-art accuracy",
    ],
    techStack: ["Sentence-Transformers", "PyTorch", "FAISS"],
  },
];

export default function About() {
  return (
    <Layout>
      <div className="container max-w-7xl mx-auto px-4 py-12 md:py-16 overflow-hidden">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="font-display text-3xl md:text-4xl font-bold text-foreground mb-4">
            How SmartCourse Works
          </h1>
          <p className="text-lg text-muted-foreground">
            A deep dive into the NLP pipeline, preprocessing steps, and AI models
            that power our intelligent course recommendations.
          </p>
        </div>

        {/* Pipeline Section */}
        <section className="mb-20">
          <h2 className="font-display text-2xl font-bold text-foreground mb-8 text-center">
            The NLP Pipeline
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {pipelineSteps.map((step, index) => (
              <div key={step.title} className="relative">
                <Card
                  className="h-full hover-lift animate-fade-up"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <CardContent className="p-6">
                    <div className="h-12 w-12 rounded-xl gradient-primary flex items-center justify-center mb-4">
                      <step.icon className="h-6 w-6 text-primary-foreground" />
                    </div>
                    <h3 className="font-display font-semibold text-lg text-foreground mb-2">
                      {step.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {step.description}
                    </p>
                  </CardContent>
                </Card>
                {index < pipelineSteps.length - 1 && (
                  <ArrowRight className="hidden lg:block absolute top-1/2 -right-5 transform -translate-y-1/2 h-6 w-6 text-muted-foreground" />
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Dataset Section */}
        <section className="mb-20">
          <Card className="bg-secondary/30 border-border/50">
            <CardHeader>
              <CardTitle className="font-display text-2xl flex items-center gap-3">
                <Database className="h-6 w-6 text-primary" />
                Dataset Overview
              </CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div>
                <div className="font-display text-3xl font-bold text-primary mb-2">
                  50,000+
                </div>
                <p className="text-muted-foreground">
                  Courses from top educational platforms worldwide
                </p>
              </div>
              <div>
                <div className="font-display text-3xl font-bold text-primary mb-2">
                  15+
                </div>
                <p className="text-muted-foreground">
                  Subject categories covering tech, business, arts, and sciences
                </p>
              </div>
              <div>
                <div className="font-display text-3xl font-bold text-primary mb-2">
                  1M+
                </div>
                <p className="text-muted-foreground">
                  Unique terms indexed for comprehensive search coverage
                </p>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Preprocessing Section */}
        <section className="mb-20">
          <h2 className="font-display text-2xl font-bold text-foreground mb-8 text-center">
            NLP Preprocessing
          </h2>
          <Card>
            <CardContent className="p-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-4">
                  <h3 className="font-display font-semibold text-lg text-foreground">
                    Text Cleaning Steps
                  </h3>
                  <ul className="space-y-3">
                    {[
                      "Tokenization: Split text into individual words/tokens",
                      "Lowercasing: Convert all text to lowercase",
                      "Stop-word Removal: Filter common words (the, is, at)",
                      "Lemmatization: Reduce words to base form",
                      "Special Character Removal: Clean punctuation and symbols",
                      "N-gram Extraction: Capture phrase patterns",
                    ].map((item) => (
                      <li key={item} className="flex items-start gap-3">
                        <Code className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                        <span className="text-muted-foreground">{item}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="bg-secondary/50 rounded-xl p-6">
                  <h4 className="font-mono text-sm text-muted-foreground mb-4">
                    Example Transformation:
                  </h4>
                  <div className="space-y-4 font-mono text-sm">
                    <div>
                      <span className="text-muted-foreground">Input:</span>
                      <p className="text-foreground mt-1">
                        "Learn Machine Learning with Python!"
                      </p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                    <div>
                      <span className="text-muted-foreground">Tokens:</span>
                      <p className="text-foreground mt-1">
                        ["learn", "machine", "learning", "python"]
                      </p>
                    </div>
                    <ArrowRight className="h-4 w-4 text-muted-foreground" />
                    <div>
                      <span className="text-muted-foreground">Lemmatized:</span>
                      <p className="text-foreground mt-1">
                        ["learn", "machine", "learn", "python"]
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Models Section */}
        <section>
          <h2 className="font-display text-2xl font-bold text-foreground mb-8 text-center">
            AI Models
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {models.map((model, index) => (
              <Card
                key={model.name}
                className="hover-lift animate-fade-up"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <CardHeader>
                  <CardTitle className="font-display text-xl flex items-center gap-3">
                    <div
                      className={`h-10 w-10 rounded-lg flex items-center justify-center ${
                        model.color === "primary"
                          ? "gradient-primary"
                          : "gradient-accent"
                      }`}
                    >
                      <model.icon className="h-5 w-5 text-primary-foreground" />
                    </div>
                    {model.name}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <p className="text-muted-foreground">{model.description}</p>

                  <div>
                    <h4 className="font-semibold text-foreground mb-3">
                      Key Features
                    </h4>
                    <ul className="space-y-2">
                      {model.features.map((feature) => (
                        <li
                          key={feature}
                          className="flex items-center gap-2 text-sm text-muted-foreground"
                        >
                          <div
                            className={`h-1.5 w-1.5 rounded-full ${
                              model.color === "primary"
                                ? "bg-primary"
                                : "bg-accent"
                            }`}
                          />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-foreground mb-3">
                      Tech Stack
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {model.techStack.map((tech) => (
                        <span
                          key={tech}
                          className="px-3 py-1 bg-secondary rounded-full text-sm text-muted-foreground"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </Layout>
  );
}
