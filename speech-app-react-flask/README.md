# Speech Training App - React + Flask

A gamified English speaking practice platform built with **React** (Frontend) and **Python Flask** (Backend), deployed on **Netlify** and a backend hosting service.

## Features

✅ **4 Interactive Modules:**
- 🎤 Fluency Practice - Listen and repeat sentences
- 🎭 Emotion-Based Speaking - Practice with different emotions
- 📝 Sentence Speech Challenge - Speak about topics with AI feedback
- 💡 Synonym Quiz - Improve vocabulary through speaking

✅ **Technology Stack:**
- **Frontend**: React, React Router, Axios
- **Backend**: Python Flask, Flask-CORS
- **AI/ML**: Sentence Transformers, TextBlob, SpeechRecognition
- **Voice**: Web Speech API (Browser-native)
- **Data**: Wikipedia API, Datamuse API

---

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- npm or yarn

### Backend Setup

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('gutenberg')"
```

5. **Run Flask server:**
```bash
python app.py
```
Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend folder:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create .env file:**
```
REACT_APP_API_URL=http://localhost:5000/api
```

4. **Run development server:**
```bash
npm start
```
App opens at `http://localhost:3000`

---

## 📦 Deployment

### Backend Deployment (Render.com / Heroku / Railway.app)

**Using Render.com:**

1. Push backend folder to GitHub
2. Create new Web Service on Render
3. Connect your GitHub repo
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `gunicorn app:app`
6. Deploy

**Environment Variables:**
```
(None required for basic setup)
```

### Frontend Deployment (Netlify)

1. **Build the app:**
```bash
npm run build
```

2. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy React + Flask app"
git push origin main
```

3. **Deploy on Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository
   - Build command: `npm run build`
   - Publish directory: `build`
   - Set Environment Variable:
     ```
     REACT_APP_API_URL = https://your-backend-api.onrender.com/api
     ```
   - Deploy

---

## 📁 Project Structure

```
speech-app-react-flask/
├── backend/
│   ├── app.py                 # Flask server
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile               # For deployment
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.js
│   │   │   └── Navigation.css
│   │   ├── pages/
│   │   │   ├── Home.js
│   │   │   ├── Home.css
│   │   │   ├── FluencyPractice.js
│   │   │   ├── EmotionBasedSpeaking.js
│   │   │   ├── SentenceSpeechChallenge.js
│   │   │   ├── SingleWordSpark.js
│   │   │   └── Pages.css
│   │   ├── services/
│   │   │   ├── api.js         # Axios API calls
│   │   │   └── speechRecognition.js
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── .env.example
│   ├── .gitignore
│   ├── package.json
│   └── netlify.toml           # Netlify config
│
└── README.md
```

---

## 🔧 API Endpoints

### Emotion-Based Speaking
- `GET /api/emotion/generate-sentence` - Generate random sentence
- `POST /api/emotion/detect` - Detect emotion from text
- `POST /api/emotion/calculate-time` - Calculate speaking time
- `POST /api/emotion/feedback` - Get feedback on speed

### Fluency Practice
- `GET /api/fluency/get-sentences?num=5` - Get sentences from Wikipedia
- `POST /api/fluency/analyze-accuracy` - Analyze speaking accuracy

### Sentence Speech Challenge
- `GET /api/sentence/fetch-summary?topic=AI` - Get Wikipedia summary
- `POST /api/sentence/calculate-similarity` - Calculate semantic similarity
- `POST /api/sentence/generate-feedback` - Generate feedback

### Synonym Quiz
- `GET /api/synonym/get-questions?num=5` - Get synonym questions
- `POST /api/synonym/check-relevance` - Check answer relevance

---

## 🎯 Key Features Explained

### 1. **Speech Recognition**
Uses browser's Web Speech API (no server processing needed):
```javascript
const recognition = new SpeechRecognition();
recognition.start();
```

### 2. **Semantic Similarity**
Uses Sentence Transformers on backend:
```python
embeddings = bert_model.encode([text1, text2])
similarity = util.cos_sim(embeddings[0], embeddings[1])
```

### 3. **Emotion Detection**
Uses TextBlob for sentiment analysis:
```python
analysis = TextBlob(text).sentiment.polarity
```

---

## 🌐 Browser Support

| Browser | Support |
|---------|---------|
| Chrome  | ✅ Full |
| Firefox | ✅ Full |
| Safari  | ✅ Full |
| Edge    | ✅ Full |
| IE 11   | ❌ No   |

---

## 🆘 Troubleshooting

### Microphone Not Working
- Check browser permissions
- Ensure HTTPS (not localhost) or localhost
- Try different browser

### Backend API Errors
- Check Flask server is running
- Verify API URL in .env
- Check CORS is enabled in Flask

### Speech Not Recognized
- Speak clearly and loudly
- Check microphone input
- Ensure you're using a supported language

---

## 📝 License

MIT License - Feel free to use for educational purposes.

---

## 👨‍💻 Author

Created for English Speaking Practice Platform

**Questions?** Check the logs and make sure both frontend and backend are running! 🚀
