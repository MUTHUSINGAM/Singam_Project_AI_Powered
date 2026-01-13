# Speech Training & Gamified Learning App

A Streamlit-based application for English speaking practice with multiple interactive features including fluency practice, emotion-based speaking, single word challenges, and sentence speech challenges.

## Features

- 🗣️ **Fluency Practice**: Practice speaking with random sentences from Wikipedia
- 🎭 **Emotion-Based Speaking**: Practice conveying different emotions in speech
- 💡 **Single Word Spark**: Quick word pronunciation challenges
- 📝 **Sentence Speech Challenge**: Test your sentence speaking skills

## Deployment to Streamlit Cloud

### Prerequisites

1. A GitHub account
2. Your project pushed to a GitHub repository

### Step-by-Step Deployment

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the **Main file path** to: `app.py`
   - Set the **App directory** to: `Model Evalution Streamlit` (or the relative path to your app.py)
   - Click "Deploy"

3. **Your app will be live at**: `https://<your-app-name>.streamlit.app`

### Important Notes

⚠️ **Microphone Access Limitation**: 
- Speech recognition features that require microphone access (`sr.Microphone()`) may not work in Streamlit Cloud due to browser security restrictions
- Consider using file upload for audio input as an alternative for cloud deployment
- For full microphone functionality, users may need to run the app locally

### Local Development

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
Model Evalution Streamlit/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── pages/
│   ├── fluency_practice.py        # Fluency practice page
│   ├── emotion_based_speaking.py  # Emotion-based speaking page
│   ├── single_word_spark.py       # Single word challenges
│   └── sentence_speech_challenge.py # Sentence challenges
└── README.md                       # This file
```

## Dependencies

See `requirements.txt` for the complete list of dependencies.

## License

[Add your license here]
