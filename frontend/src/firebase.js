import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';
// import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: 'AIzaSyDJKsz7yiqJWDgy5v84zcNXOHiklzVVOZ0',
  authDomain: 'financial-tracker-27def.firebaseapp.com',
  projectId: 'financial-tracker-27def',
  storageBucket: 'financial-tracker-27def.firebasestorage.app',
  messagingSenderId: '682465777723',
  appId: '1:682465777723:web:806622106a3f3698ea241e',
  measurementId: 'G-48SZQRYJBZ',
};

const app = initializeApp(firebaseConfig);

const db = getFirestore(app);
// const auth = getAuth(app);

export { db };
// export { auth };
