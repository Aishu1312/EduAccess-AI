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

.stButton>button {
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

.chat-box {
    position: fixed;
    bottom: 90px;
    right: 20px;
    width: 320px;
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.3);
    z-index: 9999;
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
# TRANSLATION
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

session_defaults = {

    "summary": "",
    "quiz_started": False,
    "quiz_score": 0,
    "quiz_data": [],
    "answer_feedback": {},
    "quiz_history": [],
    "summary_history": [],
    "speech_history": [],
    "used_questions": set(),
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

    st.balloons()

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

            st.balloons()

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

            st.balloons()

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

                    st.session_state.quiz_score += 2

                else:

                    st.error("❌ Wrong Answer")

                st.info(
                    f"✔ Correct Answer: {q['answer']}"
                )

                st.warning(
                    f"📖 Explanation: {q['explanation']}"
                )

        st.markdown("---")

        total = len(st.session_state.quiz_data) * 2

        st.header(
            f"🏆 Final Score: {st.session_state.quiz_score}/{total}"
        )

        # ---------------------------------------------------
        # BALLOONS ONLY IN QUIZ
        # ---------------------------------------------------

        if st.session_state.quiz_score >= total // 2:
        st.balloons()
    
        # ---------------------------------------------------
        # SAVE QUIZ
        # ---------------------------------------------------

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
# PERSONALIZED LEARNING
# ---------------------------------------------------

elif feature == "🧠 AI Personalized Learning":

    st.header("🧠 AI Personalized Learning")

    weak_topic = st.text_input(
        "Enter Weak Topic"
    )

    if st.button("Generate Recommendations"):

        st.success(
            f"AI detected weak understanding in {weak_topic}"
        )

        recommendations = [

            f"Practice quizzes on {weak_topic}",
            f"Watch tutorials on {weak_topic}",
            f"Revise daily",
            f"Use visual diagrams for {weak_topic}"
        ]

        for rec in recommendations:

            st.info(rec)

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

        if emotion == "Confused":

            st.warning(
                "AI detected confusion. Watch beginner tutorials."
            )

        elif emotion == "Focused":

            st.success(
                "AI detected focus. Attempt hard quizzes."
            )

        elif emotion == "Stressed":

            st.error(
                "AI detected stress. Take breaks."
            )

        else:

            st.info(
                "AI suggests proper rest."
            )

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

- Suggest AI projects for Data Science
- Roadmap for Web Development
- Skills needed for Cybersecurity
- Best projects for AI/ML
- How to become Data Analyst
""")

    if st.button("Get Guidance"):

        query = career_query.lower()

        if "data science" in query:

            st.success("""
Recommended Skills:
• Python
• SQL
• Machine Learning
• Power BI

Recommended Projects:
• AI Resume Analyzer
• Sales Dashboard
• Fake News Detection
""")

        elif "ai" in query:

            st.success("""
Recommended AI Projects:
• AI Chatbot
• Resume Analyzer
• Emotion Detection
• AI Accessibility Platform
""")

        else:

            st.info("""
Build projects, improve GitHub,
practice DSA and deployment.
""")

# ---------------------------------------------------
# FLOATING ALIA ASSISTANT
# ---------------------------------------------------

st.markdown("""
<style>

/* Floating Help Button */

.help-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: linear-gradient(135deg,#2563eb,#1d4ed8);
    color: white;
    padding: 14px 22px;
    border-radius: 50px;
    font-size: 18px;
    font-weight: bold;
    z-index: 9999;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
}

/* Chat Popup */

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
# SESSION STATE
# ---------------------------------------------------

if "show_chat" not in st.session_state:
    st.session_state.show_chat = False

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

    I can help you with:

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

        # QUIZ

        if "quiz" in query:

            st.success("""
📘 Quiz Generator Steps

1️⃣ Open Quiz Generator

2️⃣ Enter Topic

3️⃣ Select Difficulty

4️⃣ Select Number of Questions

5️⃣ Click Generate Quiz
""")

        # SUMMARY

        elif "summary" in query or "notes" in query:

            st.success("""
🧠 AI Notes Summarizer Steps

1️⃣ Upload PDF or Paste Notes

2️⃣ Select Summary Length

3️⃣ Click Generate Summary
""")

        # SPEECH

        elif "speech" in query or "voice" in query:

            st.success("""
🎤 Speech-to-Text Steps

1️⃣ Open Speech-to-Text

2️⃣ Record Voice

3️⃣ AI converts speech into text
""")

        # DYSLEXIA

        elif "dyslexia" in query:

            st.success("""
📖 Dyslexia Mode Features

✅ Better readability

✅ Improved spacing

✅ Large fonts

✅ Accessibility support
""")

        # ACCESSIBILITY

        elif "accessibility" in query:

            st.success("""
♿ Accessibility Features

✅ 28 Languages

✅ High Contrast Mode

✅ Adjustable Fonts

✅ Speech Assistance
""")

        # DEFAULT

        else:

            st.info("""
Ask me about:

• Quiz
• Summary
• Speech
• Accessibility
• Dyslexia
""")
