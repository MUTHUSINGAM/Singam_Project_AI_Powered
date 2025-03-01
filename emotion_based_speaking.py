import streamlit as st
import speech_recognition as sr
from textblob import TextBlob
import nltk
import random
import time
from gtts import gTTS
import os

# Ensure NLTK data is downloaded
nltk.download('punkt')
nltk.download('gutenberg')

# Load dataset from NLTK
from nltk.corpus import gutenberg
words = list(gutenberg.words('austen-emma.txt'))

# Initialize session state
if "sentences" not in st.session_state:
    st.session_state.sentences = []

if "current_sentence" not in st.session_state:
    st.session_state.current_sentence = ""

if "last_pronounced" not in st.session_state:
    st.session_state.last_pronounced = ""

# Function to generate a dynamic sentence
def generate_sentence():
    sentence_length = random.randint(8, 15)
    sentence = " ".join(random.sample(words, sentence_length)) + "."
    return sentence.capitalize()

# Function to determine emotion
def detect_emotion(sentence):
    analysis = TextBlob(sentence).sentiment.polarity
    if analysis > 0.5:
        return "Happy 😊"
    elif 0.1 < analysis <= 0.5:
        return "Motivated 💪"
    elif -0.1 <= analysis <= 0.1:
        return "Neutral 😐"
    elif -0.5 < analysis < -0.1:
        return "Sad 😔"
    else:
        return "Angry 😠"

# Function to calculate speaking time
def calculate_speaking_time(sentence):
    words = nltk.word_tokenize(sentence)
    avg_read_speed = 3  # Average 3 words per second
    return min(len(words) / avg_read_speed, 15)  # Max limit of 15 sec per sentence

# Function to recognize user speech
def recognize_speech(timeout_duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info(f"🎤 Listening... (Max {timeout_duration} sec)")
        try:
            start_time = time.time()
            audio = recognizer.listen(source, timeout=timeout_duration)
            end_time = time.time()
            text = recognizer.recognize_google(audio)
            speaking_time = round(end_time - start_time, 2)
            return text, speaking_time
        except sr.UnknownValueError:
            return "Error: Could not understand speech", None
        except sr.RequestError:
            return "Error: Speech recognition service unavailable", None

# Function to provide feedback
def provide_feedback(actual_time, allowed_time):
    extra_time = actual_time - allowed_time
    if extra_time > 3:
        return f"⚠️ You took **{round(extra_time, 2)} extra seconds**. Try to be more concise."
    elif extra_time < -3:
        return "⚠️ You spoke too fast! Try to slow down for better clarity."
    else:
        return "✅ Your speaking speed is well-balanced!"

# Function to play speech using gTTS
def pronounce_speech(text):
    if text:
        tts = gTTS(text=text, lang='en')
        tts.save("speech.mp3")
        os.system("start speech.mp3")  # Windows
        # os.system("mpg321 speech.mp3")  # Linux/macOS
        st.session_state.last_pronounced = text  # Store last pronounced speech

# Function to run the practice session
def run_speaking_practice(num_sentences):
    st.session_state.sentences = []
    
    for i in range(num_sentences):
        sentence = generate_sentence()
        emotion = detect_emotion(sentence)
        allowed_time = calculate_speaking_time(sentence)

        st.session_state.sentences.append((sentence, emotion, allowed_time))

# UI starts here
st.title("🗣️ Speech Training & Emotion Recognition App")

num_sentences = st.number_input("Enter the number of sentences to practice (Max 50):", min_value=1, max_value=50, value=3)

if st.button("Start Practice Session"):
    run_speaking_practice(num_sentences)

for idx, (sentence, emotion, allowed_time) in enumerate(st.session_state.sentences):
    st.subheader(f"Sentence {idx+1}/{len(st.session_state.sentences)}")
    st.write(f"**Sentence:** {sentence}")
    st.write(f"**Emotion to convey:** {emotion}")
    st.write(f"⏳ **You have {round(allowed_time, 2)} seconds to read this aloud.**")

    if st.button(f"🔊 Pronounce Sentence {idx+1}", key=f"pronounce_{idx}"):
        pronounce_speech(sentence)

    user_speech, actual_time = recognize_speech(allowed_time)

    st.write(f"✅ **You said:** {user_speech}")
    if actual_time:
        st.write(f"⏱ **Time Taken:** {actual_time} seconds")
        feedback = provide_feedback(actual_time, allowed_time)
        st.write(f"📢 **Feedback:** {feedback}")

    st.write("---")  # Divider between sentences
