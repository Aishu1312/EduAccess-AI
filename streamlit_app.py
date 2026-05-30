import streamlit as st
import tempfile
import random
import os
import speech_recognition as sr
from gtts import gTTS
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# Page Configuration
st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>

.main {
    padding-top:10px;
}

.stButton > button {
    border-radius:12px;
    height:3em;
    width:100%;
    font-weight:bold;
}

.feature-card{
    padding:20px;
    border-radius:15px;
    color:white;
    margin-bottom:15px;
}

.footer{
    text-align:center;
    color:gray;
    padding:20px;
}

</style>
""", unsafe_allow_html=True)

# Language Support
LANGUAGES = {
    "English":"en-IN",
    "Hindi":"hi-IN",
    "Marathi":"mr-IN",
    "Gujarati":"gu-IN",
    "Punjabi":"pa-IN",
    "Bengali":"bn-IN",
    "Tamil":"ta-IN",
    "Telugu":"te-IN",
    "Kannada":"kn-IN",
    "Malayalam":"ml-IN",
    "Urdu":"ur-PK",
    "Spanish":"es-ES",
    "French":"fr-FR",
    "German":"de-DE",
    "Japanese":"ja-JP"
}

selected_language = st.sidebar.selectbox(
    "🌍 Select Language",
    list(LANGUAGES.keys())
)

target_lang = LANGUAGES[selected_language]

# Translation Function
def translate_text(text):

    try:
        short_lang = target_lang.split("-")[0]

        translated = GoogleTranslator(
            source="auto",
            target=short_lang
        ).translate(text)

        return translated

    except:
        return text

# Session State
defaults = {
    "summary":"",
    "quiz_started":False,
    "quiz_score":0,
    "quiz_data":[],
    "quiz_history":[],
    "user_answers":{},
    "submitted_questions":set()
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# Sidebar
st.sidebar.title("⚙️ Settings")

font_size = st.sidebar.slider(
    "Font Size",
    16,
    40,
    22
)

high_contrast = st.sidebar.checkbox(
    "High Contrast Mode"
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

# High Contrast Mode
if high_contrast:

    st.markdown("""
    <style>
    .stApp{
        background:black;
        color:white;
    }
    </style>
    """, unsafe_allow_html=True)

##--------------------------------------##
## Home Page ## 
##--------------------------------------##

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

    with col2:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">

        <h2>❓ AI Quiz Generator</h2>

        <p>
        Adaptive quizzes with Easy, Medium and Hard difficulty levels.
        </p>

        </div>
        """, unsafe_allow_html=True)

##---------------------------------------------------------##
## AI Notes Summarizer ##
##----------------------------------------------------------##

elif feature == "🧠 AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    text = ""

    if uploaded_file:

        try:
            pdf = PdfReader(uploaded_file)

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted

            st.success("PDF Loaded Successfully")

        except Exception as e:

            st.error(f"PDF Error: {e}")

    text = st.text_area(
        "Paste Notes",
        value=text,
        height=250
    )

    summary_length = st.selectbox(
        "Summary Length",
        ["Short", "Medium", "Long"]
    )

    if st.button("🚀 Generate Summary"):

        if text.strip():

            parser = PlaintextParser.from_string(
                text,
                Tokenizer("english")
            )

            summarizer = LsaSummarizer()

            if summary_length == "Short":
                count = 3

            elif summary_length == "Medium":
                count = 6

            else:
                count = 10

            summary = summarizer(
                parser.document,
                count
            )

            final_summary = " ".join(
                str(sentence)
                for sentence in summary
            )

            final_summary = translate_text(
                final_summary
            )

            st.session_state.summary = final_summary

            st.success("Summary Generated")

            st.write(final_summary)

##-------------------------------------##
## Dyslexia Reading ##
##-------------------------------------##

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header(
        "📖 Dyslexia Friendly Reading"
    )

    if st.session_state.summary == "":

        st.warning(
            "Generate Summary First"
        )

    else:

        st.markdown(
            f"""
            <div style="
            line-height:2.5;
            letter-spacing:2px;
            font-size:{font_size}px;
            padding:25px;
            background:#f4f4f4;
            border-radius:15px;
            color:black;
            ">

            {st.session_state.summary}

            </div>
            """,
            unsafe_allow_html=True
        )

##-----------------------------------------------------##
## Speech-to-Text ##
##-----------------------------------------------------##

elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    audio = st.audio_input("🎙️ Ask Your Question")

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
                language=target_lang
            )

            st.success("Question Recognized")

            st.write(question)

        except Exception as e:

            st.error(f"Error: {e}")
    
# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------


elif feature == "❓ AI Quiz Generator":

    st.header("❓ AI Adaptive Exam Quiz Generator")

    st.write("""
Prepare from Beginner → Intermediate → Advanced level.

Questions are designed for:
• Competitive Exams
• Placements
• University Preparation
""")

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    if "submitted_questions" not in st.session_state:
        st.session_state.submitted_questions = set()

    # ---------------------------------------------------
    # QUIZ HISTORY
    # ---------------------------------------------------

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

    # ---------------------------------------------------
    # INPUTS
    # ---------------------------------------------------

    exam = st.text_input(
        "📝 Enter Exam Name",
        placeholder="Example: GATE, UPSC, Placement"
    )

    topic = st.text_input(
        "📘 Enter Topic",
        placeholder="Example: Python, DBMS, AI"
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

    # ---------------------------------------------------
    # QUESTION BANKS
    # ---------------------------------------------------

    beginner_questions = [

        {
            "question": "What is Python?",
            "options": [
                "Programming Language",
                "Database",
                "Browser",
                "Operating System"
            ],
            "answer": "Programming Language",
            "explanation": "Python is a programming language."
        },

        {
            "question": "Which keyword is used to define a function?",
            "options": [
                "def",
                "func",
                "define",
                "function"
            ],
            "answer": "def",
            "explanation": "The def keyword is used to create functions."
        }
    ]

    intermediate_questions = [

        {
            "question": "What is the time complexity of Binary Search?",
            "options": [
                "O(log n)",
                "O(n)",
                "O(1)",
                "O(n²)"
            ],
            "answer": "O(log n)",
            "explanation": "Binary Search divides the search space into half."
        }
    ]

    advanced_questions = [

        {
            "question": "Which algorithm is mainly used for classification?",
            "options": [
                "Logistic Regression",
                "Linear Regression",
                "Apriori",
                "K-Means"
            ],
            "answer": "Logistic Regression",
            "explanation": "Logistic Regression is used for classification tasks."
        }
    ]

    # ---------------------------------------------------
    # DIFFICULTY LOGIC
    # ---------------------------------------------------

    if difficulty == "Beginner":

        question_pool = beginner_questions

    elif difficulty == "Intermediate":

        question_pool = (
            beginner_questions +
            intermediate_questions
        )

    else:

        question_pool = (
            beginner_questions +
            intermediate_questions +
            advanced_questions
        )

    # ---------------------------------------------------
    # GENERATE QUIZ
    # ---------------------------------------------------

    if st.button("🚀 Generate Quiz"):

        random.shuffle(question_pool)

        st.session_state.quiz_data = question_pool[:num_questions]

        st.session_state.quiz_started = True

        st.session_state.quiz_score = 0

        st.session_state.user_answers = {}

        st.session_state.submitted_questions = set()

    # ---------------------------------------------------
    # DISPLAY QUESTIONS
    # ---------------------------------------------------

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
                key=f"radio_{idx}",
                index=None
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

        # ---------------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------------

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

                "score": f"{st.session_state.quiz_score}/{total}"
            })

            st.success("✅ Quiz Saved Successfully")


##------------------------------------------------------------------##
## Accessibility Support ##
##------------------------------------------------------------------##

elif feature == "♿ Accessibility Support":

    st.header(
        "♿ Accessibility Features"
    )

    st.success(
        "🌍 Multi-language Support"
    )

    st.success(
        "🔠 Adjustable Font Size"
    )

    st.success(
        "🌗 High Contrast Mode"
    )

    st.success(
        "📖 Dyslexia Reading Mode"
    )

    st.success(
        "🎤 Speech Assistance"
    )


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
🔗 https://www.coursera.org/

🔗 https://www.udemy.com/

🔗 https://www.geeksforgeeks.org/data-science-for-beginners/
""")

            st.subheader("🎥 YouTube Tutorials")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=data+science+full+course
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
▶️ https://www.youtube.com/results?search_query=machine+learning+full+course

🔗 https://www.geeksforgeeks.org/machine-learning/
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
▶️ https://www.youtube.com/results?search_query=web+development+full+course
""")

        else:

            st.info("""
✅ Build real-world projects

✅ Improve GitHub profile

✅ Practice DSA

✅ Learn deployment

✅ Build LinkedIn presence
""")


# Final Footer 
st.markdown(
    """
    <div class='footer'>
    Made with ❤️ using Streamlit | EduAccess AI
    </div>
    """,
    unsafe_allow_html=True
)
