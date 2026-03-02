export interface Course {
  id: string;
  title: string;
  provider: string;
  description: string;
  level: string;
  duration: string;
  students: string;
  rating: number;
  tags: string[];
}

export const mockCourses: Course[] = [
  {
    id: "1",
    title: "Machine Learning Fundamentals with Python",
    provider: "Stanford Online",
    description: "Master the fundamentals of machine learning including supervised and unsupervised learning, neural networks, and practical implementations with Python.",
    level: "Intermediate",
    duration: "12 weeks",
    students: "145,000+",
    rating: 4.8,
    tags: ["Python", "ML", "AI"],
  },
  {
    id: "2",
    title: "Deep Learning Specialization",
    provider: "DeepLearning.AI",
    description: "Build neural networks from scratch, understand CNNs, RNNs, LSTMs, and Transformers. Apply deep learning to real-world projects.",
    level: "Advanced",
    duration: "16 weeks",
    students: "320,000+",
    rating: 4.9,
    tags: ["Deep Learning", "TensorFlow", "Neural Networks"],
  },
  {
    id: "3",
    title: "Natural Language Processing with Transformers",
    provider: "Hugging Face",
    description: "Learn to apply transformer models to NLP tasks including text classification, named entity recognition, and question answering.",
    level: "Advanced",
    duration: "8 weeks",
    students: "52,000+",
    rating: 4.7,
    tags: ["NLP", "Transformers", "BERT"],
  },
  {
    id: "4",
    title: "Data Science Professional Certificate",
    provider: "IBM",
    description: "Comprehensive data science training covering Python, SQL, machine learning, data visualization, and real-world capstone projects.",
    level: "Beginner",
    duration: "10 months",
    students: "280,000+",
    rating: 4.6,
    tags: ["Data Science", "Python", "SQL"],
  },
  {
    id: "5",
    title: "Full-Stack Web Development Bootcamp",
    provider: "Meta",
    description: "Learn front-end and back-end development with React, Node.js, databases, and deployment. Build production-ready applications.",
    level: "Beginner",
    duration: "6 months",
    students: "190,000+",
    rating: 4.7,
    tags: ["React", "Node.js", "Web Dev"],
  },
  {
    id: "6",
    title: "Cloud Architecture with AWS",
    provider: "Amazon Web Services",
    description: "Design scalable, secure, and cost-optimized cloud architectures. Prepare for AWS Solutions Architect certification.",
    level: "Intermediate",
    duration: "12 weeks",
    students: "85,000+",
    rating: 4.8,
    tags: ["AWS", "Cloud", "DevOps"],
  },
  {
    id: "7",
    title: "Computer Vision and Image Processing",
    provider: "OpenCV.org",
    description: "Master computer vision techniques including image processing, object detection, facial recognition, and video analysis with OpenCV.",
    level: "Intermediate",
    duration: "10 weeks",
    students: "45,000+",
    rating: 4.5,
    tags: ["Computer Vision", "OpenCV", "Python"],
  },
  {
    id: "8",
    title: "Reinforcement Learning Masterclass",
    provider: "UC Berkeley",
    description: "Deep dive into reinforcement learning algorithms, policy optimization, and multi-agent systems with practical implementations.",
    level: "Advanced",
    duration: "14 weeks",
    students: "28,000+",
    rating: 4.8,
    tags: ["RL", "AI", "Algorithms"],
  },
  {
    id: "9",
    title: "Statistical Analysis with R",
    provider: "Johns Hopkins",
    description: "Learn statistical methods, hypothesis testing, regression analysis, and data visualization using R programming language.",
    level: "Beginner",
    duration: "8 weeks",
    students: "112,000+",
    rating: 4.6,
    tags: ["R", "Statistics", "Analytics"],
  },
  {
    id: "10",
    title: "Kubernetes for DevOps Engineers",
    provider: "Linux Foundation",
    description: "Master container orchestration with Kubernetes. Learn deployments, services, networking, storage, and security best practices.",
    level: "Intermediate",
    duration: "6 weeks",
    students: "67,000+",
    rating: 4.7,
    tags: ["Kubernetes", "Docker", "DevOps"],
  },
];

export function generateRelevanceScore(index: number, modelType: "tfidf" | "neural"): number {
  const baseScore = 98 - (index * 7) + Math.random() * 5;
  const modelBonus = modelType === "neural" ? 2 : 0;
  return Math.min(99, Math.max(60, Math.round(baseScore + modelBonus)));
}
