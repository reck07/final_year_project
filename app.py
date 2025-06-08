from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from model_trainer import load_model, train_model
from data_loader import load_data
from models import db, User, Crop, Recommendation
from path_planner import PathPlanner
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import base64
import cv2
import numpy as np
import logging
import traceback
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_farming.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['GOOGLE_REDIRECT_URI'] = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')

# Initialize extensions
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Load model and scaler
MODEL_FILE = 'models/crop_model.joblib'
SCALER_FILE = 'models/crop_model_scaler.joblib'
DATA_FILE = 'data/crop_data.csv'

model = None
scaler = None

# Google OAuth2 configuration
SCOPES = ['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

def initialize_model():
    global model, scaler
    try:
        # Create directories if they don't exist
        os.makedirs('models', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Train and load model if it doesn't exist
        if not os.path.exists(MODEL_FILE) or not os.path.exists(SCALER_FILE):
            logger.info("Training new model...")
            model, scaler = train_model(DATA_FILE, MODEL_FILE)
        else:
            logger.info("Loading existing model...")
            model = load_model(MODEL_FILE)
            scaler = load_model(SCALER_FILE)
            
        logger.info("Model and scaler loaded successfully")
        return True
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return False

# Initialize model on startup
initialize_model()

# Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['name', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token for immediate login
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        }), 201
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400
        
        # Find user
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token with longer expiration
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=7)  # Extended to 7 days
        }, app.config['SECRET_KEY'])
        
        # Get user's recommendations
        recommendations = Recommendation.query.filter_by(user_id=user.id).all()
        
        return jsonify({
            'access_token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role
            },
            'recommendations': [rec.to_dict() for rec in recommendations]
        })
    except Exception as e:
        logger.error(f"Login error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred during login. Please try again.'}), 500

@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    try:
        # Get user's recommendations
        recommendations = Recommendation.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'id': current_user.id,
            'name': current_user.name,
            'email': current_user.email,
            'role': current_user.role,
            'recommendations': [rec.to_dict() for rec in recommendations]
        })
    except Exception as e:
        logger.error(f"Error getting user info: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred while fetching user data'}), 500

@app.route('/api/recommendations', methods=['GET'])
@token_required
def get_recommendations(current_user):
    try:
        recommendations = Recommendation.query.filter_by(user_id=current_user.id).all()
        return jsonify([rec.to_dict() for rec in recommendations])
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred while fetching recommendations'}), 500

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/api/crop-recommendation', methods=['POST'])
def predict():
    try:
        if not model or not scaler:
            return jsonify({'error': 'Model not loaded. Please try again later.'}), 500

        data = request.get_json()
        
        # Validate input data
        required_fields = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            try:
                float(data[field])
            except ValueError:
                return jsonify({'error': f'Invalid value for {field}. Must be a number.'}), 400

        # Convert input values to float
        user_input = pd.DataFrame({
            'N': [float(data['N'])],
            'P': [float(data['P'])],
            'K': [float(data['K'])],
            'temperature': [float(data['temperature'])],
            'humidity': [float(data['humidity'])],
            'ph': [float(data['ph'])],
            'rainfall': [float(data['rainfall'])],
        })

        # Scale the input
        user_input_scaled = scaler.transform(user_input)

        # Make prediction
        prediction = model.predict(user_input_scaled)

        # Modify the response to match the frontend's expected format
        # In a real application, you would get confidence and description from your model or data source
        recommended_crop_name = prediction[0]
        recommendation_list = [{
            'name': recommended_crop_name,
            'confidence': 0.95, # Placeholder confidence
            'description': f'Based on the provided conditions, {recommended_crop_name} is recommended.' # Placeholder description
        }]

        return jsonify({'recommendations': recommendation_list})
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/path-plan', methods=['POST'])
def path_plan():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['fieldWidth', 'fieldHeight', 'coverageRadius', 'startX', 'startY', 'pattern']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate field dimensions
        if data['fieldWidth'] <= 0 or data['fieldHeight'] <= 0 or data['coverageRadius'] <= 0:
            return jsonify({'error': 'Field dimensions and coverage radius must be positive'}), 400
        
        # Validate start point
        if (data['startX'] < 0 or data['startY'] < 0 or 
            data['startX'] > data['fieldWidth'] or data['startY'] > data['fieldHeight']):
            return jsonify({'error': 'Start point must be within field boundaries'}), 400
        
        # Validate pattern
        valid_patterns = ['zigzag', 'spiral', 'custom']
        if data['pattern'] not in valid_patterns:
            return jsonify({'error': f'Invalid pattern. Choose from: {valid_patterns}'}), 400
        
        # Create path planner instance
        planner = PathPlanner(field_size=(data['fieldWidth'], data['fieldHeight']))
        
        # Generate path with optional parameters
        path = planner.optimize_spraying_pattern(
            start_point=(data['startX'], data['startY']),
            coverage_radius=data['coverageRadius'],
            pattern=data['pattern'],
            spraying_rate=data.get('sprayingRate'),
            smooth_path=data.get('smoothPath', True)
        )
        
        if not path:
            return jsonify({'error': 'Failed to generate path'}), 500
        
        # Calculate statistics
        total_distance = calculate_total_distance(path)
        coverage_area = calculate_coverage_area(path, data['coverageRadius'])
        estimated_time = calculate_estimated_time(path, data.get('sprayingRate', 1.0))
        
        statistics = {
            'totalDistance': total_distance,
            'coverageArea': coverage_area,
            'estimatedTime': estimated_time,
            'numberOfPoints': len(path),
            'pattern': data['pattern'],
            'sprayingRate': data.get('sprayingRate', 1.0)
        }
        
        return jsonify({
            'path': path,
            'statistics': statistics
        })
        
    except Exception as e:
        logger.error(f"Error in path planning: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/path-plan/visualize', methods=['POST'])
def visualize_path():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['path', 'fieldWidth', 'fieldHeight', 'coverageRadius']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create path planner instance
        planner = PathPlanner(field_size=(data['fieldWidth'], data['fieldHeight']))
        
        # Generate visualization
        visualization = planner.visualize_path(data['path'], data['coverageRadius'])
        
        if not visualization:
            return jsonify({'error': 'Failed to generate visualization'}), 500
        
        return jsonify({
            'visualization': visualization
        })
        
    except Exception as e:
        logger.error(f"Error in visualization: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

def calculate_total_distance(path):
    """Calculate the total distance of the path."""
    total_distance = 0
    for i in range(len(path) - 1):
        dx = path[i + 1]['x'] - path[i]['x']
        dy = path[i + 1]['y'] - path[i]['y']
        total_distance += np.sqrt(dx * dx + dy * dy)
    return total_distance

def calculate_coverage_area(path, coverage_radius):
    """Calculate the total coverage area."""
    # Create a grid of points
    x_min = min(p['x'] for p in path) - coverage_radius
    x_max = max(p['x'] for p in path) + coverage_radius
    y_min = min(p['y'] for p in path) - coverage_radius
    y_max = max(p['y'] for p in path) + coverage_radius
    
    # Calculate grid resolution
    resolution = coverage_radius / 2
    x_points = np.arange(x_min, x_max + resolution, resolution)
    y_points = np.arange(y_min, y_max + resolution, resolution)
    
    # Count covered points
    covered_points = 0
    for x in x_points:
        for y in y_points:
            for point in path:
                dx = x - point['x']
                dy = y - point['y']
                if dx * dx + dy * dy <= coverage_radius * coverage_radius:
                    covered_points += 1
                    break
    
    # Calculate area
    area = covered_points * resolution * resolution
    return area

def calculate_estimated_time(path, spraying_rate=1.0):
    """Calculate estimated time to complete the path."""
    # Average speed in meters per minute
    avg_speed = 10.0  # meters per minute
    
    # Calculate total distance
    total_distance = calculate_total_distance(path)
    
    # Calculate time based on distance and spraying rate
    base_time = total_distance / avg_speed
    adjusted_time = base_time * spraying_rate
    
    return adjusted_time

@app.route('/api/pesticide-recommendation', methods=['POST'])
def pesticide_recommendation():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['crop', 'pest', 'severity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate severity level
        valid_severities = ['low', 'medium', 'high']
        if data['severity'].lower() not in valid_severities:
            return jsonify({'error': 'Severity must be one of: low, medium, high'}), 400

        # Get pesticide recommendations based on crop, pest, and severity
        pesticides = get_pesticide_recommendations(
            crop=data['crop'],
            pest=data['pest'],
            severity=data['severity'].lower()
        )
        
        return jsonify({'pesticides': pesticides})
    except Exception as e:
        logger.error(f"Pesticide recommendation error: {e}")
        return jsonify({'error': str(e)}), 500

def get_pesticide_recommendations(crop, pest, severity):
    """
    Get pesticide recommendations based on crop, pest, and severity.
    This is a simplified version - in production, this would use a trained model
    or database lookup.
    """
    # Base recommendations that can be customized based on severity
    base_recommendations = {
        'organic': {
            'name': 'Neem Oil',
            'type': 'Organic',
            'safetyLevel': 'High',
            'description': 'Natural pesticide effective against various pests.',
            'application': 'Mix 2-3 tablespoons per gallon of water and spray on affected areas.',
            'frequency': 'Apply every 7-14 days'
        },
        'natural': {
            'name': 'Pyrethrin',
            'type': 'Natural',
            'safetyLevel': 'Medium',
            'description': 'Derived from chrysanthemum flowers, effective against flying insects.',
            'application': 'Apply as directed on the label, typically 1-2 tablespoons per gallon of water.',
            'frequency': 'Apply every 5-7 days'
        },
        'synthetic': {
            'name': 'Imidacloprid',
            'type': 'Synthetic',
            'safetyLevel': 'Low',
            'description': 'Systemic insecticide effective against a wide range of pests.',
            'application': 'Follow manufacturer instructions for application rates.',
            'frequency': 'Apply as needed, not more than once every 14 days'
        }
    }

    # Adjust recommendations based on severity
    recommendations = []
    
    if severity == 'low':
        recommendations.append(base_recommendations['organic'])
    elif severity == 'medium':
        recommendations.append(base_recommendations['organic'])
        recommendations.append(base_recommendations['natural'])
    else:  # high severity
        recommendations.append(base_recommendations['organic'])
        recommendations.append(base_recommendations['natural'])
        recommendations.append(base_recommendations['synthetic'])

    # Add crop-specific notes
    for rec in recommendations:
        rec['cropSpecific'] = f"Safe for use on {crop}. Monitor plant response after first application."
        rec['pestSpecific'] = f"Effective against {pest} infestations."

    return recommendations

@app.route('/api/auth/google')
def google_login():
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": app.config['GOOGLE_CLIENT_ID'],
                    "client_secret": app.config['GOOGLE_CLIENT_SECRET'],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [app.config['GOOGLE_REDIRECT_URI']]
                }
            },
            scopes=SCOPES
        )
        flow.redirect_uri = app.config['GOOGLE_REDIRECT_URI']
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Google login error: {e}")
        return jsonify({'error': 'Failed to initiate Google login'}), 500

@app.route('/api/auth/google/callback')
def google_callback():
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": app.config['GOOGLE_CLIENT_ID'],
                    "client_secret": app.config['GOOGLE_CLIENT_SECRET'],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [app.config['GOOGLE_REDIRECT_URI']]
                }
            },
            scopes=SCOPES
        )
        flow.redirect_uri = app.config['GOOGLE_REDIRECT_URI']
        
        # Get authorization response
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Get user info
        service = build('oauth2', 'v2', credentials=credentials)
        user_info = service.userinfo().get().execute()
        
        # Check if user exists
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            # Create new user
            user = User(
                name=user_info['name'],
                email=user_info['email'],
                role='user'
            )
            db.session.add(user)
            db.session.commit()
        
        # Generate token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, app.config['SECRET_KEY'])
        
        # Redirect to frontend with token
        return redirect(f"http://localhost:3000/auth/callback?token={token}")
    except Exception as e:
        logger.error(f"Google callback error: {e}")
        return jsonify({'error': 'Failed to complete Google login'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
