import time
import nltk
import speech_recognition as sr
from textblob import TextBlob
import random

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('gutenberg')

# Load a dataset from NLTK to generate sentences dynamically
from nltk.corpus import gutenberg
words = list(gutenberg.words('austen-emma.txt'))  # Using Jane Austen's "Emma" novel for sentence generation

# Function to generate a dynamic sentence
def generate_sentence():
    sentence_length = random.randint(8, 15)  # Random length between 8-15 words
    sentence = " ".join(random.sample(words, sentence_length)) + "."
    sentence = sentence.capitalize()  # Ensure it starts with a capital letter
    emotion = detect_emotion(sentence)
    return sentence, emotion

# Function to determine emotion based on sentence meaning
def detect_emotion(sentence):
    analysis = TextBlob(sentence).sentiment.polarity  # Sentiment score (-1 to 1)

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

# Function to calculate the ideal speaking time based on sentence length
def calculate_speaking_time(sentence):
    words = nltk.word_tokenize(sentence)
    avg_read_speed = 3  # Average 3 words per second
    return min(len(words) / avg_read_speed, 15)  # Max limit of 15 sec per sentence

# Function to recognize user speech
def recognize_speech(timeout_duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak Now...")
        try:
            audio = recognizer.listen(source, timeout=timeout_duration)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Error: Could not understand speech"
        except sr.RequestError:
            return "Error: Speech recognition service unavailable"

# Main function to run speaking practice
def run_speaking_practice(num_sentences):
    for i in range(num_sentences):
        sentence, emotion = generate_sentence()
        allowed_time = calculate_speaking_time(sentence)

        print(f"\n🔹 Sentence {i+1}: {sentence}")
        print(f"🎭 Read this with **{emotion}** emotion.")
        print(f"⏳ You have {round(allowed_time, 2)} seconds to read this.")

        user_speech = recognize_speech(allowed_time)

        print(f"✅ You said: {user_speech}")
        print("-" * 50)

# Get user input with validation
while True:
    try:
        num_sentences = int(input("Enter the number of sentences to practice (Max 50): "))
        if num_sentences > 50:
            print("⚠️ Maximum allowed sentences are 50. Please enter a valid number.")
            continue
        break
    except ValueError:
        print("⚠️ Invalid input! Please enter a valid number.")

# Run the practice session
run_speaking_practice(num_sentences)
