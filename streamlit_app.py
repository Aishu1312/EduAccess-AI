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
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text("❓ AI Quiz Generator")
    )

    # -----------------------------------
    # NEW QUIZ + HISTORY
    # -----------------------------------

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

                    with st.expander(
                        f"Quiz {idx} | "
                        f"{translate_text('Topic')}: {item['topic']} | "
                        f"{translate_text('Score')}: {item['score']}"
                    ):

                        st.subheader(
                            translate_text("📘 Quiz Details")
                        )

                        for q_no, q in enumerate(
                            item["questions"],
                            start=1
                        ):

                            st.markdown("---")

                            st.write(
                                translate_text(
                                    f"Q{q_no}. {q['question']}"
                                )
                            )

                            st.success(
                                translate_text(
                                    f"✔ Correct Answer: {q['correct_answer']}"
                                )
                            )

                            st.info(
                                translate_text(
                                    f"📖 Explanation: {q['reason']}"
                                )
                            )

            else:

                st.info(
                    translate_text(
                        "No quiz history available"
                    )
                )

    # -----------------------------------
    # QUIZ INPUTS
    # -----------------------------------

    exam = st.text_input(
        translate_text("📝 Enter Exam Name")
    )

    topic = st.text_input(
        translate_text("📘 Enter Topic")
    )

    num_questions = st.slider(
        translate_text("📊 Select Number of Questions"),
        1,
        10,
        5
    )

    difficulty = st.selectbox(
        translate_text("📈 Select Difficulty"),
        ["Easy", "Medium", "Hard"]
    )

    # -----------------------------------
    # GENERATE QUIZ
    # -----------------------------------

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        st.session_state.quiz_started = True
        st.session_state.quiz_score = 0
        st.session_state.answer_feedback = {}

        question_bank = [

            {
                "question": f"What is the main purpose of {topic}?",
                "correct": f"{topic} improves efficiency and automation",
                "wrong": [
                    f"{topic} decreases productivity",
                    f"{topic} is outdated",
                    f"{topic} has no practical use"
                ],
                "reason": f"{topic} is widely used for automation and innovation."
            },

            {
                "question": f"Which industry uses {topic} extensively?",
                "correct": "Healthcare and Technology",
                "wrong": [
                    "Only agriculture",
                    "Only sports",
                    "None"
                ],
                "reason": f"{topic} is heavily used in healthcare and technology sectors."
            },

            {
                "question": f"What is an important benefit of {topic}?",
                "correct": "Automation and intelligent decision-making",
                "wrong": [
                    "Increases manual work",
                    "Reduces accuracy",
                    "No benefits"
                ],
                "reason": f"{topic} helps automate tasks and improve decisions."
            },

            {
                "question": f"What is the future scope of {topic}?",
                "correct": "Advanced AI applications",
                "wrong": [
                    "No future growth",
                    "Only paperwork",
                    "Typewriting"
                ],
                "reason": f"{topic} has strong future demand in AI and automation."
            },

            {
                "question": f"What skill is important for learning {topic}?",
                "correct": "Problem-solving",
                "wrong": [
                    "Only handwriting",
                    "Sleeping",
                    "Ignoring technology"
                ],
                "reason": "Problem-solving is essential in technology."
            },

            {
                "question": f"Why is {topic} important in modern industries?",
                "correct": "It improves productivity",
                "wrong": [
                    "It wastes time",
                    "It reduces efficiency",
                    "No importance"
                ],
                "reason": f"{topic} helps industries become more productive."
            },

            {
                "question": f"Which technology is related to {topic}?",
                "correct": "Artificial Intelligence",
                "wrong": [
                    "Typewriter",
                    "Paper filing",
                    "Manual records"
                ],
                "reason": f"{topic} is connected with modern digital technologies."
            },

            {
                "question": f"Which field benefits from {topic}?",
                "correct": "Education",
                "wrong": [
                    "None",
                    "Only farming",
                    "Only drawing"
                ],
                "reason": f"{topic} supports learning and innovation."
            },

            {
                "question": f"What is a challenge in {topic}?",
                "correct": "Data privacy and security",
                "wrong": [
                    "No challenges",
                    "Only handwriting issues",
                    "No technology needed"
                ],
                "reason": f"Security and privacy are major challenges."
            },

            {
                "question": f"Which company uses {topic} technologies?",
                "correct": "Google",
                "wrong": [
                    "No company",
                    "Only libraries",
                    "Only schools"
                ],
                "reason": f"Google uses advanced technology and AI systems."
            }

        ]

        random.shuffle(question_bank)

        selected_questions = question_bank[:num_questions]

        st.session_state.quiz_data = []

        for q in selected_questions:

            options = [q["correct"]] + q["wrong"]

            random.shuffle(options)

            q["options"] = options

            st.session_state.quiz_data.append(q)

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

            # -----------------------------
            # FEEDBACK
            # -----------------------------

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
                        f"📖 Explanation: {feedback['reason']}"
                    )
                )

                st.success(
                    translate_text(
                        f"🏆 Current Score: {feedback['score']}"
                    )
                )

        # -----------------------------------
        # FINAL SCORE
        # -----------------------------------

        total_score = len(
            st.session_state.quiz_data
        ) * 2

        st.markdown("---")

        st.header(
            translate_text(
                f"🎯 Final Score: {st.session_state.quiz_score}/{total_score}"
            )
        )

        # -----------------------------------
        # SAVE HISTORY
        # -----------------------------------

        if st.button(
            translate_text("💾 Save Quiz History")
        ):

            st.session_state.quiz_history.append({

                "topic": topic,

                "score": f"{st.session_state.quiz_score}/{total_score}",

                "questions": [

                    {
                        "question": q["question"],
                        "correct_answer": q["correct"],
                        "reason": q["reason"]
                    }

                    for q in st.session_state.quiz_data
                ]
            })

            st.success(
                translate_text(
                    "✅ Quiz Saved Successfully"
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
