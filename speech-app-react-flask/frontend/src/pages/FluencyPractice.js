import React, { useState, useEffect } from 'react';
import { fluencyAPI } from '../services/api';
import { useSpeechRecognition } from '../services/speechRecognition';
import './Pages.css';

const FluencyPractice = () => {
  const [sentences, setSentences] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [spokenText, setSpokenText] = useState('');
  const [accuracy, setAccuracy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const { startListening, isSupported } = useSpeechRecognition();

  useEffect(() => {
    if (!isSupported) {
      alert('Speech Recognition not supported in your browser. Please use Chrome, Edge, or Safari.');
    }
  }, [isSupported]);

  const startPractice = async (numSentences) => {
    setLoading(true);
    try {
      const res = await fluencyAPI.getSentences(numSentences);
      setSentences(res.data.sentences);
      setCurrentIndex(0);
      setSpokenText('');
      setAccuracy(null);
    } catch (error) {
      alert('Error fetching sentences: ' + error.message);
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
      const text = await startListening(5000);
      setSpokenText(text);

      const res = await fluencyAPI.analyzeAccuracy(sentences[currentIndex], text);
      setAccuracy(res.data.accuracy);
    } catch (error) {
      alert('Error: ' + error.message);
    }
    setIsListening(false);
  };

  const nextSentence = () => {
    if (currentIndex < sentences.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSpokenText('');
      setAccuracy(null);
    } else {
      alert('Practice completed!');
      setSentences([]);
      setCurrentIndex(0);
    }
  };

  return (
    <div className="page-container">
      <h1>🎤 English Speaking Practice App</h1>
      <p>Improve your speaking skills by listening and repeating sentences aloud.</p>

      {sentences.length === 0 ? (
        <div className="input-section">
          <label>How many sentences do you want to practice?</label>
          <input type="number" min="1" max="10" defaultValue="5" id="numSentences" />
          <button onClick={() => startPractice(parseInt(document.getElementById('numSentences').value))}>
            Start Practice
          </button>
        </div>
      ) : (
        <div className="practice-section">
          <div className="progress">
            Sentence {currentIndex + 1} of {sentences.length}
          </div>

          <div className="sentence-box">
            <h2>Sentence:</h2>
            <p className="sentence-text">{sentences[currentIndex]}</p>
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
              {accuracy !== null && (
                <div className="accuracy">
                  <h4>Accuracy: {accuracy.toFixed(2)}%</h4>
                  {accuracy > 80 && <p className="positive">✅ Great job!</p>}
                  {accuracy > 60 && accuracy <= 80 && <p className="neutral">⚠️ Good, but there are some differences</p>}
                  {accuracy <= 60 && <p className="negative">❌ Try again</p>}
                </div>
              )}
              <button onClick={nextSentence}>➡️ Next Sentence</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FluencyPractice;
