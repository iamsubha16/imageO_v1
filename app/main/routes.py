from flask import Blueprint, render_template, request, jsonify, session, current_app
from datetime import datetime
import traceback
import pytz
from app.auth.decorators import login_required
from app.services.prediction import predict_from_base64

main_bp = Blueprint('main', __name__)

local_tz = pytz.timezone("Asia/Kolkata")
local_time = datetime.now(local_tz)

# Read base64 images once at app startup
with open("static/images/favicon.txt", "r") as f:
    FAVICON_B64 = f.read().strip()  # Remove whitespace/newlines

with open("static/images/imageO.txt", "r") as f:
    IMAGEO_B64 = f.read().strip()  # Remove whitespace/newlines

with open("static/images/placeholder.txt", "r") as f:
    PLACEHOLDER_B64 = f.read().strip()  # Remove whitespace/newlines

@main_bp.route('/')
@login_required
def home():
    current_app.logger.info(f"Home page accessed by user: {session.get('email', 'Unknown')}")
    return render_template('index.html', 
                           favicon_b64=FAVICON_B64, 
                           imageo_b64=IMAGEO_B64, 
                           placeholder_b64=PLACEHOLDER_B64)

@main_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    user_email = session.get('email', 'Unknown')
    
    try:
        # Validate request
        if not request.is_json:
            current_app.logger.warning(f"Non-JSON request from {user_email}")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data or 'image' not in data:
            current_app.logger.warning(f"Invalid request data from {user_email}")
            return jsonify({'error': 'No image provided in the request.'}), 400

        current_app.logger.info(f"Prediction request from user: {user_email}")

        # Process prediction
        predicted_class, cropped_image = predict_from_base64(data['image'])
        
        current_app.logger.info(f"Prediction successful for {user_email}: {predicted_class}")
        
        return jsonify({
            'predicted_class': predicted_class,
            'cropped_image': cropped_image,
            'status': 'success'
        }), 200

    except ValueError as e:
        current_app.logger.warning(f"Validation error for {user_email}: {str(e)}")
        return jsonify({'error': f'Validation error: {str(e)}'}), 400
    
    except Exception as e:
        current_app.logger.error(f"Prediction error for {user_email}: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500

@main_bp.route('/health')
def health_check():
    try:
        # Basic health checks
        status = {
            'status': 'healthy',
            'timestamp': datetime.now(local_tz).isoformat(),
            'version': '1.0.0'
        }
        
        # Check if models are loaded
        if not current_app.config.get('ML_MODEL'):
            status['status'] = 'unhealthy'
            status['error'] = 'ML model not loaded'
            return jsonify(status), 503
            
        if not current_app.config.get('U2NET_SESSION'):
            status['status'] = 'unhealthy'
            status['error'] = 'u2net session not initialized'
            return jsonify(status), 503
        
        return jsonify(status), 200
        
    except Exception as e:
        current_app.logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now(local_tz).isoformat()
        }), 503