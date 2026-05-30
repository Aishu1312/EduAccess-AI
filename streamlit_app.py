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
        "AI Powered Accessibility Platform"
    )

    st.success(
        "Inclusive AI Learning Ecosystem"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.info("🧠 AI Notes Summarizer")

        st.info("🎤 Speech To Text")

        st.info("📖 Dyslexia Reading")

    with col2:

        st.info("❓ AI Quiz Generator")

        st.info("🧠 Personalized Learning")

        st.info("🚀 Career Mentor")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Languages",
            "15+"
        )

    with c2:
        st.metric(
            "Features",
            "8+"
        )

    with c3:
        st.metric(
            "AI Modules",
            "8"
        )

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

        pdf = PdfReader(uploaded_file)

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

        st.success(
            "PDF Loaded Successfully"
        )

    text = st.text_area(
        "Paste Notes",
        value=text,
        height=250
    )

    summary_length = st.selectbox(
        "Summary Length",
        ["Short","Medium","Long"]
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

            st.session_state.summary = (
                final_summary
            )

            st.success(
                "Summary Generated"
            )

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

    answer_mode = st.selectbox(
        "Answer Detail",
        ["Short", "Intermediate", "Advanced"]
    )

    audio = st.audio_input(
        "🎙️ Ask Your Question"
    )

    if audio:

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

            st.success("Question Recognized")

            st.subheader("📝 Question")
            st.info(question)

            q = question.lower()

            if "artificial intelligence" in q or "ai" in q:

                if answer_mode == "Short":

                    answer = """
Artificial Intelligence enables machines to perform tasks that normally require human intelligence.
"""

                elif answer_mode == "Intermediate":

                    answer = """
Artificial Intelligence allows machines to learn, reason and solve problems. Applications include healthcare, education, chatbots and recommendation systems.
"""

                else:

                    answer = """
Artificial Intelligence is the simulation of human intelligence in machines.

Major Areas:
• Machine Learning
• Deep Learning
• NLP
• Computer Vision

Applications:
• Healthcare
• Banking
• Education
• Transportation
• Cybersecurity
"""

            else:

                answer = f"""
Topic: {question}

This is an important concept for learning and practical applications.
Study examples, projects and real-world use cases to understand it deeply.
"""

            st.subheader("🤖 AI Answer")
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
                f"Error: {e}"
            )

##---------------------------------------------------------------##
## AI Quiz Generator (No Repeated Questions) ##
##---------------------------------------------------------------##

elif feature == "❓ AI Quiz Generator":

    st.header(
        "❓ AI Adaptive Quiz Generator"
    )

    topic = st.text_input(
        "Enter Topic"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    num_questions = st.slider(
        "Number of Questions",
        1,
        10,
        5
    )

    topic_lower = topic.lower()

    if "python" in topic_lower:

        question_pool = [

            {
                "question":"Which keyword defines a function?",
                "options":["def","function","define","func"],
                "answer":"def"
            },

            {
                "question":"Which datatype stores key value pairs?",
                "options":["Dictionary","List","Tuple","Set"],
                "answer":"Dictionary"
            },

            {
                "question":"Which function prints output?",
                "options":["echo()","print()","show()","display()"],
                "answer":"print()"
            },

            {
                "question":"Which symbol starts comments?",
                "options":["#","//","%","&"],
                "answer":"#"
            },

            {
                "question":"Which loop runs until condition becomes false?",
                "options":["for","while","switch","if"],
                "answer":"while"
            }
        ]

    else:

        question_pool = [

            {
                "question":f"Best way to learn {topic}?",
                "options":["Practice","Ignore","Skip","None"],
                "answer":"Practice"
            },

            {
                "question":f"What improves {topic} skills?",
                "options":["Practice","Nothing","Avoiding","Skipping"],
                "answer":"Practice"
            },

            {
                "question":f"How to master {topic}?",
                "options":["Consistency","No Revision","Skipping","None"],
                "answer":"Consistency"
            },

            {
                "question":f"Which helps learn {topic}?",
                "options":["Books","Courses","Projects","All of these"],
                "answer":"All of these"
            },

            {
                "question":f"What is important in {topic}?",
                "options":["Practice","Ignoring","Skipping","None"],
                "answer":"Practice"
            }
        ]

    if st.button("🚀 Generate Quiz"):

        selected_questions = random.sample(
            question_pool,
            min(
                num_questions,
                len(question_pool)
            )
        )

        st.session_state.quiz_data = (
            selected_questions
        )

        st.session_state.quiz_score = 0
        st.session_state.quiz_started = True

    if st.session_state.quiz_started:

        score = 0

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                f"Question {idx+1}"
            )

            st.write(q["question"])

            answer = st.radio(
                "Choose Answer",
                q["options"],
                key=f"quiz_{idx}"
            )

            if answer == q["answer"]:
                score += 1

        if st.button("Submit Quiz"):

            st.success(
                f"Final Score: {score}/{len(st.session_state.quiz_data)}"
            )

            st.session_state.quiz_history.append(
                {
                    "topic":topic,
                    "score":score
                }
            )

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

##----------------------------------------------------------##
## Personalized Learning ##
##----------------------------------------------------------##

elif feature == "🧠 AI Personalized Learning":

    st.header(
        "🧠 AI Personalized Learning"
    )

    weak_topic = st.text_input(
        "Enter Weak Topic"
    )

    learning_style = st.selectbox(
        "Learning Style",
        [
            "Visual",
            "Theory",
            "Practical",
            "Interactive"
        ]
    )

    if st.button(
        "Generate Recommendations"
    ):

        st.success(
            f"Improvement Plan for {weak_topic}"
        )

        st.markdown("""
### Daily Plan

✅ Revise concepts

✅ Practice MCQs

✅ Watch tutorials

✅ Build mini projects

✅ Weekly revision
""")

##----------------------------------------------------------##
## Emotion Aware Learning ##
##----------------------------------------------------------##

elif feature == "😊 Emotion-Aware Learning":

    st.header(
        "😊 Emotion Aware Learning"
    )

    emotion = st.selectbox(
        "How are you feeling?",
        [
            "Confused",
            "Focused",
            "Stressed",
            "Tired"
        ]
    )

    if st.button(
        "Analyze Emotion"
    ):

        if emotion == "Confused":

            st.warning(
                "Start from basics and revise slowly."
            )

        elif emotion == "Focused":

            st.success(
                "Perfect time for advanced learning."
            )

        elif emotion == "Stressed":

            st.error(
                "Take breaks and reduce pressure."
            )

        else:

            st.info(
                "Take proper rest and continue later."
            )

##--------------------------------------------------##
## AI Career Mentor ##
##--------------------------------------------------##

elif feature == "🚀 AI Career Mentor":

    st.header(
        "🚀 AI Career Mentor"
    )

    query = st.text_input(
        "Ask Career Question"
    )

    if st.button(
        "Get Guidance"
    ):

        q = query.lower()

        if "data scientist" in q:

            st.success(
                "Data Scientist Roadmap"
            )

            st.markdown("""
✅ Python

✅ SQL

✅ Statistics

✅ Machine Learning

✅ Power BI

✅ Projects

✅ Internships
""")

        elif "ai" in q:

            st.success(
                "AI Engineer Roadmap"
            )

            st.markdown("""
✅ Python

✅ Machine Learning

✅ Deep Learning

✅ NLP

✅ Computer Vision

✅ LLMs

✅ Deployment
""")

        elif "web" in q:

            st.success(
                "Web Development Roadmap"
            )

            st.markdown("""
✅ HTML

✅ CSS

✅ JavaScript

✅ React

✅ NodeJS

✅ MongoDB
""")

        else:

            st.info("""
Build projects,
improve GitHub,
practice DSA,
learn deployment,
and optimize LinkedIn.
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
