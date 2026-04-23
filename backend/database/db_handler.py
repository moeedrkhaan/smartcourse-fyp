"""
Database handler for SmartCourse recommendation system
Manages search history and saved recommendations using SQLite
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import json

class DatabaseHandler:
    """Handles all database operations for the recommendation system"""
    
    def __init__(self, db_path: str = 'smartcourse.db'):
        """
        Initialize database handler
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        print("Initializing database...")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table FIRST (before tables with foreign keys)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create search_history table with user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT NOT NULL,
                model TEXT NOT NULL,
                results_count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Create saved_recommendations table with user_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS saved_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_id TEXT NOT NULL,
                course_title TEXT,
                course_provider TEXT,
                query TEXT NOT NULL,
                model TEXT NOT NULL,
                relevance_score INTEGER,
                session_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Migrate existing tables to add user_id if column doesn't exist
        try:
            cursor.execute("ALTER TABLE search_history ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE saved_recommendations ADD COLUMN user_id INTEGER")
        except sqlite3.OperationalError:
            pass  # Column already exists

        try:
            cursor.execute("ALTER TABLE saved_recommendations ADD COLUMN session_id TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        # Create indexes for better query performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_timestamp 
            ON search_history(timestamp DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_search_user 
            ON search_history(user_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_saved_timestamp 
            ON saved_recommendations(timestamp DESC)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_saved_user 
            ON saved_recommendations(user_id)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_saved_session 
            ON saved_recommendations(session_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_saved_course 
            ON saved_recommendations(course_id)
        ''')
        
        conn.commit()
        conn.close()
        
        print("✓ Database initialized successfully")
    
    def save_search_history(
        self,
        query: str,
        model: str,
        results_count: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> int:
        """
        Save a search query to history
        
        Args:
            query: User's search query
            model: Model used ('tfidf' or 'neural')
            results_count: Number of results returned
            user_id: User ID (optional for guest users)
            session_id: Optional session identifier
            
        Returns:
            ID of inserted record
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO search_history (query, model, results_count, user_id, session_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (query, model, results_count, user_id, session_id))
        
        history_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return history_id
    
    def get_search_history(
        self,
        user_id: Optional[int] = None,
        limit: int = 50,
        session_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve search history
        
        Args:
            user_id: User ID for authenticated requests
            limit: Maximum number of records to return
            session_id: Guest session identifier for unauthenticated requests
            
        Returns:
            List of search history records
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                SELECT id, query, model, results_count, timestamp, session_id
                FROM search_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
        elif session_id:
            cursor.execute('''
                SELECT id, query, model, results_count, timestamp, session_id
                FROM search_history
                WHERE user_id IS NULL AND session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
        else:
            rows = []
            conn.close()
            return rows
        
        rows = cursor.fetchall()
        conn.close()
        
        history = []
        for row in rows:
            history.append({
                'id': row['id'],
                'query': row['query'],
                'model': row['model'],
                'results_count': row['results_count'],
                'timestamp': row['timestamp'],
                'session_id': row['session_id']
            })
        
        return history
    
    def save_recommendation(
        self,
        course_id: str,
        query: str,
        model: str,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None,
        course_title: Optional[str] = None,
        course_provider: Optional[str] = None,
        relevance_score: Optional[int] = None
    ) -> int:
        """
        Save a course recommendation
        
        Args:
            course_id: Unique course identifier
            query: Original search query
            model: Model used for recommendation
            user_id: User ID (optional for guest users)
            session_id: Guest session identifier (optional)
            course_title: Course title (optional)
            course_provider: Course provider (optional)
            relevance_score: Relevance score (optional)
            
        Returns:
            ID of inserted record
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO saved_recommendations 
            (course_id, course_title, course_provider, query, model, relevance_score, user_id, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (course_id, course_title, course_provider, query, model, relevance_score, user_id, session_id))
        
        saved_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return saved_id
    
    def get_saved_recommendations(
        self,
        user_id: Optional[int] = None,
        limit: int = 100,
        session_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Retrieve saved recommendations
        
        Args:
            user_id: User ID for authenticated requests
            limit: Maximum number of records to return
            session_id: Guest session identifier for unauthenticated requests
            
        Returns:
            List of saved recommendation records
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                SELECT id, course_id, course_title, course_provider, 
                       query, model, relevance_score, timestamp
                FROM saved_recommendations
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
        elif session_id:
            cursor.execute('''
                SELECT id, course_id, course_title, course_provider, 
                       query, model, relevance_score, timestamp
                FROM saved_recommendations
                WHERE user_id IS NULL AND session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
        else:
            rows = []
            conn.close()
            return rows
        
        rows = cursor.fetchall()
        conn.close()
        
        saved = []
        for row in rows:
            saved.append({
                'id': row['id'],
                'course_id': row['course_id'],
                'course_title': row['course_title'],
                'course_provider': row['course_provider'],
                'query': row['query'],
                'model': row['model'],
                'relevance_score': row['relevance_score'],
                'timestamp': row['timestamp']
            })
        
        return saved
    
    def is_course_saved(self, course_id: str, user_id: Optional[int] = None) -> bool:
        """
        Check if a course is already saved
        
        Args:
            course_id: Course identifier
            user_id: User ID (optional for guest users)
            
        Returns:
            True if course is saved, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM saved_recommendations
                WHERE course_id = ? AND user_id = ?
            ''', (course_id, user_id))
        else:
            cursor.execute('''
                SELECT COUNT(*) as count
                FROM saved_recommendations
                WHERE course_id = ?
            ''', (course_id,))
        
        count = cursor.fetchone()['count']
        conn.close()
        
        return count > 0
    
    def delete_search_history(
        self,
        history_id: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Delete a search history item
        
        Args:
            history_id: ID of history item
            user_id: User ID (optional, for additional security)
            session_id: Guest session ID (optional, for additional security)
            
        Returns:
            True if deleted, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                DELETE FROM search_history
                WHERE id = ? AND user_id = ?
            ''', (history_id, user_id))
        elif session_id:
            cursor.execute('''
                DELETE FROM search_history
                WHERE id = ? AND user_id IS NULL AND session_id = ?
            ''', (history_id, session_id))
        else:
            conn.close()
            return False
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def delete_saved_recommendation(
        self,
        saved_id: int,
        user_id: Optional[int] = None,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Delete a saved recommendation
        
        Args:
            saved_id: ID of saved recommendation
            user_id: User ID (optional, for additional security)
            session_id: Guest session ID (optional, for additional security)
            
        Returns:
            True if deleted, False otherwise
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('''
                DELETE FROM saved_recommendations
                WHERE id = ? AND user_id = ?
            ''', (saved_id, user_id))
        elif session_id:
            cursor.execute('''
                DELETE FROM saved_recommendations
                WHERE id = ? AND user_id IS NULL AND session_id = ?
            ''', (saved_id, session_id))
        else:
            conn.close()
            return False
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted

    def assign_guest_data_to_user(self, user_id: int, session_id: str) -> Dict[str, int]:
        """
        Assign guest session data to a user after login.

        Args:
            user_id: Logged-in user ID
            session_id: Guest session ID

        Returns:
            Counts of migrated records
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE search_history
            SET user_id = ?
            WHERE user_id IS NULL AND session_id = ?
        ''', (user_id, session_id))
        history_migrated = cursor.rowcount

        cursor.execute('''
            UPDATE saved_recommendations
            SET user_id = ?
            WHERE user_id IS NULL AND session_id = ?
        ''', (user_id, session_id))
        saved_migrated = cursor.rowcount

        conn.commit()
        conn.close()

        return {
            'history_migrated': history_migrated,
            'saved_migrated': saved_migrated
        }
    
    def get_statistics(self) -> Dict:
        """
        Get usage statistics
        
        Returns:
            Dictionary with various statistics
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total searches
        cursor.execute('SELECT COUNT(*) as count FROM search_history')
        total_searches = cursor.fetchone()['count']
        
        # Searches by model
        cursor.execute('''
            SELECT model, COUNT(*) as count
            FROM search_history
            GROUP BY model
        ''')
        searches_by_model = {row['model']: row['count'] for row in cursor.fetchall()}
        
        # Total saved recommendations
        cursor.execute('SELECT COUNT(*) as count FROM saved_recommendations')
        total_saved = cursor.fetchone()['count']
        
        # Most recent searches
        cursor.execute('''
            SELECT query, model, timestamp
            FROM search_history
            ORDER BY timestamp DESC
            LIMIT 5
        ''')
        recent_searches = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total_searches': total_searches,
            'searches_by_model': searches_by_model,
            'total_saved': total_saved,
            'recent_searches': recent_searches
        }
