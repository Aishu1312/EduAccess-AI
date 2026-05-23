import streamlit as st
import tempfile
import random
import speech_recognition as sr
from googletrans import Translator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "q_no" not in st.session_state:
    st.session_state.q_no = 1

if "used_q" not in st.session_state:
    st.session_state.used_q = []

# ---------------------------------------------------
# GOOGLE TRANSLATOR
# ---------------------------------------------------

translator = Translator()

# ---------------------------------------------------
# 28 LANGUAGE SUPPORT
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

# ---------------------------------------------------
# LANGUAGE SELECTOR
# ---------------------------------------------------

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

target_lang = LANGUAGES[selected_language]

# ---------------------------------------------------
# UI TEXT
# ---------------------------------------------------

base_text = {
    "title": "🚀 EduAccess AI",
    "subtitle": "AI-Powered Accessibility Platform",
    "choose_feature": "Choose Feature",
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech Assistant",
    "dyslexia": "📖 Dyslexia Mode",
    "quiz": "❓ Quiz Generator",
    "accessibility": "♿ Accessibility Support",
    "welcome": "Welcome to EduAccess AI",
    "future": "🚀 Future Scope"
}

lang = {}

for key, value in base_text.items():

    try:
        lang[key] = translator.translate(
            value,
            dest=target_lang
        ).text

    except:
        lang[key] = value

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙ Settings")

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
# ACCESSIBILITY SETTINGS
# ---------------------------------------------------

st.sidebar.markdown("---")

font_size = st.sidebar.slider(
    "🔠 Font Size",
    16,
    40,
    22
)

high_contrast = st.sidebar.checkbox(
    "🌗 High Contrast Mode"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

if high_contrast:

    st.markdown("""
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == lang["home"]:

    st.title(lang["title"])

    st.subheader(lang["subtitle"])

    st.success(lang["welcome"])

    st.markdown("---")

    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)

    with col1:

        st.info("🧠 AI Notes Summarizer")
        st.write(
            "Generate AI-powered educational summaries."
        )

        st.success("🎤 Speech Assistant")
        st.write(
            "Convert speech into text with AI."
        )

    with col2:

        st.warning("📖 Dyslexia Reading Mode")
        st.write(
            "Accessibility-focused reading support."
        )

        st.error("❓ Smart Quiz Generator")
        st.write(
            "Generate intelligent quiz questions."
        )

    st.markdown("---")

    st.header("♿ Accessibility Features")

    features = [
        "👁️ Blind Support → Audio + Screen Reader",
        "👂 Deaf Support → Text Interface",
        "🗣️ Speech Assistance",
        "📖 Dyslexia-Friendly Reading",
        "🌍 28-Language Support",
        "🔠 Adjustable Font Size",
        "🌗 High Contrast Mode"
    ]

    for item in features:

        try:
            translated = translator.translate(
                item,
                dest=target_lang
            ).text

            st.write(translated)

        except:
            st.write(item)

    st.markdown("---")

    st.header(lang["future"])

    future = [
        "🔹 Real-Time Sign Language Recognition",
        "🔹 AI Career Guidance",
        "🔹 Personalized AI Tutor",
        "🔹 Emotion-Aware Learning",
        "🔹 Offline Learning Support"
    ]

    for item in future:

        try:
            translated = translator.translate(
                item,
                dest=target_lang
            ).text

            st.write(translated)

        except:
            st.write(item)

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    sample_text = """
Artificial Intelligence is transforming education
through accessibility and smart learning systems.
"""

    text = st.text_area(
        "📌 Paste Notes Here",
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        "📏 Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button("🚀 Generate Summary"):

        sentences = [
            s.strip()
            for s in text.split('.')
            if s.strip()
        ]

        if summary_length == "Short":
            num = max(2, len(sentences)//4)

        elif summary_length == "Medium":
            num = max(4, len(sentences)//2)

        else:
            num = len(sentences)

        summary = ". ".join(sentences[:num]) + "."

        try:
            summary = translator.translate(
                summary,
                dest=target_lang
            ).text

        except:
            pass

        st.session_state.summary = summary

        st.success("✅ Summary Generated")

        st.markdown(f"""
        <div style="
            background-color:#14532d;
            padding:20px;
            border-radius:12px;
            color:white;
            font-size:{font_size}px;
            line-height:2;
        ">
        {summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# SPEECH ASSISTANT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header("🎤 AI Voice Assistant")

    audio = st.audio_input("🎙️ Record Voice")

    uploaded_file = st.file_uploader(
        "📂 Upload Audio",
        type=["wav", "mp3", "m4a"]
    )

    source = audio if audio else uploaded_file

    if source:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp:

            tmp.write(source.read())
            audio_path = tmp.name

        recognizer = sr.Recognizer()

        try:

            with sr.AudioFile(audio_path) as src:

                audio_data = recognizer.record(src)

                text = recognizer.recognize_google(
                    audio_data
                )

            st.subheader("📝 Your Question")
            st.write(text)

        except:

            text = ""

            st.error(
                "❌ Could not understand audio."
            )

        if text:

            st.subheader("🤖 AI Response")

            if "ai" in text.lower():

                answer = """
Artificial Intelligence enables machines to think and learn like humans.

Examples:
- ChatGPT
- Self-driving cars
- Alexa
"""

            elif "education" in text.lower():

                answer = """
AI improves education through:
- Personalized learning
- Accessibility tools
- Smart tutoring systems
"""

            else:

                answer = f"""
Your Question:
{text}

This is an educational AI assistant.
Try asking about:
- AI
- Machine Learning
- Education
"""

            try:

                answer = translator.translate(
                    answer,
                    dest=target_lang
                ).text

            except:
                pass

            st.success(answer)

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia-Friendly Reading")

    display_text = st.session_state.summary

    if not display_text:

        st.warning(
            "⚠️ Generate summary first."
        )

    else:

        st.markdown(f"""
        <div style="
            font-size:{font_size}px;
            line-height:2.5;
            letter-spacing:2px;
            background-color:#f4f4f4;
            padding:25px;
            border-radius:15px;
            color:black;
        ">
        {display_text}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header("🎯 Smart AI Quiz")

    name = st.text_input("👤 Enter Name")

    topic = st.text_input("📘 Enter Topic")

    def generate_question(topic):

        questions = [

            f"What is the purpose of {topic}?",

            f"Why is {topic} important?",

            f"What is an application of {topic}?",

            f"Which industry uses {topic}?"
        ]

        q_text = random.choice(questions)

        correct = f"{topic} improves intelligent automation"

        options = [
            correct,
            f"{topic} removes all human jobs",
            f"{topic} has no practical use",
            f"{topic} works only offline"
        ]

        random.shuffle(options)

        return q_text, options, correct

    if st.button("🚀 Start Quiz"):

        st.session_state.started = True
        st.session_state.q_no = 1
        st.session_state.score = 0

    if st.session_state.started:

        if st.session_state.q_no > 10:

            st.success(
                f"🏆 Final Score: {st.session_state.score}/10"
            )

            st.session_state.started = False

            st.stop()

        q_text, options, correct = generate_question(topic)

        st.subheader(
            f"Question {st.session_state.q_no}/10"
        )

        st.write(q_text)

        selected = st.radio(
            "Choose Answer",
            options
        )

        if st.button("✅ Submit"):

            if selected == correct:

                st.success("✅ Correct")

                st.session_state.score += 1

            else:

                st.error("❌ Wrong")

                st.write(
                    f"Correct Answer: {correct}"
                )

            st.session_state.q_no += 1

            st.rerun()

        st.progress(
            st.session_state.q_no / 10
        )

        st.write(
            f"📊 Score: {st.session_state.score}"
        )

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    accessibility_features = [

        "👁️ Blind → Audio Support",

        "👂 Deaf → Text Interface",

        "🗣️ Speech Impaired → Text Input",

        "🦽 Mobility Support → Large UI",

        "📖 Dyslexia-Friendly Reading",

        "🌍 28 Language Translation",

        "🔠 Adjustable Fonts"
    ]

    for item in accessibility_features:

        try:

            translated = translator.translate(
                item,
                dest=target_lang
            ).text

            st.write(translated)

        except:
            st.write(item)
