import os
from datetime import timedelta

class Config:
    # Set environment variables
    os.environ["XDG_CACHE_HOME"] = "/app/.cache"
    os.environ["POOCH_BASE_DIR"] = "/app/.u2net"
    os.environ["HOME"] = "/app"
    os.environ["NUMBA_DISABLE_CACHE"] = "1"
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    
    # Security settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # File upload limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Production settings
    PROPAGATE_EXCEPTIONS = True
    JSON_SORT_KEYS = False
    
    # Application constants
    CLASS_NAMES = ['Milk', 'Milk+Oil']
    ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}
    CLASSIFICATION_MODEL_REPO_ID = "iamSubha16/milk_adulterant_detector_model_v7"
    CLASSIFICATION_MODEL_NAME = "milk_adulterant_detector_model_v7.keras"
    BG_REMOVAL_MODEL_REPO_ID="iamSubha16/background_removal_model"
    BG_REMOVAL_MODEL_NAME="u2net.onnx"