from flask import Flask, request, jsonify
from flask_cors import CORS
from textblob import TextBlob
from sentence_transformers import SentenceTransformer, util
import nltk
import random
import string
import requests
import wikipediaapi
import json

app = Flask(__name__)
CORS(app)

# Download NLTK data
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('gutenberg', quiet=True)

# Load BERT model for semantic similarity
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load words from NLTK
from nltk.corpus import gutenberg, stopwords
words = list(gutenberg.words('austen-emma.txt'))

# ============= EMOTION-BASED SPEAKING =============

@app.route('/api/emotion/generate-sentence', methods=['GET'])
def generate_sentence():
    """Generate a random sentence"""
    sentence_length = random.randint(8, 15)
    sentence = " ".join(random.sample(words, sentence_length)) + "."
    return jsonify({"sentence": sentence.capitalize()})

@app.route('/api/emotion/detect', methods=['POST'])
def detect_emotion():
    """Detect emotion from text"""
    data = request.json
    text = data.get('text', '')
    
    analysis = TextBlob(text).sentiment.polarity
    
    if analysis > 0.5:
        emotion = "Happy 😊"
    elif 0.1 < analysis <= 0.5:
        emotion = "Motivated 💪"
    elif -0.1 <= analysis <= 0.1:
        emotion = "Neutral 😐"
    elif -0.5 < analysis < -0.1:
        emotion = "Sad 😔"
    else:
        emotion = "Angry 😠"
    
    return jsonify({"emotion": emotion, "polarity": float(analysis)})

@app.route('/api/emotion/calculate-time', methods=['POST'])
def calculate_speaking_time():
    """Calculate expected speaking time"""
    data = request.json
    sentence = data.get('sentence', '')
    
    words_list = nltk.word_tokenize(sentence)
    avg_read_speed = 3
    time = min(len(words_list) / avg_read_speed, 15)
    
    return jsonify({"allowed_time": round(time, 2)})

@app.route('/api/emotion/feedback', methods=['POST'])
def provide_feedback():
    """Provide feedback on speaking speed"""
    data = request.json
    actual_time = data.get('actual_time', 0)
    allowed_time = data.get('allowed_time', 0)
    
    extra_time = actual_time - allowed_time
    
    if extra_time > 3:
        feedback = f"⚠️ You took {round(extra_time, 2)} extra seconds. Try to be more concise."
    elif extra_time < -3:
        feedback = "⚠️ You spoke too fast! Try to slow down for better clarity."
    else:
        feedback = "✅ Your speaking speed is well-balanced!"
    
    return jsonify({"feedback": feedback})

# ============= FLUENCY PRACTICE =============

@app.route('/api/fluency/get-sentences', methods=['GET'])
def get_fluency_sentences():
    """Fetch random sentences from Wikipedia"""
    num = request.args.get('num', 5, type=int)
    
    sentences = []
    attempts = 0
    while len(sentences) < num and attempts < num * 5:
        try:
            import wikipedia
            random_title = wikipedia.random()
            summary = wikipedia.summary(random_title, sentences=3)
            extracted = nltk.tokenize.sent_tokenize(summary)
            sentences.extend(extracted)
            attempts += 1
        except:
            attempts += 1
            continue
    
    return jsonify({"sentences": sentences[:num]})

@app.route('/api/fluency/calculate-time', methods=['POST'])
def fluency_calculate_time():
    """Calculate speaking time for fluency"""
    data = request.json
    sentence = data.get('sentence', '')
    
    words_list = nltk.word_tokenize(sentence)
    avg_read_speed = 3
    time = min(len(words_list) / avg_read_speed, 15)
    
    return jsonify({"allowed_time": round(time, 2)})

@app.route('/api/fluency/analyze-accuracy', methods=['POST'])
def analyze_accuracy():
    """Analyze speaking accuracy"""
    data = request.json
    correct_sentence = data.get('correct_sentence', '')
    spoken_text = data.get('spoken_text', '')
    
    correct_words = set(nltk.word_tokenize(correct_sentence.lower()))
    spoken_words = set(nltk.word_tokenize(spoken_text.lower()))
    
    if len(correct_words) == 0:
        accuracy = 0
    else:
        accuracy = (len(correct_words & spoken_words) / len(correct_words)) * 100
    
    return jsonify({"accuracy": round(accuracy, 2)})

# ============= SENTENCE SPEECH CHALLENGE =============

@app.route('/api/sentence/fetch-summary', methods=['GET'])
def fetch_summary():
    """Fetch Wikipedia summary"""
    topic = request.args.get('topic', '')
    
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent="SpeechPracticeApp/1.0"
    )
    
    page = wiki_wiki.page(topic)
    if page.exists():
        return jsonify({"summary": page.summary})
    else:
        return jsonify({"error": "No Wikipedia article found"}), 404

@app.route('/api/sentence/extract-keywords', methods=['POST'])
def extract_keywords():
    """Extract keywords from text"""
    data = request.json
    text = data.get('text', '')
    
    stopwords_set = set(nltk.corpus.stopwords.words('english'))
    translator = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(translator).lower()
    tokens = nltk.word_tokenize(cleaned_text)
    keywords = [word for word in tokens if word not in stopwords_set and len(word) > 2]
    
    return jsonify({"keywords": keywords})

@app.route('/api/sentence/calculate-similarity', methods=['POST'])
def calculate_similarity():
    """Calculate semantic similarity"""
    data = request.json
    user_speech = data.get('user_speech', '')
    reference_text = data.get('reference_text', '')
    
    if not user_speech or not reference_text:
        return jsonify({"similarity": 0})
    
    embeddings = bert_model.encode([user_speech, reference_text])
    similarity = float(util.cos_sim(embeddings[0], embeddings[1]).item() * 100)
    
    return jsonify({"similarity": round(similarity, 2)})

@app.route('/api/sentence/generate-feedback', methods=['POST'])
def generate_sentence_feedback():
    """Generate feedback for speech"""
    data = request.json
    user_speech = data.get('user_speech', '')
    reference_text = data.get('reference_text', '')
    
    if not user_speech:
        return jsonify({"feedback": "⚠ No speech detected. Try speaking clearly and loudly."})
    
    user_keywords = set(extract_keywords_logic(user_speech))
    reference_keywords = set(extract_keywords_logic(reference_text))
    
    missing_keywords = reference_keywords - user_keywords
    feedback_list = []
    
    if missing_keywords:
        feedback_list.append(f"⚠ Missing keywords: {', '.join(list(missing_keywords)[:5])}")
    
    if len(user_speech.split()) < len(reference_text.split()) * 0.5:
        feedback_list.append("🗣 Your speech is too short. Elaborate more.")
    
    if not feedback_list:
        feedback_list.append("✅ Well done! Your speech covers the topic well.")
    
    return jsonify({"feedback": "\n".join(feedback_list)})

def extract_keywords_logic(text):
    """Helper function to extract keywords"""
    stopwords_set = set(nltk.corpus.stopwords.words('english'))
    translator = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(translator).lower()
    tokens = nltk.word_tokenize(cleaned_text)
    return [word for word in tokens if word not in stopwords_set and len(word) > 2]

# ============= SINGLE WORD SPARK (SYNONYM QUIZ) =============

@app.route('/api/synonym/get-questions', methods=['GET'])
def get_synonym_questions():
    """Fetch synonym questions"""
    num = request.args.get('num', 5, type=int)
    
    questions = []
    attempts = 0
    
    while len(questions) < num and attempts < num * 5:
        try:
            letter = random.choice(string.ascii_lowercase)
            resp = requests.get("https://api.datamuse.com/words", 
                              params={"sp": f"{letter}*", "max": 50}, 
                              timeout=5)
            if resp.status_code != 200:
                attempts += 1
                continue
            
            words_data = resp.json()
            if not words_data:
                attempts += 1
                continue
            
            word = random.choice(words_data)["word"]
            
            syn_resp = requests.get("https://api.datamuse.com/words",
                                   params={"rel_syn": word, "max": 10},
                                   timeout=5)
            if syn_resp.status_code != 200:
                attempts += 1
                continue
            
            syn_data = syn_resp.json()
            if syn_data:
                synonym = random.choice(syn_data)["word"]
                questions.append({
                    "question": f"What is another word for '{word}'?",
                    "answer": synonym.lower()
                })
            
            attempts += 1
        except:
            attempts += 1
            continue
    
    return jsonify({"questions": questions})

@app.route('/api/synonym/check-relevance', methods=['POST'])
def check_synonym_relevance():
    """Check answer relevance"""
    data = request.json
    user_answer = data.get('user_answer', '')
    correct_answer = data.get('correct_answer', '')
    
    if not user_answer:
        return jsonify({"relevance": 0, "points": 0})
    
    embeddings = bert_model.encode([user_answer, correct_answer])
    relevance = float(util.cos_sim(embeddings[0], embeddings[1]).item() * 100)
    
    # Calculate points
    if relevance >= 90:
        points = 15
    elif relevance >= 80:
        points = 10
    elif relevance >= 70:
        points = 8
    elif relevance >= 60:
        points = 5
    elif relevance >= 50:
        points = 3
    else:
        points = 0
    
    return jsonify({
        "relevance": round(relevance, 2),
        "points": points
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
