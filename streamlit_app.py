import streamlit as st
import json
import random
import tempfile
import os
import sqlite3
import hashlib
from datetime import datetime
from reportlab.pdfgen import canvas
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS
import nltk

import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# USER AUTHENTICATION DATABASE
conn = sqlite3.connect("eduaccess_users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)""")
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

# USER HISTORY FILE
def get_history_file():
    username = st.session_state.get("username", "guest")
    return f"history_{username}.json"

def load_history():
    history_file = get_history_file()
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    history_file = get_history_file()
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

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
    history = history[-500:]
    save_history(history)

# New function to save general notes or summaries
def save_to_history(category, content):
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "category": category,
        "content": content
    })
    history = history[-500:]
    save_history(history)

# NLTK DOWNLOAD
try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")

# PAGE CONFIG
st.set_page_config(page_title="EduAccess AI", page_icon="🚀", layout="wide")

# CUSTOM CSS
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 23px !important;
}
p, li, div, span, label, .stMarkdown, .stText, .stRadio, .stSelectbox, .stButton, .stAlert {
    font-size: 23px !important;
}
</style>
""", unsafe_allow_html=True)

# LANGUAGE SUPPORT
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

# SIDEBAR
st.sidebar.title("⚙️ Settings")
selected_language = st.sidebar.selectbox("🌍 Choose Language", list(LANGUAGES.keys()))
font_size = st.sidebar.slider("🔠 Font Size", 16, 40, 23)
high_contrast = st.sidebar.checkbox("🌗 Dark Contrast Mode")

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

feature = st.sidebar.selectbox("Choose Feature", list(FEATURES.keys()))

# GLOBAL FONT SIZE
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-size: {font_size}px !important;
}}
p, li, div, span, label, .stMarkdown, .stText, .stRadio, .stSelectbox, .stButton, .stAlert {{
    font-size: {font_size}px !important;
}}
</style>
""", unsafe_allow_html=True)

# TRANSLATION FUNCTION
def translate_text(text):
    if selected_language == "English":
        return text
    try:
        return GoogleTranslator(source="auto", target=LANGUAGES[selected_language]).translate(text)
    except:
        return text

# SAFE TRANSLATION
DO_NOT_TRANSLATE = [
    "Choose Language", "Font Size", "Dark Contrast Mode", "Core Features"
]

def tr(text):
    if text in DO_NOT_TRANSLATE:
        return text
    return translate_text(text)

# HIGH CONTRAST MODE
if high_contrast:
    st.markdown("""<style>.stApp{background:#000;color:#fff;}</style>""", unsafe_allow_html=True)

# LOGIN SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# SESSION DEFAULTS
defaults = {
    "learning_streak": 0,
    "topics_learned": [],
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
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# LOGIN PAGE
if not st.session_state.logged_in:
    st.title("🔐 " + tr("EduAccess AI"))
    option = st.radio("Choose Option", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if option == "Register":
        if st.button("Create Account"):
            if username.strip() == "" or password.strip() == "":
                st.warning("Enter username and password")
            else:
                try:
                    register_user(username, password)
                    st.success("Account Created Successfully")
                except:
                    st.error("Username already exists")
    else:
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.experimental_rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# HOME PAGE
if feature == "🏠 Home":
    st.title(tr("🚀 EduAccess AI"))
    st.subheader(tr("AI-Powered Accessibility Platform for Students"))
    st.success(tr("Inclusive AI Learning Ecosystem"))
    st.markdown("---")
    st.header("🌟 Core Features")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="feature-card" style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">
        <h2>{tr("🧠 AI Notes Summarizer")}</h2>
        <p>{tr("Generate concise AI-powered summaries from notes and PDFs.")}</p>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card" style="background:linear-gradient(135deg,#16a34a,#166534);">
        <h2>{tr("🎤 Speech-to-Text")}</h2>
        <p>{tr("Convert spoken language into text with multilingual support.")}</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="feature-card" style="background:linear-gradient(135deg,#f59e0b,#b45309);">
        <h2>{tr("📖 Dyslexia-Friendly Reading")}</h2>
        <p>{tr("Accessible reading mode with improved readability.")}</p>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card" style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">
        <h2>{tr("❓ AI Quiz Generator")}</h2>
        <p>{tr("Adaptive quizzes with Easy, Medium and Hard levels.")}</p>
        </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.header(tr("🚀 Advanced AI Features"))
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
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(tr("🌍 Languages"), "15+")
    with col2:
        st.metric(tr("⚙️ Features"), "5+")
    with col3:
        st.metric(tr("🚀 AI Modules"), "5")
    st.markdown("---")
    st.header(tr("🎯 Why EduAccess AI?"))
    st.success(
        tr("""
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
""")
    )

# USER PROFILE
elif feature == "👤 User Profile":
    st.header("👤 User Profile")
    st.success(f"Welcome {st.session_state.username}")
    st.write(f"Username: {st.session_state.username}")
    st.write("Account Type: Student")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

# AI NOTES SUMMARIZER
elif feature == "🧠 AI Notes Summarizer":
    st.header(translate_text("🧠 AI Notes Summarizer"))
    uploaded_file = st.file_uploader(translate_text("Upload PDF"), type=["pdf"])
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
    text = st.text_area(translate_text("Paste Notes"), value=text, height=300)
    LENGTH_OPTIONS = ["Short", "Medium", "Long"]
    length_idx = st.selectbox(translate_text("Summary Length"), range(len(LENGTH_OPTIONS)), format_func=lambda i: translate_text(LENGTH_OPTIONS[i]))
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
            save_to_history("📝 Notes Summary", final_summary)
            st.success(translate_text("Summary Generated Successfully"))
            st.write(final_summary)

# SPEECH TO TEXT
elif feature == "🎤 Speech-to-Text":
    st.header(translate_text("🎤 Speech-to-Text"))
    st.write(translate_text("Ask a question using your microphone."))
    audio = st.file_uploader(translate_text("🎙️ Record Question"), type=["wav"])
    if audio:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio.read())
                audio_path = tmp.name
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
            question = recognizer.recognize_google(audio_data, language=LANGUAGES[selected_language])
            st.success(translate_text("Question Recognized"))
            st.subheader(translate_text("📝 Your Question"))
            st.info(question)
            q = question.lower()
            if "python" in q:
                answer = translate_text("Python is a high-level programming language known for simplicity, readability and powerful libraries.")
            elif "artificial intelligence" in q or "ai" in q:
                answer = translate_text("Artificial Intelligence enables machines to learn, reason, make decisions and perform tasks that usually require human intelligence.")
            elif "machine learning" in q:
                answer = translate_text("Machine Learning is a branch of AI where systems learn patterns from data and improve automatically.")
            elif "dbms" in q:
                answer = translate_text("DBMS stands for Database Management System. It helps store, retrieve and manage data efficiently.")
            else:
                answer = translate_text(f"Topic: {question}\n\nThis topic is important for academic and professional learning.\n\nStudy the fundamentals, solve practice questions and build projects related to this topic.")
            st.subheader(translate_text("🤖 AI Answer"))
            st.success(answer)
            lang_code = LANGUAGES[selected_language]
            try:
                tts = gTTS(text=answer, lang=lang_code)
            except:
                tts = gTTS(text=answer, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                with open(fp.name, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
            st.session_state.speech_history.append({"question": question, "answer": answer})
            save_to_history("🎤 Speech Q&A", f"Q: {question}\nA: {answer}")
        except Exception as e:
            st.error(translate_text("Speech Error") + f": {e}")

# DYSLEXIA FRIENDLY READING
elif feature == "📖 Dyslexia-Friendly Reading":
    st.header(translate_text("📖 Dyslexia-Friendly Reading"))
    if st.session_state.summary == "":
        st.warning(translate_text("Generate a summary first using the AI Notes Summarizer."))
    else:
        st.markdown(f"""
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
        """, unsafe_allow_html=True)
        st.success(translate_text("Reading mode activated."))

# AI QUIZ GENERATOR
elif feature == "❓ AI Quiz Generator":
    st.header("❓ AI Adaptive Quiz Generator")
    topic = st.text_input("Enter Topic")
    difficulty = st.selectbox("🎯 Select Difficulty", ["Basic", "Advanced", "Expert"])
    num_questions = st.slider("📊 Number of Questions", 5, 30, 10)  # Changed max to 30

    def generate_questions(topic, difficulty, num_questions):
        # Generate questions from 0 to 30
        prompt = f"""
        Generate {num_questions} UNIQUE MCQ questions on {topic}.
        Difficulty Level: {difficulty}
        Rules:
        No duplicate questions.
        No duplicate options.
        Exactly 4 options.
        One correct answer.
        Include explanation.
        Questions must be educational and relevant.
        Return ONLY valid JSON.
        Format:
        [{{"question":"Question","options":["A","B","C","D"],"answer":"Correct Option","explanation":"Explanation"}}]"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9
            )
            content = response.choices[0].message.content
            content = content.replace("```json", "").replace("```", "")
            questions = json.loads(content)
            unique_questions = []
            seen = set()
            for q in questions:
                question_text = q["question"].strip()
                if question_text not in seen:
                    seen.add(question_text)
                    q["options"] = list(dict.fromkeys(q["options"]))
                    if len(q["options"]) == 4:
                        unique_questions.append(q)
            return unique_questions
        except Exception as e:
            st.error(f"Quiz Generation Error: {e}")
            return []

    if st.button("🚀 Generate Quiz"):
        if topic.strip() == "":
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating AI Quiz..."):
                st.session_state.quiz_questions = generate_questions(topic, difficulty, num_questions)
                st.session_state.quiz_generated = True
                st.session_state.user_answers = {}

    if st.session_state.get("quiz_generated", False) and len(st.session_state.quiz_questions) > 0:
        st.markdown("---")
        st.subheader("📝 Quiz Questions")
        for idx, q in enumerate(st.session_state.quiz_questions):
            st.markdown("---")
            st.write(f"### Question {idx+1}")
            st.write(q["question"])
            answer = st.radio("Choose Answer", q["options"], key=f"quiz_{idx}")
            st.session_state.user_answers[idx] = answer

        if st.button("✅ Submit Quiz"):
            score = 0
            review = []
            total_questions = len(st.session_state.quiz_questions)
            for idx, q in enumerate(st.session_state.quiz_questions):
                user_answer = st.session_state.user_answers.get(idx, "")
                is_correct = (user_answer == q["answer"])
                if is_correct:
                    score += 1
                review.append({
                    "question": q["question"],
                    "options": q["options"],
                    "user_answer": user_answer,
                    "correct_answer": q["answer"],
                    "is_correct": is_correct,
                    "explanation": q.get("explanation", "")
                })
            percentage = (score / total_questions) * 100
            st.markdown("---")
            st.success(f"🏆 Final Score: {score}/{total_questions}")
            st.info(f"📊 Percentage: {percentage:.2f}%")
            if percentage >= 80:
                st.balloons()
                st.success("🎉 Outstanding Performance!")
            elif percentage >= 60:
                st.success("👍 Good Work!")
            else:
                st.warning("📚 Keep Practicing!")
            if percentage >= 90:
                st.success("🏅 Expert Level Achieved")
            elif percentage >= 75:
                st.success("🥈 Advanced Level Performance")
            elif percentage >= 50:
                st.success("🥉 Basic Level Performance")
            save_quiz_history(topic, difficulty, f"{score}/{total_questions}", percentage, review)
            st.markdown("---")
            st.subheader("📖 Detailed Answer Review")
            for item in review:
                st.markdown("---")
                st.write(f"### ❓ {item['question']}")
                st.write(f"Your Answer: {item['user_answer']}")
                st.write(f"Correct Answer: {item['correct_answer']}")
                if item["is_correct"]:
                    st.success("✅ Correct")
                else:
                    st.error("❌ Incorrect")
                st.info(item["explanation"])

# ACCESSIBILITY SUPPORT
elif feature == "♿ Accessibility Support":
    st.header(translate_text("♿ Accessibility Support"))
    st.success(translate_text("🌍 Multi-language Support"))
    st.success(translate_text("🔠 Adjustable Font Size"))
    st.success(translate_text("🌗 High Contrast Mode"))
    st.success(translate_text("📖 Dyslexia Reading Mode"))
    st.success(translate_text("🎤 Speech Assistance"))
    st.markdown("---")
    st.info(translate_text("Use the sidebar to change language, font size and accessibility settings."))
    st.markdown("---")
    st.subheader(translate_text("Why Accessibility Matters?"))
    st.write(translate_text("Accessibility ensures that every learner, including students with visual, hearing, language or learning difficulties, can access education equally."))

# AI PERSONALIZED LEARNING
elif feature == "🧠 AI Personalized Learning":
    st.header(translate_text("🧠 AI Personalized Learning"))
    weak_topic = st.text_input(translate_text("📘 Enter Weak Topic"))
    STYLE_OPTIONS = ["Visual", "Theory", "Practical", "Interactive"]
    style_idx = st.selectbox(translate_text("🎯 Preferred Learning Style"),
                             range(len(STYLE_OPTIONS)),
                             format_func=lambda i: translate_text(STYLE_OPTIONS[i]))
    learning_style = STYLE_OPTIONS[style_idx]
    if st.button(translate_text("🚀 Generate Recommendations")):
        if weak_topic.strip() == "":
            st.warning(translate_text("⚠️ Please enter a topic"))
        else:
            st.success(translate_text(f"AI detected weak understanding in {weak_topic}"))
            st.markdown("---")
            st.subheader(translate_text("📘 Practice Resources"))
            st.markdown(f"🔗 https://www.google.com/search?q=GeeksforGeeks+{weak_topic}+quiz")
            st.markdown(f"🔗 https://www.google.com/search?q={weak_topic}+MCQ+questions")
            st.markdown("---")
            st.subheader(translate_text("🎥 Best YouTube Tutorials"))
            st.markdown(f"▶️ https://www.youtube.com/results?search_query={weak_topic}+full+course")
            st.markdown(f"▶️ https://www.youtube.com/results?search_query=learn+{weak_topic}+for+beginners")
            st.markdown("---")
            st.subheader(translate_text("📅 Daily Revision Plan"))
            st.info(translate_text(f"Revise {weak_topic} daily\nSolve practice questions\nWatch one tutorial every day\nCreate handwritten notes\nWeekly revision"))
            st.markdown("---")
            st.subheader(translate_text("📊 Visual Learning"))
            st.markdown(f"🔗 https://www.google.com/search?q={weak_topic}+diagram")
            st.markdown(f"🔗 https://www.google.com/search?q={weak_topic}+infographics")
            save_to_history("🧠 Personalized Learning", f"Topic: {weak_topic} | Style: {learning_style}")

# 😊 EMOTION-AWARE LEARNING
elif feature == "😊 Emotion-Aware Learning":
    st.header(translate_text("😊 Emotion-Aware Learning"))
    emotion = st.selectbox(translate_text("💭 How are you feeling?"), ["Confused", "Focused", "Stressed", "Tired"])
    if st.button(translate_text("🧠 Analyze Emotion")):
        if emotion == "Confused":
            st.warning(translate_text("AI detected confusion in learning."))
            st.info(translate_text("Start from basics, watch beginner tutorials, and practice easy questions."))
        elif emotion == "Focused":
            st.success(translate_text("AI detected high focus level."))
            st.info(translate_text("Excellent! Continue learning advanced concepts and build projects."))
        elif emotion == "Stressed":
            st.error(translate_text("AI detected stress."))
            st.info(translate_text("Take a short break, drink water, and return with a fresh mind."))
        elif emotion == "Tired":
            st.warning(translate_text("AI detected tiredness."))
            st.info(translate_text("Take short breaks. Sleep properly. Reduce pressure. Practice mindfulness."))

# 🚀 AI CAREER MENTOR
elif feature == "🚀 AI Career Mentor":
    st.header(translate_text("🚀 AI Career Mentor"))
    career_query = st.text_input(translate_text("💬 Ask Career Guidance"))
    if st.button(translate_text("🚀 Get Guidance")):
        query = career_query.lower()
        if "data science" in query:
            st.success("📊 Data Science Career Roadmap")
        elif "ai" in query:
            st.success("🤖 AI / ML Career Roadmap")
        elif "web" in query:
            st.success("🌐 Web Development Roadmap")
        elif "cybersecurity" in query:
            st.success("🔐 Cybersecurity Career Roadmap")
        else:
            st.info("Build projects, improve GitHub, practice DSA and strengthen your LinkedIn profile.")
        save_to_history("🚀 Career Query", career_query)

# ANALYTICS DASHBOARD
elif feature == "📈 Analytics Dashboard":
    st.header("📈 Learning Analytics Dashboard")
    history = load_history()
    quiz_attempts = 0
    total_percentage = 0
    topics = set()
    lessons_completed = 0
    for item in history:
        if item.get("category") == "Quiz":
            quiz_attempts += 1
            total_percentage += item.get("percentage", 0)
            if item.get("topic"):
                topics.add(item["topic"])
        elif item.get("category") in ["📝 Notes Summary", "🎤 Speech Q&A", "🧠 Personalized Learning"]:
            lessons_completed += 1
    accuracy = (total_percentage / quiz_attempts) if quiz_attempts > 0 else 0
    learning_streak = min(len(history), 30)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Lessons Completed", lessons_completed)
        st.metric("🎯 Quiz Attempts", quiz_attempts)
    with col2:
        st.metric("🏆 Accuracy", f"{accuracy:.1f}%")
        st.metric("🔥 Learning Streak", f"{learning_streak} Days")
    with col3:
        st.metric("📖 Topics Learned", len(topics))
    st.markdown("---")
    st.subheader("📊 Quiz Performance Trend")
    performance_data = []
    for item in history:
        if item.get("category") == "Quiz":
            performance_data.append({"Attempt": len(performance_data) + 1, "Score": item.get("percentage", 0)})
    if performance_data:
        st.line_chart({"Score": [x["Score"] for x in performance_data]})
    else:
        st.info("Attempt quizzes to view progress.")
    st.markdown("---")
    st.subheader("📖 Topics Learned")
    if len(topics) > 0:
        for topic in topics:
            st.success(topic)
    else:
        st.info("No topics learned yet.")
    st.markdown("---")
    st.subheader("🌍 SDG 4 Impact Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Students Supported", len(history))
    with col2:
        st.metric("Languages Supported", len(LANGUAGES))
    with col3:
        st.metric("Accessibility Features", 5)
    with col4:
        st.metric("Topics Learned", len(topics))

# HISTORY
elif feature == "📜 History":
    st.header("📜 Learning History")
    history = load_history()
    if not history:
        st.info("No history available yet.")
    else:
        st.success(f"Total Records: {len(history)}")
        for record in reversed(history):
            with st.expander(f"{record.get('category', 'Unknown')} | {record.get('timestamp', 'N/A')}"):
                if record.get("category") == "Quiz":
                    st.write(f"Topic: {record.get('topic', 'N/A')}")
                    st.write(f"Difficulty: {record.get('difficulty', 'N/A')}")
                    st.write(f"Score: {record.get('score', 'N/A')}")
                    st.write(f"Percentage: {record.get('percentage', 0)}%")
                else:
                    st.write(record.get("content", ""))
        history_json = json.dumps(history, indent=2, ensure_ascii=False)
        st.download_button("⬇ Download History", data=history_json, file_name=f"{st.session_state.username}_history.json", mime="application/json")

# FOOTER
st.markdown(f"""{translate_text("Made with")} ❤️ {translate_text("using Streamlit")} | EduAccess AI""", unsafe_allow_html=True)
