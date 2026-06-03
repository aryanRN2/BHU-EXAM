// State Manager for BHU Exam Prep website using localStorage

export const StateManager = {
  // --- USER SESSION ---
  getCurrentUser() {
    const user = localStorage.getItem('bhu_user');
    return user ? JSON.parse(user) : null;
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

  initializeExam(examId, totalQuestions, durationMinutes) {
    const examState = {
      examId,
      timeRemaining: durationMinutes * 60, // in seconds
      currentQuestionIndex: 0,
      answers: {}, // questionId -> selectedOption (A, B, C, D)
      flagged: {}, // questionId -> boolean
      totalQuestions,
      startedAt: Date.now()
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
  }
};
