import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import FluencyPractice from './pages/FluencyPractice';
import EmotionBasedSpeaking from './pages/EmotionBasedSpeaking';
import SentenceSpeechChallenge from './pages/SentenceSpeechChallenge';
import SingleWordSpark from './pages/SingleWordSpark';
import './App.css';

function App() {
  return (
    <Router>
      <Navigation />
      <div className="app-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/fluency" element={<FluencyPractice />} />
          <Route path="/emotion" element={<EmotionBasedSpeaking />} />
          <Route path="/sentence" element={<SentenceSpeechChallenge />} />
          <Route path="/synonym" element={<SingleWordSpark />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
