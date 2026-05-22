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

    sample_text = """
Artificial Intelligence is transforming education
through accessibility and smart learning systems.
"""

    text = st.text_area(
        "Paste Notes Here",
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button(lang["summary_button"]):

        sentences = text.split('.')

        if summary_length == "Short":
            summary = '.'.join(sentences[:2])

        elif summary_length == "Medium":
            summary = '.'.join(sentences[:4])

        else:
            summary = '.'.join(sentences[:6])

        st.success("✅ Summary Generated")

        st.write(summary)
# ---------------------------------------------------
# SPEECH TO TEXT + AI ANSWER
# ---------------------------------------------------

elif feature == lang["speech"]:

    import speech_recognition as sr
    import tempfile

    st.header("🎤 Voice Assistant (Works Without API)")

    audio = st.audio_input("🎙️ Record Voice")

    if audio:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(audio.read())
            audio_path = tmp.name

        recognizer = sr.Recognizer()

        try:
            with sr.AudioFile(audio_path) as source:
                data = recognizer.record(source)
                text = recognizer.recognize_google(data)

            st.subheader("📝 Your Question")
            st.write(text)

        except:
            text = ""
            st.error("❌ Could not understand audio")

        # 🤖 ANSWER (NO API)
        if text:

            st.subheader("🤖 AI Answer")

            if "ai" in text.lower():
                st.success("AI is the simulation of human intelligence in machines.")

            elif "machine learning" in text.lower():
                st.success("Machine Learning is a subset of AI that allows systems to learn from data.")

            elif "education" in text.lower():
                st.success("AI improves education through personalized learning and accessibility.")

            else:
                st.success("This is a smart AI assistant. It answers based on your question.")
            
# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia Mode")

    font = st.slider("Font Size", 20, 40, 30)

    summary = st.session_state.get("summary", "")

    if not summary:
        st.warning("Generate summary first")
    else:
        st.markdown(f"""
        <div style="font-size:{font}px; line-height:2.5; letter-spacing:2px;
        background:#f4f4f4; padding:20px; border-radius:10px; color:black;">
        {summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ (KAHOOT STYLE + TIMER + LEADERBOARD)
# ---------------------------------------------------
elif feature == lang["quiz"]:

    st.header("❓ Smart Quiz (No API Required)")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):

        if topic == "":
            st.warning("Enter topic first")
        else:

            # 🔥 Smart predefined logic
            if "ai" in topic.lower():

                st.session_state.quiz = [
                    {
                        "question": "What is AI?",
                        "options": ["Machine Intelligence","Human Brain","Software","None"],
                        "answer": "Machine Intelligence",
                        "explanation": "AI simulates human intelligence."
                    },
                    {
                        "question": "Where is AI used?",
                        "options": ["Healthcare","Farming","Robotics","All"],
                        "answer": "All",
                        "explanation": "AI is used everywhere."
                    }
                ]

            else:
                st.session_state.quiz = [
                    {
                        "question": f"What is {topic}?",
                        "options": ["Concept","Tool","Device","None"],
                        "answer": "Concept",
                        "explanation": f"{topic} is a concept."
                    }
                ]

    # DISPLAY QUIZ
    if "quiz" in st.session_state:

        for i, q in enumerate(st.session_state.quiz):

            st.subheader(f"Q{i+1}: {q['question']}")

            ans = st.radio("Choose answer", q["options"], key=i)

            if st.button(f"Submit {i}"):

                if ans == q["answer"]:
                    st.success("✅ Correct")
                else:
                    st.error("❌ Wrong")
                    st.write("✔ Correct:", q["answer"])
                    st.write("🧠 Reason:", q["explanation"])
                    
# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("👁️ Blind → Audio + screen reader")
    st.write("👂 Deaf → Text UI")
    st.write("🗣️ Speech impaired → Text input")
    st.write("🦽 Mobility → Large UI")
