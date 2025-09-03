// Import Firebase SDK modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

// Your Firebase config object
const firebaseConfig = {
  apiKey: "AIzaSyADwHA7HaZwq1SgAHA3CdRV9EErLQnCyis",
  authDomain: "imageo-3ba1a.firebaseapp.com",
  projectId: "imageo-3ba1a",
  storageBucket: "imageo-3ba1a.appspot.com",
  messagingSenderId: "51178781903",
  appId: "1:51178781903:web:59a01bb42ddc5c7002cbba",
  measurementId: "G-GV1E9WWYLF"
};

// Initialize Firebase app and auth
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Signup function
async function signup(email, password) {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;
    showToast("Signup successful! Welcome " + user.email, true);
    window.location.href = "/login";  // redirect after signup
  } catch (error) {
    showToast("Signup failed: " + err.message, false);
    console.error("Signup error", error);
  }
}

// Wait for DOM content to load
document.addEventListener("DOMContentLoaded", () => {
  // Email/password signup form listener
  const signupForm = document.getElementById("signup-form");
  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = signupForm.email.value.trim();
      const password = signupForm.password.value.trim();
      signup(email, password);
    });
  }

  // Google signup/login button listener
  const googleBtn = document.getElementById('google-signup');
  if (googleBtn) {
    googleBtn.addEventListener('click', async () => {
      const provider = new GoogleAuthProvider();
      try {
        const result = await signInWithPopup(auth, provider);
        const token = await result.user.getIdToken();

        await fetch('/sessionLogin', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ idToken: token })
        });

        showToast("Google Signup successful!", true);
        window.location.href = "/";
      } catch (err) {
        showToast("Google Signup failed: " + err.message, false);
        console.error(err);
      }
    });
  }
});

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