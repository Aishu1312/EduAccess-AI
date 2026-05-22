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

    st.header("🎤 Speech-to-Text + AI Answer")

    st.subheader("🎙️ Record Voice")
    audio_value = st.audio_input("Record")

    st.subheader("📂 Upload Audio")
    file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

    audio_source = None

    if audio_value:
        audio_source = audio_value
        st.audio(audio_value)

    elif file:
        audio_source = file
        st.audio(file)

    if audio_source:

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_source.read())
                temp_path = tmp.name

            if "OPENAI_API_KEY" not in st.secrets:
                st.warning("API key missing. Showing demo output.")
                text = "What is Artificial Intelligence?"
            else:
                openai.api_key = st.secrets["OPENAI_API_KEY"]

                with open(temp_path, "rb") as f:
                    transcript = openai.audio.transcriptions.create(
                        model="gpt-4o-mini-transcribe",
                        file=f
                    )
                text = transcript.text

            st.success("📝 Transcribed Text")
            st.write(text)

            # 🔥 AI ANSWER
            if "OPENAI_API_KEY" in st.secrets:

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful tutor."},
                        {"role": "user", "content": text}
                    ]
                )

                answer = response.choices[0].message.content

                st.markdown("### 🤖 AI Answer")
                st.success(answer)

        except Exception as e:
            st.error("Error processing audio")
            st.write(str(e))

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
                key=f"radio_{i}"
            )

            if st.button(f"Submit Answer {i+1}", key=f"btn_{i}"):

                if user_ans == item["answer"]:
                    st.success("✅ Correct Answer")
                else:
                    st.error("❌ Wrong Answer")
                    st.write(f"✔ Correct Answer: {item['answer']}")
                    st.write(f"🧠 Explanation: {item['explanation']}")

            st.markdown("---")

# ---------------- ACCESSIBILITY ---------------- #

elif feature_key == "accessibility":

    st.header("♿ Accessibility Support")

    st.write("Supports all Divyang users")
    st.write("👁️ Blind | 👂 Deaf | 🗣️ Speech | 🦽 Mobility | 🧠 Cognitive")
