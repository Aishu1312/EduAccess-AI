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
    st.write("Inclusive AI learning platform for all students.")

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    text = st.text_area("Paste Notes Here")

    if st.button("Generate Summary"):

        sentences = [s.strip() for s in text.split('.') if s.strip()]
        summary = ". ".join(sentences[:4])

        st.session_state.summary = summary

        st.success("Summary Generated")
        st.write(summary)

# ---------------------------------------------------
# SPEECH TO TEXT + AI ANSWER
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header("🎤 Speech-to-Text + AI Answer")

    audio = st.audio_input("Record Voice")
    file = st.file_uploader("Upload Audio", type=["wav","mp3"])

    source = audio if audio else file

    if source:

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(source.read())
            path = tmp.name

        if "OPENAI_API_KEY" not in st.secrets:
            st.warning("Demo Mode")
            text = "What is AI?"
        else:
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with open(path, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=f
                )
            text = transcript.text

        st.write("📝", text)

        if "OPENAI_API_KEY" in st.secrets:
            res = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": text}]
            )
            st.success(res.choices[0].message.content)

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

    st.header("❓ AI Quiz (Kahoot Style)")

    name = st.text_input("Enter Your Name")
    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):

        if "OPENAI_API_KEY" not in st.secrets:
            st.error("API key missing")
        else:
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            prompt = f"""
            Generate 3 MCQ questions on {topic} in JSON format.
            """

            res = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )

            try:
                quiz = json.loads(res.choices[0].message.content)
                st.session_state.quiz = quiz
                st.session_state.score = 0
            except:
                st.error("Error generating quiz")

    if "quiz" in st.session_state:

        for i, q in enumerate(st.session_state.quiz):

            st.subheader(q["question"])

            start = time.time()

            ans = st.radio("Choose", q["options"], key=i)

            if st.button(f"Submit {i}"):

                time_taken = int(time.time() - start)

                if ans == q["answer"]:
                    st.success(f"Correct! ⏱️ {time_taken}s")
                    st.session_state.score += 1
                else:
                    st.error("Wrong")
                    st.write("Correct:", q["answer"])
                    st.write("Explanation:", q["explanation"])

        if st.button("Finish Quiz"):

            st.success(f"Final Score: {st.session_state.score}")

            st.session_state.leaderboard.append(
                {"name": name, "score": st.session_state.score}
            )

    # LEADERBOARD
    if st.session_state.leaderboard:

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
