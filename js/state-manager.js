// State Manager for BHU Exam Prep website using localStorage

export const StateManager = {
  // --- USER SESSION ---
  getCurrentUser() {
    let user = localStorage.getItem('bhu_user');
    if (!user) {
      const defaultUser = { name: 'Aryan Maurya', roll: '24220MAT051' };
      localStorage.setItem('bhu_user', JSON.stringify(defaultUser));
      return defaultUser;
    }
    return JSON.parse(user);
  },

  setCurrentUser(user) {
    if (user) {
      localStorage.setItem('bhu_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('bhu_user');
    }
  },

  logout() {
    localStorage.removeItem('bhu_user');
    localStorage.removeItem('bhu_active_exam');
    window.location.href = 'index.html';
  },

  // --- ACTIVE EXAM STATE ---
  getActiveExam() {
    const exam = localStorage.getItem('bhu_active_exam');
    return exam ? JSON.parse(exam) : null;
  },

  setActiveExam(examState) {
    if (examState) {
      localStorage.setItem('bhu_active_exam', JSON.stringify(examState));
    } else {
      localStorage.removeItem('bhu_active_exam');
    }
  },

  initializeExam(examId, totalQuestions, durationMinutes, type = 'mcq', questionsList = null, allQuestions = null) {
    const examState = {
      examId,
      timeRemaining: durationMinutes * 60, // in seconds
      currentQuestionIndex: 0,
      answers: {}, // questionId -> selectedOption or { evaluated, marks, suggestions }
      flagged: {}, // questionId -> boolean
      totalQuestions: questionsList ? questionsList.length : totalQuestions,
      startedAt: Date.now(),
      type,
      selectedQuestions: questionsList,
      allQuestions: allQuestions // Full pool for "Show All Questions" feature
    };
    this.setActiveExam(examState);
    return examState;
  },

  updateActiveExam(fields) {
    const current = this.getActiveExam();
    if (current) {
      const updated = { ...current, ...fields };
      this.setActiveExam(updated);
      return updated;
    }
    return null;
  },

  // --- ATTEMPTS HISTORY ---
  getAttempts() {
    const attempts = localStorage.getItem('bhu_attempts');
    return attempts ? JSON.parse(attempts) : [];
  },

  saveAttempt(attempt) {
    const attempts = this.getAttempts();
    attempts.push(attempt);
    localStorage.setItem('bhu_attempts', JSON.stringify(attempts));
  },

  getExamStats() {
    const attempts = this.getAttempts();
    if (attempts.length === 0) {
      return {
        averageScore: 0,
        examsPassed: 0,
        totalMinutes: 0
      };
    }

    const totalScore = attempts.reduce((sum, a) => sum + a.score, 0);
    const averageScore = Math.round((totalScore / attempts.length) * 10) / 10;
    const examsPassed = attempts.filter(a => a.score >= 50).length;
    
    // Total minutes spent
    const totalMinutes = attempts.reduce((sum, a) => {
      const durationSeconds = a.durationSpent || 0;
      return sum + Math.round(durationSeconds / 60);
    }, 0);

    return {
      averageScore,
      examsPassed,
      totalMinutes
    };
  },

  // --- ENV FILE LOADER ---
  async loadEnv() {
    try {
      const res = await fetch('/api/config');
      if (res.ok) {
        return await res.json();
      }
      
      const resEnv = await fetch('.env');
      if (!resEnv.ok) throw new Error('Not found');
      const text = await resEnv.text();
      const env = {};
      text.split('\n').forEach(line => {
        const parts = line.split('=');
        if (parts.length >= 2) {
          const key = parts[0].trim();
          const val = parts.slice(1).join('=').trim();
          env[key] = val.replace(/(^["']|["']$)/g, ''); // remove quotes
        }
      });
      return env;
    } catch (e) {
      console.warn("Could not load config:", e);
      return {};
    }
  }
};

// --- INDEXEDDB STORAGE FOR THEORY IMAGES ---
const DB_NAME = 'BHUExamTheoryDB';
const STORE_NAME = 'answers';

export const TheoryStorage = {
  dbPromise: null,
  getDB() {
    if (!this.dbPromise) {
      this.dbPromise = new Promise((resolve, reject) => {
        const req = indexedDB.open(DB_NAME, 1);
        req.onupgradeneeded = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains(STORE_NAME)) {
            db.createObjectStore(STORE_NAME);
          }
        };
        req.onsuccess = (e) => resolve(e.target.result);
        req.onerror = (e) => reject(e.target.error);
      });
    }
    return this.dbPromise;
  },
  async saveImage(key, base64) {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      const req = store.put(base64, key);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  },
  async getImage(key) {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const req = store.get(key);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
  },
  async deleteImage(key) {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      const req = store.delete(key);
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  },
  async clearAll() {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE_NAME, 'readwrite');
      const store = tx.objectStore(STORE_NAME);
      const req = store.clear();
      req.onsuccess = () => resolve();
      req.onerror = () => reject(req.error);
    });
  }
};
