import streamlit as st
import tempfile
import random
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 10px;
}

.stButton > button {
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    width: 100%;
}

.feature-card {
    padding: 22px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
    transition: 0.3s;
}

.feature-card:hover {
    transform: scale(1.02);
}

.footer {
    text-align:center;
    padding:20px;
    color:gray;
    font-size:14px;
}

.chat-popup {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 340px;
    background: white;
    padding: 20px;
    border-radius: 20px;
    z-index: 9999;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
}

.chat-title {
    color: #2563eb;
    font-size: 24px;
    font-weight: bold;
}

.chat-text {
    color: black;
    line-height: 1.7;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LANGUAGE SUPPORT
# ---------------------------------------------------

LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Urdu": "ur-PK",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Japanese": "ja-JP"
}

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

target_lang = LANGUAGES[selected_language]

# ---------------------------------------------------
# TRANSLATION FUNCTION
# ---------------------------------------------------

def translate_text(text):

    try:

        short_lang = target_lang.split("-")[0]

        return GoogleTranslator(
            source='auto',
            target=short_lang
        ).translate(text)

    except:

        return text

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

session_defaults = {

    "summary": "",
    "quiz_started": False,
    "quiz_score": 0,
    "quiz_data": [],
    "quiz_history": [],
    "summary_history": [],
    "speech_history": [],
    "show_chat": False
}

for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙️ Settings")

font_size = st.sidebar.slider(
    "🔠 Font Size",
    16,
    40,
    22
)

high_contrast = st.sidebar.checkbox(
    "🌗 High Contrast Mode"
)

feature = st.sidebar.selectbox(

    "Choose Feature",

    [
        "🏠 Home",
        "🧠 AI Notes Summarizer",
        "🎤 Speech-to-Text",
        "📖 Dyslexia-Friendly Reading",
        "❓ AI Quiz Generator",
        "♿ Accessibility Support",
        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor"
    ]
)

# ---------------------------------------------------
# HIGH CONTRAST
# ---------------------------------------------------

if high_contrast:

    st.markdown("""
    <style>
    .stApp {
        background-color:black;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == "🏠 Home":

    st.title("🚀 EduAccess AI")

    st.subheader(
        "AI-Powered Accessibility Platform for Students"
    )

    st.success(
        "Inclusive AI Learning Ecosystem"
    )

    st.markdown("---")

    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">

        <h2>🧠 AI Notes Summarizer</h2>

        <p>
        Generate concise AI-powered summaries from notes and PDFs.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#16a34a,#166534);">

        <h2>🎤 Speech-to-Text</h2>

        <p>
        Convert spoken language into text with multilingual support.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#f59e0b,#b45309);">

        <h2>📖 Dyslexia-Friendly Reading</h2>

        <p>
        Accessible reading mode with better spacing and readability.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">

        <h2>❓ AI Quiz Generator</h2>

        <p>
        Adaptive quizzes with Easy, Medium and Hard difficulty levels.
        </p>

        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == "🧠 AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    uploaded_file = st.file_uploader(
        "📂 Upload PDF",
        type=["pdf"]
    )

    text = ""

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

        st.success("✅ PDF Uploaded Successfully")

    manual_text = st.text_area(
        "📌 Paste Notes Here",
        height=250
    )

    if manual_text:

        text += manual_text

    summary_length = st.selectbox(

        "📏 Select Summary Length",

        ["Short", "Medium", "Detailed"]
    )

    if st.button("🚀 Generate Summary"):

        if text.strip() != "":

            sentences = [

                s.strip()

                for s in text.split(".")
                if s.strip()
            ]

            if summary_length == "Short":

                num = max(2, len(sentences)//4)

            elif summary_length == "Medium":

                num = max(4, len(sentences)//2)

            else:

                num = len(sentences)

            summary = ". ".join(sentences[:num]) + "."

            translated_summary = translate_text(summary)

            st.session_state.summary = translated_summary

            st.success("✅ Summary Generated")

            st.markdown(f"""
            <div style="
                background:#14532d;
                padding:20px;
                border-radius:15px;
                color:white;
                font-size:{font_size}px;
                line-height:2;
            ">
            {translated_summary}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.warning("⚠️ Enter Notes")

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    audio = st.audio_input(
        "🎙️ Record Voice"
    )

    if audio:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp:

            tmp.write(audio.read())

            audio_path = tmp.name

        recognizer = sr.Recognizer()

        try:

            with sr.AudioFile(audio_path) as source:

                audio_data = recognizer.record(source)

                text = recognizer.recognize_google(

                    audio_data,
                    language=target_lang
                )

            st.success("✅ Speech Recognized")

            st.write(text)

            st.audio(audio)

        except:

            st.error("❌ Could not understand audio")

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header("📖 Dyslexia-Friendly Reading")

    if st.session_state.summary == "":

        st.warning("⚠️ Generate summary first")

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
        {st.session_state.summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == "❓ AI Quiz Generator":

    st.header("❓ AI Adaptive Exam Quiz Generator")

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    if "submitted_questions" not in st.session_state:
        st.session_state.submitted_questions = set()

    topic = st.text_input("📘 Enter Topic")

    difficulty = st.selectbox(
        "🎯 Select Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    beginner_questions = [
        {
            "question": "What is Python?",
            "options": [
                "Programming Language",
                "Snake",
                "Browser",
                "Database"
            ],
            "answer": "Programming Language"
        }
    ]

    intermediate_questions = [
        {
            "question": "What is OOP?",
            "options": [
                "Object Oriented Programming",
                "Operating Output Program",
                "Open Office Project",
                "None"
            ],
            "answer": "Object Oriented Programming"
        }
    ]

    advanced_questions = [
        {
            "question": "Which algorithm is used in classification?",
            "options": [
                "Logistic Regression",
                "K-Means",
                "Apriori",
                "Linear Search"
            ],
            "answer": "Logistic Regression"
        }
    ]

    if difficulty == "Beginner":
        question_pool = beginner_questions

    elif difficulty == "Intermediate":
        question_pool = beginner_questions + intermediate_questions

    else:
        question_pool = (
            beginner_questions +
            intermediate_questions +
            advanced_questions
        )

    if st.button("🚀 Generate Quiz"):

        random.shuffle(question_pool)

        st.session_state.quiz_data = question_pool

        st.session_state.quiz_started = True

        st.session_state.quiz_score = 0

    if st.session_state.quiz_started:

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.subheader(
                f"Q{idx+1}. {q['question']}"
            )

            answer = st.radio(
                "Choose Answer",
                q["options"],
                key=f"q_{idx}"
            )

            if st.button(
                f"Submit Q{idx+1}",
                key=f"submit_{idx}"
            ):

                if answer == q["answer"]:

                    st.success("✅ Correct")

                    st.session_state.quiz_score += 2

                    st.balloons()

                else:

                    st.error("❌ Wrong")

                    st.info(
                        f"Correct Answer: {q['answer']}"
                    )

        st.header(
            f"🏆 Score: {st.session_state.quiz_score}"
        )

# ---------------------------------------------------
# ACCESSIBILITY SUPPORT
# ---------------------------------------------------

elif feature == "♿ Accessibility Support":

    st.header("♿ Accessibility Support")

    st.success("🌍 Multi-language Support")
    st.success("🔠 Adjustable Font Size")
    st.success("🌗 High Contrast Mode")
    st.success("📖 Dyslexia Reading")
    st.success("🎤 Speech Assistance")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">

Made with ❤️ using Streamlit | EduAccess AI

</div>
""", unsafe_allow_html=True)
```
