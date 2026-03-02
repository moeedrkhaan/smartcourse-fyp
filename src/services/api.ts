/**
 * API Service for Frontend
 * Handles all communication with Flask backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';

export interface RecommendationRequest {
  query: string;
  model: 'tfidf' | 'neural';
}

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
  relevanceScore: number;
  model: string;
}

export interface RecommendationResponse {
  success: boolean;
  query: string;
  model: {
    type: string;
    description: string;
    strengths: string;
  };
  results: Course[];
  history_id: number;
  timestamp: string;
}

export interface SearchHistory {
  id: number;
  query: string;
  model: string;
  results_count: number;
  timestamp: string;
  session_id?: string;
}

export interface SavedRecommendation {
  id: number;
  course_id: string;
  course_title: string;
  course_provider: string;
  query: string;
  model: string;
  relevance_score: number;
  timestamp: string;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  /**
   * Get authorization headers with JWT token if available
   */
  private getHeaders(includeAuth: boolean = true): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (includeAuth) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) {
      throw new Error('API health check failed');
    }
    return response.json();
  }

  /**
   * Get course recommendations
   */
  async getRecommendations(
    query: string,
    model: 'tfidf' | 'neural'
  ): Promise<RecommendationResponse> {
    const response = await fetch(`${this.baseURL}/recommend`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ query, model }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get recommendations');
    }

    return response.json();
  }

  /**
   * Get search history
   */
  async getSearchHistory(limit: number = 50): Promise<SearchHistory[]> {
    const response = await fetch(`${this.baseURL}/history?limit=${limit}`, {
      headers: this.getHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to get search history');
    }

    const data = await response.json();
    return data.history;
  }

  /**
   * Save a recommendation
   */
  async saveRecommendation(
    courseId: string,
    query: string,
    model: string
  ): Promise<any> {
    const response = await fetch(`${this.baseURL}/save`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        course_id: courseId,
        query: query,
        model: model,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to save recommendation');
    }

    return response.json();
  }

  /**
   * Get saved recommendations
   */
  async getSavedRecommendations(limit: number = 100): Promise<SavedRecommendation[]> {
    const response = await fetch(`${this.baseURL}/saved?limit=${limit}`, {
      headers: this.getHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to get saved recommendations');
    }

    const data = await response.json();
    return data.saved;
  }

  /**
   * Compare both models side-by-side
   */
  async compareModels(query: string): Promise<any> {
    const response = await fetch(`${this.baseURL}/compare`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to compare models');
    }

    return response.json();
  }

  /**
   * Get all courses
   */
  async getAllCourses(): Promise<Course[]> {
    const response = await fetch(`${this.baseURL}/courses`);
    
    if (!response.ok) {
      throw new Error('Failed to get courses');
    }

    const data = await response.json();
    return data.courses;
  }

  /**
   * Delete a search history item
   */
  async deleteSearchHistory(historyId: number): Promise<any> {
    const response = await fetch(`${this.baseURL}/history/${historyId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to delete history item');
    }

    return response.json();
  }

  /**
   * Delete a saved recommendation
   */
  async deleteSavedRecommendation(savedId: number): Promise<any> {
    const response = await fetch(`${this.baseURL}/saved/${savedId}`, {
      method: 'DELETE',
      headers: this.getHeaders(),
    });

    if (!response.ok) {
      throw new Error('Failed to delete saved recommendation');
    }

    return response.json();
  }
}

export const apiService = new ApiService();
export default apiService;
