import streamlit as st
import tempfile
import random
import speech_recognition as sr
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader

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

    features = [

        "🧠 AI Personalized Learning",
        "😊 Emotion-Aware Learning",
        "🚀 AI Career Mentor",
        "🌍 Multi-language Support",
        "♿ Accessibility Features"
    ]

    for item in features:

        st.info(item)

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == "🧠 AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    uploaded_file = st.file_uploader(
        "📂 Upload PDF",
        type=["pdf"]
    )

    text = ""

    if uploaded_file:

        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:

            extracted = page.extract_text()

            if extracted:

                text += extracted

        st.success("✅ PDF Uploaded Successfully")

    manual_text = st.text_area(
        "📌 Paste Notes Here",
        height=250
    )

    if manual_text:

        text += manual_text

    summary_length = st.selectbox(

        "📏 Select Summary Length",

        ["Short", "Medium", "Detailed"]
    )

    if st.button("🚀 Generate Summary"):

        if text.strip() != "":

            sentences = [

                s.strip()

                for s in text.split(".")
                if s.strip()
            ]

            if summary_length == "Short":

                num = max(2, len(sentences)//4)

            elif summary_length == "Medium":

                num = max(4, len(sentences)//2)

            else:

                num = len(sentences)

            summary = ". ".join(sentences[:num]) + "."

            translated_summary = translate_text(summary)

            st.session_state.summary = translated_summary

            st.session_state.summary_history.append(
                translated_summary
            )

            st.success("✅ Summary Generated")

            st.markdown(f"""
            <div style="
                background:#14532d;
                padding:20px;
                border-radius:15px;
                color:white;
                font-size:{font_size}px;
                line-height:2;
            ">
            {translated_summary}
            </div>
            """, unsafe_allow_html=True)

        else:

            st.warning("⚠️ Enter Notes")

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    audio = st.audio_input(
        "🎙️ Record Voice"
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

                text = recognizer.recognize_google(

                    audio_data,
                    language=target_lang
                )

            st.success("✅ Speech Recognized")

            st.write(text)

            st.audio(audio)

            st.session_state.speech_history.append(text)

        except:

            st.error("❌ Could not understand audio")

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == "📖 Dyslexia-Friendly Reading":

    st.header("📖 Dyslexia-Friendly Reading")

    if st.session_state.summary == "":

        st.warning("⚠️ Generate summary first")

    else:

        st.markdown(f"""
        <div style="
            font-size:{font_size}px;
            line-height:2.5;
            letter-spacing:2px;
            background-color:#f4f4f4;
            padding:25px;
            border-radius:15px;
            color:black;
            font-family:OpenDyslexic;
        ">
        {st.session_state.summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == "❓ AI Quiz Generator":

    st.header("❓ AI Adaptive Quiz Generator")

    with st.expander("📚 Quiz History"):

        if st.session_state.quiz_history:

            for idx, quiz in enumerate(
                reversed(st.session_state.quiz_history),
                start=1
            ):

                with st.expander(
                    f"Quiz {idx} | {quiz['topic']} | {quiz['score']}"
                ):

                    for q in quiz["questions"]:

                        st.markdown("---")

                        st.write(q["question"])

                        st.success(
                            f"✔ Correct Answer: {q['answer']}"
                        )

                        st.info(
                            f"📖 {q['explanation']}"
                        )

        else:

            st.info("No quiz history available")

    topic = st.text_input("📘 Enter Topic")

    difficulty = st.selectbox(
        "🎯 Select Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    num_questions = st.slider(
        "📊 Number of Questions",
        1,
        10,
        5
    )

    # QUESTION BANK

    question_bank = []

    if topic != "":

        for i in range(1, 21):

            question_bank.extend([

                {
                    "question": f"What is {topic} mainly used for?",
                    "answer": "Improving efficiency and automation",
                    "options": [
                        "Improving efficiency and automation",
                        "Cooking food",
                        "Playing games only",
                        "No real-world use"
                    ],
                    "explanation": f"{topic} helps improve productivity and automation."
                },

                {
                    "question": f"Why do students learn {topic}?",
                    "answer": "To develop practical and analytical skills",
                    "options": [
                        "To develop practical and analytical skills",
                        "To waste time",
                        "No reason",
                        "Only for entertainment"
                    ],
                    "explanation": f"{topic} helps students gain industry-relevant skills."
                },

                {
                    "question": f"How is {topic} used in industries?",
                    "answer": "Automation and intelligent systems",
                    "options": [
                        "Automation and intelligent systems",
                        "Only paperwork",
                        "No usage",
                        "Sports activities"
                    ],
                    "explanation": "Industries use it for automation and smart systems."
                },

                {
                    "question": f"What is an important benefit of {topic}?",
                    "answer": "Improved productivity",
                    "options": [
                        "Improved productivity",
                        "Reduced learning",
                        "No advantages",
                        "Only theory"
                    ],
                    "explanation": f"{topic} increases efficiency and productivity."
                }

            ])

    if difficulty == "Easy":

        pool = question_bank[:20]

    elif difficulty == "Medium":

        pool = question_bank[10:40]

    else:

        pool = question_bank[20:60]

    if st.button("🚀 Generate Quiz"):

        if topic == "":

            st.warning("⚠️ Please enter a topic")

        else:

            random.shuffle(pool)

            selected = random.sample(
                pool,
                min(num_questions, len(pool))
            )

            st.session_state.quiz_data = selected

            st.session_state.quiz_started = True

            st.session_state.quiz_score = 0

    if st.session_state.quiz_started:

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                f"Q{idx+1}. {q['question']}"
            )

            answer = st.radio(
                "Choose Answer",
                q["options"],
                key=f"quiz_{idx}"
            )

            if st.button(
                f"Submit Q{idx+1}",
                key=f"submit_{idx}"
            ):

                if answer == q["answer"]:

                    st.success("✅ Correct Answer")

                    # BALLOONS ONLY HERE
                    st.balloons()

                    st.session_state.quiz_score += 2

                else:

                    st.error("❌ Wrong Answer")

                st.info(
                    f"✔ Correct Answer: {q['answer']}"
                )

                st.warning(
                    f"📖 Explanation: {q['explanation']}"
                )

        total = len(st.session_state.quiz_data) * 2

        st.header(
            f"🏆 Final Score: {st.session_state.quiz_score}/{total}"
        )

        if st.button("💾 Save Quiz"):

            st.session_state.quiz_history.append({

                "topic": topic,
                "score": f"{st.session_state.quiz_score}/{total}",
                "questions": st.session_state.quiz_data
            })

            st.success("✅ Quiz Saved Successfully")

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == "♿ Accessibility Support":

    st.header("♿ Accessibility Support")

    features = [

        "🌍 Multi-language Support",
        "🔠 Adjustable Font Size",
        "🌗 High Contrast Mode",
        "📖 Dyslexia Reading",
        "🎤 Speech Assistance"
    ]

    for item in features:

        st.success(item)

# ---------------------------------------------------
# AI PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == "🧠 AI Personalized Learning":

    st.header("🧠 AI Personalized Learning")

    weak_topic = st.text_input(
        "Enter Weak Topic"
    )

    learning_style = st.selectbox(
        "Preferred Learning Style",
        [
            "Visual",
            "Theory",
            "Practical",
            "Interactive"
        ]
    )

    if st.button("Generate Recommendations"):

        if weak_topic.strip() == "":

            st.warning("⚠️ Please enter a topic")

        else:

            st.success(
                f"AI detected weak understanding in {weak_topic}"
            )

            st.markdown("---")

            st.subheader("📘 Practice Quizzes")

            st.markdown(f"""
🔗 [GeeksforGeeks Quiz on {weak_topic}]
(https://www.google.com/search?q=GeeksforGeeks+{weak_topic}+quiz)

🔗 [MCQ Practice for {weak_topic}]
(https://www.google.com/search?q={weak_topic}+MCQ+questions)
""")

            st.markdown("---")

            st.subheader("🎥 Best YouTube Tutorials")

            st.markdown(f"""
▶️ [YouTube Tutorials for {weak_topic}]
(https://www.youtube.com/results?search_query={weak_topic}+full+course)

▶️ [Beginner Friendly {weak_topic} Tutorials]
(https://www.youtube.com/results?search_query=learn+{weak_topic}+for+beginners)
""")

            st.markdown("---")

            st.subheader("📅 Daily Revision Plan")

            st.info(f"""
✅ Revise {weak_topic} concepts daily

✅ Solve 5 practice questions everyday

✅ Watch one tutorial daily

✅ Create handwritten notes

✅ Revise weak concepts weekly
""")

            st.markdown("---")

            st.subheader("📊 Visual Learning Resources")

            st.markdown(f"""
🖼️ [Visual Diagrams for {weak_topic}]
(https://www.google.com/search?q={weak_topic}+diagram)

🖼️ [Infographics on {weak_topic}]
(https://www.google.com/search?q={weak_topic}+infographics)
""")

# ---------------------------------------------------
# EMOTION LEARNING
# ---------------------------------------------------

elif feature == "😊 Emotion-Aware Learning":

    st.header("😊 Emotion-Aware Learning")

    emotion = st.selectbox(

        "How are you feeling?",

        [
            "Confused",
            "Focused",
            "Stressed",
            "Tired"
        ]
    )

    if st.button("Analyze Emotion"):

        st.markdown("---")

        if emotion == "Confused":

            st.warning(
                "AI detected confusion in learning."
            )

            st.subheader("📘 Recommended Beginner Tutorials")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=beginner+programming+tutorials

▶️ https://www.youtube.com/results?search_query=easy+computer+science+tutorials
""")

            st.subheader("📚 Recommended Actions")

            st.info("""
✅ Start from basics

✅ Use visual diagrams

✅ Practice easy quizzes

✅ Watch beginner tutorials daily
""")

        elif emotion == "Focused":

            st.success(
                "AI detected high focus level."
            )

            st.subheader("🚀 Advanced Recommendations")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=advanced+programming+projects

▶️ https://www.geeksforgeeks.org/
""")

            st.info("""
✅ Attempt hard quizzes

✅ Build projects

✅ Practice coding daily

✅ Learn advanced concepts
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

✅ Reduce study pressure

✅ Sleep properly

✅ Practice mindfulness
""")

        else:

            st.info(
                "AI detected tiredness."
            )

            st.subheader("😴 Recovery Suggestions")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=study+motivation

▶️ https://www.youtube.com/results?search_query=focus+music+for+studying
""")

            st.info("""
✅ Take proper rest

✅ Drink water

✅ Continue learning tomorrow

✅ Avoid over-studying
""")

# ---------------------------------------------------
# CAREER MENTOR
# ---------------------------------------------------

elif feature == "🚀 AI Career Mentor":

    st.header("🚀 AI Career Mentor")

    career_query = st.text_input(
        "Ask Career Guidance"
    )

    st.markdown("""
### 💡 Sample Questions

- How to become Data Scientist
- AI Engineer roadmap
- Web Development roadmap
- Best AI projects
- Skills for Cybersecurity
""")

    if st.button("Get Guidance"):

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
▶️ https://www.coursera.org/

▶️ https://www.udemy.com/

▶️ https://www.geeksforgeeks.org/data-science-for-beginners/
""")

            st.subheader("💻 Recommended Projects")

            st.info("""
• AI Resume Analyzer

• Sales Prediction Dashboard

• Fake News Detection

• Chatbot using AI
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

            st.subheader("💻 Recommended Projects")

            st.info("""
• AI Chatbot

• Emotion Detection

• AI Accessibility Platform

• Resume Analyzer
""")

            st.subheader("🎥 Learning Resources")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=machine+learning+full+course

▶️ https://www.geeksforgeeks.org/machine-learning/
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

            st.subheader("💻 Recommended Projects")

            st.info("""
• Portfolio Website

• E-commerce Website

• Blog Platform

• AI Integrated Website
""")

            st.subheader("🎥 Tutorials")

            st.markdown("""
▶️ https://www.youtube.com/results?search_query=web+development+full+course
""")

        # DEFAULT

        else:

            st.info("""
✅ Build real-world projects

✅ Improve GitHub profile

✅ Learn deployment

✅ Practice DSA

✅ Build LinkedIn presence
""")

# ---------------------------------------------------
# NEED HELP BUTTON
# ---------------------------------------------------

col1, col2, col3 = st.columns([8,1,1])

with col3:

    if st.button("🤖 Need Help?"):

        st.session_state.show_chat = (
            not st.session_state.show_chat
        )

# ---------------------------------------------------
# CHAT POPUP
# ---------------------------------------------------

if st.session_state.show_chat:

    st.markdown("""
    <div class="chat-popup">

    <div class="chat-title">
    👋 Hi, I am Alia
    </div>

    <div class="chat-text">

    Your AI Accessibility Assistant

    <br><br>

    💬 Ask Alia anything below

    <br><br>

    ✅ Quiz Generator  
    ✅ AI Notes Summarizer  
    ✅ Speech-to-Text  
    ✅ Accessibility Features  
    ✅ Dyslexia Mode

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

    user_query = st.text_input(
        "💬 Ask Alia"
    )

    if st.button("🚀 Send"):

        query = user_query.lower()

        if "quiz" in query:

            st.success("""
📘 Quiz Generator Steps

1️⃣ Open Quiz Generator

2️⃣ Enter Topic

3️⃣ Select Difficulty

4️⃣ Select Number of Questions

5️⃣ Click Generate Quiz
""")

        elif "summary" in query or "notes" in query:

            st.success("""
🧠 AI Notes Summarizer Steps

1️⃣ Upload PDF or Paste Notes

2️⃣ Select Summary Length

3️⃣ Click Generate Summary
""")

        elif "speech" in query or "voice" in query:

            st.success("""
🎤 Speech-to-Text Steps

1️⃣ Open Speech-to-Text

2️⃣ Record Voice

3️⃣ AI converts speech into text
""")

        elif "dyslexia" in query:

            st.success("""
📖 Dyslexia Mode Features

✅ Better readability

✅ Improved spacing

✅ Large fonts

✅ Accessibility support
""")

        elif "accessibility" in query:

            st.success("""
♿ Accessibility Features

✅ Multi-language Support

✅ High Contrast Mode

✅ Adjustable Fonts

✅ Speech Assistance
""")

        else:

            st.info("""
Ask me about:

• Quiz
• Summary
• Speech
• Accessibility
• Dyslexia
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("""
<div class="footer">

Made with ❤️ using Streamlit | EduAccess AI

</div>
""", unsafe_allow_html=True)
