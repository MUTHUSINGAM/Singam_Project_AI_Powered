import streamlit as st
import subprocess

def run_script(script_name):
    """Run a selected Python script."""
    try:
        process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            st.write(line)
        for err in process.stderr:
            st.error(err)
    except Exception as e:
        st.error(f"Error running script: {e}")

# Streamlit UI
def main():
    st.title("🗣️ Speech Training & Gamified Learning App")
    
    st.header("Select a Phase")
    phase = st.radio("Choose a phase:", ["Training Phase", "Gamified Phase"])
    
    if phase == "Training Phase":
        st.subheader("Training Modules")
        option = st.selectbox("Choose a training module:", ["Fluency Practice", "Emotion-Based Speaking"])
        
        if st.button("Start Training"):
            if option == "Fluency Practice":
                run_script("speechPractice.py")  # Runs speechPractice.py
            elif option == "Emotion-Based Speaking":
                run_script("EmotionSpeech.py")  # Runs EmotionSpeech.py
    
    elif phase == "Gamified Phase":
        st.subheader("Gamified Learning Modules")
        option = st.selectbox("Choose a game:", ["Single Word Spark", "Sentence Speech Challenge"])
        
        if st.button("Start Game"):
            if option == "Single Word Spark":
                run_script("project.py")  # Runs project.py
            elif option == "Sentence Speech Challenge":
                run_script("sentenceSpeech.py")  # Runs sentenceSpeech.py

if __name__ == "__main__":
    main()
