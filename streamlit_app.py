import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- LANGUAGE SYSTEM ---------------- #

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
    "Arabic": "ar"
}

st.sidebar.title("🌐 Language Settings")
selected_language = st.sidebar.selectbox("Choose Language", list(languages.keys()))
lang_code = languages[selected_language]

def tr(text):
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# ---------------- ACCESSIBILITY SETTINGS ---------------- #

st.sidebar.title("♿ Accessibility")

font_size = st.sidebar.slider("Font Size", 14, 30, 18)

high_contrast = st.sidebar.checkbox("High Contrast Mode")

# ---------------- STYLING ---------------- #

bg_color = "#000000" if high_contrast else "#050816"
text_color = "#FFFFFF" if high_contrast else "#E5E7EB"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
    font-size: {font_size}px;
}}

.feature-box {{
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    background: linear-gradient(90deg,#1e3a8a,#0f172a);
}}

</style>
""", unsafe_allow_html=True)

# ---------------- TEXT TO SPEECH ---------------- #

def speak(text):
    tts = gTTS(text=text, lang=lang_code)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

# ---------------- HEADER ---------------- #

st.title(tr("🚀 EduAccess AI"))
st.subheader(tr("AI Platform for Divyang and All Students"))

st.write(tr(
    "This platform helps students learn using AI with full accessibility support for visually impaired, hearing impaired, speech impaired, and mobility-impaired users."
))

st.divider()

# ---------------- CORE FEATURES ---------------- #

st.header(tr("✨ Core Features"))

col1, col2 = st.columns(2)

features = [
    ("📘 AI Notes Summarizer", "Generate short summaries from notes"),
    ("🎤 Speech to Text (Upload Audio)", "Convert uploaded audio into text"),
    ("🔊 Text to Speech", "Listen to study content"),
    ("📖 Dyslexia Friendly UI", "Easy reading design"),
    ("❓ AI Quiz Generator", "Auto generate quiz"),
    ("🌍 Full Language Translation", "Translate everything instantly")
]

for i, (title, desc) in enumerate(features):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
        <div class="feature-box">
        <b>{tr(title)}</b><br><br>
        {tr(desc)}
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------------- ACCESSIBILITY ---------------- #

st.header(tr("♿ Accessibility Support"))

st.write(tr("Designed for ALL Divyang users:"))

st.markdown(f"""
- 👁️ {tr("For Blind: Text-to-Speech, screen reader friendly")}
- 👂 {tr("For Deaf: Full text-based interface")}
- 🗣️ {tr("For Speech Impairment: Text input instead of voice")}
- 🦽 {tr("For Mobility Issues: Keyboard-free large UI")}
- 🧠 {tr("For Learning Disabilities: Simple UI + summaries")}
""")

st.divider()

# ---------------- TEXT TO SPEECH ---------------- #

st.header(tr("🔊 Text to Speech"))

text_input = st.text_area(tr("Enter text"))

if st.button(tr("Convert to Speech")):
    if text_input:
        audio_file = speak(text_input)
        st.audio(audio_file)

st.divider()

# ---------------- AUDIO TO TEXT (UPLOAD BASED) ---------------- #

st.header(tr("🎤 Audio to Text"))

uploaded_file = st.file_uploader(tr("Upload audio file"), type=["wav", "mp3"])

if uploaded_file:
    st.success(tr("Audio uploaded successfully"))
    st.audio(uploaded_file)

    st.info(tr("Speech-to-text feature can be integrated using Whisper API (advanced feature)"))

st.divider()

# ---------------- FUTURE FEATURES ---------------- #

st.header(tr("🚀 Future Scope"))

future = [
    "Sign Language Recognition",
    "AI Personal Tutor",
    "Emotion-Based Learning",
    "Career Guidance AI",
    "Offline Mode"
]

for f in future:
    st.write("🔹", tr(f))

# ---------------- FOOTER ---------------- #

st.divider()

st.success(tr(
    "EduAccess AI ensures inclusive education for every student using advanced AI and accessibility tools."
))
