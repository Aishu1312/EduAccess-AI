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
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    st.write(
        translate_text(
            "Convert speech into text and get smart AI explanations."
        )
    )

    # -----------------------------------------
    # EXPLANATION TYPE
    # -----------------------------------------

    answer_type = st.selectbox(
        translate_text("📚 Select Explanation Type"),
        [
            "Short",
            "Medium",
            "Detailed"
        ]
    )

    # -----------------------------------------
    # AUDIO INPUT
    # -----------------------------------------

    audio = st.audio_input(
        translate_text("🎙️ Record Voice")
    )

    uploaded_file = st.file_uploader(
        translate_text("📂 Upload Audio"),
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

            st.subheader(
                translate_text("📝 Your Question")
            )

            st.info(text)

        except:

            text = ""

            st.error(
                translate_text(
                    "❌ Could not understand audio."
                )
            )

        # -----------------------------------------
        # SMART AI ANSWER
        # -----------------------------------------

        if text:

            st.subheader(
                translate_text(
                    "🤖 AI Explanation"
                )
            )

            query = text.lower()

            # -----------------------------------------
            # EXCEL
            # -----------------------------------------

            if "excel" in query:

                if answer_type == "Short":

                    answer = """
Microsoft Excel is a spreadsheet software used for calculations and data analysis.

Real-world Example:
Companies use Excel for salary sheets and reports.
"""

                elif answer_type == "Medium":

                    answer = """
Microsoft Excel is a spreadsheet application used to organize, calculate, and analyze data.

Features:
• Formulas
• Charts
• Tables
• Data analysis

Real-world Examples:
• Student marksheets
• Budget planning
• Attendance records
"""

                else:

                    answer = """
Microsoft Excel is a powerful spreadsheet software developed by Microsoft used for calculations, reporting, data analysis, and visualization.

Advantages:
• Fast calculations
• Data organization
• Graphs and charts
• Business analytics

Real-world Examples:
• Banking reports
• Salary management
• Inventory tracking
• Educational result systems

Excel is widely used in education, accounting, business, and data analytics.
"""

            # -----------------------------------------
            # AI
            # -----------------------------------------

            elif "ai" in query or "artificial intelligence" in query:

                if answer_type == "Short":

                    answer = """
Artificial Intelligence enables machines to think and learn like humans.

Real-world Example:
ChatGPT and Alexa use AI technology.
"""

                elif answer_type == "Medium":

                    answer = """
Artificial Intelligence (AI) allows machines to perform tasks that normally require human intelligence.

Applications:
• Chatbots
• Voice assistants
• Healthcare systems

Real-world Examples:
• Siri
• Netflix recommendations
• Self-driving cars
"""

                else:

                    answer = """
Artificial Intelligence (AI) is a branch of computer science that enables machines to simulate human intelligence.

AI systems can:
• Learn from data
• Solve problems
• Recognize speech
• Make decisions

Advantages:
• Automation
• Faster processing
• Smart learning
• Better accessibility

Real-world Examples:
• ChatGPT
• Alexa
• Medical diagnosis systems
• Autonomous vehicles

AI is transforming education, healthcare, banking, and transportation industries.
"""

            # -----------------------------------------
            # PHOTOSYNTHESIS
            # -----------------------------------------

            elif "photosynthesis" in query:

                if answer_type == "Short":

                    answer = """
Photosynthesis is the process by which plants make food using sunlight.

Real-world Example:
Plants produce oxygen through photosynthesis.
"""

                elif answer_type == "Medium":

                    answer = """
Photosynthesis is a biological process where plants convert sunlight into food.

Requirements:
• Sunlight
• Water
• Carbon dioxide

Real-world Example:
Plants help maintain oxygen balance on Earth.
"""

                else:

                    answer = """
Photosynthesis is the process by which green plants prepare food using sunlight, water, and carbon dioxide.

Importance:
• Produces oxygen
• Supports food chains
• Maintains ecosystem balance

Real-world Examples:
• Crop growth
• Forest ecosystems
• Oxygen production

Photosynthesis is essential for life on Earth.
"""

            # -----------------------------------------
            # CLOUD COMPUTING
            # -----------------------------------------

            elif "cloud computing" in query:

                if answer_type == "Short":

                    answer = """
Cloud Computing provides online storage and computing services.

Real-world Example:
Google Drive uses cloud computing.
"""

                elif answer_type == "Medium":

                    answer = """
Cloud Computing delivers storage, software, and services through the internet.

Advantages:
• Remote access
• Online backup
• Scalability

Real-world Examples:
• Google Drive
• Dropbox
• AWS
"""

                else:

                    answer = """
Cloud Computing is a technology that provides servers, storage, databases, and software over the internet.

Benefits:
• Cost efficiency
• Scalability
• Data backup
• Remote accessibility

Real-world Examples:
• Google Drive
• Microsoft Azure
• Amazon Web Services
• Netflix infrastructure

Cloud computing is widely used in businesses, education, and modern applications.
"""

            # -----------------------------------------
            # DEFAULT
            # -----------------------------------------

            else:

                if answer_type == "Short":

                    answer = f"""
{text} is an important concept related to education or technology.

Real-world Example:
{text} is used in real-world learning and applications.
"""

                elif answer_type == "Medium":

                    answer = f"""
{text} is an important topic used in academics and industries.

Key Points:
• Improves understanding
• Helps solve problems
• Used in modern systems

Real-world Examples:
• Education
• Business applications
• Smart technologies
"""

                else:

                    answer = f"""
{text} is an important concept used in academics, science, and technology.

Advantages:
• Better learning
• Improved productivity
• Smart problem-solving

Real-world Examples:
• Educational systems
• AI platforms
• Healthcare technologies
• Business software

Understanding {text} helps students and professionals apply knowledge in practical situations.
"""

            translated_answer = translate_text(answer)

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
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header(
        translate_text(
            "❓ AI Quiz Generator"
        )
    )

    exam = st.text_input(
        translate_text(
            "📝 Enter Exam Name"
        )
    )

    topic = st.text_input(
        translate_text(
            "📘 Enter Topic"
        )
    )

    num_questions = st.slider(
        translate_text(
            "📊 Select Number of Questions"
        ),
        1,
        10,
        5
    )

    if st.button(
        translate_text(
            "🚀 Generate Quiz"
        )
    ):

        st.subheader(
            translate_text(
                "📚 Generated Questions"
            )
        )

        # -----------------------------------------
        # QUESTION BANK
        # -----------------------------------------

        question_templates = [

            {
                "question":
                f"What is the primary purpose of {topic}?",

                "correct":
                f"{topic} improves efficiency and problem-solving",

                "wrong": [
                    f"{topic} has no practical use",
                    f"{topic} only works manually",
                    f"{topic} decreases productivity"
                ]
            },

            {
                "question":
                f"Which field commonly uses {topic}?",

                "correct":
                "Education, healthcare, and technology industries",

                "wrong": [
                    "Only farming industries",
                    "Only sports activities",
                    "Only transportation systems"
                ]
            },

            {
                "question":
                f"What is an advantage of {topic}?",

                "correct":
                "Automation and improved productivity",

                "wrong": [
                    "Slower performance",
                    "No real-world applications",
                    "Increased manual work"
                ]
            },

            {
                "question":
                f"How does {topic} help society?",

                "correct":
                "It improves efficiency and accessibility",

                "wrong": [
                    "It removes all technology",
                    "It increases errors",
                    "It reduces innovation"
                ]
            },

            {
                "question":
                f"What is a real-world example of {topic}?",

                "correct":
                f"{topic} applications in education and industries",

                "wrong": [
                    "Stone-age communication",
                    "Traditional handwritten storage only",
                    "No modern usage"
                ]
            },

            {
                "question":
                f"What is the future scope of {topic}?",

                "correct":
                "Smart automation and innovation",

                "wrong": [
                    "Technology removal",
                    "Reduced development",
                    "No future applications"
                ]
            },

            {
                "question":
                f"Why is {topic} important today?",

                "correct":
                "It supports modern digital systems",

                "wrong": [
                    "It is outdated",
                    "It reduces efficiency",
                    "It has no applications"
                ]
            },

            {
                "question":
                f"What challenge is associated with {topic}?",

                "correct":
                "Implementation and resource management",

                "wrong": [
                    "No challenges exist",
                    "It works perfectly everywhere",
                    "It removes all human effort instantly"
                ]
            },

            {
                "question":
                f"Which statement about {topic} is correct?",

                "correct":
                f"{topic} is useful in modern industries",

                "wrong": [
                    f"{topic} has no importance",
                    f"{topic} only works offline",
                    f"{topic} is never used practically"
                ]
            },

            {
                "question":
                f"How does {topic} improve learning?",

                "correct":
                "By making systems smarter and interactive",

                "wrong": [
                    "By reducing accessibility",
                    "By removing automation",
                    "By slowing down communication"
                ]
            }
        ]

        # -----------------------------------------
        # RANDOM QUESTIONS
        # -----------------------------------------

        random.shuffle(question_templates)

        selected_questions = question_templates[:num_questions]

        # -----------------------------------------
        # DISPLAY QUESTIONS
        # -----------------------------------------

        score = 0

        for idx, q in enumerate(selected_questions):

            st.markdown("---")

            question = translate_text(
                q["question"]
            )

            correct = translate_text(
                q["correct"]
            )

            wrong_options = [
                translate_text(opt)
                for opt in q["wrong"]
            ]

            options = [correct] + wrong_options

            random.shuffle(options)

            st.subheader(
                f"{idx+1}. {question}"
            )

            user_answer = st.radio(
                translate_text(
                    "Choose Answer"
                ),
                options,
                key=f"quiz_{idx}"
            )

            if st.button(
                translate_text(
                    f"✅ Submit Question {idx+1}"
                ),
                key=f"submit_{idx}"
            ):

                if user_answer == correct:

                    st.success(
                        translate_text(
                            "✅ Correct Answer"
                        )
                    )

                    score += 1

                else:

                    st.error(
                        translate_text(
                            "❌ Wrong Answer"
                        )
                    )

                    st.info(
                        translate_text(
                            f"Correct Answer: {correct}"
                        )
                    )

        st.markdown("---")

        st.success(
            translate_text(
                "🎉 Quiz Generated Successfully"
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
