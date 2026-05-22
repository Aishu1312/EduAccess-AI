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

    import tempfile
    import openai

    st.header("🎤 Ask Anything (Voice AI Assistant)")

    st.write("Speak or upload audio and get intelligent answers.")

    # INPUT OPTIONS
    audio = st.audio_input("🎙️ Record Voice")
    file = st.file_uploader("📂 Upload Audio", type=["wav","mp3","m4a"])

    source = audio if audio else file

    if source:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(source.read())
            path = tmp.name

        # ---------------- TRANSCRIPTION ---------------- #

        try:
            if "OPENAI_API_KEY" not in st.secrets:
                raise Exception("No API Key")

            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with open(path, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=f
                )

            user_text = transcript.text

        except Exception:
            # 🔥 fallback if API fails
            st.warning("⚠️ Could not transcribe audio. Please try again or check API key.")
            user_text = ""

        # ---------------- SHOW QUESTION ---------------- #

        if user_text:
            st.subheader("📝 Your Question")
            st.write(user_text)

            # ---------------- AI ANSWER ---------------- #

            try:
                if "OPENAI_API_KEY" not in st.secrets:
                    raise Exception("No API Key")

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful AI tutor. Give clear, simple, educational answers."
                        },
                        {
                            "role": "user",
                            "content": user_text
                        }
                    ]
                )

                answer = response.choices[0].message.content

                st.subheader("🤖 AI Answer")
                st.success(answer)

            except Exception:
                # 🔥 SMART DEMO RESPONSE (dynamic)
                st.subheader("🤖 AI Answer")

                demo_answer = f"""
You asked: "{user_text}"

This is a demo response because API is not configured.

Answer:
Artificial Intelligence (AI) is the simulation of human intelligence in machines.
It is used in healthcare, education, robotics, and automation.

👉 Add your OpenAI API key to get real AI answers.
"""
                st.info(demo_answer)

        else:
            st.error("❌ No speech detected. Try speaking clearly.")
            
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

    import openai, json, time

    st.header("❓ Kahoot Style AI Quiz")

    name = st.text_input("Enter Your Name")
    topic = st.text_input("Enter Topic")

    if st.button("🎯 Generate Quiz"):

        if "OPENAI_API_KEY" not in st.secrets:
            st.warning("Demo Quiz Mode")

            st.session_state.quiz = [
                {
                    "question": f"What is {topic}?",
                    "options": ["Definition","Tool","Language","None"],
                    "answer": "Definition",
                    "explanation": f"{topic} is a concept."
                },
                {
                    "question": f"Where is {topic} used?",
                    "options": ["Healthcare","Cooking","Sports","None"],
                    "answer": "Healthcare",
                    "explanation": f"{topic} is widely used in healthcare."
                }
            ]

        else:
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]

                prompt = f"""
                Create 3 MCQs on {topic}.
                Format JSON:
                [{{"question":"","options":[],"answer":"","explanation":""}}]
                """

                res = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                st.session_state.quiz = json.loads(res.choices[0].message.content)
                st.session_state.score = 0

            except:
                st.error("API failed → switching to demo")

    # ---------------- QUIZ PLAY ---------------- #

    if "quiz" in st.session_state:

        for i, q in enumerate(st.session_state.quiz):

            st.subheader(f"Q{i+1}: {q['question']}")

            start_time = time.time()

            ans = st.radio("Choose answer", q["options"], key=f"q{i}")

            if st.button(f"Submit Q{i+1}", key=f"btn{i}"):

                time_taken = int(time.time() - start_time)

                if ans == q["answer"]:
                    st.success(f"✅ Correct (⏱ {time_taken}s)")
                    st.session_state.score += 1
                else:
                    st.error("❌ Wrong")
                    st.write("✔ Correct:", q["answer"])
                    st.write("🧠 Reason:", q["explanation"])

            st.markdown("---")

        # 🏁 FINAL SCORE
        if st.button("🏁 Finish Quiz"):

            st.success(f"Final Score: {st.session_state.score}")

            if name:
                if "leaderboard" not in st.session_state:
                    st.session_state.leaderboard = []

                st.session_state.leaderboard.append({
                    "name": name,
                    "score": st.session_state.score
                })

    # 🏆 LEADERBOARD
    if "leaderboard" in st.session_state:

        st.header("🏆 Leaderboard")

        sorted_board = sorted(
            st.session_state.leaderboard,
            key=lambda x: x["score"],
            reverse=True
        )

        for i, entry in enumerate(sorted_board):
            st.write(f"{i+1}. {entry['name']} - {entry['score']}")
# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("👁️ Blind → Audio + screen reader")
    st.write("👂 Deaf → Text UI")
    st.write("🗣️ Speech impaired → Text input")
    st.write("🦽 Mobility → Large UI")
