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

session_defaults = {
    "summary": "",
    "quiz_started": False,
    "quiz_score": 0,
    "quiz_data": [],
    "answer_feedback": {},
    "quiz_history": [],
    "last_feature": "",
    "notes_history": [],
    "speech_history": []
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# LANGUAGES
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
    "speech": "🎤 Speech-to-Text",
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
# RESET QUIZ WHEN LEAVING QUIZ PAGE
# ---------------------------------------------------

if (
    st.session_state.last_feature == lang["quiz"]
    and feature != lang["quiz"]
):

    st.session_state.quiz_started = False
    st.session_state.quiz_score = 0
    st.session_state.quiz_data = []
    st.session_state.answer_feedback = {}

st.session_state.last_feature = feature

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
                "🎤 Speech-to-Text"
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

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    st.header(
        translate_text("🧠 AI Notes Summarizer")
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button(
            translate_text("🆕 New Notes")
        ):

            st.session_state.summary = ""
            st.rerun()

    sample_text = """
Artificial Intelligence is transforming education
through accessibility and smart learning systems.
"""

    text = st.text_area(
        translate_text("📌 Paste Notes Here"),
        value=sample_text,
        height=250
    )

    summary_length = st.selectbox(
        translate_text("📏 Select Summary Length"),
        ["Short", "Medium", "Detailed"]
    )

    if st.button(
        translate_text("🚀 Generate Summary")
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

        summary = ". ".join(sentences[:num]) + "."

        translated_summary = translate_text(summary)

        st.session_state.summary = translated_summary

        st.session_state.notes_history.append(
            translated_summary
        )

        st.success(
            translate_text("✅ Summary Generated")
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
        {translated_summary}
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.notes_history:

        st.markdown("---")

        st.subheader(
            translate_text("📘 Notes History")
        )

        for item in reversed(
            st.session_state.notes_history
        ):

            st.info(item)

# ---------------------------------------------------
# SPEECH TO TEXT
# ---------------------------------------------------

elif feature == lang["speech"]:

    st.header(
        translate_text("🎤 Speech-to-Text")
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button(
            translate_text("🆕 New Speech")
        ):

            st.rerun()

    answer_type = st.selectbox(
        translate_text("📚 Select Explanation Type"),
        ["Short", "Medium", "Detailed"]
    )

    audio = st.audio_input(
        translate_text("🎙️ Record Voice")
    )

    uploaded_file = st.file_uploader(
        translate_text("📂 Upload Audio"),
        type=["wav", "mp3", "m4a"]
    )

    source = audio if audio else uploaded_file

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

        if text:

            st.subheader(
                translate_text("🤖 AI Explanation")
            )

            if answer_type == "Short":

                answer = f"""
{text} is an important topic.

Real-world Example:
Used in education, business, and technology.
"""

            elif answer_type == "Medium":

                answer = f"""
{text} is an important concept used in academics and industries.

Key Points:
• Improves learning
• Helps solve problems
• Used in modern systems

Real-world Examples:
• Education
• Healthcare
• Business technologies
"""

            else:

                answer = f"""
{text} is an important concept used in science, education, and technology.

Advantages:
• Better learning
• Improved productivity
• Smart automation
• Problem-solving

Real-world Examples:
• Educational systems
• AI platforms
• Healthcare technologies
• Banking software

Understanding {text} helps students and professionals apply concepts practically.
"""

            translated_answer = translate_text(answer)

            st.session_state.speech_history.append({
                "question": text,
                "answer": translated_answer
            })

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

    if st.session_state.speech_history:

        st.markdown("---")

        st.subheader(
            translate_text("📜 Speech History")
        )

        for item in reversed(
            st.session_state.speech_history
        ):

            st.info(
                translate_text(
                    f"Question: {item['question']}"
                )
            )

            st.success(item["answer"])

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature == lang["dyslexia"]:

    st.header(
        translate_text("📖 Dyslexia-Friendly Reading")
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
        translate_text("❓ AI Quiz Generator")
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            translate_text("🆕 New Quiz")
        ):

            st.session_state.quiz_started = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_data = []
            st.session_state.answer_feedback = {}
            st.rerun()

    exam = st.text_input(
        translate_text("📝 Enter Exam Name")
    )

    topic = st.text_input(
        translate_text("📘 Enter Topic")
    )

    num_questions = st.slider(
        translate_text("📊 Select Number of Questions"),
        1,
        15,
        5
    )

    if st.button(
        translate_text("🚀 Generate Quiz")
    ):

        st.session_state.quiz_started = True
        st.session_state.quiz_score = 0
        st.session_state.answer_feedback = {}

        question_bank = []

        for i in range(15):

            question_bank.append({

                "question":
                f"What is the importance of {topic}?",

                "correct":
                f"{topic} supports smart digital systems",

                "wrong": [
                    f"{topic} has no practical use",
                    f"{topic} decreases productivity",
                    f"{topic} removes innovation"
                ],

                "reason":
                f"{topic} improves automation, productivity, and modern learning."
            })

        random.shuffle(question_bank)

        st.session_state.quiz_data = question_bank[:num_questions]

        for q in st.session_state.quiz_data:

            options = [q["correct"]] + q["wrong"]

            random.shuffle(options)

            q["options"] = options

    if st.session_state.quiz_started:

        for idx, q in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown("---")

            st.subheader(
                f"Q{idx+1}. {translate_text(q['question'])}"
            )

            translated_options = [
                translate_text(opt)
                for opt in q["options"]
            ]

            selected = st.radio(
                translate_text("Choose Answer"),
                translated_options,
                key=f"radio_{idx}"
            )

            if st.button(
                translate_text(f"Submit Q{idx+1}"),
                key=f"submit_{idx}"
            ):

                correct_translated = translate_text(
                    q["correct"]
                )

                is_correct = (
                    selected == correct_translated
                )

                if is_correct:

                    st.session_state.quiz_score += 2

                st.session_state.answer_feedback[idx] = {

                    "correct": is_correct,
                    "correct_answer": q["correct"],
                    "reason": q["reason"],
                    "points": 2 if is_correct else 0
                }

                st.session_state.quiz_history.append({

                    "question": q["question"],
                    "selected": selected,
                    "correct": q["correct"],
                    "reason": q["reason"]
                })

            if idx in st.session_state.answer_feedback:

                feedback = st.session_state.answer_feedback[idx]

                if feedback["correct"]:

                    st.success(
                        translate_text(
                            "✅ Correct Answer"
                        )
                    )

                    st.balloons()

                else:

                    st.error(
                        translate_text(
                            "❌ Wrong Answer"
                        )
                    )

                st.info(
                    translate_text(
                        f"✔ Correct Answer: {feedback['correct_answer']}"
                    )
                )

                st.warning(
                    translate_text(
                        f"📖 Reason: {feedback['reason']}"
                    )
                )

                st.success(
                    translate_text(
                        f"🏆 Points Achieved: {feedback['points']}"
                    )
                )

        st.markdown("---")

        total_score = len(
            st.session_state.quiz_data
        ) * 2

        st.header(
            translate_text(
                f"🎯 Final Score: {st.session_state.quiz_score}/{total_score}"
            )
        )

        st.markdown("---")

        st.subheader(
            translate_text("📘 Quiz History")
        )

        for item in reversed(
            st.session_state.quiz_history
        ):

            st.info(
                translate_text(
                    f"Question: {item['question']}"
                )
            )

            st.write(
                translate_text(
                    f"Your Answer: {item['selected']}"
                )
            )

            st.success(
                translate_text(
                    f"Correct Answer: {item['correct']}"
                )
            )

            st.warning(
                translate_text(
                    f"Reason: {item['reason']}"
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
