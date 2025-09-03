import numpy as np
import cv2
from PIL import Image
from io import BytesIO
from rembg import remove
from flask import current_app

def remove_background(image):
    try:
        input_img = image.convert("RGBA")
        u2net_session = current_app.config['U2NET_SESSION']
        no_bg = remove(input_img, session=u2net_session, safe_mode=True)
        return Image.open(BytesIO(no_bg)).convert("RGBA") if isinstance(no_bg, bytes) else no_bg
    except Exception as e:
        current_app.logger.error(f"Background removal failed: {str(e)}")
        raise

def crop_foreground(img_rgba):
    try:
        img_np = np.array(img_rgba)
        alpha = img_np[:, :, 3]
        mask = alpha > 0
        coords = np.argwhere(mask)
        if coords.size == 0:
            current_app.logger.warning("No foreground detected in image")
            return img_rgba
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        return img_rgba.crop((x0, y0, x1, y1))
    except Exception as e:
        current_app.logger.error(f"Foreground cropping failed: {str(e)}")
        return img_rgba

def flatten_on_white(img_rgba):
    try:
        img_rgba = img_rgba.convert("RGBA")
        background = Image.new("RGBA", img_rgba.size, (255, 255, 255, 255))
        composited = Image.alpha_composite(background, img_rgba)
        return composited.convert("RGB")
    except Exception as e:
        current_app.logger.error(f"Image flattening failed: {str(e)}")
        raise

def correct_blue_tint(img_rgb):
    try:
        hsv = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2HSV)
        hsv[..., 0] = (hsv[..., 0] + 10) % 180
        hsv[..., 1] = np.clip(hsv[..., 1] * 1.2, 0, 255)
        corrected = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        return Image.fromarray(corrected)
    except Exception as e:
        current_app.logger.error(f"Blue tint correction failed: {str(e)}")
        return img_rgb

def gamma_correction(img_rgb, gamma=1.1):
    try:
        img_np = np.array(img_rgb) / 255.0
        img_np = np.power(img_np, gamma)
        corrected = (img_np * 255).astype(np.uint8)
        return Image.fromarray(corrected)
    except Exception as e:
        current_app.logger.error(f"Gamma correction failed: {str(e)}")
        return img_rgb

def adaptive_histogram(img_rgb):
    try:
        lab = cv2.cvtColor(np.array(img_rgb), cv2.COLOR_RGB2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[..., 0] = clahe.apply(lab[..., 0])
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        return Image.fromarray(enhanced)
    except Exception as e:
        current_app.logger.error(f"Adaptive histogram failed: {str(e)}")
        return img_rgb

def preprocess_image_from_base64(base64_str, output_size=(224, 224)):
    try:
        from app.utils.validators import validate_base64_image
        
        # Validate input
        is_valid, error_msg = validate_base64_image(base64_str)
        if not is_valid:
            raise ValueError(error_msg)
        
        # Decode and load image
        import base64
        image_data = base64.b64decode(base64_str.split(',')[-1])
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        
        # Image processing pipeline
        no_bg = remove_background(image)
        cropped = crop_foreground(no_bg)
        flattened = flatten_on_white(cropped)
        color_corrected = correct_blue_tint(flattened)
        gamma_corrected = gamma_correction(color_corrected)
        contrast_adjusted = adaptive_histogram(gamma_corrected)
        resized = contrast_adjusted.resize(output_size, Image.Resampling.LANCZOS)
        
        return resized
        
    except Exception as e:
        current_app.logger.error(f"Image preprocessing failed: {str(e)}")
        raise