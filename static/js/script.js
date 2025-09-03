import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";

window.addEventListener('DOMContentLoaded', () => {
  const message = sessionStorage.getItem('toastMessage');
  const isSuccess = sessionStorage.getItem('toastSuccess') === 'true';

  if (message) {
    showToast(message, isSuccess);
    sessionStorage.removeItem('toastMessage');   
    sessionStorage.removeItem('toastSuccess');
  }
});

const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const predictionText = document.getElementById('predictionText');
const captureBtn = document.getElementById('captureBtn');
const uploadInput = document.getElementById('uploadInput');
const imagePreview = document.getElementById('imagePreview');
const switchCameraBtn = document.getElementById('switchCameraBtn');

let currentFacingMode = 'environment'; // Default to back camera
let currentStream = null;
let isCameraActive = false; // Track if camera is on

switchCameraBtn.disabled = true;

startCameraBtn.addEventListener('click', toggleCamera);
switchCameraBtn.addEventListener('click', switchCamera);

// On/Off function of camera
async function toggleCamera() {
  const cameraControlBtn = document.getElementById('startCameraBtn');
  const cameraControlIcon = document.getElementById('cameraControlIcon');
  const cameraControlText = document.getElementById('cameraControlText');

  if (!isCameraActive) {
    // Start camera
    await startCamera(currentFacingMode);
    isCameraActive = true;
    video.classList.add('active'); // <-- Fade-in effect
    cameraControlIcon.className = 'fas fa-stop text-xs'; // Change icon to stop
    cameraControlText.textContent = 'Stop Camera';
    switchCameraBtn.disabled = false; // Enable Switch Camera button
  } else {
    // Stop camera
    // stopCamera();
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
    }
    isCameraActive = false;
    video.srcObject = null;
    video.classList.remove('active'); // <-- Fade-out effect
    cameraControlIcon.className = 'fas fa-play text-xs';
    cameraControlText.textContent = 'Start Camera';
    switchCameraBtn.disabled = true; // Disable Switch Camera button when camera is stopped
    showToast('Camera stopped', true);
  }
}

// Start the camera with the given facing mode
async function startCamera(facingMode) {
  // Stop any existing video stream
  if (currentStream) {
    currentStream.getTracks().forEach(track => track.stop());
  }

  try {
    // Define constraints for video stream
    const constraints = {
      video: {
        facingMode: { ideal: facingMode },
        width: { ideal: 1280 },
        height: { ideal: 720 }
      }
    };

    // Access camera
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = stream;
    currentStream = stream;
    currentFacingMode = facingMode;

    video.classList.remove('hidden'); // Show video when camera starts
    showToast(`Camera started: ${facingMode === 'environment' ? 'back' : 'front'} camera`, true);
  } catch (err) {
    showToast('Camera access error: ' + err.message, false);
  }
}

// Stop the camera
function stopCamera() {
  const cameraControlBtn = document.getElementById('startCameraBtn');
  const cameraControlIcon = document.getElementById('cameraControlIcon');
  const cameraControlText = document.getElementById('cameraControlText');

  if (currentStream) {
    currentStream.getTracks().forEach(track => track.stop());
    currentStream = null;
  }

  video.srcObject = null;
  video.classList.add('hidden'); // Hide the video when stopped
  isCameraActive = false;
  
  cameraControlIcon.className = 'fas fa-play text-xs'; // Change icon back to play
  cameraControlText.textContent = 'Start Camera';
  showToast('Camera stopped', true);
}

// Initial camera load
document.addEventListener('DOMContentLoaded', function() {
  // Do not start the camera immediately
  if (uploadInput) {
    uploadInput.addEventListener('change', handleUpload);
  }
  
  const captureBtn = document.getElementById('captureBtn');
  if (captureBtn) {
    captureBtn.addEventListener('click', capture);
  }
});

// Switch camera between front and back
function switchCamera() {
  if (!isCameraActive) return;  // Prevent switching if camera is not active
  
  const newFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  startCamera(newFacingMode);
}

// Send image data to Flask for prediction and handle UI updates
async function sendPrediction(base64Image) {
  // Update image preview
  imagePreview.src = base64Image;
  imagePreview.style.display = 'block';

  // Disable capture button and show loading
  if (captureBtn) captureBtn.disabled = true;
  predictionText.textContent = 'Loading...';

  // Reset result styling
  const resultDiv = document.getElementById('predictionText');
  resultDiv.classList.remove(
    'border-green-500', 'border-red-500', 
    'text-green-600', 'dark:text-green-400', 
    'text-red-600', 'dark:text-red-400',
    'text-indigo-600', 'dark:text-indigo-400' // Remove all previous colors
  );

  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64Image })
    });

    const data = await res.json();

    if (data.error) {
      showToast('Prediction error: ' + data.error, false);
      // predictionText.textContent = `Error: ${data.error}`;
    } else {
      // predictionText.innerHTML = `Predicted Class: <strong>${data.predicted_class}</strong><br>Confidence: <strong>${data.confidence}%</strong>`;
      predictionText.innerHTML = `Predicted Class: <strong>${data.predicted_class}</strong>`;

      // Change the color based on the predicted class
      if (data.predicted_class === "Milk") {
        predictionText.classList.add('text-green-600', 'dark:text-green-400');  // Green color for Milk
      } else {
        predictionText.classList.add('text-red-600', 'dark:text-red-400');  // Red color for milk+oil
      }

      // Display cropped image
      const croppedImagePreview = document.getElementById('croppedImagePreview');
      croppedImagePreview.src = data.cropped_image;  // Set base64 string as the source
      croppedImagePreview.style.display = 'block';  // Make it visible

      showToast('Prediction complete', true);
    }
  } catch (err) {
    // predictionText.textContent = `Error: ${err.message}`;
    showToast('Connection error: ' + err.message, false);
  } finally {
    if (captureBtn) captureBtn.disabled = false;
  }
}

// Capture the current frame from the video and predict
function capture() {
  if (!currentStream) {
    showToast('Camera not available', false);
    return;
  }

  const context = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const base64Image = canvas.toDataURL('image/jpeg');

  sendPrediction(base64Image);
}

// Handle file uploads and predict
function handleUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  // Validate file type
  if (!file.type.match('image.*')) {
    showToast('Please select an image file', false);
    return;
  }

  // Validate file size (e.g., limit to 1MB)
  if (file.size > 4 * 1024 * 1024) {
    showToast('File size exceeds 4MB', false);
    return;
  }

  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      const context = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      context.drawImage(img, 0, 0);
      const base64Image = canvas.toDataURL('image/jpeg');

      sendPrediction(base64Image);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

// Show toast notification
function showToast(message, isSuccess) {
  const toast = document.getElementById('toast');

  // Update the toast message
  toast.textContent = message;

  // Set toast styling
  if (isSuccess) {
    toast.classList.remove('bg-red-500');
    toast.classList.add('bg-green-500', 'text-white');
  } else {
    toast.classList.remove('bg-green-500');
    toast.classList.add('bg-red-500', 'text-white');
  }

  // Show the toast
  toast.classList.remove('hidden');

  // Automatically hide the toast after 3 seconds
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 3000);
}

// Your Firebase config object
const firebaseConfig = {
  apiKey: "AIzaSyADwHA7HaZwq1SgAHA3CdRV9EErLQnCyis",
  authDomain: "imageo-3ba1a.firebaseapp.com",
  projectId: "imageo-3ba1a",
  storageBucket: "imageo-3ba1a.appspot.com",  // fixed typo here
  messagingSenderId: "51178781903",
  appId: "1:51178781903:web:59a01bb42ddc5c7002cbba",
  measurementId: "G-GV1E9WWYLF"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);

document.addEventListener('DOMContentLoaded', () => {
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      const auth = getAuth();
      try {
        await signOut(auth); // Sign out from Firebase

        // Then, clear Flask session by hitting /logout
        window.location.href = "/logout";
      } catch (error) {
        console.error("Logout failed:", error);
        alert("Logout failed: " + error.message);
      }
    });
  }
});