import time
import base64
import tensorflow as tf
import traceback
from io import BytesIO
from flask import current_app
from app.services.image_processing import preprocess_image_from_base64

def predict_from_base64(base64_str):
    try:
        start_time = time.time()
        
        # Preprocess the image
        processed_img = preprocess_image_from_base64(base64_str)
        preprocessing_time = time.time() - start_time
        
        # Prepare for prediction
        prediction_start = time.time()
        img_array = tf.keras.preprocessing.image.img_to_array(processed_img)
        img_array = tf.expand_dims(img_array, 0)

        # Perform prediction
        model = current_app.config['ML_MODEL']
        prediction = model.predict(img_array, verbose=0)[0][0]
        class_index = 1 if prediction > 0.5 else 0
        predicted_class = current_app.config['CLASS_NAMES'][class_index]
        
        prediction_time = time.time() - prediction_start

        # Encode processed image back to base64
        encoding_start = time.time()
        buffered = BytesIO()
        processed_img.save(buffered, format="JPEG", quality=85, optimize=True)
        cropped_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        cropped_base64 = f"data:image/jpeg;base64,{cropped_base64}"
        encoding_time = time.time() - encoding_start
        
        total_time = time.time() - start_time
        
        # Log performance metrics
        current_app.logger.info(
            f"Prediction completed - Class: {predicted_class} - "
            f"Preprocessing: {preprocessing_time:.3f}s, "
            f"Prediction: {prediction_time:.3f}s, "
            f"Encoding: {encoding_time:.3f}s, "
            f"Total: {total_time:.3f}s"
        )

        return predicted_class, cropped_base64

    except Exception as e:
        current_app.logger.error(f"Prediction failed: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        raise