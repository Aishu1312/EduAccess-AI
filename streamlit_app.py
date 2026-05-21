import streamlit as st
from gtts import gTTS
import speech_recognition as sr

st.set_page_config(page_title="EduAccess AI", layout="wide")

st.title("🚀 EduAccess AI")
st.subheader("Inclusive Intelligent Learning Platform")

# Sidebar
st.sidebar.title("Features")
feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Home",
        "AI Notes Summarizer",
        "Speech-to-Text",
        "Dyslexia-Friendly Mode",
        "Quiz Generator"
    ]
)

# HOME
if feature == "Home":
    st.header("Welcome to EduAccess AI")
    st.write("""
    AI-powered accessibility platform designed for inclusive learning.
    """)

# SUMMARIZER
elif feature == "AI Notes Summarizer":
    st.header("🧠 AI Notes Summarizer")

    text = st.text_area("Paste Notes Here")

    if st.button("Summarize"):
        summary = text[:300] + "..."
        st.success("Summary Generated")
        st.write(summary)

# SPEECH TO TEXT
elif feature == "Speech-to-Text":
    st.header("🎤 Speech-to-Text")

    st.write("Speech recognition feature placeholder")

# DYSLEXIA MODE
elif feature == "Dyslexia-Friendly Mode":
    st.header("📖 Dyslexia-Friendly Reading")

    st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        line-height:2;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p class="big-font">This is a dyslexia-friendly reading mode example.</p>',
        unsafe_allow_html=True
    )

# QUIZ GENERATOR
elif feature == "Quiz Generator":
    st.header("❓ AI Quiz Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):
        st.write("1. What is AI?")
        st.write("2. Define NLP.")
        st.write("3. Explain accessibility.")
