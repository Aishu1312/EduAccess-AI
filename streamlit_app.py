import streamlit as st
from deep_translator import GoogleTranslator
import tempfile
import openai

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# LANGUAGE SETUP
# ---------------------------------------------------

languages = [
    "English", "Hindi", "Marathi", "Tamil", "Telugu",
    "Kannada", "Gujarati", "Punjabi", "Bengali",
    "Malayalam", "Urdu", "French", "German",
    "Spanish", "Chinese", "Japanese"
]

lang_codes = {
    "English": "en", "Hindi": "hi", "Marathi": "mr",
    "Tamil": "ta", "Telugu": "te", "Kannada": "kn",
    "Gujarati": "gu", "Punjabi": "pa", "Bengali": "bn",
    "Malayalam": "ml", "Urdu": "ur", "French": "fr",
    "German": "de", "Spanish": "es", "Chinese": "zh-cn",
    "Japanese": "ja"
}

# ---------------------------------------------------
# SIDEBAR LANGUAGE
# ---------------------------------------------------

st.sidebar.title("🌐 Language Settings")

selected_language = st.sidebar.selectbox(
    "Choose Dashboard Language",
    languages
)

lang_code = lang_codes.get(selected_language, "en")

# ---------------------------------------------------
# TRANSLATION FUNCTION
# ---------------------------------------------------

def tr(text):
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# ---------------------------------------------------
# FEATURE NAVIGATION (FIXED 🔥)
# ---------------------------------------------------

feature_options = {
    "home": "🏠 Home",
    "summarizer": "🧠 AI Notes Summarizer",
    "speech": "🎤 Speech-to-Text",
    "dyslexia": "📖 Dyslexia Mode",
    "quiz": "❓ Quiz Generator",
    "accessibility": "♿ Accessibility Support"
}

feature_key = st.sidebar.selectbox(
    tr("Choose Feature"),
    list(feature_options.keys()),
    format_func=lambda x: tr(feature_options[x])
)

# ---------------------------------------------------
# ACCESSIBILITY SETTINGS
# ---------------------------------------------------

st.sidebar.markdown("### ♿ Accessibility")

font_size = st.sidebar.slider(tr("Font Size"), 14, 30, 18)
contrast = st.sidebar.checkbox(tr("High Contrast Mode"))

bg = "#000000" if contrast else "#050816"
text = "#FFFFFF" if contrast else "#E5E7EB"

st.markdown(f"""
<style>
body {{
    background-color: {bg};
    color: {text};
    font-size: {font_size}px;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HOME
# ---------------------------------------------------

if feature_key == "home":

    st.title(tr("🚀 EduAccess AI"))
    st.subheader(tr("AI-Powered Accessibility Platform"))

    st.write(tr(
        "An inclusive platform for blind, deaf, speech-impaired, and physically challenged students."
    ))

    st.markdown("---")

    st.header(tr("🌟 Core Features"))

    col1, col2 = st.columns(2)

    with col1:
        st.info(tr("🧠 AI Notes Summarizer"))
        st.write(tr("Generate summaries from notes"))

        st.success(tr("🎤 Speech-to-Text"))
        st.write(tr("Convert voice into text"))

    with col2:
        st.warning(tr("📖 Dyslexia Mode"))
        st.write(tr("Easy reading UI"))

        st.error(tr("❓ Quiz Generator"))
        st.write(tr("Generate exam questions"))

# ---------------------------------------------------
# SUMMARIZER
# ---------------------------------------------------

elif feature == lang["summarizer"]:

    import openai
    import tempfile

    st.header("🧠 AI Notes Summarizer + Voice Assistant")

    # ---------------- TEXT INPUT ---------------- #

    sample_text = """Artificial Intelligence is transforming education through accessibility and smart learning systems."""

    text = st.text_area(
        "Paste Notes Here",
        value=sample_text,
        height=200
    )

    summary_length = st.selectbox(
        "Select Summary Length",
        ["Short", "Medium", "Detailed"]
    )

    # ---------------- VOICE INPUT ---------------- #

    st.markdown("### 🎤 Ask Using Voice")

    audio_value = st.audio_input("🎙️ Record Your Question")

    voice_text = ""

    if audio_value:

        st.audio(audio_value)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_value.read())
            temp_path = tmp.name

        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with open(temp_path, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=f
                )

            voice_text = transcript.text

            st.success("✅ Voice Converted to Text")

            st.write("📝 You said:")
            st.write(voice_text)

        except Exception as e:
            st.error("Error in voice recognition")
            st.write(str(e))

    # ---------------- SUMMARIZER ---------------- #

    if st.button(lang["summary_button"]):

        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if summary_length == "Short":
            num = max(2, len(sentences)//4)

        elif summary_length == "Medium":
            num = max(4, len(sentences)//2)

        else:
            num = len(sentences)

        summary = ". ".join(sentences[:num]) + "."

        st.success("✅ Summary Generated")

        st.markdown(f"""
        <div style="
            background-color:#14532d;
            padding:15px;
            border-radius:10px;
            color:white;
        ">
        {summary}
        </div>
        """, unsafe_allow_html=True)

    # ---------------- AI ANSWER FROM VOICE ---------------- #

    if voice_text:

        st.markdown("---")
        st.subheader("🤖 AI Answer")

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI tutor."},
                    {"role": "user", "content": voice_text}
                ]
            )

            answer = response.choices[0].message.content

            st.markdown(f"""
            <div style="
                background-color:#1e3a8a;
                padding:15px;
                border-radius:10px;
                color:white;
            ">
            {answer}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error("AI response error")
            st.write(str(e))

# ---------------------------------------------------
# SPEECH TO TEXT (REAL AI 🔥)
# ---------------------------------------------------

elif feature_key == "speech":

    st.header(tr("🎤 Speech-to-Text"))

    st.write(tr("Upload audio file to convert speech into text"))

    audio_file = st.file_uploader(
        tr("Upload Audio"),
        type=["wav", "mp3", "m4a"]
    )

    if audio_file is not None:

        st.audio(audio_file)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            temp_path = tmp.name

        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with open(temp_path, "rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=f
                )

            st.success(tr("Transcription Successful"))
            st.subheader(tr("📝 Transcribed Text"))

            st.write(transcript.text)

        except Exception as e:
            st.error(tr("Error in transcription"))
            st.write(str(e))

# ---------------------------------------------------
# DYSLEXIA MODE
# ---------------------------------------------------

elif feature_key == "dyslexia":

    st.header(tr("📖 Dyslexia Mode"))

    size = st.slider(tr("Adjust Font Size"), 20, 40, 30)

    text_display = tr("Artificial Intelligence improves accessible education.")

    st.markdown(f"""
    <div style="
        font-size:{size}px;
        line-height:2.5;
        letter-spacing:2px;
        background:#f4f4f4;
        padding:20px;
        border-radius:10px;
        color:black;">
        {text_display}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# QUIZ
# ---------------------------------------------------

elif feature_key == "quiz":

    st.header(tr("❓ Quiz Generator"))

    topic = st.text_input(tr("Enter Topic"))

    if st.button(tr("Generate Quiz")):

        questions = [
            f"What is {topic}?",
            f"Explain {topic}",
            f"Advantages of {topic}",
            f"Limitations of {topic}",
            f"Applications of {topic}"
        ]

        for i, q in enumerate(questions):
            st.write(f"{i+1}. {tr(q)}")

# ---------------------------------------------------
# ACCESSIBILITY
# ---------------------------------------------------

elif feature_key == "accessibility":

    st.header(tr("♿ Accessibility Support"))

    st.write(tr("Designed for all Divyang users"))

    st.write(tr("👁️ Blind: Screen reader + audio"))
    st.write(tr("👂 Deaf: Text-based UI"))
    st.write(tr("🗣️ Mute: Text interaction"))
    st.write(tr("🦽 Mobility: Large UI"))
    st.write(tr("🧠 Learning disabilities support"))
