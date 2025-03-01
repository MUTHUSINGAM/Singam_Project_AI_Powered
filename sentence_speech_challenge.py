import streamlit as st
import speech_recognition as sr
import nltk
import string
import wikipediaapi
from sentence_transformers import SentenceTransformer, util

# ✅ Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# ✅ Load Sentence-BERT model for answer similarity checking
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

bert_model = load_model()

# ✅ Function to fetch a summary from Wikipedia
def fetch_wikipedia_summary(topic):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent="SpeechPracticeApp/1.0 (muthusingam539@gmail.com)"
    )

    page = wiki_wiki.page(topic)
    if page.exists():
        return page.summary
    else:
        st.error("❌ No Wikipedia article found for the given topic.")
        return None

# ✅ Function to extract keywords from text
def extract_keywords(text):
    stopwords = set(nltk.corpus.stopwords.words('english'))
    translator = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(translator).lower()
    tokens = nltk.word_tokenize(cleaned_text)
    keywords = [word for word in tokens if word not in stopwords and len(word) > 2]
    return set(keywords)

# ✅ Function to recognize speech
def recognize_speech(duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=duration)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.warning("⚠ Time is up! No speech detected.")
            return None
        except sr.UnknownValueError:
            st.warning("❌ Could not understand speech. Try again.")
            return None
        except sr.RequestError:
            st.error("⚠ Speech recognition service is unavailable.")
            return None

# ✅ Function to compute average embedding
def average_embedding(text):
    if not text:
        return None
    embeddings = bert_model.encode([text])
    return embeddings[0]

# ✅ Function to generate feedback
def generate_feedback(user_speech, reference_text):
    if not user_speech:
        return "⚠ No speech detected. Try speaking clearly and loudly."

    user_keywords = extract_keywords(user_speech)
    reference_keywords = extract_keywords(reference_text)

    missing_keywords = reference_keywords - user_keywords
    extra_keywords = user_keywords - reference_keywords

    feedback = []

    if missing_keywords:
        feedback.append(f"⚠ Missing important keywords: {', '.join(list(missing_keywords)[:5])}")

    if extra_keywords:
        feedback.append(f"🛠 Extra words used that may not be relevant: {', '.join(list(extra_keywords)[:5])}")

    if len(user_speech.split()) < len(reference_text.split()) * 0.5:
        feedback.append("🗣 Your speech is too short. Try elaborating more on the topic.")

    if len(feedback) == 0:
        feedback.append("✅ Well done! Your speech covers the topic well.")

    return "\n".join(feedback)

# ✅ Function to improve speech
def improve_speech(user_speech, reference_text):
    user_words = user_speech.split()
    reference_words = reference_text.split()

    improved_speech = []
    for word in reference_words:
        if word.lower() in user_words:
            improved_speech.append(word)
        else:
            improved_speech.append(word)

    return " ".join(improved_speech)

# ✅ Streamlit UI Layout
st.title("🗣️ English Speaking Practice with AI Feedback")

# Initialize reference_paragraph before using it
reference_paragraph = None

# ✅ Input topic
topic = st.text_input("📌 Enter a topic for your practice:")

if topic:
    # ✅ Fetch Wikipedia Summary
    reference_paragraph = fetch_wikipedia_summary(topic)

    if reference_paragraph:  # Check if summary was found
        st.subheader("📚 Reference Paragraph")
        st.write(reference_paragraph)

    # ✅ Set speaking time
    duration = st.slider("⏳ Set your speaking time (seconds):", min_value=10, max_value=120, value=30)

    # ✅ Start speaking button
    if st.button("🎤 Start Speaking"):
        user_speech = recognize_speech(duration)

        if user_speech:
            st.subheader("🗣 Your Speech")
            st.write(user_speech)

            reference_vector = average_embedding(reference_paragraph)
            user_vector = average_embedding(user_speech)

            if reference_vector is not None and user_vector is not None:
                similarity = util.cos_sim(reference_vector, user_vector).item() * 100
                similarity = round(similarity, 2)
                st.write(f"🔍 Cosine Similarity: **{similarity}%**")

                # ✅ Generate feedback
                feedback = generate_feedback(user_speech, reference_paragraph)
                st.subheader("📢 Feedback")
                st.write(feedback)

                # ✅ Improve speech
                improved_speech = improve_speech(user_speech, reference_paragraph)
                st.subheader("✨ Improved Version of Your Speech")
                st.write(improved_speech)
