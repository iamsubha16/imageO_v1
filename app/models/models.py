import os
import shutil
import tensorflow as tf
from tensorflow.keras.applications.xception import preprocess_input
from rembg.session_factory import new_session

def initialize_models(app):
    try:
        app.logger.info("Initializing u2net session...")

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_dir = os.path.join(base_dir, "models")
        local_model_path = os.path.join(model_dir, "u2net.onnx")

        cache_dir = os.path.expanduser("~/.u2net")
        os.makedirs(cache_dir, exist_ok=True)
        cached_model_path = os.path.join(cache_dir, "u2net.onnx")
        
        # Use local model if available
        if os.path.isfile(local_model_path):
            app.logger.info(f"Found local u2net model at {local_model_path}")
            shutil.copyfile(local_model_path, cached_model_path)
            app.logger.info(f"Copied u2net model to cache: {cached_model_path}")
            u2net_session = new_session()
            app.logger.info("u2net session initialized with local cached model")
        else:
            # Debug info and fallback
            if os.path.exists(model_dir):
                files = os.listdir(model_dir)
                app.logger.error(f"u2net.onnx not found in models/ directory. Available files: {files}")
            else:
                app.logger.error(f"Models directory not found at {model_dir}")

            app.logger.warning("Using default u2net model (will download, slower startup)")
            u2net_session = new_session()
            app.logger.info("u2net session initialized with default model")
        
        app.logger.info("Loading milk adulterant detection model...")
        model = tf.keras.models.load_model(
            app.config['MODEL_PATH'],
            custom_objects={'preprocess_input': preprocess_input},
            safe_mode=False
        )
        app.logger.info("Milk detection model loaded successfully")
        
        return u2net_session, model
        
    except Exception as e:
        app.logger.error(f"Failed to initialize models: {str(e)}")
        raise