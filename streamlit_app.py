import streamlit as st
import tempfile
import random
import speech_recognition as sr
from deep_translator import GoogleTranslator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# LANGUAGE SUPPORT
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
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Turkish": "tr",
    "Thai": "th",
    "Indonesian": "id"
}

# ---------------------------------------------------
# SIDEBAR LANGUAGE
# ---------------------------------------------------

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
        return GoogleTranslator(
            source='auto',
            target=target_lang
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
    "answer_feedback": {},
    "quiz_history": [],
    "summary_history": [],
    "speech_history": []
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# UI TEXT
# ---------------------------------------------------

base_text = {
    "choose_feature": "Choose Feature",
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech-to-Text",
    "dyslexia": "📖 Dyslexia-Friendly Mode",
    "quiz": "❓ Quiz Generator",
    "accessibility": "♿ Accessibility Support",
    "assistant": "🤖 AI Assistant"
}

lang = {}

for key, value in base_text.items():
    lang[key] = translate_text(value)

# ---------------------------------------------------
# SIDEBAR SETTINGS
# ---------------------------------------------------

st.sidebar.title(
    translate_text("⚙️ Settings")
)

font_size = st.sidebar.slider(
    translate_text("🔠 Font Size"),
    16,
    40,
    22
)

high_contrast = st.sidebar.checkbox(
    translate_text("🌗 High Contrast Mode")
)

feature = st.sidebar.selectbox(
    lang["choose_feature"],
    [
        lang["home"],
        lang["summarizer"],
        lang["speech"],
        lang["dyslexia"],
        lang["quiz"],
        lang["accessibility"],
        lang["assistant"]
    ]
)

# ---------------------------------------------------
# HIGH CONTRAST MODE
# ---------------------------------------------------

if high_contrast:

    st.markdown(
        """
        <style>
        .stApp {
            background-color: black;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == lang["home"]:

    st.title(
        translate_text("🚀 EduAccess AI")
    )

    st.subheader(
        translate_text(
            "AI-Powered Accessibility Platform for Disabled Students"
        )
    )

    st.write(
        translate_text(
            """
EduAccess AI is an intelligent inclusive learning platform
designed to help students with disabilities learn more effectively
using Artificial Intelligence, NLP, speech technologies,
and accessibility-focused tools.
"""
        )
    )

    st.markdown("---")

    st.header(
        translate_text("🌟 Core Features")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            translate_text(
                "🧠 AI Notes Summarizer"
            )
        )

        st.write(
            translate_text(
                "Generate concise AI-powered summaries from long educational notes."
            )
        )

        st.success(
            translate_text(
                "🎤 Speech-to-Text"
            )
        )

        st.write(
            translate_text(
                "Convert spoken language into text for accessible learning."
            )
        )

    with col2:

        st.warning(
            translate_text(
                "📖 Dyslexia-Friendly Reading"
            )
        )

        st.write(
            translate_text(
                "Improve readability using accessible fonts and spacing."
            )
        )

        st.error(
            translate_text(
                "❓ AI Quiz Generator"
            )
        )

        st.write(
            translate_text(
                "Generate quizzes based on exams and topics."
            )
        )

    st.markdown("---")

    st.header(
        translate_text("♿ Accessibility Support")
    )

    accessibility_features = [
        "✅ Dyslexia Support",
        "✅ Speech Impairment Support",
        "✅ Reading Assistance",
        "✅ High Contrast Mode",
        "✅ 28 Language Support",
        "✅ Adjustable Font Sizes"
    ]

    for item in accessibility_features:
        st.write(
            translate_text(item)
        )

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header(
        translate_text("🧠 AI Notes Summarizer")
    )

    text = st.text_area(
        translate_text("📌 Paste Notes Here"),
        height=250
    )

    summary_length = st.selectbox(
        translate_text("📏 Select Summary Length"),
        ["Short", "Medium", "Detailed"]
    )

    if st.button(
        translate_text("🚀 Generate Summary")
    ):

        if text:

            sentences = [
                s.strip() for s in text.split(".") if s.strip()
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

            st.session_state.summary_history.append(
                translated_summary
            )

            st.success(
                translate_text("✅ Summary Generated Successfully")
            )

            st.markdown(f"""
            <div style="
                background-color:#14532d;
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

            st.warning(
                translate_text("⚠️ Please enter notes")
            )

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    st.write(
        translate_text(
            "Convert your voice into text using AI."
        )
    )

    audio = st.audio_input(
        translate_text("🎙️ Record Your Voice")
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

            st.success(
                translate_text("✅ Speech Recognized")
            )

            st.subheader(
                translate_text("📝 Recognized Text")
            )

            st.write(text)

            st.session_state.speech_history.append(text)

        except:

            st.error(
                translate_text(
                    "❌ Could not understand audio"
                )
            )

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header(
        translate_text(
            "📖 Dyslexia-Friendly Reading"
        )
    )

    dyslexia_text = translate_text(
        """
Artificial Intelligence is transforming education
by making learning more personalized, accessible,
and inclusive for students across the world.
"""
    )

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
    {dyslexia_text}
    </div>
    """, unsafe_allow_html=True)

    st.success(
        translate_text(
            "✅ Accessibility Mode Enabled"
        )
    )

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text("❓ AI Quiz Generator")
    )

    exam = st.text_input(
        translate_text("📝 Enter Exam Name")
    )

    topic = st.text_input(
        translate_text("📘 Enter Topic")
    )

    num_questions = st.slider(
        translate_text("📊 Number of Questions"),
        1,
        10,
        5
    )

    difficulty = st.selectbox(
        translate_text("📈 Difficulty"),
        ["Easy", "Medium", "Hard"]
    )

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        st.success(
            translate_text(
                f"{num_questions} Questions Generated"
            )
        )

        question_bank = [
            f"What is {topic}?",
            f"Explain advantages of {topic}.",
            f"Where is {topic} used?",
            f"What are applications of {topic}?",
            f"Why is {topic} important?",
            f"Explain future scope of {topic}.",
            f"What are challenges in {topic}?",
            f"Define {topic}.",
            f"Explain working of {topic}.",
            f"Compare {topic} with traditional methods."
        ]

        random.shuffle(question_bank)

        for i in range(num_questions):

            st.markdown("---")

            st.subheader(
                translate_text(
                    f"Q{i+1}. {question_bank[i]}"
                )
            )

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header(
        translate_text(
            "♿ Accessibility Support"
        )
    )

    features = [
        "👁️ Blind Support",
        "👂 Deaf Support",
        "🗣️ Speech Assistance",
        "📖 Dyslexia-Friendly Reading",
        "🌍 28 Language Support",
        "🔠 Adjustable Font Size",
        "🌗 High Contrast Mode"
    ]

    for item in features:

        st.write(
            translate_text(item)
        )

# ---------------------------------------------------
# AI ASSISTANT
# ---------------------------------------------------

elif feature == lang["assistant"]:

    st.header(
        translate_text(
            "🤖 EduAccess AI Assistant"
        )
    )

    st.write(
        translate_text(
            "Ask questions about how to use EduAccess AI."
        )
    )

    user_query = st.text_input(
        translate_text("Ask your question")
    )

    if st.button(
        translate_text("Ask Assistant")
    ):

        query = user_query.lower()

        if "summary" in query:

            response = """
1. Open AI Notes Summarizer
2. Paste notes
3. Select summary length
4. Click Generate Summary
"""

        elif "quiz" in query:

            response = """
1. Open Quiz Generator
2. Enter exam name
3. Enter topic
4. Generate quiz
"""

        elif "speech" in query:

            response = """
1. Open Speech-to-Text
2. Record your voice
3. AI converts speech into text
"""

        else:

            response = """
Welcome to EduAccess AI.

You can ask about:
• Summary
• Quiz
• Speech
• Accessibility
"""

        st.success(
            translate_text(response)
        )
