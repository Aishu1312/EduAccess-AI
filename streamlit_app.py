import streamlit as st
import os, json, re, time, base64, hashlib, random, io
from datetime import datetime
import pandas as pd

# ── Page config MUST be first Streamlit call ────────────────
st.set_page_config(
    page_title="EduAccess AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Optional imports with graceful fallback ──────────────────
try:
    from google import genai as google_genai
    GEMINI_OK = True
except Exception:
    GEMINI_OK = False

try:
    from gtts import gTTS
    GTTS_OK = True
except Exception:
    GTTS_OK = False

try:
    import PyPDF2
    PDF_OK = True
except Exception:
    PDF_OK = False

try:
    from deep_translator import GoogleTranslator
    TRANS_OK = True
except Exception:
    TRANS_OK = False

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_OK = True
except Exception:
    PLOTLY_OK = False

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors as rl_colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_OK = True
except Exception:
    REPORTLAB_OK = False

# ══════════════════════════════════════════════════════════════
#  28 SUPPORTED LANGUAGES
# ══════════════════════════════════════════════════════════════
LANGUAGES = {
    "English": "en",        "Hindi": "hi",          "Marathi": "mr",
    "Telugu": "te",         "Tamil": "ta",           "Kannada": "kn",
    "Malayalam": "ml",      "Bengali": "bn",         "Gujarati": "gu",
    "Punjabi": "pa",        "Odia": "or",            "Urdu": "ur",
    "Spanish": "es",        "French": "fr",          "German": "de",
    "Portuguese": "pt",     "Italian": "it",         "Dutch": "nl",
    "Russian": "ru",        "Arabic": "ar",          "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN", "Korean": "ko", "Turkish": "tr",
    "Polish": "pl",         "Swedish": "sv",         "Norwegian": "no",
    "Swahili": "sw",
}
LANG_NAMES = list(LANGUAGES.keys())

# ══════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "logged_in": False, "username": "", "role": "student",
        "users": {}, "progress": {}, "quiz_scores": [],
        "chat_history": [],
        "dyslexia_mode": False, "high_contrast": False,
        "font_size": "Medium", "lang": "English",
        "leaderboard": [], "page": "🏠 Home",
        "gemini_key": "", "gemini_client": None,
        "current_quiz": [], "quiz_answers": {},
        "quiz_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ══════════════════════════════════════════════════════════════
#  GEMINI  (new google-genai SDK)
# ══════════════════════════════════════════════════════════════
def configure_gemini(api_key: str) -> bool:
    if not (GEMINI_OK and api_key and api_key.strip()):
        return False
    try:
        client = google_genai.Client(api_key=api_key.strip())
        st.session_state.gemini_client = client
        st.session_state.gemini_key    = api_key.strip()
        return True
    except Exception:
        return False

def gemini_chat(prompt: str, system: str = "") -> str:
    client = st.session_state.get("gemini_client")
    if not client:
        return "⚠️ Gemini API not configured. Please add your API key in the sidebar."
    try:
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=full_prompt,
        )
        return response.text or "No response generated."
    except Exception as e:
        err = str(e)
        if "API_KEY" in err.upper() or "INVALID" in err.upper():
            return "❌ Invalid API key. Please check your Gemini API key in the sidebar."
        if "QUOTA" in err.upper():
            return "⏳ API quota exceeded. Please wait a moment and try again."
        return f"❌ AI Error: {err[:200]}"

# ══════════════════════════════════════════════════════════════
#  TRANSLATION
# ══════════════════════════════════════════════════════════════
def translate_text(text: str, target: str) -> str:
    if target == "en" or not text.strip():
        return text
    if TRANS_OK:
        try:
            return GoogleTranslator(source="auto", target=target).translate(text[:4999])
        except Exception:
            pass
    return text

def t(text: str) -> str:
    code = LANGUAGES.get(st.session_state.lang, "en")
    if code == "en":
        return text
    return translate_text(text, code)

# ══════════════════════════════════════════════════════════════
#  STYLING
# ══════════════════════════════════════════════════════════════
FONT_SIZES = {"Small": "14px", "Medium": "17px", "Large": "21px", "Extra Large": "26px"}

def apply_styles():
    fs = FONT_SIZES.get(st.session_state.font_size, "17px")
    dyslexia_font = (
        "OpenDyslexic, 'Comic Sans MS', Arial, sans-serif"
        if st.session_state.dyslexia_mode
        else "'Segoe UI', Arial, sans-serif"
    )
    bg       = "#000000" if st.session_state.high_contrast else "#0f1117"
    txt      = "#ffffff"
    card_bg  = "#1a1a1a" if st.session_state.high_contrast else "#1e2130"
    accent   = "#FFD700" if st.session_state.high_contrast else "#6C63FF"

    st.markdown(f"""
    <style>
    html, body, [class*="css"] {{
        font-family: {dyslexia_font} !important;
        font-size: {fs} !important;
    }}
    .stApp {{ background-color: {bg}; color: {txt}; }}
    .edu-card {{
        background: {card_bg};
        border-radius: 14px;
        padding: 18px;
        margin: 8px 0;
        border-left: 4px solid {accent};
    }}
    .hero-title {{
        font-size: 2.6em; font-weight: 900; text-align: center;
        background: linear-gradient(135deg, {accent}, #FF6B9D);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }}
    .badge {{
        display: inline-block; padding: 3px 10px; border-radius: 20px;
        font-size: 0.78em; font-weight: bold;
        background: {accent}33; color: {accent}; margin: 2px;
    }}
    .chat-user {{
        background: #2d2d4e; border-radius: 12px;
        padding: 10px 14px; margin: 6px 0; text-align: right;
    }}
    .chat-bot {{
        background: #1e3a5f; border-radius: 12px;
        padding: 10px 14px; margin: 6px 0;
    }}
    .cert-box {{
        border: 6px double {accent}; border-radius: 20px;
        padding: 40px; text-align: center; margin: 20px 0;
        background: linear-gradient(135deg, #1a1a2e, #16213e);
    }}
    .metric-card {{
        background: {card_bg}; border-radius: 12px;
        padding: 18px; text-align: center;
        border: 1px solid {accent}44;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {accent}, #FF6B9D) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 700 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_styles()

# ══════════════════════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════════════════════
def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username, password, role="student"):
    if not username or not password:
        return False, "Username and password required."
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
        st.session_state.logged_in  = True
        st.session_state.username   = username
        st.session_state.role       = u["role"]
        return True, "Login successful!"
    return False, "Invalid username or password."

# Ensure demo account always exists
if "demo" not in st.session_state.users:
    register_user("demo", "demo123", "student")

# ══════════════════════════════════════════════════════════════
#  TEXT-TO-SPEECH
# ══════════════════════════════════════════════════════════════
def tts_audio(text: str, lang_code: str = "en"):
    if not GTTS_OK:
        st.warning("gTTS not available.")
        return
    try:
        buf = io.BytesIO()
        gTTS(text=text[:3000], lang=lang_code, slow=False).write_to_fp(buf)
        buf.seek(0)
        st.audio(buf, format="audio/mp3")
    except Exception as e:
        st.error(f"TTS error: {e}")

# ══════════════════════════════════════════════════════════════
#  PDF TEXT EXTRACTION
# ══════════════════════════════════════════════════════════════
def extract_pdf_text(uploaded_file) -> str:
    if not PDF_OK:
        return "PyPDF2 not installed."
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception as e:
        return f"PDF read error: {e}"

# ══════════════════════════════════════════════════════════════
#  AI HELPERS
# ══════════════════════════════════════════════════════════════
def ai_summarize(text: str, lang: str = "English") -> str:
    return gemini_chat(
        f"Summarize in {lang} using simple words, short sentences, and bullet points.\n\nTEXT:\n{text[:4000]}",
        system="You are a friendly teacher helping students with learning difficulties."
    )

def generate_quiz(text: str, num_q: int = 5, difficulty: str = "Medium") -> list:
    raw = gemini_chat(
        f"Create {num_q} MCQs (difficulty={difficulty}) from this text.\n"
        f"Return ONLY a valid JSON array like: "
        f'[{{"question":"...","options":["A","B","C","D"],"answer":"A","explanation":"..."}}]\n\n'
        f"TEXT: {text[:3000]}"
    )
    try:
        cleaned = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(cleaned)
        if isinstance(data, list) and data:
            return data
    except Exception:
        pass
    return [{
        "question": "What is the main idea of the text you provided?",
        "options": ["To inform", "To entertain", "To persuade", "To describe"],
        "answer": "To inform",
        "explanation": "Most educational texts aim to inform the reader.",
    }]

# ══════════════════════════════════════════════════════════════
#  CERTIFICATE
# ══════════════════════════════════════════════════════════════
def make_certificate(name: str, score: int, date: str) -> bytes:
    if not REPORTLAB_OK:
        return b""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=60, bottomMargin=60)
    styles = getSampleStyleSheet()
    gold   = rl_colors.HexColor("#FFD700")
    elems  = []
    T = lambda s, **kw: ParagraphStyle(s, **kw)
    title_s = T("ti", fontSize=28, textColor=gold,    alignment=1, spaceAfter=16, fontName="Helvetica-Bold")
    sub_s   = T("su", fontSize=18, textColor=rl_colors.white, alignment=1, spaceAfter=12)
    body_s  = T("bo", fontSize=13, textColor=rl_colors.lightgrey, alignment=1, spaceAfter=8)
    elems += [
        Spacer(1, 0.4*inch),
        Paragraph("🎓 CERTIFICATE OF ACHIEVEMENT", title_s),
        Spacer(1, 0.2*inch),
        Paragraph("This certifies that", body_s),
        Paragraph(f"<b>{name}</b>", sub_s),
        Paragraph("has successfully completed the EduAccess AI Quiz", body_s),
        Paragraph(f"with a score of <b>{score}%</b>", sub_s),
        Spacer(1, 0.2*inch),
        Paragraph(f"Date: {date}", body_s),
        Spacer(1, 0.3*inch),
        Paragraph("EduAccess AI · Empowering Every Learner", body_s),
    ]
    doc.build(elems)
    return buf.getvalue()

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown('<div style="text-align:center;font-size:1.8em;font-weight:900;">🎓 EduAccess AI</div>', unsafe_allow_html=True)
        st.caption("Final Year Major Project")
        st.markdown("---")

        # API Key
        with st.expander("🔑 Gemini API Key", expanded=not bool(st.session_state.gemini_client)):
            key_input = st.text_input("Paste your API key", type="password",
                                      value=st.session_state.gemini_key,
                                      help="Free key at aistudio.google.com")
            if st.button("✅ Activate AI", use_container_width=True):
                if configure_gemini(key_input):
                    st.success("🟢 AI Ready!")
                    st.rerun()
                else:
                    st.error("❌ Invalid key or google-genai not installed.")
            if st.session_state.gemini_client:
                st.success("🟢 Gemini Connected")

        # Accessibility
        st.markdown("### ♿ Accessibility")
        st.session_state.dyslexia_mode = st.toggle("🔤 Dyslexia Font",  st.session_state.dyslexia_mode)
        st.session_state.high_contrast = st.toggle("🌓 High Contrast",  st.session_state.high_contrast)
        st.session_state.font_size = st.select_slider(
            "🔠 Font Size", ["Small","Medium","Large","Extra Large"],
            value=st.session_state.font_size)

        # Language
        st.markdown("### 🌐 Language (28)")
        st.session_state.lang = st.selectbox(
            "Select Language", LANG_NAMES,
            index=LANG_NAMES.index(st.session_state.lang))

        # Navigation
        st.markdown("### 📚 Menu")
        all_pages = [
            "🏠 Home", "🔐 Login",
            "🤖 AI Chatbot", "📝 Summarizer",
            "❓ AI Quiz", "📊 Analytics",
            "🏆 Leaderboard", "📈 Progress",
            "🌍 Translate", "🎤 Voice Tools",
            "📄 PDF Export", "👤 Profile",
        ]
        for pg in all_pages:
            if st.button(pg, key=f"nav_{pg}", use_container_width=True):
                st.session_state.page = pg
                st.rerun()

        # User strip
        if st.session_state.logged_in:
            st.markdown("---")
            u = st.session_state.users.get(st.session_state.username, {})
            st.markdown(f"👋 **{st.session_state.username}** · ⭐ {u.get('xp',0)} XP")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username  = ""
                st.session_state.page      = "🏠 Home"
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  PAGE: HOME
# ══════════════════════════════════════════════════════════════
def page_home():
    st.markdown('<h1 class="hero-title">🎓 EduAccess AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;opacity:.8;">AI-powered accessibility platform for every learner · 28 languages · Dyslexia-friendly</p>', unsafe_allow_html=True)
    st.markdown("")

    cards = [
        ("🤖","AI Chatbot","Ask anything in your language"),
        ("📝","AI Summarizer","Summarize PDFs & text with AI"),
        ("❓","AI Quiz","Auto-generate quizzes from content"),
        ("🌍","28 Languages","All major Indian + world languages"),
        ("🔤","Dyslexia Mode","Special fonts & high contrast"),
        ("🎤","Voice Playback","Listen to any content aloud"),
        ("🏆","Leaderboard","Compete and earn XP badges"),
        ("📜","Certificates","PDF certificates on quiz completion"),
    ]
    cols = st.columns(4)
    for i,(icon,name,desc) in enumerate(cards):
        with cols[i%4]:
            st.markdown(f"""
            <div class="edu-card" style="text-align:center;min-height:120px;">
                <div style="font-size:2em;">{icon}</div>
                <div style="font-weight:bold;margin:4px 0;">{name}</div>
                <div style="font-size:.82em;opacity:.7;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if not st.session_state.logged_in:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔐 Login / Register", use_container_width=True):
                st.session_state.page = "🔐 Login"
                st.rerun()
        with c2:
            if st.button("👀 Try Demo (no login)", use_container_width=True):
                login_user("demo","demo123")
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  PAGE: AUTH
# ══════════════════════════════════════════════════════════════
def page_auth():
    st.markdown("## 🔐 Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form", clear_on_submit=False):
            un = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                ok, msg = login_user(un, pw)
                if ok:
                    st.success(msg)
                    st.session_state.page = "🏠 Home"
                    st.rerun()
                else:
                    st.error(msg)
        st.info("🎯 Demo account — username: `demo`  password: `demo123`")

    with tab2:
        with st.form("reg_form", clear_on_submit=True):
            nu = st.text_input("Choose Username")
            np = st.text_input("Choose Password", type="password")
            ro = st.selectbox("Role", ["student","teacher"])
            if st.form_submit_button("Register", use_container_width=True):
                ok, msg = register_user(nu, np, ro)
                if ok:
                    st.success(msg + " You can now login.")
                else:
                    st.error(msg)

# ══════════════════════════════════════════════════════════════
#  PAGE: CHATBOT
# ══════════════════════════════════════════════════════════════
def page_chatbot():
    st.markdown("## 🤖 AI Chatbot")
    lang_code = LANGUAGES.get(st.session_state.lang, "en")

    # Quick topic chips
    topics = ["Explain photosynthesis simply","What is the solar system?",
               "Help me with fractions","Explain the water cycle","What is AI?"]
    cols = st.columns(len(topics))
    for i, tp in enumerate(topics):
        with cols[i]:
            if st.button(tp, key=f"chip_{i}"):
                st.session_state.chat_history.append({"role":"user","content":tp})
                sys = f"You are a friendly, patient teacher. Answer in {st.session_state.lang}. Use simple words, emojis, and bullet points. Be encouraging."
                reply = gemini_chat(tp, system=sys)
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                if st.session_state.logged_in:
                    st.session_state.users[st.session_state.username]["xp"] = \
                        st.session_state.users[st.session_state.username].get("xp",0) + 2
                st.rerun()

    st.markdown("---")

    # Chat history
    for msg in st.session_state.chat_history[-30:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bot">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
            if GTTS_OK:
                btn_key = f"tts_{abs(hash(msg['content']))%999999}"
                if st.button("🔊 Listen", key=btn_key):
                    tts_audio(msg["content"][:600], lang_code)

    # Input row
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_area("Ask anything...", height=80, label_visibility="collapsed",
                                   placeholder="Type your question here...")
        c1, c2 = st.columns([5,1])
        with c1: send  = st.form_submit_button("Send 💬", use_container_width=True)
        with c2: clear = st.form_submit_button("🗑️",      use_container_width=True)

    if send and user_input.strip():
        st.session_state.chat_history.append({"role":"user","content":user_input.strip()})
        sys = f"You are a helpful, encouraging teacher. Respond in {st.session_state.lang}. Use simple, accessible language with emojis."
        reply = gemini_chat(user_input.strip(), system=sys)
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        if st.session_state.logged_in:
            st.session_state.users[st.session_state.username]["xp"] = \
                st.session_state.users[st.session_state.username].get("xp",0) + 2
        st.rerun()
    if clear:
        st.session_state.chat_history = []
        st.rerun()

# ══════════════════════════════════════════════════════════════
#  PAGE: SUMMARIZER
# ══════════════════════════════════════════════════════════════
def page_summarizer():
    st.markdown("## 📝 AI Summarizer")
    src = st.radio("Input source", ["Paste Text","Upload PDF"], horizontal=True)
    text = ""

    if src == "Paste Text":
        text = st.text_area("Paste your text here", height=220)
    else:
        pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if pdf:
            with st.spinner("Extracting text from PDF..."):
                text = extract_pdf_text(pdf)
            st.success(f"✅ Extracted {len(text.split())} words")
            with st.expander("Preview extracted text"):
                st.text_area("", text[:2000], height=150, disabled=True)

    if text.strip():
        c1, c2 = st.columns(2)
        with c1: sum_lang = st.selectbox("Summarize in language", LANG_NAMES)
        with c2: detail   = st.select_slider("Detail", ["Brief","Standard","Detailed"], value="Standard")

        if st.button("✨ Summarize with AI", use_container_width=True):
            if not st.session_state.gemini_client:
                st.warning("⚠️ Please configure your Gemini API key in the sidebar first.")
            else:
                with st.spinner("AI is thinking..."):
                    summary = ai_summarize(text, sum_lang)
                st.markdown("### 📋 Summary")
                st.markdown(f'<div class="edu-card">{summary}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    if GTTS_OK and st.button("🔊 Listen to Summary"):
                        tts_audio(summary[:600], LANGUAGES.get(sum_lang,"en"))
                with c2:
                    st.download_button("💾 Download Summary", summary,
                        file_name="summary.txt", mime="text/plain")
                if st.session_state.logged_in:
                    u = st.session_state.users[st.session_state.username]
                    u["xp"] = u.get("xp",0) + 5
                    st.session_state.progress.setdefault(st.session_state.username,[]).append(
                        {"type":"summary","date":datetime.now().strftime("%Y-%m-%d %H:%M"),"lang":sum_lang})

# ══════════════════════════════════════════════════════════════
#  PAGE: QUIZ
# ══════════════════════════════════════════════════════════════
def page_quiz():
    st.markdown("## ❓ AI Quiz Generator")

    if not st.session_state.quiz_submitted:
        # Setup screen
        if not st.session_state.current_quiz:
            topic = st.text_area("Paste study material / topic", height=160,
                placeholder="Paste any chapter, article, or notes...")
            c1,c2,c3 = st.columns(3)
            with c1: num_q    = st.number_input("Questions", 3, 15, 5)
            with c2: diff     = st.selectbox("Difficulty", ["Easy","Medium","Hard"])
            with c3: quiz_lang = st.selectbox("Quiz language", LANG_NAMES)

            if st.button("🎲 Generate Quiz", use_container_width=True):
                if not topic.strip():
                    st.warning("Please paste some study material first.")
                elif not st.session_state.gemini_client:
                    st.warning("⚠️ Configure Gemini API key in the sidebar first.")
                else:
                    with st.spinner("Generating quiz..."):
                        qs = generate_quiz(topic, int(num_q), diff)
                        # Translate if needed
                        code = LANGUAGES.get(quiz_lang,"en")
                        if code != "en" and TRANS_OK:
                            for q in qs:
                                q["question"]    = translate_text(q["question"], code)
                                q["options"]     = [translate_text(o,code) for o in q["options"]]
                                q["explanation"] = translate_text(q.get("explanation",""), code)
                        st.session_state.current_quiz   = qs
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                    st.rerun()
        else:
            # Question screen
            st.markdown(f"**{len(st.session_state.current_quiz)} Questions — choose your answers below**")
            with st.form("quiz_form"):
                for i, q in enumerate(st.session_state.current_quiz):
                    st.markdown(f'<div class="edu-card"><b>Q{i+1}. {q["question"]}</b></div>',
                                 unsafe_allow_html=True)
                    ans = st.radio("", q["options"], key=f"q_{i}",
                                   label_visibility="collapsed")
                    st.session_state.quiz_answers[i] = ans
                    st.markdown("")
                if st.form_submit_button("✅ Submit Quiz", use_container_width=True):
                    st.session_state.quiz_submitted = True
                    st.rerun()

            if st.button("🔄 Reset / New Quiz"):
                st.session_state.current_quiz   = []
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.rerun()
    else:
        # Results screen
        qs      = st.session_state.current_quiz
        answers = st.session_state.quiz_answers
        correct = sum(1 for i,q in enumerate(qs) if answers.get(i)==q["answer"])
        total   = len(qs)
        score   = int((correct/total)*100) if total else 0
        color   = "#22c55e" if score>=70 else "#f59e0b" if score>=40 else "#ef4444"
        emoji   = "🏆 Excellent!" if score>=80 else "👍 Good Job!" if score>=60 else "📚 Keep Practicing!"

        st.markdown(f"""
        <div style="text-align:center;padding:24px;">
            <div style="font-size:4.5em;font-weight:900;color:{color};">{score}%</div>
            <div style="font-size:1.4em;">{correct}/{total} correct</div>
            <div style="font-size:1.2em;margin-top:6px;">{emoji}</div>
        </div>""", unsafe_allow_html=True)

        with st.expander("📖 Review Answers"):
            for i,q in enumerate(qs):
                ua   = answers.get(i,"")
                ok   = ua == q["answer"]
                icon = "✅" if ok else "❌"
                st.markdown(f"**{icon} Q{i+1}. {q['question']}**")
                st.markdown(f"Your: `{ua}` | Correct: `{q['answer']}`")
                if q.get("explanation"):
                    st.info(f"💡 {q['explanation']}")
                st.markdown("---")

        # Save + XP
        if st.session_state.logged_in:
            un = st.session_state.username
            u  = st.session_state.users[un]
            u["xp"] = u.get("xp",0) + score//5
            u["completed_quizzes"] = u.get("completed_quizzes",0) + 1
            if score>=80 and "🏆 Quiz Master" not in u.get("badges",[]):
                u.setdefault("badges",[]).append("🏆 Quiz Master")
            st.session_state.quiz_scores.append({
                "user":un,"score":score,
                "date":datetime.now().strftime("%Y-%m-%d %H:%M"),"questions":total
            })
            lb  = st.session_state.leaderboard
            ent = next((x for x in lb if x["user"]==un), None)
            if ent:
                ent["best"]     = max(ent["best"],score)
                ent["attempts"] = ent.get("attempts",0)+1
            else:
                lb.append({"user":un,"best":score,"attempts":1})

        # Certificate
        if score >= 60:
            st.success("🎉 You earned a certificate!")
            cert = make_certificate(
                st.session_state.username or "Learner",
                score, datetime.now().strftime("%B %d, %Y"))
            if cert:
                st.download_button("📜 Download Certificate (PDF)", cert,
                    file_name="certificate.pdf", mime="application/pdf",
                    use_container_width=True)
            else:
                st.markdown(f"""
                <div class="cert-box">
                    <h2 style="color:#FFD700;">🎓 CERTIFICATE OF ACHIEVEMENT</h2>
                    <p>This certifies that</p>
                    <h3 style="color:#FFD700;">{st.session_state.username or 'Learner'}</h3>
                    <p>completed the EduAccess AI Quiz with a score of</p>
                    <h2 style="color:#FFD700;">{score}%</h2>
                    <p style="opacity:.7;">EduAccess AI · {datetime.now().strftime("%B %d, %Y")}</p>
                </div>""", unsafe_allow_html=True)

        c1,c2 = st.columns(2)
        with c1:
            if st.button("🔄 New Quiz", use_container_width=True):
                st.session_state.current_quiz   = []
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.rerun()
        with c2:
            if st.button("📊 View Analytics", use_container_width=True):
                st.session_state.page = "📊 Analytics"
                st.rerun()

# ══════════════════════════════════════════════════════════════
#  PAGE: ANALYTICS
# ══════════════════════════════════════════════════════════════
def page_analytics():
    st.markdown("## 📊 Quiz Analytics Dashboard")
    scores = st.session_state.quiz_scores
    if not scores:
        st.info("No quiz attempts yet. Take a quiz first!")
        return
    df = pd.DataFrame(scores)
    c1,c2,c3,c4 = st.columns(4)
    for col, icon, label, val in [
        (c1,"📝","Total Quizzes",str(len(df))),
        (c2,"🎯","Avg Score",   f"{df['score'].mean():.1f}%"),
        (c3,"🏆","Best Score",  f"{df['score'].max()}%"),
        (c4,"📈","Last Score",  f"{df['score'].iloc[-1]}%"),
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div style="font-size:1.8em;">{icon}</div>'
                        f'<div style="font-size:1.5em;font-weight:bold;">{val}</div>'
                        f'<div style="opacity:.7;">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    if PLOTLY_OK:
        c1,c2 = st.columns(2)
        with c1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=df["score"], mode="lines+markers",
                line=dict(color="#6C63FF",width=3), marker=dict(size=8,color="#FF6B9D")))
            fig.add_hline(y=df["score"].mean(), line_dash="dash", line_color="#FFD700",
                          annotation_text="Average")
            fig.update_layout(title="Score Trend", paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)", font_color="white",
                xaxis_title="Attempt", yaxis_title="Score (%)", yaxis=dict(range=[0,105]))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            bkts = {"Excellent ≥80":0,"Good 60-79":0,"Average 40-59":0,"Needs Work <40":0}
            for s in df["score"]:
                if s>=80: bkts["Excellent ≥80"]+=1
                elif s>=60: bkts["Good 60-79"]+=1
                elif s>=40: bkts["Average 40-59"]+=1
                else: bkts["Needs Work <40"]+=1
            fig2 = go.Figure(go.Pie(
                labels=list(bkts.keys()), values=list(bkts.values()), hole=0.45,
                marker_colors=["#22c55e","#6C63FF","#f59e0b","#ef4444"]))
            fig2.update_layout(title="Performance Distribution",
                paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.dataframe(df)

    with st.expander("📋 Full History"):
        st.dataframe(df, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: LEADERBOARD
# ══════════════════════════════════════════════════════════════
def page_leaderboard():
    st.markdown("## 🏆 Leaderboard")
    lb = sorted(st.session_state.leaderboard, key=lambda x: x["best"], reverse=True)
    if not lb:
        st.info("No scores yet! Take a quiz to appear here.")
        return
    medals = ["🥇","🥈","🥉"]
    for i, ent in enumerate(lb[:10]):
        m   = medals[i] if i<3 else f"#{i+1}"
        me  = ent["user"] == st.session_state.username
        brd = "border:2px solid #FFD700;" if me else ""
        st.markdown(f"""
        <div class="edu-card" style="{brd}display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:1.3em;">{m} <b>{ent['user']}</b>{"  🫵 You" if me else ""}</span>
            <span><b style="color:#FFD700;">{ent['best']}%</b> best · {ent.get('attempts',1)} attempt(s)</span>
        </div>""", unsafe_allow_html=True)

    if PLOTLY_OK and lb:
        fig = go.Figure(go.Bar(
            x=[e["user"] for e in lb[:10]],
            y=[e["best"]  for e in lb[:10]],
            marker_color=["#FFD700" if e["user"]==st.session_state.username else "#6C63FF" for e in lb[:10]],
            text=[f"{e['best']}%" for e in lb[:10]], textposition="outside"))
        fig.update_layout(title="Top Scores", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", font_color="white", yaxis=dict(range=[0,108]))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: PROGRESS
# ══════════════════════════════════════════════════════════════
def page_progress():
    st.markdown("## 📈 My Progress")
    if not st.session_state.logged_in:
        st.warning("Please login to see your progress.")
        return
    un = st.session_state.username
    u  = st.session_state.users.get(un,{})
    p  = st.session_state.progress.get(un,[])
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("⭐ XP Points",       u.get("xp",0))
    with c2: st.metric("📝 Quizzes Done",    u.get("completed_quizzes",0))
    with c3: st.metric("🎖️ Badges",          len(u.get("badges",[])))
    if u.get("badges"):
        st.markdown("### 🎖️ Badges")
        for b in u["badges"]: st.markdown(f'<span class="badge">{b}</span>', unsafe_allow_html=True)
    lvl    = u.get("xp",0)//50+1
    xp_mod = u.get("xp",0)%50
    st.markdown(f"### 🎮 Level {lvl}")
    st.progress(xp_mod/50, text=f"{xp_mod}/50 XP to next level")
    if p:
        st.markdown("### 📅 Activity")
        for item in reversed(p[-10:]):
            st.markdown(f'<div class="edu-card" style="padding:10px;">📝 {item.get("type","").title()} · {item.get("date","")} · {item.get("lang","")}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: TRANSLATE
# ══════════════════════════════════════════════════════════════
def page_translate():
    st.markdown("## 🌍 Translation (28 Languages)")
    c1,c2 = st.columns(2)
    with c1: src_lang = st.selectbox("From", LANG_NAMES, key="tf")
    with c2: tgt_lang = st.selectbox("To",   LANG_NAMES, index=2, key="tt")
    inp = st.text_area("Enter text", height=150)
    if st.button("🌐 Translate", use_container_width=True) and inp.strip():
        tgt_code = LANGUAGES.get(tgt_lang,"en")
        src_code = LANGUAGES.get(src_lang,"en")
        result   = ""
        if TRANS_OK:
            try:
                result = GoogleTranslator(source=src_code, target=tgt_code).translate(inp)
            except Exception:
                pass
        if not result:  # fallback to Gemini
            result = gemini_chat(f"Translate from {src_lang} to {tgt_lang}. Return only the translation:\n\n{inp}")
        st.markdown(f'<div class="edu-card" style="font-size:1.1em;">{result}</div>', unsafe_allow_html=True)
        if GTTS_OK and st.button("🔊 Listen"):
            tts_audio(result[:600], tgt_code)
        st.download_button("💾 Download", result, file_name="translation.txt")

# ══════════════════════════════════════════════════════════════
#  PAGE: VOICE TOOLS
# ══════════════════════════════════════════════════════════════
def page_voice():
    st.markdown("## 🎤 Voice Tools")
    tab1, tab2 = st.tabs(["🔊 Text to Speech","📖 Dyslexia Read-Aloud"])

    with tab1:
        vtext = st.text_area("Enter text to speak", height=160)
        c1,c2 = st.columns(2)
        with c1: v_lang = st.selectbox("Language", LANG_NAMES, key="vtl")
        with c2: speed  = st.select_slider("Speed",["Slow","Normal"],value="Normal")
        if st.button("🔊 Generate Speech", use_container_width=True):
            if vtext.strip() and GTTS_OK:
                buf = io.BytesIO()
                gTTS(text=vtext[:3000], lang=LANGUAGES.get(v_lang,"en"),
                     slow=(speed=="Slow")).write_to_fp(buf)
                buf.seek(0)
                st.audio(buf, format="audio/mp3")
                st.download_button("💾 Download MP3", buf.getvalue(),
                    file_name="speech.mp3", mime="audio/mp3")
            elif not GTTS_OK:
                st.error("gTTS not installed.")

    with tab2:
        st.info("Paste study material and listen chunk by chunk — ideal for dyslexic learners.")
        rtext  = st.text_area("Study material", height=180)
        chunks = st.slider("Words per chunk", 40,300,120)
        if rtext.strip() and st.button("▶️ Read Aloud", use_container_width=True):
            words  = rtext.split()
            parts  = [" ".join(words[i:i+chunks]) for i in range(0,len(words),chunks)]
            for i,part in enumerate(parts[:6]):
                st.markdown(f'<div class="edu-card" style="line-height:2.2;">{part}</div>', unsafe_allow_html=True)
                if GTTS_OK:
                    buf = io.BytesIO()
                    gTTS(text=part, lang=LANGUAGES.get(st.session_state.lang,"en"), slow=True).write_to_fp(buf)
                    buf.seek(0)
                    st.audio(buf, format="audio/mp3")

# ══════════════════════════════════════════════════════════════
#  PAGE: PDF EXPORT
# ══════════════════════════════════════════════════════════════
def page_pdf_export():
    st.markdown("## 📄 PDF Export")
    title   = st.text_input("Document title", value="EduAccess AI Report")
    content = st.text_area("Content to export", height=220)
    inc_hdr = st.checkbox("Include date/header", value=True)
    if st.button("📄 Generate PDF", use_container_width=True):
        if not content.strip():
            st.warning("Please enter some content.")
            return
        if REPORTLAB_OK:
            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=A4)
            styles = getSampleStyleSheet()
            purple = rl_colors.HexColor("#6C63FF")
            ts = ParagraphStyle("ti", fontSize=20, textColor=purple,
                                 spaceAfter=12, fontName="Helvetica-Bold")
            bs = ParagraphStyle("bo", fontSize=12, spaceAfter=8, leading=18)
            elems = []
            if inc_hdr:
                elems += [Paragraph(f"EduAccess AI · {datetime.now().strftime('%B %d, %Y')}", styles["Normal"]),
                           Spacer(1, 0.15*inch)]
            elems.append(Paragraph(title, ts))
            elems.append(Spacer(1, 0.1*inch))
            for line in content.split("\n"):
                if line.strip():
                    elems.append(Paragraph(line, bs))
            doc.build(elems)
            st.success("✅ PDF ready!")
            st.download_button("💾 Download PDF", buf.getvalue(),
                file_name=f"{title.replace(' ','_')}.pdf", mime="application/pdf",
                use_container_width=True)
        else:
            out = f"EduAccess AI Report\n{'='*40}\n{title}\n{datetime.now()}\n\n{content}"
            st.download_button("💾 Download TXT (install reportlab for PDF)", out,
                file_name=f"{title}.txt", mime="text/plain", use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  PAGE: PROFILE
# ══════════════════════════════════════════════════════════════
def page_profile():
    st.markdown("## 👤 My Profile")
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        return
    un = st.session_state.username
    u  = st.session_state.users.get(un,{})
    c1,c2 = st.columns([1,2])
    with c1:
        st.markdown(f"""
        <div class="edu-card" style="text-align:center;">
            <div style="font-size:3.5em;">👤</div>
            <h3>{un}</h3>
            <span class="badge">{u.get('role','student').title()}</span>
            <p style="opacity:.7;font-size:.85em;">Joined {u.get('joined','')}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.metric("⭐ XP Points", u.get("xp",0))
        st.metric("📝 Quizzes", u.get("completed_quizzes",0))
        st.metric("🎖️ Badges",  len(u.get("badges",[])))
        if u.get("badges"):
            st.markdown("**Badges:** " + "  ".join(u["badges"]))
    my = [s for s in st.session_state.quiz_scores if s.get("user")==un]
    if my and PLOTLY_OK:
        fig = px.line(pd.DataFrame(my), y="score", title="My Score History",
                      markers=True, color_discrete_sequence=["#6C63FF"])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                          font_color="white", yaxis=dict(range=[0,105]))
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
ROUTES = {
    "🏠 Home":        page_home,
    "🔐 Login":       page_auth,
    "🤖 AI Chatbot":  page_chatbot,
    "📝 Summarizer":  page_summarizer,
    "❓ AI Quiz":     page_quiz,
    "📊 Analytics":   page_analytics,
    "🏆 Leaderboard": page_leaderboard,
    "📈 Progress":    page_progress,
    "🌍 Translate":   page_translate,
    "🎤 Voice Tools": page_voice,
    "📄 PDF Export":  page_pdf_export,
    "👤 Profile":     page_profile,
}
PROTECTED = {"🤖 AI Chatbot","📝 Summarizer","❓ AI Quiz",
             "📊 Analytics","📈 Progress","👤 Profile"}

# ── Run ──────────────────────────────────────────────────────
sidebar()
apply_styles()   # re-apply after sidebar toggles

pg = st.session_state.page
if pg in PROTECTED and not st.session_state.logged_in:
    st.warning("⚠️ Please login first to access this feature.")
    page_auth()
else:
    ROUTES.get(pg, page_home)()

st.markdown("---")
st.markdown(
    '<div style="text-align:center;opacity:.45;font-size:.78em;">'
    '🎓 EduAccess AI · Final Year Major Project · '
    'Streamlit + Gemini AI · 28 Languages · Dyslexia-Friendly'
    '</div>', unsafe_allow_html=True)
