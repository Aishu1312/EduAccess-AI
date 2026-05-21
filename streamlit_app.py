import streamlit as st

st.set_page_config(page_title="EduAccess AI")

st.title("🚀 EduAccess AI")
st.subheader("AI-Powered Accessibility Platform")

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

if feature == "Home":
    st.write("Welcome to EduAccess AI")

elif feature == "AI Notes Summarizer":
    text = st.text_area("Paste Notes")

    if st.button("Summarize"):
        st.success("Summary Generated")
        st.write(text[:200] + "...")

elif feature == "Speech-to-Text":
    st.write("Speech-to-text feature demo")

elif feature == "Dyslexia-Friendly Mode":
    st.markdown("""
    <style>
    .big-font {
        font-size:24px !important;
        line-height:2;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p class="big-font">Dyslexia-friendly reading mode enabled.</p>',
        unsafe_allow_html=True
    )

elif feature == "Quiz Generator":
    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):
        st.write("1. What is AI?")
        st.write("2. Define NLP.")
