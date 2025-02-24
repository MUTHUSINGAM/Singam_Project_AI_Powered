import requests
import time
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util
import nltk
import string
import wikipediaapi

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))

# Load Sentence-BERT model for embeddings
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def fetch_wikipedia_summary(topic):
    """
    Fetches a summary of the given topic from Wikipedia.
    """
    wiki_wiki = wikipediaapi.Wikipedia(user_agent="SpeechPracticeApp/1.0 (muthusingam539@gmail.com)", language="en")
    page = wiki_wiki.page(topic)
    
    if page.exists():
        return page.summary
    else:
        print("❌ No Wikipedia article found for the given topic.")
        return None

def extract_keywords(text):
    """
    Extracts keywords from text by:
      - Lowercasing
      - Removing punctuation
      - Filtering out stopwords and short tokens.
    """
    translator = str.maketrans("", "", string.punctuation)
    cleaned_text = text.translate(translator).lower()
    tokens = cleaned_text.split()
    keywords = [word for word in tokens if word not in STOPWORDS and len(word) > 2]
    return set(keywords)

def recognize_speech(timeout):
    """
    Captures user's speech using Google Speech Recognition.
    """
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 1.0
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=2)

        print(f"🎤 Please speak about the topic (You have {timeout} seconds)...")
        start_time = time.time()
        speech_text = []

        while time.time() - start_time < timeout:
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
                text = recognizer.recognize_google(audio)
                print("🗣 Recognized:", text)
                speech_text.append(text)
            except sr.UnknownValueError:
                print("❌ Could not understand, please continue speaking...")
            except sr.RequestError:
                print("⚠ Speech recognition service unavailable. Trying again...")
            except sr.WaitTimeoutError:
                print("⏳ No speech detected for a while. Continuing...")

        final_text = " ".join(speech_text)
        return final_text if final_text else None

def average_embedding(text):
    """
    Computes the average embedding for the given text.
    """
    if not text:
        return None
    embeddings = bert_model.encode([text])
    return embeddings[0]

def generate_feedback(user_speech, reference_text):
    """
    Analyzes user's speech and provides improvement suggestions.
    """
    if not user_speech:
        return "No speech detected. Try speaking clearly and loudly."

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

def improve_speech(user_speech, reference_text):
    """
    Generates an improved version of the user's speech.
    """
    user_words = user_speech.split()
    reference_words = reference_text.split()

    # Keep structure similar but improve coherence
    improved_speech = []
    for word in reference_words:
        if word.lower() in user_words:
            improved_speech.append(word)
        else:
            improved_speech.append(word)  # Retain reference context

    return " ".join(improved_speech)

def run_quiz():
    print("📚 Welcome to the English Speaking Practice Quiz (Context Relationship Edition)!")

    # 1. Get a topic from the user.
    topic = input("Enter a topic for your practice: ").strip()
    if not topic:
        print("⚠ No topic provided. Exiting.")
        return

    # 2. Fetch a reference paragraph from Wikipedia.
    reference_paragraph = fetch_wikipedia_summary(topic)
    if not reference_paragraph:
        print("❌ Failed to fetch reference content. Exiting.")
        return
    print(f"\nReference Paragraph for '{topic}':\n{reference_paragraph}\n")

    # 3. Get user speech duration
    try:
        timeout = int(input("Specify the time (in seconds) for your speech: ").strip())
        if timeout <= 0:
            print("⚠ Invalid time specified. Exiting.")
            return
    except ValueError:
        print("⚠ Invalid input. Please enter a valid number. Exiting.")
        return

    # 4. Capture user's speech
    print("\nNow, please speak about the topic. Your answer will be analyzed for its contextual alignment.")
    user_speech = recognize_speech(timeout=timeout)
    if not user_speech:
        print("❌ No speech detected. Exiting.")
        return

    # 5. Compute the embeddings for similarity analysis
    reference_vector = average_embedding(reference_paragraph)
    user_vector = average_embedding(user_speech)
    if reference_vector is None or user_vector is None:
        print("❌ Failed to compute embeddings. Exiting.")
        return

    # 6. Compute similarity score
    similarity = util.cos_sim(reference_vector, user_vector).item() * 100
    similarity = round(similarity, 2)
    print(f"\n🔎 Cosine Similarity between the reference paragraph and your speech: {similarity}%")

    # 7. Provide feedback
    feedback = generate_feedback(user_speech, reference_paragraph)
    print("\n📢 Feedback on Your Speech:\n", feedback)

    # 8. Generate improved speech
    improved_speech = improve_speech(user_speech, reference_paragraph)
    print("\n✨ Improved Version of Your Speech:\n", improved_speech)

    # 9. Display the user's speech and the reference paragraph.
    print("\n🗣 Your Speech:")
    print(user_speech)
    print("\n📌 Reference Paragraph:")
    print(reference_paragraph)

if __name__ == "__main__":
    run_quiz()
