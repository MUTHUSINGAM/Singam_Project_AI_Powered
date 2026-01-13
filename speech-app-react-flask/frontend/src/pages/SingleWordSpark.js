import React, { useState, useEffect } from 'react';
import { synonymAPI } from '../services/api';
import { useSpeechRecognition } from '../services/speechRecognition';
import './Pages.css';

const SingleWordSpark = () => {
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [totalScore, setTotalScore] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const { startListening, isSupported } = useSpeechRecognition();

  useEffect(() => {
    if (!isSupported) {
      alert('Speech Recognition not supported in your browser.');
    }
  }, [isSupported]);

  const startQuiz = async (numQuestions) => {
    setLoading(true);
    try {
      const res = await synonymAPI.getQuestions(numQuestions);
      setQuestions(res.data.questions);
      setCurrentIndex(0);
      setTotalScore(0);
    } catch (error) {
      alert('Error fetching questions: ' + error.message);
    }
    setLoading(false);
  };

  const handleAnswer = async () => {
    if (!isSupported || questions.length === 0) return;

    setIsListening(true);
    try {
      const userAnswer = await startListening(5000);
      const question = questions[currentIndex];

      const res = await synonymAPI.checkRelevance(userAnswer, question.answer);
      const relevance = res.data.relevance;
      const points = res.data.points;

      // Update questions array with answer info
      const updatedQuestions = [...questions];
      updatedQuestions[currentIndex] = {
        ...updatedQuestions[currentIndex],
        user_answer: userAnswer,
        relevance,
        points,
      };
      setQuestions(updatedQuestions);
      setTotalScore(totalScore + points);

      // Move to next question
      if (currentIndex < questions.length - 1) {
        setCurrentIndex(currentIndex + 1);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
    setIsListening(false);
  };

  if (questions.length === 0) {
    return (
      <div className="page-container">
        <h1>🎙️ English Speaking Practice Quiz (Synonym Edition)</h1>
        <p>🗣️ Improve your vocabulary by speaking synonyms aloud!</p>

        <div className="input-section">
          <label>Select the number of questions:</label>
          <input type="number" min="1" max="10" defaultValue="5" id="numQuestions" />
          <button onClick={() => startQuiz(parseInt(document.getElementById('numQuestions').value))} disabled={loading}>
            {loading ? 'Loading...' : 'Start Quiz'}
          </button>
        </div>
      </div>
    );
  }

  const quizComplete = currentIndex >= questions.length;
  const currentQuestion = questions[currentIndex];

  return (
    <div className="page-container">
      <h1>🎙️ English Speaking Practice Quiz (Synonym Edition)</h1>

      {!quizComplete ? (
        <div className="practice-section">
          <div className="progress">
            Question {currentIndex + 1} of {questions.length}
          </div>

          <div className="question-box">
            <h2>{currentQuestion.question}</h2>
          </div>

          <button 
            onClick={handleAnswer} 
            disabled={isListening || loading}
            className={isListening ? 'listening' : ''}
          >
            {isListening ? '🎙️ Listening...' : '🎤 Speak Answer'}
          </button>

          {currentQuestion.user_answer && (
            <div className="result-box">
              <h3>You said: {currentQuestion.user_answer}</h3>
              <p>Correct answer: {currentQuestion.answer}</p>
              <p>Similarity: {currentQuestion.relevance}%</p>
              <p className="points">Points: {currentQuestion.points}/15</p>
            </div>
          )}
        </div>
      ) : (
        <div className="result-box">
          <h2>🎉 Quiz Complete!</h2>
          <h3>Final Score: {totalScore} / {questions.length * 15}</h3>

          <h3>Results Summary:</h3>
          {questions.map((q, idx) => (
            <div key={idx} className="question-review">
              <p><strong>Q{idx + 1}:</strong> {q.question}</p>
              <p>✅ Correct: {q.answer}</p>
              <p>🎤 Your answer: {q.user_answer}</p>
              <p>🔍 Similarity: {q.relevance}%</p>
              <p>🏆 Points: {q.points}</p>
            </div>
          ))}

          <button onClick={() => setQuestions([])}>🔄 Restart Quiz</button>
        </div>
      )}
    </div>
  );
};

export default SingleWordSpark;
