import os, time
import streamlit as st
from sample_calls import SAMPLE_CALLS
from analyzer import analyze_transcript

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="vocAI – Call Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Session state ────────────────────────────────────────────
DEFAULTS = {"stage":"input","transcript":"","analysis":None,"active_section":1}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY",""))

# ── Constants ────────────────────────────────────────────────
STAGES = [
    (1,"Instant Summary","01","⚡"),
    (2,"Emotional Intelligence","02","🧠"),
    (3,"Agent Performance","03","🏆"),
    (4,"Conversation Intelligence","04","💬"),
    (5,"Email Generator","05","✉️"),
    (6,"AI Coach Mode","06","🎯"),
]

ANALYSIS_STEPS = [
    "Extracting summary",
    "Mapping emotions",
    "Scoring performance",
    "Understanding conversation",
    "Generating email",
    "Final insights",
]

# ── CSS (UPDATED ONLY) ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root{
--bg:#f7fbfb;
--bg2:#ffffff;
--bg3:#eef7f6;

--border:#dcefed;
--border2:#c6e3df;

--accent:#0ea5a4;
--accent2:#14b8a6;

--text:#0f172a;
--text2:#475569;
--text3:#94a3b8;

--font:'Inter',sans-serif;

--shadow-sm:0 2px 6px rgba(0,0,0,0.04);
--shadow-md:0 6px 20px rgba(0,0,0,0.06);
}

html,body,[class*="css"]{
font-family:var(--font)!important;
background:var(--bg)!important;
color:var(--text)!important;
}

#MainMenu,footer,header{visibility:hidden!important;}

.main .block-container{
padding:2.2rem 2.8rem 5rem 2.8rem!important;
max-width:1100px!important;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background:#ffffff!important;
border-right:1px solid var(--border)!important;
}

/* Buttons */
.stButton>button{
background:var(--accent)!important;
color:white!important;
border-radius:10px!important;
font-weight:600!important;
}

.stButton>button:hover{
background:var(--accent2)!important;
}

/* Cards */
.sample-card{
background:white;
border:1px solid var(--border);
border-radius:12px;
padding:16px;
margin-bottom:10px;
box-shadow:var(--shadow-sm);
}

/* Text area */
textarea{
border-radius:10px!important;
border:1px solid var(--border2)!important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("## vocAI")
        for num,label,_,_ in STAGES:
            if st.button(label, key=f"nav_{num}"):
                st.session_state.active_section = num

# ── Render Sidebar ──────────────────────────────────────────
render_sidebar()

# ── INPUT PAGE ──────────────────────────────────────────────
if st.session_state.stage == "input":

    st.markdown('''
    <div style="font-size:44px;font-weight:900;">
    voc<span style="color:#0ea5a4;">AI</span>
    </div>
    <div style="color:#64748b;margin-bottom:20px;">
    Call Intelligence Platform
    </div>
    ''', unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["Sample Calls","Upload Audio","Paste Transcript"])

    with tab3:
        ti = st.text_area("", height=250)
        if st.button("Run Analysis"):
            if ti.strip():
                st.session_state.transcript = ti
                st.session_state.stage = "analyzing"
                st.rerun()

    with tab1:
        for idx,s in enumerate(SAMPLE_CALLS):
            st.markdown(f'<div class="sample-card">{s["title"]}</div>', unsafe_allow_html=True)
            if st.button("Analyze", key=f"s{idx}"):
                st.session_state.transcript = s["transcript"]
                st.session_state.stage = "analyzing"
                st.rerun()

    with tab2:
        uploaded = st.file_uploader("Upload file", type=["mp3","wav","m4a"])
        if uploaded:
            if st.button("Transcribe & Analyze"):
                st.session_state.transcript = "audio transcript"
                st.session_state.stage = "analyzing"
                st.rerun()

# ── ANALYZING ──────────────────────────────────────────────
elif st.session_state.stage == "analyzing":

    st.markdown("<h2>Analyzing...</h2>", unsafe_allow_html=True)

    pb = st.progress(0)
    st_ = st.empty()

    if groq_api_key:
        result = analyze_transcript(
            st.session_state.transcript,
            groq_api_key,
            pb,
            st_,
            ANALYSIS_STEPS
        )
        st.session_state.analysis = result
        st.session_state.stage = "results"
        st.rerun()

# ── RESULTS ────────────────────────────────────────────────
elif st.session_state.stage == "results":
    st.write("Results loaded")

# ── Footer ────────────────────────────────────────────────
st.markdown("<div style='text-align:center;color:#94a3b8;'>vocAI · AI Call Intelligence</div>", unsafe_allow_html=True)
