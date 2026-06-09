import streamlit as st
import random
import tempfile
import os
import json
import sqlite3
import hashlib

from datetime import datetime

from openai import OpenAI
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS

import nltk
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# =====================================================
# USER AUTHENTICATION DATABASE
# =====================================================

conn = sqlite3.connect(
    "eduaccess_users.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(

username TEXT PRIMARY KEY,

password TEXT

)
""")

conn.commit()

def make_hash(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()

def register_user(
    username,
    password
):

    c.execute(

        "INSERT INTO users VALUES (?,?)",

        (
            username,
            make_hash(password)
        )
    )

    conn.commit()

def login_user(
    username,
    password
):

    c.execute(

        """
        SELECT *
        FROM users
        WHERE username=?
        AND password=?
        """,

        (
            username,
            make_hash(password)
        )
    )

    return c.fetchone()
    
# --------------------------------------------------
# NLTK DOWNLOAD
# --------------------------------------------------

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:10px;
}

.stButton > button{
    width:100%;
    border-radius:12px;
    height:3em;
    font-weight:bold;
}

.feature-card{
    padding:22px;
    border-radius:20px;
    color:white;
    margin-bottom:20px;
    transition:0.3s;
}

.feature-card:hover{
    transform:scale(1.02);
}

.footer{
    text-align:center;
    color:gray;
    padding:20px;
    font-size:14px;
}

.metric-box{
    padding:20px;
    border-radius:15px;
    text-align:center;
    background:#f0f2f6;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LANGUAGE SUPPORT
# --------------------------------------------------

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
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja"
}

# --------------------------------------------------
# PERSISTENT HISTORY (JSON FILE)
# --------------------------------------------------

HISTORY_FILE = "eduaccess_history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_to_history(category, content):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "content": str(content)
    })
    history = history[-300:]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

font_size = st.sidebar.slider(
    "🔠 Font Size",
    16,
    40,
    23
)

high_contrast = st.sidebar.checkbox(
    "🌗 Dark Contrast Mode"
)

FEATURES = {

    "🏠 Home":"🏠 Home",

    "👤 User Profile":"👤 User Profile",

    "🧠 AI Notes Summarizer":"🧠 AI Notes Summarizer",

    "🎤 Speech-to-Text":"🎤 Speech-to-Text",

    "📖 Dyslexia-Friendly Reading":"📖 Dyslexia-Friendly Reading",

    "❓ AI Quiz Generator":"❓ AI Quiz Generator",

    "📈 Analytics Dashboard":"📈 Analytics Dashboard",

    "♿ Accessibility Support":"♿ Accessibility Support",

    "🧠 AI Personalized Learning":"🧠 AI Personalized Learning",

    "😊 Emotion-Aware Learning":"😊 Emotion-Aware Learning",

    "🚀 AI Career Mentor":"🚀 AI Career Mentor",

    "📜 History":"📜 History"
}


feature = st.sidebar.selectbox(
    "Choose Feature",
    list(FEATURES.keys())
)

# ==========================================
# GLOBAL FONT SIZE
# ==========================================

st.markdown(
    f"""
    <style>

    html,
    body,
    [class*="css"] {{
        font-size: {font_size}px !important;
    }}

    p,
    li,
    div,
    span,
    label,
    .stMarkdown,
    .stText,
    .stRadio,
    .stSelectbox,
    .stButton,
    .stAlert {{
        font-size: {font_size}px !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# TRANSLATION FUNCTION  (defined after selected_language)
# --------------------------------------------------


def translate_text(text):
    if selected_language == "English":
        return text
    try:
        return GoogleTranslator(
            source="auto",
            target=LANGUAGES[selected_language]
        ).translate(text)
    except Exception:
        return text

# ==========================================
# SAFE TRANSLATION
# ==========================================

DO_NOT_TRANSLATE = [

    "Choose Language",
    "Font Size",
    "Dark Contrast Mode",
    "Core Features"
]

def tr(text):

    if text in DO_NOT_TRANSLATE:

        return text

    return translate_text(text)

# --------------------------------------------------
# HIGH CONTRAST MODE
# --------------------------------------------------

if high_contrast:
    st.markdown("""
    <style>
    .stApp{
        background:black;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# LOGIN SESSION
# =====================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = ""

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "summary": "",
    "quiz_generated": False,
    "quiz_score": 0,
    "quiz_questions": [],
    "quiz_history": [],
    "user_answers": {},
    "submitted_questions": set(),
    "speech_history": [],
    "summary_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value
if "logged_in" not in st.session_state:
    st.session_state.logged_in=False

if "username" not in st.session_state:
    st.session_state.username=""

# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.logged_in:

    st.title("🔐 EduAccess AI")

    option = st.radio(

        "Choose Option",

        [
            "Login",
            "Register"
        ]
    )

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if option == "Register":

        if st.button(
            "Create Account"
        ):

            if (
                username.strip() == ""
                or
                password.strip() == ""
            ):

                st.warning(
                    "Enter username and password"
                )

            else:

                try:

                    register_user(
                        username,
                        password
                    )

                    st.success(
                        "Account Created Successfully"
                    )

                except:

                    st.error(
                        "Username already exists"
                    )

    else:

        if st.button(
            "Login"
        ):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True

                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

    st.stop()

# ==================================================
# HOME PAGE
# ==================================================

if feature == "🏠 Home":

    st.title(
        tr("🚀 EduAccess AI")
    )

    st.subheader(
        tr("AI-Powered Accessibility Platform for Students")
    )

    st.success(
        tr("Inclusive AI Learning Ecosystem")
    )

    st.markdown("---")

    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">

        <h2>{tr("🧠 AI Notes Summarizer")}</h2>

        <p>
        {tr("Generate concise AI-powered summaries from notes and PDFs.")}
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#16a34a,#166534);">

        <h2>{tr("🎤 Speech-to-Text")}</h2>

        <p>
        {tr("Convert spoken language into text with multilingual support.")}
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#f59e0b,#b45309);">

        <h2>{tr("📖 Dyslexia-Friendly Reading")}</h2>

        <p>
        {tr("Accessible reading mode with improved readability.")}
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">

        <h2>{tr("❓ AI Quiz Generator")}</h2>

        <p>
        {tr("Adaptive quizzes with Easy, Medium and Hard levels.")}
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header(
        tr("🚀 Advanced AI Features")
    )

    advanced_features = [

        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor",
        "🌍 Multi-language Support",
        "♿ Accessibility Features"
    ]

    for item in advanced_features:
        st.info(tr(item))

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(tr("🌍 Languages"), "15+")

    with c2:
        st.metric(tr("⚙️ Features"), "5+")

    with c3:
        st.metric(tr("🚀 AI Modules"), "5")

    st.markdown("---")

    st.header(
        tr("🎯 Why EduAccess AI?")
    )

    st.success(
        tr(
            """
✅ Helps students learn faster and smarter

✅ Supports 15+ languages for inclusive learning

✅ AI-powered Notes Summarization

✅ Speech-to-Text with Voice Assistance

✅ Dyslexia-Friendly Reading Support

✅ Adaptive Quiz Generation

✅ Personalized Learning Recommendations

✅ Emotion-Aware Learning Guidance

✅ AI Career Mentorship and Roadmaps

✅ Accessibility-focused educational ecosystem
"""
        )
    )

# =====================================================
# USER PROFILE
# =====================================================

elif feature == "👤 User Profile":

    st.header("👤 User Profile")

    st.success(

        f"Welcome {st.session_state.username}"

    )

    st.write(

        f"Username: {st.session_state.username}"

    )

    st.write(

        f"Account Type: Student"

    )

    if st.button(
        "Logout"
    ):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.rerun()

# ==================================================
# AI NOTES SUMMARIZER
# ==================================================

elif feature == "🧠 AI Notes Summarizer":

    st.header(translate_text("🧠 AI Notes Summarizer"))

    uploaded_file = st.file_uploader(
        translate_text("Upload PDF"),
        type=["pdf"]
    )

    text = ""

    if uploaded_file:
        try:
            pdf = PdfReader(uploaded_file)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            st.success(translate_text("PDF Loaded Successfully"))
        except Exception as e:
            st.error(f"PDF Error: {e}")

    text = st.text_area(
        translate_text("Paste Notes"),
        value=text,
        height=300
    )

    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    length_idx = st.selectbox(
        translate_text("Summary Length"),
        range(len(LENGTH_OPTIONS)),
        format_func=lambda i: translate_text(LENGTH_OPTIONS[i])
    )
    summary_length = LENGTH_OPTIONS[length_idx]

    if st.button(translate_text("🚀 Generate Summary")):

        if text.strip() == "":
            st.warning(translate_text("Please enter or upload notes."))
        else:
            sentences = text.split(".")

            if summary_length == "Short":
                count = min(5, len(sentences))
            elif summary_length == "Medium":
                count = min(10, len(sentences))
            else:
                count = min(20, len(sentences))

            final_summary = ".".join(sentences[:count])
            final_summary = translate_text(final_summary)

            st.session_state.summary = final_summary
            st.session_state.summary_history.append(final_summary)

            save_to_history(
                "📝 Notes Summary",
                final_summary
            )

            st.success(translate_text("Summary Generated Successfully"))
            st.write(final_summary)

# ==================================================
# SPEECH TO TEXT
# ==================================================

elif feature == "🎤 Speech-to-Text":

    st.header(translate_text("🎤 Speech-to-Text"))

    st.write(translate_text("Ask a question using your microphone."))

    audio = st.audio_input(translate_text("🎙️ Record Question"))

    if audio:
        try:
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ) as tmp:
                tmp.write(audio.read())
                audio_path = tmp.name

            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)

            question = recognizer.recognize_google(
                audio_data,
                language=LANGUAGES[selected_language]
            )

            st.success(translate_text("Question Recognized"))
            st.subheader(translate_text("📝 Your Question"))
            st.info(question)

            q = question.lower()

            if "python" in q:
                answer = translate_text(
                    "Python is a high-level programming language known for simplicity, readability and powerful libraries."
                )

            elif "artificial intelligence" in q or "ai" in q:
                answer = translate_text(
                    "Artificial Intelligence enables machines to learn, reason, make decisions and perform tasks that usually require human intelligence."
                )

            elif "machine learning" in q:
                answer = translate_text(
                    "Machine Learning is a branch of AI where systems learn patterns from data and improve automatically."
                )

            elif "dbms" in q:
                answer = translate_text(
                    "DBMS stands for Database Management System. It helps store, retrieve and manage data efficiently."
                )

            else:
                answer = translate_text(
                    f"Topic: {question}\n\nThis topic is important for academic and professional learning.\n\nStudy the fundamentals, solve practice questions and build projects related to this topic."
                )

            st.subheader(translate_text("🤖 AI Answer"))
            st.success(answer)

            lang_code = LANGUAGES[selected_language]
            try:
                tts = gTTS(text=answer, lang=lang_code)
            except Exception:
                tts = gTTS(text=answer, lang="en")

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            ) as fp:
                tts.save(fp.name)
                with open(fp.name, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")

            st.session_state.speech_history.append({
                "question": question,
                "answer": answer
            })

            save_to_history(
                "🎤 Speech Q&A",
                f"Q: {question}\nA: {answer}"
            )

        except Exception as e:
            st.error(translate_text("Speech Error") + f": {e}")

# ==================================================
# DYSLEXIA FRIENDLY READING
# ==================================================

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header(translate_text("📖 Dyslexia-Friendly Reading"))

    if st.session_state.summary == "":
        st.warning(translate_text("Generate a summary first using the AI Notes Summarizer."))
    else:
        st.markdown(
            f"""
            <div style="
            line-height:2.5;
            letter-spacing:2px;
            font-size:{font_size}px;
            padding:25px;
            background:#f4f4f4;
            color:black;
            border-radius:15px;
            ">
            {st.session_state.summary}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.success(translate_text("Reading mode activated."))

# ==================================================
# QUIZ GENERATOR
# ==================================================

elif feature == "❓ AI Quiz Generator":

    st.header(
        translate_text(
            "❓ AI Adaptive Quiz Generator"
        )
    )

    topic = st.text_input(
        translate_text(
            "📘 Enter Subject"
        )
    )

    difficulty = st.selectbox(
        translate_text(
            "🎯 Difficulty"
        ),
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    num_questions = st.slider(
        translate_text(
            "📊 Number of Questions"
        ),
        1,
        30,
        10
    )

    if st.button(
        translate_text(
            "🚀 Generate Quiz"
        )
    ):

        if topic.strip() == "":

            st.warning(
                translate_text(
                    "Please enter a subject."
                )
            )

        else:

            with st.spinner(
                "Generating Quiz..."
            ):

                st.session_state.quiz_questions = (
                    generate_questions(
                        topic,
                        difficulty,
                        num_questions
                    )
                )

                st.session_state.quiz_generated = True

    if (
        st.session_state.quiz_generated
        and
        st.session_state.quiz_questions
    ):

        answers = {}

        st.markdown("---")

        for idx, q in enumerate(
            st.session_state.quiz_questions
        ):

            st.subheader(
                f"Question {idx+1}"
            )

            st.write(
                q["question"]
            )

            answers[idx] = st.radio(
                "Choose Answer",
                q["options"],
                key=f"quiz_{idx}"
            )

        if st.button(
            "✅ Submit Quiz"
        ):

            score = 0

            review = []

            for idx, q in enumerate(
                st.session_state.quiz_questions
            ):

                user_answer = answers[idx]

                correct = (
                    user_answer
                    ==
                    q["answer"]
                )

                if correct:
                    score += 2

                review.append({

                    "question":
                    q["question"],

                    "options":
                    q["options"],

                    "user_answer":
                    user_answer,

                    "correct_answer":
                    q["answer"],

                    "is_correct":
                    correct,

                    "explanation":
                    q["explanation"]
                })

            total = (
                len(
                    st.session_state.quiz_questions
                ) * 2
            )

            percentage = (
                score / total
            ) * 100

            st.success(
                f"🏆 Score: {score}/{total}"
            )

            st.info(
                f"📊 Percentage: {percentage:.2f}%"
            )

            save_to_history(
                "Quiz",
                {
                    "topic": topic,
                    "difficulty": difficulty,
                    "score": f"{score}/{total}",
                    "percentage": percentage,
                    "questions": review
                }
            )

            st.markdown("---")

            st.subheader(
                "📖 Answer Review"
            )

            for item in review:

                st.write(
                    f"### ❓ {item['question']}"
                )

                st.write(
                    f"Your Answer: {item['user_answer']}"
                )

                st.write(
                    f"Correct Answer: {item['correct_answer']}"
                )

                if item["is_correct"]:

                    st.success(
                        "✅ Correct"
                    )

                else:

                    st.error(
                        "❌ Incorrect"
                    )

                st.info(
                    item["explanation"]
                )

                st.markdown("---")

# ==================================================
# ACCESSIBILITY SUPPORT
# ==================================================

elif feature == "♿ Accessibility Support":

    st.header(
        translate_text(
            "♿ Accessibility Support"
        )
    )

    st.success(
        translate_text(
            "🌍 Multi-language Support"
        )
    )

    st.success(
        translate_text(
            "🔠 Adjustable Font Size"
        )
    )

    st.success(
        translate_text(
            "🌗 High Contrast Mode"
        )
    )

    st.success(
        translate_text(
            "📖 Dyslexia Reading Mode"
        )
    )

    st.success(
        translate_text(
            "🎤 Speech Assistance"
        )
    )

    st.markdown("---")

    st.info(
        translate_text(
            "Use the sidebar to change language, font size and accessibility settings."
        )
    )

    st.markdown("---")

    st.subheader(
        translate_text(
            "Why Accessibility Matters?"
        )
    )

    st.write(
        translate_text(
            "Accessibility ensures that every learner, including students with visual, hearing, language or learning difficulties, can access education equally."
        )
    )

# ==================================================
# AI PERSONALIZED LEARNING
# ==================================================

elif feature == "🧠 AI Personalized Learning":

    st.header(translate_text("🧠 AI Personalized Learning"))

    weak_topic = st.text_input(translate_text("📘 Enter Weak Topic"))

    STYLE_OPTIONS = ["Visual", "Theory", "Practical", "Interactive"]
    style_idx = st.selectbox(
        translate_text("🎯 Preferred Learning Style"),
        range(len(STYLE_OPTIONS)),
        format_func=lambda i: translate_text(STYLE_OPTIONS[i])
    )
    learning_style = STYLE_OPTIONS[style_idx]

    if st.button(translate_text("🚀 Generate Recommendations")):

        if weak_topic.strip() == "":
            st.warning(translate_text("⚠️ Please enter a topic"))
        else:
            st.success(
                translate_text(f"AI detected weak understanding in {weak_topic}")
            )

            st.markdown("---")

            st.subheader(translate_text("📘 Practice Resources"))

            st.markdown(f"""
🔗 https://www.google.com/search?q=GeeksforGeeks+{weak_topic}+quiz

🔗 https://www.google.com/search?q={weak_topic}+MCQ+questions
""")

            st.markdown("---")

            st.subheader(translate_text("🎥 Best YouTube Tutorials"))

            st.markdown(f"""
▶️ https://www.youtube.com/results?search_query={weak_topic}+full+course

▶️ https://www.youtube.com/results?search_query=learn+{weak_topic}+for+beginners
""")

            st.markdown("---")

            st.subheader(translate_text("📅 Daily Revision Plan"))

            st.info(translate_text(f"""
Revise {weak_topic} daily
Solve practice questions
Watch one tutorial everyday
Create handwritten notes
Weekly revision
"""))

            st.markdown("---")

            st.subheader(translate_text("📊 Visual Learning"))

            st.markdown(f"""
🔗 https://www.google.com/search?q={weak_topic}+diagram

🔗 https://www.google.com/search?q={weak_topic}+infographics
""")

            save_to_history(
                "🧠 Personalized Learning",
                f"Topic: {weak_topic} | Style: {learning_style}"
            )

# ==================================================
# EMOTION-AWARE LEARNING
# ==================================================

elif feature == "😊 Emotion-Aware Learning":

    st.header(translate_text("😊 Emotion-Aware Learning"))

    EMOTION_OPTIONS = ["Confused", "Focused", "Stressed", "Tired"]
    emotion_idx = st.selectbox(
        translate_text("💭 How are you feeling?"),
        range(len(EMOTION_OPTIONS)),
        format_func=lambda i: translate_text(EMOTION_OPTIONS[i])
    )
    emotion = EMOTION_OPTIONS[emotion_idx]

    if st.button(translate_text("🧠 Analyze Emotion")):

        st.markdown("---")

        if emotion == "Confused":
            st.warning(translate_text("AI detected confusion in learning."))
            st.subheader(translate_text("🎥 Beginner Tutorials"))
            st.markdown("""
▶️ https://www.youtube.com/results?search_query=beginner+programming+tutorials

▶️ https://www.youtube.com/results?search_query=easy+computer+science+tutorials
""")
            st.info(translate_text(
                "Start from basics. Watch visual tutorials. Practice beginner quizzes. Revise concepts slowly."
            ))

        elif emotion == "Focused":
            st.success(translate_text("AI detected high focus level."))
            st.subheader(translate_text("🚀 Advanced Recommendations"))
            st.markdown("""
▶️ https://www.youtube.com/results?search_query=advanced+programming+projects

🔗 https://www.geeksforgeeks.org/
""")
            st.info(translate_text(
                "Build projects. Practice coding. Learn advanced concepts. Attempt difficult quizzes."
            ))

        elif emotion == "Stressed":
            st.error(translate_text("AI detected stress."))
            st.subheader(translate_text("🧘 Relaxation Resources"))
            st.markdown("""
▶️ https://www.youtube.com/results?search_query=student+stress+management

▶️ https://www.youtube.com/results?search_query=study+motivation
""")
            st.info(translate_text(
                "Take short breaks. Sleep properly. Reduce pressure. Practice mindfulness."
            ))

        else:
            st.info(translate_text("AI detected tiredness."))
            st.subheader(translate_text("😴 Recovery Suggestions"))
            st.markdown("""
▶️ https://www.youtube.com/results?search_query=focus+music+for+studying

▶️ https://www.youtube.com/results?search_query=study+motivation
""")
            st.info(translate_text(
                recommendation_text = """
Take short breaks.
Sleep properly.
Reduce pressure.
Practice mindfulness.
"""
            ))

        save_to_history(
    "😊 Emotion Check",
    {

        "emotion": emotion,

        "recommendation":
        recommendation_text
    }
)

# ==================================================
# AI CAREER MENTOR
# ==================================================

elif feature == "🚀 AI Career Mentor":

    st.header(translate_text("🚀 AI Career Mentor"))

    career_query = st.text_input(translate_text("💬 Ask Career Guidance"))

    st.markdown(f"""
### 💡 {translate_text("Sample Questions")}

• {translate_text("How to become Data Scientist")}

• {translate_text("AI Engineer roadmap")}

• {translate_text("Web Development roadmap")}

• {translate_text("Best AI projects")}

• {translate_text("Skills for Cybersecurity")}
""")

    if st.button(translate_text("🚀 Get Guidance")):

        query = career_query.lower()

        st.markdown("---")

        if "data science" in query or "data scientist" in query:

            st.success(translate_text("📊 Data Science Career Roadmap"))

            st.subheader(translate_text("🛠️ Skills Required"))
            st.info(translate_text("Python, SQL, Machine Learning, Power BI, Statistics"))

            st.subheader(translate_text("📚 Best Courses"))
            st.markdown("""
🔗 https://www.coursera.org/

🔗 https://www.udemy.com/

🔗 https://www.geeksforgeeks.org/data-science-for-beginners/
""")

            st.subheader(translate_text("🎥 YouTube Tutorials"))
            st.markdown("▶️ https://www.youtube.com/results?search_query=data+science+full+course")

        elif "ai" in query or "machine learning" in query:

            st.success(translate_text("🤖 AI / ML Career Roadmap"))

            st.subheader(translate_text("🛠️ Skills Required"))
            st.info(translate_text("Python, Machine Learning, Deep Learning, NLP, Computer Vision"))

            st.subheader(translate_text("🎥 Learning Resources"))
            st.markdown("""
▶️ https://www.youtube.com/results?search_query=machine+learning+full+course

🔗 https://www.geeksforgeeks.org/machine-learning/
""")

        elif "web" in query:

            st.success(translate_text("🌐 Web Development Roadmap"))

            st.subheader(translate_text("🛠️ Skills Required"))
            st.info(translate_text("HTML, CSS, JavaScript, React, Node.js"))

            st.subheader(translate_text("🎥 Tutorials"))
            st.markdown("▶️ https://www.youtube.com/results?search_query=web+development+full+course")

        elif "cybersecurity" in query or "cyber" in query:

            st.success(translate_text("🔐 Cybersecurity Career Roadmap"))

            st.subheader(translate_text("🛠️ Skills Required"))
            st.info(translate_text("Networking, Linux, Python, Ethical Hacking, Cryptography"))

            st.subheader(translate_text("🎥 Tutorials"))
            st.markdown("▶️ https://www.youtube.com/results?search_query=cybersecurity+full+course")

        else:

            st.info(translate_text(
                "Build real-world projects. Improve GitHub profile. Practice DSA. Learn deployment. Build LinkedIn presence."
            ))

        save_to_history(
    "🚀 Career Query",
    {

        "query": career_query,

        "career_guidance":
        generated_guidance
    }
)

# ==================================================
# HISTORY
# ==================================================

elif feature == "📜 History":

    st.header(translate_text("📜 Your Learning History"))

    history = load_history()

    if not history:

        st.info(
            translate_text(
                "No history available yet."
            )
        )

    else:

        st.success(
            f"📊 Total Records: {len(history)}"
        )

        st.markdown("---")

        categories = ["All"]

        for item in history:

            category = item.get(
                "category",
                "Unknown"
            )

            if category not in categories:

                categories.append(
                    category
                )

        selected_category = st.selectbox(
            translate_text(
                "📂 Filter by Category"
            ),
            categories
        )

        if selected_category == "All":

            filtered_history = history

        else:

            filtered_history = [
                item
                for item in history
                if item.get("category")
                == selected_category
            ]

        st.markdown("---")

        for record in reversed(filtered_history):

            category = record.get(
                "category",
                "Unknown"
            )

            timestamp = record.get(
                "timestamp",
                "N/A"
            )

            with st.expander(
                f"📌 {category} | {timestamp}"
            ):

                if category == "Quiz":

                    st.subheader(
                        "❓ Quiz Attempt"
                    )

                    st.write(
                        f"📘 Topic: {record.get('topic', 'N/A')}"
                    )

                    st.write(
                        f"🎯 Difficulty: {record.get('difficulty', 'N/A')}"
                    )

                    st.write(
                        f"🏆 Score: {record.get('score', 'N/A')}"
                    )

                    if "percentage" in record:

                        st.write(
                            f"📊 Percentage: {record['percentage']:.2f}%"
                        )

                    questions = record.get(
                        "questions",
                        []
                    )

                    for idx, q in enumerate(
                        questions,
                        start=1
                    ):

                        st.markdown("---")

                        st.markdown(
                            f"### Question {idx}"
                        )

                        st.write(
                            q.get(
                                "question",
                                ""
                            )
                        )

                        options = q.get(
                            "options",
                            []
                        )

                        if options:

                            st.write(
                                "Options:"
                            )

                            for option in options:

                                st.write(
                                    f"• {option}"
                                )

                        st.success(
                            f"Your Answer: {q.get('user_answer', '')}"
                        )

                        st.info(
                            f"Correct Answer: {q.get('correct_answer', '')}"
                        )

                        if q.get(
                            "is_correct",
                            False
                        ):

                            st.success(
                                "✅ Correct"
                            )

                        else:

                            st.error(
                                "❌ Incorrect"
                            )

                        st.warning(
                            f"Explanation: {q.get('explanation', '')}"
                        )

                else:

                    st.write(
                        record.get(
                            "content",
                            ""
                        )
                    )

        st.markdown("---")

        if st.button(
            translate_text(
                "🗑️ Clear All History"
            )
        ):

            try:

                if os.path.exists(
                    HISTORY_FILE
                ):

                    os.remove(
                        HISTORY_FILE
                    )

                st.success(
                    translate_text(
                        "History Cleared Successfully"
                    )
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )
                
# ==================================================
# FOOTER
# ==================================================

st.markdown(
    f"""
    <div class='footer'>
    {translate_text("Made with")} ❤️ {translate_text("using Streamlit")} | EduAccess AI
    </div>
    """,
    unsafe_allow_html=True
)
