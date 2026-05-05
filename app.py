import streamlit as st
import os
from groq import Groq
import time

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="vocAI – Call Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Imports ──────────────────────────────────────────────────────────────────
from sample_calls import SAMPLE_CALLS
from analyzer import analyze_transcript

# ─── Inject Global CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:         #0b0e17;
    --bg2:        #111520;
    --bg3:        #181d2e;
    --border:     #1f2640;
    --border2:    #2a3255;
    --accent:     #6c63ff;
    --accent2:    #8b85ff;
    --accent-glow: rgba(108,99,255,0.18);
    --green:      #00e5a0;
    --red:        #ff4f6d;
    --amber:      #ffb340;
    --blue:       #40a9ff;
    --text:       #e8eaf6;
    --text2:      #9097b8;
    --text3:      #5c6380;
    --font:       'DM Sans', sans-serif;
    --mono:       'DM Mono', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font) !important;
    background: var(--bg) !important;
    color: var(--text) !important;
}

/* ─── Sidebar ─── */
section[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    width: 280px !important;
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
}
.sb-brand-logo {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--text);
}
.sb-brand-logo span { color: var(--accent2); }
.sb-brand-sub {
    font-size: 11px;
    color: var(--text3);
    margin-top: 3px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* ─── Sidebar section label ─── */
.sb-section-label {
    padding: 6px 24px 4px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
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
    font-weight: 400 !important;
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
    background: var(--accent-glow) !important;
    color: var(--text) !important;
}

/* Active nav item override via data hack — rely on class injection */
.nav-active button {
    background: var(--accent-glow) !important;
    color: var(--accent2) !important;
    border-left: 2px solid var(--accent2) !important;
    font-weight: 600 !important;
}

/* ─── Sidebar status dots ─── */
.dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.dot-done  { background: var(--green); }
.dot-active { background: var(--accent2); box-shadow: 0 0 6px var(--accent); }
.dot-idle  { background: var(--border2); }

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
    font-weight: 600;
    color: var(--text);
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
    background: var(--accent-glow);
    border-color: var(--accent);
    color: var(--accent2);
}
.bc-step.done {
    background: rgba(0,229,160,0.08);
    border-color: rgba(0,229,160,0.3);
    color: var(--green);
}
.bc-arrow { color: var(--text3); font-size: 11px; }

/* ─── Input stage cards ─── */
.input-hero {
    text-align: center;
    padding: 48px 24px 36px;
}
.input-hero-title {
    font-size: 36px;
    font-weight: 700;
    letter-spacing: -1px;
    color: var(--text);
    line-height: 1.2;
}
.input-hero-title span { color: var(--accent2); }
.input-hero-sub {
    font-size: 15px;
    color: var(--text2);
    margin-top: 12px;
    max-width: 500px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.6;
}

/* ─── Tabs ─── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg2) !important;
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
    background: var(--bg3) !important;
    color: var(--text) !important;
    border: 1px solid var(--border2) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    padding: 24px 0 0 0 !important;
}

/* ─── Text area ─── */
.stTextArea textarea {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ─── Buttons ─── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    font-family: var(--font) !important;
    letter-spacing: 0 !important;
    transition: all 0.18s ease !important;
    box-shadow: 0 4px 16px rgba(108,99,255,0.25) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(108,99,255,0.4) !important;
    background: var(--accent2) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Sample card ─── */
.sample-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
    transition: border-color 0.2s, transform 0.2s;
    cursor: default;
}
.sample-card:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
}
.sample-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 5px;
}
.sample-meta {
    font-size: 11.5px;
    color: var(--text3);
    margin-bottom: 8px;
    letter-spacing: 0.02em;
}
.sample-preview {
    font-size: 13px;
    color: var(--text2);
    font-style: italic;
    line-height: 1.5;
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
    width: 72px; height: 72px;
    border-radius: 50%;
    background: var(--accent-glow);
    border: 2px solid var(--accent);
    margin-bottom: 28px;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 var(--accent-glow); }
    50% { transform: scale(1.1); box-shadow: 0 0 0 14px transparent; }
}
.analyzing-title {
    font-size: 22px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
}
.analyzing-sub { font-size: 13px; color: var(--text2); margin-bottom: 32px; }

/* ─── Stage header ─── */
.stage-hdr {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 0 0 24px 0;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}
.stage-num {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--accent2);
    font-family: var(--mono);
    background: var(--accent-glow);
    border: 1px solid rgba(108,99,255,0.3);
    padding: 3px 9px;
    border-radius: 6px;
}
.stage-title {
    font-size: 19px;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.2px;
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
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
}
.metric-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 8px;
}
.metric-value {
    font-size: 17px;
    font-weight: 600;
    color: var(--text);
    line-height: 1.2;
}

/* ─── Summary box ─── */
.summary-box {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 6px;
}
.summary-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 10px;
}
.summary-text {
    font-size: 14.5px;
    color: var(--text);
    line-height: 1.7;
}

/* ─── Resolution badge ─── */
.res-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 99px;
    letter-spacing: 0.04em;
}
.res-resolved { background: rgba(0,229,160,0.12); color: var(--green); border: 1px solid rgba(0,229,160,0.3); }
.res-unresolved { background: rgba(255,79,109,0.12); color: var(--red); border: 1px solid rgba(255,79,109,0.3); }
.res-escalated { background: rgba(255,179,64,0.12); color: var(--amber); border: 1px solid rgba(255,179,64,0.3); }

/* ─── Expander ─── */
details {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0 !important;
    margin-bottom: 12px !important;
}
details summary {
    padding: 16px 20px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text) !important;
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
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
}
.phase-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text3); margin-bottom: 10px; font-weight: 600; }
.phase-emoji { font-size: 26px; margin-bottom: 6px; }
.phase-value { font-size: 13px; font-weight: 600; color: var(--text); }

/* ─── Spike items ─── */
.subsection-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text3);
    margin: 18px 0 10px 0;
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
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    border: 1px solid;
    white-space: nowrap;
    flex-shrink: 0;
}
.spike-desc { font-size: 13.5px; color: var(--text); line-height: 1.5; }
.critical-item {
    background: rgba(255,179,64,0.07);
    border: 1px solid rgba(255,179,64,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13.5px;
    color: var(--amber);
    margin-bottom: 8px;
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
.score-number { font-size: 26px; font-weight: 700; color: var(--text); line-height: 1; }
.score-label { font-size: 11px; color: var(--text3); }
.score-title { font-size: 13px; color: var(--text2); font-weight: 500; }

/* ─── Score bars ─── */
.score-bar-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 12px;
}
.score-bar-label {
    width: 170px;
    font-size: 13px;
    color: var(--text2);
    flex-shrink: 0;
}
.score-bar-track {
    flex: 1;
    height: 6px;
    background: var(--bg3);
    border-radius: 99px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.score-bar-num {
    font-size: 12px;
    font-family: var(--mono);
    color: var(--text2);
    width: 36px;
    text-align: right;
    flex-shrink: 0;
}

/* ─── Quote blocks ─── */
.quote-block {
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 10px;
    font-style: italic;
}
.customer-quote {
    background: var(--bg3);
    border-left: 3px solid var(--blue);
    color: var(--text);
}
.best-quote {
    background: rgba(0,229,160,0.07);
    border-left: 3px solid var(--green);
    color: var(--text);
}
.worst-quote {
    background: rgba(255,79,109,0.07);
    border-left: 3px solid var(--red);
    color: var(--text);
}

/* ─── Critical moments ─── */
.moment-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 10px;
}
.moment-icon { font-size: 20px; flex-shrink: 0; }
.moment-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em; color: var(--text3); margin-bottom: 4px; font-weight: 600; }
.moment-desc { font-size: 13.5px; color: var(--text); line-height: 1.5; }

/* ─── Rewrite cards ─── */
.rewrite-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.rewrite-original {
    font-size: 13.5px;
    color: var(--text2);
    line-height: 1.5;
    margin-bottom: 10px;
}
.rewrite-arrow {
    font-size: 12px;
    font-weight: 600;
    color: var(--accent2);
    letter-spacing: 0.05em;
    margin-bottom: 10px;
}
.rewrite-better {
    font-size: 13.5px;
    color: var(--green);
    line-height: 1.5;
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
.orig-tag { background: rgba(255,79,109,0.15); color: var(--red); }
.better-tag { background: rgba(0,229,160,0.12); color: var(--green); }

/* ─── Pathway steps ─── */
.pathway-step {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 13px 0;
    border-bottom: 1px solid var(--border);
}
.pathway-num {
    width: 26px; height: 26px;
    border-radius: 50%;
    background: var(--accent-glow);
    border: 1px solid var(--accent);
    color: var(--accent2);
    font-size: 11px;
    font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-family: var(--mono);
}
.pathway-text { font-size: 13.5px; color: var(--text); line-height: 1.5; padding-top: 2px; }

/* ─── Mistake items ─── */
.mistake-item {
    background: rgba(255,79,109,0.06);
    border: 1px solid rgba(255,79,109,0.18);
    border-radius: 8px;
    padding: 11px 16px;
    font-size: 13.5px;
    color: var(--text);
    margin-bottom: 8px;
}

/* ─── Biz cards ─── */
.biz-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.biz-card-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 12px;
    letter-spacing: -0.1px;
}
.biz-item {
    font-size: 13.5px;
    color: var(--text2);
    padding: 7px 0;
    border-bottom: 1px solid var(--border);
    line-height: 1.5;
}
.biz-item:last-child { border-bottom: none; }
.escalation-card { border-color: rgba(255,79,109,0.25); }
.upsell-card { border-color: rgba(0,229,160,0.2); }
.recs-card { border-color: rgba(108,99,255,0.3); }
.rec-item { color: var(--text); }

/* ─── Email box ─── */
.email-wrap {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 20px;
}
.email-header {
    background: var(--bg3);
    border-bottom: 1px solid var(--border);
    padding: 16px 24px;
}
.email-subject-label {
    font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text3); margin-bottom: 5px; font-weight: 600;
}
.email-subject {
    font-size: 15px; font-weight: 600; color: var(--text);
}
.email-body {
    padding: 22px 24px;
    font-size: 14px;
    color: var(--text);
    line-height: 1.75;
    white-space: pre-wrap;
    font-family: var(--font);
}
.email-copy-hint {
    font-size: 12px; color: var(--text3); padding: 12px 24px;
    border-top: 1px solid var(--border);
    background: var(--bg3);
}
.email-type-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 18px;
}

/* ─── Warning / info ─── */
.voc-warning {
    background: rgba(255,179,64,0.08);
    border: 1px solid rgba(255,179,64,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13.5px;
    color: var(--amber);
    margin-bottom: 20px;
}

/* ─── Footer ─── */
.voc-footer {
    text-align: center;
    font-size: 12px;
    color: var(--text3);
    padding: 32px 0 16px;
    letter-spacing: 0.04em;
}

/* ─── Progress bar ─── */
.stProgress > div > div {
    background: var(--accent) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: var(--bg3) !important;
    border-radius: 99px !important;
}

/* ─── Select box ─── */
.stSelectbox > div > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 9px !important;
    color: var(--text) !important;
}

/* ─── File uploader ─── */
[data-testid="stFileUploader"] {
    background: var(--bg2) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: 12px !important;
}

/* ─── New analysis button (secondary) ─── */
.btn-secondary button {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    color: var(--text2) !important;
    box-shadow: none !important;
}
.btn-secondary button:hover {
    background: var(--bg2) !important;
    color: var(--text) !important;
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
    1: "📄", 2: "😊", 3: "🧑‍💼", 4: "💬", 5: "✉️", 6: "🧠"
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
    <div class="input-hero">
        <div class="input-hero-title">Turn calls into<br><span>actionable intelligence</span></div>
        <div class="input-hero-sub">
            Paste a transcript, pick a demo, or upload audio — vocAI handles the rest
            with a 6-stage AI analysis pipeline.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📝  Paste Transcript", "📁  Sample Calls", "🎙️  Upload Audio"])

    with tab1:
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

    with tab2:
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

    with tab3:
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

        # Copyable version
        with st.expander("📋  Copy raw email text"):
            st.code(f"Subject: {subject}\n\n{body}", language=None)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        col_back, col_next = st.columns(2)
        with col_back:
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← Conversation Intelligence", key="b5_back"):
                st.session_state.active_section = 4; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_next:
            if st.button("Continue → AI Coach", key="b5_next"):
                st.session_state.active_section = 6; st.rerun()

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
    vocAI · Powered by Groq &amp; LLaMA · Built for Customer Excellence
</div>
""", unsafe_allow_html=True)
