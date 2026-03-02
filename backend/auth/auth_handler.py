"""
Authentication Handler for SmartCourse
Handles user registration, login, and JWT token management
"""

import sqlite3
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

class AuthHandler:
    """Handles user authentication operations"""
    
    def __init__(self, db_path: str = 'smartcourse.db'):
        """
        Initialize auth handler
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize_users_table(self):
        """Create users table if it doesn't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_email 
            ON users(email)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_users_username 
            ON users(username)
        ''')
        
        conn.commit()
        conn.close()
        
        print("✓ Users table initialized")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            password: Plain text password
            password_hash: Stored password hash
            
        Returns:
            True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def register_user(self, email: str, username: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Register a new user
        
        Args:
            email: User email
            username: Username
            password: Plain text password
            
        Returns:
            Tuple of (success, message, user_id)
        """
        # Validate input
        if not email or not username or not password:
            return False, "All fields are required", None
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters", None
        
        if '@' not in email:
            return False, "Invalid email format", None
        
        # Hash password
        password_hash = self.hash_password(password)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (email, username, password_hash)
                VALUES (?, ?, ?)
            ''', (email.lower(), username, password_hash))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return True, "User registered successfully", user_id
            
        except sqlite3.IntegrityError as e:
            conn.close()
            if 'email' in str(e):
                return False, "Email already registered", None
            elif 'username' in str(e):
                return False, "Username already taken", None
            else:
                return False, "Registration failed", None
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}", None
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Login a user
        
        Args:
            email: User email
            password: Plain text password
            
        Returns:
            Tuple of (success, message, user_data)
        """
        if not email or not password:
            return False, "Email and password are required", None
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, username, password_hash
            FROM users
            WHERE email = ?
        ''', (email.lower(),))
        
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return False, "Invalid email or password", None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            conn.close()
            return False, "Invalid email or password", None
        
        conn.close()
        
        user_data = {
            'id': user['id'],
            'email': user['email'],
            'username': user['username']
        }
        
        return True, "Login successful", user_data
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data dict or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, username, created_at
            FROM users
            WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'created_at': user['created_at']
            }
        
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User data dict or None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, email, username, created_at
            FROM users
            WHERE email = ?
        ''', (email.lower(),))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user['id'],
                'email': user['email'],
                'username': user['username'],
                'created_at': user['created_at']
            }
        
        return None
