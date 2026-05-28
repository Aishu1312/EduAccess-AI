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
# LANGUAGE SELECTOR
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
    "speech_history": [],
    "used_questions": set(),
    "show_chat": False
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
    "accessibility": "♿ Accessibility Support"
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
        translate_text("🧠 AI Personalized Learning"),
        translate_text("😊 Emotion-Aware Learning"),
        translate_text("🚀 AI Career Mentor")
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
        translate_text("""
EduAccess AI is an intelligent inclusive learning platform
designed to help students with disabilities learn more effectively
using Artificial Intelligence, NLP, speech technologies,
and accessibility-focused tools.
""")
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

        st.success(
            translate_text(
                "🎤 Speech-to-Text"
            )
        )

    with col2:

        st.warning(
            translate_text(
                "📖 Dyslexia-Friendly Reading"
            )
        )

        st.error(
            translate_text(
                "❓ AI Quiz Generator"
            )
        )

    st.markdown("---")

    st.header(
        translate_text("♿ Accessibility Support")
    )

    features = [
        "✅ Dyslexia Support",
        "✅ Speech Assistance",
        "✅ 28 Language Support",
        "✅ Adjustable Font Size",
        "✅ High Contrast Mode",
        "✅ AI Learning Support"
    ]

    for item in features:

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

    uploaded_file = st.file_uploader(
        translate_text("📂 Upload PDF"),
        type=["pdf"]
    )

    pdf_text = ""

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:

                pdf_text += extracted

    text = st.text_area(
        translate_text("📌 Paste Notes Here"),
        value=pdf_text,
        height=300
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

            summary = ". ".join(
                sentences[:num]
            ) + "."

            translated_summary = translate_text(
                summary
            )

            st.session_state.summary = translated_summary

            st.session_state.summary_history.append(
                translated_summary
            )

            st.success(
                translate_text(
                    "✅ Summary Generated Successfully"
                )
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
                translate_text(
                    "⚠️ Please enter notes"
                )
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
                    audio_data
                )

            translated = translate_text(text)

            st.success(
                translate_text(
                    "✅ Speech Recognized"
                )
            )

            st.write(translated)

            st.session_state.speech_history.append(
                translated
            )

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

    if not st.session_state.summary:

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
        translate_text(
            "🧠 AI Adaptive Quiz Generator"
        )
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
                                f"Q. {q['question']}"
                            )
                        )

                        st.success(
                            translate_text(
                                f"✔ Answer: {q['answer']}"
                            )
                        )

                        st.info(
                            translate_text(
                                f"📖 Explanation: {q['explanation']}"
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
                "No use",
                "Only game",
                "None"
            ],
            "explanation": f"{topic} is widely used."
        }
    ]

    medium_questions = [
        {
            "question": f"How is {topic} used in industries?",
            "answer": "Automation",
            "options": [
                "Automation",
                "Only paperwork",
                "No use",
                "None"
            ],
            "explanation": f"{topic} supports automation."
        }
    ]

    hard_questions = [
        {
            "question": f"Explain advanced applications of {topic}.",
            "answer": "AI predictive systems",
            "options": [
                "AI predictive systems",
                "No applications",
                "Only typing",
                "None"
            ],
            "explanation": "Used in advanced AI."
        }
    ]

    if difficulty == "Easy":

        question_pool = easy_questions

    elif difficulty == "Medium":

        question_pool = medium_questions

    else:

        question_pool = hard_questions

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        random.shuffle(question_pool)

        st.session_state.quiz_data = question_pool[
            :num_questions
        ]

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

            answer = st.radio(
                translate_text("Choose Answer"),
                translated_options,
                key=f"quiz_{idx}"
            )

            if st.button(
                translate_text(f"Submit Q{idx+1}"),
                key=f"submit_{idx}"
            ):

                correct = translate_text(
                    q["answer"]
                )

                if answer == correct:

                    st.success(
                        translate_text(
                            "✅ Correct Answer"
                        )
                    )

                    st.session_state.quiz_score += 2

                else:

                    st.error(
                        translate_text(
                            "❌ Wrong Answer"
                        )
                    )

                st.info(
                    translate_text(
                        f"✔ Correct Answer: {q['answer']}"
                    )
                )

                st.warning(
                    translate_text(
                        f"📖 Explanation: {q['explanation']}"
                    )
                )

        total = len(
            st.session_state.quiz_data
        ) * 2

        st.header(
            translate_text(
                f"🏆 Final Score: {st.session_state.quiz_score}/{total}"
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
                    "✅ Quiz Saved Successfully"
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
# PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == translate_text(
    "🧠 AI Personalized Learning"
):

    st.header(
        translate_text(
            "🧠 AI Personalized Learning"
        )
    )

    weak_topic = st.text_input(
        translate_text(
            "Enter Weak Topic"
        )
    )

    learning_style = st.selectbox(
        translate_text(
            "Preferred Learning Style"
        ),
        [
            "Visual",
            "Practical",
            "Theory",
            "Interactive"
        ]
    )

    if st.button(
        translate_text(
            "Generate Recommendations"
        )
    ):

        st.success(
            translate_text(
                f"AI detected weak understanding in {weak_topic}"
            )
        )

        recommendations = [

            f"Practice quizzes on {weak_topic}",

            f"Watch tutorials on {weak_topic}",

            f"Revise fundamentals daily",

            f"Use visual diagrams"

        ]

        for rec in recommendations:

            st.info(
                translate_text(rec)
            )

# ---------------------------------------------------
# EMOTION LEARNING
# ---------------------------------------------------

elif feature == translate_text(
    "😊 Emotion-Aware Learning"
):

    st.header(
        translate_text(
            "😊 Emotion-Aware Learning"
        )
    )

    emotion = st.selectbox(
        translate_text(
            "How are you feeling?"
        ),
        [
            "Confused",
            "Stressed",
            "Focused",
            "Tired"
        ]
    )

    if st.button(
        translate_text(
            "Analyze Emotion"
        )
    ):

        if emotion == "Confused":

            st.warning(
                translate_text(
                    "AI detected confusion. Use visual learning."
                )
            )

        elif emotion == "Stressed":

            st.error(
                translate_text(
                    "AI detected stress. Take breaks."
                )
            )

        elif emotion == "Focused":

            st.success(
                translate_text(
                    "AI detected strong focus."
                )
            )

        else:

            st.info(
                translate_text(
                    "AI suggests taking proper rest."
                )
            )

# ---------------------------------------------------
# CAREER MENTOR
# ---------------------------------------------------

elif feature == translate_text(
    "🚀 AI Career Mentor"
):

    st.header(
        translate_text(
            "🚀 AI Career Mentor"
        )
    )

    query = st.text_input(
        translate_text(
            "Ask Career Guidance"
        )
    )

    if st.button(
        translate_text(
            "Get AI Guidance"
        )
    ):

        if "data science" in query.lower():

            st.success("""
• AI Resume Analyzer
• Fake News Detection
• Sales Dashboard
• ML Recommendation System
""")

        elif "ai" in query.lower():

            st.success("""
• AI Chatbot
• Emotion Detection
• NLP Summarizer
• AI Interview Coach
""")

        else:

            st.info("""
• Build projects
• Improve GitHub
• Learn deployment
• Practice DSA
""")

# ---------------------------------------------------
# FLOATING ASSISTANT
# ---------------------------------------------------

st.markdown("""
<style>

.chat-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #2563eb;
    color: white;
    padding: 14px 22px;
    border-radius: 50px;
    font-size: 18px;
    font-weight: bold;
    z-index: 99999;
}

.chat-popup {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 340px;
    background-color: white;
    border-radius: 20px;
    padding: 20px;
    z-index: 99999;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
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
    ✅ Summary<br>
    ✅ Quiz<br>
    ✅ Accessibility<br>
    ✅ Career Guidance<br>
    </p>

    </div>
    """, unsafe_allow_html=True)

    user_query = st.text_input(
        "💬 Ask Alia"
    )

    if st.button("🚀 Send"):

        st.success(
            translate_text(
                "Thanks for your question. Alia is guiding you."
            )
        )
```
