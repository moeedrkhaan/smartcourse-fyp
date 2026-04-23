"""
Course Dataset Loader
Loads and manages course data for the recommendation system
"""

import pandas as pd
import json
import os
import ast
from typing import List, Dict

class CourseDataLoader:
    """Handles loading and managing course dataset"""
    
    def __init__(self, data_path: str = None):
        """
        Initialize course data loader
        
        Args:
            data_path: Path to course data file (JSON or CSV)
        """
        self.data_path = data_path
        self.courses_df = None

    def _resolve_data_path(self) -> str:
        """Resolve best available dataset path with clear priority."""
        candidates = []

        if self.data_path:
            candidates.append(self.data_path)

        env_path = os.getenv('COURSE_DATA_PATH', '').strip()
        if env_path:
            candidates.append(env_path)

        candidates.extend([
            'data/processed/courses_cleaned.csv',
            'data/courses.json',
        ])

        for path in candidates:
            if path and os.path.exists(path):
                return path

        # Keep default behavior path for logs when nothing exists.
        return self.data_path or 'data/courses.json'

    def _normalize_tags(self, value):
        """Convert tags field into a clean list of strings."""
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        if pd.isna(value):
            return []

        text = str(value).strip()
        if not text:
            return []

        if text.startswith('[') and text.endswith(']'):
            try:
                parsed = ast.literal_eval(text)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except Exception:
                pass

        for sep in ['|', ',', ';']:
            if sep in text:
                return [part.strip() for part in text.split(sep) if part.strip()]

        return [text]
    
    def load_courses(self) -> pd.DataFrame:
        """
        Load course data from file or use default dataset
        
        Returns:
            DataFrame with course information
        """
        active_path = self._resolve_data_path()
        try:
            # Try loading from file
            if active_path.endswith('.json'):
                with open(active_path, 'r', encoding='utf-8') as f:
                    courses_data = json.load(f)
                self.courses_df = pd.DataFrame(courses_data)
            elif active_path.endswith('.csv'):
                self.courses_df = pd.read_csv(active_path)
            else:
                raise ValueError(f"Unsupported file format: {active_path}")
            
            print(f"  → Loaded {len(self.courses_df)} courses from {active_path}")
            
        except FileNotFoundError:
            print(f"  → Course data file not found at {active_path}")
            print(f"  → Using default course dataset")
            self.courses_df = self._get_default_courses()
        
        # Validate and clean data
        self._validate_courses()
        
        return self.courses_df
    
    def _validate_courses(self):
        """Validate and clean course data"""
        required_columns = ['id', 'title', 'provider', 'description']
        
        # Check required columns
        for col in required_columns:
            if col not in self.courses_df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Fill missing optional columns with defaults
        if 'tags' not in self.courses_df.columns:
            self.courses_df['tags'] = [[] for _ in range(len(self.courses_df))]
        
        if 'level' not in self.courses_df.columns:
            self.courses_df['level'] = 'Not specified'
        
        if 'duration' not in self.courses_df.columns:
            self.courses_df['duration'] = 'Self-paced'
        
        if 'students' not in self.courses_df.columns:
            self.courses_df['students'] = 'N/A'
        
        if 'rating' not in self.courses_df.columns:
            self.courses_df['rating'] = 0.0

        if 'department' not in self.courses_df.columns:
            self.courses_df['department'] = 'General'

        if 'url' not in self.courses_df.columns:
            self.courses_df['url'] = ''

        # Normalize tags and type-safe fields.
        self.courses_df['tags'] = self.courses_df['tags'].apply(self._normalize_tags)
        self.courses_df['title'] = self.courses_df['title'].astype(str).str.strip()
        self.courses_df['description'] = self.courses_df['description'].astype(str).str.strip()
        self.courses_df['provider'] = self.courses_df['provider'].astype(str).str.strip()
        self.courses_df['department'] = self.courses_df['department'].astype(str).str.strip()
        self.courses_df['rating'] = pd.to_numeric(self.courses_df['rating'], errors='coerce').fillna(0.0)
        self.courses_df['rating'] = self.courses_df['rating'].clip(lower=0.0, upper=5.0)
        
        # Remove empty critical rows.
        self.courses_df = self.courses_df[
            (self.courses_df['title'] != '') & (self.courses_df['description'] != '')
        ].copy()

        # Remove duplicates
        initial_count = len(self.courses_df)
        self.courses_df = self.courses_df.drop_duplicates(subset=['id'])
        removed = initial_count - len(self.courses_df)
        if removed > 0:
            print(f"  → Removed {removed} duplicate courses")
    
    def _get_default_courses(self) -> pd.DataFrame:
        """
        Get default course dataset for testing/demo
        
        Returns:
            DataFrame with sample courses
        """
        courses = [
            {
                "id": "1",
                "title": "Machine Learning Fundamentals with Python",
                "provider": "Stanford Online",
                "description": "Master the fundamentals of machine learning including supervised and unsupervised learning, neural networks, and practical implementations with Python. Learn regression, classification, clustering, and deep learning basics.",
                "level": "Intermediate",
                "duration": "12 weeks",
                "students": "145,000+",
                "rating": 4.8,
                "tags": ["Python", "Machine Learning", "AI", "Neural Networks", "Deep Learning"]
            },
            {
                "id": "2",
                "title": "Deep Learning Specialization",
                "provider": "DeepLearning.AI",
                "description": "Build neural networks from scratch, understand CNNs, RNNs, LSTMs, and Transformers. Apply deep learning to computer vision, NLP, and sequence modeling. Real-world projects included.",
                "level": "Advanced",
                "duration": "16 weeks",
                "students": "320,000+",
                "rating": 4.9,
                "tags": ["Deep Learning", "TensorFlow", "Neural Networks", "CNN", "RNN", "LSTM"]
            },
            {
                "id": "3",
                "title": "Natural Language Processing with Transformers",
                "provider": "Hugging Face",
                "description": "Learn to apply transformer models to NLP tasks including text classification, named entity recognition, question answering, and text generation. Use BERT, GPT, and T5 models.",
                "level": "Advanced",
                "duration": "8 weeks",
                "students": "52,000+",
                "rating": 4.7,
                "tags": ["NLP", "Transformers", "BERT", "GPT", "Text Processing"]
            },
            {
                "id": "4",
                "title": "Data Science Professional Certificate",
                "provider": "IBM",
                "description": "Complete data science program covering Python, SQL, data analysis, visualization, machine learning, and big data. Build portfolio projects and earn professional certificate.",
                "level": "Beginner",
                "duration": "10 months",
                "students": "500,000+",
                "rating": 4.6,
                "tags": ["Data Science", "Python", "SQL", "Data Analysis", "Visualization"]
            },
            {
                "id": "5",
                "title": "Full-Stack Web Development Bootcamp",
                "provider": "Meta",
                "description": "Learn HTML, CSS, JavaScript, React, Node.js, Express, MongoDB, and deployment. Build real-world web applications from front-end to back-end.",
                "level": "Beginner",
                "duration": "6 months",
                "students": "280,000+",
                "rating": 4.7,
                "tags": ["Web Development", "JavaScript", "React", "Node.js", "Full Stack"]
            },
            {
                "id": "6",
                "title": "Python for Data Science and Machine Learning",
                "provider": "University of Michigan",
                "description": "Comprehensive Python course for data science. Learn NumPy, Pandas, Matplotlib, Scikit-learn, and statistical analysis. Apply ML algorithms to real datasets.",
                "level": "Intermediate",
                "duration": "14 weeks",
                "students": "420,000+",
                "rating": 4.8,
                "tags": ["Python", "Data Science", "Pandas", "NumPy", "Machine Learning"]
            },
            {
                "id": "7",
                "title": "Computer Vision and Image Processing",
                "provider": "MIT OpenCourseWare",
                "description": "Study computer vision fundamentals, image processing, object detection, facial recognition, and semantic segmentation. Use OpenCV and PyTorch.",
                "level": "Advanced",
                "duration": "12 weeks",
                "students": "95,000+",
                "rating": 4.7,
                "tags": ["Computer Vision", "Image Processing", "OpenCV", "PyTorch", "Object Detection"]
            },
            {
                "id": "8",
                "title": "Cloud Computing with AWS",
                "provider": "Amazon Web Services",
                "description": "Master AWS services including EC2, S3, Lambda, RDS, and CloudFormation. Learn cloud architecture, deployment, scaling, and security best practices.",
                "level": "Intermediate",
                "duration": "10 weeks",
                "students": "180,000+",
                "rating": 4.6,
                "tags": ["Cloud Computing", "AWS", "DevOps", "Infrastructure", "Deployment"]
            },
            {
                "id": "9",
                "title": "Cybersecurity Fundamentals",
                "provider": "ISC2",
                "description": "Learn security principles, risk management, cryptography, network security, and incident response. Prepare for CISSP certification.",
                "level": "Intermediate",
                "duration": "16 weeks",
                "students": "125,000+",
                "rating": 4.5,
                "tags": ["Cybersecurity", "Network Security", "Cryptography", "Risk Management"]
            },
            {
                "id": "10",
                "title": "iOS App Development with Swift",
                "provider": "Apple Developer",
                "description": "Build iOS apps from scratch using Swift and SwiftUI. Learn iOS design patterns, API integration, Core Data, and App Store deployment.",
                "level": "Beginner",
                "duration": "12 weeks",
                "students": "75,000+",
                "rating": 4.8,
                "tags": ["iOS", "Swift", "SwiftUI", "Mobile Development", "App Development"]
            },
            {
                "id": "11",
                "title": "Artificial Intelligence: Foundations of Computational Agents",
                "provider": "MIT",
                "description": "Comprehensive AI course covering search algorithms, knowledge representation, planning, reasoning under uncertainty, and reinforcement learning.",
                "level": "Advanced",
                "duration": "15 weeks",
                "students": "110,000+",
                "rating": 4.9,
                "tags": ["AI", "Algorithms", "Reinforcement Learning", "Knowledge Representation"]
            },
            {
                "id": "12",
                "title": "Blockchain and Cryptocurrency Technologies",
                "provider": "Berkeley",
                "description": "Understand blockchain fundamentals, cryptocurrency economics, smart contracts, DeFi, and NFTs. Build blockchain applications with Ethereum.",
                "level": "Intermediate",
                "duration": "8 weeks",
                "students": "88,000+",
                "rating": 4.5,
                "tags": ["Blockchain", "Cryptocurrency", "Ethereum", "Smart Contracts", "DeFi"]
            },
            {
                "id": "13",
                "title": "Data Structures and Algorithms",
                "provider": "Princeton",
                "description": "Master fundamental data structures (arrays, linked lists, trees, graphs) and algorithms (sorting, searching, dynamic programming). Essential for coding interviews.",
                "level": "Intermediate",
                "duration": "10 weeks",
                "students": "320,000+",
                "rating": 4.9,
                "tags": ["Data Structures", "Algorithms", "Computer Science", "Programming"]
            },
            {
                "id": "14",
                "title": "UI/UX Design Principles",
                "provider": "Google",
                "description": "Learn user interface design, user experience research, prototyping with Figma, usability testing, and design thinking methodology.",
                "level": "Beginner",
                "duration": "6 weeks",
                "students": "195,000+",
                "rating": 4.7,
                "tags": ["UI/UX", "Design", "Figma", "User Research", "Prototyping"]
            },
            {
                "id": "15",
                "title": "DevOps and CI/CD Pipeline",
                "provider": "Linux Foundation",
                "description": "Master DevOps practices, Docker, Kubernetes, Jenkins, GitLab CI, infrastructure as code, and automated testing and deployment.",
                "level": "Advanced",
                "duration": "12 weeks",
                "students": "145,000+",
                "rating": 4.8,
                "tags": ["DevOps", "Docker", "Kubernetes", "CI/CD", "Automation"]
            },
            {
                "id": "16",
                "title": "SQL and Database Management",
                "provider": "Oracle",
                "description": "Comprehensive SQL course covering queries, joins, subqueries, indexing, normalization, and database design. Learn PostgreSQL and MySQL.",
                "level": "Beginner",
                "duration": "8 weeks",
                "students": "410,000+",
                "rating": 4.6,
                "tags": ["SQL", "Database", "PostgreSQL", "MySQL", "Data Management"]
            },
            {
                "id": "17",
                "title": "Game Development with Unity",
                "provider": "Unity Technologies",
                "description": "Create 2D and 3D games using Unity and C#. Learn game physics, animation, AI, multiplayer networking, and monetization strategies.",
                "level": "Intermediate",
                "duration": "14 weeks",
                "students": "225,000+",
                "rating": 4.7,
                "tags": ["Game Development", "Unity", "C#", "3D Graphics", "Game Design"]
            },
            {
                "id": "18",
                "title": "Quantum Computing Fundamentals",
                "provider": "IBM Quantum",
                "description": "Introduction to quantum computing concepts, quantum gates, algorithms, and programming with Qiskit. Explore quantum supremacy and applications.",
                "level": "Advanced",
                "duration": "10 weeks",
                "students": "42,000+",
                "rating": 4.6,
                "tags": ["Quantum Computing", "Qiskit", "Quantum Algorithms", "Physics"]
            },
            {
                "id": "19",
                "title": "Business Analytics with Excel and Power BI",
                "provider": "Microsoft",
                "description": "Learn data analysis, visualization, dashboards, and business intelligence using Excel, Power BI, and DAX. Make data-driven business decisions.",
                "level": "Beginner",
                "duration": "6 weeks",
                "students": "350,000+",
                "rating": 4.5,
                "tags": ["Business Analytics", "Excel", "Power BI", "Data Visualization", "BI"]
            },
            {
                "id": "20",
                "title": "Ethical Hacking and Penetration Testing",
                "provider": "EC-Council",
                "description": "Learn ethical hacking techniques, vulnerability assessment, penetration testing, and security auditing. Prepare for CEH certification.",
                "level": "Advanced",
                "duration": "16 weeks",
                "students": "98,000+",
                "rating": 4.8,
                "tags": ["Ethical Hacking", "Penetration Testing", "Security", "CEH", "Cybersecurity"]
            }
        ]
        
        return pd.DataFrame(courses)
    
    def get_all_courses_json(self) -> List[Dict]:
        """
        Get all courses as list of dictionaries
        
        Returns:
            List of course dictionaries
        """
        if self.courses_df is None:
            self.load_courses()
        
        return self.courses_df.to_dict('records')
    
    def get_course_by_id(self, course_id: str) -> Dict:
        """
        Get a specific course by ID
        
        Args:
            course_id: Course identifier
            
        Returns:
            Course dictionary or None if not found
        """
        if self.courses_df is None:
            self.load_courses()
        
        course = self.courses_df[self.courses_df['id'] == course_id]
        
        if len(course) == 0:
            return None
        
        return course.iloc[0].to_dict()
    
    def save_courses(self, filepath: str):
        """
        Save courses to JSON file
        
        Args:
            filepath: Path to save courses
        """
        if self.courses_df is None:
            raise ValueError("No courses loaded")
        
        courses_list = self.courses_df.to_dict('records')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(courses_list, f, indent=2, ensure_ascii=False)
        
        print(f"Courses saved to {filepath}")
