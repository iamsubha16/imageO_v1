import base64
from PIL import Image
from io import BytesIO
from flask import current_app

def validate_base64_image(base64_str):
    try:
        if not base64_str or not isinstance(base64_str, str):
            return False, "Invalid base64 string"
        
        if not base64_str.startswith('data:image/'):
            return False, "Invalid image format"
        
        # Extract MIME type
        mime_type = base64_str.split(',')[0].split(':')[1].split(';')[0]
        if mime_type not in current_app.config['ALLOWED_IMAGE_TYPES']:
            return False, f"Unsupported image type: {mime_type}"
        
        # Decode base64 data
        image_data = base64.b64decode(base64_str.split(',')[-1])
        if len(image_data) == 0:
            return False, "Empty image data"
        
        # Validate with PIL
        Image.open(BytesIO(image_data))
        return True, None
        
    except Exception as e:
        return False, f"Invalid image data: {str(e)}"