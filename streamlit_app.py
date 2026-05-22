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

    st.header("❓ Smart Quiz Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Start Quiz"):

        quiz = []

        # 🔹 BASIC (10)
        basic_questions = [
            ("What does AI stand for?", ["Artificial Intelligence", "Automated Input", "Advanced Interface", "None"], "Artificial Intelligence"),
            ("Which language is popular for AI?", ["Python", "HTML", "CSS", "SQL"], "Python"),
            ("AI is used in?", ["Healthcare", "Education", "Robotics", "All of the above"], "All of the above"),
            ("Which is an AI assistant?", ["Siri", "Calculator", "Notepad", "Paint"], "Siri"),
            ("AI works using?", ["Data", "Guessing", "Magic", "Luck"], "Data"),
        ]

        # 🔹 MEDIUM (5)
        medium_questions = [
            ("Machine Learning is a subset of?", ["AI", "Web Dev", "Networking", "Database"], "AI"),
            ("Which library is used in Python for ML?", ["Scikit-learn", "Bootstrap", "React", "Flask"], "Scikit-learn"),
            ("Supervised learning uses?", ["Labeled data", "No data", "Random data", "Images only"], "Labeled data"),
            ("Which is not AI?", ["Calculator", "Chatbot", "Robot", "Voice Assistant"], "Calculator"),
            ("Neural networks are inspired by?", ["Human brain", "Computer chips", "Internet", "Robots"], "Human brain"),
        ]

        # 🔹 HARD (5)
        hard_questions = [
            ("What is overfitting?", [
                "Model learns noise",
                "Model is perfect",
                "Model ignores data",
                "None"
            ], "Model learns noise"),

            ("Bias in AI means?", [
                "Unfair results",
                "Fast processing",
                "Correct output",
                "None"
            ], "Unfair results"),

            ("Deep Learning uses?", [
                "Neural networks",
                "HTML",
                "Excel",
                "PowerPoint"
            ], "Neural networks"),

            ("Which is NLP task?", [
                "Text analysis",
                "Image editing",
                "Video rendering",
                "None"
            ], "Text analysis"),

            ("AI ethics deals with?", [
                "Fairness & safety",
                "Coding speed",
                "Hardware",
                "None"
            ], "Fairness & safety"),
        ]

        # 👉 Combine + add numbering
        all_questions = basic_questions + medium_questions + hard_questions

        for i, (q, opts, ans) in enumerate(all_questions):
            quiz.append({
                "question": f"{i+1}. {q}",
                "options": opts,
                "answer": ans
            })

        st.session_state["quiz"] = quiz
        st.session_state["q_index"] = 0
        st.session_state["score"] = 0

    # 🚀 RUN QUIZ
    if "quiz" in st.session_state:

        q_index = st.session_state["q_index"]
        quiz = st.session_state["quiz"]

        if q_index < len(quiz):

            q = quiz[q_index]

            st.subheader(q["question"])

            user_ans = st.radio(
                "Choose Answer",
                q["options"],
                key=f"q_{q_index}"
            )

            if st.button("Submit Answer"):

                if user_ans == q["answer"]:
                    st.success("✅ Correct!")
                    st.session_state["score"] += 1
                else:
                    st.error("❌ Wrong")
                    st.write(f"✔ Correct Answer: {q['answer']}")

                st.session_state["q_index"] += 1

        else:
            st.success(f"🎉 Quiz Completed! Score: {st.session_state['score']}/20")
            
# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("👁️ Blind → Audio + screen reader")
    st.write("👂 Deaf → Text UI")
    st.write("🗣️ Speech impaired → Text input")
    st.write("🦽 Mobility → Large UI")
