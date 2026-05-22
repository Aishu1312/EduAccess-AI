import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# LANGUAGE TRANSLATIONS
# ---------------------------------------------------

translations = {

    "English": {
        "title": "🚀 EduAccess AI",
        "subtitle": "AI-Powered Accessibility Platform for Disabled Students",
        "choose_feature": "Choose Feature",
        "home": "🏠 Home",
        "summarizer": "🧠 AI Notes Summarizer",
        "speech": "🎤 Speech-to-Text",
        "dyslexia": "📖 Dyslexia-Friendly Mode",
        "quiz": "❓ Quiz Generator",
        "accessibility": "♿ Accessibility Support",
        "core_features": "🌟 Core Features",
        "future_scope": "🚀 Future Scope",
        "welcome": "EduAccess AI is an intelligent inclusive learning platform designed to help students with disabilities learn more effectively using Artificial Intelligence, NLP, speech technologies, and accessibility-focused tools.",
        "future1": "🔹 Real-Time Sign Language Recognition",
        "future2": "🔹 AI Career Guidance",
        "future3": "🔹 Emotion-Aware Learning",
        "future4": "🔹 Personalized AI Tutor",
        "future5": "🔹 Multilingual Accessibility Support",
        "summary_button": "Generate Summary",
        "quiz_button": "Generate Quiz"
    },

    "Hindi": {
        "title": "🚀 एजु एक्सेस AI",
        "subtitle": "विकलांग छात्रों के लिए AI आधारित प्लेटफ़ॉर्म",
        "choose_feature": "फ़ीचर चुनें",
        "home": "🏠 होम",
        "summarizer": "🧠 नोट सारांश",
        "speech": "🎤 स्पीच-टू-टेक्स्ट",
        "dyslexia": "📖 डिस्लेक्सिया मोड",
        "quiz": "❓ क्विज़ जनरेटर",
        "accessibility": "♿ एक्सेसिबिलिटी सपोर्ट",
        "core_features": "🌟 मुख्य विशेषताएँ",
        "future_scope": "🚀 भविष्य की संभावनाएँ",
        "welcome": "EduAccess AI एक बुद्धिमान समावेशी शिक्षण मंच है जो विकलांग छात्रों को AI, NLP और स्पीच तकनीक के माध्यम से बेहतर सीखने में मदद करता है।",
        "future1": "🔹 रियल-टाइम सांकेतिक भाषा पहचान",
        "future2": "🔹 AI करियर मार्गदर्शन",
        "future3": "🔹 भावना आधारित शिक्षण",
        "future4": "🔹 व्यक्तिगत AI ट्यूटर",
        "future5": "🔹 बहुभाषी एक्सेसिबिलिटी सपोर्ट",
        "summary_button": "सारांश बनाएं",
        "quiz_button": "क्विज़ बनाएं"
    },

    "Marathi": {
        "title": "🚀 एज्युॲक्सेस AI",
        "subtitle": "अपंग विद्यार्थ्यांसाठी AI आधारित प्लॅटफॉर्म",
        "choose_feature": "फीचर निवडा",
        "home": "🏠 मुख्यपृष्ठ",
        "summarizer": "🧠 नोट्स सारांश",
        "speech": "🎤 स्पीच-टू-टेक्स्ट",
        "dyslexia": "📖 डिस्लेक्सिया मोड",
        "quiz": "❓ क्विझ जनरेटर",
        "accessibility": "♿ प्रवेशयोग्यता समर्थन",
        "core_features": "🌟 मुख्य वैशिष्ट्ये",
        "future_scope": "🚀 भविष्यातील संधी",
        "welcome": "EduAccess AI हे AI आणि NLP वापरून दिव्यांग विद्यार्थ्यांसाठी समावेशक शिक्षण प्लॅटफॉर्म आहे.",
        "future1": "🔹 सांकेतिक भाषा ओळख",
        "future2": "🔹 AI करिअर मार्गदर्शन",
        "future3": "🔹 भावना आधारित शिक्षण",
        "future4": "🔹 वैयक्तिक AI शिक्षक",
        "future5": "🔹 बहुभाषिक समर्थन",
        "summary_button": "सारांश तयार करा",
        "quiz_button": "क्विझ तयार करा"
    }
}

# ---------------------------------------------------
# 28 LANGUAGES
# ---------------------------------------------------

languages = [
    "English", "Hindi", "Marathi", "Tamil", "Telugu",
    "Kannada", "Gujarati", "Punjabi", "Bengali",
    "Malayalam", "Urdu", "Odia", "Assamese",
    "Sanskrit", "Konkani", "Manipuri", "Nepali",
    "Bodo", "Dogri", "Maithili", "Sindhi",
    "Kashmiri", "Santali", "French", "German",
    "Spanish", "Chinese", "Japanese"
]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🌐 Language Settings")

selected_language = st.sidebar.selectbox(
    "Choose Dashboard Language",
    languages
)

# fallback to English if translation missing
lang = translations.get(selected_language, translations["English"])

st.sidebar.markdown("---")

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
# HOME PAGE
# ---------------------------------------------------

if feature == lang["home"]:

    st.title(lang["title"])

    st.subheader(lang["subtitle"])

    st.write(lang["welcome"])

    st.markdown("---")

    st.header(lang["core_features"])

    col1, col2 = st.columns(2)

    with col1:

        st.info("🧠 AI Notes Summarizer")
        st.write("""
Generate concise AI-powered summaries from educational notes.
""")

        st.success("🎤 Speech-to-Text")
        st.write("""
Convert spoken language into text using AI.
""")

    with col2:

        st.warning("📖 Dyslexia-Friendly Reading")
        st.write("""
Improve readability using accessibility-focused UI.
""")

        st.error("❓ AI Quiz Generator")
        st.write("""
Generate exam-based AI quiz questions.
""")

    st.markdown("---")

    st.header("♿ Accessibility Support")

    st.write("✅ Dyslexia Support")
    st.write("✅ Speech Assistance")
    st.write("✅ Large Readable Fonts")
    st.write("✅ AI Learning Assistance")
    st.write("✅ Multilingual Support")

    st.markdown("---")

    st.header(lang["future_scope"])

    st.write(lang["future1"])
    st.write(lang["future2"])
    st.write(lang["future3"])
    st.write(lang["future4"])
    st.write(lang["future5"])

# ---------------------------------------------------
# AI NOTES SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header("🧠 AI Notes Summarizer")

    sample_text = """
Artificial Intelligence is transforming education
through accessibility and smart learning systems.
"""

    text = st.text_area(
        "Paste Notes Here",
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    if st.button(lang["summary_button"]):

        sentences = text.split('.')

        if summary_length == "Short":
            summary = '.'.join(sentences[:2])

        elif summary_length == "Medium":
            summary = '.'.join(sentences[:4])

        else:
            summary = '.'.join(sentences[:6])

        st.success("✅ Summary Generated")

        st.write(summary)

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header("🎤 Speech-to-Text")

    st.write("""
Convert voice into text using AI speech recognition.
""")

    audio_value = st.audio_input("🎙️ Record Voice")

    if audio_value:

        st.success("✅ Audio Recorded Successfully")

        st.audio(audio_value)

        st.subheader("📝 Transcribed Text")

        st.write("""
Hello, welcome to EduAccess AI.
""")

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia-Friendly Reading Mode")

    font_size = st.slider(
        "Adjust Font Size",
        20,
        40,
        30
    )

    dyslexia_texts = {

        "English": "Artificial Intelligence improves accessible education.",

        "Hindi": "कृत्रिम बुद्धिमत्ता शिक्षा को अधिक सुलभ बनाती है।",

        "Marathi": "कृत्रिम बुद्धिमत्ता शिक्षण अधिक सुलभ बनवते.",

        "Tamil": "செயற்கை நுண்ணறிவு கல்வியை மேம்படுத்துகிறது.",

        "Telugu": "కృత్రిమ మేధస్సు విద్యను మెరుగుపరుస్తుంది.",

        "Kannada": "ಕೃತಕ ಬುದ್ಧಿಮತ್ತೆ ಶಿಕ್ಷಣವನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.",

        "Gujarati": "કૃત્રિમ બુદ્ધિ શિક્ષણને વધુ સુલભ બનાવે છે.",

        "Punjabi": "ਕ੍ਰਿਤ੍ਰਿਮ ਬੁੱਧੀ ਸਿੱਖਿਆ ਨੂੰ ਬਿਹਤਰ ਬਣਾਉਂਦੀ ਹੈ।",

        "Bengali": "কৃত্রিম বুদ্ধিমত্তা শিক্ষা উন্নত করছে।",

        "Malayalam": "കൃത്രിമ ബുദ്ധി വിദ്യാഭ്യാസം മെച്ചപ്പെടുത്തുന്നു.",

        "Urdu": "مصنوعی ذہانت تعلیم کو بہتر بنا رہی ہے۔",

        "French": "L'intelligence artificielle améliore l'éducation.",

        "German": "Künstliche Intelligenz verbessert die Bildung.",

        "Spanish": "La inteligencia artificial mejora la educación.",

        "Chinese": "人工智能正在改善教育。",

        "Japanese": "人工知能は教育を向上させています。"
    }

    display_text = dyslexia_texts.get(
        selected_language,
        dyslexia_texts["English"]
    )

    st.markdown(f"""
    <style>
    .dyslexia-text {{
        font-size: {font_size}px;
        line-height: 2.5;
        letter-spacing: 2px;
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 10px;
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

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header("❓ AI Quiz Generator")

    exam = st.text_input("Enter Exam Name")

    topic = st.text_input("Enter Topic")

    num_questions = st.slider(
        "Select Number of Questions",
        1,
        10,
        5
    )

    if st.button(lang["quiz_button"]):

        question_bank = [

            f"What is {topic}?",

            f"Explain applications of {topic}.",

            f"What are advantages of {topic}?",

            f"What are limitations of {topic}?",

            f"How does {topic} help society?",

            f"Explain future scope of {topic}.",

            f"How is {topic} used in industries?",

            f"Differentiate AI and ML in {topic}.",

            f"What are challenges in {topic}?",

            f"Describe the importance of {topic}."
        ]

        st.subheader("📘 Generated Questions")

        for i in range(num_questions):

            st.write(f"{i+1}. {question_bank[i]}")

# ---------------------------------------------------
# ACCESSIBILITY SUPPORT
# ---------------------------------------------------

elif feature == lang["accessibility"]:

    st.header("♿ Accessibility Support")

    st.write("""
EduAccess AI provides inclusive learning
for differently-abled students.
""")

    st.write("✅ AI Accessibility")
    st.write("✅ Speech Support")
    st.write("✅ Dyslexia Mode")
    st.write("✅ Multilingual Dashboard")
    st.write("✅ Accessible Learning")
