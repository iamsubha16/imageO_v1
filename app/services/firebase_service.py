import os
import base64
import json
import firebase_admin
from firebase_admin import credentials

def initialize_firebase(app):
    try:
        firebase_creds_b64 = os.environ.get("FIREBASE_CREDS")
        if not firebase_creds_b64:
            raise ValueError("FIREBASE_CREDS environment variable not set")

        decoded = base64.b64decode(firebase_creds_b64)
        creds_dict = json.loads(decoded)
        
        app.logger.info("Firebase credentials decoded successfully")
        
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)
        app.logger.info("Firebase initialized successfully")
        
    except Exception as e:
        app.logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise