import time
import nltk
import streamlit as st
import speech_recognition as sr
import wikipedia
import random
import pyttsx3
import threading

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the Text-to-Speech (TTS) engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed
engine.setProperty('volume', 1)  # Set volume

# ✅ Function to pronounce the current sentence in a separate thread
def pronounce_current_sentence(sentence):
    def speak():
        engine.say(sentence)
        engine.runAndWait()
    
    tts_thread = threading.Thread(target=speak)
    tts_thread.start()

# ✅ Function to fetch random sentences from Wikipedia
def get_random_sentences(num_sentences):
    sentences = []
    while len(sentences) < num_sentences:
        try:
            random_title = wikipedia.random()
            summary = wikipedia.summary(random_title, sentences=5)
            extracted_sentences = nltk.tokenize.sent_tokenize(summary)
            sentences.extend(extracted_sentences)
        except Exception:
            continue  # Try again if an error occurs
    return sentences[:num_sentences]

# ✅ Function to calculate speaking time
def calculate_speaking_time(sentence):
    words = nltk.word_tokenize(sentence)
    avg_read_speed = 3  # Average 3 words per second
    return min(len(words) / avg_read_speed, 15)

# ✅ Function to recognize speech
def recognize_speech(timeout_duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"🎤 Speak now... (Listening for {timeout_duration} seconds)")
        try:
            audio = recognizer.listen(source, timeout=timeout_duration)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "❌ Error: Could not understand speech."
        except sr.RequestError:
            return "⚠️ Error: Speech recognition service unavailable."

# ✅ Initialize Streamlit Session State
if "sentences" not in st.session_state:
    st.session_state.sentences = []
    st.session_state.current_index = 0
    st.session_state.result = None
    st.session_state.allowed_time = 0

# ✅ Streamlit UI
st.title("🎤 English Speaking Practice App")
st.write("Improve your speaking skills by listening and repeating sentences aloud.")

# ✅ Select Number of Sentences at Start
if not st.session_state.sentences:
    num_sentences = st.number_input("Enter the number of sentences to practice (Max 10):", min_value=1, max_value=10, value=5)
    
    if st.button("Start Practice"):
        st.session_state.sentences = get_random_sentences(num_sentences)
        st.session_state.current_index = 0
        st.session_state.result = None
        st.session_state.allowed_time = calculate_speaking_time(st.session_state.sentences[0])
        st.rerun()

# ✅ Only proceed if sentences exist
if st.session_state.sentences:
    current_sentence = st.session_state.sentences[st.session_state.current_index]
    st.write(f"**Sentence {st.session_state.current_index + 1}:** {current_sentence}")

    # ✅ Pronounce the current sentence correctly each time
    if st.button("🔊 How to Pronounce"):
        pronounce_current_sentence(current_sentence)

    # ✅ Speech Recognition
    if st.button("🎙️ Start Speaking"):
        st.session_state.result = recognize_speech(st.session_state.allowed_time)

    # ✅ Display Speech Recognition Result & Feedback
    if st.session_state.result:
        st.write(f"✅ **You said:** {st.session_state.result}")

        # ✅ Accuracy Calculation
        correct_words = set(nltk.word_tokenize(current_sentence.lower()))
        spoken_words = set(nltk.word_tokenize(st.session_state.result.lower()))
        accuracy = (len(correct_words & spoken_words) / len(correct_words)) * 100

        # ✅ Speed Analysis
        time_taken = len(spoken_words) / 3  # Approximate time taken
        speed = len(spoken_words) / time_taken  # Words per second
        normal_speed = len(correct_words) / st.session_state.allowed_time

        if speed > normal_speed * 1.3:
            st.write("⚠️ You are speaking too fast! Try to slow down.")
        elif speed < normal_speed * 0.7:
            st.write("⚠️ You are speaking too slowly! Try to speak more fluently.")
        else:
            st.write("✅ Your speaking speed is balanced.")

        # ✅ Extra Time Analysis
        extra_time = time_taken - st.session_state.allowed_time
        if extra_time > 0:
            st.write(f"⏳ You took {round(extra_time, 2)} seconds extra.")

        st.write(f"🎯 Accuracy: {round(accuracy, 2)}%")

    # ✅ Next Sentence Button
    if st.button("➡️ Next Sentence"):
        if st.session_state.current_index < len(st.session_state.sentences) - 1:
            st.session_state.current_index += 1
            st.session_state.result = None
            st.session_state.allowed_time = calculate_speaking_time(st.session_state.sentences[st.session_state.current_index])
            st.rerun()
        else:
            st.success("🎉 Practice Completed!")

    # ✅ Restart Practice Button
    if st.button("🔄 Restart Practice"):
        st.session_state.sentences = []
        st.session_state.current_index = 0
        st.session_state.result = None
        st.rerun()
