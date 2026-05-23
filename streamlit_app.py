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
# TRANSLATOR
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
# SESSION STATES
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
    "dyslexia_history": []
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# UI TEXT
# ---------------------------------------------------

base_text = {
    "title": "🚀 EduAccess AI",
    "subtitle": "AI-Powered Accessibility Platform",
    "choose_feature": "Choose Feature",
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech-to-Text",
    "dyslexia": "📖 Dyslexia-Friendly Reading",
    "quiz": "❓ AI Quiz Generator",
    "accessibility": "♿ Accessibility Support"
}

lang = {}

for key, value in base_text.items():
    lang[key] = translate_text(value)

# ---------------------------------------------------
# SIDEBAR SETTINGS
# ---------------------------------------------------

st.sidebar.title(
    translate_text("⚙ Settings")
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
        lang["accessibility"]
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

    st.title(translate_text("🚀 EduAccess AI"))

    st.subheader(
        translate_text(
            "AI-Powered Accessibility Platform"
        )
    )

    st.success(
        translate_text(
            "Welcome to EduAccess AI"
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

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header(
        translate_text("🧠 AI Notes Summarizer")
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button(
            translate_text("🆕 New Notes")
        ):
            st.session_state.summary = ""
            st.rerun()

    with col2:
        with st.expander(
            translate_text("📚 Notes History")
        ):
            if st.session_state.summary_history:
                for idx, item in enumerate(
                    reversed(st.session_state.summary_history),
                    start=1
                ):
                    st.subheader(f"Notes {idx}")
                    st.write(item)
            else:
                st.info(
                    translate_text("No history available")
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

        sentences = [
            s.strip() for s in text.split('.') if s.strip()
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

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button(
            translate_text("🆕 New Speech")
        ):
            st.rerun()

    with col2:
        with st.expander(
            translate_text("📚 Speech History")
        ):
            if st.session_state.speech_history:
                for idx, item in enumerate(
                    reversed(st.session_state.speech_history),
                    start=1
                ):
                    st.subheader(f"Speech {idx}")
                    st.write(item)
            else:
                st.info(
                    translate_text("No history available")
                )

    answer_type = st.selectbox(
        translate_text("📚 Select Explanation Type"),
        ["Short", "Medium", "Detailed"]
    )

    audio = st.audio_input(
        translate_text("🎙️ Record Voice")
    )

    uploaded_file = st.file_uploader(
        translate_text("📂 Upload Audio"),
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
                text = recognizer.recognize_google(audio_data)

            st.subheader(
                translate_text("📝 Your Question")
            )

            st.info(text)

            question = text.lower()

            if "difference" in question:

                answer = f"""
<table border='1' style='width:100%; color:white;'>
<tr>
<th>Feature</th>
<th>Supervised Learning</th>
<th>Unsupervised Learning</th>
</tr>
<tr>
<td>Data</td>
<td>Labeled Data</td>
<td>Unlabeled Data</td>
</tr>
<tr>
<td>Purpose</td>
<td>Prediction</td>
<td>Pattern Detection</td>
</tr>
<tr>
<td>Examples</td>
<td>Spam Detection</td>
<td>Customer Segmentation</td>
</tr>
</table>

Real-world Example:
Netflix recommendations use unsupervised learning while email spam filters use supervised learning.
"""

            elif "excel" in question:

                if answer_type == "Short":
                    answer = "Excel is spreadsheet software used for calculations and reports."

                elif answer_type == "Medium":
                    answer = """
Excel is used for calculations, charts, and data analysis.

Examples:
• Attendance sheets
• Budget management
• Student marksheets
"""

                else:
                    answer = """
Microsoft Excel is a spreadsheet application used for organizing, calculating, analyzing, and visualizing data.

Features:
• Formulas
• Charts
• Tables
• Pivot Tables
• Data Analysis

Real-world Examples:
• Banking reports
• Inventory management
• School result systems
• Salary calculations
"""

            elif "artificial intelligence" in question or "ai" in question:

                answer = """
Artificial Intelligence enables machines to simulate human intelligence.

Applications:
• Chatbots
• Voice Assistants
• Medical Diagnosis
• Self-driving Cars

Real-world Examples:
• ChatGPT
• Alexa
• Netflix Recommendations
"""

            else:

                answer = f"""
{text} is an important topic related to education and technology.

Key Points:
• Improves learning
• Supports innovation
• Helps solve real-world problems

Real-world Example:
{text} is widely used in academics and industries.
"""

            translated_answer = translate_text(answer)

            st.subheader(
                translate_text("🤖 AI Explanation")
            )

            st.markdown(f"""
            <div style="
                background-color:#0f172a;
                padding:20px;
                border-radius:15px;
                color:white;
                font-size:{font_size}px;
                line-height:2;
            ">
            {translated_answer}
            </div>
            """, unsafe_allow_html=True)

            st.session_state.speech_history.append({
                "question": text,
                "answer": answer
            })

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

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button(
            translate_text("🆕 New Reading")
        ):
            st.session_state.summary = ""
            st.rerun()

    with col2:
        with st.expander(
            translate_text("📚 Reading History")
        ):
            if st.session_state.summary_history:
                for idx, item in enumerate(
                    reversed(st.session_state.summary_history),
                    start=1
                ):
                    st.subheader(f"Reading {idx}")
                    st.write(item)

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
        translate_text("❓ AI Quiz Generator")
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button(
            translate_text("🆕 New Quiz")
        ):

            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_data = []
            st.session_state.answer_feedback = {}

            st.rerun()

    with col2:

        with st.expander(
            translate_text("📚 Quiz History")
        ):

            if st.session_state.quiz_history:

                for idx, item in enumerate(
                    reversed(st.session_state.quiz_history),
                    start=1
                ):

                    st.subheader(f"Quiz {idx}")

                    st.write(
                        translate_text(
                            f"Topic: {item['topic']}"
                        )
                    )

                    st.write(
                        translate_text(
                            f"Score: {item['score']}"
                        )
                    )

            else:
                st.info(
                    translate_text("No quiz history available")
                )

    exam = st.text_input(
        translate_text("📝 Enter Exam Name")
    )

    topic = st.text_input(
        translate_text("📘 Enter Topic")
    )

    num_questions = st.slider(
        translate_text("📊 Select Number of Questions"),
        1,
        15,
        5
    )

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        st.session_state.quiz_started = True
        st.session_state.quiz_score = 0
        st.session_state.answer_feedback = {}

        question_bank = []

        for i in range(1, 16):

            question_bank.append({
                "question": f"What is an important concept of {topic}?",
                "correct": f"{topic} improves efficiency and innovation",
                "wrong": [
                    f"{topic} has no practical use",
                    f"{topic} decreases productivity",
                    f"{topic} only works manually"
                ],
                "reason": f"{topic} is widely used in industries, education, and technology."
            })

        random.shuffle(question_bank)

        selected_questions = question_bank[:num_questions]

        st.session_state.quiz_data = []

        for q in selected_questions:

            options = [q["correct"]] + q["wrong"]
            random.shuffle(options)

            q["options"] = options

            st.session_state.quiz_data.append(q)

    if st.session_state.quiz_started:

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                f"Q{idx+1}. {translate_text(q['question'])}"
            )

            translated_options = [
                translate_text(opt)
                for opt in q["options"]
            ]

            selected = st.radio(
                translate_text("Choose Answer"),
                translated_options,
                key=f"radio_{idx}"
            )

            if st.button(
                translate_text(f"Submit Q{idx+1}"),
                key=f"submit_{idx}"
            ):

                correct_translated = translate_text(
                    q["correct"]
                )

                is_correct = (
                    selected == correct_translated
                )

                if is_correct:
                    st.session_state.quiz_score += 2

                st.session_state.answer_feedback[idx] = {
                    "correct": is_correct,
                    "correct_answer": q["correct"],
                    "reason": q["reason"],
                    "score": st.session_state.quiz_score
                }

            if idx in st.session_state.answer_feedback:

                feedback = st.session_state.answer_feedback[idx]

                if feedback["correct"]:
                    st.success(
                        translate_text(
                            "✅ Correct Answer"
                        )
                    )
                    st.balloons()

                else:
                    st.error(
                        translate_text(
                            "❌ Wrong Answer"
                        )
                    )

                st.info(
                    translate_text(
                        f"✔ Correct Answer: {feedback['correct_answer']}"
                    )
                )

                st.warning(
                    translate_text(
                        f"📖 Reason: {feedback['reason']}"
                    )
                )

                st.success(
                    translate_text(
                        f"🏆 Points Achieved: {feedback['score']}"
                    )
                )

        total_score = len(
            st.session_state.quiz_data
        ) * 2

        st.markdown("---")

        st.header(
            translate_text(
                f"🎯 Final Score: {st.session_state.quiz_score}/{total_score}"
            )
        )

        if st.button(
            translate_text("💾 Save Quiz History")
        ):

            st.session_state.quiz_history.append({
                "topic": topic,
                "score": f"{st.session_state.quiz_score}/{total_score}"
            })

            st.success(
                translate_text("Quiz Saved Successfully")
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
        "👁️ Blind Support → Audio + Screen Reader",
        "👂 Deaf Support → Text Interface",
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
