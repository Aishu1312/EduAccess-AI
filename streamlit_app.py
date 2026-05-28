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
# ADVANCED QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text("🧠 AI Adaptive Quiz Generator")
    )

    st.write(
        translate_text(
            "Generate intelligent quizzes with adaptive difficulty levels."
        )
    )

    # -----------------------------------
    # HISTORY
    # -----------------------------------

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

    # -----------------------------------
    # INPUTS
    # -----------------------------------

    exam = st.text_input(
        translate_text("📝 Enter Exam Name")
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
        15,
        5
    )

    # -----------------------------------
    # QUESTION BANK
    # -----------------------------------

    easy_questions = [
        {
            "question": f"What is {topic}?",
            "answer": f"{topic} is an important concept.",
            "options": [
                f"{topic} is an important concept.",
                "It is a game",
                "It is unrelated to studies",
                "None"
            ],
            "explanation": f"{topic} is widely used in education and technology."
        },
        {
            "question": f"Why is {topic} useful?",
            "answer": "It improves learning and productivity.",
            "options": [
                "It improves learning and productivity.",
                "It wastes time",
                "No benefits",
                "None"
            ],
            "explanation": f"{topic} helps improve efficiency."
        }
    ]

    medium_questions = [
        {
            "question": f"How is {topic} used in industries?",
            "answer": "Automation and intelligent systems",
            "options": [
                "Automation and intelligent systems",
                "Only paperwork",
                "Manual calculations",
                "None"
            ],
            "explanation": f"{topic} is used in automation and AI."
        },
        {
            "question": f"What challenge exists in {topic}?",
            "answer": "Data privacy",
            "options": [
                "Data privacy",
                "No challenge",
                "Only handwriting",
                "None"
            ],
            "explanation": "Privacy is a major concern."
        }
    ]

    hard_questions = [
        {
            "question": f"Explain advanced applications of {topic}.",
            "answer": "AI-driven predictive systems",
            "options": [
                "AI-driven predictive systems",
                "Only manual systems",
                "No applications",
                "Typewriting"
            ],
            "explanation": f"{topic} powers predictive AI systems."
        },
        {
            "question": f"How does {topic} contribute to future technologies?",
            "answer": "By enabling intelligent automation",
            "options": [
                "By enabling intelligent automation",
                "By reducing innovation",
                "No contribution",
                "None"
            ],
            "explanation": "Automation is key to future technology."
        }
    ]

    if difficulty == "Easy":
        question_pool = easy_questions

    elif difficulty == "Medium":
        question_pool = medium_questions

    else:
        question_pool = hard_questions

    # -----------------------------------
    # GENERATE QUIZ
    # -----------------------------------

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        random.shuffle(question_pool)

        selected_questions = []

        for q in question_pool:

            if q["question"] not in st.session_state.used_questions:

                selected_questions.append(q)

                st.session_state.used_questions.add(
                    q["question"]
                )

            if len(selected_questions) == num_questions:
                break

        st.session_state.quiz_data = selected_questions
        st.session_state.quiz_score = 0
        st.session_state.quiz_started = True
        st.session_state.answer_feedback = {}

    # -----------------------------------
    # DISPLAY QUIZ
    # -----------------------------------

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

                correct_answer = translate_text(
                    q["answer"]
                )

                if answer == correct_answer:

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

        st.markdown("---")

        total = len(
            st.session_state.quiz_data
        ) * 2

        st.header(
            translate_text(
                f"🏆 Final Score: {st.session_state.quiz_score}/{total}"
            )
        )

        # SAVE HISTORY

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
# AI PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == "🧠 AI Personalized Learning":

    st.header("🧠 AI Personalized Learning")

    weak_topic = st.text_input(
        "Enter Weak Topic"
    )

    learning_style = st.selectbox(
        "Preferred Learning Style",
        [
            "Visual",
            "Practical",
            "Theory",
            "Interactive"
        ]
    )

    if st.button("Generate Recommendations"):

        st.success(
            f"AI detected weak understanding in {weak_topic}"
        )

        recommendations = [

            f"Practice quizzes on {weak_topic}",

            f"Watch YouTube tutorials on {weak_topic}",

            f"Revise fundamentals daily",

            f"Use visual diagrams for {weak_topic}"
        ]

        for rec in recommendations:

            st.info(rec)

# ---------------------------------------------------
# FLOATING AI CHAT ASSISTANT
# ---------------------------------------------------

st.markdown("""
<style>

/* Floating Chat Button */
.chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #2563eb;
    color: white;
    padding: 15px 18px;
    border-radius: 50px;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    z-index: 9999;
    animation: pulse 2s infinite;
}

/* Pulse Animation */
@keyframes pulse {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
    100% {
        transform: scale(1);
    }
}

.chat-box {
    background-color: #0f172a;
    padding: 20px;
    border-radius: 15px;
    color: white;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# Floating button
st.markdown(
    """
    <div class="chat-button">
    🤖 Need Help?
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# FLOATING AI ASSISTANT
# ---------------------------------------------------

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

# Floating Button CSS

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
    cursor: pointer;
    z-index: 99999;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
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

.chat-title {
    font-size: 22px;
    font-weight: bold;
    color: #2563eb;
}

.chat-text {
    color: black;
    font-size: 16px;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)

# BUTTON

if st.button("🤖 Alia Assistant"):

    st.session_state.show_chat = (
        not st.session_state.show_chat
    )

# POPUP WINDOW

if st.session_state.show_chat:

    st.markdown("""
    <div class="chat-popup">

    <div class="chat-title">
    👋 Hi, I am Alia
    </div>

    <div class="chat-text">

    Your AI Accessibility Assistant.

    I can help you with:

    ✅ AI Notes Summarizer  
    ✅ Speech-to-Text  
    ✅ Quiz Generator  
    ✅ Dyslexia Mode  
    ✅ Accessibility Features  

    Ask me anything below 👇

    </div>

    </div>
    """, unsafe_allow_html=True)

    user_query = st.text_input(
        "💬 Ask Alia"
    )

    if st.button("🚀 Send"):

        query = user_query.lower()

        # ---------------------------------
        # SUMMARY
        # ---------------------------------

        if "summary" in query or "notes" in query:

            st.success("""
📘 Steps to Generate Summary

1️⃣ Open AI Notes Summarizer  
2️⃣ Paste educational notes  
3️⃣ Select summary length  
4️⃣ Click Generate Summary  
5️⃣ AI generates concise notes
""")

        # ---------------------------------
        # QUIZ
        # ---------------------------------

        elif "quiz" in query:

            st.success("""
❓ Steps to Generate Quiz

1️⃣ Open Quiz Generator  
2️⃣ Enter exam name  
3️⃣ Enter topic  
4️⃣ Select question count  
5️⃣ Click Generate Quiz
""")

        # ---------------------------------
        # SPEECH
        # ---------------------------------

        elif "speech" in query or "voice" in query:

            st.success("""
🎤 Steps for Speech-to-Text

1️⃣ Open Speech-to-Text  
2️⃣ Click microphone  
3️⃣ Speak clearly  
4️⃣ AI converts speech into text
""")

        # ---------------------------------
        # DYSLEXIA
        # ---------------------------------

        elif "dyslexia" in query:

            st.success("""
📖 Dyslexia-Friendly Reading

This feature helps students with:
✅ Reading difficulties
✅ Dyslexia
✅ Visual stress

Features:
• Large fonts
• Better spacing
• Simplified reading
• Multilingual support
""")

        # ---------------------------------
        # ACCESSIBILITY
        # ---------------------------------

        elif "accessibility" in query:

            st.success("""
♿ Accessibility Features

✅ 28 Language Support  
✅ Adjustable Fonts  
✅ High Contrast Mode  
✅ Voice Assistance  
✅ AI Learning Support  
✅ Inclusive Education
""")

        # ---------------------------------
        # DEFAULT
        # ---------------------------------

        else:

            st.info("""
🤖 Ask Me About:

• Summary
• Quiz
• Speech
• Accessibility
• Dyslexia

Example:
➡️ How to generate summary?
➡️ How to use quiz?
➡️ How speech recognition works?
""")
