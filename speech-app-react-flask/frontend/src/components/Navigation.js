import React from 'react';
import { Link } from 'react-router-dom';
import './Navigation.css';

const Navigation = () => {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-logo">
          🎓 Speech Training App
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link to="/fluency" className="nav-link">🎤 Fluency Practice</Link>
          </li>
          <li className="nav-item">
            <Link to="/emotion" className="nav-link">🎭 Emotion Speaking</Link>
          </li>
          <li className="nav-item">
            <Link to="/sentence" className="nav-link">📝 Sentence Challenge</Link>
          </li>
          <li className="nav-item">
            <Link to="/synonym" className="nav-link">💡 Synonym Quiz</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;
