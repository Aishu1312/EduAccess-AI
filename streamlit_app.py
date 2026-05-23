import streamlit as st
import tempfile
import random
import speech_recognition as sr
from deep_translator import GoogleTranslator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "started" not in st.session_state:
    st.session_state.started = False

if "q_no" not in st.session_state:
    st.session_state.q_no = 1

# ---------------------------------------------------
# 28 LANGUAGES
# ---------------------------------------------------

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
    "Odia": "or",
    "Assamese": "as",
    "Sanskrit": "sa",
    "Nepali": "ne",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Turkish": "tr",
    "Thai": "th",
    "Indonesian": "id"
}

# ---------------------------------------------------
# LANGUAGE SELECTOR
# ---------------------------------------------------

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
        return GoogleTranslator(
            source='auto',
            target=target_lang
        ).translate(text)

    except:
        return text

# ---------------------------------------------------
# UI TEXT
# ---------------------------------------------------

base_text = {
   "title": "🚀 EduAccess AI",
    "subtitle": "AI-Powered Accessibility Platform",
    "choose_feature": "Choose Feature",
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech Assistant",
    "dyslexia": "📖 Dyslexia Mode",
    "quiz": "❓ Quiz Generator",
    "accessibility": "♿ Accessibility Support",
    "welcome": "Welcome to EduAccess AI",
    "future": "🚀 Future Scope"
}

lang = {}

for key, value in base_text.items():
    lang[key] = translate_text(value)

# ---------------------------------------------------
# SIDEBAR SETTINGS
# ---------------------------------------------------

st.sidebar.title(
    translate_text("⚙ Settings")
)

font_size = st.sidebar.slider(
    translate_text("🔠 Font Size"),
    16,
    40,
    22
)

high_contrast = st.sidebar.checkbox(
    translate_text("🌗 High Contrast Mode")
)

feature = st.sidebar.selectbox(
    lang["choose_feature"],
    [
        lang["home"],
        lang["summarizer"],
        lang["speech"],
        lang["dyslexia"],
        lang["quiz"],
        lang["accessibility"]
    ]
)

# ---------------------------------------------------
# HIGH CONTRAST MODE
# ---------------------------------------------------

if high_contrast:

    st.markdown("""
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature == lang["home"]:

    st.title(lang["title"])

    st.subheader(lang["subtitle"])

    st.success(lang["welcome"])

    st.markdown("---")

    st.header(
        translate_text("🌟 Core Features")
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            translate_text(
                "🧠 AI Notes Summarizer"
            )
        )

        st.write(
            translate_text(
                "Generate AI-powered educational summaries."
            )
        )

        st.success(
            translate_text(
                "🎤 Speech Assistant"
            )
        )

        st.write(
            translate_text(
                "Convert speech into text with AI."
            )
        )

    with col2:

        st.warning(
            translate_text(
                "📖 Dyslexia Reading Mode"
            )
        )

        st.write(
            translate_text(
                "Accessibility-focused reading support."
            )
        )

        st.error(
            translate_text(
                "❓ Smart Quiz Generator"
            )
        )

        st.write(
            translate_text(
                "Generate intelligent quiz questions."
            )
        )

    st.markdown("---")

    st.header(
        translate_text(
            "♿ Accessibility Features"
        )
    )

    features = [

        "👁️ Blind Support → Audio + Screen Reader",

        "👂 Deaf Support → Text Interface",

        "🗣️ Speech Assistance",

        "📖 Dyslexia-Friendly Reading",

        "🌍 28 Language Support",

        "🔠 Adjustable Font Size",

        "🌗 High Contrast Mode"
    ]

    for item in features:
        st.write(
            translate_text(item)
        )

    st.markdown("---")

    st.header(lang["future"])

    future = [

        "🔹 Real-Time Sign Language Recognition",

        "🔹 AI Career Guidance",

        "🔹 Personalized AI Tutor",

        "🔹 Emotion-Aware Learning",

        "🔹 Offline Learning Support"
    ]

    for item in future:
        st.write(
            translate_text(item)
        )

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header(
        translate_text(
            "🧠 AI Notes Summarizer"
        )
    )

    sample_text = """
Artificial Intelligence is transforming education
through accessibility and smart learning systems.
"""

    text = st.text_area(
        translate_text(
            "📌 Paste Notes Here"
        ),
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        translate_text(
            "📏 Select Summary Length"
        ),
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    if st.button(
        translate_text(
            "🚀 Generate Summary"
        )
    ):

        sentences = [
            s.strip()
            for s in text.split('.')
            if s.strip()
        ]

        if summary_length == "Short":
            num = max(2, len(sentences)//4)

        elif summary_length == "Medium":
            num = max(4, len(sentences)//2)

        else:
            num = len(sentences)

        summary = ". ".join(
            sentences[:num]
        ) + "."

        summary = translate_text(summary)

        st.session_state.summary = summary

        st.success(
            translate_text(
                "✅ Summary Generated"
            )
        )

        st.markdown(f"""
        <div style="
            background-color:#14532d;
            padding:20px;
            border-radius:12px;
            color:white;
            font-size:{font_size}px;
            line-height:2;
        ">
        {summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# SPEECH TO TEXT + SMART AI ANSWER
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text(
            "🎤 Speech-to-Text"
        )
    )

    st.write(
        translate_text(
            "Convert speech into text and get AI-powered educational explanations."
        )
    )

    # -----------------------------------------
    # ANSWER STYLE
    # -----------------------------------------

    answer_type = st.selectbox(
        translate_text(
            "📚 Select Explanation Type"
        ),
        [
            translate_text("Short"),
            translate_text("Medium"),
            translate_text("Detailed")
        ]
    )

    # -----------------------------------------
    # AUDIO INPUT
    # -----------------------------------------

    audio = st.audio_input(
        translate_text(
            "🎙️ Record Voice"
        )
    )

    uploaded_file = st.file_uploader(
        translate_text(
            "📂 Upload Audio"
        ),
        type=["wav", "mp3", "m4a"]
    )

    source = audio if audio else uploaded_file

    # -----------------------------------------
    # PROCESS AUDIO
    # -----------------------------------------

    if source:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as tmp:

            tmp.write(source.read())

            audio_path = tmp.name

        recognizer = sr.Recognizer()

        try:

            with sr.AudioFile(audio_path) as src:

                audio_data = recognizer.record(src)

                text = recognizer.recognize_google(
                    audio_data
                )

            # -----------------------------------------
            # SHOW QUESTION
            # -----------------------------------------

            st.subheader(
                translate_text(
                    "📝 Your Question"
                )
            )

            st.info(text)

        except:

            text = ""

            st.error(
                translate_text(
                    "❌ Could not understand audio. Please speak clearly."
                )
            )

        # -----------------------------------------
        # AI ANSWER SECTION
        # -----------------------------------------

        if text:

            st.subheader(
                translate_text(
                    "🤖 AI Explanation"
                )
            )

            query = text.lower()

            # -----------------------------------------
            # AI TOPIC RESPONSES
            # -----------------------------------------

            if "artificial intelligence" in query or "ai" in query:

                if answer_type == translate_text("Short"):

                    answer = """
Artificial Intelligence (AI) enables machines to mimic human intelligence.

Real-world Example:
ChatGPT and Alexa use AI to answer questions and assist users.
"""

                elif answer_type == translate_text("Medium"):

                    answer = """
Artificial Intelligence (AI) is a technology that allows machines to think, learn, and make decisions similar to humans.

AI systems analyze data, recognize patterns, and automate tasks.

Real-world Examples:
• ChatGPT for conversations
• Self-driving cars
• Netflix recommendation system
• Face recognition in smartphones
"""

                else:

                    answer = """
Artificial Intelligence (AI) is a branch of computer science that enables machines to perform tasks requiring human intelligence such as learning, reasoning, problem-solving, and decision-making.

AI works using algorithms, machine learning, and large datasets. Modern AI systems can understand language, recognize images, and generate intelligent responses.

Advantages of AI:
• Automation of repetitive tasks
• Faster decision-making
• Personalized learning
• Improved accessibility

Real-world Examples:
• ChatGPT for education and communication
• Google Assistant and Alexa
• Medical diagnosis systems
• AI-based recommendation systems
• Smart traffic management

AI is transforming industries like healthcare, education, banking, and transportation.
"""

            # -----------------------------------------
            # MACHINE LEARNING
            # -----------------------------------------

            elif "machine learning" in query:

                if answer_type == translate_text("Short"):

                    answer = """
Machine Learning allows computers to learn from data.

Real-world Example:
Netflix movie recommendations.
"""

                elif answer_type == translate_text("Medium"):

                    answer = """
Machine Learning is a subset of AI where systems learn patterns from data and improve automatically.

Real-world Examples:
• YouTube recommendations
• Spam email filtering
• Fraud detection systems
"""

                else:

                    answer = """
Machine Learning (ML) is a branch of Artificial Intelligence that enables systems to learn from data without being explicitly programmed.

ML models analyze patterns and make predictions or decisions.

Types of Machine Learning:
• Supervised Learning
• Unsupervised Learning
• Reinforcement Learning

Applications:
• Healthcare diagnosis
• Recommendation systems
• Stock market prediction
• Speech recognition

Real-world Examples:
• Netflix recommendations
• Google Translate
• Face recognition
• Chatbots
"""

            # -----------------------------------------
            # EDUCATION
            # -----------------------------------------

            elif "education" in query:

                if answer_type == translate_text("Short"):

                    answer = """
AI improves education through personalized learning.

Example:
AI tutors help students learn at their own pace.
"""

                elif answer_type == translate_text("Medium"):

                    answer = """
AI in education provides personalized learning experiences and accessibility support.

Benefits:
• Smart tutoring
• Automated quizzes
• Voice learning support

Real-world Example:
Duolingo uses AI for language learning.
"""

                else:

                    answer = """
Artificial Intelligence is transforming education by making learning smarter, more interactive, and accessible.

AI helps students through:
• Personalized learning paths
• AI tutors
• Voice assistants
• Smart quiz generation
• Accessibility tools for disabilities

Advantages:
• Learn anytime
• Adaptive learning speed
• Better student engagement

Real-world Examples:
• Duolingo language learning
• ChatGPT educational support
• AI-powered virtual classrooms
"""

            # -----------------------------------------
            # DEFAULT ANSWER
            # -----------------------------------------

            else:

                if answer_type == translate_text("Short"):

                    answer = f"""
This topic relates to educational or general knowledge concepts.

Real-world Example:
Technology is widely used in modern education and industry.
"""

                elif answer_type == translate_text("Medium"):

                    answer = f"""
Your question is related to educational concepts and modern technology applications.

AI systems help students learn faster through smart assistance and automation.

Real-world Examples:
• Online learning platforms
• AI chatbots
• Smart assistants
"""

                else:

                    answer = f"""
Your question explores concepts related to education, technology, or intelligent systems.

Modern AI-based platforms provide:
• Personalized learning
• Accessibility support
• Smart tutoring
• Voice assistance
• Automated content generation

Real-world Examples:
• ChatGPT
• Google Assistant
• AI tutors
• Smart classrooms

These technologies improve learning efficiency and accessibility worldwide.
"""

            # -----------------------------------------
            # TRANSLATE ANSWER
            # -----------------------------------------

            translated_answer = translate_text(answer)

            # -----------------------------------------
            # DISPLAY ANSWER
            # -----------------------------------------

            st.markdown(f"""
            <div style="
                background-color:#0f172a;
                padding:20px;
                border-radius:15px;
                color:white;
                font-size:{font_size}px;
                line-height:2;
            ">
            {translated_answer}
            </div>
            """, unsafe_allow_html=True)
# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header(
        translate_text(
            "📖 Dyslexia-Friendly Reading"
        )
    )

    if not st.session_state.summary:

        st.warning(
            translate_text(
                "⚠️ Generate summary first."
            )
        )

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
        ">
        {st.session_state.summary}
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text(
            "🎯 Smart AI Quiz"
        )
    )

    topic = st.text_input(
        translate_text(
            "📘 Enter Topic"
        )
    )

    def generate_question(topic):

        questions = [

            f"What is the purpose of {topic}?",

            f"Why is {topic} important?",

            f"What is an application of {topic}?"
        ]

        q_text = random.choice(questions)

        correct = (
            f"{topic} improves automation"
        )

        options = [
            correct,
            f"{topic} has no use",
            f"{topic} removes humans",
            f"{topic} works offline only"
        ]

        random.shuffle(options)

        return q_text, options, correct

    if st.button(
        translate_text(
            "🚀 Start Quiz"
        )
    ):

        st.session_state.started = True
        st.session_state.q_no = 1
        st.session_state.score = 0

    if st.session_state.started:

        if st.session_state.q_no > 10:

            st.success(
                translate_text(
                    f"🏆 Final Score: {st.session_state.score}/10"
                )
            )

            st.stop()

        q_text, options, correct = generate_question(topic)

        st.subheader(
            translate_text(
                f"Question {st.session_state.q_no}/10"
            )
        )

        translated_options = [
            translate_text(opt)
            for opt in options
        ]

        st.write(
            translate_text(q_text)
        )

        selected = st.radio(
            translate_text(
                "Choose Answer"
            ),
            translated_options
        )

        if st.button(
            translate_text(
                "✅ Submit"
            )
        ):

            if selected == translate_text(correct):

                st.success(
                    translate_text(
                        "✅ Correct"
                    )
                )

                st.session_state.score += 1

            else:

                st.error(
                    translate_text(
                        "❌ Wrong"
                    )
                )

            st.session_state.q_no += 1

            st.rerun()

        st.progress(
            st.session_state.q_no / 10
        )

        st.write(
            translate_text(
                f"📊 Score: {st.session_state.score}"
            )
        )

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header(
        translate_text(
            "♿ Accessibility Support"
        )
    )

    accessibility_features = [

        "👁️ Blind → Audio Support",

        "👂 Deaf → Text Interface",

        "🗣️ Speech Impaired → Text Input",

        "🦽 Mobility Support → Large UI",

        "📖 Dyslexia-Friendly Reading",

        "🌍 28 Language Translation",

        "🔠 Adjustable Fonts"
    ]

    for item in accessibility_features:

        st.write(
            translate_text(item)
        )
