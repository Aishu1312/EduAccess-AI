import streamlit as st
import json
import random
import tempfile
import os
import sqlite3
import hashlib
from datetime import datetime
from reportlab.pdfgen import canvas
from openai import OpenAI
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS
import nltk

# Initialize OpenAI Client
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
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    c.execute(
        "INSERT INTO users VALUES (?,?)",
        (username, make_hash(password))
    )
    conn.commit()

def login_user(username, password):
    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, make_hash(password))
    )
    return c.fetchone()

# =====================================================
# USER HISTORY MANAGEMENT
# =====================================================

def get_history_file():
    username = st.session_state.get("username", "guest")
    return f"history_{username}.json"

def load_history():
    history_file = get_history_file()
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    history_file = get_history_file()
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def save_to_history(category, content):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "content": str(content)
    })
    history = history[-500:]  # Keep last 500 records
    save_history(history)

def save_quiz_history(topic, difficulty, score, percentage, review):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": "Quiz",
        "topic": topic,
        "difficulty": difficulty,
        "score": score,
        "percentage": percentage,
        "questions": review
    })
    save_history(history)

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

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.main{ padding-top:10px; }
.stButton > button{ width:100%; border-radius:12px; height:3em; font-weight:bold; }
.feature-card{ padding:22px; border-radius:20px; color:white; margin-bottom:20px; transition:0.3s; }
.feature-card:hover{ transform:scale(1.02); }
.footer{ text-align:center; color:gray; padding:20px; font-size:14px; }
.metric-box{ padding:20px; border-radius:15px; text-align:center; background:#f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LANGUAGE SUPPORT
# --------------------------------------------------

LANGUAGES = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu",
    "Punjabi": "pa", "Bengali": "bn", "Tamil": "ta", "Telugu": "te",
    "Kannada": "kn", "Malayalam": "ml", "Urdu": "ur", "Spanish": "es",
    "French": "fr", "German": "de", "Japanese": "ja"
}

# --------------------------------------------------
# SIDEBAR SETTINGS
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")

selected_language = st.sidebar.selectbox(
    "🌍 Choose Language",
    list(LANGUAGES.keys())
)

font_size = st.sidebar.slider(
    "🔠 Font Size",
    16, 40, 23
)

high_contrast = st.sidebar.checkbox(
    "🌗 Dark Contrast Mode"
)

FEATURES = {
    "🏠 Home": "🏠 Home",
    "👤 User Profile": "👤 User Profile",
    "🧠 AI Notes Summarizer": "🧠 AI Notes Summarizer",
    "🎤 Speech-to-Text": "🎤 Speech-to-Text",
    "📖 Dyslexia-Friendly Reading": "📖 Dyslexia-Friendly Reading",
    "❓ AI Quiz Generator": "❓ AI Quiz Generator",
    "📈 Analytics Dashboard": "📈 Analytics Dashboard",
    "♿ Accessibility Support": "♿ Accessibility Support",
    "🧠 AI Personalized Learning": "🧠 AI Personalized Learning",
    "😊 Emotion-Aware Learning": "😊 Emotion-Aware Learning",
    "🚀 AI Career Mentor": "🚀 AI Career Mentor",
    "📜 History": "📜 History"
}

feature = st.sidebar.selectbox(
    "Choose Feature",
    list(FEATURES.keys())
)

# ==========================================
# GLOBAL FONT SIZE & CONTRAST
# ==========================================

st.markdown(
    f"""
    <style>
    html, body, [class*="css"] {{ font-size: {font_size}px !important; }}
    p, li, div, span, label, .stMarkdown, .stText, .stRadio, .stSelectbox, .stButton, .stAlert {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if high_contrast:
    st.markdown("""
    <style>
    .stApp{ background:black; color:white; }
    </style>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# TRANSLATION FUNCTIONS
# --------------------------------------------------

def translate_text(text):
    if selected_language == "English" or not text:
        return text
    try:
        return GoogleTranslator(
            source="auto",
            target=LANGUAGES[selected_language]
        ).translate(text)
    except Exception:
        return text

DO_NOT_TRANSLATE = ["Choose Language", "Font Size", "Dark Contrast Mode", "Core Features"]

def tr(text):
    if text in DO_NOT_TRANSLATE:
        return text
    return translate_text(text)

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

defaults = {
    "logged_in": False,
    "username": "",
    "learning_streak": 0,
    "topics_learned": [],
    "summary": "",
    "quiz_generated": False,
    "quiz_score": 0,
    "quiz_questions": [],
    "user_answers": {},
    "speech_history": [],
    "summary_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =====================================================
# AUTHENTICATION UI
# =====================================================

if not st.session_state.logged_in:
    st.title("🔐 EduAccess AI")
    auth_option = st.radio("Choose Option", ["Login", "Register"])
    auth_user = st.text_input("Username")
    auth_pass = st.text_input("Password", type="password")

    if auth_option == "Register":
        if st.button("Create Account"):
            if auth_user.strip() == "" or auth_pass.strip() == "":
                st.warning("Enter username and password")
            else:
                try:
                    register_user(auth_user, auth_pass)
                    st.success("Account Created Successfully")
                except Exception:
                    st.error("Username already exists")
    else:
        if st.button("Login"):
            user = login_user(auth_user, auth_pass)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = auth_user
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# ==================================================
# FEATURE ROUTING
# ==================================================

# --- HOME ---
if feature == "🏠 Home":
    st.title(tr("🚀 EduAccess AI"))
    st.subheader(tr("AI-Powered Accessibility Platform for Students"))
    st.success(tr("Inclusive AI Learning Ecosystem"))
    st.markdown("---")
    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="feature-card" style="background:linear-gradient(135deg,#2563eb,#1e3a8a);"><h2>{tr("🧠 AI Notes Summarizer")}</h2><p>{tr("Generate concise AI-powered summaries from notes and PDFs.")}</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-card" style="background:linear-gradient(135deg,#16a34a,#166534);"><h2>{tr("🎤 Speech-to-Text")}</h2><p>{tr("Convert spoken language into text with multilingual support.")}</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="feature-card" style="background:linear-gradient(135deg,#f59e0b,#b45309);"><h2>{tr("📖 Dyslexia-Friendly Reading")}</h2><p>{tr("Accessible reading mode with improved readability.")}</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="feature-card" style="background:linear-gradient(135deg,#dc2626,#7f1d1d);"><h2>{tr("❓ AI Quiz Generator")}</h2><p>{tr("Adaptive quizzes with Easy, Medium and Hard levels.")}</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.header(tr("🚀 Advanced AI Features"))
    for item in ["🧠 AI Personalized Learning", "😊 Emotion-Aware Learning", "🚀 AI Career Mentor", "🌍 Multi-language Support", "♿ Accessibility Features"]:
        st.info(tr(item))

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric(tr("🌍 Languages"), "15+")
    c2.metric(tr("⚙️ Features"), "10+")
    c3.metric(tr("🚀 AI Modules"), "5")

# --- USER PROFILE ---
elif feature == "👤 User Profile":
    st.header("👤 User Profile")
    st.success(f"Welcome {st.session_state.username}")
    st.write(f"Username: {st.session_state.username}")
    st.write("Account Type: Student")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# --- AI NOTES SUMMARIZER ---
elif feature == "🧠 AI Notes Summarizer":
    st.header(tr("🧠 AI Notes Summarizer"))
    uploaded_file = st.file_uploader(tr("Upload PDF"), type=["pdf"])
    pdf_text = ""
    if uploaded_file:
        try:
            pdf = PdfReader(uploaded_file)
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted: pdf_text += extracted + "\n"
            st.success(tr("PDF Loaded Successfully"))
        except Exception as e:
            st.error(f"PDF Error: {e}")

    input_text = st.text_area(tr("Paste Notes"), value=pdf_text, height=300)
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    summary_length = st.selectbox(tr("Summary Length"), LENGTH_OPTIONS)

    if st.button(tr("🚀 Generate Summary")):
        if input_text.strip() == "":
            st.warning(tr("Please enter or upload notes."))
        else:
            sentences = input_text.split(".")
            count = 5 if summary_length == "Short" else 10 if summary_length == "Medium" else 20
            final_summary = ".".join(sentences[:min(count, len(sentences))])
            translated_summary = translate_text(final_summary)
            st.session_state.summary = translated_summary
            st.session_state.summary_history.append(translated_summary)
            save_to_history("📝 Notes Summary", translated_summary)
            st.success(tr("Summary Generated Successfully"))
            st.write(translated_summary)

# --- SPEECH TO TEXT ---
elif feature == "🎤 Speech-to-Text":
    st.header(tr("🎤 Speech-to-Text"))
    st.write(tr("Ask a question using your microphone."))
    audio = st.audio_input(tr("🎙️ Record Question"))
    if audio:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio.read())
                audio_path = tmp.name
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
            question = recognizer.recognize_google(audio_data, language=LANGUAGES[selected_language])
            st.success(tr("Question Recognized"))
            st.info(question)

            q_lower = question.lower()
            if "python" in q_lower:
                answer = "Python is a high-level programming language known for simplicity and readability."
            elif "ai" in q_lower or "artificial intelligence" in q_lower:
                answer = "AI enables machines to learn and perform human-like tasks."
            else:
                answer = f"Topic: {question}. This is important for your learning. Study the fundamentals and practice."
            
            translated_ans = translate_text(answer)
            st.subheader(tr("🤖 AI Answer"))
            st.success(translated_ans)

            tts = gTTS(text=translated_ans, lang=LANGUAGES.get(selected_language, "en"))
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                with open(fp.name, "rb") as af:
                    st.audio(af.read(), format="audio/mp3")
            
            save_to_history("🎤 Speech Q&A", f"Q: {question}\nA: {translated_ans}")
        except Exception as e:
            st.error(f"{tr('Speech Error')}: {e}")

# --- DYSLEXIA FRIENDLY READING ---
elif feature == "📖 Dyslexia-Friendly Reading":
    st.header(tr("📖 Dyslexia-Friendly Reading"))
    if not st.session_state.summary:
        st.warning(tr("Generate a summary first using the AI Notes Summarizer."))
    else:
        st.markdown(f'<div style="line-height:2.5; letter-spacing:2px; font-size:{font_size}px; padding:25px; background:#f4f4f4; color:black; border-radius:15px;">{st.session_state.summary}</div>', unsafe_allow_html=True)
        st.success(tr("Reading mode activated."))

# --- QUIZ GENERATOR ---
elif feature == "❓ AI Quiz Generator":
    st.header("❓ AI Adaptive Quiz Generator")
    q_topic = st.text_input("Enter Topic")
    q_diff = st.selectbox("🎯 Select Difficulty", ["Basic", "Advanced", "Expert"])
    q_num = st.slider("📊 Number of Questions", 5, 20, 10)

    if st.button("🚀 Generate Quiz"):
        if not q_topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating AI Quiz..."):
                prompt = f"Generate {q_num} UNIQUE MCQ questions on {q_topic}. Level: {q_diff}. Return ONLY valid JSON: [{{'question':'','options':['','','',''],'answer':'','explanation':''}}]"
                try:
                    resp = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.8)
                    content = resp.choices[0].message.content.replace("```json", "").replace("```", "")
                    st.session_state.quiz_questions = json.loads(content)
                    st.session_state.quiz_generated = True
                    st.session_state.user_answers = {}
                except Exception as e:
                    st.error(f"Quiz Error: {e}")

    if st.session_state.quiz_generated and st.session_state.quiz_questions:
        for idx, q in enumerate(st.session_state.quiz_questions):
            st.markdown("---")
            st.write(f"### Question {idx+1}")
            st.write(q["question"])
            st.session_state.user_answers[idx] = st.radio("Choose Answer", q["options"], key=f"q_{idx}")

        if st.button("✅ Submit Quiz"):
            score = sum(1 for i, q in enumerate(st.session_state.quiz_questions) if st.session_state.user_answers.get(i) == q["answer"])
            total = len(st.session_state.quiz_questions)
            perc = (score / total) * 100
            st.success(f"🏆 Score: {score}/{total} ({perc:.2f}%)")
            if perc >= 80: st.balloons()
            
            review_list = []
            for i, q in enumerate(st.session_state.quiz_questions):
                correct = st.session_state.user_answers.get(i) == q["answer"]
                review_list.append({"question": q["question"], "user_answer": st.session_state.user_answers.get(i), "correct_answer": q["answer"], "is_correct": correct, "explanation": q["explanation"]})
                with st.expander(f"Q{i+1}: {'✅' if correct else '❌'}"):
                    st.write(f"**Correct Answer:** {q['answer']}")
                    st.info(f"**Explanation:** {q['explanation']}")
            save_quiz_history(q_topic, q_diff, f"{score}/{total}", perc, review_list)

# --- ANALYTICS DASHBOARD ---
elif feature == "📈 Analytics Dashboard":
    st.header("📈 Learning Analytics Dashboard")
    hist = load_history()
    quizzes = [i for i in hist if i.get("category") == "Quiz"]
    topics = {i.get("topic") for i in quizzes if i.get("topic")}
    lessons = sum(1 for i in hist if i.get("category") in ["📝 Notes Summary", "🎤 Speech Q&A", "🧠 Personalized Learning"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Lessons", lessons)
    col1.metric("🎯 Quizzes", len(quizzes))
    avg_acc = sum(i.get("percentage", 0) for i in quizzes) / len(quizzes) if quizzes else 0
    col2.metric("🏆 Avg Accuracy", f"{avg_acc:.1f}%")
    col2.metric("🔥 Streak", f"{min(len(hist), 30)} Days")
    col3.metric("📖 Topics", len(topics))

    if quizzes:
        st.line_chart([q.get("percentage", 0) for q in quizzes])

# --- HISTORY ---
elif feature == "📜 History":
    st.header("📜 Learning History")
    hist = load_history()
    if not hist:
        st.info("No history available.")
    else:
        for record in reversed(hist):
            with st.expander(f"{record.get('category')} | {record.get('timestamp')}"):
                if record.get("category") == "Quiz":
                    st.write(f"Topic: {record.get('topic')} | Score: {record.get('score')} ({record.get('percentage')}%)")
                else:
                    st.write(record.get("content"))
        st.download_button("⬇ Download History", json.dumps(hist, indent=2), f"{st.session_state.username}_history.json")

# --- OTHER FEATURES (Simplified for brevity) ---
elif feature == "♿ Accessibility Support":
    st.header(tr("♿ Accessibility Support"))
    for item in ["🌍 Multi-language Support", "🔠 Adjustable Font Size", "🌗 High Contrast Mode", "📖 Dyslexia Reading Mode"]:
        st.success(tr(item))

elif feature == "🧠 AI Personalized Learning":
    st.header(tr("🧠 AI Personalized Learning"))
    wt = st.text_input(tr("📘 Enter Weak Topic"))
    if st.button(tr("🚀 Generate Recommendations")):
        st.info(tr(f"Resources for {wt}: Practice daily, watch tutorials, and create notes."))
        save_to_history("🧠 Personalized Learning", wt)

elif feature == "😊 Emotion-Aware Learning":
    st.header(tr("😊 Emotion-Aware Learning"))
    emo = st.selectbox(tr("💭 How are you feeling?"), ["Confused", "Focused", "Stressed", "Tired"])
    if st.button(tr("🧠 Analyze Emotion")):
        advice = {"Confused": "Start from basics.", "Focused": "Keep going!", "Stressed": "Take a break.", "Tired": "Rest well."}
        st.info(tr(advice.get(emo)))

elif feature == "🚀 AI Career Mentor":
    st.header(tr("🚀 AI Career Mentor"))
    cq = st.text_input(tr("💬 Ask Career Guidance"))
    if st.button(tr("🚀 Get Guidance")):
        st.success(tr("Focus on projects, networking, and skill building."))
        save_to_history("🚀 Career Query", cq)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(f"<div class='footer'>{tr('Made with')} ❤️ {tr('using Streamlit')} | EduAccess AI</div>", unsafe_allow_html=True)
