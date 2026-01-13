import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  const modules = [
    {
      title: '🎤 Fluency Practice',
      description: 'Improve your speaking skills by listening and repeating sentences.',
      path: '/fluency',
      color: '#667eea'
    },
    {
      title: '🎭 Emotion-Based Speaking',
      description: 'Practice speaking with different emotions and get instant feedback.',
      path: '/emotion',
      color: '#764ba2'
    },
    {
      title: '📝 Sentence Speech Challenge',
      description: 'Pick a topic and speak about it with AI-powered feedback.',
      path: '/sentence',
      color: '#f093fb'
    },
    {
      title: '💡 Synonym Quiz',
      description: 'Improve your vocabulary by speaking synonyms aloud!',
      path: '/synonym',
      color: '#f5576c'
    }
  ];

  return (
    <div className="home-container">
      <section className="hero">
        <div className="hero-content">
          <h1>🎓 Welcome to Speech Training App</h1>
          <p>Master English speaking through interactive, gamified learning experiences</p>
          <p className="subtitle">Choose a module below to get started!</p>
        </div>
      </section>

      <section className="modules-grid">
        {modules.map((module, index) => (
          <Link to={module.path} key={index} className="module-card">
            <div className="module-header" style={{ borderTopColor: module.color }}>
              <h2>{module.title}</h2>
            </div>
            <p className="module-description">{module.description}</p>
            <div className="module-footer">
              <span className="cta">Learn More →</span>
            </div>
          </Link>
        ))}
      </section>

      <section className="features">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-item">
            <span className="feature-icon">🎙️</span>
            <h3>Voice Recognition</h3>
            <p>Real-time speech recognition using advanced AI</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📊</span>
            <h3>Instant Feedback</h3>
            <p>Get detailed feedback on accuracy and pronunciation</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🎯</span>
            <h3>Gamified Learning</h3>
            <p>Earn points and improve through interactive challenges</p>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📈</span>
            <h3>Progress Tracking</h3>
            <p>Monitor your improvement over time</p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2026 Speech Training App. Master English Speaking Today!</p>
      </footer>
    </div>
  );
};

export default Home;
