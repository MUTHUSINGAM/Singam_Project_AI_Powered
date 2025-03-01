# AI-Powered Public Speaking Training Platform

## Overview
The Speech Training & Gamified Learning App is a Streamlit-based web application designed to enhance speech fluency and expression through interactive exercises. The app provides real-time feedback and gamified learning experiences to help users improve their public speaking skills. Additionally, the platform includes a module for hearing-impaired individuals, converting Tamil speech to sign language.

## Technologies Used
- **Streamlit**: For building the web-based interactive interface.
- **Streamlit Pages API**: For modular navigation between different training exercises.
- **Speech Recognition API**: Converts speech to text and provides feedback.
- **Text-to-Speech (TTS) API**: Pronounces sentences for accurate learning.
- **Sentence-BERT**: Used for similarity scoring in speech evaluation.
- **Wikipedia API**: Fetches random sentences for practice.
- **NLTK Gutenberg Corpus**: Generates emotion-based sentences.
- **Google Speech Recognition API**: Recognizes user speech.
- **Datamuse API**: Fetches synonyms for vocabulary exercises.

## Application Structure
```
Model Evaluation Streamlit/
│── pages/
│   ├── emotion_based_speaking.py
│   ├── fluency_practice.py
│   ├── sentence_speech_challenge.py
│   ├── single_word_spark.py
│── app.py
│── requirements.txt
```

## Modules
### 1. Fluency Practice (🗣️)
Helps users practice smooth and continuous speech.

**Features:**
- 🎤 Speech Recognition
- 🔊 Text-to-Speech (TTS)
- 📖 Wikipedia Sentence Fetching
- 📈 Accuracy & Speed Analysis
- ⏳ Time Calculation
- 🔄 Restart & Next Sentence Options

**Workflow:**
1. User selects the number of sentences to practice.
2. Random sentences are fetched from Wikipedia.
3. User listens to correct pronunciation.
4. User speaks the sentence aloud.
5. App analyzes pronunciation accuracy and speaking speed.
6. User receives feedback and can proceed or restart.

### 2. Emotion-Based Speaking (🎭)
Enhances speech delivery by incorporating emotional expressions.

**Features:**
- Dynamic Sentence Generation
- Emotion Detection
- Speech Recognition
- Speaking Time Analysis
- TTS Pronunciation Assistance

**Workflow:**
1. User selects the number of sentences for practice.
2. App generates random sentences and assigns emotions.
3. User listens to correct pronunciation.
4. Speech is recorded and analyzed for accuracy and speed.
5. Feedback on fluency and emotion expression is provided.

### 3. Single Word Spark (💡)
Focuses on articulation and pronunciation of individual words through a voice-based quiz.

**Features:**
- 🎙️ Voice-based quiz interaction
- 📚 Synonym-based questions using Datamuse API
- 🤖 Speech Recognition
- 📊 Sentence-BERT similarity scoring
- 🔄 Automated quiz progression
- 🏆 Real-time scoring system

**Workflow:**
1. User selects the number of quiz questions.
2. Random words and synonyms are fetched.
3. User speaks the correct synonym aloud.
4. Speech is recognized and compared using Sentence-BERT.
5. Scores are calculated based on similarity percentage.

### 4. Sentence Speech Challenge (📝)
Encourages structured sentence formation and verbal delivery.

**Features:**
- Speech Recognition
- Wikipedia Content Extraction
- Keyword Analysis
- AI-Based Feedback
- Speech Similarity Scoring
- Speech Enhancement Suggestions

**Workflow:**
1. User selects a Wikipedia topic for practice.
2. App fetches a summary of the topic.
3. User listens to the correct pronunciation.
4. User speaks the passage aloud.
5. System compares speech with reference text and provides feedback.

### 5. Tamil Speech to Sign Language
A module designed to assist hearing-impaired individuals by converting Tamil speech into sign language.

**Features:**
- Converts Tamil speech into Tamil text.
- Maps Tamil text to sign language images.
- Displays the corresponding hand gestures sequentially.

**Workflow:**
1. User clicks "Record Speech" and speaks in Tamil.
2. System converts speech into Tamil text.
3. Extracts individual Tamil characters.
4. Maps characters to sign language images.
5. Displays hand gestures for interpretation.

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/MUTHUSINGAM/ai-speech-training-platform.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Model_Evaluation_Streamlit
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the Streamlit application:
   ```sh
   streamlit run app.py
   ```

## Future Enhancements
- **Real-time AI coaching** using GPT-based models.
- **Multilingual support** for non-English speakers.
- **Advanced emotion recognition** with deep learning models.
- **Personalized training** with user progress tracking.

## Contact
For any issues or suggestions, reach out via:
- **Email**: muthusingam539@gmail.com
- **LinkedIn**: [Muthusingam](https://www.linkedin.com/in/muthusingam18/)
- **GitHub**: [MUTHUSINGAM](https://github.com/MUTHUSINGAM)

---
