"""
SmartCourse Recommendation System - Flask Backend API
Provides intelligent course recommendations using TF-IDF and Neural models
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from datetime import datetime, timedelta
import traceback
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models.tfidf_model import TFIDFRecommender
from models.neural_model import NeuralRecommender
from database.db_handler import DatabaseHandler
from data.course_loader import CourseDataLoader
from auth.auth_handler import AuthHandler

app = Flask(__name__)

# CORS Configuration - Allow requests from frontend
# In production, update this to your specific frontend URL
cors_origins = os.getenv('CORS_ORIGINS', '*').split(',')
CORS(app, origins=cors_origins, supports_credentials=True)

# JWT Configuration - Load from environment variable
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key-for-development')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
jwt = JWTManager(app)

# Initialize components
db_handler = DatabaseHandler()
course_loader = CourseDataLoader()
auth_handler = AuthHandler()
tfidf_model = None
neural_model = None

def initialize_models():
    """Initialize ML models with course data"""
    global tfidf_model, neural_model
    
    print("Loading course dataset...")
    courses_df = course_loader.load_courses()
    
    print("Initializing TF-IDF model...")
    tfidf_model = TFIDFRecommender(courses_df)
    
    print("Initializing Neural model (this may take a moment)...")
    print("  → Downloading Sentence-BERT model (~90MB, first time only)")
    print("  → Please wait, this may take 1-2 minutes...")
    try:
        neural_model = NeuralRecommender(courses_df)
        print("✓ All models initialized successfully!")
    except Exception as e:
        print(f"⚠ Neural model failed to load: {str(e)}")
        print("  → Will use TF-IDF as fallback for both models")
        neural_model = None

# Initialize database and models on app startup (for production servers like gunicorn)
db_handler.initialize_database()
initialize_models()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': {
            'tfidf': tfidf_model is not None,
            'neural': neural_model is not None
        }
    })

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    """
    User registration endpoint
    Accepts: { "email": "user@example.com", "username": "username", "password": "password" }
    Returns: User data and JWT token
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not email or not username or not password:
            return jsonify({'error': 'Email, username, and password are required'}), 400
        
        # Validate email format (basic validation)
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Register user
        success, message, user_id = auth_handler.register_user(email, username, password)
        
        if not success:
            return jsonify({'error': message}), 400
        
        # Create JWT token
        access_token = create_access_token(identity=user_id)
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user_id,
                'email': email,
                'username': username
            },
            'token': access_token
        }), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during registration'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """
    User login endpoint
    Accepts: { "email": "user@example.com", "password": "password" }
    Returns: User data and JWT token
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Attempt login
        success, message, user_data = auth_handler.login_user(email, password)
        
        if not success:
            return jsonify({'error': message}), 401
        
        # Create JWT token
        access_token = create_access_token(identity=user_data['id'])
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user_data['id'],
                'email': user_data['email'],
                'username': user_data['username']
            },
            'token': access_token
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during login'}), 500

@app.route('/api/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user information
    Requires: JWT token in Authorization header
    Returns: User data
    """
    try:
        user_id = get_jwt_identity()
        
        success, message, user_data = auth_handler.get_user_by_id(user_id)
        
        if not success:
            return jsonify({'error': message}), 404
        
        return jsonify({
            'user': {
                'id': user_data['id'],
                'email': user_data['email'],
                'username': user_data['username'],
                'created_at': user_data['created_at']
            }
        }), 200
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': 'An error occurred'}), 500

# ============================================================================
# Recommendation Endpoints
# ============================================================================

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """
    Main recommendation endpoint
    Accepts: { "query": "user preferences", "model": "tfidf" | "neural" }
    Returns: List of top 10 courses with relevance scores
    """
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        query = data['query'].strip()
        model_type = data.get('model', 'neural').lower()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        if model_type not in ['tfidf', 'neural']:
            return jsonify({'error': 'Model must be either "tfidf" or "neural"'}), 400
        
        # Get recommendations from selected model
        if model_type == 'tfidf':
            recommendations = tfidf_model.recommend(query, top_n=10)
            model_info = {
                'type': 'TF-IDF',
                'description': 'Keyword frequency-based matching',
                'strengths': 'Precise keyword matching, fast processing'
            }
        else:
            # Neural model not loaded yet
            if neural_model is None:
                # Fallback to TF-IDF
                recommendations = tfidf_model.recommend(query, top_n=10)
                model_info = {
                    'type': 'TF-IDF (Neural model unavailable)',
                    'description': 'Using TF-IDF as fallback',
                    'strengths': 'Precise keyword matching, fast processing'
                }
            else:
                recommendations = neural_model.recommend(query, top_n=10)
                model_info = {
                    'type': 'Neural (Sentence-BERT)',
                    'description': 'Semantic understanding using transformers',
                    'strengths': 'Understands context and meaning, handles synonyms'
                }
        
        # Save to history (with user_id if authenticated)
        history_id = db_handler.save_search_history(
            query=query,
            model=model_type,
            results_count=len(recommendations),
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'query': query,
            'model': model_info,
            'results': recommendations,
            'history_id': history_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in /api/recommend: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Retrieve user's search history
    Returns: List of previous searches with timestamps
    """
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        limit = request.args.get('limit', 50, type=int)
        history = db_handler.get_search_history(user_id=user_id, limit=limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
        
    except Exception as e:
        print(f"Error in /api/history: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_recommendation():
    """
    Save a course recommendation
    Accepts: { "course_id": "id", "query": "original query", "model": "tfidf"|"neural" }
    """
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        data = request.get_json()
        
        required_fields = ['course_id', 'query', 'model']
        if not all(field in data for field in required_fields):
            return jsonify({'error': f'Missing required fields: {required_fields}'}), 400
        
        saved_id = db_handler.save_recommendation(
            course_id=data['course_id'],
            query=data['query'],
            model=data['model'],
            user_id=user_id
        )
        
        return jsonify({
            'success': True,
            'saved_id': saved_id,
            'message': 'Recommendation saved successfully'
        })
        
    except Exception as e:
        print(f"Error in /api/save: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved', methods=['GET'])
def get_saved_recommendations():
    """
    Retrieve user's saved recommendations
    """
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        limit = request.args.get('limit', 100, type=int)
        saved = db_handler.get_saved_recommendations(user_id=user_id, limit=limit)
        
        return jsonify({
            'success': True,
            'saved': saved,
            'count': len(saved)
        })
        
    except Exception as e:
        print(f"Error in /api/saved: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare', methods=['POST'])
def compare_models():
    """
    Compare TF-IDF and Neural models side-by-side for the same query
    Accepts: { "query": "user preferences" }
    Returns: Results from both models for comparison
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 400
        
        query = data['query'].strip()
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        # Get results from both models
        tfidf_results = tfidf_model.recommend(query, top_n=10)
        
        if neural_model is not None:
            neural_results = neural_model.recommend(query, top_n=10)
        else:
            # Fallback: use TF-IDF for both
            neural_results = tfidf_model.recommend(query, top_n=10)
        
        return jsonify({
            'success': True,
            'query': query,
            'tfidf': {
                'model': 'TF-IDF',
                'results': tfidf_results
            },
            'neural': {
                'model': 'Neural (Sentence-BERT)' if neural_model else 'TF-IDF (fallback)',
                'results': neural_results
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in /api/compare: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    """Delete a search history item"""
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        # Delete the history item
        deleted = db_handler.delete_search_history(history_id, user_id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'History item deleted successfully'
            })
        else:
            return jsonify({'error': 'History item not found or unauthorized'}), 404
        
    except Exception as e:
        print(f"Error in /api/history/<id>: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/saved/<int:saved_id>', methods=['DELETE'])
def delete_saved(saved_id):
    """Delete a saved recommendation"""
    try:
        # Check for optional JWT authentication
        user_id = None
        try:
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
        except:
            pass  # Guest user
        
        # Delete the saved item
        deleted = db_handler.delete_saved_recommendation(saved_id, user_id)
        
        if deleted:
            return jsonify({
                'success': True,
                'message': 'Saved recommendation deleted successfully'
            })
        else:
            return jsonify({'error': 'Saved item not found or unauthorized'}), 404
        
    except Exception as e:
        print(f"Error in /api/saved/<id>: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/courses', methods=['GET'])
def get_all_courses():
    """Get all available courses in the dataset"""
    try:
        courses = course_loader.get_all_courses_json()
        return jsonify({
            'success': True,
            'courses': courses,
            'count': len(courses)
        })
    except Exception as e:
        print(f"Error in /api/courses: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("SmartCourse Recommendation System - Backend API")
    print("=" * 50)
    print("\nStarting Flask development server...")
    print("API will be available at: http://localhost:5000")
    print("=" * 50)
    
    # Use debug=False for production, or read from environment
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
