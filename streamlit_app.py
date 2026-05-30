import streamlit as st
import os, json, re, time, base64, hashlib, random, io
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# ── optional heavy imports (graceful fallback) ──────────────
try:
    import google.generativeai as genai
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

try:
    from gtts import gTTS
    GTTS_OK = True
except ImportError:
    GTTS_OK = False

try:
    import PyPDF2
    PDF_OK = True
except ImportError:
    PDF_OK = False

try:
    from deep_translator import GoogleTranslator
    TRANS_OK = True
except ImportError:
    TRANS_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_OK = True
except ImportError:
    REPORTLAB_OK = False

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  28 SUPPORTED LANGUAGES
# ══════════════════════════════════════════════════════════════
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Marathi": "mr", "Telugu": "te",
    "Tamil": "ta", "Kannada": "kn", "Malayalam": "ml", "Bengali": "bn",
    "Gujarati": "gu", "Punjabi": "pa", "Odia": "or", "Urdu": "ur",
    "Spanish": "es", "French": "fr", "German": "de", "Portuguese": "pt",
    "Italian": "it", "Dutch": "nl", "Russian": "ru", "Arabic": "ar",
    "Japanese": "ja", "Chinese (Simplified)": "zh-CN", "Korean": "ko",
    "Turkish": "tr", "Polish": "pl", "Swedish": "sv", "Norwegian": "no",
    "Swahili": "sw",
}

LANG_NAMES = list(LANGUAGES.keys())

# ══════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "logged_in": False, "username": "", "role": "student",
        "users": {}, "progress": {}, "quiz_scores": [], "chat_history": [],
        "dyslexia_mode": False, "high_contrast": False, "font_size": "Medium",
        "lang": "English", "leaderboard": [], "page": "🏠 Home",
        "gemini_key": "", "gemini_configured": False,
        "current_quiz": [], "quiz_answers": {}, "quiz_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════
#  GEMINI SETUP
# ══════════════════════════════════════════════════════════════
def configure_gemini(api_key: str):
    if GEMINI_OK and api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.gemini_configured = True
            return True
        except Exception:
            pass
    return False

def gemini_chat(prompt: str, system: str = "") -> str:
    if not (GEMINI_OK and st.session_state.gemini_configured):
        return "⚠️ Gemini API not configured. Please add your API key in the sidebar."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        full = f"{system}\n\n{prompt}" if system else prompt
        response = model.generate_content(full)
        return response.text
    except Exception as e:
        return f"❌ AI Error: {str(e)}"

# ══════════════════════════════════════════════════════════════
#  TRANSLATION HELPER
# ══════════════════════════════════════════════════════════════
def translate_text(text: str, target_lang_code: str) -> str:
    if target_lang_code == "en" or not TRANS_OK:
        return text
    try:
        return GoogleTranslator(source="auto", target=target_lang_code).translate(text[:4999])
    except Exception:
        return text

def t(text: str) -> str:
    """Translate to selected UI language."""
    code = LANGUAGES.get(st.session_state.lang, "en")
    if code == "en":
        return text
    return translate_text(text, code)

# ══════════════════════════════════════════════════════════════
#  STYLING  (Dyslexia / High-contrast / Font-size)
# ══════════════════════════════════════════════════════════════
FONT_SIZES = {"Small": "14px", "Medium": "17px", "Large": "21px", "Extra Large": "26px"}

def apply_styles():
    fs = FONT_SIZES.get(st.session_state.font_size, "17px")
    dyslexia_font = "'OpenDyslexic', 'Comic Sans MS', Arial, sans-serif" if st.session_state.dyslexia_mode else "'Segoe UI', Arial, sans-serif"
    bg = "#0a0a0a" if st.session_state.high_contrast else "#0f1117"
    text_color = "#ffffff" if st.session_state.high_contrast else "#fafafa"
    card_bg = "#1a1a1a" if st.session_state.high_contrast else "#1e2130"
    accent = "#FFD700" if st.session_state.high_contrast else "#6C63FF"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=OpenDyslexic&display=swap');

    html, body, [class*="css"] {{
        font-family: {dyslexia_font} !important;
        font-size: {fs} !important;
        background-color: {bg} !important;
        color: {text_color} !important;
    }}
    .stApp {{ background-color: {bg}; }}
    .edu-card {{
        background: {card_bg};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid {accent};
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}
    .hero-title {{
        font-size: 2.8em; font-weight: 900;
        background: linear-gradient(135deg, {accent}, #FF6B9D);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 8px;
    }}
    .badge {{
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        font-size: 0.8em; font-weight: bold;
        background: {accent}33; color: {accent}; margin: 2px;
    }}
    .quiz-option {{
        background: {card_bg}; border: 2px solid #333;
        border-radius: 10px; padding: 10px 16px; margin: 6px 0;
        cursor: pointer; transition: all 0.2s;
    }}
    .quiz-option:hover {{ border-color: {accent}; }}
    .correct {{ border-color: #22c55e !important; background: #22c55e22 !important; }}
    .wrong   {{ border-color: #ef4444 !important; background: #ef444422 !important; }}
    .chat-user {{ background:#2d2d4e; border-radius:12px; padding:10px 14px; margin:6px 0; text-align:right; }}
    .chat-bot  {{ background:#1e3a5f; border-radius:12px; padding:10px 14px; margin:6px 0; }}
    .cert-box {{
        border: 6px double {accent}; border-radius: 20px;
        padding: 40px; text-align: center; margin: 20px 0;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
    }}
    .stButton>button {{
        background: linear-gradient(135deg, {accent}, #FF6B9D);
        color: white; border: none; border-radius: 10px;
        font-weight: 700; transition: all 0.3s;
    }}
    .stButton>button:hover {{ opacity: 0.85; transform: translateY(-1px); }}
    .metric-card {{
        background: {card_bg}; border-radius: 12px;
        padding: 18px; text-align: center;
        border: 1px solid {accent}44;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# ══════════════════════════════════════════════════════════════
#  AUTH HELPERS
# ══════════════════════════════════════════════════════════════
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, role="student"):
    if username in st.session_state.users:
        return False, "Username already exists."
    st.session_state.users[username] = {
        "password": hash_pw(password), "role": role,
        "joined": datetime.now().strftime("%Y-%m-%d"),
        "xp": 0, "badges": [], "completed_quizzes": 0,
    }
    st.session_state.progress[username] = []
    return True, "Registered successfully!"

def login_user(username, password):
    u = st.session_state.users.get(username)
    if u and u["password"] == hash_pw(password):
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.role = u["role"]
        return True, "Login successful!"
    return False, "Invalid credentials."

# ══════════════════════════════════════════════════════════════
#  TEXT → SPEECH
# ══════════════════════════════════════════════════════════════
def text_to_speech(text: str, lang_code: str = "en"):
    if not GTTS_OK:
        st.warning("gTTS not installed.")
        return
    try:
        buf = io.BytesIO()
        tts = gTTS(text=text[:3000], lang=lang_code, slow=False)
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf, format="audio/mp3")
    except Exception as e:
        st.error(f"TTS Error: {e}")

# ══════════════════════════════════════════════════════════════
#  PDF TEXT EXTRACT
# ══════════════════════════════════════════════════════════════
def extract_pdf_text(uploaded_file) -> str:
    if not PDF_OK:
        return "PyPDF2 not installed."
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        return f"PDF Error: {e}"

# ══════════════════════════════════════════════════════════════
#  AI SUMMARIZE
# ══════════════════════════════════════════════════════════════
def ai_summarize(text: str, lang: str = "English") -> str:
    prompt = f"""Summarize the following text in {lang} language.
Make it easy to understand for a student with learning difficulties.
Use simple words, short sentences, and bullet points where possible.

TEXT:
{text[:4000]}

SUMMARY:"""
    return gemini_chat(prompt)

# ══════════════════════════════════════════════════════════════
#  AI QUIZ GENERATION
# ══════════════════════════════════════════════════════════════
def generate_quiz(text: str, num_q: int = 5, difficulty: str = "Medium") -> list:
    prompt = f"""Generate exactly {num_q} multiple-choice questions from the text below.
Difficulty: {difficulty}. Format as valid JSON array:
[{{"question":"...","options":["A","B","C","D"],"answer":"A","explanation":"..."}}]
Only return the JSON array, nothing else.

TEXT: {text[:3000]}"""
    raw = gemini_chat(prompt)
    try:
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception:
        # fallback sample
        return [{
            "question": "What is the main topic of this text?",
            "options": ["Learning", "Technology", "Science", "History"],
            "answer": "Learning",
            "explanation": "Based on the content provided."
        }]

# ══════════════════════════════════════════════════════════════
#  CERTIFICATE GENERATOR (PDF via reportlab)
# ══════════════════════════════════════════════════════════════
def generate_certificate(name: str, topic: str, score: int, date: str) -> bytes:
    if not REPORTLAB_OK:
        return b""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=60, bottomMargin=60)
    styles = getSampleStyleSheet()
    gold = colors.HexColor("#FFD700")
    elements = []
    title_style = ParagraphStyle("title", fontSize=32, textColor=gold,
                                  alignment=1, spaceAfter=20, fontName="Helvetica-Bold")
    sub_style   = ParagraphStyle("sub",   fontSize=16, textColor=colors.white,
                                  alignment=1, spaceAfter=12)
    body_style  = ParagraphStyle("body",  fontSize=13, textColor=colors.lightgrey,
                                  alignment=1, spaceAfter=8)
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("🎓 CERTIFICATE OF ACHIEVEMENT", title_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("This is to certify that", body_style))
    elements.append(Paragraph(f"<b>{name}</b>", sub_style))
    elements.append(Paragraph("has successfully completed the quiz on", body_style))
    elements.append(Paragraph(f"<b>{topic}</b>", sub_style))
    elements.append(Paragraph(f"with a score of <b>{score}%</b>", body_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Date: {date}", body_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("EduAccess AI — Empowering Every Learner", body_style))
    doc.build(elements)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown('<div style="text-align:center;font-size:2em;">🎓 EduAccess AI</div>', unsafe_allow_html=True)
        st.markdown("---")

        # ── API Key ─────────────────────────────────────────
        with st.expander("🔑 Gemini API Key", expanded=not st.session_state.gemini_configured):
            key = st.text_input("API Key", type="password", value=st.session_state.gemini_key,
                                help="Get free key at aistudio.google.com")
            if st.button("Configure AI"):
                if configure_gemini(key):
                    st.session_state.gemini_key = key
                    st.success("✅ AI Ready!")
                else:
                    st.error("❌ Invalid key")
            if st.session_state.gemini_configured:
                st.success("🟢 AI Connected")

        # ── Accessibility ────────────────────────────────────
        st.markdown("### ♿ Accessibility")
        st.session_state.dyslexia_mode  = st.toggle("🔤 Dyslexia Font",   st.session_state.dyslexia_mode)
        st.session_state.high_contrast  = st.toggle("🌓 High Contrast",   st.session_state.high_contrast)
        st.session_state.font_size = st.select_slider(
            "🔠 Font Size", ["Small", "Medium", "Large", "Extra Large"],
            value=st.session_state.font_size)

        # ── Language ─────────────────────────────────────────
        st.markdown("### 🌐 Language")
        st.session_state.lang = st.selectbox("UI Language", LANG_NAMES,
            index=LANG_NAMES.index(st.session_state.lang))

        # ── Navigation ───────────────────────────────────────
        st.markdown("### 📚 Navigation")
        pages = [
            "🏠 Home", "🤖 AI Chatbot", "📝 AI Summarizer",
            "❓ AI Quiz", "📊 Analytics", "🏆 Leaderboard",
            "📈 Progress", "🌍 Translate", "🎤 Voice Tools",
            "📄 PDF Export", "👤 Profile",
        ]
        if not st.session_state.logged_in:
            pages = ["🏠 Home", "🔐 Login / Register"]
        for p in pages:
            if st.button(p, use_container_width=True):
                st.session_state.page = p
                st.rerun()

        # ── User Info ─────────────────────────────────────────
        if st.session_state.logged_in:
            st.markdown("---")
            st.markdown(f"👋 **{st.session_state.username}**")
            u = st.session_state.users.get(st.session_state.username, {})
            st.markdown(f"⭐ XP: **{u.get('xp', 0)}** | 🏅 Badges: **{len(u.get('badges', []))}**")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username  = ""
                st.session_state.page = "🏠 Home"
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  PAGES
# ══════════════════════════════════════════════════════════════

# ── HOME ─────────────────────────────────────────────────────
def page_home():
    st.markdown('<h1 class="hero-title">🎓 EduAccess AI</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center;font-size:1.1em;opacity:0.8;">{t("AI-powered accessibility platform for every learner")}</p>', unsafe_allow_html=True)

    cols = st.columns(4)
    features = [
        ("🤖", "AI Chatbot", "Ask anything, get smart answers"),
        ("📝", "AI Summarizer", "Summarize long texts instantly"),
        ("❓", "AI Quiz", "Auto-generate quizzes from content"),
        ("🌍", "28 Languages", "Learn in your native language"),
        ("🔤", "Dyslexia Mode", "Special fonts & high contrast"),
        ("🎤", "Voice Playback", "Listen to any content"),
        ("🏆", "Leaderboard", "Compete and earn badges"),
        ("📜", "Certificates", "Earn PDF certificates on quiz"),
    ]
    for i, (icon, name, desc) in enumerate(features):
        with cols[i % 4]:
            st.markdown(f"""
            <div class="edu-card" style="text-align:center;">
                <div style="font-size:2em;">{icon}</div>
                <div style="font-weight:bold;margin:6px 0;">{t(name)}</div>
                <div style="font-size:0.85em;opacity:0.7;">{t(desc)}</div>
            </div>""", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info(f"👆 {t('Please login or register to access all features.')}")
        if st.button(t("🔐 Login / Register"), use_container_width=True):
            st.session_state.page = "🔐 Login / Register"
            st.rerun()

# ── LOGIN / REGISTER ─────────────────────────────────────────
def page_auth():
    st.markdown(f"## 🔐 {t('Login / Register')}")
    tab1, tab2 = st.tabs([t("Login"), t("Register")])

    with tab1:
        with st.form("login_form"):
            un = st.text_input(t("Username"))
            pw = st.text_input(t("Password"), type="password")
            if st.form_submit_button(t("Login")):
                ok, msg = login_user(un, pw)
                if ok:
                    st.success(t(msg))
                    st.session_state.page = "🏠 Home"
                    st.rerun()
                else:
                    st.error(t(msg))
        st.info(t("Demo: username=demo, password=demo123"))
        if "demo" not in st.session_state.users:
            register_user("demo", "demo123", "student")

    with tab2:
        with st.form("reg_form"):
            new_un = st.text_input(t("Choose Username"))
            new_pw = st.text_input(t("Choose Password"), type="password")
            role   = st.selectbox(t("Role"), ["student", "teacher"])
            if st.form_submit_button(t("Register")):
                ok, msg = register_user(new_un, new_pw, role)
                if ok:
                    st.success(t(msg))
                else:
                    st.error(t(msg))

# ── AI CHATBOT ───────────────────────────────────────────────
def page_chatbot():
    st.markdown(f"## 🤖 {t('AI Chatbot')}")
    lang_code = LANGUAGES.get(st.session_state.lang, "en")

    # Preset topics for kids/learners
    presets = [
        "Explain photosynthesis simply",
        "Tell me about the solar system",
        "What is machine learning?",
        "Explain water cycle like I'm 10",
        "Help me understand fractions",
    ]
    st.markdown(f"**{t('Quick Topics:')}**")
    cols = st.columns(len(presets))
    for i, p in enumerate(presets):
        with cols[i]:
            if st.button(p, key=f"preset_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": p})
                sys = f"You are a friendly, patient teacher. Answer in {st.session_state.lang}. Use simple language suitable for students with learning difficulties. Use emojis and bullet points."
                reply = gemini_chat(p, system=sys)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history[-20:]:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
                if GTTS_OK:
                    if st.button("🔊", key=f"tts_{hash(msg['content'])}"):
                        text_to_speech(msg["content"][:500], lang_code)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area(t("Ask me anything..."), height=80)
        col1, col2 = st.columns([4, 1])
        with col1:
            send = st.form_submit_button(t("Send 💬"), use_container_width=True)
        with col2:
            clear = st.form_submit_button(t("Clear"), use_container_width=True)

    if send and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        sys = f"You are a helpful, friendly teacher. Respond in {st.session_state.lang}. Use simple, accessible language with emojis. Be encouraging."
        reply = gemini_chat(user_input, system=sys)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        if st.session_state.logged_in:
            u = st.session_state.users[st.session_state.username]
            u["xp"] = u.get("xp", 0) + 2
        st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()

# ── AI SUMMARIZER ────────────────────────────────────────────
def page_summarizer():
    st.markdown(f"## 📝 {t('AI Summarizer')}")
    src = st.radio(t("Input Source"), [t("Paste Text"), t("Upload PDF"), t("Enter URL")])
    text = ""

    if src == t("Paste Text"):
        text = st.text_area(t("Paste your text here"), height=200)

    elif src == t("Upload PDF"):
        pdf = st.file_uploader(t("Upload PDF"), type=["pdf"])
        if pdf:
            with st.spinner(t("Extracting text...")):
                text = extract_pdf_text(pdf)
            st.success(f"✅ {t('Extracted')} {len(text.split())} {t('words')}")
            with st.expander(t("View Extracted Text")):
                st.text_area("", text, height=200)

    elif src == t("Enter URL"):
        url = st.text_input(t("Enter webpage URL"))
        if url and st.button(t("Fetch Content")):
            try:
                import urllib.request
                with urllib.request.urlopen(url, timeout=8) as r:
                    html = r.read().decode("utf-8", errors="ignore")
                text = re.sub(r"<[^>]+>", " ", html)
                text = re.sub(r"\s+", " ", text).strip()[:5000]
                st.success(t("Content fetched!"))
            except Exception as e:
                st.error(f"URL Error: {e}")

    if text:
        col1, col2 = st.columns(2)
        with col1:
            sum_lang = st.selectbox(t("Summarize in"), LANG_NAMES)
        with col2:
            detail = st.select_slider(t("Detail Level"), ["Brief", "Standard", "Detailed"])

        if st.button(t("✨ Summarize with AI"), use_container_width=True):
            with st.spinner(t("AI is thinking...")):
                summary = ai_summarize(text, sum_lang)
            st.markdown(f"### 📋 {t('Summary')}")
            st.markdown(f'<div class="edu-card">{summary}</div>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                if GTTS_OK and st.button(t("🔊 Listen to Summary")):
                    text_to_speech(summary, LANGUAGES.get(sum_lang, "en"))
            with col2:
                st.download_button(t("💾 Download Summary"), summary,
                                   file_name="summary.txt", mime="text/plain")

            if st.session_state.logged_in:
                u = st.session_state.users[st.session_state.username]
                u["xp"] = u.get("xp", 0) + 5
                p = st.session_state.progress.get(st.session_state.username, [])
                p.append({"type": "summary", "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "lang": sum_lang})
                st.session_state.progress[st.session_state.username] = p

# ── AI QUIZ ──────────────────────────────────────────────────
def page_quiz():
    st.markdown(f"## ❓ {t('AI Quiz Generator')}")

    if not st.session_state.quiz_submitted:
        # Quiz setup
        if not st.session_state.current_quiz:
            st.markdown(f"### {t('Set Up Your Quiz')}")
            topic_text = st.text_area(t("Paste study material or topic"), height=150,
                placeholder=t("e.g. Paste any chapter, article, or notes here..."))
            col1, col2, col3 = st.columns(3)
            with col1:
                num_q = st.number_input(t("Number of Questions"), 3, 15, 5)
            with col2:
                diff = st.selectbox(t("Difficulty"), ["Easy", "Medium", "Hard"])
            with col3:
                quiz_lang = st.selectbox(t("Quiz Language"), LANG_NAMES)

            if st.button(t("🎲 Generate Quiz"), use_container_width=True):
                if not topic_text:
                    st.warning(t("Please enter some study material first."))
                else:
                    with st.spinner(t("Generating quiz with AI...")):
                        qs = generate_quiz(topic_text, num_q, diff)
                        if quiz_lang != "English" and TRANS_OK:
                            code = LANGUAGES.get(quiz_lang, "en")
                            for q in qs:
                                q["question"] = translate_text(q["question"], code)
                                q["options"]  = [translate_text(o, code) for o in q["options"]]
                                q["explanation"] = translate_text(q.get("explanation",""), code)
                        st.session_state.current_quiz   = qs
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                        st.rerun()
        else:
            # Show questions
            st.markdown(f"### {t('Answer the Questions')}")
            qs = st.session_state.current_quiz
            with st.form("quiz_form"):
                for i, q in enumerate(qs):
                    st.markdown(f'<div class="edu-card"><b>Q{i+1}. {q["question"]}</b></div>', unsafe_allow_html=True)
                    ans = st.radio("", q["options"], key=f"q_{i}", label_visibility="collapsed")
                    st.session_state.quiz_answers[i] = ans
                    st.markdown("")

                submitted = st.form_submit_button(t("✅ Submit Quiz"), use_container_width=True)

            if submitted:
                st.session_state.quiz_submitted = True
                st.rerun()

            if st.button(t("🔄 New Quiz")):
                st.session_state.current_quiz = []
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()

    else:
        # Results
        qs      = st.session_state.current_quiz
        answers = st.session_state.quiz_answers
        correct = sum(1 for i, q in enumerate(qs) if answers.get(i) == q["answer"])
        total   = len(qs)
        score   = int((correct / total) * 100) if total else 0

        # Animated score
        color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 40 else "#ef4444"
        st.markdown(f"""
        <div style="text-align:center;padding:30px;">
            <div style="font-size:5em;font-weight:900;color:{color};">{score}%</div>
            <div style="font-size:1.5em;">{correct}/{total} {t('Correct')}</div>
            <div style="font-size:1.2em;margin-top:8px;">
                {'🏆 Excellent!' if score>=80 else '👍 Good Job!' if score>=60 else '📚 Keep Practicing!'}
            </div>
        </div>""", unsafe_allow_html=True)

        # Review answers
        with st.expander(t("📖 Review Answers")):
            for i, q in enumerate(qs):
                user_ans = answers.get(i, "")
                is_correct = user_ans == q["answer"]
                icon = "✅" if is_correct else "❌"
                st.markdown(f"**{icon} Q{i+1}. {q['question']}**")
                st.markdown(f"Your answer: `{user_ans}` | Correct: `{q['answer']}`")
                if q.get("explanation"):
                    st.info(f"💡 {q['explanation']}")
                st.markdown("---")

        # Save score + XP
        if st.session_state.logged_in:
            un = st.session_state.username
            u  = st.session_state.users[un]
            u["xp"] = u.get("xp", 0) + score // 5
            u["completed_quizzes"] = u.get("completed_quizzes", 0) + 1
            if score >= 80 and "🏆 Quiz Master" not in u.get("badges", []):
                u.setdefault("badges", []).append("🏆 Quiz Master")
            st.session_state.quiz_scores.append({
                "user": un, "score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "questions": total,
            })
            # Update leaderboard
            lb = st.session_state.leaderboard
            entry = next((x for x in lb if x["user"] == un), None)
            if entry:
                entry["best"] = max(entry["best"], score)
                entry["attempts"] += 1
            else:
                lb.append({"user": un, "best": score, "attempts": 1, "xp": u["xp"]})

        # Certificate
        if score >= 60:
            st.success(t("🎉 Congratulations! You earned a certificate!"))
            cert_bytes = generate_certificate(
                st.session_state.username or "Learner",
                "AI Quiz", score,
                datetime.now().strftime("%B %d, %Y")
            )
            if cert_bytes:
                st.download_button(t("📜 Download Certificate (PDF)"), cert_bytes,
                    file_name="certificate.pdf", mime="application/pdf",
                    use_container_width=True)
            else:
                # HTML fallback certificate
                st.markdown(f"""
                <div class="cert-box">
                    <h2 style="color:#FFD700;">🎓 CERTIFICATE OF ACHIEVEMENT</h2>
                    <p>This certifies that</p>
                    <h3 style="color:#FFD700;">{st.session_state.username or 'Learner'}</h3>
                    <p>completed the AI Quiz with a score of</p>
                    <h2 style="color:#FFD700;">{score}%</h2>
                    <p style="font-size:0.9em;">EduAccess AI · {datetime.now().strftime("%B %d, %Y")}</p>
                </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(t("🔄 New Quiz"), use_container_width=True):
                st.session_state.current_quiz   = []
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.rerun()
        with col2:
            if st.button(t("📊 View Analytics"), use_container_width=True):
                st.session_state.page = "📊 Analytics"
                st.rerun()

# ── ANALYTICS DASHBOARD ──────────────────────────────────────
def page_analytics():
    st.markdown(f"## 📊 {t('Quiz Analytics Dashboard')}")
    scores = st.session_state.quiz_scores

    if not scores:
        st.info(t("No quiz attempts yet. Take a quiz to see analytics!"))
        return

    df = pd.DataFrame(scores)

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div style="font-size:2em;">📝</div><div style="font-size:1.4em;font-weight:bold;">{len(df)}</div><div>{t("Total Quizzes")}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div style="font-size:2em;">🎯</div><div style="font-size:1.4em;font-weight:bold;">{df["score"].mean():.1f}%</div><div>{t("Avg Score")}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div style="font-size:2em;">🏆</div><div style="font-size:1.4em;font-weight:bold;">{df["score"].max()}%</div><div>{t("Best Score")}</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div style="font-size:2em;">📈</div><div style="font-size:1.4em;font-weight:bold;">{df["score"].iloc[-1]}%</div><div>{t("Last Score")}</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=df["score"], mode="lines+markers",
            line=dict(color="#6C63FF", width=3),
            marker=dict(size=8, color="#FF6B9D"),
            name=t("Score")))
        fig.add_hline(y=df["score"].mean(), line_dash="dash",
                      line_color="#FFD700", annotation_text=t("Average"))
        fig.update_layout(title=t("Score Trend"), paper_bgcolor="rgba(0,0,0,0)",
                          plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                          xaxis_title=t("Attempt"), yaxis_title=t("Score (%)"),
                          yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        buckets = {"Excellent (80-100)": 0, "Good (60-79)": 0,
                   "Average (40-59)": 0, "Needs Work (<40)": 0}
        for s in df["score"]:
            if s >= 80: buckets["Excellent (80-100)"] += 1
            elif s >= 60: buckets["Good (60-79)"] += 1
            elif s >= 40: buckets["Average (40-59)"] += 1
            else: buckets["Needs Work (<40)"] += 1
        fig2 = go.Figure(go.Pie(
            labels=list(buckets.keys()), values=list(buckets.values()),
            hole=0.4, marker_colors=["#22c55e","#6C63FF","#f59e0b","#ef4444"]))
        fig2.update_layout(title=t("Performance Distribution"),
                           paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander(t("📋 Detailed History")):
        st.dataframe(df.rename(columns={"score": "Score (%)", "date": "Date",
                                         "questions": "Questions", "user": "User"}),
                     use_container_width=True)

# ── LEADERBOARD ──────────────────────────────────────────────
def page_leaderboard():
    st.markdown(f"## 🏆 {t('Leaderboard')}")
    lb = sorted(st.session_state.leaderboard, key=lambda x: x["best"], reverse=True)

    if not lb:
        st.info(t("No scores yet. Be the first to take a quiz!"))
        return

    medals = ["🥇", "🥈", "🥉"]
    for i, entry in enumerate(lb[:10]):
        medal = medals[i] if i < 3 else f"#{i+1}"
        is_me = entry["user"] == st.session_state.username
        bg = "border: 2px solid #FFD700;" if is_me else ""
        st.markdown(f"""
        <div class="edu-card" style="{bg}display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:1.4em;">{medal} <b>{entry['user']}</b>{"  (You)" if is_me else ""}</span>
            <span><b style="color:#FFD700;">{entry['best']}%</b> best · {entry['attempts']} attempts</span>
        </div>""", unsafe_allow_html=True)

    # Bar chart
    fig = go.Figure(go.Bar(
        x=[e["user"] for e in lb[:10]],
        y=[e["best"] for e in lb[:10]],
        marker_color=["#FFD700" if e["user"] == st.session_state.username else "#6C63FF" for e in lb[:10]],
        text=[f"{e['best']}%" for e in lb[:10]], textposition="outside"))
    fig.update_layout(title=t("Top Players"), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                      yaxis=dict(range=[0, 105]))
    st.plotly_chart(fig, use_container_width=True)

# ── PROGRESS TRACKING ────────────────────────────────────────
def page_progress():
    st.markdown(f"## 📈 {t('Progress Tracking')}")
    if not st.session_state.logged_in:
        st.warning(t("Please login to see your progress."))
        return

    un = st.session_state.username
    u  = st.session_state.users.get(un, {})
    p  = st.session_state.progress.get(un, [])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card">⭐<br><b style="font-size:1.5em">{u.get("xp",0)}</b><br>XP Points</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card">📝<br><b style="font-size:1.5em">{u.get("completed_quizzes",0)}</b><br>{t("Quizzes Done")}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card">🎖️<br><b style="font-size:1.5em">{len(u.get("badges",[]))}</b><br>{t("Badges Earned")}</div>', unsafe_allow_html=True)

    # Badges
    if u.get("badges"):
        st.markdown(f"### 🎖️ {t('Your Badges')}")
        for b in u["badges"]:
            st.markdown(f'<span class="badge">{b}</span>', unsafe_allow_html=True)

    # XP Progress bar
    level = u.get("xp", 0) // 50 + 1
    xp_in_level = u.get("xp", 0) % 50
    st.markdown(f"### 🎮 {t('Level')} {level}")
    st.progress(xp_in_level / 50, text=f"{xp_in_level}/50 XP to next level")

    # Activity timeline
    if p:
        st.markdown(f"### 📅 {t('Recent Activity')}")
        for item in reversed(p[-10:]):
            icon = "📝" if item.get("type") == "summary" else "❓"
            st.markdown(f'<div class="edu-card" style="padding:10px;">{icon} {item.get("type","activity").title()} · {item.get("date","")} · {item.get("lang","")}</div>', unsafe_allow_html=True)

# ── TRANSLATION ──────────────────────────────────────────────
def page_translate():
    st.markdown(f"## 🌍 {t('Translation Tool')}")
    st.caption(t("Supports 28 languages including all major Indian languages"))

    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox(t("From"), LANG_NAMES, key="trans_from")
    with col2:
        tgt_lang = st.selectbox(t("To"), LANG_NAMES, index=2, key="trans_to")

    input_text = st.text_area(t("Enter text to translate"), height=150)

    if st.button(t("🌐 Translate"), use_container_width=True):
        if input_text:
            if TRANS_OK:
                with st.spinner(t("Translating...")):
                    src_code = LANGUAGES.get(src_lang, "en")
                    tgt_code = LANGUAGES.get(tgt_lang, "en")
                    try:
                        result = GoogleTranslator(source=src_code, target=tgt_code).translate(input_text)
                        st.markdown(f"### {t('Translation')}")
                        st.markdown(f'<div class="edu-card" style="font-size:1.1em;">{result}</div>', unsafe_allow_html=True)
                        if GTTS_OK:
                            if st.button(t("🔊 Listen")):
                                text_to_speech(result, tgt_code)
                        st.download_button(t("💾 Download"), result, file_name="translation.txt")
                    except Exception as e:
                        # Fallback to Gemini
                        prompt = f"Translate this text from {src_lang} to {tgt_lang}. Return only the translation:\n\n{input_text}"
                        result = gemini_chat(prompt)
                        st.markdown(f'<div class="edu-card">{result}</div>', unsafe_allow_html=True)
            else:
                prompt = f"Translate from {src_lang} to {tgt_lang}. Return only the translation:\n\n{input_text}"
                result = gemini_chat(prompt)
                st.markdown(f'<div class="edu-card">{result}</div>', unsafe_allow_html=True)
        else:
            st.warning(t("Please enter text to translate."))

# ── VOICE TOOLS ──────────────────────────────────────────────
def page_voice():
    st.markdown(f"## 🎤 {t('Voice Tools')}")

    tab1, tab2 = st.tabs([t("🔊 Text to Speech"), t("📖 Read Aloud")])

    with tab1:
        st.markdown(f"#### {t('Convert any text to speech in 28 languages')}")
        voice_text = st.text_area(t("Enter text"), height=150,
            placeholder=t("Type or paste any text here..."))
        v_lang = st.selectbox(t("Speak in"), LANG_NAMES)
        speed = st.select_slider(t("Speed"), ["Slow", "Normal"], value="Normal")

        if st.button(t("🔊 Generate Speech"), use_container_width=True):
            if voice_text and GTTS_OK:
                with st.spinner(t("Generating audio...")):
                    code = LANGUAGES.get(v_lang, "en")
                    buf = io.BytesIO()
                    tts = gTTS(text=voice_text[:3000], lang=code, slow=(speed=="Slow"))
                    tts.write_to_fp(buf)
                    buf.seek(0)
                    st.audio(buf, format="audio/mp3")
                    st.success(t("✅ Audio generated!"))
                    st.download_button(t("💾 Download MP3"), buf.getvalue(),
                                       file_name="speech.mp3", mime="audio/mp3")
            elif not GTTS_OK:
                st.error(t("gTTS library not installed."))

    with tab2:
        st.markdown(f"#### {t('Dyslexia-friendly read-aloud mode')}")
        st.info(t("Paste any study material and listen to it being read aloud — great for dyslexic learners!"))
        read_text = st.text_area(t("Study material"), height=200)
        chunk_size = st.slider(t("Words per chunk"), 50, 500, 150)

        if read_text and st.button(t("▶️ Read Aloud"), use_container_width=True):
            words = read_text.split()
            chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
            for i, chunk in enumerate(chunks[:5]):  # limit to 5 chunks
                st.markdown(f'<div class="edu-card" style="line-height:2;">{chunk}</div>', unsafe_allow_html=True)
                if GTTS_OK:
                    buf = io.BytesIO()
                    tts = gTTS(text=chunk, lang=LANGUAGES.get(st.session_state.lang,"en"), slow=True)
                    tts.write_to_fp(buf)
                    buf.seek(0)
                    st.audio(buf, format="audio/mp3")

# ── PDF EXPORT ───────────────────────────────────────────────
def page_pdf_export():
    st.markdown(f"## 📄 {t('PDF Export')}")
    st.markdown(t("Generate professional PDF reports from your content"))

    doc_title = st.text_input(t("Document Title"), value="EduAccess AI Report")
    content   = st.text_area(t("Content to export"), height=200,
                              placeholder=t("Paste summary, notes, quiz results..."))
    include_header = st.checkbox(t("Include header with date"), value=True)

    if st.button(t("📄 Generate PDF"), use_container_width=True):
        if content:
            if REPORTLAB_OK:
                buf = io.BytesIO()
                doc = SimpleDocTemplate(buf, pagesize=A4)
                styles = getSampleStyleSheet()
                elements = []
                title_style = ParagraphStyle("t", fontSize=20, textColor=colors.HexColor("#6C63FF"),
                                              spaceAfter=12, fontName="Helvetica-Bold")
                body_style  = ParagraphStyle("b", fontSize=12, spaceAfter=8, leading=18)
                if include_header:
                    elements.append(Paragraph(f"EduAccess AI · {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]))
                    elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph(doc_title, title_style))
                elements.append(Spacer(1, 0.1*inch))
                for line in content.split("\n"):
                    if line.strip():
                        elements.append(Paragraph(line, body_style))
                doc.build(elements)
                st.success(t("✅ PDF generated!"))
                st.download_button(t("💾 Download PDF"), buf.getvalue(),
                    file_name=f"{doc_title.replace(' ','_')}.pdf", mime="application/pdf",
                    use_container_width=True)
            else:
                # Plain text fallback
                output = f"EduAccess AI Report\n{'='*40}\n{doc_title}\n{datetime.now()}\n\n{content}"
                st.download_button(t("💾 Download TXT"), output,
                    file_name=f"{doc_title}.txt", mime="text/plain",
                    use_container_width=True)
                st.warning(t("Install reportlab for PDF export: pip install reportlab"))
        else:
            st.warning(t("Please enter content to export."))

# ── PROFILE ──────────────────────────────────────────────────
def page_profile():
    st.markdown(f"## 👤 {t('My Profile')}")
    if not st.session_state.logged_in:
        st.warning(t("Please login to view your profile."))
        return

    un = st.session_state.username
    u  = st.session_state.users.get(un, {})

    col1, col2 = st.columns([1, 2])
    with col1:
        avatar = hashlib.md5(un.encode()).hexdigest()[:6]
        st.markdown(f"""
        <div class="edu-card" style="text-align:center;">
            <div style="font-size:4em;">👤</div>
            <h2>{un}</h2>
            <span class="badge">{u.get('role','student').title()}</span>
            <p style="opacity:0.7;">Joined: {u.get('joined','')}</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"### {t('Stats')}")
        st.metric(t("XP Points"), u.get("xp", 0))
        st.metric(t("Quizzes Completed"), u.get("completed_quizzes", 0))
        st.metric(t("Badges"), len(u.get("badges", [])))

        if u.get("badges"):
            st.markdown(f"**{t('Badges')}:** " + "  ".join(u["badges"]))

    # Quiz score history chart
    my_scores = [s for s in st.session_state.quiz_scores if s.get("user") == un]
    if my_scores:
        df = pd.DataFrame(my_scores)
        fig = px.line(df, y="score", title=t("My Score History"),
                      markers=True, color_discrete_sequence=["#6C63FF"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", yaxis=dict(range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
ROUTE_MAP = {
    "🏠 Home":               page_home,
    "🔐 Login / Register":   page_auth,
    "🤖 AI Chatbot":         page_chatbot,
    "📝 AI Summarizer":      page_summarizer,
    "❓ AI Quiz":            page_quiz,
    "📊 Analytics":          page_analytics,
    "🏆 Leaderboard":        page_leaderboard,
    "📈 Progress":           page_progress,
    "🌍 Translate":          page_translate,
    "🎤 Voice Tools":        page_voice,
    "📄 PDF Export":         page_pdf_export,
    "👤 Profile":            page_profile,
}

# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
sidebar()
apply_styles()  # re-apply after sidebar changes

page_fn = ROUTE_MAP.get(st.session_state.page, page_home)

# Guard pages that require login
PROTECTED = {"🤖 AI Chatbot","📝 AI Summarizer","❓ AI Quiz",
             "📊 Analytics","📈 Progress","👤 Profile"}
if st.session_state.page in PROTECTED and not st.session_state.logged_in:
    st.warning(t("⚠️ Please login first to access this feature."))
    page_auth()
else:
    page_fn()

# ── Footer ───────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f'<div style="text-align:center;opacity:0.5;font-size:0.8em;">'
    f'🎓 EduAccess AI · Final Year Major Project · '
    f'Built with ❤️ using Streamlit + Gemini AI · '
    f'Supports 28 Languages · Dyslexia Friendly</div>',
    unsafe_allow_html=True
)
