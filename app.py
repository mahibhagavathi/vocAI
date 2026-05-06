import streamlit as st
import os
from groq import Groq
import time

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="vocAI – Call Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded")

 # ─── Sidebar state control ─────────────────────────────
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

if st.session_state.sidebar_open:
    st.markdown("""
    <script>
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) sidebar.style.display = "block";
    </script>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <script>
        const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) sidebar.style.display = "none";
    </script>
    """, unsafe_allow_html=True)

# ─── Floating toggle button (always visible) ───────────
st.markdown("""
<style>
#sidebarToggle {
    position: fixed;
    top: 12px;
    left: 12px;
    z-index: 999999;
}
</style>
""", unsafe_allow_html=True)

if st.button(
    "☰" if not st.session_state.sidebar_open else "✕",
    key="sidebar_toggle"
):
    st.session_state.sidebar_open = not st.session_state.sidebar_open
    st.rerun()

# ─── Imports ──────────────────────────────────────────────────────────────────
from sample_calls import SAMPLE_CALLS
from analyzer import analyze_transcript

# ─── Inject Global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:           #f7f6fb;
    --bg2:          #ffffff;
    --bg3:          #f0eef8;
    --border:       #e2ddf2;
    --border2:      #ccc6e8;
    --accent:       #5b3fce;
    --accent2:      #7c5fe6;
    --accent3:      #9d7ff5;
    --accent-light: rgba(91,63,206,0.08);
    --accent-glow:  rgba(91,63,206,0.14);
    --heading:      #2d1b69;
    --subheading:   #5b3fce;
    --green:        #0e9e6e;
    --green-bg:     rgba(14,158,110,0.08);
    --green-border: rgba(14,158,110,0.25);
    --red:          #d63f5a;
    --red-bg:       rgba(214,63,90,0.07);
    --red-border:   rgba(214,63,90,0.22);
    --amber:        #c47e0a;
    --amber-bg:     rgba(196,126,10,0.08);
    --amber-border: rgba(196,126,10,0.25);
    --blue:         #2563a8;
    --blue-bg:      rgba(37,99,168,0.08);
    --text:         #1a1228;
    --text2:        #4a4060;
    --text3:        #8878aa;
    --font:         'Plus Jakarta Sans', sans-serif;
    --mono:         'JetBrains Mono', monospace;
    --shadow-sm:    0 1px 4px rgba(91,63,206,0.08);
    --shadow-md:    0 4px 16px rgba(91,63,206,0.10);
    --shadow-lg:    0 8px 32px rgba(91,63,206,0.13);
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ─── Sidebar ─── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid var(--border) !important;
    width: 280px !important;
    box-shadow: 2px 0 12px rgba(91,63,206,0.06) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ─── Main area ─── */
.main .block-container {
    padding: 2rem 2.5rem 4rem 2.5rem !important;
    max-width: 1100px !important;
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ─── Sidebar brand ─── */
.sb-brand {
    padding: 28px 24px 20px 24px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 8px;
    background: linear-gradient(135deg, #f0eef8 0%, #ffffff 100%);
}
.sb-brand-logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--heading);
}
.sb-brand-logo span { color: var(--accent2); }
.sb-brand-sub {
    font-size: 10.5px;
    color: var(--text3);
    margin-top: 3px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ─── Sidebar section label ─── */
.sb-section-label {
    padding: 6px 24px 4px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text3);
}

/* ─── Nav buttons ─── */
.stSidebar .stButton > button {
    width: 100% !important;
    text-align: left !important;
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 11px 24px !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    color: var(--text2) !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    font-family: var(--font) !important;
    letter-spacing: 0 !important;
    box-shadow: none !important;
}
.stSidebar .stButton > button:hover {
    background: var(--accent-light) !important;
    color: var(--accent) !important;
}

/* ─── Sidebar status dots ─── */
.dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.dot-done   { background: var(--green); }
.dot-active { background: var(--accent2); box-shadow: 0 0 6px var(--accent-glow); }
.dot-idle   { background: var(--border2); }

/* ─── Sidebar divider ─── */
.sb-divider {
    height: 1px;
    background: var(--border);
    margin: 10px 16px;
}

/* ─── Sidebar info box ─── */
.sb-info {
    margin: 16px;
    padding: 14px;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    font-size: 12px;
    color: var(--text2);
    line-height: 1.6;
}
.sb-info b { color: var(--text); }

/* ─── Page header ─── */
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
}
.page-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--heading);
    letter-spacing: -0.3px;
}
.page-subtitle {
    font-size: 13px;
    color: var(--text3);
    margin-top: 3px;
}

/* ─── Progress breadcrumb ─── */
.breadcrumb {
    display: flex;
    gap: 6px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 28px;
}
.bc-step {
    font-size: 11.5px;
    padding: 4px 12px;
    border-radius: 99px;
    border: 1px solid var(--border2);
    color: var(--text3);
    background: var(--bg2);
    font-weight: 500;
}
.bc-step.active {
    background: var(--accent-light);
    border-color: var(--accent);
    color: var(--accent);
    font-weight: 600;
}
.bc-step.done {
    background: var(--green-bg);
    border-color: var(--green-border);
    color: var(--green);
    font-weight: 600;
}
.bc-arrow { color: var(--text3); font-size: 11px; }

/* ─── Input stage cards ─── */
.input-hero {
    text-align: center;
    padding: 52px 24px 40px;
}
.input-hero-title {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: var(--heading);
    line-height: 1.15;
}
.input-hero-title span { color: var(--accent2); }
.input-hero-sub {
    font-size: 15.5px;
    color: var(--text2);
    margin-top: 14px;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.65;
    font-weight: 400;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg3) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text2) !important;
    border-radius: 8px !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    font-family: var(--font) !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg2) !important;
    color: var(--accent) !important;
    border: 1px solid var(--border2) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 24px 0 0 0 !important;
}

/* ─── Text area ─── */
.stTextArea textarea {
    background: var(--bg2) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}
.stTextArea textarea::placeholder { color: var(--text3) !important; }

/* ─── Buttons ─── */
.stButton > button {
    background: var(--accent) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    font-family: var(--font) !important;
    letter-spacing: 0 !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 3px 12px rgba(91,63,206,0.28) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(91,63,206,0.38) !important;
    background: var(--accent2) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ─── Sample card ─── */
.sample-card {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    cursor: default;
}
.sample-card:hover {
    border-color: var(--accent2);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
.sample-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--heading);
    margin-bottom: 5px;
}
.sample-meta {
    font-size: 11.5px;
    color: var(--text3);
    margin-bottom: 8px;
    letter-spacing: 0.02em;
    font-weight: 500;
}
.sample-preview {
    font-size: 13px;
    color: var(--text2);
    font-style: italic;
    line-height: 1.55;
}

/* ─── Analyzing screen ─── */
.analyzing-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 24px;
    text-align: center;
}
.analyzing-orb {
    width: 76px; height: 76px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-light), var(--bg3));
    border: 2.5px solid var(--accent2);
    margin-bottom: 28px;
    animation: pulse 2s ease-in-out infinite;
    box-shadow: 0 0 0 0 var(--accent-glow);
}
@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 var(--accent-glow); }
    50%       { transform: scale(1.08); box-shadow: 0 0 0 16px transparent; }
}
.analyzing-title {
    font-size: 23px;
    font-weight: 700;
    color: var(--heading);
    margin-bottom: 6px;
    letter-spacing: -0.3px;
}
.analyzing-sub { font-size: 14px; color: var(--text2); margin-bottom: 32px; }

/* ─── Stage header ─── */
.stage-hdr {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 0 0 24px 0;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--border);
}
.stage-num {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--accent);
    font-family: var(--mono);
    background: var(--accent-light);
    border: 1.5px solid var(--border2);
    padding: 3px 10px;
    border-radius: 6px;
    text-transform: uppercase;
}
.stage-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--heading);
    letter-spacing: -0.3px;
}

/* ─── Metric cards ─── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 20px;
}
.metric-card {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: var(--shadow-sm);
}
.metric-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 9px;
}
.metric-value {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.25;
}

/* ─── Summary box ─── */
.summary-box {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 22px 26px;
    margin-top: 8px;
    box-shadow: var(--shadow-sm);
}
.summary-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--subheading);
    margin-bottom: 11px;
}
.summary-text {
    font-size: 14.5px;
    color: var(--text);
    line-height: 1.75;
}

/* ─── Resolution badge ─── */
.res-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 13px;
    border-radius: 99px;
    letter-spacing: 0.03em;
}
.res-resolved   { background: var(--green-bg);  color: var(--green); border: 1.5px solid var(--green-border); }
.res-unresolved { background: var(--red-bg);    color: var(--red);   border: 1.5px solid var(--red-border); }
.res-escalated  { background: var(--amber-bg);  color: var(--amber); border: 1.5px solid var(--amber-border); }

/* ─── Expander ─── */
details {
    background: var(--bg2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0 !important;
    margin-bottom: 12px !important;
    box-shadow: var(--shadow-sm) !important;
}
details summary {
    padding: 16px 20px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--heading) !important;
    cursor: pointer !important;
}
.exp-inner { padding: 4px 4px 8px 4px; }

/* ─── Phase cards ─── */
.phase-grid {
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.phase-card {
    background: var(--bg3);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 18px;
    text-align: center;
}
.phase-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.09em; color: var(--subheading); margin-bottom: 10px; font-weight: 700; }
.phase-emoji { font-size: 28px; margin-bottom: 6px; }
.phase-value { font-size: 13px; font-weight: 700; color: var(--text); }

/* ─── Spike items ─── */
.subsection-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.09em;
    text-transform: uppercase;
    color: var(--subheading);
    margin: 20px 0 10px 0;
}
.spike-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
}
.spike-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 99px;
    border: 1.5px solid;
    white-space: nowrap;
    flex-shrink: 0;
}
.spike-desc { font-size: 13.5px; color: var(--text); line-height: 1.55; }
.critical-item {
    background: var(--amber-bg);
    border: 1.5px solid var(--amber-border);
    border-radius: 8px;
    padding: 11px 15px;
    font-size: 13.5px;
    color: var(--amber);
    margin-bottom: 8px;
    font-weight: 500;
}

/* ─── Score ring ─── */
.score-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0 24px;
}
.score-ring {
    width: 108px; height: 108px;
    border-radius: 50%;
    background: conic-gradient(var(--accent) calc(var(--score) * 36deg), var(--bg3) 0deg);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
    box-shadow: var(--shadow-md);
}
.score-inner {
    width: 82px; height: 82px;
    border-radius: 50%;
    background: var(--bg2);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-number { font-size: 26px; font-weight: 800; color: var(--heading); line-height: 1; }
.score-label  { font-size: 11px; color: var(--text3); font-weight: 500; }
.score-title  { font-size: 13px; color: var(--text2); font-weight: 600; }

/* ─── Score bars ─── */
.score-bar-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 13px;
}
.score-bar-label {
    width: 170px;
    font-size: 13px;
    color: var(--text2);
    flex-shrink: 0;
    font-weight: 500;
}
.score-bar-track {
    flex: 1;
    height: 7px;
    background: var(--bg3);
    border-radius: 99px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.score-bar-num {
    font-size: 12px;
    font-family: var(--mono);
    color: var(--text);
    font-weight: 600;
    width: 36px;
    text-align: right;
    flex-shrink: 0;
}

/* ─── Quote blocks ─── */
.quote-block {
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 14px;
    line-height: 1.65;
    margin-bottom: 10px;
    font-style: italic;
}
.customer-quote {
    background: var(--blue-bg);
    border-left: 3px solid var(--blue);
    color: var(--text);
}
.best-quote {
    background: var(--green-bg);
    border-left: 3px solid var(--green);
    color: var(--text);
}
.worst-quote {
    background: var(--red-bg);
    border-left: 3px solid var(--red);
    color: var(--text);
}

/* ─── Critical moments ─── */
.moment-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 15px;
    background: var(--bg3);
    border: 1.5px solid var(--border);
    border-radius: 10px;
    margin-bottom: 10px;
}
.moment-icon { font-size: 20px; flex-shrink: 0; }
.moment-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--subheading); margin-bottom: 5px; font-weight: 700; }
.moment-desc  { font-size: 13.5px; color: var(--text); line-height: 1.55; }

/* ─── Rewrite cards ─── */
.rewrite-card {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-sm);
}
.rewrite-original {
    font-size: 13.5px;
    color: var(--text2);
    line-height: 1.55;
    margin-bottom: 12px;
}
.rewrite-arrow {
    font-size: 12px;
    font-weight: 700;
    color: var(--subheading);
    letter-spacing: 0.05em;
    margin-bottom: 12px;
}
.rewrite-better {
    font-size: 13.5px;
    color: var(--green);
    line-height: 1.55;
    font-weight: 500;
}
.rw-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 8px;
    vertical-align: middle;
}
.orig-tag   { background: var(--red-bg);   color: var(--red); }
.better-tag { background: var(--green-bg); color: var(--green); }

/* ─── Pathway steps ─── */
.pathway-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border);
}
.pathway-num {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: var(--accent-light);
    border: 1.5px solid var(--accent2);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-family: var(--mono);
}
.pathway-text { font-size: 13.5px; color: var(--text); line-height: 1.55; padding-top: 3px; }

/* ─── Mistake items ─── */
.mistake-item {
    background: var(--red-bg);
    border: 1.5px solid var(--red-border);
    border-radius: 8px;
    padding: 11px 16px;
    font-size: 13.5px;
    color: var(--text);
    margin-bottom: 8px;
}

/* ─── Biz cards ─── */
.biz-card {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-sm);
}
.biz-card-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--heading);
    margin-bottom: 13px;
    letter-spacing: -0.1px;
}
.biz-item {
    font-size: 13.5px;
    color: var(--text2);
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    line-height: 1.55;
}
.biz-item:last-child { border-bottom: none; }
.escalation-card { border-color: var(--red-border); }
.upsell-card     { border-color: var(--green-border); }
.recs-card       { border-color: var(--border2); }
.rec-item        { color: var(--text); font-weight: 500; }

/* ─── Email box ─── */
.email-wrap {
    background: var(--bg2);
    border: 1.5px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 20px;
    box-shadow: var(--shadow-md);
}
.email-header {
    background: var(--bg3);
    border-bottom: 1.5px solid var(--border);
    padding: 16px 24px;
}
.email-subject-label {
    font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--subheading); margin-bottom: 5px; font-weight: 700;
}
.email-subject {
    font-size: 15px; font-weight: 700; color: var(--heading);
}
.email-body {
    padding: 24px 26px;
    font-size: 14px;
    color: var(--text);
    line-height: 1.8;
    white-space: pre-wrap;
    font-family: var(--font);
}
.email-copy-hint {
    font-size: 12px; color: var(--text3); padding: 12px 24px;
    border-top: 1px solid var(--border);
    background: var(--bg3);
    font-weight: 500;
}
.email-type-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 15px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 18px;
}

/* ─── Warning / info ─── */
.voc-warning {
    background: var(--amber-bg);
    border: 1.5px solid var(--amber-border);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13.5px;
    color: var(--amber);
    margin-bottom: 20px;
    font-weight: 500;
}

/* ─── Footer ─── */
.voc-footer {
    text-align: center;
    font-size: 12px;
    color: var(--text3);
    padding: 32px 0 16px;
    letter-spacing: 0.05em;
    font-weight: 500;
}

/* ─── Progress bar ─── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent3)) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: var(--bg3) !important;
    border-radius: 99px !important;
    border: 1px solid var(--border) !important;
}

/* ─── Select box ─── */
.stSelectbox > div > div {
    background: var(--bg2) !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: 9px !important;
    color: var(--text) !important;
}

/* ─── File uploader ─── */
[data-testid="stFileUploader"] {
    background: var(--bg2) !important;
    border: 2px dashed var(--border2) !important;
    border-radius: 12px !important;
}

/* ─── New analysis button (secondary) ─── */
.btn-secondary button {
    background: var(--bg2) !important;
    border: 1.5px solid var(--border2) !important;
    color: var(--text2) !important;
    box-shadow: none !important;
}
.btn-secondary button:hover {
    background: var(--bg3) !important;
    color: var(--accent) !important;
    border-color: var(--accent2) !important;
    box-shadow: none !important;
    transform: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────────────────────────
defaults = {
    "stage": "input",
    "transcript": "",
    "analysis": None,
    "active_section": 1,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── API Key ──────────────────────────────────────────────────────────────────
groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
STAGES = [
    (1, "Instant Summary",             "01"),
    (2, "Emotional Intelligence",       "02"),
    (3, "Agent Performance",            "03"),
    (4, "Conversation Intelligence",    "04"),
    (5, "Email Generator",             "05"),
    (6, "AI Coach Mode",               "06"),
]

STAGE_ICONS = {
    1: "⚡", 2: "🧠", 3: "🏆", 4: "💬", 5: "✉️", 6: "🎯"
}

with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-brand-logo">voc<span>AI</span></div>
        <div class="sb-brand-sub">Call Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

    analysis_done = st.session_state.analysis is not None

    if st.session_state.stage in ("results", "analyzing"):
        st.markdown('<div class="sb-section-label">Analysis Stages</div>', unsafe_allow_html=True)

        for num, label, code in STAGES:
            if analysis_done:
                if num < st.session_state.active_section:
                    dot = '<span class="dot dot-done"></span>'
                elif num == st.session_state.active_section:
                    dot = '<span class="dot dot-active"></span>'
                else:
                    dot = '<span class="dot dot-idle"></span>'
            else:
                dot = '<span class="dot dot-idle"></span>'

            btn_label = f"{STAGE_ICONS[num]}  {label}"
            clicked = st.button(btn_label, key=f"nav_{num}", disabled=not analysis_done)
            if clicked:
                st.session_state.active_section = num
                st.rerun()

        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)

    if st.session_state.stage == "results":
        st.markdown('<div class="sb-section-label">Actions</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← New Analysis", key="nav_reset"):
                st.session_state.stage = "input"
                st.session_state.analysis = None
                st.session_state.transcript = ""
                st.session_state.active_section = 1
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    if analysis_done and st.session_state.stage == "results":
        a = st.session_state.analysis
        s1 = a.get("stage1", {})
        resolution = s1.get("resolution", "Unknown")
        color_map = {"Resolved": "#00e5a0", "Unresolved": "#ff4f6d", "Escalated": "#ffb340"}
        col = color_map.get(resolution, "#9097b8")
        st.markdown(f"""
        <div class="sb-info">
            <b>Current Call</b><br>
            {s1.get('issue_type','—')}<br>
            <span style="color:{col}; font-weight:600;">● {resolution}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;">
        <div style="font-size:11px;color:var(--text3);">Powered by Groq · LLaMA</div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def stage_header(num_str, title):
    st.markdown(f"""
    <div class="stage-hdr">
        <span class="stage-num">{num_str}</span>
        <span class="stage-title">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def breadcrumb(active_num):
    crumbs = ""
    for num, label, code in STAGES:
        if num < active_num:
            crumbs += f'<span class="bc-step done">✓ {label}</span><span class="bc-arrow">›</span>'
        elif num == active_num:
            crumbs += f'<span class="bc-step active">{label}</span>'
    st.markdown(f'<div class="breadcrumb">{crumbs}</div>', unsafe_allow_html=True)


def resolution_badge(resolution):
    cls_map = {
        "Resolved": "res-resolved",
        "Unresolved": "res-unresolved",
        "Escalated": "res-escalated",
    }
    cls = cls_map.get(resolution, "res-unresolved")
    return f'<span class="res-badge {cls}">{resolution}</span>'


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT STAGE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "input":

    if not groq_api_key:
        st.markdown("""
        <div class="voc-warning">
            ⚠️ &nbsp; Add your <strong>GROQ_API_KEY</strong> in Streamlit Secrets to enable AI analysis.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
   <div class="input-hero-title">
    vocAI <br>
    <span>From conversations to clarity</span> 
    </div>
    <div class="input-hero-sub">
    Upload an audio file, paste a transcript, or use a sample call. In seconds, vocAI breaks it down into structured insights using a 6-stage AI analysis engine.
    </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📁  Sample Calls", "🎙️  Upload Audio", "📝  Paste Transcript"])

    with tab3:
        transcript_input = st.text_area(
            label="",
            placeholder="Agent: Thank you for calling Support, how can I help you today?\nCustomer: Hi, I've been charged twice for my subscription...\n...",
            height=260,
            key="transcript_paste"
        )
        if st.button("⚡  Run Analysis", key="btn_paste", use_container_width=True):
            if transcript_input.strip():
                st.session_state.transcript = transcript_input.strip()
                st.session_state.stage = "analyzing"
                st.rerun()
            else:
                st.error("Please paste a transcript first.")

    with tab1:
        for idx, sample in enumerate(SAMPLE_CALLS):
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(f"""
                <div class="sample-card">
                    <div class="sample-title">{sample['title']}</div>
                    <div class="sample-meta">{sample.get('type','—')} &nbsp;·&nbsp; {sample.get('duration','—')} &nbsp;·&nbsp; {sample.get('outcome','—')}</div>
                    <div class="sample-preview">{sample.get('preview','')}</div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
                if st.button("Analyze →", key=f"sample_{idx}"):
                    st.session_state.transcript = sample["transcript"]
                    st.session_state.stage = "analyzing"
                    st.rerun()

    with tab2:
        st.markdown('<div style="font-size:13px;color:var(--text2);margin-bottom:14px;">Upload an MP3 or WAV file — transcription powered by Groq Whisper.</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=["mp3", "wav", "m4a"])
        if uploaded:
            if st.button("⚡  Transcribe & Analyze", key="btn_audio", use_container_width=True):
                if groq_api_key:
                    with st.spinner("Transcribing audio with Whisper..."):
                        try:
                            client = Groq(api_key=groq_api_key)
                            transcription = client.audio.transcriptions.create(
                                file=(uploaded.name, uploaded.read(), uploaded.type),
                                model="whisper-large-v3",
                            )
                            st.session_state.transcript = transcription.text
                            st.session_state.stage = "analyzing"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Transcription error: {e}")
                else:
                    st.error("GROQ_API_KEY required for audio transcription.")

# ═══════════════════════════════════════════════════════════════════════════════
# ANALYZING STAGE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "analyzing":

    st.markdown("""
    <div class="analyzing-wrap">
        <div class="analyzing-orb"></div>
        <div class="analyzing-title">Analyzing your call…</div>
        <div class="analyzing-sub">Running 6-stage intelligence pipeline</div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        "📄  Extracting summary & issue classification",
        "😊  Mapping emotional intelligence layer",
        "🧑‍💼  Scoring agent performance",
        "💬  Identifying conversation intelligence",
        "✉️  Preparing email & coaching context",
        "📊  Building business strategy insights",
    ]

    progress_bar = st.progress(0)
    status_text = st.empty()

    if groq_api_key:
        try:
            result = analyze_transcript(
                st.session_state.transcript,
                groq_api_key,
                progress_bar,
                status_text,
                steps
            )
            st.session_state.analysis = result
            st.session_state.stage = "results"
            st.session_state.active_section = 1
            st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            if st.button("← Go back"):
                st.session_state.stage = "input"
                st.rerun()
    else:
        for i, step in enumerate(steps):
            status_text.markdown(f'<div style="font-size:13px;color:var(--text2);text-align:center;margin-top:8px;">{step}</div>', unsafe_allow_html=True)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.4)
        st.warning("No API key found. Please add GROQ_API_KEY to Streamlit Secrets.")
        if st.button("← Go back"):
            st.session_state.stage = "input"
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# RESULTS STAGE
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.stage == "results":

    a  = st.session_state.analysis
    sec = st.session_state.active_section

    breadcrumb(sec)

    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 1 — INSTANT SUMMARY
    # ─────────────────────────────────────────────────────────────────────────
    if sec == 1:
        stage_header("01", "Instant Summary")
        s1 = a.get("stage1", {})

        resolution = s1.get("resolution", "Unknown")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Issue Type</div>
                <div class="metric-value">{s1.get('issue_type', 'N/A')}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Customer Intent</div>
                <div class="metric-value">{s1.get('intent', 'N/A')}</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Resolution</div>
                <div class="metric-value">{resolution_badge(resolution)}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="summary-box">
            <div class="summary-label">Call Summary</div>
            <div class="summary-text">{s1.get('summary', 'No summary available.')}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        if st.button("Continue → Emotional Intelligence"):
            st.session_state.active_section = 2
            st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 2 — EMOTIONAL INTELLIGENCE
    # ─────────────────────────────────────────────────────────────────────────
    elif sec == 2:
        stage_header("02", "Emotional Intelligence")
        s2 = a.get("stage2", {})

        phases = s2.get("sentiment_phases", {})
        emojis = {"Positive": "😊", "Negative": "😠", "Neutral": "😐", "Mixed": "😕"}
        phase_keys = [("beginning", "Beginning"), ("middle", "Middle"), ("end", "End")]

        st.markdown('<div class="subsection-label">Sentiment Journey</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (key, label) in enumerate(phase_keys):
            val = phases.get(key, "N/A")
            with cols[i]:
                st.markdown(f"""
                <div class="phase-card">
                    <div class="phase-label">{label}</div>
                    <div class="phase-emoji">{emojis.get(val, '🔲')}</div>
                    <div class="phase-value">{val}</div>
                </div>""", unsafe_allow_html=True)

        spikes = s2.get("emotion_spikes", [])
        if spikes:
            st.markdown('<div class="subsection-label">⚡ Emotion Spikes Detected</div>', unsafe_allow_html=True)
            emotion_colors = {
                "Anger": "#ff4d6d", "Frustration": "#ffa94d",
                "Confusion": "#748ffc", "Satisfaction": "#00d68f", "Anxiety": "#ffb340"
            }
            for spike in spikes:
                ec = emotion_colors.get(spike.get("emotion", ""), "#9097b8")
                st.markdown(f"""
                <div class="spike-item">
                    <span class="spike-badge" style="background:{ec}22;color:{ec};border-color:{ec}55">{spike.get('emotion','')}</span>
                    <span class="spike-desc">{spike.get('description','')}</span>
                </div>""", unsafe_allow_html=True)

        critical = s2.get("critical_moments", [])
        if critical:
            st.markdown('<div class="subsection-label">⚠️ Critical Moments</div>', unsafe_allow_html=True)
            for moment in critical:
                st.markdown(f'<div class="critical-item">⚠ {moment}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        col_back, col_next = st.columns(2)
        with col_back:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← Summary", key="b2_back"):
                st.session_state.active_section = 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_next:
            if st.button("Continue → Agent Performance", key="b2_next"):
                st.session_state.active_section = 3; st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 3 — AGENT PERFORMANCE
    # ─────────────────────────────────────────────────────────────────────────
    elif sec == 3:
        stage_header("03", "Agent Performance Scorecard")
        s3 = a.get("stage3", {})

        overall = s3.get("overall_score", 0)
        st.markdown(f"""
        <div class="score-hero">
            <div class="score-ring" style="--score:{overall}">
                <div class="score-inner">
                    <div class="score-number">{overall}</div>
                    <div class="score-label">/ 10</div>
                </div>
            </div>
            <div class="score-title">Overall Agent Score</div>
        </div>""", unsafe_allow_html=True)

        sub_scores = [
            ("Communication Clarity",  s3.get("communication_score", 0),    "🗣️"),
            ("Problem-Solving",        s3.get("problem_solving_score", 0),   "🧠"),
            ("Empathy & Tone",         s3.get("empathy_score", 0),           "💙"),
            ("Response Speed",         s3.get("response_speed_score", 0),    "⏱️"),
        ]
        for label, score, icon in sub_scores:
            pct = score * 10
            bar_color = "#00e5a0" if score >= 7 else "#ffb340" if score >= 5 else "#ff4f6d"
            st.markdown(f"""
            <div class="score-bar-row">
                <div class="score-bar-label">{icon} {label}</div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width:{pct}%;background:{bar_color}"></div>
                </div>
                <div class="score-bar-num">{score}/10</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        col_back, col_next = st.columns(2)
        with col_back:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← Emotional Intelligence", key="b3_back"):
                st.session_state.active_section = 2; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_next:
            if st.button("Continue → Conversation Intelligence", key="b3_next"):
                st.session_state.active_section = 4; st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 4 — CONVERSATION INTELLIGENCE
    # ─────────────────────────────────────────────────────────────────────────
    elif sec == 4:
        stage_header("04", "Conversation Intelligence")
        s4 = a.get("stage4", {})

        key_sentences = s4.get("key_customer_sentences", [])
        if key_sentences:
            st.markdown('<div class="subsection-label">💬 Key Customer Statements</div>', unsafe_allow_html=True)
            for sentence in key_sentences:
                st.markdown(f'<div class="quote-block customer-quote">"{sentence}"</div>', unsafe_allow_html=True)

        best  = s4.get("agent_best_reply", "")
        worst = s4.get("agent_worst_reply", "")
        if best:
            st.markdown('<div class="subsection-label">✅ Agent Best Response</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="quote-block best-quote">"{best}"</div>', unsafe_allow_html=True)
        if worst:
            st.markdown('<div class="subsection-label">❌ Agent Weakest Response</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="quote-block worst-quote">"{worst}"</div>', unsafe_allow_html=True)

        critical_moments = s4.get("critical_moments", {})
        if critical_moments:
            st.markdown('<div class="subsection-label">⚡ Critical Call Moments</div>', unsafe_allow_html=True)
            moment_icons  = {"escalation_point": "🔺", "confusion_point": "❓", "resolution_moment": "✅"}
            moment_labels = {"escalation_point": "Escalation Point", "confusion_point": "Confusion Point", "resolution_moment": "Resolution Moment"}
            for key, val in critical_moments.items():
                if val:
                    st.markdown(f"""
                    <div class="moment-item">
                        <span class="moment-icon">{moment_icons.get(key,'📍')}</span>
                        <div>
                            <div class="moment-label">{moment_labels.get(key, key)}</div>
                            <div class="moment-desc">{val}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        col_back, col_next = st.columns(2)
        with col_back:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← Agent Performance", key="b4_back"):
                st.session_state.active_section = 3; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_next:
            if st.button("Continue → Email Generator", key="b4_next"):
                st.session_state.active_section = 5; st.rerun()

    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 5 — AI EMAIL GENERATOR
    # ─────────────────────────────────────────────────────────────────────────
    elif sec == 5:
        stage_header("05", "AI Email Generator")
        s1 = a.get("stage1", {})
        s4 = a.get("stage4", {})

        resolution    = s1.get("resolution", "Unresolved")
        issue_type    = s1.get("issue_type", "your issue")
        summary_text  = s1.get("summary", "")
        intent        = s1.get("intent", "")

        # Extract contextual details from transcript
        transcript_raw = st.session_state.transcript

        # Try to extract customer name
        import re
        customer_name_match = re.search(
            r"(?:customer|client|caller)[:\s]+(?:my name is |i'm |i am )?([A-Z][a-z]+)",
            transcript_raw, re.IGNORECASE
        )
        customer_name = customer_name_match.group(1) if customer_name_match else "Valued Customer"

        # Try to extract ticket / order / account number
        ticket_match = re.search(
            r"(?:ticket|order|case|account|ref(?:erence)?)[:\s#]*([A-Z0-9\-]{4,})",
            transcript_raw, re.IGNORECASE
        )
        ticket_num = ticket_match.group(1) if ticket_match else None

        # Contextual lines from call
        key_statements = s4.get("key_customer_sentences", [])
        primary_concern = key_statements[0] if key_statements else intent

        badge_cfg = {
            "Resolved":   ("✅ Issue Resolved",    "rgba(0,229,160,0.12)",   "#00e5a0"),
            "Unresolved": ("⏳ Follow-Up Required", "rgba(255,179,64,0.12)",  "#ffb340"),
            "Escalated":  ("🔺 Escalation Update",  "rgba(255,79,109,0.12)", "#ff4f6d"),
        }
        badge_label, badge_bg, badge_col = badge_cfg.get(resolution, badge_cfg["Unresolved"])

        st.markdown(f"""
        <div class="email-type-badge" style="background:{badge_bg};color:{badge_col};border:1px solid {badge_col}44;">
            {badge_label}
        </div>
        """, unsafe_allow_html=True)

        # ── Generate email content based on resolution ──────────────────────
        if resolution == "Resolved":
            subject = f"Your {issue_type} has been resolved – Thank you for your patience"
            ticket_line = f"Reference: #{ticket_num}\n" if ticket_num else ""
            body = f"""Hi {customer_name},

Great news — we're happy to confirm that your {issue_type.lower()} has been fully resolved.

{ticket_line}Here's a quick recap of what we addressed:
{summary_text}

We completely understand how frustrating it can be when things don't go as expected, and we sincerely appreciate the patience you showed throughout this process. Our team worked hard to make sure this was handled properly for you.

If you have a moment, we'd love to hear about your experience — your feedback genuinely helps us improve:
👉 [Leave Feedback]

Is there anything else we can help you with? Don't hesitate to reach out — we're always here.

Warm regards,
Support Team"""

        elif resolution == "Escalated":
            subject = f"Important update on your {issue_type} – Escalation in progress"
            ticket_line = f"Reference: #{ticket_num}\n" if ticket_num else ""
            body = f"""Hi {customer_name},

Thank you for bringing this to our attention. I want to personally let you know that your {issue_type.lower()} has been escalated to our specialized team who are best equipped to resolve it.

{ticket_line}Here's where things stand:
{summary_text}

What happens next:
  • A senior specialist has been assigned to your case
  • You will receive a direct update within 24 hours
  • Your case is being treated as high priority

We understand this situation has caused you inconvenience — particularly regarding: "{primary_concern}"

We are committed to making this right for you and will keep you updated every step of the way.

If you need to reach us urgently, please reply to this email with your reference number.

With apologies for the disruption,
Senior Support Team"""

        else:  # Unresolved
            subject = f"We're still working on your {issue_type} – Here's an update"
            ticket_line = f"Reference: #{ticket_num}\n" if ticket_num else ""
            body = f"""Hi {customer_name},

Thank you for reaching out to us. I wanted to make sure you have a clear picture of where things stand with your {issue_type.lower()}.

{ticket_line}Current status:
{summary_text}

We heard you when you mentioned: "{primary_concern}" — and we want you to know this is being actively worked on.

Here's what we're doing right now:
  • Our team is actively investigating the root cause
  • We've flagged this internally with our technical team
  • You can expect a resolution update within 24–48 hours

We know your time is valuable and we're sorry this hasn't been resolved yet. We'll make sure to follow up proactively — you won't need to chase us.

If anything changes or you have more information to share, simply reply to this email.

Thank you for your understanding,
Support Team"""

        # ── Render the email ─────────────────────────────────────────────────
        st.markdown(f"""
        <div class="email-wrap">
            <div class="email-header">
                <div class="email-subject-label">Subject Line</div>
                <div class="email-subject">{subject}</div>
            </div>
            <div class="email-body">{body}</div>
            <div class="email-copy-hint">✦ Review and personalize before sending · Customer name auto-detected from transcript</div>
        </div>
        """, unsafe_allow_html=True)


    # ─────────────────────────────────────────────────────────────────────────
    # STAGE 6 — AI COACH MODE + BUSINESS DASHBOARD
    # ─────────────────────────────────────────────────────────────────────────
    elif sec == 6:
        stage_header("06", "AI Coach Mode")
        s5 = a.get("stage5", {})
        s6 = a.get("stage6", {})

        rewrites = s5.get("response_rewrites", [])
        if rewrites:
            st.markdown('<div class="subsection-label">💡 Suggested Response Rewrites</div>', unsafe_allow_html=True)
            for rw in rewrites:
                st.markdown(f"""
                <div class="rewrite-card">
                    <div class="rewrite-original"><span class="rw-tag orig-tag">ORIGINAL</span>{rw.get('original','')}</div>
                    <div class="rewrite-arrow">↓ Better response</div>
                    <div class="rewrite-better"><span class="rw-tag better-tag">IMPROVED</span>{rw.get('improved','')}</div>
                </div>""", unsafe_allow_html=True)

        ideal_flow = s5.get("ideal_resolution_pathway", [])
        if ideal_flow:
            st.markdown('<div class="subsection-label">🧭 Ideal Resolution Pathway</div>', unsafe_allow_html=True)
            for step_i, step_text in enumerate(ideal_flow, 1):
                st.markdown(f"""
                <div class="pathway-step">
                    <div class="pathway-num">{step_i}</div>
                    <div class="pathway-text">{step_text}</div>
                </div>""", unsafe_allow_html=True)

        mistakes = s5.get("mistake_summary", [])
        if mistakes:
            st.markdown('<div class="subsection-label">📉 Mistake Summary</div>', unsafe_allow_html=True)
            for m in mistakes:
                st.markdown(f'<div class="mistake-item">⚠ {m}</div>', unsafe_allow_html=True)

        # Business dashboard split
        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="subsection-label">📊 Business Dashboard</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            tips = s6.get("coaching_tips", [])
            if tips:
                st.markdown('<div class="biz-card">', unsafe_allow_html=True)
                st.markdown('<div class="biz-card-title">🎓 Coaching Tips</div>', unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f'<div class="biz-item">→ {tip}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            escalation = s6.get("escalation_suggestions", [])
            if escalation:
                st.markdown('<div class="biz-card escalation-card">', unsafe_allow_html=True)
                st.markdown('<div class="biz-card-title">🚨 Escalation Triggers</div>', unsafe_allow_html=True)
                for e in escalation:
                    st.markdown(f'<div class="biz-item">→ {e}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            upsell = s6.get("upsell_opportunities", [])
            if upsell:
                st.markdown('<div class="biz-card upsell-card">', unsafe_allow_html=True)
                st.markdown('<div class="biz-card-title">💰 Upsell / Cross-Sell Opportunities</div>', unsafe_allow_html=True)
                for u in upsell:
                    st.markdown(f'<div class="biz-item">→ {u}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            insights = s6.get("strategic_insights", [])
            if insights:
                st.markdown('<div class="biz-card">', unsafe_allow_html=True)
                st.markdown('<div class="biz-card-title">📊 Strategic Insights</div>', unsafe_allow_html=True)
                for ins in insights:
                    st.markdown(f'<div class="biz-item">→ {ins}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        team_recs = s6.get("ai_recommendations", [])
        if team_recs:
            st.markdown('<div class="biz-card recs-card">', unsafe_allow_html=True)
            st.markdown('<div class="biz-card-title">🧠 AI Recommendations for Teams</div>', unsafe_allow_html=True)
            for rec in team_recs:
                st.markdown(f'<div class="biz-item rec-item">✦ {rec}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("← Email Generator", key="b6_back"):
            st.session_state.active_section = 5; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="voc-footer">
    vocAI · Powered by Groq &amp; LLaMA · Built by Mahitha Bhagavathi
</div>
""", unsafe_allow_html=True)
