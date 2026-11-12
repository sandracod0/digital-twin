"""
Digital Twin - Streamlit chat app
Run:  streamlit run app.py
"""
import os
import json
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# 1. PROFILE  -> EDIT THIS SECTION: this is "you"
# ============================================================
PROFILE = {
    "name": "Mercyline Sandra",
    "location": "Nairobi, Kenya",
    "role": "Computer Science student and aspiring AI engineer",
    "bio": (
        "I am a third-year Computer Science student in Nairobi who loves building "
        "practical software that solves everyday problems. I enjoy Python, web apps "
        "and AI, and I am learning how to turn ideas into tools people can actually use."
    ),
    "skills": [
        "Python",
        "Streamlit",
        "HTML, CSS and JavaScript",
        "SQL and databases",
        "Git and GitHub",
        "Prompt engineering and LLM apps",
        "Data structures and algorithms",
    ],
    "interests": [
        "AI for Africa",
        "Education technology",
        "Mobile-friendly web apps",
        "Open source",
        "Mentoring other students",
    ],
    "experience": [
        "Built this AI digital twin chatbot with Streamlit as part of an AI engineering course",
        "Created a student timetable and revision planner web app",
        "Built a Swahili-English vocabulary quiz app in Python",
        "Member of the university computer science club, helping first-year students learn to code",
        "Completed a campus internship project building a simple records dashboard",
    ],
    "goals": (
        "Graduate with a strong CS degree, land an AI or software engineering role, "
        "and build AI tools in English and Kiswahili that help students and small "
        "businesses across Africa."
    ),
    "tone": "friendly, clear, enthusiastic but professional",
}

# ============================================================
# 2. Page config + translations
# ============================================================
st.set_page_config(
    page_title=f"{PROFILE['name']} | Digital Twin",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed",  # better on mobile
)

TEXT = {
    "English": {
        "title": "Digital Twin",
        "subtitle": "Ask me anything about my work, skills and experience.",
        "placeholder": "Type your question...",
        "thinking": "Thinking...",
        "settings": "Settings",
        "dark": "Dark mode",
        "lang": "Language",
        "temp": "Creativity",
        "length": "Max reply length",
        "stats": "Usage statistics",
        "msgs": "Messages",
        "avg": "Avg response (s)",
        "tokens": "Est. tokens",
        "export": "Export chat",
        "clear": "Clear chat",
        "confirm": "Yes, clear it",
        "cancel": "Cancel",
        "sure": "Are you sure? This deletes the whole conversation.",
        "cleared": "Chat cleared.",
        "no_key": "No API key found. Add GROQ_API_KEY (or another provider key) to your .env file.",
        "error": "Something went wrong. Please try again.",
        "suggest": "Try asking:",
        "examples": ["Who are you?", "What are your skills?", "Tell me about your projects", "What are your goals?"],
        "welcome": f"Hi! I'm {PROFILE['name']}'s digital twin. How can I help?",
    },
    "Kiswahili": {
        "title": "Pacha wa Kidijitali",
        "subtitle": "Niulize chochote kuhusu kazi, ujuzi na uzoefu wangu.",
        "placeholder": "Andika swali lako...",
        "thinking": "Nafikiria...",
        "settings": "Mipangilio",
        "dark": "Hali ya giza",
        "lang": "Lugha",
        "temp": "Ubunifu",
        "length": "Urefu wa jibu",
        "stats": "Takwimu za matumizi",
        "msgs": "Ujumbe",
        "avg": "Wastani wa jibu (s)",
        "tokens": "Makadirio ya tokeni",
        "export": "Hamisha mazungumzo",
        "clear": "Futa mazungumzo",
        "confirm": "Ndiyo, futa",
        "cancel": "Ghairi",
        "sure": "Una uhakika? Mazungumzo yote yatafutwa.",
        "cleared": "Mazungumzo yamefutwa.",
        "no_key": "Hakuna API key. Weka GROQ_API_KEY (au key nyingine) kwenye faili la .env.",
        "error": "Hitilafu imetokea. Tafadhali jaribu tena.",
        "suggest": "Jaribu kuuliza:",
        "examples": ["Wewe ni nani?", "Una ujuzi gani?", "Niambie kuhusu miradi yako", "Malengo yako ni yapi?"],
        "welcome": f"Habari! Mimi ni pacha wa kidijitali wa {PROFILE['name']}. Nikusaidie vipi?",
    },
}

# ============================================================
# 3. Session state
# ============================================================
def init_state():
    defaults = {
        "messages": [],
        "lang": "English",
        "dark": False,
        "temperature": 0.7,
        "max_tokens": 600,
        "response_times": [],
        "confirm_clear": False,
        "pending": None,  # clicked example question
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


init_state()

# ============================================================
# 4. Sidebar (settings, stats, export, clear)
# ============================================================
with st.sidebar:
    t = TEXT[st.session_state.lang]
    st.header(f"⚙️ {t['settings']}")

    st.session_state.lang = st.selectbox(
        t["lang"], list(TEXT.keys()), index=list(TEXT.keys()).index(st.session_state.lang)
    )
    t = TEXT[st.session_state.lang]

    st.session_state.dark = st.toggle(f"🌙 {t['dark']}", value=st.session_state.dark)
    st.session_state.temperature = st.slider(t["temp"], 0.0, 1.0, st.session_state.temperature, 0.1)
    st.session_state.max_tokens = st.slider(t["length"], 100, 1500, st.session_state.max_tokens, 50)

    st.divider()
    st.subheader(f"📊 {t['stats']}")
    times = st.session_state.response_times
    est_tokens = sum(len(m["content"]) for m in st.session_state.messages) // 4
    c1, c2 = st.columns(2)
    c1.metric(t["msgs"], len(st.session_state.messages))
    c2.metric(t["avg"], f"{(sum(times) / len(times)):.1f}" if times else "0.0")
    st.metric(t["tokens"], est_tokens)

    st.divider()
    if st.session_state.messages:
        payload = json.dumps(
            {
                "exported_at": datetime.now().isoformat(timespec="seconds"),
                "twin": PROFILE["name"],
                "messages": st.session_state.messages,
            },
            indent=2,
            ensure_ascii=False,
        )
        st.download_button(
            f"💾 {t['export']}",
            payload,
            file_name=f"digital_twin_chat_{datetime.now():%Y%m%d_%H%M}.json",
            mime="application/json",
            use_container_width=True,
        )

        if not st.session_state.confirm_clear:
            if st.button(f"🗑️ {t['clear']}", use_container_width=True):
                st.session_state.confirm_clear = True
                st.rerun()
        else:
            st.warning(t["sure"])
            a, b = st.columns(2)
            if a.button(t["confirm"], type="primary", use_container_width=True):
                st.session_state.messages = []
                st.session_state.response_times = []
                st.session_state.confirm_clear = False
                st.toast(t["cleared"], icon="✅")
                st.rerun()
            if b.button(t["cancel"], use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()

t = TEXT[st.session_state.lang]

# ============================================================
# 5. Styling (mobile friendly + dark/light)
# ============================================================
if st.session_state.dark:
    bg, fg, card = "#0e1117", "#fafafa", "#1c1f26"
else:
    bg, fg, card = "#ffffff", "#1a1a1a", "#f4f6fb"

st.markdown(
    f"""
    <style>
    .stApp {{ background-color: {bg}; color: {fg}; }}
    .stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp span {{ color: {fg}; }}
    [data-testid="stChatMessage"] {{ background: {card}; border-radius: 14px; padding: 0.6rem 0.9rem; }}
    .hero {{ text-align:center; padding: 0.5rem 0 1rem 0; }}
    .hero h1 {{ margin-bottom: 0; font-size: clamp(1.6rem, 5vw, 2.4rem); }}
    .hero p {{ opacity: .75; margin-top: .3rem; }}
    @media (max-width: 640px) {{
        .block-container {{ padding: 1rem .6rem 5rem .6rem; }}
        .stButton button {{ width: 100%; }}
    }}
    #MainMenu, footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 6. LLM layer (Anthropic or OpenAI, whichever key is in .env)
# ============================================================
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")


def build_system_prompt() -> str:
    p = PROFILE
    return f"""You are the digital twin of {p['name']}. Speak in first person as {p['name']}.

ABOUT ME
- Location: {p['location']}
- Role: {p['role']}
- Bio: {p['bio']}
- Skills: {', '.join(p['skills'])}
- Interests: {', '.join(p['interests'])}
- Experience: {'; '.join(p['experience'])}
- Goals: {p['goals']}

RULES
- Tone: {p['tone']}.
- Only state facts that are in the profile above. If asked something you don't know,
  say so honestly and offer to pass the question on. Never invent details.
- Reply in {st.session_state.lang}.
- Keep answers concise and easy to read on a phone."""


def stream_reply(history):
    """Yield text chunks from whichever provider is configured."""
    system = build_system_prompt()
    temp = st.session_state.temperature
    max_tokens = st.session_state.max_tokens

    if ANTHROPIC_KEY:
        import anthropic

        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        with client.messages.stream(
            model=os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
            max_tokens=max_tokens,
            temperature=temp,
            system=system,
            messages=history,
        ) as stream:
            for text in stream.text_stream:
                yield text

    elif OPENAI_KEY or GROQ_KEY or GEMINI_KEY:
        from openai import OpenAI

        # Groq and Gemini both offer OpenAI-compatible endpoints
        if GROQ_KEY:
            client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
            model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
        elif GEMINI_KEY:
            client = OpenAI(
                api_key=GEMINI_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
            model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        else:
            client = OpenAI(api_key=OPENAI_KEY)
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        extra = {}
        if model.startswith("openai/gpt-oss"):
            # these are reasoning models: keep thinking short so replies are fast
            extra["extra_body"] = {"reasoning_effort": "low"}

        stream = client.chat.completions.create(
            model=model,
            temperature=temp,
            max_tokens=max(max_tokens, 1000),
            messages=[{"role": "system", "content": system}] + history,
            stream=True,
            **extra,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    else:
        raise RuntimeError("NO_KEY")


# ============================================================
# 7. Main UI
# ============================================================
st.markdown(
    f"""<div class="hero"><h1>🎭 {PROFILE['name']}</h1>
    <p>{t['title']} · {t['subtitle']}</p></div>""",
    unsafe_allow_html=True,
)

if not (ANTHROPIC_KEY or OPENAI_KEY or GROQ_KEY or GEMINI_KEY):
    st.error(t["no_key"])
    st.stop()

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🎭"):
        st.write(t["welcome"])
    st.caption(t["suggest"])
    cols = st.columns(2)
    for i, q in enumerate(t["examples"]):
        if cols[i % 2].button(q, key=f"ex{i}"):
            st.session_state.pending = q
            st.rerun()

# Render history
for m in st.session_state.messages:
    with st.chat_message(m["role"], avatar="🧑" if m["role"] == "user" else "🎭"):
        st.write(m["content"])

# Input (typed or clicked example)
user_input = st.chat_input(t["placeholder"]) or st.session_state.pending
st.session_state.pending = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="🧑"):
        st.write(user_input)

    with st.chat_message("assistant", avatar="🎭"):
        start = time.time()
        try:
            with st.spinner(t["thinking"]):
                reply = st.write_stream(stream_reply(st.session_state.messages))
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.response_times.append(time.time() - start)
            st.rerun()  # only rerun on success so the sidebar stats refresh
        except Exception as e:
            if type(e).__name__ in ("RerunException", "StopException"):
                raise  # let Streamlit handle its own control-flow exceptions
            # keep the error on screen (no rerun here)
            st.session_state.messages.pop()
            if str(e) == "NO_KEY":
                st.error(t["no_key"])
            else:
                st.error(t["error"])
                st.code(f"{type(e).__name__}: {e}")