import streamlit as st
import random
import tempfile
import os
import json
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS
import nltk
from datetime import datetime

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
    22
)

high_contrast = st.sidebar.checkbox(
    "🌗 High Contrast Mode"
)

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "🏠 Home",
        "🧠 AI Notes Summarizer",
        "🎤 Speech-to-Text",
        "📖 Dyslexia-Friendly Reading",
        "❓ AI Quiz Generator",
        "♿ Accessibility Support",
        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor",
        "📜 History"
    ]
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

# ==================================================
# HOME PAGE
# ==================================================

if feature == "🏠 Home":

    st.title(translate_text("🚀 EduAccess AI"))
    st.subheader(translate_text("AI-Powered Accessibility Platform for Students"))
    st.success(translate_text("Inclusive AI Learning Ecosystem"))

    st.markdown("---")

    st.header(translate_text("🌟 Core Features"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">
        <h2>🧠 {translate_text("AI Notes Summarizer")}</h2>
        <p>{translate_text("Generate concise AI-powered summaries from notes and PDFs.")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#16a34a,#166534);">
        <h2>🎤 {translate_text("Speech-to-Text")}</h2>
        <p>{translate_text("Convert spoken language into text with multilingual support.")}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#f59e0b,#b45309);">
        <h2>📖 {translate_text("Dyslexia-Friendly Reading")}</h2>
        <p>{translate_text("Accessible reading mode with improved readability.")}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">
        <h2>❓ {translate_text("AI Quiz Generator")}</h2>
        <p>{translate_text("Adaptive quizzes with Easy, Medium and Hard levels.")}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header(translate_text("🚀 Advanced AI Features"))

    advanced_features = [
        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor",
        "🌍 Multi-language Support",
        "♿ Accessibility Features"
    ]

    for item in advanced_features:
        st.info(translate_text(item))

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(translate_text("🌍 Languages"), "15+")

    with c2:
        st.metric(translate_text("⚙️ Features"), "5+")

    with c3:
        st.metric(translate_text("🚀 AI Modules"), "5")

    st.markdown("---")

    st.header("🎯 Why EduAccess AI?")

    st.success("""
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

    st.header("❓ AI Adaptive Quiz Generator")

    # --------------------------------------
    # SESSION STATE
    # --------------------------------------

    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    # --------------------------------------
    # INPUTS
    # --------------------------------------

    topic = st.text_input(
        "📘 Enter Subject"
    )

    difficulty = st.selectbox(
        "🎯 Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    num_questions = st.slider(
        "📊 Number of Questions",
        5,
        30,
        10
    )

    # --------------------------------------
    # GENERATE QUIZ
    # --------------------------------------

    if st.button("🚀 Generate Quiz"):

        if topic.strip() == "":

            st.warning(
                "Please enter a subject."
            )

        else:

            st.session_state.quiz_questions = (
                generate_questions(
                    topic,
                    difficulty,
                    num_questions
                )
            )

            st.session_state.quiz_generated = True

    # --------------------------------------
    # DISPLAY QUIZ
    # --------------------------------------

    if st.session_state.quiz_generated:

        answers = {}

        st.markdown("---")

        for idx, q in enumerate(
            st.session_state.quiz_questions
        ):

            st.subheader(
                f"Question {idx + 1}"
            )

            st.write(
                q["question"]
            )

            answers[idx] = st.radio(
                "Choose Answer",
                q["options"],
                key=f"quiz_{idx}"
            )

        # ----------------------------------
        # SUBMIT QUIZ
        # ----------------------------------

        if st.button("✅ Submit Quiz"):

            score = 0

            review = []

            for idx, q in enumerate(
                st.session_state.quiz_questions
            ):

                user_answer = answers[idx]

                if user_answer == q["answer"]:
                    score += 2

                review.append({

                    "question":
                    q["question"],

                    "user_answer":
                    user_answer,

                    "correct_answer":
                    q["answer"],

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

            if percentage >= 80:

                st.balloons()

                st.success(
                    "🌟 Excellent Performance!"
                )

            elif percentage >= 50:

                st.warning(
                    "👍 Good Job. Keep Practicing."
                )

            else:

                st.error(
                    "📚 Needs Improvement."
                )

            st.markdown("---")

            st.subheader(
                "📖 Answer Review"
            )

            for idx, item in enumerate(
                review,
                start=1
            ):

                st.markdown(
                    f"### Q{idx}"
                )

                st.write(
                    item["question"]
                )

                st.success(
                    f"Your Answer: {item['user_answer']}"
                )

                st.info(
                    f"Correct Answer: {item['correct_answer']}"
                )

                st.warning(
                    f"Reason: {item['explanation']}"
                )

                st.markdown("---")

            # ----------------------------------
            # SAVE TO HISTORY
            # ----------------------------------

            quiz_record = {

                "category": "Quiz",

                "timestamp":
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M"
                ),

                "topic":
                topic,

                "difficulty":
                difficulty,

                "score":
                f"{score}/{total}",

                "questions":
                review
            }

            save_history(
                quiz_record
            )

            st.success(
                "✅ Quiz Saved to History"
            )

        # ----------------------------------
        # GENERATE NEW QUIZ
        # ----------------------------------

        st.markdown("---")

        if st.button(
            "🔄 Generate New Quiz"
        ):

            st.session_state.quiz_questions = (
                generate_questions(
                    topic,
                    difficulty,
                    num_questions
                )
            )

            st.rerun()

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
                "Take proper rest. Drink water. Continue tomorrow. Avoid over-studying."
            ))

        save_to_history("😊 Emotion Check", f"Emotion: {emotion}")

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

        save_to_history("🚀 Career Query", f"Query: {career_query}")

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
            translate_text(
                f"Total Records: {len(history)}"
            )
        )

        st.markdown("---")

        categories = ["All"]

        for item in history:

            if item.get("category") not in categories:

                categories.append(
                    item.get("category")
                )

        selected_category = st.selectbox(
            translate_text("📂 Filter by Category"),
            categories
        )

        if selected_category == "All":

            filtered_history = history

        else:

            filtered_history = [

                h for h in history

                if h.get("category")
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
                ""
            )

            with st.expander(
                f"📌 {category} | {timestamp}"
            ):

                # -----------------------
                # QUIZ HISTORY
                # -----------------------

                if category == "Quiz":

                    st.subheader("❓ Quiz Details")

                    st.write(
                        f"📘 Topic: "
                        f"{record.get('topic','N/A')}"
                    )

                    st.write(
                        f"🏆 Score: "
                        f"{record.get('score','N/A')}"
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
                            f"### Q{idx}"
                        )

                        st.write(
                            q.get(
                                "question",
                                ""
                            )
                        )

                        st.success(
                            f"Your Answer: "
                            f"{q.get('user_answer','')}"
                        )

                        st.info(
                            f"Correct Answer: "
                            f"{q.get('correct_answer','')}"
                        )

                        st.warning(
                            f"Reason: "
                            f"{q.get('explanation','')}"
                        )

                # -----------------------
                # SUMMARY HISTORY
                # -----------------------

                elif category == "Summary":

                    st.subheader(
                        "🧠 Notes Summary"
                    )

                    st.write(
                        record.get(
                            "summary",
                            ""
                        )
                    )

                # -----------------------
                # SPEECH HISTORY
                # -----------------------

                elif category == "Speech":

                    st.subheader(
                        "🎤 Speech Interaction"
                    )

                    st.markdown(
                        "### 📝 Question"
                    )

                    st.info(
                        record.get(
                            "question",
                            ""
                        )
                    )

                    st.markdown(
                        "### 🤖 Answer"
                    )

                    st.success(
                        record.get(
                            "answer",
                            ""
                        )
                    )

                # -----------------------
                # DEFAULT
                # -----------------------

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
