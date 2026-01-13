import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// ============= EMOTION-BASED SPEAKING =============

export const emotionAPI = {
  generateSentence: () => axios.get(`${API_BASE}/emotion/generate-sentence`),
  detectEmotion: (text) => axios.post(`${API_BASE}/emotion/detect`, { text }),
  calculateTime: (sentence) => axios.post(`${API_BASE}/emotion/calculate-time`, { sentence }),
  provideFeedback: (actualTime, allowedTime) => 
    axios.post(`${API_BASE}/emotion/feedback`, { actual_time: actualTime, allowed_time: allowedTime }),
};

// ============= FLUENCY PRACTICE =============

export const fluencyAPI = {
  getSentences: (num) => axios.get(`${API_BASE}/fluency/get-sentences?num=${num}`),
  calculateTime: (sentence) => axios.post(`${API_BASE}/fluency/calculate-time`, { sentence }),
  analyzeAccuracy: (correctSentence, spokenText) =>
    axios.post(`${API_BASE}/fluency/analyze-accuracy`, { correct_sentence: correctSentence, spoken_text: spokenText }),
};

// ============= SENTENCE SPEECH CHALLENGE =============

export const sentenceAPI = {
  fetchSummary: (topic) => axios.get(`${API_BASE}/sentence/fetch-summary?topic=${topic}`),
  extractKeywords: (text) => axios.post(`${API_BASE}/sentence/extract-keywords`, { text }),
  calculateSimilarity: (userSpeech, referenceText) =>
    axios.post(`${API_BASE}/sentence/calculate-similarity`, { user_speech: userSpeech, reference_text: referenceText }),
  generateFeedback: (userSpeech, referenceText) =>
    axios.post(`${API_BASE}/sentence/generate-feedback`, { user_speech: userSpeech, reference_text: referenceText }),
};

// ============= SYNONYM QUIZ =============

export const synonymAPI = {
  getQuestions: (num) => axios.get(`${API_BASE}/synonym/get-questions?num=${num}`),
  checkRelevance: (userAnswer, correctAnswer) =>
    axios.post(`${API_BASE}/synonym/check-relevance`, { user_answer: userAnswer, correct_answer: correctAnswer }),
};
