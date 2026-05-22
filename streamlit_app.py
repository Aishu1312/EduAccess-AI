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

    import tempfile
    import openai

    st.header("🎤 Speech-to-Text + AI Answer")

    st.write("Convert voice into text and get AI answer.")

    # 🎙️ MIC INPUT
    st.subheader("🎙️ Record Voice")
    audio_value = st.audio_input("Record your voice")

    # 📂 FILE UPLOAD
    st.subheader("📂 Upload Audio")
    uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])

    audio_source = None

    if audio_value:
        audio_source = audio_value
        st.audio(audio_value)

    elif uploaded_file:
        audio_source = uploaded_file
        st.audio(uploaded_file)

    if audio_source:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_source.read())
            temp_path = tmp.name

        try:
            if "OPENAI_API_KEY" not in st.secrets:
                st.warning("API key missing — showing demo output.")
                user_text = "What is Artificial Intelligence?"
            else:
                openai.api_key = st.secrets["OPENAI_API_KEY"]

                with open(temp_path, "rb") as f:
                    transcript = openai.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=f
                    )
                user_text = transcript.text

            st.success("📝 Transcribed Text")
            st.write(user_text)

            # 🤖 AI ANSWER
            if "OPENAI_API_KEY" in st.secrets:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful tutor."},
                        {"role": "user", "content": user_text}
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown("### 🤖 AI Answer")
                st.success(answer)

        except Exception as e:
            st.error("Error processing audio")
            st.write(str(e))

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header("📖 Dyslexia-Friendly Reading Mode")

    font_size = st.slider("Adjust Font Size", 20, 40, 30)

    # ✅ Use summary if available
    display_text = st.session_state.get("summary", "")

if not display_text:
    st.warning("⚠️ Generate summary first in Summarizer section")
else:
    st.markdown(f""" ... """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="
        font-size: {font_size}px;
        line-height: 2.5;
        letter-spacing: 2px;
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 10px;
        color: black;
    ">
    {display_text}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ GENERATOR
# ---------------------------------------------------

elif feature == lang["quiz"]:

    st.header("❓ AI Quiz Generator")

    topic = st.text_input("Enter Topic")

    if st.button(lang["quiz_button"]):

        st.session_state.quiz = [
            {
                "q": f"What is {topic}?",
                "options": ["Definition", "Example", "Tool", "None"],
                "answer": "Definition",
                "explanation": f"{topic} refers to its definition."
            },
            {
                "q": f"Where is {topic} used?",
                "options": ["Healthcare", "Sports", "Cooking", "None"],
                "answer": "Healthcare",
                "explanation": f"{topic} is widely used in healthcare."
            }
        ]

    if "quiz" in st.session_state:

        for i, item in enumerate(st.session_state.quiz):

            st.subheader(f"Q{i+1}: {item['q']}")

            user_ans = st.radio(
                "Choose answer",
                item["options"],
                key=f"q_{i}"
            )

            if st.button(f"Submit Answer {i+1}", key=f"btn_{i}"):

                if user_ans == item["answer"]:
                    st.success("✅ Correct Answer")
                else:
                    st.error("❌ Wrong Answer")
                    st.write(f"✔ Correct Answer: {item['answer']}")
                    st.write(f"🧠 Explanation: {item['explanation']}")

            st.markdown("---")

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
