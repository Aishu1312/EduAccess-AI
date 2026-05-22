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

translations = {
    "English": {
        "title": "🚀 EduAccess AI",
        "subtitle": "AI-Powered Accessibility Platform",
        "choose_feature": "Choose Feature",
        "home": "🏠 Home",
        "summarizer": "🧠 AI Notes Summarizer",
        "speech": "🎤 Speech-to-Text",
        "dyslexia": "📖 Dyslexia Mode",
        "quiz": "❓ Quiz Generator",
        "accessibility": "♿ Accessibility Support",
        "summary_button": "Generate Summary"
    }
}

languages = ["English"]

st.sidebar.title("🌐 Language Settings")
selected_language = st.sidebar.selectbox("Language", languages)
lang = translations["English"]

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
    import time

    st.header("🎯 Kahoot-Style Smart Quiz")

    # -------------------------------
    # USER INPUT (FIXED ORDER)
    # -------------------------------
    name = st.text_input("Enter Your Name")
    topic = st.text_input("Enter Topic")

    # -------------------------------
    # INIT SESSION
    # -------------------------------
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "q_index" not in st.session_state:
        st.session_state.q_index = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    # -------------------------------
    # QUESTION GENERATOR (SMART)
    # -------------------------------
    def generate_questions(topic):

        questions = []

        # EASY (10)
        for i in range(10):
            q = {
                "question": f"{i+1}. Which statement correctly explains {topic}?",
                "options": [
                    f"{topic} is used only for entertainment",
                    f"{topic} involves intelligent decision making",
                    f"{topic} has no real-world applications",
                    f"{topic} is unrelated to technology"
                ],
                "answer": f"{topic} involves intelligent decision making"
            }
            questions.append(q)

        # MEDIUM (5)
        for i in range(10, 15):
            q = {
                "question": f"{i+1}. What is a key characteristic of {topic} systems?",
                "options": [
                    "They cannot learn from data",
                    "They adapt based on patterns",
                    "They only follow fixed instructions",
                    "They avoid automation"
                ],
                "answer": "They adapt based on patterns"
            }
            questions.append(q)

        # HARD (5)
        for i in range(15, 20):
            q = {
                "question": f"{i+1}. Which scenario best represents advanced use of {topic}?",
                "options": [
                    "Manual calculations",
                    "Rule-based automation only",
                    "Self-learning predictive systems",
                    "Static database queries"
                ],
                "answer": "Self-learning predictive systems"
            }
            questions.append(q)

        random.shuffle(questions)
        return questions

    # -------------------------------
    # START QUIZ
    # -------------------------------
    if st.button("Start Quiz") and topic and name:
        st.session_state.quiz = generate_questions(topic)
        st.session_state.quiz_started = True
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.start_time = time.time()

    # -------------------------------
    # QUIZ UI
    # -------------------------------
    if st.session_state.quiz_started:

        quiz = st.session_state.quiz
        i = st.session_state.q_index
        q = quiz[i]

        # TIMER
        time_limit = 20
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, time_limit - elapsed)

        st.markdown(f"""
        📍 Question {i+1}/20 | ⏱ Time Left: {remaining}s
        """)

        # QUESTION
        st.subheader(q["question"])

        selected = st.radio(
            "Choose Answer",
            q["options"],
            key=f"q_{i}"
        )

        # -------------------------------
        # SUBMIT
        # -------------------------------
        if st.button("Submit Answer"):

            if selected == q["answer"]:
                st.success("✅ Correct!")
                st.session_state.score += 1
            else:
                st.error("❌ Wrong!")
                st.write(f"✔ Correct Answer: {q['answer']}")

            st.session_state.answers[i] = selected

        # -------------------------------
        # NAVIGATION
        # -------------------------------
        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Previous") and i > 0:
                st.session_state.q_index -= 1
                st.session_state.start_time = time.time()

        with col2:
            if st.button("Next ➡") and i < 19:
                st.session_state.q_index += 1
                st.session_state.start_time = time.time()

        # -------------------------------
        # PROGRESS
        # -------------------------------
        attempted = len(st.session_state.answers)

        st.info(f"📊 Attempted: {attempted}/20")
        st.progress(attempted / 20)

        # -------------------------------
        # FINAL RESULT
        # -------------------------------
        if attempted == 20:
            st.success(f"🏆 Final Score: {st.session_state.score}/20")

            # LEADERBOARD (basic)
            if "leaderboard" not in st.session_state:
                st.session_state.leaderboard = []

            st.session_state.leaderboard.append(
                {"name": name, "score": st.session_state.score}
            )

            st.subheader("🏅 Leaderboard")

            sorted_lb = sorted(
                st.session_state.leaderboard,
                key=lambda x: x["score"],
                reverse=True
            )

            for rank, player in enumerate(sorted_lb, 1):
                st.write(f"{rank}. {player['name']} - {player['score']}")
            
# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("👁️ Blind → Audio + screen reader")
    st.write("👂 Deaf → Text UI")
    st.write("🗣️ Speech impaired → Text input")
    st.write("🦽 Mobility → Large UI")
