import os
import shutil
import tensorflow as tf
from tensorflow.keras.applications.xception import preprocess_input
from rembg.session_factory import new_session
from huggingface_hub import hf_hub_download
import onnxruntime as ort
import os
from dotenv import load_dotenv

load_dotenv() 

# token = os.getenv("HF_TOKEN")

def initialize_models(app):
    try:

        # --------------------------------------------  BACKGROUND REMOVAL MODEL   --------------------------------------------

        app.logger.info("Initializing u2net session...")

        # Cache directory for the model
        cache_dir = os.path.expanduser("~/.u2net")
        os.makedirs(cache_dir, exist_ok=True)
        cached_model_path = os.path.join(cache_dir, "u2net.onnx")

        hf_token = os.environ.get("HF_TOKEN")
        try:
            # Try fetching the model from Hugging Face
            hf_model_path = hf_hub_download(
                repo_id=app.config['BG_REMOVAL_MODEL_REPO_ID'],
                filename=app.config['BG_REMOVAL_MODEL_NAME'],
                token=hf_token
            )
            shutil.copyfile(hf_model_path, cached_model_path)
            app.logger.info(f"u2net model fetched from Hugging Face and cached at: {cached_model_path}")
            
            # Load ONNX session directly
            u2net_session = new_session(model_path=cached_model_path)

            app.logger.info("u2net session initialized with HF cached model")

        except Exception as e:
            # HF download failed, fallback to default automatic download
            app.logger.warning(f"Failed to fetch u2net from Hugging Face: {str(e)}")
            app.logger.info("Using default u2net model (will download automatically, slower startup)")
            u2net_session = new_session()  # Default download inside new_session
            app.logger.info("u2net session initialized with default model")
        
        # -----------------------------------------------  CLASSIFICATION MODEL   -----------------------------------------------

        app.logger.info("Loading milk adulterant detection model...")
        # repo_id = "iamSubha16/milk_adulterant_detector_model_v7"
        # filename = "milk_adulterant_detector_model_v7.keras"

        token = os.environ.get("HF_TOKEN")
        model_path = hf_hub_download(
            repo_id=app.config['CLASSIFICATION_MODEL_REPO_ID'],
            filename=app.config['CLASSIFICATION_MODEL_NAME'],
            token=token
        )

        model = tf.keras.models.load_model(
            model_path,
            custom_objects={'preprocess_input': preprocess_input},
            safe_mode=False
        )

        app.logger.info("Milk detection model loaded successfully")
        
        return u2net_session, model
        
    except Exception as e:
        app.logger.error(f"Failed to initialize models: {str(e)}")
        raise