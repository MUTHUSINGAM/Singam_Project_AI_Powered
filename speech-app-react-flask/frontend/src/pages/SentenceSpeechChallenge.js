import React, { useState } from 'react';
import { sentenceAPI } from '../services/api';
import { useSpeechRecognition } from '../services/speechRecognition';
import './Pages.css';

const SentenceSpeechChallenge = () => {
  const [topic, setTopic] = useState('');
  const [summary, setSummary] = useState('');
  const [duration, setDuration] = useState(30);
  const [spokenText, setSpokenText] = useState('');
  const [similarity, setSimilarity] = useState(null);
  const [feedbackText, setFeedbackText] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const { startListening, isSupported } = useSpeechRecognition();

  const handleTopicSubmit = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    try {
      const res = await sentenceAPI.fetchSummary(topic);
      setSummary(res.data.summary);
      setSpokenText('');
      setSimilarity(null);
      setFeedbackText('');
    } catch (error) {
      alert('Error fetching topic: ' + error.message);
    }
    setLoading(false);
  };

  const handleSpeak = async () => {
    if (!isSupported) {
      alert('Speech Recognition not supported');
      return;
    }

    setIsListening(true);
    try {
      const text = await startListening(duration * 1000);
      setSpokenText(text);

      const simRes = await sentenceAPI.calculateSimilarity(text, summary);
      setSimilarity(simRes.data.similarity);

      const feedbackRes = await sentenceAPI.generateFeedback(text, summary);
      setFeedbackText(feedbackRes.data.feedback);
    } catch (error) {
      alert('Error: ' + error.message);
    }
    setIsListening(false);
  };

  return (
    <div className="page-container">
      <h1>🗣️ English Speaking Practice with AI Feedback</h1>
      <p>Pick a topic and speak about it. Get AI-powered feedback on your speech.</p>

      {!summary ? (
        <form onSubmit={handleTopicSubmit} className="input-section">
          <input
            type="text"
            placeholder="Enter a topic (e.g., 'Artificial Intelligence')"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
          <button type="submit" disabled={loading || !topic.trim()}>
            {loading ? 'Loading...' : 'Fetch Topic'}
          </button>
        </form>
      ) : (
        <div className="practice-section">
          <div className="sentence-box">
            <h2>📚 Reference Text:</h2>
            <p>{summary}</p>
          </div>

          <div className="input-section">
            <label>Speaking time (seconds):</label>
            <input
              type="range"
              min="10"
              max="120"
              value={duration}
              onChange={(e) => setDuration(parseInt(e.target.value))}
            />
            <span>{duration}s</span>
          </div>

          <button 
            onClick={handleSpeak} 
            disabled={isListening || loading}
            className={isListening ? 'listening' : ''}
          >
            {isListening ? '🎙️ Listening...' : '🎤 Start Speaking'}
          </button>

          {spokenText && (
            <div className="result-box">
              <h3>Your Speech:</h3>
              <p>{spokenText}</p>
              
              {similarity !== null && (
                <div className="similarity">
                  <h4>🔍 Similarity Score: {similarity.toFixed(2)}%</h4>
                </div>
              )}

              {feedbackText && (
                <div className="feedback">
                  <h4>📢 Feedback:</h4>
                  <p>{feedbackText}</p>
                </div>
              )}

              <button onClick={() => {
                setTopic('');
                setSummary('');
                setSpokenText('');
              }}>🔄 Try Another Topic</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SentenceSpeechChallenge;
