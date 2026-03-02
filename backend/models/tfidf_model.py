"""
TF-IDF Based Course Recommender
Uses Term Frequency-Inverse Document Frequency for keyword-based matching
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
from typing import List, Dict

class TFIDFRecommender:
    """
    TF-IDF based recommendation system
    Strengths: Exact keyword matching, fast processing
    Best for: Queries with specific technical terms and keywords
    """
    
    def __init__(self, courses_df: pd.DataFrame):
        """
        Initialize TF-IDF model with course data
        
        Args:
            courses_df: DataFrame with columns: id, title, provider, description, etc.
        """
        self.courses_df = courses_df.copy()
        self.vectorizer = None
        self.tfidf_matrix = None
        
        # Combine text fields for better matching
        self.courses_df['combined_text'] = (
            self.courses_df['title'] + ' ' +
            self.courses_df['description'] + ' ' +
            self.courses_df['tags'].apply(lambda x: ' '.join(x) if isinstance(x, list) else str(x))
        )
        
        self._train_model()
    
    def _train_model(self):
        """Train TF-IDF vectorizer on course corpus"""
        print("  → Training TF-IDF vectorizer...")
        
        # Configure TF-IDF with optimal parameters
        self.vectorizer = TfidfVectorizer(
            max_features=5000,          # Limit vocabulary size
            ngram_range=(1, 3),         # Use unigrams, bigrams, and trigrams
            stop_words='english',       # Remove common English words
            min_df=1,                   # Minimum document frequency
            max_df=0.8,                 # Maximum document frequency
            lowercase=True,
            strip_accents='unicode'
        )
        
        # Fit and transform course descriptions
        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.courses_df['combined_text']
        )
        
        print(f"  → TF-IDF matrix shape: {self.tfidf_matrix.shape}")
        print(f"  → Vocabulary size: {len(self.vectorizer.vocabulary_)}")
    
    def recommend(self, query: str, top_n: int = 10) -> List[Dict]:
        """
        Get course recommendations for a user query
        
        Args:
            query: Natural language search query
            top_n: Number of recommendations to return
            
        Returns:
            List of recommended courses with relevance scores
        """
        # Transform query to TF-IDF vector
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity between query and all courses
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top N indices
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        # Build recommendations list
        recommendations = []
        for idx in top_indices:
            course = self.courses_df.iloc[idx]
            similarity_score = float(similarities[idx])
            
            # Convert to percentage (0-100)
            relevance_score = int(similarity_score * 100)
            
            recommendations.append({
                'id': str(course['id']),
                'title': course['title'],
                'provider': course['provider'],
                'description': course['description'],
                'level': course.get('level', 'Not specified'),
                'duration': course.get('duration', 'Self-paced'),
                'students': course.get('students', 'N/A'),
                'rating': float(course.get('rating', 0)),
                'tags': course['tags'] if isinstance(course['tags'], list) else [],
                'relevanceScore': relevance_score,
                'model': 'tfidf'
            })
        
        return recommendations
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        joblib.dump({
            'vectorizer': self.vectorizer,
            'tfidf_matrix': self.tfidf_matrix,
            'courses_df': self.courses_df
        }, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        data = joblib.load(filepath)
        self.vectorizer = data['vectorizer']
        self.tfidf_matrix = data['tfidf_matrix']
        self.courses_df = data['courses_df']
        print(f"Model loaded from {filepath}")
    
    def get_feature_importance(self, query: str, top_n: int = 10) -> List[tuple]:
        """
        Get most important keywords for a query
        Useful for debugging and understanding recommendations
        """
        query_vector = self.vectorizer.transform([query])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get non-zero features
        scores = query_vector.toarray()[0]
        important_features = [(feature_names[i], scores[i]) 
                            for i in scores.argsort()[-top_n:][::-1] 
                            if scores[i] > 0]
        
        return important_features
