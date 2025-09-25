# imageO - AI-Powered Milk Adulterant Detection System

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1+-green.svg)](https://flask.palletsprojects.com)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19+-orange.svg)](https://tensorflow.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

imageO is an intelligent web application that leverages computer vision and machine learning to detect edible oil adulteration in milk samples through image analysis. The system combines advanced background removal techniques with deep learning classification to provide accurate, real-time detection of milk quality.

### Core Capabilities

- **Automated Background Removal**: Utilizes U²-Net neural network for precise subject isolation
- **Advanced Image Processing**: Multi-stage enhancement pipeline including cropping, color correction, and contrast optimization
- **AI-Powered Classification**: Binary classification system distinguishing between pure milk and oil-adulterated samples
- **Secure Authentication**: Firebase-based user authentication with session management
- **Production Ready**: Comprehensive logging, health monitoring, and error handling

## Architecture

### System Components

```
imageO/
├── app/
│   ├── __init__.py              # Application factory and configuration
│   ├── config.py                # Environment and Flask configurations
│   ├── auth/                    # Authentication module
│   │   ├── decorators.py        # Login required decorators
│   │   └── routes.py            # Authentication endpoints
│   ├── main/                    # Core application routes
│   │   └── routes.py            # Main endpoints and prediction API
│   ├── models/                  # Model initialization and management
│   │   └── models.py            # U²-Net and classification model setup
│   ├── services/                # Business logic services
│   │   ├── firebase_service.py  # Firebase Admin SDK integration
│   │   ├── image_processing.py  # Image preprocessing pipeline
│   │   └── prediction.py        # ML inference service
│   └── utils/                   # Utility modules
│       ├── logging_config.py    # Structured logging configuration
│       └── validators.py        # Input validation utilities
├── templates/                   # Jinja2 HTML templates
├── static/                      # Static assets (CSS, JavaScript, images)
├── run.py                       # Application entry point
├── Dockerfile                   # Container configuration
└── requirements.txt             # Python dependencies
```

## Technical Implementation

### Image Processing Pipeline

1. **Background Removal**: U²-Net model removes background elements for focused analysis
2. **Foreground Extraction**: Alpha mask-based cropping to isolate the milk sample
3. **Color Correction**: White balance adjustment and blue tint correction
4. **Enhancement**: Gamma correction and CLAHE (Contrast Limited Adaptive Histogram Equalization)
5. **Standardization**: Resize to 224×224 pixels for model input

### Machine Learning Models

- **Background Removal**: U²-Net ONNX model via `rembg` library
- **Classification**: Custom TensorFlow/Keras model trained for milk adulteration detection
- **Model Repository**: Hosted on Hugging Face Hub for reliable access and versioning

### Authentication Flow

1. Client authenticates using Firebase Web SDK
2. Firebase ID token exchanged for server-side session
3. Protected routes validate session before processing requests
4. Secure logout clears both client and server sessions

## Installation & Setup

### Prerequisites

- Python 3.12 or higher
- Firebase project with Web App configuration
- Hugging Face account (optional, for faster model downloads)

### Environment Configuration

Create a `.env` file in the project root:

```env
FIREBASE_CREDS=<base64-encoded-firebase-service-account-json>
HF_TOKEN=<hugging-face-token>
SECRET_KEY=<flask-secret-key>
FLASK_ENV=production
PORT=7860
```

#### Generate Firebase Credentials

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("path\to\firebase-credentials.json"))
```

**Linux/macOS:**
```bash
base64 -i path/to/firebase-credentials.json
```

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/imageO.git
   cd imageO
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   export FIREBASE_CREDS="<base64-encoded-credentials>"
   export HF_TOKEN="<your-huggingface-token>"
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:7860`

### Docker Deployment

```bash
# Build the image
docker build -t imageo .

# Run the container
docker run -p 7860:7860 \
  -e FIREBASE_CREDS="<base64-credentials>" \
  -e HF_TOKEN="<huggingface-token>" \
  imageo
```

## API Reference

### Authentication Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/login` | GET | Login page with Firebase authentication |
| `/auth/sessionLogin` | POST | Exchange Firebase ID token for session |
| `/auth/logout` | GET | Clear user session |

### Application Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/` | GET | ✓ | Main application interface |
| `/predict` | POST | ✓ | Image analysis and classification |
| `/health` | GET | ✗ | System health and model status |

### Prediction API

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEA..."
}
```

**Response:**
```json
{
  "predicted_class": "Milk",
  "confidence": 0.95,
  "cropped_image": "data:image/jpeg;base64,..."
}
```

**Example Usage:**
```bash
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<session-cookie>" \
  -d '{"image": "data:image/jpeg;base64,<base64-image>"}'
```

## Configuration

### Application Limits

- **Maximum Upload Size**: 16 MB
- **Supported Image Formats**: JPEG, JPG, PNG, WebP
- **Image Processing Timeout**: 30 seconds
- **Session Duration**: 24 hours

### Model Configuration

- **U²-Net Model**: `iamSubha16/background_removal_model/u2net.onnx`
- **Classification Model**: `iamSubha16/milk_adulterant_detector_model_v7/milk_adulterant_detector_model_v7.keras`

## Monitoring & Logging

The application includes comprehensive logging and monitoring:

- **Structured Logging**: JSON-formatted logs with timestamps and severity levels
- **Log Rotation**: Automatic log file rotation to manage disk usage
- **Health Checks**: Real-time monitoring of model availability and system status
- **Error Tracking**: Detailed error reporting with stack traces

Logs are written to `logs/milk_detector.log` and console output.

## Security Features

- **Session-Based Authentication**: Secure server-side session management
- **Input Validation**: Comprehensive validation of image uploads and requests
- **CSRF Protection**: Built-in Flask security measures
- **Environment Isolation**: Sensitive credentials stored as environment variables
- **Production Security**: Security headers and HTTPS-ready configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [U²-Net](https://github.com/xuebinqin/U-2-Net) for background removal capabilities
- [rembg](https://github.com/danielgatis/rembg) for ONNX model integration
- [TensorFlow](https://tensorflow.org) for machine learning framework
- [Firebase](https://firebase.google.com) for authentication services
- [Hugging Face](https://huggingface.co) for model hosting and distribution

## Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation in the `docs/` directory


