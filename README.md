## imageO – AI-based Milk Adulterant Detector

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

imageO is a Flask web app that detects edible-oil adulteration in milk images. It removes background using U^2-Net, enhances the image, and classifies it with a TensorFlow model. Authentication is handled via Firebase.

### Key features
- Background removal with U^2-Net (ONNX via `rembg`)
- Image enhancement pipeline (crop, white flatten, tint/gamma, CLAHE)
- Binary classification: `Milk` vs `Milk+Oil`
- Firebase client auth; secure Flask server session
- Health checks and structured logging

## Project structure
```
app/
  __init__.py              # App factory; loads config, logging, models, firebase
  config.py                # Constants and Flask settings
  auth/
    decorators.py         # `login_required`
    routes.py             # /auth/login, /auth/logout, /auth/sessionLogin
  main/
    routes.py             # / (protected), /predict, /health
  models/
    models.py             # Initialize U^2-Net session and TF model from HF Hub
  services/
    firebase_service.py   # Initialize firebase_admin from base64 creds
    image_processing.py   # Preprocessing pipeline
    prediction.py         # Model inference, returns predicted class + cropped image
  utils/
    logging_config.py     # Rotating file + console logging
    validators.py         # Base64 image validation
templates/
  index.html, login.html, signup.html
static/
  css/style.css, js/*.js, images/*.txt (base64 assets)
run.py                    # Entrypoint (uses app factory)
Dockerfile                # Gunicorn image (port 7860)
requirements.txt          # Pinned dependencies
```

## How it works
1) Frontend (in `templates/index.html` and `static/js/script.js`)
- Captures camera frame or uploads image, sends base64 to `/predict`.
- Displays predicted class and cropped image returned by the API.

2) API (`app/main/routes.py`)
- `/predict` (POST, auth required) validates JSON, runs preprocessing + inference.
- Returns `{ predicted_class, cropped_image }`.
- `/health` checks model/session availability.

3) Preprocessing (`app/services/image_processing.py`)
- Remove background (U^2-Net via `rembg` session in app config)
- Crop foreground by alpha mask
- Flatten on white, correct blue tint, gamma correction, CLAHE
- Resize to 224x224 and return a `PIL.Image`

4) Models (`app/models/models.py`)
- U^2-Net ONNX loaded through `rembg.session_factory.new_session()`.
- Milk classifier loaded from Hugging Face Hub (`keras` model).

5) Auth (`app/auth/routes.py` + frontend `login.js`/`register.js`)
- Client signs in with Firebase Web SDK, obtains `idToken`.
- Sends `idToken` to `/auth/sessionLogin` to create Flask session.
- `@login_required` protects main routes. `/auth/logout` clears session.

Note: `/auth/signup` is currently disabled on the server and returns 403; use Firebase client flows.

## Requirements
- Python 3.12+
- A Firebase project (Web app) for client auth
- Hugging Face account/token (optional but recommended for faster U^2-Net download)

## Environment variables
- `FIREBASE_CREDS` (required): Base64-encoded Firebase service account JSON used by `firebase_admin`.
- `SECRET_KEY` (optional): Flask secret key; defaults to random if unset.
- `FLASK_ENV` (optional): `production` or `development`. Affects cookie security flags.
- `PORT` (optional): Defaults to `7860`.
- `HF_TOKEN` (optional): Hugging Face token to accelerate model downloads.

Hugging Face repos used (see `app/config.py`):
- Classification: `iamSubha16/milk_adulterant_detector_model_v7` → `milk_adulterant_detector_model_v7.keras`
- Background removal: `iamSubha16/background_removal_model` → `u2net.onnx`

### Create FIREBASE_CREDS (Windows PowerShell)
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("path\to\firebase-credentials.json"))
```
Then set it in PowerShell for a session:
```powershell
$env:FIREBASE_CREDS = "<base64-string>"
$env:HF_TOKEN = "<optional-hf-token>"
```

You can also use a `.env` file in the project root. `python-dotenv` is loaded by model and firebase initializers.

Example `.env`:
```env
FIREBASE_CREDS=base64-of-service-account-json
HF_TOKEN=hf_xxx
SECRET_KEY=change-me
FLASK_ENV=production
```

## Run locally
```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1   # PowerShell on Windows
pip install --upgrade pip
pip install -r requirements.txt
setx FIREBASE_CREDS "<base64>"   # Or use $env:FIREBASE_CREDS for current shell
setx HF_TOKEN "<optional>"
python run.py
```

App starts on `http://localhost:7860`.

## Docker
The provided `Dockerfile` runs the app with Gunicorn.
```bash
docker build -t imageo .
docker run -p 7860:7860 -e FIREBASE_CREDS="<base64>" -e HF_TOKEN="<token>" imageo
```

## Endpoints
- `GET /auth/login` – Login page (Firebase client auth)
- `POST /auth/sessionLogin` – Exchanges Firebase `idToken` for Flask session
- `GET /auth/logout` – Clears session
- `GET /` – Home (requires session)
- `POST /predict` – JSON `{ image: "data:image/jpeg;base64,..." }`
- `GET /health` – Health and model readiness

Example request
```bash
curl -X POST http://localhost:7860/predict \
  -H "Content-Type: application/json" \
  -b "session=<your-session-cookie>" \
  -d '{"image": "data:image/jpeg;base64,/9j/..."}'
```

## Operational details
- Max upload size: 16 MB (`MAX_CONTENT_LENGTH`)
- Allowed image types: `image/jpeg`, `image/jpg`, `image/png`, `image/webp`
- Logs: `logs/milk_detector.log` (rotating) + console
- Error handlers: 400/401/403/404/413/500 with JSON responses

## License
MIT – see `LICENSE`.

## Acknowledgments
- `rembg` / U^2-Net for background removal
- TensorFlow/Keras for classification
- Firebase for authentication
