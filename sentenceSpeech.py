import time
import requests
import speech_recognition as sr
import nltk
import wikipedia
import random

# Download necessary NLTK data
nltk.download('punkt')

# Function to fetch a random sentence from Wikipedia
def get_random_sentence():
    while True:
        try:
            random_title = wikipedia.random()
            summary = wikipedia.summary(random_title, sentences=5)
            sentences = nltk.tokenize.sent_tokenize(summary)
            return random.choice(sentences)
        except Exception:
            continue  # Try again if an error occurs

# Function to calculate speaking time (max 15 sec)
def calculate_speaking_time(sentence):
    words = nltk.word_tokenize(sentence)
    avg_read_speed = 3  # Words per second
    return min(len(words) / avg_read_speed, 15)

# Function to recognize speech
def recognize_speech(timeout_duration):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak Now...")
        try:
            start_time = time.time()
            audio = recognizer.listen(source, timeout=timeout_duration)
            end_time = time.time()
            text = recognizer.recognize_google(audio)
            return text, end_time - start_time
        except sr.UnknownValueError:
            return "Error: Could not understand speech", None
        except sr.RequestError:
            return "Error: Speech recognition service unavailable", None

# Main function to run speaking practice
def run_speaking_practice(num_sentences):
    for i in range(num_sentences):
        sentence = get_random_sentence()
        allowed_time = calculate_speaking_time(sentence)

        print(f"\n🔹 Sentence {i+1}: {sentence}")
        print(f"⏳ You have {round(allowed_time, 2)} seconds to read this.")

        user_speech, time_taken = recognize_speech(allowed_time)

        if "Error" in user_speech:
            print(f"❌ {user_speech}")
        else:
            print(f"✅ You said: {user_speech}")
            print(f"⏳ Time taken: {round(time_taken, 2)} sec")

            # Calculate accuracy
            correct_words = set(nltk.word_tokenize(sentence.lower()))
            spoken_words = set(nltk.word_tokenize(user_speech.lower()))
            accuracy = (len(correct_words & spoken_words) / len(correct_words)) * 100

            # Speed Analysis
            speed = len(spoken_words) / time_taken  # Words per second
            normal_speed = len(correct_words) / allowed_time  # Ideal words per second

            if speed > normal_speed * 1.3:
                print("⚠️ You are speaking too fast! Try to slow down.")
            elif speed < normal_speed * 0.7:
                print("⚠️ You are speaking too slowly! Try to speak more fluently.")
            else:
                print("✅ Your speaking speed is balanced.")

            # Extra time analysis
            extra_time = time_taken - allowed_time
            if extra_time > 0:
                print(f"⏳ You took {round(extra_time, 2)} seconds extra.")

            print(f"🎯 Accuracy: {round(accuracy, 2)}%")
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
