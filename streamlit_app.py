import streamlit as st
import time
import openai
import tempfile
import json

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="EduAccess AI", page_icon="🚀", layout="wide")

# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []

# ---------------------------------------------------
# TRANSLATIONS (same as yours)
# ---------------------------------------------------

from googletrans import Translator

translator = Translator()

# ---------------------------------------------------
# MULTILINGUAL SUPPORT
# ---------------------------------------------------

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Turkish": "tr",
    "Thai": "th",
    "Indonesian": "id"
}

# ----------------------------
# LANGUAGE SELECTOR
# ----------------------------

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

target_lang = LANGUAGES[selected_language]

# ---------------------------------------------------
# DEFAULT ENGLISH TEXT
# ---------------------------------------------------

base_text = {
    "title": "🚀 EduAccess AI",
    "subtitle": "AI-Powered Accessibility Platform",
    "choose_feature": "Choose Feature",
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech-to-Text",
    "dyslexia": "📖 Dyslexia Mode",
    "quiz": "❓ Quiz Generator",
    "accessibility": "♿ Accessibility Support",
    "summary_button": "Generate Summary",
    "welcome": "Welcome to EduAccess AI",
    "core_features": "🌟 Core Features",
    "future_scope": "🚀 Future Scope"
}

# ---------------------------------------------------
# AUTO TRANSLATE UI
# ---------------------------------------------------

lang = {}

for key, value in base_text.items():

    try:
        translated = translator.translate(
            value,
            dest=target_lang
        ).text

        lang[key] = translated

    except:
        lang[key] = value

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Urdu": "ur",
    "Odia": "or",
    "Assamese": "as",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Turkish": "tr",
    "Thai": "th",
    "Indonesian": "id"
}

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

target_lang = LANGUAGES[selected_language]

feature = st.sidebar.selectbox(
    lang["choose_feature"],
    [
        lang["home"],
        lang["summarizer"],
        lang["speech"],
        lang["dyslexia"],
        lang["quiz"],
        lang["accessibility"]
    ]
)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == lang["home"]:

    st.title(lang["title"])

    st.subheader(lang["subtitle"])

    st.write(lang.get("welcome", "Welcome to EduAccess AI"))

    st.markdown("---")

    st.header(lang.get("core_features", "🌟 Core Features"))

    col1, col2 = st.columns(2)

    with col1:

        st.info("🧠 AI Notes Summarizer")
        st.write("Generate concise AI-powered summaries from educational notes.")

        st.success("🎤 Speech-to-Text")
        st.write("Convert spoken language into text using AI.")

    with col2:

        st.warning("📖 Dyslexia-Friendly Reading")
        st.write("Improve readability using accessibility-focused UI.")

        st.error("❓ AI Quiz Generator")
        st.write("Generate exam-based AI quiz questions.")

    st.markdown("---")

    st.header("♿ Accessibility Support")

    st.write("✅ Dyslexia Support")
    st.write("✅ Speech Assistance")
    st.write("✅ Large Readable Fonts")
    st.write("✅ AI Learning Assistance")
    st.write("✅ Multilingual Support")

    st.markdown("---")

    st.header(lang.get("future_scope", "🚀 Future Scope"))

    st.write(lang.get("future1", "🔹 Real-Time Sign Language Recognition"))
    st.write(lang.get("future2", "🔹 AI Career Guidance"))
    st.write(lang.get("future3", "🔹 Emotion-Aware Learning"))
    st.write(lang.get("future4", "🔹 Personalized AI Tutor"))
    st.write(lang.get("future5", "🔹 Multilingual Accessibility Support"))

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    sample_text = """Artificial Intelligence is transforming education through accessibility and smart learning systems."""

    text = st.text_area(
        "📌 Paste Notes Here",
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button("Generate Summary"):

        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if summary_length == "Short":
            num = max(2, len(sentences)//4)
        elif summary_length == "Medium":
            num = max(4, len(sentences)//2)
        else:
            num = len(sentences)

        summary = ". ".join(sentences[:num]) + "."

        # ✅ store summary globally
        st.session_state["summary"] = summary

        st.success("✅ Summary Generated")

        st.markdown(f"""
        <div style="
            background-color:#14532d;
            padding:15px;
            border-radius:10px;
            color:white;
        ">
        {summary}
        </div>
        """, unsafe_allow_html=True)
    
# ---------------------------------------------------
# SPEECH TO TEXT + AI ANSWER
# ---------------------------------------------------

elif feature == lang["speech"]:

    import speech_recognition as sr
    import tempfile

    st.header("🎤 Voice Assistant (No API Required)")

    # 🎙️ MIC INPUT
    audio = st.audio_input("🎙️ Record Voice")

    # 📂 FILE UPLOAD (ADDED ✅)
    uploaded_file = st.file_uploader("📂 Upload Audio", type=["wav", "mp3", "m4a"])

    source = audio if audio else uploaded_file

    if source:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(source.read())
            audio_path = tmp.name

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_path) as src:
                audio_data = recognizer.record(src)
                text = recognizer.recognize_google(audio_data)

            st.subheader("📝 Your Question")
            st.write(text)

        except:
            text = ""
            st.error("❌ Could not understand audio. Speak clearly.")

        # 🤖 DETAILED AI ANSWER (NO API)
        if text:

            st.subheader("🤖 AI Answer")

            text_lower = text.lower()

            if "ai" in text_lower:
                st.success("""
Artificial Intelligence (AI) refers to machines that can mimic human intelligence.

👉 Example:
- Chatbots like ChatGPT
- Self-driving cars

👉 Real Life Use:
- Healthcare diagnosis
- Smart assistants like Alexa
""")

            elif "machine learning" in text_lower:
                st.success("""
Machine Learning is a part of AI where systems learn from data.

👉 Example:
- Netflix recommendations
- Spam email detection

👉 How it works:
System learns patterns from past data and predicts future outcomes.
""")

            elif "education" in text_lower:
                st.success("""
AI is transforming education by making learning personalized and accessible.

👉 Example:
- AI tutors
- Voice-based learning for blind students

👉 Benefits:
- Learn anytime
- Learn at your own pace
""")

            else:
                st.success(f"""
Your Question: {text}

👉 Explanation:
This is an intelligent response system. Based on your query, here's a simple explanation:

- The topic relates to general knowledge or academics
- Try asking about AI, ML, Science, or Education

👉 Example:
Ask: "What is AI?" or "Explain Machine Learning"
""")
            
# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia-Friendly Reading Mode")

    font_size = st.slider("Adjust Font Size", 20, 40, 30)

    display_text = st.session_state.get("summary", "")

    if not display_text:
        st.warning("⚠️ Generate summary first in Summarizer section")

    else:
        st.markdown(f"""
        <div style="
            font-size: {font_size}px;
            line-height: 2.5;
            letter-spacing: 2px;
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            color: black;
        ">
        {display_text}
        </div>
        """, unsafe_allow_html=True)
        
# ---------------------------------------------------
# QUIZ (KAHOOT STYLE + TIMER + LEADERBOARD)
# ---------------------------------------------------
elif feature == lang["quiz"]:

    import random
    import speech_recognition as sr
    import tempfile

    st.header("🎯 KBC Style Smart Quiz (No Repeat)")

    name = st.text_input("👤 Enter Your Name")
    topic = st.text_input("📘 Enter Topic")

    # SESSION
    if "started" not in st.session_state:
        st.session_state.started = False
    if "q_no" not in st.session_state:
        st.session_state.q_no = 1
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "used_q" not in st.session_state:
        st.session_state.used_q = []

    # ---------------------------
    # LARGE QUESTION BANK (DYNAMIC)
    # ---------------------------
    def generate_question(topic):

        question_types = [

            f"What is the primary purpose of {topic}?",
            f"Which of the following best defines {topic}?",
            f"How is {topic} used in real-world applications?",
            f"What makes {topic} important in modern systems?",
            f"Which scenario is an example of {topic}?",
            f"What is a limitation of {topic}?",
            f"How does {topic} improve efficiency?",
            f"Which field benefits the most from {topic}?",
            f"What distinguishes {topic} from traditional approaches?",
            f"Why is {topic} widely adopted today?",
            f"What is a key component of {topic}?",
            f"What problem does {topic} solve?",
            f"Which statement about {topic} is correct?",
            f"What happens when {topic} is applied?",
            f"What is the future scope of {topic}?",
            f"Which industry uses {topic} the most?",
            f"What is the role of data in {topic}?",
            f"How does {topic} impact decision making?",
            f"What is a real-life example of {topic}?",
            f"What is the biggest advantage of {topic}?"
        ]

        # REMOVE USED QUESTIONS
        remaining = list(set(question_types) - set(st.session_state.used_q))

        if not remaining:
            st.session_state.used_q = []
            remaining = question_types

        q_text = random.choice(remaining)
        st.session_state.used_q.append(q_text)

        # SMART OPTIONS (CONFUSING)
        correct = f"{topic} enables intelligent and automated decision-making"

        distractors = [
            f"{topic} works only manually without automation",
            f"{topic} has no practical real-world use",
            f"{topic} completely replaces human intelligence"
        ]

        options = [correct] + distractors
        random.shuffle(options)

        return q_text, options, correct

    # ---------------------------
    # START QUIZ
    # ---------------------------
    if st.button("🚀 Start Quiz") and topic and name:

        st.session_state.started = True
        st.session_state.q_no = 1
        st.session_state.score = 0
        st.session_state.used_q = []

    # ---------------------------
    # QUIZ FLOW
    # ---------------------------
    if st.session_state.started:

        if st.session_state.q_no > 15:
            st.success(f"🏆 Final Score: {st.session_state.score}/15")
            st.session_state.started = False
            st.stop()

        q_text, options, correct = generate_question(topic)

        st.markdown(f"### 🎤 Question {st.session_state.q_no}/20")
        st.subheader(q_text)

        selected = st.radio("Choose Answer", options)

        # 🎙️ VOICE
        st.markdown("🎙️ Speak Answer (Optional)")
        audio = st.audio_input("Record")

        spoken = ""

        if audio:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(audio.read())
                path = tmp.name

            r = sr.Recognizer()

            try:
                with sr.AudioFile(path) as source:
                    data = r.record(source)
                    spoken = r.recognize_google(data)

                st.info(f"🗣️ You said: {spoken}")

            except:
                st.warning("Voice not clear")

        # SUBMIT
        if st.button("✅ Submit"):

            final = selected

            for opt in options:
                if opt.lower() in spoken.lower():
                    final = opt

            if final == correct:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error("❌ Wrong")
                st.write(f"✔ Correct: {correct}")

            st.session_state.q_no += 1
            st.rerun()

        # PROGRESS
        st.progress(st.session_state.q_no / 15)
        st.write(f"📊 Score: {st.session_state.score}")
            
# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("👁️ Blind → Audio + screen reader")
    st.write("👂 Deaf → Text UI")
    st.write("🗣️ Speech impaired → Text input")
    st.write("🦽 Mobility → Large UI")
