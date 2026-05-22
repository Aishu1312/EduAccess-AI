import streamlit as st
from deep_translator import GoogleTranslator
import tempfile
import openai

st.set_page_config(page_title="EduAccess AI", page_icon="🚀", layout="wide")

# ---------------- LANGUAGE ---------------- #

languages = ["English","Hindi","Marathi","Tamil","Telugu"]
lang_codes = {"English":"en","Hindi":"hi","Marathi":"mr","Tamil":"ta","Telugu":"te"}

st.sidebar.title("🌐 Language Settings")
selected_language = st.sidebar.selectbox("Choose Language", languages)
lang_code = lang_codes.get(selected_language,"en")

def tr(text):
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except:
        return text

# ---------------- FEATURE NAV ---------------- #

feature_options = {
    "home":"🏠 Home",
    "summarizer":"🧠 AI Notes Summarizer",
    "speech":"🎤 Speech-to-Text",
    "dyslexia":"📖 Dyslexia Mode",
    "quiz":"❓ Quiz Generator"
}

feature_key = st.sidebar.selectbox(
    "Choose Feature",
    list(feature_options.keys()),
    format_func=lambda x: feature_options[x]
)

# ---------------- HOME ---------------- #

if feature_key == "home":
    st.title("🚀 EduAccess AI")
    st.write("AI-powered inclusive learning platform")

# ---------------- SUMMARIZER ---------------- #

elif feature_key == "summarizer":

    st.header("🧠 AI Notes Summarizer")

    text = st.text_area("Paste Notes Here", height=200)

    length = st.selectbox("Summary Length", ["Short","Medium","Detailed"])

    if st.button("Generate Summary"):

        sentences = [s.strip() for s in text.split('.') if s.strip()]

        if length == "Short":
            num = 2
        elif length == "Medium":
            num = 4
        else:
            num = len(sentences)

        summary = ". ".join(sentences[:num]) + "."

        # ✅ SAVE FOR DYSLEXIA
        st.session_state["summary"] = summary

        st.success("Summary Generated")
        st.write(summary)

# ---------------- SPEECH ---------------- #

elif feature_key == "speech":

    st.header("🎤 Speech-to-Text")

    st.subheader("🎙️ Record Voice")
    audio_value = st.audio_input("Record")

    st.subheader("📂 Upload Audio")
    file = st.file_uploader("Upload", type=["wav","mp3"])

    audio_source = None

    if audio_value:
        audio_source = audio_value
        st.audio(audio_value)

    if file:
        audio_source = file
        st.audio(file)

    if audio_source:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_source.read())
            temp_path = tmp.name

        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with open(temp_path,"rb") as f:
                transcript = openai.audio.transcriptions.create(
                    model="gpt-4o-mini-transcribe",
                    file=f
                )

            st.success("Transcribed")
            st.write(transcript.text)

        except Exception as e:
            st.error(str(e))

# ---------------- DYSLEXIA ---------------- #

elif feature_key == "dyslexia":

    st.header("📖 Dyslexia Mode")

    size = st.slider("Font Size",20,40,30)

    # ✅ USE SUMMARY
    text_display = st.session_state.get(
        "summary",
        "No summary generated yet. Please generate summary first."
    )

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

# ---------------- QUIZ ---------------- #

elif feature_key == "quiz":

    st.header("❓ Quiz Generator")

    topic = st.text_input("Enter Topic")

    if st.button("Generate Quiz"):

        quiz = [
            {
                "q": f"What is {topic}?",
                "options": ["Definition","Example","Tool","None"],
                "answer": "Definition",
                "explanation": f"{topic} refers to its definition."
            },
            {
                "q": f"Where is {topic} used?",
                "options": ["Healthcare","Sports","Cooking","None"],
                "answer": "Healthcare",
                "explanation": f"{topic} is widely used in healthcare."
            }
        ]

        for i, item in enumerate(quiz):

            st.subheader(f"Q{i+1}: {item['q']}")

            user_ans = st.radio(
                "Choose answer",
                item["options"],
                key=f"q{i}"
            )

            if st.button(f"Submit Q{i+1}"):

                if user_ans == item["answer"]:
                    st.success("✅ Correct Answer")
                else:
                    st.error("❌ Wrong Answer")
                    st.write(f"✔ Correct: {item['answer']}")
                    st.write(f"🧠 Reason: {item['explanation']}")

# ---------------- ACCESSIBILITY ---------------- #

elif feature_key == "accessibility":

    st.header("♿ Accessibility Support")

    st.write("Supports all Divyang users")
    st.write("👁️ Blind | 👂 Deaf | 🗣️ Speech | 🦽 Mobility | 🧠 Cognitive")
