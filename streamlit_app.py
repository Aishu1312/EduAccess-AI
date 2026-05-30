import streamlit as st
import random
import tempfile
import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
from gtts import gTTS
import nltk

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
# TRANSLATION FUNCTION
# --------------------------------------------------

def translate_text(text):
    try:
        return GoogleTranslator(
            source="auto",
            target=LANGUAGES[selected_language]
        ).translate(text)
    except:
        return text

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

defaults = {
    "summary": "",
    "quiz_started": False,
    "quiz_score": 0,
    "quiz_data": [],
    "quiz_history": [],
    "user_answers": {},
    "submitted_questions": set(),
    "speech_history": [],
    "summary_history": []
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

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
        "🚀 AI Career Mentor"
    ]
)

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
# HOME PAGE
# --------------------------------------------------

if feature == "🏠 Home":

    title = translate_text("🚀 EduAccess AI")
    subtitle = translate_text(
        "AI-Powered Accessibility Platform for Students"
    )

    st.title(title)

    st.subheader(subtitle)

    st.success(
        translate_text(
            "Inclusive AI Learning Ecosystem"
        )
    )

    st.markdown("---")

    st.header(
        translate_text("🌟 Core Features")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#2563eb,#1e3a8a);">

        <h2>🧠 AI Notes Summarizer</h2>

        <p>
        Generate concise AI-powered summaries
        from notes and PDFs.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#16a34a,#166534);">

        <h2>🎤 Speech-to-Text</h2>

        <p>
        Convert spoken language into text
        with multilingual support.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#f59e0b,#b45309);">

        <h2>📖 Dyslexia-Friendly Reading</h2>

        <p>
        Accessible reading mode with
        improved readability.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card"
        style="background:linear-gradient(135deg,#dc2626,#7f1d1d);">

        <h2>❓ AI Quiz Generator</h2>

        <p>
        Adaptive quizzes with Easy,
        Medium and Hard levels.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header(
        translate_text("🚀 Advanced AI Features")
    )

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
        st.metric("🌍 Languages", "15+")

    with c2:
        st.metric("⚙️ Features", "9")

    with c3:
        st.metric("🚀 AI Modules", "8")

# --------------------------------------------------
# AI NOTES SUMMARIZER
# --------------------------------------------------

elif feature == "🧠 AI Notes Summarizer":

    st.header(
        translate_text("🧠 AI Notes Summarizer")
    )

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

            st.success(
                translate_text(
                    "PDF Loaded Successfully"
                )
            )

        except Exception as e:

            st.error(f"PDF Error: {e}")

    text = st.text_area(
        translate_text("Paste Notes"),
        value=text,
        height=300
    )

    summary_length = st.selectbox(
        translate_text("Summary Length"),
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    if st.button(
        translate_text("🚀 Generate Summary")
    ):

        if text.strip() == "":

            st.warning(
                translate_text(
                    "Please enter or upload notes."
                )
            )

        else:

            sentences = text.split(".")

            if summary_length == "Short":
                count = min(5, len(sentences))

            elif summary_length == "Medium":
                count = min(10, len(sentences))

            else:
                count = min(20, len(sentences))

            final_summary = ".".join(
                sentences[:count]
            )

            final_summary = translate_text(
                final_summary
            )

            st.session_state.summary = (
                final_summary
            )

            st.session_state.summary_history.append(
                final_summary
            )

            st.success(
                translate_text(
                    "Summary Generated Successfully"
                )
            )

            st.write(final_summary)

# --------------------------------------------------
# SPEECH TO TEXT
# --------------------------------------------------

elif feature == "🎤 Speech-to-Text":

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    st.write(
        translate_text(
            "Ask a question using your microphone."
        )
    )

    audio = st.audio_input(
        translate_text("🎙️ Record Question")
    )

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

                audio_data = recognizer.record(
                    source
                )

            question = recognizer.recognize_google(
                audio_data,
                language=LANGUAGES[selected_language]
            )

            st.success(
                translate_text(
                    "Question Recognized"
                )
            )

            st.subheader(
                translate_text("📝 Your Question")
            )

            st.info(question)

            q = question.lower()

            # ---------------------------------------
            # AI RESPONSES
            # ---------------------------------------

            if "python" in q:

                answer = """
Python is a high-level programming language
known for simplicity, readability and
powerful libraries.
"""

            elif "artificial intelligence" in q or "ai" in q:

                answer = """
Artificial Intelligence enables machines
to learn, reason, make decisions and
perform tasks that usually require
human intelligence.
"""

            elif "machine learning" in q:

                answer = """
Machine Learning is a branch of AI
where systems learn patterns from
data and improve automatically.
"""

            elif "dbms" in q:

                answer = """
DBMS stands for Database Management System.
It helps store, retrieve and manage data
efficiently.
"""

            else:

                answer = f"""
Topic: {question}

This topic is important for academic
and professional learning.

Study the fundamentals, solve practice
questions and build projects related
to this topic.
"""

            answer = translate_text(answer)

            st.subheader(
                translate_text(
                    "🤖 AI Answer"
                )
            )

            st.success(answer)

            # ---------------------------------------
            # FEMALE VOICE OUTPUT
            # ---------------------------------------

            lang_code = LANGUAGES[selected_language]

            try:

                tts = gTTS(
                    text=answer,
                    lang=lang_code
                )

            except:

                tts = gTTS(
                    text=answer,
                    lang="en"
                )

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            ) as fp:

                tts.save(fp.name)

                with open(
                    fp.name,
                    "rb"
                ) as audio_file:

                    st.audio(
                        audio_file.read(),
                        format="audio/mp3"
                    )

            st.session_state.speech_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        except Exception as e:

            st.error(
                f"Speech Error: {e}"
            )

# --------------------------------------------------
# DYSLEXIA FRIENDLY READING
# --------------------------------------------------

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header(
        translate_text(
            "📖 Dyslexia-Friendly Reading"
        )
    )

    if st.session_state.summary == "":

        st.warning(
            translate_text(
                "Generate a summary first."
            )
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
            color:black;
            border-radius:15px;
            ">

            {st.session_state.summary}

            </div>
            """,
            unsafe_allow_html=True
        )

        st.success(
            translate_text(
                "Reading mode activated."
            )
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


# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == "❓ AI Quiz Generator":

    st.header("❓ AI Adaptive Quiz Generator")

    st.write("""
Prepare for:
✅ Placements
✅ University Exams
✅ GATE
✅ Technical Interviews
✅ Competitive Exams
""")

    topic = st.selectbox(
        "📘 Select Subject",
        [
            "Python",
            "AI",
            "Machine Learning",
            "DBMS"
        ]
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
        1,
        20,
        5
    )

    # ---------------------------------------------------
    # QUESTION BANK
    # ---------------------------------------------------

    PYTHON_QUESTIONS = [

        {
            "question":"What is Python?",
            "options":[
                "Programming Language",
                "Database",
                "Browser",
                "OS"
            ],
            "answer":"Programming Language"
        },

        {
            "question":"Which keyword creates a function?",
            "options":[
                "def",
                "function",
                "func",
                "create"
            ],
            "answer":"def"
        },

        {
            "question":"Which data type is mutable?",
            "options":[
                "Tuple",
                "String",
                "List",
                "Integer"
            ],
            "answer":"List"
        },

        {
            "question":"Which symbol is used for comments?",
            "options":[
                "//",
                "#",
                "/*",
                "--"
            ],
            "answer":"#"
        },

        {
            "question":"Which function prints output?",
            "options":[
                "echo()",
                "show()",
                "print()",
                "display()"
            ],
            "answer":"print()"
        }
    ]

    AI_QUESTIONS = [

        {
            "question":"What does AI stand for?",
            "options":[
                "Artificial Intelligence",
                "Automated Internet",
                "Artificial Integration",
                "Auto Intelligence"
            ],
            "answer":"Artificial Intelligence"
        },

        {
            "question":"Which is a branch of AI?",
            "options":[
                "Machine Learning",
                "Networking",
                "Compiler Design",
                "DBMS"
            ],
            "answer":"Machine Learning"
        },

        {
            "question":"ChatGPT belongs to?",
            "options":[
                "NLP",
                "DBMS",
                "Operating System",
                "Networking"
            ],
            "answer":"NLP"
        },

        {
            "question":"AI is mainly used to?",
            "options":[
                "Mimic human intelligence",
                "Replace internet",
                "Delete data",
                "Compile programs"
            ],
            "answer":"Mimic human intelligence"
        },

        {
            "question":"Which is AI application?",
            "options":[
                "Self Driving Cars",
                "Keyboard",
                "Monitor",
                "Mouse"
            ],
            "answer":"Self Driving Cars"
        }
    ]

    ML_QUESTIONS = [

        {
            "question":"Which algorithm is used for classification?",
            "options":[
                "Logistic Regression",
                "Linear Regression",
                "Apriori",
                "KNN Tree"
            ],
            "answer":"Logistic Regression"
        },

        {
            "question":"What is overfitting?",
            "options":[
                "Model memorizes training data",
                "Model too simple",
                "No training",
                "No testing"
            ],
            "answer":"Model memorizes training data"
        },

        {
            "question":"Which is supervised learning?",
            "options":[
                "Linear Regression",
                "K-Means",
                "Apriori",
                "PCA"
            ],
            "answer":"Linear Regression"
        },

        {
            "question":"K-Means belongs to?",
            "options":[
                "Clustering",
                "Classification",
                "Regression",
                "NLP"
            ],
            "answer":"Clustering"
        },

        {
            "question":"Dataset split includes?",
            "options":[
                "Train Test",
                "Input Output",
                "Rows Columns",
                "CPU GPU"
            ],
            "answer":"Train Test"
        }
    ]

    DBMS_QUESTIONS = [

        {
            "question":"What does DBMS stand for?",
            "options":[
                "Database Management System",
                "Data Binary Management",
                "Digital Base System",
                "Database Machine System"
            ],
            "answer":"Database Management System"
        },

        {
            "question":"Primary key must be?",
            "options":[
                "Unique",
                "Null",
                "Repeated",
                "Optional"
            ],
            "answer":"Unique"
        },

        {
            "question":"SQL stands for?",
            "options":[
                "Structured Query Language",
                "System Query Language",
                "Simple Query Language",
                "Sequential Query Language"
            ],
            "answer":"Structured Query Language"
        },

        {
            "question":"Which command retrieves data?",
            "options":[
                "SELECT",
                "INSERT",
                "UPDATE",
                "DELETE"
            ],
            "answer":"SELECT"
        },

        {
            "question":"Normalization reduces?",
            "options":[
                "Redundancy",
                "Tables",
                "Rows",
                "Queries"
            ],
            "answer":"Redundancy"
        }
    ]

    if topic == "Python":
        question_pool = PYTHON_QUESTIONS

    elif topic == "AI":
        question_pool = AI_QUESTIONS

    elif topic == "Machine Learning":
        question_pool = ML_QUESTIONS

    else:
        question_pool = DBMS_QUESTIONS

    # ---------------------------------------------------
    # SESSION STATE
    # ---------------------------------------------------

    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []

    # ---------------------------------------------------
    # GENERATE QUIZ
    # ---------------------------------------------------

    if st.button("🚀 Generate Quiz"):

        available = question_pool.copy()

        random.shuffle(available)

        st.session_state.quiz_questions = available[
            :min(num_questions, len(available))
        ]

        st.session_state.quiz_generated = True

    # ---------------------------------------------------
    # DISPLAY QUIZ
    # ---------------------------------------------------

    if st.session_state.quiz_generated:

        st.markdown("---")

        answers = {}

        for idx, q in enumerate(
            st.session_state.quiz_questions
        ):

            st.subheader(
                f"Question {idx+1}"
            )

            st.write(q["question"])

            answers[idx] = st.radio(
                "Choose Answer",
                q["options"],
                key=f"answer_{idx}"
            )

        if st.button("✅ Submit Quiz"):

            score = 0

            for idx, q in enumerate(
                st.session_state.quiz_questions
            ):

                if answers[idx] == q["answer"]:
                    score += 2

            total = (
                len(
                    st.session_state.quiz_questions
                ) * 2
            )

            st.success(
                f"🏆 Score: {score}/{total}"
            )

            percentage = (
                score / total
            ) * 100

            st.info(
                f"📊 Percentage: {percentage:.2f}%"
            )

            if percentage >= 80:
                st.balloons()
                st.success(
                    "Excellent Performance!"
                )

            elif percentage >= 50:
                st.warning(
                    "Good Job. Keep Practicing."
                )

            else:
                st.error(
                    "Needs Improvement."
                )

            st.markdown("---")

            st.subheader(
                "📖 Answer Review"
            )

            for q in st.session_state.quiz_questions:

                st.write(
                    f"✅ {q['question']}"
                )

                st.info(
                    f"Correct Answer: {q['answer']}"
                )


##------------------------------------------------------------------##
## Accessibility Support ##
##------------------------------------------------------------------##

elif feature == "♿ Accessibility Support":

   st.success(
    f"Score: {score}/{total}"
)

elif feature == "♿ Accessibility Support":

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
