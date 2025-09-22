// // Import Firebase modules
// import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
// import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

// // Your Firebase project configuration
// const firebaseConfig = {
//   apiKey: "AIzaSyADwHA7HaZwq1SgAHA3CdRV9EErLQnCyis",
//   authDomain: "imageo-3ba1a.firebaseapp.com",
//   projectId: "imageo-3ba1a",
//   storageBucket: "imageo-3ba1a.appspot.com",
//   messagingSenderId: "51178781903",
//   appId: "1:51178781903:web:59a01bb42ddc5c7002cbba",
//   measurementId: "G-GV1E9WWYLF"
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);
// const auth = getAuth(app);

// // Wait for DOM to load
// document.addEventListener('DOMContentLoaded', () => {
//   const loginBtn = document.getElementById('email-login'); // Your login button
//   const googleBtn = document.getElementById('google-login'); // Your Google login button

//   if (loginBtn) {
//     loginBtn.addEventListener('click', async (e) => {
//       e.preventDefault();

//       const email = document.querySelector('input[type="email"]').value.trim();
//       const password = document.querySelector('input[type="password"]').value.trim();

//       try {
//         const userCredential = await signInWithEmailAndPassword(auth, email, password);
//         const user = userCredential.user;
//         const idToken = await user.getIdToken();

//         const response = await fetch('auth/sessionLogin', {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({ idToken })
//         });

//         if (!response.ok) throw new Error('Session login failed');

//         showToast("Login successful!", true);
//         sessionStorage.setItem('toastMessage', 'Login successful!');
//         sessionStorage.setItem('toastSuccess', 'true'); 
//         window.location.href = "/"; // Redirect to homepage

//       } catch (error) {
//         console.error("Login error:", error);
//         showToast("Login failed: " + error.message, false);
//       }
//     });
//   }

//   if (googleBtn) {
//     googleBtn.addEventListener('click', async () => {
//       const provider = new GoogleAuthProvider();
//       try {
//         const result = await signInWithPopup(auth, provider);
//         const user = result.user;
//         const idToken = await user.getIdToken();

//         const response = await fetch('auth/sessionLogin', {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({ idToken })
//         });

//         if (!response.ok) throw new Error('Session login failed');

//         showToast("Google Login successful!", true);
//         sessionStorage.setItem('toastMessage', 'Google Login successful!');
//         sessionStorage.setItem('toastSuccess', 'true');  // or 'false' for error
//         window.location.href = "/";

//       } catch (err) {
//         console.error("Google login error:", err);
//         showToast("Google Login failed: " + err.message, false);
//       }
//     });
//   }
// });

// // Show toast notification
// function showToast(message, isSuccess) {
//   const toast = document.getElementById('toast');

//   // Update the toast message
//   toast.textContent = message;

//   // Set toast styling
//   if (isSuccess) {
//     toast.classList.remove('bg-red-500');
//     toast.classList.add('bg-green-500', 'text-white');
//   } else {
//     toast.classList.remove('bg-green-500');
//     toast.classList.add('bg-red-500', 'text-white');
//   }

//   // Show the toast
//   toast.classList.remove('hidden');

//   // Automatically hide the toast after 3 seconds
//   setTimeout(() => {
//     toast.classList.add('hidden');
//   }, 3000);
// }


// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/11.8.1/firebase-auth.js";

// Your Firebase project configuration
const firebaseConfig = {
  apiKey: "AIzaSyADwHA7HaZwq1SgAHA3CdRV9EErLQnCyis",
  authDomain: "imageo-3ba1a.firebaseapp.com",
  projectId: "imageo-3ba1a",
  storageBucket: "imageo-3ba1a.appspot.com",
  messagingSenderId: "51178781903",
  appId: "1:51178781903:web:59a01bb42ddc5c7002cbba",
  measurementId: "G-GV1E9WWYLF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('email-login'); // Email login button
  const googleBtn = document.getElementById('google-login'); // Google login button

  // Email + Password login
  if (loginBtn) {
    loginBtn.addEventListener('click', async (e) => {
      e.preventDefault();

      const email = document.querySelector('input[type="email"]').value.trim();
      const password = document.querySelector('input[type="password"]').value.trim();

      try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        const idToken = await user.getIdToken();

        const response = await fetch('/auth/sessionLogin', {   // ✅ Correct absolute path
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ idToken })
        });

        if (!response.ok) throw new Error('Session login failed');

        showToast("Login successful!", true);
        sessionStorage.setItem('toastMessage', 'Login successful!');
        sessionStorage.setItem('toastSuccess', 'true'); 
        window.location.href = "/"; // Redirect to homepage

      } catch (error) {
        console.error("Login error:", error);
        showToast("Login failed: " + error.message, false);
      }
    });
  }

  // Google login
  if (googleBtn) {
    googleBtn.addEventListener('click', async () => {
      const provider = new GoogleAuthProvider();

      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const idToken = await user.getIdToken();

        const response = await fetch('/auth/sessionLogin', {  // ✅ Correct absolute path
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ idToken })
        });

        if (!response.ok) throw new Error('Session login failed');

        showToast("Google Login successful!", true);
        sessionStorage.setItem('toastMessage', 'Google Login successful!');
        sessionStorage.setItem('toastSuccess', 'true');
        window.location.href = "/"; // Redirect to homepage

      } catch (err) {
        console.error("Google login error:", err);
        showToast("Google Login failed: " + err.message, false);
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
