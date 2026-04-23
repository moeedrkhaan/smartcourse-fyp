"""
Neural Network Based Course Recommender
Uses Sentence-BERT for semantic understanding and similarity
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import torch

class NeuralRecommender:
    """
    Neural network-based recommendation system using Sentence-BERT
    Strengths: Semantic understanding, context awareness, synonym handling
    Best for: Natural language queries with conceptual meaning
    """
    
    def __init__(self, courses_df: pd.DataFrame, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize Neural recommender with pre-trained Sentence-BERT
        
        Args:
            courses_df: DataFrame with columns: id, title, provider, description, etc.
            model_name: Hugging Face model name (default: lightweight MiniLM model)
        """
        self.courses_df = courses_df.copy()
        self.model_name = model_name
        self.model = None
        self.course_embeddings = None
        
        # Check for GPU availability
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"  → Using device: {self.device}")
        
        # Combine text fields for better semantic understanding
        self.courses_df['combined_text'] = (
            self.courses_df['title'] + '. ' +
            self.courses_df['description'] + ' ' +
            self.courses_df['tags'].apply(
                lambda x: '. '.join(x) if isinstance(x, list) else str(x)
            )
        )
        
        self._load_model()
        self._encode_courses()
    
    def _load_model(self):
        """Load pre-trained Sentence-BERT model"""
        print(f"  → Loading Sentence-BERT model: {self.model_name}")
        print("    (First time may take a few minutes to download)")
        
        self.model = SentenceTransformer(self.model_name, device=self.device)
        
        print(f"  → Model loaded successfully")
        print(f"  → Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
    
    def _encode_courses(self):
        """Encode all course descriptions into embeddings"""
        print("  → Encoding course descriptions (this may take a moment)...")
        
        # Batch encode for efficiency
        self.course_embeddings = self.model.encode(
            self.courses_df['combined_text'].tolist(),
            batch_size=32,
            show_progress_bar=True,
            convert_to_tensor=False,  # Return numpy arrays
            normalize_embeddings=True  # Normalize for cosine similarity
        )
        
        print(f"  → Encoded {len(self.course_embeddings)} courses")
        print(f"  → Embeddings shape: {self.course_embeddings.shape}")
    
    def recommend(self, query: str, top_n: int = 10) -> List[Dict]:
        """
        Get course recommendations using semantic similarity
        
        Args:
            query: Natural language search query
            top_n: Number of recommendations to return
            
        Returns:
            List of recommended courses with relevance scores
        """
        # Encode query
        query_embedding = self.model.encode(
            [query],
            convert_to_tensor=False,
            normalize_embeddings=True
        )
        
        # Calculate cosine similarity with all courses
        similarities = cosine_similarity(
            query_embedding,
            self.course_embeddings
        ).flatten()
        
        # Get top N indices
        top_indices = similarities.argsort()[-top_n:][::-1]
        
        # Build recommendations list
        recommendations = []
        for idx in top_indices:
            course = self.courses_df.iloc[idx]
            similarity_score = float(similarities[idx])
            
            # Convert to percentage (0-100)
            # Neural models often have higher baseline similarity, so we adjust
            relevance_score = int(min(similarity_score * 100, 100))
            
            recommendations.append({
                'id': str(course['id']),
                'title': str(course['title']),
                'provider': str(course['provider']),
                'description': str(course['description']),
                'level': str(course.get('level', 'Not specified')),
                'duration': str(course.get('duration', 'Self-paced')),
                'students': str(course.get('students', 'N/A')),
                'rating': float(course.get('rating', 0)),
                'tags': course['tags'] if isinstance(course['tags'], list) else [],
                'relevanceScore': relevance_score,
                'model': 'neural'
            })
        
        return recommendations
    
    def batch_recommend(self, queries: List[str], top_n: int = 10) -> List[List[Dict]]:
        """
        Get recommendations for multiple queries efficiently
        
        Args:
            queries: List of natural language search queries
            top_n: Number of recommendations per query
            
        Returns:
            List of recommendation lists
        """
        # Batch encode queries
        query_embeddings = self.model.encode(
            queries,
            batch_size=32,
            convert_to_tensor=False,
            normalize_embeddings=True
        )
        
        # Calculate similarities for all queries
        similarities = cosine_similarity(query_embeddings, self.course_embeddings)
        
        # Get recommendations for each query
        all_recommendations = []
        for query_idx, query in enumerate(queries):
            query_similarities = similarities[query_idx]
            top_indices = query_similarities.argsort()[-top_n:][::-1]
            
            recommendations = []
            for idx in top_indices:
                course = self.courses_df.iloc[idx]
                similarity_score = float(query_similarities[idx])
                relevance_score = int(min(similarity_score * 100, 100))
                
                recommendations.append({
                    'id': str(course['id']),
                    'title': str(course['title']),
                    'provider': str(course['provider']),
                    'description': str(course['description']),
                    'level': str(course.get('level', 'Not specified')),
                    'duration': str(course.get('duration', 'Self-paced')),
                    'students': str(course.get('students', 'N/A')),
                    'rating': float(course.get('rating', 0)),
                    'tags': course['tags'] if isinstance(course['tags'], list) else [],
                    'relevanceScore': relevance_score,
                    'model': 'neural'
                })
            
            all_recommendations.append(recommendations)
        
        return all_recommendations
    
    def semantic_search(self, query: str, threshold: float = 0.3) -> List[Dict]:
        """
        Semantic search with minimum similarity threshold
        Returns all courses above the threshold, not just top N
        """
        query_embedding = self.model.encode(
            [query],
            convert_to_tensor=False,
            normalize_embeddings=True
        )
        
        similarities = cosine_similarity(
            query_embedding,
            self.course_embeddings
        ).flatten()
        
        # Filter by threshold
        relevant_indices = np.where(similarities >= threshold)[0]
        
        # Sort by similarity
        sorted_indices = relevant_indices[similarities[relevant_indices].argsort()[::-1]]
        
        recommendations = []
        for idx in sorted_indices:
            course = self.courses_df.iloc[idx]
            similarity_score = float(similarities[idx])
            relevance_score = int(min(similarity_score * 100, 100))
            
            recommendations.append({
                'id': str(course['id']),
                'title': str(course['title']),
                'provider': str(course['provider']),
                'description': str(course['description']),
                'level': str(course.get('level', 'Not specified')),
                'duration': str(course.get('duration', 'Self-paced')),
                'students': str(course.get('students', 'N/A')),
                'rating': float(course.get('rating', 0)),
                'tags': course['tags'] if isinstance(course['tags'], list) else [],
                'relevanceScore': relevance_score,
                'model': 'neural'
            })
        
        return recommendations
