import streamlit as st

st.set_page_config(
    page_title="EduAccess AI",
    layout="wide"
)

# Title
st.title("🚀 EduAccess AI")
st.subheader("AI-Powered Accessibility Platform for Disabled Students")

# Sidebar
feature = st.sidebar.selectbox(
    "Choose Feature",
    [
        "Home",
        "AI Notes Summarizer",
        "Speech-to-Text",
        "Dyslexia-Friendly Mode",
        "Quiz Generator"
    ]
)

# HOME PAGE
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

# SUMMARIZER
elif feature == "🧠 AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    st.write("""
    Paste educational notes, research content, or study material
    and generate an AI-powered concise summary.
    """)

    text = st.text_area(
        "Paste Notes Here",
        height=250
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
                summary = '.'.join(sentences[:6])

            st.success("Summary Generated Successfully")

            st.subheader("📄 Generated Summary")

            st.write(summary)

        else:
            st.warning("Please enter notes.")

# SPEECH TO TEXT
elif feature == "🎤 Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    st.write("Convert your voice into text using AI.")

    audio_value = st.audio_input("Record your voice")

    if audio_value:
        st.success("Audio recorded successfully!")

        st.audio(audio_value)

        st.info("Speech recognition processing feature can be integrated here.")

# DYSLEXIA MODE
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
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '''
        <div class="dyslexia-text">
        Artificial Intelligence is transforming education by
        making learning more personalized, accessible, and inclusive
        for students across the world.
        </div>
        ''',
        unsafe_allow_html=True
    )

    st.success("Accessibility mode enabled successfully.")

# QUIZ GENERATORelif feature == "❓ Quiz Generator":

    st.header("❓ AI Quiz Generator")

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
                f"{num_questions} questions generated for {exam}"
            )

            for i in range(1, num_questions + 1):

                st.write(
                    f"{i}. Explain {topic} concept related to {exam} exam."
                )

        else:
            st.warning("Please enter exam name and topic.")
