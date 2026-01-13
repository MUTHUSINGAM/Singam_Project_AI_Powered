import React, { useState } from 'react';
import { emotionAPI } from '../services/api';
import { useSpeechRecognition } from '../services/speechRecognition';
import './Pages.css';

const EmotionBasedSpeaking = () => {
  const [sentence, setSentence] = useState('');
  const [emotion, setEmotion] = useState('');
  const [allowedTime, setAllowedTime] = useState(0);
  const [spokenText, setSpokenText] = useState('');
  const [actualTime, setActualTime] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [loading, setLoading] = useState(false);
  const { startListening, isSupported } = useSpeechRecognition();

  const generateSentence = async () => {
    setLoading(true);
    try {
      const res = await emotionAPI.generateSentence();
      const newSentence = res.data.sentence;
      setSentence(newSentence);

      const emotionRes = await emotionAPI.detectEmotion(newSentence);
      setEmotion(emotionRes.data.emotion);

      const timeRes = await emotionAPI.calculateTime(newSentence);
      setAllowedTime(timeRes.data.allowed_time);

      setSpokenText('');
      setActualTime(null);
      setFeedback('');
    } catch (error) {
      alert('Error generating sentence: ' + error.message);
    }
    setLoading(false);
  };

  const handleSpeak = async () => {
    if (!isSupported) {
      alert('Speech Recognition not supported');
      return;
    }

    setIsListening(true);
    const startTime = Date.now();

    try {
      const text = await startListening(allowedTime * 1000);
      const endTime = Date.now();
      const timeTaken = (endTime - startTime) / 1000;

      setSpokenText(text);
      setActualTime(timeTaken);

      const feedbackRes = await emotionAPI.provideFeedback(timeTaken, allowedTime);
      setFeedback(feedbackRes.data.feedback);
    } catch (error) {
      alert('Error: ' + error.message);
    }

    setIsListening(false);
  };

  return (
    <div className="page-container">
      <h1>🗣️ Speech Training & Emotion Recognition App</h1>
      <p>Practice speaking with different emotions and get instant feedback.</p>

      {!sentence ? (
        <div className="input-section">
          <button onClick={generateSentence} disabled={loading}>
            {loading ? 'Loading...' : 'Generate Sentence'}
          </button>
        </div>
      ) : (
        <div className="practice-section">
          <div className="sentence-box">
            <h2>Sentence:</h2>
            <p className="sentence-text">{sentence}</p>
            <h3>Emotion to convey: {emotion}</h3>
            <p>You have {allowedTime.toFixed(2)} seconds to read this aloud.</p>
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
              <h3>You said:</h3>
              <p>{spokenText}</p>
              {actualTime && (
                <>
                  <p>⏱️ Time taken: {actualTime.toFixed(2)} seconds</p>
                  <p>📢 Feedback: {feedback}</p>
                </>
              )}
              <button onClick={generateSentence}>🔄 Next Sentence</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default EmotionBasedSpeaking;
