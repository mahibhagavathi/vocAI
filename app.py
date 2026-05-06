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

# ── CSS (FULL REDESIGN) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root{
--bg:#f9fbfb;
--card:#ffffff;
--border:#e6f0ef;
--text:#0f172a;
--sub:#5f6f73;

--accent:#0ea5a4;
--accent-soft:#e6f7f6;
--accent-strong:#0891b2;

--radius:14px;
--shadow:0 4px 20px rgba(0,0,0,0.04);
}

html,body,[class*="css"]{
font-family:'Inter',sans-serif!important;
background:var(--bg)!important;
color:var(--text)!important;
}

#MainMenu, footer, header{visibility:hidden;}

.main .block-container{
padding:2.5rem 3rem 4rem 3rem;
max-width:1100px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
background:#ffffff;
border-right:1px solid var(--border);
}

.sb-title{
font-size:20px;
font-weight:800;
padding:20px;
}

.sb-step{
display:flex;
align-items:center;
gap:10px;
padding:10px 20px;
font-size:14px;
color:var(--sub);
cursor:pointer;
}

.sb-step.active{
color:var(--accent);
font-weight:600;
}

.dot{
width:8px;
height:8px;
border-radius:50%;
background:#cbd5e1;
}

.dot.active{
background:var(--accent);
box-shadow:0 0 0 4px rgba(14,165,164,0.15);
}

/* Cards */
.card{
background:var(--card);
border-radius:var(--radius);
padding:20px;
box-shadow:var(--shadow);
transition:all .2s ease;
}

.card:hover{
transform:translateY(-2px);
box-shadow:0 8px 28px rgba(0,0,0,0.06);
}

/* Buttons */
.stButton>button{
background:var(--accent);
color:white;
border:none;
border-radius:10px;
padding:10px 18px;
font-weight:600;
transition:all .2s;
}

.stButton>button:hover{
background:var(--accent-strong);
transform:translateY(-1px);
}

/* Inputs */
textarea{
border-radius:12px!important;
border:1px solid var(--border)!important;
}

/* Hero */
.hero{
text-align:center;
padding:40px 0 30px;
}

.hero-title{
font-size:34px;
font-weight:800;
letter-spacing:-1px;
margin-bottom:10px;
}

.hero-sub{
font-size:16px;
color:var(--sub);
max-width:520px;
margin:auto;
line-height:1.6;
}

/* Animation shimmer */
@keyframes shimmer{
0%{background-position:-400px 0;}
100%{background-position:400px 0;}
}

.shimmer{
background:linear-gradient(90deg,#eee 25%,#f5f5f5 37%,#eee 63%);
background-size:400px 100%;
animation:shimmer 1.4s infinite;
height:14px;
border-radius:6px;
}

/* Floating animation */
@keyframes float{
0%{transform:translateY(0);}
50%{transform:translateY(-6px);}
100%{transform:translateY(0);}
}

.float{
animation:float 3s ease-in-out infinite;
}

/* Footer */
.footer{
text-align:center;
color:#94a3b8;
font-size:12px;
margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown('<div class="sb-title">vocAI</div>', unsafe_allow_html=True)

        steps = ["Summary","Emotion","Agent","Conversation","Email","Coach"]
        for i,step in enumerate(steps,1):
            active = "active" if st.session_state.active_section==i else ""
            st.markdown(f'<div class="sb-step {active}"><div class="dot {active}"></div>{step}</div>', unsafe_allow_html=True)

# ── Input Page ─────────────────────────────────────────────
render_sidebar()

if st.session_state.stage == "input":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">Turn conversations into clarity</div>
        <div class="hero-sub">
            Analyze customer calls, extract insights, and generate actions — instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["Sample","Upload","Paste"])

    with tab3:
        ti = st.text_area("",height=250)
        if st.button("Run Analysis",use_container_width=True):
            if ti.strip():
                st.session_state.transcript=ti
                st.session_state.stage="analyzing"
                st.rerun()

    with tab1:
        for i,s in enumerate(SAMPLE_CALLS):
            st.markdown(f'<div class="card">{s["title"]}</div>', unsafe_allow_html=True)
            if st.button("Analyze",key=i):
                st.session_state.transcript=s["transcript"]
                st.session_state.stage="analyzing"
                st.rerun()

# ── Analyzing ─────────────────────────────────────────────
elif st.session_state.stage == "analyzing":

    st.markdown("""
    <div style="text-align:center;padding:80px;">
        <img class="float" src="https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif" width="120">
        <h2>Analyzing your call...</h2>
    </div>
    """, unsafe_allow_html=True)

    pb = st.progress(0)
    st_ = st.empty()

    if groq_api_key:
        result = analyze_transcript(st.session_state.transcript, groq_api_key, pb, st_, [])
        st.session_state.analysis=result
        st.session_state.stage="results"
        st.rerun()

# ── Results ─────────────────────────────────────────────
elif st.session_state.stage == "results":

    st.markdown('<div class="card">Results Loaded ✅</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────
st.markdown('<div class="footer">vocAI · AI Call Intelligence</div>', unsafe_allow_html=True)
