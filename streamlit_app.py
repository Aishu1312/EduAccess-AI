import streamlit as st
import tempfile
import random
import speech_recognition as sr
from gtts import gTTS
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import os
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 10px;
}

.stButton > button {
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    width: 100%;
}

.feature-card {
    padding: 22px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
    transition: 0.3s;
}

.feature-card:hover {
    transform: scale(1.02);
}

.footer {
    text-align:center;
    padding:20px;
    color:gray;
    font-size:14px;
}

.chat-popup {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 340px;
    background: white;
    padding: 20px;
    border-radius: 20px;
    z-index: 9999;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
}

.chat-title {
    color: #2563eb;
    font-size: 24px;
    font-weight: bold;
}

.chat-text {
    color: black;
    line-height: 1.7;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LANGUAGE SUPPORT
# ---------------------------------------------------

LANGUAGES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Urdu": "ur-PK",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Japanese": "ja-JP"
}

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

        short_lang = target_lang.split("-")[0]

        return GoogleTranslator(
            source='auto',
            target=short_lang
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
    "quiz_history": [],
    "summary_history": [],
    "speech_history": [],
    "show_chat": False
}

for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("⚙️ Settings")

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
        "🚀 AI Career Mentor"
    ]
)

# ---------------------------------------------------
# HIGH CONTRAST
# ---------------------------------------------------

if high_contrast:

    st.markdown("""
    <style>
    .stApp {
        background-color:black;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == "🏠 Home":

    st.title("🚀 EduAccess AI")

    st.subheader(
        "AI-Powered Accessibility Platform for Students"
    )

    st.success(
        "Inclusive AI Learning Ecosystem"
    )

    st.markdown("---")

    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">

        <h2>🧠 AI Notes Summarizer</h2>

        <p>
        Generate concise AI-powered summaries from notes and PDFs.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#16a34a,#166534);">

        <h2>🎤 Speech-to-Text</h2>

        <p>
        Convert spoken language into text with multilingual support.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#f59e0b,#b45309);">

        <h2>📖 Dyslexia-Friendly Reading</h2>

        <p>
        Accessible reading mode with better spacing and readability.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">

        <h2>❓ AI Quiz Generator</h2>

        <p>
        Adaptive quizzes with Easy, Medium and Hard difficulty levels.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header("🚀 Advanced AI Features")

    advanced_features = [

        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor",
        "🌍 Multi-language Support",
        "♿ Accessibility Features"
    ]

    for item in advanced_features:

        st.info(item)

    st.markdown("---")

    st.header("📈 EduAccess AI Highlights")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            label="Supported Languages",
            value="15+"
        )

    with c2:
        st.metric(
            label="Accessibility Features",
            value="5+"
        )

    with c3:
        st.metric(
            label="AI Modules",
            value="8"
        )

    st.markdown("---")

    st.header("🎯 Why EduAccess AI?")

    st.success("""
✅ Helps students learn faster

✅ Supports multiple languages

✅ Accessibility-friendly design

✅ AI-powered learning assistance

✅ Personalized career guidance

✅ Adaptive quiz generation
""")

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------
if st.button("🚀 Generate Summary"):

    if text.strip():

        parser = PlaintextParser.from_string(
            text,
            Tokenizer("english")
        )

        summarizer = LsaSummarizer()

        if summary_length == "Short":
            sentence_count = 3

        elif summary_length == "Medium":
            sentence_count = 6

        else:
            sentence_count = 10

        summary_sentences = summarizer(
            parser.document,
            sentence_count
        )

        summary = " ".join(
            str(sentence)
            for sentence in summary_sentences
        )

        translated_summary = translate_text(summary)

        st.session_state.summary = translated_summary

        st.success("✅ Summary Generated")

        st.markdown(
            f"""
            <div style="
            background:#14532d;
            padding:20px;
            border-radius:15px;
            color:white;
            font-size:{font_size}px;
            line-height:2;">
            {translated_summary}
            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# SPEECH TO TEXT + AI ANSWER
# ---------------------------------------------------

elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    answer_mode = st.selectbox(
        "Answer Detail",
        [
            "Short",
            "Intermediate",
            "Advanced"
        ]
    )

    audio = st.audio_input(
        "🎙️ Ask Your Question"
    )

    if audio:

        st.audio(audio)

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

                question = recognizer.recognize_google(
                    audio_data,
                    language=target_lang
                )

            st.success("✅ Question Recognized")

            st.markdown("### 📝 Question")

            st.info(question)

            q = question.lower()

            if "artificial intelligence" in q or "ai" in q:

                if answer_mode == "Short":

                    answer = """
Artificial Intelligence (AI) enables machines to perform tasks that normally require human intelligence such as learning, reasoning, and decision-making.

Example:
Google Assistant and ChatGPT.
"""

                elif answer_mode == "Intermediate":

                    answer = """
Artificial Intelligence (AI) is a technology that allows machines to mimic human intelligence.

Applications:
• Chatbots
• Self-driving cars
• Recommendation systems
• Healthcare diagnosis

Real-life Example:
Netflix recommends movies using AI.
"""

                else:

                    answer = """
Artificial Intelligence (AI) is the simulation of human intelligence in machines.

Major branches:
• Machine Learning
• Deep Learning
• NLP
• Computer Vision

Applications:
• Healthcare
• Education
• Banking
• Transportation
• Cybersecurity

Real-life Example:
When Amazon recommends products or Google Maps suggests routes, AI is working behind the scenes.
"""

            else:

                answer = f"""
Topic: {question}

This topic is important for learning.

Real-life Example:
Understanding {question} helps solve practical problems in education and industry.

For deeper learning, refer to tutorials, projects, and case studies.
"""

            st.markdown("### 🤖 AI Answer")

            st.success(answer)

            tts = gTTS(
                text=answer,
                lang="en"
            )

            tts.save("answer.mp3")

            with open(
                "answer.mp3",
                "rb"
            ) as audio_file:

                st.audio(
                    audio_file.read(),
                    format="audio/mp3"
                )

        except Exception as e:

            st.error(
                f"❌ Error: {e}"
            )
            
# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header("📖 Dyslexia-Friendly Reading")

    st.markdown("""
    <style>

    .dyslexia-text {

        line-height: 2.8;
        letter-spacing: 2px;
        word-spacing: 4px;
        font-size: 24px;

    }

    </style>
    """, unsafe_allow_html=True)

    if st.session_state.summary == "":

        st.warning("⚠️ Generate summary first from AI Notes Summarizer")

    else:

        st.markdown(
            f"""
            <div class="dyslexia-text">

            {st.session_state.summary}

            </div>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == "❓ AI Quiz Generator":

    st.header("❓ AI Adaptive Exam Quiz Generator")

    st.write(
        "Prepare from Beginner → Intermediate → Advanced level."
    )

    # SESSION STATES

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    if "submitted_questions" not in st.session_state:
        st.session_state.submitted_questions = set()

    # QUIZ HISTORY

    with st.expander("📚 Quiz History"):

        if st.session_state.quiz_history:

            for idx, quiz in enumerate(
                reversed(st.session_state.quiz_history),
                start=1
            ):

                st.markdown(f"""
### Quiz {idx}

📘 Topic: {quiz['topic']}

🏆 Score: {quiz['score']}
""")

        else:

            st.info("No quiz history available")

    # INPUTS

    exam = st.text_input(
        "📝 Enter Exam Name",
        placeholder="Example: Placement, GATE, UPSC"
    )

    topic = st.text_input(
        "📘 Enter Topic",
        placeholder="Example: Excel, Python, DBMS"
    )

    difficulty = st.selectbox(
        "🎯 Select Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    num_questions = st.slider(
        "📊 Number of Questions",
        1,
        10,
        5
    )

    # QUESTION POOLS

    topic_lower = topic.lower()

    if "excel" in topic_lower:

        question_pool = [

            {
                "question": "Which function calculates average in Excel?",
                "options": [
                    "AVG",
                    "AVERAGE",
                    "MEAN",
                    "CALCULATE"
                ],
                "answer": "AVERAGE",
                "explanation": "AVERAGE calculates mean value."
            },

            {
                "question": "Which symbol starts formulas in Excel?",
                "options": [
                    "=",
                    "#",
                    "%",
                    "$"
                ],
                "answer": "=",
                "explanation": "Excel formulas start with ="
            },

            {
                "question": "Shortcut to save workbook?",
                "options": [
                    "Ctrl + S",
                    "Ctrl + P",
                    "Ctrl + D",
                    "Ctrl + X"
                ],
                "answer": "Ctrl + S",
                "explanation": "Ctrl + S saves workbook."
            },

            {
                "question": "Which chart shows trends?",
                "options": [
                    "Pie",
                    "Line",
                    "Bar",
                    "Area"
                ],
                "answer": "Line",
                "explanation": "Line charts show trends."
            },

            {
                "question": "Intersection of row and column?",
                "options": [
                    "Cell",
                    "Sheet",
                    "Box",
                    "Table"
                ],
                "answer": "Cell",
                "explanation": "Rows and columns intersect at cells."
            }

        ]

    elif "python" in topic_lower:

        question_pool = [

            {
                "question": "Which keyword defines function?",
                "options": [
                    "def",
                    "function",
                    "define",
                    "func"
                ],
                "answer": "def",
                "explanation": "def creates functions."
            },

            {
                "question": "Which datatype stores key-value pairs?",
                "options": [
                    "Dictionary",
                    "Tuple",
                    "List",
                    "Set"
                ],
                "answer": "Dictionary",
                "explanation": "Dictionary stores key-value pairs."
            },

            {
                "question": "Which function prints output?",
                "options": [
                    "show()",
                    "print()",
                    "echo()",
                    "display()"
                ],
                "answer": "print()",
                "explanation": "print() displays output."
            },

            {
                "question": "Which symbol is used for comments?",
                "options": [
                    "#",
                    "//",
                    "%",
                    "<!--"
                ],
                "answer": "#",
                "explanation": "# creates comments."
            },

            {
                "question": "Which loop repeats while condition is true?",
                "options": [
                    "for",
                    "if",
                    "while",
                    "switch"
                ],
                "answer": "while",
                "explanation": "while loop repeats until condition becomes false."
            }

        ]

    else:

        question_pool = [

            {
                "question": f"What is important in {topic}?",
                "options": [
                    "Practice",
                    "Skipping",
                    "Ignoring",
                    "None"
                ],
                "answer": "Practice",
                "explanation": "Practice improves understanding."
            },

            {
                "question": f"Best way to learn {topic}?",
                "options": [
                    "Projects",
                    "Avoiding",
                    "Skipping",
                    "Nothing"
                ],
                "answer": "Projects",
                "explanation": "Projects improve practical learning."
            },

            {
                "question": f"What helps in mastering {topic}?",
                "options": [
                    "Consistency",
                    "No revision",
                    "Skipping",
                    "None"
                ],
                "answer": "Consistency",
                "explanation": "Consistency improves skills."
            },

            {
                "question": f"Which platform helps learn {topic}?",
                "options": [
                    "YouTube",
                    "Books",
                    "Courses",
                    "All of these"
                ],
                "answer": "All of these",
                "explanation": "All resources help learning."
            },

            {
                "question": f"What improves {topic} skills?",
                "options": [
                    "Practice",
                    "Ignoring",
                    "Sleeping",
                    "Nothing"
                ],
                "answer": "Practice",
                "explanation": "Practice improves skills."
            }

        ]

    # GENERATE QUIZ

    if st.button("🚀 Generate Quiz"):

        random.shuffle(question_pool)

       selected_questions = []

while len(selected_questions) < num_questions:

    selected_questions.extend(question_pool)

random.shuffle(selected_questions)

selected_questions = selected_questions[:num_questions]

        st.session_state.quiz_data = selected_questions

        st.session_state.quiz_started = True

        st.session_state.quiz_score = 0

        st.session_state.user_answers = {}

        st.session_state.submitted_questions = set()

    # DISPLAY QUIZ

    if st.session_state.quiz_started:

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                f"Q{idx+1}. {q['question']}"
            )

            user_answer = st.radio(
                "Choose Answer",
                q["options"],
                key=f"radio_{idx}"
            )

            if st.button(
                f"Submit Q{idx+1}",
                key=f"submit_{idx}"
            ):

                st.session_state.user_answers[idx] = user_answer

                st.session_state.submitted_questions.add(idx)

                if user_answer == q["answer"]:

                    st.success("✅ Correct Answer")

                    st.session_state.quiz_score += 2

                    st.balloons()

                else:

                    st.error("❌ Wrong Answer")

                st.info(
                    f"✔ Correct Answer: {q['answer']}"
                )

                st.warning(
                    f"📖 Explanation: {q['explanation']}"
                )

        total = len(
            st.session_state.quiz_data
        ) * 2

        st.markdown("---")

        st.header(
            f"🏆 Final Score: {st.session_state.quiz_score}/{total}"
        )

        if st.button("💾 Save Quiz"):

            st.session_state.quiz_history.append({

                "topic": topic,

                "score":
                f"{st.session_state.quiz_score}/{total}"
            })

            st.success(
                "✅ Quiz Saved Successfully"
            )
# ---------------------------------------------------
# ACCESSIBILITY SUPPORT
# ---------------------------------------------------

elif feature == "♿ Accessibility Support":

    st.header("♿ Accessibility Support")

    st.success("🌍 Multi-language Support")
    st.success("🔠 Adjustable Font Size")
    st.success("🌗 High Contrast Mode")
    st.success("📖 Dyslexia Reading")
    st.success("🎤 Speech Assistance")


# ---------------------------------------------------
# AI PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == "🧠 AI Personalized Learning":

    st.header("🧠 AI Personalized Learning")

    weak_topic = st.text_input(
        "📘 Enter Weak Topic"
    )

    learning_style = st.selectbox(
        "🎯 Preferred Learning Style",
        [
            "Visual",
            "Theory",
            "Practical",
            "Interactive"
        ]
    )

    if st.button("🚀 Generate Recommendations"):

        if weak_topic.strip() == "":

            st.warning("⚠️ Please enter a topic")

        else:

            st.success(
                f"AI detected weak understanding in {weak_topic}"
            )

            st.markdown("---")

            st.subheader("📘 Practice Resources")

            st.markdown(f"""
🔗 https://www.google.com/search?q=GeeksforGeeks+{weak_topic}+quiz

🔗 https://www.google.com/search?q={weak_topic}+MCQ+questions
""")

            st.markdown("---")

            st.subheader("🎥 Best YouTube Tutorials")

            st.markdown(f"""
▶️ https://www.youtube.com/results?search_query={weak_topic}+full+course

▶️ https://www.youtube.com/results?search_query=learn+{weak_topic}+for+beginners
""")

            st.markdown("---")

            st.subheader("📅 Daily Revision Plan")

            st.info(f"""
✅ Revise {weak_topic} daily

✅ Solve practice questions

✅ Watch one tutorial everyday

✅ Create handwritten notes

✅ Weekly revision
""")

            st.markdown("---")

            st.subheader("📊 Visual Learning")

            st.markdown(f"""
🔗 https://www.google.com/search?q={weak_topic}+diagram

🔗 https://www.google.com/search?q={weak_topic}+infographics
""")

# ---------------------------------------------------
# EMOTION-AWARE LEARNING
# ---------------------------------------------------

elif feature == "😊 Emotion-Aware Learning":

    st.header("😊 Emotion-Aware Learning")

    emotion = st.selectbox(

        "💭 How are you feeling?",

        [
            "Confused",
            "Focused",
            "Stressed",
            "Tired"
        ]
    )

    if st.button("🧠 Analyze Emotion"):

        st.markdown("---")

        if emotion == "Confused":

            st.warning(
                "AI detected confusion in learning."
            )

            st.subheader("🎥 Beginner Tutorials")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=beginner+programming+tutorials

▶️ https://www.youtube.com/results?search_query=easy+computer+science+tutorials
""")

            st.info("""
✅ Start from basics

✅ Watch visual tutorials

✅ Practice beginner quizzes

✅ Revise concepts slowly
""")

        elif emotion == "Focused":

            st.success(
                "AI detected high focus level."
            )

            st.subheader("🚀 Advanced Recommendations")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=advanced+programming+projects

🔗 https://www.geeksforgeeks.org/
""")

            st.info("""
✅ Build projects

✅ Practice coding

✅ Learn advanced concepts

✅ Attempt difficult quizzes
""")

        elif emotion == "Stressed":

            st.error(
                "AI detected stress."
            )

            st.subheader("🧘 Relaxation Resources")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=student+stress+management

▶️ https://www.youtube.com/results?search_query=study+motivation
""")

            st.info("""
✅ Take short breaks

✅ Sleep properly

✅ Reduce pressure

✅ Practice mindfulness
""")

        else:

            st.info(
                "AI detected tiredness."
            )

            st.subheader("😴 Recovery Suggestions")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=focus+music+for+studying

▶️ https://www.youtube.com/results?search_query=study+motivation
""")

            st.info("""
✅ Take proper rest

✅ Drink water

✅ Continue tomorrow

✅ Avoid over-studying
""")

# ---------------------------------------------------
# AI CAREER MENTOR
# ---------------------------------------------------

elif feature == "🚀 AI Career Mentor":

    st.header("🚀 AI Career Mentor")

    career_query = st.text_input(
        "💬 Ask Career Guidance"
    )

    st.markdown("""
### 💡 Sample Questions

• How to become Data Scientist

• AI Engineer roadmap

• Web Development roadmap

• Best AI projects

• Skills for Cybersecurity
""")

    if st.button("🚀 Get Guidance"):

        query = career_query.lower()

        st.markdown("---")

        # DATA SCIENCE

        if "data science" in query or "data scientist" in query:

            st.success("📊 Data Science Career Roadmap")

            st.subheader("🛠️ Skills Required")

            st.info("""
✅ Python

✅ SQL

✅ Machine Learning

✅ Power BI

✅ Statistics
""")

            st.subheader("📚 Best Courses")

            st.markdown("""
🔗 Coursera:
https://www.coursera.org/

🔗 Udemy:
https://www.udemy.com/

🔗 GeeksforGeeks:
https://www.geeksforgeeks.org/data-science-for-beginners/
""")

            st.subheader("🎥 YouTube Tutorials")

            st.markdown("""
▶️ Data Science Full Course:
https://www.youtube.com/results?search_query=data+science+full+course
""")

        # AI / ML

        elif "ai" in query or "machine learning" in query:

            st.success("🤖 AI / ML Career Roadmap")

            st.subheader("🛠️ Skills Required")

            st.info("""
✅ Python

✅ Machine Learning

✅ Deep Learning

✅ NLP

✅ Computer Vision
""")

            st.subheader("🎥 Learning Resources")

            st.markdown("""
▶️ Machine Learning Full Course:
https://www.youtube.com/results?search_query=machine+learning+full+course

🔗 GeeksforGeeks ML:
https://www.geeksforgeeks.org/machine-learning/
""")

        # WEB DEVELOPMENT

        elif "web" in query:

            st.success("🌐 Web Development Roadmap")

            st.subheader("🛠️ Skills Required")

            st.info("""
✅ HTML

✅ CSS

✅ JavaScript

✅ React

✅ Node.js
""")

            st.subheader("🎥 Tutorials")

            st.markdown("""
▶️ Web Development Full Course:
https://www.youtube.com/results?search_query=web+development+full+course
""")

        # DEFAULT

        else:

            st.success("🚀 Career Growth Recommendations")

            st.info("""
✅ Build real-world projects

✅ Improve GitHub profile

✅ Practice DSA

✅ Learn deployment

✅ Build LinkedIn presence
""")

            st.subheader("🎥 YouTube Resources")

            st.markdown("""
▶️ DSA Preparation:
https://www.youtube.com/results?search_query=dsa+full+course

▶️ GitHub Portfolio:
https://www.youtube.com/results?search_query=github+portfolio+tutorial

▶️ Deployment Tutorials:
https://www.youtube.com/results?search_query=deployment+tutorial

▶️ LinkedIn Optimization:
https://www.youtube.com/results?search_query=linkedin+profile+for+students
""")

            st.subheader("🔗 Useful Links")

            st.markdown("""
🔗 LeetCode:
https://leetcode.com/

🔗 GitHub:
https://github.com/

🔗 LinkedIn:
https://www.linkedin.com/

🔗 GeeksforGeeks:
https://www.geeksforgeeks.org/
""")


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">

Made with ❤️ using Streamlit | EduAccess AI

</div>
""", unsafe_allow_html=True)
