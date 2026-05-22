# streamlit_app.py

import streamlit as st
from googletrans import Translator
import speech_recognition as sr
from PIL import Image
import pyttsx3

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide",
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #050816;
    color: white;
    font-family: 'Arial';
}

/* Bigger fonts for low vision users */
.big-text {
    font-size: 22px !important;
    line-height: 1.8;
}

/* Feature Boxes */
.feature-box {
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

/* Accessibility */
.access-box {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
    background-color: #2563eb;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TRANSLATION SYSTEM ---------------- #

translator = Translator()

languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese": "zh-cn",
    "Japanese": "ja",
    "Russian": "ru",
    "Arabic": "ar"
}

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🌐 Language Settings")

selected_language = st.sidebar.selectbox(
    "Choose Dashboard Language",
    list(languages.keys())
)

lang_code = languages[selected_language]

theme = st.sidebar.selectbox(
    "🎨 Theme",
    ["Dark", "Light"]
)

# ---------------- TRANSLATE FUNCTION ---------------- #

def tr(text):
    try:
        return translator.translate(text, dest=lang_code).text
    except:
        return text

# ---------------- TEXT TO SPEECH ---------------- #

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# ---------------- HEADER ---------------- #

st.title(tr("🚀 EduAccess AI"))

st.subheader(
    tr("AI-Powered Learning Platform for Divyang and Normal Students")
)

st.write(
    tr(
        "EduAccess AI helps students learn better using Artificial Intelligence, NLP, accessibility tools, speech technologies, and inclusive education support."
    )
)

st.divider()

# ---------------- CORE FEATURES ---------------- #

st.header(tr("✨ Core Features"))

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#1e3a8a,#0f172a)">
    📘 {tr("AI Notes Summarizer")}
    <br><br>
    <span class='big-text'>
    {tr("Generate concise AI-powered summaries from educational notes.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#065f46,#0f172a)">
    🎤 {tr("Speech-to-Text")}
    <br><br>
    <span class='big-text'>
    {tr("Convert spoken language into text using AI.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#7c3aed,#0f172a)">
    🗣️ {tr("Text-to-Speech")}
    <br><br>
    <span class='big-text'>
    {tr("Read study material aloud for visually impaired students.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#854d0e,#0f172a)">
    📖 {tr("Dyslexia-Friendly Reading")}
    <br><br>
    <span class='big-text'>
    {tr("Improve readability using accessibility-focused UI.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#7f1d1d,#0f172a)">
    ❓ {tr("AI Quiz Generator")}
    <br><br>
    <span class='big-text'>
    {tr("Generate exam-based AI quiz questions instantly.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="feature-box" style="background:linear-gradient(90deg,#0f766e,#0f172a)">
    🌍 {tr("Real-Time Language Translation")}
    <br><br>
    <span class='big-text'>
    {tr("Translate all content into multiple global languages instantly.")}
    </span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- ACCESSIBILITY SUPPORT ---------------- #

st.header(tr("♿ Accessibility Support"))

st.markdown(f"""
<div class="access-box">

✅ {tr("Support for Blind / Visually Impaired Students")}  
<br><br>

✅ {tr("Speech Assistance for Students who Cannot Speak")}  
<br><br>

✅ {tr("AI Voice Navigation for Hands-Free Control")}  
<br><br>

✅ {tr("Keyboard-Free Learning Experience")}  
<br><br>

✅ {tr("Large Readable Fonts for Low Vision Students")}  
<br><br>

✅ {tr("Hearing-Impaired Friendly Text Communication")}  
<br><br>

✅ {tr("Support for Students with No Hands or Limited Mobility")}  
<br><br>

✅ {tr("Wheelchair-Friendly Digital Accessibility")}  
<br><br>

✅ {tr("AI-Based Learning Assistance for Cognitive Disabilities")}  
<br><br>

✅ {tr("Screen Reader Compatibility")}  
<br><br>

✅ {tr("Multilingual Learning Support")}  

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- VOICE INPUT ---------------- #

st.header(tr("🎤 Voice Input Demo"))

if st.button(tr("Start Voice Recognition")):

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            st.info(tr("Listening... Please speak now."))

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            st.success(tr("Recognized Speech:"))
            st.write(text)

    except:
        st.error(tr("Microphone not detected or speech could not be recognized."))

# ---------------- TEXT TO SPEECH ---------------- #

st.header(tr("🔊 Text To Speech"))

tts_text = st.text_area(
    tr("Enter text to read aloud")
)

if st.button(tr("Read Aloud")):

    if tts_text:
        speak_text(tts_text)
        st.success(tr("Reading completed."))

# ---------------- FUTURE FEATURES ---------------- #

st.divider()

st.header(tr("🚀 Future Possibilities"))

future_features = [
    "Real-time Sign Language Recognition",
    "AI Career Guidance",
    "Emotion-Based Learning Assistance",
    "Personalized AI Tutor",
    "Voice-Controlled Navigation",
    "Brain-Computer Interface Support",
    "AI-Based Exam Preparation",
    "Smart Attendance System",
    "AI Mental Health Support",
    "Offline Learning Support"
]

for feature in future_features:
    st.write("🔹", tr(feature))

# ---------------- FOOTER ---------------- #

st.divider()

st.success(
    tr(
        "EduAccess AI is designed to provide inclusive education for every student, including Divyang students, through Artificial Intelligence and accessibility technologies."
    )
)
