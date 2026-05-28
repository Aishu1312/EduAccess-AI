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
    "Odia": "or-IN",
    "Assamese": "as-IN",
    "Sanskrit": "sa-IN",
    "Nepali": "ne-NP",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Portuguese": "pt-PT",
    "Russian": "ru-RU",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN",
    "Arabic": "ar-SA",
    "Turkish": "tr-TR",
    "Thai": "th-TH",
    "Indonesian": "id-ID"
}

# ---------------------------------------------------
# LANGUAGE SELECTION
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

defaults = {

    "summary": "",
    "quiz_started": False,
    "quiz_score": 0,
    "quiz_data": [],
    "quiz_history": [],
    "summary_history": [],
    "speech_history": [],
    "show_chat": False,
    "used_questions": set()
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ---------------------------------------------------
# UI TEXT
# ---------------------------------------------------

base_text = {

    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech-to-Text",
    "dyslexia": "📖 Dyslexia-Friendly Reading",
    "quiz": "❓ AI Quiz Generator",
    "accessibility": "♿ Accessibility Support",
    "learning": "🧠 AI Personalized Learning",
    "emotion": "😊 Emotion-Aware Learning",
    "career": "🚀 AI Career Mentor"
}

lang = {}

for key, value in base_text.items():

    lang[key] = translate_text(value)

# ---------------------------------------------------
# SIDEBAR
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

    translate_text("Choose Feature"),

    [
        lang["home"],
        lang["summarizer"],
        lang["speech"],
        lang["dyslexia"],
        lang["quiz"],
        lang["accessibility"],
        lang["learning"],
        lang["emotion"],
        lang["career"]
    ]
)

# ---------------------------------------------------
# HIGH CONTRAST
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
EduAccess AI helps students with disabilities using AI,
speech technologies, NLP, quizzes, summaries,
accessibility support, and personalized learning.
"""
        )
    )

    st.markdown("---")

    st.header(
        translate_text("🌟 Core Features")
    )

    features = [

        "🧠 AI Notes Summarizer",
        "🎤 Speech-to-Text",
        "📖 Dyslexia-Friendly Reading",
        "❓ AI Quiz Generator",
        "🧠 Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor"
    ]

    for item in features:

        st.info(
            translate_text(item)
        )

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header(
        translate_text("🧠 AI Notes Summarizer")
    )

    uploaded_file = st.file_uploader(
        translate_text("📂 Upload PDF"),
        type=["pdf"]
    )

    text = ""

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

        st.success(
            translate_text("✅ PDF Text Extracted")
        )

    manual_text = st.text_area(
        translate_text("📌 Paste Notes Here"),
        height=250
    )

    if manual_text:

        text += manual_text

    summary_length = st.selectbox(

        translate_text("📏 Select Summary Length"),

        ["Short", "Medium", "Detailed"]
    )

    if st.button(
        translate_text("🚀 Generate Summary")
    ):

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

            st.session_state.summary_history.append(
                translated_summary
            )

            st.success(
                translate_text("✅ Summary Generated")
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
                translate_text("⚠️ Enter Notes")
            )

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    audio = st.audio_input(
        translate_text("🎙️ Record Voice")
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
        translate_text("📖 Dyslexia-Friendly Reading")
    )

    if st.session_state.summary == "":

        st.warning(
            translate_text(
                "⚠️ Generate summary first"
            )
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
        {st.session_state.summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text("❓ AI Adaptive Quiz Generator")
    )

    with st.expander(
        translate_text("📚 Quiz History")
    ):

        if st.session_state.quiz_history:

            for idx, quiz in enumerate(

                reversed(st.session_state.quiz_history),
                start=1
            ):

                with st.expander(

                    f"Quiz {idx} | {quiz['topic']} | {quiz['score']}"
                ):

                    for q in quiz["questions"]:

                        st.markdown("---")

                        st.write(
                            translate_text(
                                q["question"]
                            )
                        )

                        st.success(
                            translate_text(
                                f"✔ {q['answer']}"
                            )
                        )

                        st.info(
                            translate_text(
                                q["explanation"]
                            )
                        )

        else:

            st.info(
                translate_text(
                    "No quiz history available"
                )
            )

    topic = st.text_input(
        translate_text("📘 Enter Topic")
    )

    difficulty = st.selectbox(

        translate_text("🎯 Select Difficulty"),

        ["Easy", "Medium", "Hard"]
    )

    num_questions = st.slider(

        translate_text("📊 Number of Questions"),

        1,
        10,
        5
    )

    easy_questions = [

        {
            "question": f"What is {topic}?",
            "answer": f"{topic} is an important concept.",
            "options": [
                f"{topic} is an important concept.",
                "It is a game",
                "None",
                "No use"
            ],
            "explanation": f"{topic} is useful in studies."
        },

        {
            "question": f"Why is {topic} important?",
            "answer": "It improves knowledge",
            "options": [
                "It improves knowledge",
                "No benefits",
                "Waste of time",
                "None"
            ],
            "explanation": "It helps learning."
        }
    ]

    medium_questions = [

        {
            "question": f"How is {topic} used in industries?",
            "answer": "Automation",
            "options": [
                "Automation",
                "No usage",
                "Cooking",
                "Gaming"
            ],
            "explanation": "Industries use automation."
        }
    ]

    hard_questions = [

        {
            "question": f"What is advanced use of {topic}?",
            "answer": "AI systems",
            "options": [
                "AI systems",
                "No use",
                "Manual typing",
                "None"
            ],
            "explanation": "AI uses advanced technologies."
        }
    ]

    if difficulty == "Easy":

        pool = easy_questions

    elif difficulty == "Medium":

        pool = medium_questions

    else:

        pool = hard_questions

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        random.shuffle(pool)

        selected = pool[:num_questions]

        st.session_state.quiz_data = selected

        st.session_state.quiz_started = True

        st.session_state.quiz_score = 0

    if st.session_state.quiz_started:

        for idx, q in enumerate(

            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                translate_text(
                    f"Q{idx+1}. {q['question']}"
                )
            )

            translated_options = [

                translate_text(opt)

                for opt in q["options"]
            ]

            ans = st.radio(

                translate_text("Choose Answer"),

                translated_options,

                key=f"quiz_{idx}"
            )

            if st.button(

                translate_text(f"Submit Q{idx+1}"),

                key=f"submit_{idx}"
            ):

                if ans == translate_text(q["answer"]):

                    st.success(
                        translate_text(
                            "✅ Correct"
                        )
                    )

                    st.session_state.quiz_score += 2

                else:

                    st.error(
                        translate_text(
                            "❌ Wrong"
                        )
                    )

                st.info(
                    translate_text(
                        f"✔ Answer: {q['answer']}"
                    )
                )

                st.warning(
                    translate_text(
                        f"📖 {q['explanation']}"
                    )
                )

        total = len(
            st.session_state.quiz_data
        ) * 2

        st.header(
            translate_text(
                f"🏆 Score: {st.session_state.quiz_score}/{total}"
            )
        )

        if st.button(
            translate_text("💾 Save Quiz")
        ):

            st.session_state.quiz_history.append({

                "topic": topic,
                "score": f"{st.session_state.quiz_score}/{total}",
                "questions": st.session_state.quiz_data
            })

            st.success(
                translate_text(
                    "Quiz Saved"
                )
            )

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header(
        translate_text("♿ Accessibility Support")
    )

    features = [

        "🌍 28 Language Support",
        "🔠 Adjustable Font Size",
        "🌗 High Contrast Mode",
        "📖 Dyslexia Reading",
        "🎤 Speech Assistance"
    ]

    for item in features:

        st.write(
            translate_text(item)
        )

# ---------------------------------------------------
# AI PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == lang["learning"]:

    st.header(
        translate_text(
            "🧠 AI Personalized Learning"
        )
    )

    weak_topic = st.text_input(
        translate_text("Enter Weak Topic")
    )

    if st.button(
        translate_text("Generate Recommendations")
    ):

        st.success(
            translate_text(
                f"AI detected weak understanding in {weak_topic}"
            )
        )

        recommendations = [

            f"Practice quizzes on {weak_topic}",
            f"Watch tutorials on {weak_topic}",
            "Revise daily",
            "Use visual diagrams"
        ]

        for rec in recommendations:

            st.info(
                translate_text(rec)
            )

# ---------------------------------------------------
# EMOTION AWARE LEARNING
# ---------------------------------------------------

elif feature == lang["emotion"]:

    st.header(
        translate_text(
            "😊 Emotion-Aware Learning"
        )
    )

    emotion = st.selectbox(

        translate_text("How are you feeling?"),

        [
            "Confused",
            "Stressed",
            "Focused",
            "Tired"
        ]
    )

    if st.button(
        translate_text("Analyze Emotion")
    ):

        if emotion == "Confused":

            st.warning(
                translate_text(
                    "AI suggests beginner tutorials."
                )
            )

        elif emotion == "Stressed":

            st.error(
                translate_text(
                    "Take breaks and relax."
                )
            )

        elif emotion == "Focused":

            st.success(
                translate_text(
                    "Try advanced quizzes."
                )
            )

        else:

            st.info(
                translate_text(
                    "Take proper rest."
                )
            )

# ---------------------------------------------------
# CAREER MENTOR
# ---------------------------------------------------

elif feature == lang["career"]:

    st.header(
        translate_text(
            "🚀 AI Career Mentor"
        )
    )

    career_query = st.text_input(
        translate_text("Ask Career Guidance")
    )

    if st.button(
        translate_text("Get Guidance")
    ):

        query = career_query.lower()

        if "data science" in query:

            st.success(
                translate_text(
                    """
Recommended Skills:
• Python
• SQL
• Machine Learning
• Power BI
"""
                )
            )

        elif "ai" in query:

            st.success(
                translate_text(
                    """
Recommended AI Projects:
• Chatbot
• AI Accessibility Platform
• Resume Analyzer
"""
                )
            )

        else:

            st.info(
                translate_text(
                    "Build projects and improve GitHub."
                )
            )

# ---------------------------------------------------
# FLOATING AI ASSISTANT
# ---------------------------------------------------

st.markdown("""
<style>

.chat-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #2563eb;
    color: white;
    padding: 14px 20px;
    border-radius: 50px;
    z-index: 99999;
    font-size: 18px;
    font-weight: bold;
}

.chat-popup {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 320px;
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    z-index: 99999;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

if st.button("🤖 Alia Assistant"):

    st.session_state.show_chat = (

        not st.session_state.show_chat
    )

if st.session_state.show_chat:

    st.markdown("""
    <div class="chat-popup">
    <h3>👋 Hi, I am Alia</h3>
    <p>
    I can help you with:
    <br><br>
    ✅ Summaries
    <br>
    ✅ Quizzes
    <br>
    ✅ Accessibility
    <br>
    ✅ Speech Recognition
    </p>
    </div>
    """, unsafe_allow_html=True)

    user_query = st.text_input("💬 Ask Alia")

    if st.button("🚀 Send"):

        query = user_query.lower()

        if "summary" in query:

            st.success(
                "Go to AI Notes Summarizer and paste notes."
            )

        elif "quiz" in query:

            st.success(
                "Open Quiz Generator and enter topic."
            )

        elif "speech" in query:

            st.success(
                "Use microphone in Speech-to-Text."
            )

        else:

            st.info(
                "Ask about summary, quiz, speech or accessibility."
            )
