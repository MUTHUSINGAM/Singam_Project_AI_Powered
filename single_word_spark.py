import streamlit as st
import requests
import random
import string
import speech_recognition as sr
from sentence_transformers import SentenceTransformer, util

# ✅ Cache the model to improve performance
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

bert_model = load_model()

# ✅ Function to fetch a synonym question
def get_datamuse_synonym_question():
    base_url = "https://api.datamuse.com/words"
    max_attempts = 10

    for _ in range(max_attempts):
        letter = random.choice(string.ascii_lowercase)
        resp = requests.get(base_url, params={"sp": f"{letter}*", "max": 50}, timeout=10)
        if resp.status_code != 200:
            continue
        words_data = resp.json()
        if not words_data:
            continue
        word = random.choice(words_data)["word"]

        syn_resp = requests.get(base_url, params={"rel_syn": word, "max": 10}, timeout=10)
        if syn_resp.status_code != 200:
            continue
        syn_data = syn_resp.json()
        if syn_data:
            synonym = random.choice(syn_data)["word"]
            return {"question": f"What is another word for '{word}'?", "answer": synonym.lower()}
    return None

# ✅ Function to get multiple questions
def get_synonym_questions(amount=5):
    questions = []
    attempts = 0
    while len(questions) < amount and attempts < amount * 5:
        q = get_datamuse_synonym_question()
        if q:
            questions.append(q)
        attempts += 1
    return questions if len(questions) >= amount else None

# ✅ Function to recognize speech input with improved accuracy
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak your answer.")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)  # ✅ Adjust noise settings
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)  # ✅ Reduced timeout for faster response
            return recognizer.recognize_google(audio).lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return None

# ✅ Function to check answer relevance using Sentence-BERT
def check_answer_relevance(user_answer, correct_answer):
    if not user_answer:
        return 0
    embeddings = bert_model.encode([user_answer, correct_answer])
    return round(util.cos_sim(embeddings[0], embeddings[1]).item() * 100, 2)

# ✅ Function to calculate score
def score_relevance(relevance):
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

# ✅ Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = None
    st.session_state.current_question = 0
    st.session_state.total_score = 0
    st.session_state.quiz_started = False
    st.session_state.auto_next = False  # ✅ Automatically move to the next question

# ✅ Start the quiz
def start_quiz(num_questions):
    st.session_state.questions = get_synonym_questions(num_questions)
    st.session_state.current_question = 0
    st.session_state.total_score = 0
    st.session_state.quiz_started = True
    st.session_state.auto_next = True  # ✅ Start auto mode
    st.experimental_rerun()

# ✅ Process the answer and move to the next question
def process_answer():
    if st.session_state.current_question < len(st.session_state.questions):
        question = st.session_state.questions[st.session_state.current_question]
        user_answer = recognize_speech()

        if user_answer:
            relevance = check_answer_relevance(user_answer, question["answer"])
            points = score_relevance(relevance)
            st.session_state.total_score += points

            st.session_state.questions[st.session_state.current_question]["user_answer"] = user_answer
            st.session_state.questions[st.session_state.current_question]["relevance"] = relevance
            st.session_state.questions[st.session_state.current_question]["points"] = points
        else:
            st.warning("⚠ No valid answer detected. 0 points.")
            st.session_state.questions[st.session_state.current_question]["user_answer"] = "No Answer"
            st.session_state.questions[st.session_state.current_question]["relevance"] = 0
            st.session_state.questions[st.session_state.current_question]["points"] = 0

        st.session_state.current_question += 1
        if st.session_state.current_question < len(st.session_state.questions):
            st.experimental_rerun()  # ✅ Automatically move to next question

# ✅ Streamlit UI
st.title("🎙️ English Speaking Practice Quiz (Synonym Edition)")
st.write("🗣️ Improve your vocabulary by speaking synonyms aloud!")

if not st.session_state.quiz_started:
    num_questions = st.slider("Select the number of questions:", 1, 10, 5)
    if st.button("Start Quiz"):
        start_quiz(num_questions)

elif st.session_state.current_question < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"🔹 Question {st.session_state.current_question + 1}:")
    st.write(q['question'])

    # ✅ Automatically enable microphone & process answer
    process_answer()

elif st.session_state.current_question == len(st.session_state.questions):
    st.success(f"🎉 Quiz Completed! Your Final Score: {st.session_state.total_score} / {len(st.session_state.questions) * 15}")

    # ✅ Display results
    st.write("### 📚 Review of Questions and Answers:")
    for i, q in enumerate(st.session_state.questions):
        st.write(f"**Q{i+1}:** {q['question']}")
        st.write(f"✅ **Correct Answer:** {q['answer']}")
        st.write(f"🎤 **Your Answer:** {q.get('user_answer', 'No Answer')}")
        st.write(f"🔍 **Similarity Score:** {q.get('relevance', 0)}%")
        st.write(f"🏆 **Points Earned:** {q.get('points', 0)}")
        st.write("---")

    if st.button("Restart Quiz"):
        st.session_state.quiz_started = False
        st.session_state.questions = None
        st.session_state.current_question = 0
        st.session_state.total_score = 0
        st.experimental_rerun()
