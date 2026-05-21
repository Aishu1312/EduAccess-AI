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
if feature == "Home":
    st.header("Welcome to EduAccess AI")

    st.write("""
    EduAccess AI is an intelligent accessibility platform designed
    to help disabled students learn more effectively using AI,
    NLP, speech technologies, and inclusive design.
    """)

    st.markdown("### Features")
    st.write("✅ AI Notes Summarizer")
    st.write("✅ Speech-to-Text")
    st.write("✅ Dyslexia-Friendly Reading")
    st.write("✅ AI Quiz Generator")
    st.write("✅ Accessibility Support")

# SUMMARIZER
elif feature == "AI Notes Summarizer":

    st.header("🧠 AI Notes Summarizer")

    text = st.text_area("Paste your educational notes here")

    if st.button("Generate Summary"):

        if text:
            summary = text[:300] + "..."

            st.success("Summary Generated Successfully")
            st.write(summary)

        else:
            st.warning("Please enter some notes.")

# SPEECH TO TEXT
elif feature == "Speech-to-Text":

    st.header("🎤 Speech-to-Text")

    st.write("""
    This feature converts spoken audio into text
    for accessibility support.
    """)

    st.info("Speech recognition demo feature.")

# DYSLEXIA MODE
elif feature == "Dyslexia-Friendly Mode":

    st.header("📖 Dyslexia-Friendly Reading Mode")

    st.markdown("""
    <style>
    .dyslexia-font {
        font-size:24px;
        line-height:2;
        letter-spacing:2px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p class="dyslexia-font">'
        'This is a dyslexia-friendly reading mode example.'
        '</p>',
        unsafe_allow_html=True
    )

# QUIZ GENERATOR
elif feature == "Quiz Generator":

    st.header("❓ AI Quiz Generator")

    topic = st.text_input("Enter Quiz Topic")

    if st.button("Generate Quiz"):

        if topic:

            st.write(f"### Quiz on {topic}")

            st.write("1. What is Artificial Intelligence?")
            st.write("2. Explain NLP.")
            st.write("3. What is Machine Learning?")

        else:
            st.warning("Please enter a topic.")
