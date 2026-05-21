import streamlit as st

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# LANGUAGE TRANSLATIONS
# -----------------------------------

translations = {

    "English": {
        "title": "🚀 EduAccess AI",
        "subtitle": "AI-Powered Accessibility Platform for Disabled Students",
        "home": "🏠 Home",
        "summarizer": "🧠 AI Notes Summarizer",
        "speech": "🎤 Speech-to-Text",
        "dyslexia": "📖 Dyslexia-Friendly Mode",
        "quiz": "❓ Quiz Generator",
        "accessibility": "♿ Accessibility Support"
    },

    "Hindi": {
        "title": "🚀 एजु एक्सेस AI",
        "subtitle": "विकलांग छात्रों के लिए AI आधारित प्लेटफ़ॉर्म",
        "home": "🏠 होम",
        "summarizer": "🧠 नोट सारांश",
        "speech": "🎤 स्पीच-टू-टेक्स्ट",
        "dyslexia": "📖 डिस्लेक्सिया मोड",
        "quiz": "❓ क्विज़ जनरेटर",
        "accessibility": "♿ एक्सेसिबिलिटी सपोर्ट"
    },

    "Marathi": {
        "title": "🚀 एज्युॲक्सेस AI",
        "subtitle": "अपंग विद्यार्थ्यांसाठी AI आधारित प्लॅटफॉर्म",
        "home": "🏠 मुख्यपृष्ठ",
        "summarizer": "🧠 नोट्स सारांश",
        "speech": "🎤 स्पीच-टू-टेक्स्ट",
        "dyslexia": "📖 डिस्लेक्सिया मोड",
        "quiz": "❓ क्विझ जनरेटर",
        "accessibility": "♿ प्रवेशयोग्यता समर्थन"
    }
}

# -----------------------------------
# 28 LANGUAGES
# -----------------------------------

languages = [
    "English",
    "Hindi",
    "Marathi",
    "Tamil",
    "Telugu",
    "Kannada",
    "Gujarati",
    "Punjabi",
    "Bengali",
    "Malayalam",
    "Urdu",
    "Odia",
    "Assamese",
    "Sanskrit",
    "Konkani",
    "Manipuri",
    "Nepali",
    "Bodo",
    "Dogri",
    "Maithili",
    "Sindhi",
    "Kashmiri",
    "Santali",
    "French",
    "German",
    "Spanish",
    "Chinese",
    "Japanese"
]

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🌐 Language Settings")

selected_language = st.sidebar.selectbox(
    "Choose Dashboard Language",
    languages
)

# Default fallback
lang = translations.get(selected_language, translations["English"])

st.sidebar.markdown("---")

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        lang["home"],
        lang["summarizer"],
        lang["speech"],
        lang["dyslexia"],
        lang["quiz"],
        lang["accessibility"]
    ]
)

# -----------------------------------
# HOME PAGE
# -----------------------------------

if feature == lang["home"]:

    st.title(lang["title"])

    st.subheader(lang["subtitle"])

    st.write("""
    EduAccess AI is an intelligent inclusive learning platform
    designed to help students with disabilities learn more effectively
    using Artificial Intelligence, NLP, speech technologies,
    and accessibility-focused tools.
    """)

    st.markdown("---")

    st.header("🌟 Core Features")

    col1, col2 = st.columns(2)

    with col1:

        st.info("🧠 AI Notes Summarizer")
        st.write("""
        Generate concise AI-powered summaries from
        long educational notes and study materials.
        """)

        st.success("🎤 Speech-to-Text")
        st.write("""
        Convert spoken language into text
        for accessible learning support.
        """)

    with col2:

        st.warning("📖 Dyslexia-Friendly Reading")
        st.write("""
        Improve readability using accessible fonts,
        spacing, and visual enhancements.
        """)

        st.error("❓ AI Quiz Generator")
        st.write("""
        Generate customized quizzes based on
        exams, topics, and difficulty levels.
        """)

    st.markdown("---")

    st.header("♿ Accessibility Support")

    st.write("""
    EduAccess AI focuses on inclusive education
    for students with:
    """)

    st.write("✅ Dyslexia")
    st.write("✅ Visual Learning Difficulties")
    st.write("✅ Speech Impairments")
    st.write("✅ Reading Challenges")
    st.write("✅ Learning Disabilities")

    st.markdown("---")

    st.header("🚀 Future Scope")

    st.write("""
    Future versions of EduAccess AI may include:
    """)

    st.write("🔹 Real-Time Sign Language Recognition")
    st.write("🔹 AI Career Guidance")
    st.write("🔹 Emotion-Aware Learning")
    st.write("🔹 Personalized AI Tutor")
    st.write("🔹 Multilingual Accessibility Support")

# -----------------------------------
# AI NOTES SUMMARIZER
# -----------------------------------

elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    sample_text = """
Artificial Intelligence (AI) is transforming modern education
through smart learning systems, automation, and accessibility.
"""

    text = st.text_area(
        "Paste Notes Here",
        value=sample_text,
        height=300
    )

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button("Generate Summary"):

        if text:

            sentences = text.split('.')

            if summary_length == "Short":
                summary = '.'.join(sentences[:2])

            elif summary_length == "Medium":
                summary = '.'.join(sentences[:4])

            else:
                summary = '.'.join(sentences[:7])

            st.success("✅ Summary Generated Successfully")

            st.subheader("📄 Generated Summary")

            st.write(summary)

            st.info(f"📊 Word Count: {len(text.split())}")

        else:
            st.warning("Please enter notes.")

# -----------------------------------
# SPEECH TO TEXT
# -----------------------------------

elif feature == lang["speech"]:

    st.header("🎤 Speech-to-Text")

    st.write("""
    Convert voice into text using AI speech recognition.
    """)

    st.markdown("## 🎙️ AI Voice Recorder")

    audio_value = st.audio_input("Record Your Voice")

    if audio_value:

        st.success("✅ Voice Recorded Successfully")

        st.audio(audio_value)

        st.subheader("📝 Transcribed Text")

        st.write("""
Hello, welcome to EduAccess AI accessibility platform.
""")

# -----------------------------------
# DYSLEXIA MODE
# -----------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia-Friendly Reading Mode")

    dyslexia_texts = {

        "English": "Artificial Intelligence is making education more inclusive.",

        "Hindi": "कृत्रिम बुद्धिमत्ता शिक्षा को अधिक समावेशी बना रही है।",

        "Marathi": "कृत्रिम बुद्धिमत्ता शिक्षण अधिक समावेशक बनवत आहे.",

        "Tamil": "செயற்கை நுண்ணறிவு கல்வியை மேலும் உள்ளடக்கியதாக மாற்றுகிறது.",

        "Telugu": "కృత్రిమ మేధస్సు విద్యను మరింత అందుబాటులోకి తెస్తోంది.",

        "Kannada": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಶಿಕ್ಷಣವನ್ನು ಹೆಚ್ಚು ಒಳಗೊಂಡಂತೆ ಮಾಡುತ್ತಿದೆ.",

        "Gujarati": "કૃત્રિમ બુદ્ધિ શિક્ષણને વધુ સર્વસમાવેશક બનાવી રહી છે.",

        "Punjabi": "ਕ੍ਰਿਤ੍ਰਿਮ ਬੁੱਧੀ ਸਿੱਖਿਆ ਨੂੰ ਹੋਰ ਸਮਾਵੇਸ਼ੀ ਬਣਾ ਰਹੀ ਹੈ।"
    }

    display_text = dyslexia_texts.get(
        selected_language,
        dyslexia_texts["English"]
    )

    font_size = st.slider(
        "🔠 Adjust Font Size",
        20,
        40,
        30
    )

    st.markdown(f"""
    <style>
    .dyslexia-text {{
        font-size: {font_size}px;
        line-height: 2.8;
        letter-spacing: 2px;
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        padding: 25px;
        border-radius: 12px;
        color: black;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="dyslexia-text">
        {display_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("✅ Accessibility Reading Mode Enabled")

# -----------------------------------
# QUIZ GENERATOR
# -----------------------------------

elif feature == lang["quiz"]:

    st.header("❓ AI Quiz Generator")

    exam = st.text_input(
        "Enter Exam Name",
        placeholder="Example: UPSC, JEE, Interview"
    )

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: AI"
    )

    num_questions = st.slider(
        "Select Number of Questions",
        1,
        10,
        5
    )

    difficulty = st.selectbox(
        "Choose Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    if st.button("Generate Quiz"):

        if exam and topic:

            st.success(
                f"✅ {num_questions} Questions Generated"
            )

            question_bank = [

                f"What is {topic}?",

                f"Explain the importance of {topic}.",

                f"What are applications of {topic}?",

                f"What are advantages of {topic}?",

                f"What are limitations of {topic}?",

                f"How is {topic} used in industries?",

                f"Explain future scope of {topic}.",

                f"Differentiate AI and ML in {topic}.",

                f"What are challenges in {topic}?",

                f"How does {topic} improve education?"
            ]

            for i in range(num_questions):

                st.write(
                    f"{i+1}. {question_bank[i]}"
                )

        else:
            st.warning("Please enter exam name and topic.")

# -----------------------------------
# ACCESSIBILITY SUPPORT
# -----------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("""
    EduAccess AI supports inclusive learning
    for differently-abled students.
    """)

    st.subheader("🌟 Features")

    st.write("✅ Multilingual Dashboard")
    st.write("✅ Dyslexia-Friendly Reading")
    st.write("✅ Speech-to-Text")
    st.write("✅ AI Notes Summarizer")
    st.write("✅ Quiz Generator")
    st.write("✅ Large Readable Fonts")

    st.markdown("---")

    st.subheader("🚀 Future Enhancements")

    st.write("🔹 AI Sign Language Detection")
    st.write("🔹 Real-Time Translation")
    st.write("🔹 Emotion Detection")
    st.write("🔹 Personalized AI Tutor")
    st.write("🔹 Smart Accessibility Analytics")

    st.success("✅ Accessibility Support Enabled")
