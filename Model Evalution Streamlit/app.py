import streamlit as st

# Define pages
fluency_practice = st.Page("pages/fluency_practice.py", title="Fluency Practice", icon="🗣️")
emotion_based_speaking = st.Page("pages/emotion_based_speaking.py", title="Emotion-Based Speaking", icon="🎭")
single_word_spark = st.Page("pages/single_word_spark.py", title="Single Word Spark", icon="💡")
sentence_speech_challenge = st.Page("pages/sentence_speech_challenge.py", title="Sentence Speech Challenge", icon="📝")

# Configure navigation
pg = st.navigation([
    fluency_practice,
    emotion_based_speaking,
    single_word_spark,
    sentence_speech_challenge
])

# Set global page configuration
st.set_page_config(page_title="Speech Training & Gamified Learning App", page_icon="🎓")

# Run the selected page
pg.run()
