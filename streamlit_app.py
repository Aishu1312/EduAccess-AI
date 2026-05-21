import streamlit as st

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🚀 EduAccess AI")

feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "🏠 Home",
        "🧠 AI Notes Summarizer",
        "🎤 Speech-to-Text",
        "📖 Dyslexia-Friendly Mode",
        "❓ Quiz Generator",
        "♿ Accessibility Support"
    ]
)

# -----------------------------------
# HOME PAGE
# -----------------------------------

if feature == "🏠 Home":

    st.title("🚀 EduAccess AI")

    st.subheader(
        "AI-Powered Accessibility Platform for Disabled Students"
    )

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

elif feature == "🧠 AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    st.write("""
    Paste educational notes, research content,
    or study material and generate an AI-powered summary.
    """)

    sample_text = """
Artificial Intelligence (AI) is a branch of computer science
that enables machines to perform tasks that normally require
human intelligence. These tasks include learning, reasoning,
problem-solving, understanding language, and recognizing patterns.
AI technologies are widely used in healthcare, education,
finance, transportation, and cybersecurity.

Machine Learning is a subset of AI where systems learn from
data without explicit programming. Deep Learning is another
subset that uses neural networks to process large amounts of data.
Natural Language Processing (NLP) allows machines to understand
human language and generate responses.

AI is transforming modern industries by improving efficiency,
reducing human effort, and enabling automation. However,
ethical concerns such as data privacy, bias, and job displacement
must also be addressed.
"""

    st.info("📌 Sample Notes Added Below For Testing")

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

            word_count = len(text.split())

            st.info(f"📊 Total Word Count: {word_count}")

        else:
            st.warning("Please enter notes.")

# -----------------------------------
# SPEECH TO TEXT
# -----------------------------------

elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    st.write("""
    Convert your voice into text using AI-powered
    speech recognition technology.
    """)

    st.markdown("## 🎙️ Microphone Recording")

    audio_value = st.audio_input("Click the microphone and record your voice")

    if audio_value:

        st.success("✅ Audio Recorded Successfully!")

        st.audio(audio_value)

        st.info("""
        AI speech recognition can be integrated here
        using Google Speech API or OpenAI Whisper.
        """)

        st.write("📝 Transcribed Text Placeholder:")
        st.write("\"Hello, welcome to EduAccess AI speech recognition system.\"")

# -----------------------------------
# DYSLEXIA MODE
# -----------------------------------

elif feature == "📖 Dyslexia-Friendly Mode":

    st.header("📖 Dyslexia-Friendly Reading Mode")

    st.write("""
    This mode improves readability for students with dyslexia
    by increasing spacing, font size, and visual clarity.
    """)

    st.markdown("""
    <style>
    .dyslexia-text {
        font-size: 28px;
        line-height: 2.5;
        letter-spacing: 2px;
        font-family: Arial, sans-serif;
        background-color: #f4f4f4;
        padding: 20px;
        border-radius: 10px;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <div class="dyslexia-text">
        Artificial Intelligence is transforming education by
        making learning more personalized, accessible,
        and inclusive for students across the world.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.success("✅ Accessibility Mode Enabled Successfully")

# -----------------------------------
# QUIZ GENERATOR
# -----------------------------------

elif feature == "❓ Quiz Generator":

    st.header("❓ AI Quiz Generator")

    st.write("""
    Generate customized AI-based quiz questions
    for competitive exams and academic preparation.
    """)

    exam = st.text_input(
        "Enter Exam Name",
        placeholder="Example: UPSC, JEE, NEET, Python Interview"
    )

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Artificial Intelligence"
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
                f"✅ {num_questions} questions generated for {exam}"
            )

            st.subheader("📘 Generated Quiz Questions")

            for i in range(1, num_questions + 1):

                st.write(
                    f"{i}. Explain {topic} concept related to {exam} exam ({difficulty} level)."
                )

        else:
            st.warning("⚠️ Please enter exam name and topic.")

# -----------------------------------
# ACCESSIBILITY SUPPORT
# -----------------------------------

elif feature == "♿ Accessibility Support":

    st.header("♿ Accessibility Support")

    st.write("""
    EduAccess AI is designed to provide inclusive learning
    support for students with disabilities and learning challenges.
    """)

    st.markdown("---")

    st.subheader("🌟 Supported Accessibility Features")

    st.write("✅ Dyslexia-Friendly Reading")
    st.write("✅ Speech-to-Text Conversion")
    st.write("✅ AI Learning Assistance")
    st.write("✅ Large Readable Fonts")
    st.write("✅ Accessible Learning Interface")
    st.write("✅ AI Quiz Support")

    st.markdown("---")

    st.subheader("🎯 Goal of EduAccess AI")

    st.write("""
    Our goal is to make education more accessible,
    inclusive, and AI-powered for future generations.
    """)

    st.success("✅ Accessibility Support Enabled")
