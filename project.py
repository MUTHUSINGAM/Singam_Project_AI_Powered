import requests
import time
import random
import string
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util

# Load Sentence-BERT model for answer similarity checking
bert_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def get_datamuse_synonym_question():
    """
    Dynamically generate a synonym question using the Datamuse API.
    It picks a random letter, fetches up to 50 words starting with that letter,
    selects one at random, then queries for synonyms. If at least one synonym is found,
    it returns a question and one correct synonym.
    """
    base_url = "https://api.datamuse.com/words"
    max_attempts = 10
    
    for _ in range(max_attempts):
        letter = random.choice(string.ascii_lowercase)
        # Fetch words starting with the chosen letter
        resp = requests.get(base_url, params={"sp": f"{letter}*", "max": 50}, timeout=10)
        if resp.status_code != 200:
            continue
        words_data = resp.json()
        if not words_data:
            continue
        word = random.choice(words_data)["word"]
        
        # Query for synonyms of the chosen word
        syn_resp = requests.get(base_url, params={"rel_syn": word, "max": 10}, timeout=10)
        if syn_resp.status_code != 200:
            continue
        syn_data = syn_resp.json()
        if syn_data:
            synonym = random.choice(syn_data)["word"]
            question_text = f"What is another word for '{word}'?"
            return {"question": question_text, "answer": synonym.lower(), "type": "synonym"}
    return None

def get_synonym_questions(amount=5):
    questions = []
    attempts = 0
    # Attempt several times to collect enough questions
    while len(questions) < amount and attempts < amount * 5:
        q = get_datamuse_synonym_question()
        if q:
            questions.append(q)
        attempts += 1
    return questions if len(questions) >= amount else None

def get_user_question_count():
    """
    Continuously prompts the user until they enter a number between 1 and 25.
    """
    while True:
        try:
            count = int(input("Enter the number of questions you want to practice (1 to 25): "))
            if count < 1 or count > 25:
                print("⚠ Only between 1 and 25 questions are allowed. Please try again.")
            else:
                return count
        except ValueError:
            print("❌ Invalid input. Please enter a valid number.")

def recognize_speech(timeout=5, retry=1):
    """
    Captures the user's spoken answer using Google Speech Recognition.
    Calibrates for ambient noise and optionally retries once if needed.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        for attempt in range(retry + 1):
            print("🎤 Speak your answer now (You have 5 seconds)...")
            try:
                audio = recognizer.listen(source, timeout=timeout)
                user_answer = recognizer.recognize_google(audio)
                print(f"🗣 You said: {user_answer}")
                return user_answer.lower()
            except sr.WaitTimeoutError:
                print("⏳ Time's up! No response detected.")
            except sr.UnknownValueError:
                print("❌ Could not understand audio.")
            except sr.RequestError:
                print("⚠ Speech recognition service unavailable.")
            if attempt < retry:
                print("Let's try again...")
    return None

def check_answer_relevance(user_answer, correct_answer):
    """
    Computes the cosine similarity between the user's answer and the correct synonym
    using Sentence-BERT, and returns a percentage score.
    """
    if not user_answer:
        return 0
    embeddings = bert_model.encode([user_answer, correct_answer])
    relevance_score = util.cos_sim(embeddings[0], embeddings[1]).item() * 100
    return round(relevance_score, 2)

def score_relevance(relevance):
    """
    Returns a score based on the relevance percentage:
      - 90% or higher: 15 points
      - 80% to 89%: 10 points
      - 70% to 79%: 8 points
      - 60% to 69%: 5 points
      - 50% to 59%: 3 points
      - Below 50%: 0 points
    """
    if relevance >= 90:
        return 15
    elif relevance >= 80:
        return 10
    elif relevance >= 70:
        return 8
    elif relevance >= 60:
        return 5
    elif relevance >= 50:
        return 3
    else:
        return 0

def run_quiz():
    print("📚 Welcome to the English Speaking Practice Quiz (Synonym Edition)!")
    
    num_questions = get_user_question_count()
    
    questions = get_synonym_questions(num_questions)
    if not questions:
        print("❌ Failed to fetch enough questions. Try again later.")
        return

    total_score = 0
    for i, q in enumerate(questions):
        print(f"\n🔹 Question {i+1} ({q['type']}): {q['question']}")
        user_answer = recognize_speech(timeout=5, retry=1)
        if user_answer:
            relevance = check_answer_relevance(user_answer, q["answer"])
            print(f"🔎 Answer Relevance: {relevance}%")
            points = score_relevance(relevance)
            if points == 15:
                print("🎉 Excellent! You get 15 points.")
            elif points == 10:
                print("🎉 Correct! You get 10 points.")
            elif points == 8:
                print("👍 Good job! You get 8 points.")
            elif points == 5:
                print("🙂 Partially correct. You get 5 points.")
            elif points == 3:
                print("🙁 Almost there. You get 3 points.")
            else:
                print("❌ Incorrect. 0 points.")
            total_score += points
        else:
            print("⚠ No valid answer detected. 0 points.")
        time.sleep(2)
    
    print(f"\n🏆 Final Score: {total_score} / {num_questions * 15}")
    print("📌 Quiz completed! Keep practicing your English speaking skills.")
    
    # Review section
    print("\n📚 Review of Questions and Correct Answers:")
    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['question']}  Correct Answer: {q['answer']}")

if __name__ == "__main__":
    run_quiz()
