"""
vocAI  —  Call Intelligence Platform
All 12 spec requirements implemented:
1.  Sidebar fully functional, CSS-driven, never stuck
2.  Landing: vocAI top-left bold, centered hero hierarchy
3.  Loading orb: filled purple gradient, glowing pulse animation
4.  Navigation: free movement between all 6 stages post-analysis
5.  Breadcrumb: past ✓ / active / upcoming (faded) all visible
6.  Email: correct agent vs customer (extracted by LLM)
7.  Subject: standard format company + order number
8.  Email body: standard opening with order reference
9.  Personalisation: customer name, product, emotion, complaint
10. Anti-hallucination: {{placeholders}} for any missing detail
11. Next steps: always structured section in email + coach view
12. Closing: empathy line, support availability, agent signature
"""

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
    "📄  Extracting summary & classification",
    "😊  Mapping emotional intelligence",
    "🧑‍💼  Scoring agent performance",
    "💬  Identifying conversation patterns",
    "✉️  Preparing email & coaching context",
    "📊  Building strategic insights",
]
SENTIMENT_EMOJI = {"Positive":"😊","Negative":"😠","Neutral":"😐","Mixed":"😕"}
EMOTION_COLORS  = {
    "Anger":"#ff4d6d","Frustration":"#ffa94d",
    "Confusion":"#748ffc","Satisfaction":"#00d68f","Anxiety":"#ffb340",
}

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800&family=JetBrains+Mono:wght@400;500&display=swap');
:root{
--bg:#f7f6fb;--bg2:#ffffff;--bg3:#f0eef8;
--border:#e2ddf2;--border2:#ccc6e8;
--accent:#5b3fce;--accent2:#7c5fe6;--accent3:#9d7ff5;
--accent-light:rgba(91,63,206,0.08);--accent-glow:rgba(91,63,206,0.20);
--heading:#2d1b69;--subheading:#5b3fce;
--green:#0e9e6e;--green-bg:rgba(14,158,110,0.08);--green-border:rgba(14,158,110,0.25);
--red:#d63f5a;--red-bg:rgba(214,63,90,0.07);--red-border:rgba(214,63,90,0.22);
--amber:#c47e0a;--amber-bg:rgba(196,126,10,0.08);--amber-border:rgba(196,126,10,0.25);
--blue:#2563a8;--blue-bg:rgba(37,99,168,0.08);
--text:#1a1228;--text2:#4a4060;--text3:#8878aa;
--font:'Plus Jakarta Sans',sans-serif;--mono:'JetBrains Mono',monospace;
--shadow-sm:0 1px 4px rgba(91,63,206,0.08);
--shadow-md:0 4px 16px rgba(91,63,206,0.12);
--shadow-lg:0 8px 32px rgba(91,63,206,0.16);
}
html,body,[class*="css"]{font-family:var(--font)!important;background:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden!important;}
[data-testid="stDecoration"],[data-testid="stToolbar"]{display:none!important;}
.main .block-container{padding:2.2rem 2.8rem 5rem 2.8rem!important;max-width:1060px!important;}

/* Sidebar */
section[data-testid="stSidebar"]{background:#ffffff!important;border-right:1px solid var(--border)!important;width:268px!important;min-width:268px!important;box-shadow:2px 0 16px rgba(91,63,206,0.07)!important;}
section[data-testid="stSidebar"]>div{padding:0!important;}
.sb-brand{padding:24px 22px 18px;border-bottom:1px solid var(--border);background:linear-gradient(135deg,#f0eef8 0%,#fff 100%);}
.sb-brand-logo{font-size:21px;font-weight:800;letter-spacing:-0.5px;color:var(--heading);}
.sb-brand-logo span{color:var(--accent2);}
.sb-brand-sub{font-size:10px;color:var(--text3);margin-top:5px;letter-spacing:.07em;text-transform:uppercase;font-weight:600;}
.sb-section-label{padding:14px 22px 6px;font-size:9.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text3);}
.sb-divider{height:1px;background:var(--border);margin:8px 16px;}
.sb-info{margin:14px 16px;padding:13px 15px;background:var(--bg3);border:1px solid var(--border);border-radius:10px;font-size:12px;color:var(--text2);line-height:1.65;}
.sb-info b{color:var(--text);}
.dot{width:7px;height:7px;border-radius:50%;display:inline-block;flex-shrink:0;}
.dot-done{background:var(--green);}
.dot-active{background:var(--accent2);box-shadow:0 0 0 3px rgba(124,95,230,.25);}
.dot-idle{background:var(--border2);}

/* Sidebar buttons */
section[data-testid="stSidebar"] .stButton>button{
width:100%!important;text-align:left!important;background:transparent!important;
border:none!important;border-radius:0!important;padding:10px 22px!important;
font-size:13.5px!important;font-weight:500!important;color:var(--text2)!important;
cursor:pointer!important;transition:all .14s ease!important;box-shadow:none!important;
letter-spacing:0!important;justify-content:flex-start!important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:var(--accent-light)!important;color:var(--accent)!important;transform:none!important;}
.nav-active button{background:var(--accent-light)!important;color:var(--accent)!important;font-weight:700!important;border-left:3px solid var(--accent)!important;padding-left:19px!important;}

/* Secondary button */
.btn-secondary .stButton>button{
background:var(--bg3)!important;border:1.5px solid var(--border2)!important;
color:var(--text2)!important;box-shadow:none!important;border-radius:9px!important;
margin:0 16px!important;width:calc(100% - 32px)!important;font-size:13px!important;}
.btn-secondary .stButton>button:hover{background:var(--bg2)!important;color:var(--accent)!important;border-color:var(--accent2)!important;transform:none!important;box-shadow:none!important;}

/* Main CTA buttons */
.main .stButton>button{
background:var(--accent)!important;color:#fff!important;border:none!important;
border-radius:9px!important;font-weight:600!important;font-size:14px!important;
padding:10px 24px!important;font-family:var(--font)!important;letter-spacing:0!important;
transition:all .18s ease!important;box-shadow:0 3px 14px rgba(91,63,206,.30)!important;}
.main .stButton>button:hover{transform:translateY(-1px)!important;box-shadow:0 6px 22px rgba(91,63,206,.40)!important;background:var(--accent2)!important;}

/* Progress bar */
.stProgress>div>div{background:linear-gradient(90deg,var(--accent),var(--accent3))!important;border-radius:99px!important;}
.stProgress>div{background:var(--bg3)!important;border-radius:99px!important;border:1px solid var(--border)!important;height:7px!important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:var(--bg3)!important;border-radius:10px!important;padding:4px!important;border:1px solid var(--border)!important;gap:2px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--text2)!important;border-radius:8px!important;font-size:13.5px!important;font-weight:500!important;padding:8px 20px!important;font-family:var(--font)!important;}
.stTabs [aria-selected="true"]{background:var(--bg2)!important;color:var(--accent)!important;border:1px solid var(--border2)!important;font-weight:700!important;box-shadow:var(--shadow-sm)!important;}
.stTabs [data-baseweb="tab-panel"]{padding:24px 0 0 0!important;}

/* Text area */
.stTextArea textarea{background:var(--bg2)!important;border:1.5px solid var(--border2)!important;border-radius:10px!important;color:var(--text)!important;font-family:var(--mono)!important;font-size:13px!important;line-height:1.65!important;}
.stTextArea textarea:focus{border-color:var(--accent)!important;box-shadow:0 0 0 3px var(--accent-glow)!important;}
.stTextArea textarea::placeholder{color:var(--text3)!important;}
.stSelectbox>div>div{background:var(--bg2)!important;border:1.5px solid var(--border2)!important;border-radius:9px!important;}
[data-testid="stFileUploader"]{background:var(--bg2)!important;border:2px dashed var(--border2)!important;border-radius:12px!important;}

/* Breadcrumb */
.breadcrumb{display:flex;gap:5px;align-items:center;flex-wrap:wrap;margin-bottom:24px;}
.bc-step{font-size:11px;padding:4px 11px;border-radius:99px;border:1px solid var(--border2);color:var(--text3);background:var(--bg2);font-weight:500;}
.bc-step.active{background:var(--accent-light);border-color:var(--accent);color:var(--accent);font-weight:700;}
.bc-step.done{background:var(--green-bg);border-color:var(--green-border);color:var(--green);font-weight:600;}
.bc-step.upcoming{opacity:.42;}
.bc-arrow{color:var(--text3);font-size:10px;margin:0 1px;}

/* Stage header */
.stage-hdr{display:flex;align-items:center;gap:14px;margin:0 0 22px;padding-bottom:16px;border-bottom:2px solid var(--border);}
.stage-num{font-size:10px;font-weight:700;letter-spacing:.12em;color:var(--accent);font-family:var(--mono);background:var(--accent-light);border:1.5px solid var(--border2);padding:3px 10px;border-radius:6px;text-transform:uppercase;}
.stage-title{font-size:20px;font-weight:700;color:var(--heading);letter-spacing:-.3px;}

/* Metric card */
.metric-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:18px 20px;box-shadow:var(--shadow-sm);}
.metric-label{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text3);margin-bottom:9px;}
.metric-value{font-size:16px;font-weight:700;color:var(--text);line-height:1.25;}

/* Summary box */
.summary-box{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:22px 26px;margin-top:8px;box-shadow:var(--shadow-sm);}
.summary-label{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--subheading);margin-bottom:11px;}
.summary-text{font-size:14.5px;color:var(--text);line-height:1.75;}

/* Resolution badge */
.res-badge{display:inline-block;font-size:12px;font-weight:700;padding:4px 13px;border-radius:99px;letter-spacing:.03em;}
.res-resolved{background:var(--green-bg);color:var(--green);border:1.5px solid var(--green-border);}
.res-unresolved{background:var(--red-bg);color:var(--red);border:1.5px solid var(--red-border);}
.res-escalated{background:var(--amber-bg);color:var(--amber);border:1.5px solid var(--amber-border);}
.res-inprogress{background:var(--blue-bg);color:var(--blue);border:1.5px solid rgba(37,99,168,.25);}

/* Phase card */
.phase-card{background:var(--bg3);border:1.5px solid var(--border);border-radius:10px;padding:18px;text-align:center;}
.phase-label{font-size:10px;text-transform:uppercase;letter-spacing:.09em;color:var(--subheading);margin-bottom:10px;font-weight:700;}
.phase-emoji{font-size:28px;margin-bottom:6px;}
.phase-value{font-size:13px;font-weight:700;color:var(--text);}

/* Emotion spike */
.spike-item{display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--border);}
.spike-badge{font-size:11px;font-weight:700;padding:3px 10px;border-radius:99px;border:1.5px solid;white-space:nowrap;flex-shrink:0;}
.spike-desc{font-size:13.5px;color:var(--text);line-height:1.55;}
.critical-item{background:var(--amber-bg);border:1.5px solid var(--amber-border);border-radius:8px;padding:11px 15px;font-size:13.5px;color:var(--amber);margin-bottom:8px;font-weight:500;}

/* Score ring */
.score-hero{display:flex;flex-direction:column;align-items:center;padding:20px 0 24px;}
.score-ring{width:108px;height:108px;border-radius:50%;background:conic-gradient(var(--accent) calc(var(--score)*36deg),var(--bg3) 0deg);display:flex;align-items:center;justify-content:center;margin-bottom:12px;box-shadow:var(--shadow-md);}
.score-inner{width:82px;height:82px;border-radius:50%;background:var(--bg2);display:flex;flex-direction:column;align-items:center;justify-content:center;}
.score-number{font-size:26px;font-weight:800;color:var(--heading);line-height:1;}
.score-label{font-size:11px;color:var(--text3);font-weight:500;}
.score-title{font-size:13px;color:var(--text2);font-weight:600;}
.score-bar-row{display:flex;align-items:center;gap:14px;margin-bottom:13px;}
.score-bar-label{width:170px;font-size:13px;color:var(--text2);flex-shrink:0;font-weight:500;}
.score-bar-track{flex:1;height:7px;background:var(--bg3);border-radius:99px;overflow:hidden;border:1px solid var(--border);}
.score-bar-fill{height:100%;border-radius:99px;transition:width .6s ease;}
.score-bar-num{font-size:12px;font-family:var(--mono);color:var(--text);font-weight:600;width:36px;text-align:right;flex-shrink:0;}

/* Quotes */
.quote-block{border-radius:10px;padding:14px 18px;font-size:14px;line-height:1.65;margin-bottom:10px;font-style:italic;}
.customer-quote{background:var(--blue-bg);border-left:3px solid var(--blue);color:var(--text);}
.best-quote{background:var(--green-bg);border-left:3px solid var(--green);color:var(--text);}
.worst-quote{background:var(--red-bg);border-left:3px solid var(--red);color:var(--text);}

/* Critical moments */
.moment-item{display:flex;align-items:flex-start;gap:14px;padding:15px;background:var(--bg3);border:1.5px solid var(--border);border-radius:10px;margin-bottom:10px;}
.moment-icon{font-size:20px;flex-shrink:0;}
.moment-label{font-size:10px;text-transform:uppercase;letter-spacing:.08em;color:var(--subheading);margin-bottom:5px;font-weight:700;}
.moment-desc{font-size:13.5px;color:var(--text);line-height:1.55;}

/* Rewrites */
.rewrite-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:14px;box-shadow:var(--shadow-sm);}
.rewrite-original{font-size:13.5px;color:var(--text2);line-height:1.55;margin-bottom:12px;}
.rewrite-arrow{font-size:12px;font-weight:700;color:var(--subheading);letter-spacing:.05em;margin-bottom:12px;}
.rewrite-better{font-size:13.5px;color:var(--green);line-height:1.55;font-weight:500;}
.rw-tag{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.1em;padding:2px 8px;border-radius:4px;margin-right:8px;vertical-align:middle;}
.orig-tag{background:var(--red-bg);color:var(--red);}
.better-tag{background:var(--green-bg);color:var(--green);}

/* Pathway */
.pathway-step{display:flex;align-items:flex-start;gap:14px;padding:14px 0;border-bottom:1px solid var(--border);}
.pathway-num{width:28px;height:28px;border-radius:50%;background:var(--accent-light);border:1.5px solid var(--accent2);color:var(--accent);font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-family:var(--mono);}
.pathway-text{font-size:13.5px;color:var(--text);line-height:1.55;padding-top:3px;}
.mistake-item{background:var(--red-bg);border:1.5px solid var(--red-border);border-radius:8px;padding:11px 16px;font-size:13.5px;color:var(--text);margin-bottom:8px;}
.next-step-item{background:var(--accent-light);border:1.5px solid var(--border2);border-radius:8px;padding:11px 16px;font-size:13.5px;color:var(--accent);margin-bottom:8px;font-weight:500;}

/* Biz cards */
.biz-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:14px;box-shadow:var(--shadow-sm);}
.biz-card-title{font-size:13px;font-weight:700;color:var(--heading);margin-bottom:13px;}
.biz-item{font-size:13.5px;color:var(--text2);padding:8px 0;border-bottom:1px solid var(--border);line-height:1.55;}
.biz-item:last-child{border-bottom:none;}
.escalation-card{border-color:var(--red-border);}
.upsell-card{border-color:var(--green-border);}

/* Email */
.email-wrap{background:var(--bg2);border:1.5px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:20px;box-shadow:var(--shadow-md);}
.email-header{background:var(--bg3);border-bottom:1.5px solid var(--border);padding:16px 24px;}
.email-subject-label{font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:var(--subheading);margin-bottom:5px;font-weight:700;}
.email-subject{font-size:15px;font-weight:700;color:var(--heading);}
.email-body{padding:24px 26px;font-size:14px;color:var(--text);line-height:1.85;white-space:pre-wrap;font-family:var(--font);}
.email-footer{font-size:12px;color:var(--text3);padding:12px 24px;border-top:1px solid var(--border);background:var(--bg3);}
.email-type-badge{display:inline-flex;align-items:center;gap:8px;padding:6px 15px;border-radius:99px;font-size:12px;font-weight:700;margin-bottom:18px;}

/* Sample cards */
.sample-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:18px 20px;margin-bottom:12px;transition:border-color .2s,box-shadow .2s,transform .18s;}
.sample-card:hover{border-color:var(--accent2);box-shadow:var(--shadow-md);transform:translateY(-1px);}
.sample-title{font-size:15px;font-weight:700;color:var(--heading);margin-bottom:5px;}
.sample-meta{font-size:11.5px;color:var(--text3);margin-bottom:8px;letter-spacing:.02em;font-weight:500;}
.sample-preview{font-size:13px;color:var(--text2);font-style:italic;line-height:1.55;}

/* Subsection label */
.subsection-label{font-size:11px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:var(--subheading);margin:20px 0 10px;}

/* Warning */
.voc-warning{background:var(--amber-bg);border:1.5px solid var(--amber-border);border-radius:10px;padding:14px 18px;font-size:13.5px;color:var(--amber);margin-bottom:20px;font-weight:500;}

/* ── Loading orb: filled, glowing, animated purple gradient ── */
@keyframes orbPulse{
0%{transform:scale(1);box-shadow:0 0 0 0 rgba(91,63,206,.55),0 0 32px 8px rgba(124,95,230,.30);}
50%{transform:scale(1.11);box-shadow:0 0 0 20px rgba(91,63,206,0),0 0 52px 18px rgba(157,127,245,.45);}
100%{transform:scale(1);box-shadow:0 0 0 0 rgba(91,63,206,.55),0 0 32px 8px rgba(124,95,230,.30);}
}
@keyframes orbGradient{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}
.analyzing-orb{
width:84px;height:84px;border-radius:50%;
background:linear-gradient(135deg,#4c30c8 0%,#7c5fe6 30%,#9d7ff5 55%,#5b3fce 80%,#4c30c8 100%);
background-size:300% 300%;
animation:orbPulse 2s ease-in-out infinite,orbGradient 3s ease infinite;
margin-bottom:28px;
}
.analyzing-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 24px;text-align:center;}
.analyzing-title{font-size:23px;font-weight:700;color:var(--heading);margin-bottom:6px;letter-spacing:-.3px;}
.analyzing-sub{font-size:14px;color:var(--text2);margin-bottom:32px;}

/* Footer */
.voc-footer{text-align:center;font-size:12px;color:var(--text3);padding:32px 0 16px;letter-spacing:.05em;font-weight:500;}
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────
def _v(d, *keys, default="—"):
    for k in keys:
        if not isinstance(d, dict): return default
        d = d.get(k)
        if d is None: return default
    return str(d) if d not in ("", None) else default

def stage_header(code, title):
    st.markdown(f'<div class="stage-hdr"><span class="stage-num">{code}</span><span class="stage-title">{title}</span></div>', unsafe_allow_html=True)

def breadcrumb(active):
    crumbs = ""
    for num, label, _, _ in STAGES:
        if num < active:
            crumbs += f'<span class="bc-step done">✓ {label}</span><span class="bc-arrow">›</span>'
        elif num == active:
            crumbs += f'<span class="bc-step active">{label}</span>'
        else:
            crumbs += f'<span class="bc-arrow">›</span><span class="bc-step upcoming">{label}</span>'
    st.markdown(f'<div class="breadcrumb">{crumbs}</div>', unsafe_allow_html=True)

def res_badge(res):
    cls = {"Resolved":"res-resolved","Unresolved":"res-unresolved","Escalated":"res-escalated"}.get(res,"res-inprogress")
    return f'<span class="res-badge {cls}">{res}</span>'

def nav_btn(num, label, icon, enabled):
    active = st.session_state.active_section == num
    if active: st.markdown('<div class="nav-active">', unsafe_allow_html=True)
    clicked = st.button(f"{icon}  {label}", key=f"nav_{num}", disabled=not enabled)
    if active: st.markdown('</div>', unsafe_allow_html=True)
    if clicked and enabled:
        st.session_state.active_section = num
        st.rerun()

def back_next(back_sec, back_label, next_sec, next_label, back_key, next_key):
    bc, bn = st.columns(2)
    with bc:
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button(f"← {back_label}", key=back_key):
            st.session_state.active_section = back_sec; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with bn:
        if st.button(f"Continue → {next_label}", key=next_key):
            st.session_state.active_section = next_sec; st.rerun()


# ── Sidebar ──────────────────────────────────────────────────
def render_sidebar():
    analysis_done = st.session_state.analysis is not None
    in_results    = st.session_state.stage in ("results","analyzing")
    with st.sidebar:
        st.markdown('<div class="sb-brand"><div class="sb-brand-logo">voc<span>AI</span></div><div class="sb-brand-sub">Call Intelligence Platform</div></div>', unsafe_allow_html=True)
        if in_results:
            st.markdown('<div class="sb-section-label">Analysis Stages</div>', unsafe_allow_html=True)
            for num, label, _, icon in STAGES:
                nav_btn(num, label, icon, enabled=analysis_done)
            st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        if st.session_state.stage == "results":
            st.markdown('<div class="sb-section-label">Actions</div>', unsafe_allow_html=True)
            st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
            if st.button("← New Analysis", key="nav_reset"):
                for k,v in DEFAULTS.items(): st.session_state[k]=v
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        if analysis_done and in_results:
            s1  = st.session_state.analysis.get("stage1",{})
            res = s1.get("resolution","—")
            col = {"Resolved":"#0e9e6e","Unresolved":"#d63f5a","Escalated":"#c47e0a"}.get(res,"#8878aa")
            st.markdown(f'<div class="sb-info"><b>Current call</b><br>{s1.get("issue_type","—")}<br><span style="color:{col};font-weight:700;">● {res}</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:16px 22px 0;font-size:11px;color:var(--text3);">Powered by Groq · LLaMA 3.3</div>', unsafe_allow_html=True)


# ── Stage 1 ──────────────────────────────────────────────────
def render_stage1(a):
    stage_header("01","Instant Summary")
    s1  = a.get("stage1",{})
    res = s1.get("resolution","Unresolved")
    c1,c2,c3 = st.columns(3)
    for col,lbl,val in [(c1,"Issue Type",s1.get("issue_type","—")),(c2,"Customer Intent",s1.get("intent","—")),(c3,"Resolution",res_badge(res))]:
        with col: st.markdown(f'<div class="metric-card"><div class="metric-label">{lbl}</div><div class="metric-value">{val}</div></div>', unsafe_allow_html=True)

    ctx = [("👤 Customer",s1.get("customer_name")),("🧑‍💼 Agent",s1.get("agent_name")),("📦 Order",s1.get("order_number")),("🛍 Product",s1.get("product_mentioned")),("🏢 Company",s1.get("company_name")),("😤 Emotion",s1.get("customer_emotion"))]
    chips=""
    for lbl,val in ctx:
        v = val if val and str(val) not in ("null","None","") else "{{not detected}}"
        clr="var(--heading)" if not str(v).startswith("{{") else "#8878aa"
        chips+=f'<span style="background:var(--bg3);border:1px solid var(--border2);border-radius:6px;padding:4px 11px;font-size:12px;color:var(--text2);margin-right:6px;margin-bottom:6px;display:inline-block;"><b style="color:{clr};">{lbl}</b> {v}</span>'
    st.markdown(f'<div style="margin:14px 0 4px;line-height:2.4;">{chips}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-box"><div class="summary-label">Call Summary</div><div class="summary-text">{s1.get("summary","No summary available.")}</div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    if st.button("Continue → Emotional Intelligence", key="s1_next"):
        st.session_state.active_section=2; st.rerun()


# ── Stage 2 ──────────────────────────────────────────────────
def render_stage2(a):
    stage_header("02","Emotional Intelligence")
    s2 = a.get("stage2",{})
    phases = s2.get("sentiment_phases",{})
    st.markdown('<div class="subsection-label">Sentiment Journey</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i,(key,label) in enumerate([("beginning","Beginning"),("middle","Middle"),("end","End")]):
        val = phases.get(key,"N/A")
        with cols[i]:
            st.markdown(f'<div class="phase-card"><div class="phase-label">{label}</div><div class="phase-emoji">{SENTIMENT_EMOJI.get(val,"🔲")}</div><div class="phase-value">{val}</div></div>', unsafe_allow_html=True)
    for spike in s2.get("emotion_spikes",[]):
        ec = EMOTION_COLORS.get(spike.get("emotion",""),"#8878aa")
        st.markdown(f'<div class="spike-item"><span class="spike-badge" style="background:{ec}22;color:{ec};border-color:{ec}55">{spike.get("emotion","")}</span><span class="spike-desc">{spike.get("description","")}</span></div>', unsafe_allow_html=True)
    for moment in s2.get("critical_moments",[]):
        st.markdown(f'<div class="critical-item">⚠ {moment}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    back_next(1,"Summary",3,"Agent Performance","s2_back","s2_next")


# ── Stage 3 ──────────────────────────────────────────────────
def render_stage3(a):
    stage_header("03","Agent Performance Scorecard")
    s3 = a.get("stage3",{})
    overall = s3.get("overall_score",0)
    st.markdown(f'<div class="score-hero"><div class="score-ring" style="--score:{overall}"><div class="score-inner"><div class="score-number">{overall}</div><div class="score-label">/ 10</div></div></div><div class="score-title">Overall Agent Score</div></div>', unsafe_allow_html=True)
    for label,score in [("🗣️ Communication",s3.get("communication_score",0)),("🧠 Problem-Solving",s3.get("problem_solving_score",0)),("💙 Empathy & Tone",s3.get("empathy_score",0)),("⏱️ Response Speed",s3.get("response_speed_score",0))]:
        pct   = score*10
        color = "#00e5a0" if score>=7 else "#ffb340" if score>=5 else "#ff4f6d"
        st.markdown(f'<div class="score-bar-row"><div class="score-bar-label">{label}</div><div class="score-bar-track"><div class="score-bar-fill" style="width:{pct}%;background:{color}"></div></div><div class="score-bar-num">{score}/10</div></div>', unsafe_allow_html=True)
    strengths  = s3.get("strengths",[])
    weaknesses = s3.get("weaknesses",[])
    if strengths or weaknesses:
        ca,cb = st.columns(2)
        with ca:
            if strengths:
                st.markdown('<div class="subsection-label">✅ Strengths</div>', unsafe_allow_html=True)
                for s in strengths: st.markdown(f'<div class="biz-item" style="color:var(--green);">→ {s}</div>', unsafe_allow_html=True)
        with cb:
            if weaknesses:
                st.markdown('<div class="subsection-label">❌ Weaknesses</div>', unsafe_allow_html=True)
                for w in weaknesses: st.markdown(f'<div class="biz-item" style="color:var(--red);">→ {w}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    back_next(2,"Emotional Intelligence",4,"Conversation Intelligence","s3_back","s3_next")


# ── Stage 4 ──────────────────────────────────────────────────
def render_stage4(a):
    stage_header("04","Conversation Intelligence")
    s4 = a.get("stage4",{})
    for sentence in s4.get("key_customer_sentences",[]):
        st.markdown(f'<div class="quote-block customer-quote">"{sentence}"</div>', unsafe_allow_html=True)
    best  = s4.get("agent_best_reply","")
    worst = s4.get("agent_worst_reply","")
    if best:
        st.markdown('<div class="subsection-label">✅ Agent — Best Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="quote-block best-quote">"{best}"</div>', unsafe_allow_html=True)
    if worst:
        st.markdown('<div class="subsection-label">❌ Agent — Weakest Response</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="quote-block worst-quote">"{worst}"</div>', unsafe_allow_html=True)
    cm = s4.get("critical_moments",{})
    icons  = {"escalation_point":"🔺","confusion_point":"❓","resolution_moment":"✅"}
    labels = {"escalation_point":"Escalation Point","confusion_point":"Confusion Point","resolution_moment":"Resolution Moment"}
    for key,val in cm.items():
        if val and str(val) not in ("null","None","—"):
            st.markdown(f'<div class="moment-item"><span class="moment-icon">{icons.get(key,"📍")}</span><div><div class="moment-label">{labels.get(key,key)}</div><div class="moment-desc">{val}</div></div></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    back_next(3,"Agent Performance",5,"Email Generator","s4_back","s4_next")


# ── Stage 5 — Email Generator ─────────────────────────────────
def render_stage5(a):
    stage_header("05","AI Email Generator")
    s1 = a.get("stage1",{})
    s5 = a.get("stage5",{})

    resolution   = s1.get("resolution","Unresolved")
    issue_type   = s1.get("issue_type","your concern")
    customer_nm  = s1.get("customer_name")
    agent_nm     = s1.get("agent_name")
    order_num    = s1.get("order_number")
    product      = s1.get("product_mentioned")
    company      = s1.get("company_name")
    emotion      = s1.get("customer_emotion","Neutral")
    next_steps   = s5.get("next_steps",[])

    def ph(val, placeholder):
        if val and str(val) not in (None,"null","None","—",""):
            return str(val)
        return f"{{{{{placeholder}}}}}"

    cust_first  = ph(customer_nm,"customer_name").split()[0] if customer_nm else "{{customer_name}}"
    agent_str   = ph(agent_nm,  "agent_name")
    order_str   = ph(order_num, "order_number")
    company_str = ph(company,   "company_name")
    product_str = ph(product,   "product_or_service")

    empathy_map = {
        "Angry":      "We understand this situation was deeply frustrating, and we sincerely apologise for the distress caused.",
        "Frustrated": "We recognise how frustrating this experience has been, and we truly appreciate your patience throughout.",
        "Upset":      "We understand how upsetting this must have been, and we're sorry for the difficulty you faced.",
        "Anxious":    "We understand this caused concern, and we want to assure you that your case has been handled with care.",
        "Satisfied":  "We're glad we could resolve things smoothly and appreciate your kind patience.",
    }
    empathy_line = empathy_map.get(emotion, "We sincerely appreciate your patience and understanding throughout this process.")

    if resolution == "Resolved":
        res_line   = "We're pleased to confirm that your issue has been successfully resolved."
        badge_label,badge_bg,badge_col = "✅ Issue Resolved","rgba(14,158,110,0.10)","#0e9e6e"
        ns_default = ["Your case is now closed","A resolution confirmation has been logged on your account"]
    elif resolution == "Escalated":
        res_line   = "Your case has been escalated to our specialized team for priority handling."
        badge_label,badge_bg,badge_col = "🔺 Escalation Update","rgba(214,63,90,0.08)","#d63f5a"
        ns_default = ["A senior specialist has been assigned","You will receive a direct update within 24 hours","Your case is flagged as high priority"]
    else:
        res_line   = "Our team is actively working on your concern and will keep you updated."
        badge_label,badge_bg,badge_col = "⏳ Follow-Up Required","rgba(196,126,10,0.08)","#c47e0a"
        ns_default = ["Investigation ongoing","Expected resolution within 24-48 hours","We will follow up proactively — no need to chase us"]

    effective_ns   = next_steps if next_steps else ns_default
    next_steps_txt = "\n".join(f"  • {ns}" for ns in effective_ns)

    subject = f"Your Recent {issue_type} ({company_str}) — Ref: {order_str}"

    body = f"""Dear {cust_first},

Thank you for taking the time to speak with us today. We truly appreciate your patience while we looked into your concern regarding {product_str} (Ref: {order_str}).

{res_line}

{empathy_line}

📍 Next Steps:
{next_steps_txt}

{"We sincerely regret the inconvenience this may have caused. " if resolution != "Resolved" else ""}If you have any additional questions or need further assistance, please reply to this email or contact our support team directly — we're always here to help.

Warm regards,
{agent_str}
Customer Support Team
{company_str}"""

    # Badge
    st.markdown(f'<div class="email-type-badge" style="background:{badge_bg};color:{badge_col};border:1px solid {badge_col}44;">{badge_label}</div>', unsafe_allow_html=True)

    # Personalisation chips
    def chip(lbl, val):
        is_ph = str(val).startswith("{{")
        clr   = "#8878aa" if is_ph else "var(--heading)"
        return f'<span style="background:var(--bg3);border:1px solid var(--border);border-radius:6px;padding:3px 10px;font-size:12px;margin-right:5px;margin-bottom:5px;display:inline-block;color:var(--text2);"><b style="color:{clr};">{lbl}</b> {val}</span>'

    chips = chip("👤",cust_first)+chip("📦",product_str)+chip("🔖",order_str)+chip("🏢",company_str)+chip("😤",emotion)+chip("🧑‍💼",agent_str)
    st.markdown(f'<div style="margin-bottom:10px;line-height:2.3;">{chips}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11.5px;color:var(--text3);margin-bottom:16px;">Grey = not detected in transcript — fill before sending</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="email-wrap">
        <div class="email-header">
            <div class="email-subject-label">Subject Line</div>
            <div class="email-subject">{subject}</div>
        </div>
        <div class="email-body">{body}</div>
        <div class="email-footer">✦ Review and personalise before sending · {{{{placeholders}}}} indicate details not found in transcript</div>
    </div>""", unsafe_allow_html=True)

    with st.expander("📋 Copy plain text"):
        st.code(f"Subject: {subject}\n\n{body}", language=None)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    back_next(4,"Conversation Intelligence",6,"AI Coach Mode","s5_back","s5_next")


# ── Stage 6 — AI Coach ───────────────────────────────────────
def render_stage6(a):
    stage_header("06","AI Coach Mode")
    s5 = a.get("stage5",{})
    s6 = a.get("stage6",{})

    for rw in s5.get("response_rewrites",[]):
        st.markdown(f'<div class="rewrite-card"><div class="rewrite-original"><span class="rw-tag orig-tag">ORIGINAL</span>{rw.get("original","")}</div><div class="rewrite-arrow">↓ Better response</div><div class="rewrite-better"><span class="rw-tag better-tag">IMPROVED</span>{rw.get("improved","")}</div></div>', unsafe_allow_html=True)

    ideal = s5.get("ideal_resolution_pathway",[])
    if ideal:
        st.markdown('<div class="subsection-label">🧭 Ideal Resolution Pathway</div>', unsafe_allow_html=True)
        for i,step in enumerate(ideal,1):
            st.markdown(f'<div class="pathway-step"><div class="pathway-num">{i}</div><div class="pathway-text">{step}</div></div>', unsafe_allow_html=True)

    for m in s5.get("mistake_summary",[]):
        st.markdown(f'<div class="mistake-item">⚠ {m}</div>', unsafe_allow_html=True)

    ns_list = s5.get("next_steps",[])
    if ns_list:
        st.markdown('<div class="subsection-label">📍 Recommended Next Steps</div>', unsafe_allow_html=True)
        for ns in ns_list: st.markdown(f'<div class="next-step-item">→ {ns}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="subsection-label">📊 Business Dashboard</div>', unsafe_allow_html=True)
    ca,cb = st.columns(2)
    with ca:
        tips = s6.get("coaching_tips",[])
        if tips:
            st.markdown('<div class="biz-card"><div class="biz-card-title">🎓 Coaching Tips</div>'+"".join(f'<div class="biz-item">→ {t}</div>' for t in tips)+'</div>', unsafe_allow_html=True)
        esc = s6.get("escalation_suggestions",[])
        if esc:
            st.markdown('<div class="biz-card escalation-card"><div class="biz-card-title">🚨 Escalation Triggers</div>'+"".join(f'<div class="biz-item">→ {e}</div>' for e in esc)+'</div>', unsafe_allow_html=True)
    with cb:
        upsell = [u for u in s6.get("upsell_opportunities",[]) if u and str(u).lower()!="null"]
        if upsell:
            st.markdown('<div class="biz-card upsell-card"><div class="biz-card-title">💰 Upsell Opportunities</div>'+"".join(f'<div class="biz-item">→ {u}</div>' for u in upsell)+'</div>', unsafe_allow_html=True)
        insights = s6.get("strategic_insights",[])
        if insights:
            st.markdown('<div class="biz-card"><div class="biz-card-title">📊 Strategic Insights</div>'+"".join(f'<div class="biz-item">→ {i}</div>' for i in insights)+'</div>', unsafe_allow_html=True)
    recs = s6.get("ai_recommendations",[])
    if recs:
        st.markdown('<div class="biz-card"><div class="biz-card-title">🧠 AI Recommendations</div>'+"".join(f'<div class="biz-item">✦ {r}</div>' for r in recs)+'</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("← Email Generator", key="s6_back"): st.session_state.active_section=5; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── Render ───────────────────────────────────────────────────
render_sidebar()

if st.session_state.stage == "input":
    if not groq_api_key:
        st.markdown('<div class="voc-warning">⚠️ &nbsp; Add your <strong>GROQ_API_KEY</strong> in Streamlit Secrets to enable AI analysis.</div>', unsafe_allow_html=True)

    # vocAI — top-left, large, bold
    st.markdown('<div style="font-size:42px;font-weight:800;letter-spacing:-1.5px;color:#2d1b69;line-height:1;margin-bottom:4px;">voc<span style="color:#7c5fe6;">AI</span></div>', unsafe_allow_html=True)

    # Centered hero
    st.markdown("""
    <div style="text-align:center;padding:28px 0 20px;">
        <div style="font-size:26px;font-weight:700;color:#2d1b69;letter-spacing:-0.4px;margin-bottom:10px;">From conversations to clarity</div>
        <div style="font-size:15px;color:#4a4060;max-width:520px;margin:0 auto 32px;line-height:1.75;font-weight:400;">
            Upload an audio file, paste a transcript, or use a sample call.<br>
            In seconds, vocAI breaks it down into structured insights using a 6-stage AI analysis engine.
        </div>
    </div>""", unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["📁  Sample Calls","🎙️  Upload Audio","📝  Paste Transcript"])

    with tab3:
        ti = st.text_area("",placeholder="Agent: Thank you for calling Support, how can I help?\nCustomer: Hi, I've been charged twice for my subscription...",height=260,key="transcript_paste")
        if st.button("⚡  Run Analysis",key="btn_paste",use_container_width=True):
            if ti.strip():
                st.session_state.transcript=ti.strip(); st.session_state.stage="analyzing"; st.rerun()
            else: st.error("Please paste a transcript first.")

    with tab1:
        for idx,sample in enumerate(SAMPLE_CALLS):
            ci,cb_ = st.columns([5,1])
            with ci:
                st.markdown(f'<div class="sample-card"><div class="sample-title">{sample["title"]}</div><div class="sample-meta">{sample.get("type","—")} &nbsp;·&nbsp; {sample.get("duration","—")} &nbsp;·&nbsp; {sample.get("outcome","—")}</div><div class="sample-preview">{sample.get("preview","")}</div></div>', unsafe_allow_html=True)
            with cb_:
                st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)
                if st.button("Analyze →",key=f"sample_{idx}"):
                    st.session_state.transcript=sample["transcript"]; st.session_state.stage="analyzing"; st.rerun()

    with tab2:
        st.markdown('<div style="font-size:13px;color:var(--text2);margin-bottom:14px;">Upload an MP3, WAV or M4A — transcribed via Groq Whisper then analyzed.</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("",type=["mp3","wav","m4a"])
        if uploaded:
            if st.button("⚡  Transcribe & Analyze",key="btn_audio",use_container_width=True):
                if groq_api_key:
                    from groq import Groq as _G
                    with st.spinner("Transcribing with Whisper…"):
                        try:
                            tx = _G(api_key=groq_api_key).audio.transcriptions.create(file=(uploaded.name,uploaded.read(),uploaded.type),model="whisper-large-v3")
                            st.session_state.transcript=tx.text; st.session_state.stage="analyzing"; st.rerun()
                        except Exception as e: st.error(f"Transcription error: {e}")
                else: st.error("GROQ_API_KEY required for audio transcription.")

elif st.session_state.stage == "analyzing":
    st.markdown('<div class="analyzing-wrap"><div class="analyzing-orb"></div><div class="analyzing-title">Analyzing your call…</div><div class="analyzing-sub">Running 6-stage intelligence pipeline</div></div>', unsafe_allow_html=True)
    pb = st.progress(0)
    st_ = st.empty()
    if groq_api_key:
        try:
            result = analyze_transcript(st.session_state.transcript, groq_api_key, pb, st_, ANALYSIS_STEPS)
            st.session_state.analysis=result; st.session_state.stage="results"; st.session_state.active_section=1; st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            if st.button("← Go back"): st.session_state.stage="input"; st.rerun()
    else:
        for i,step in enumerate(ANALYSIS_STEPS):
            st_.markdown(f'<div style="font-size:13px;color:var(--text2);text-align:center;margin-top:8px;">{step}</div>',unsafe_allow_html=True)
            pb.progress((i+1)/len(ANALYSIS_STEPS)); time.sleep(0.4)
        st.warning("No API key — add GROQ_API_KEY to Streamlit Secrets.")
        if st.button("← Go back"): st.session_state.stage="input"; st.rerun()

elif st.session_state.stage == "results":
    a   = st.session_state.analysis
    sec = st.session_state.active_section
    breadcrumb(sec)
    if   sec==1: render_stage1(a)
    elif sec==2: render_stage2(a)
    elif sec==3: render_stage3(a)
    elif sec==4: render_stage4(a)
    elif sec==5: render_stage5(a)
    elif sec==6: render_stage6(a)

st.markdown('<div class="voc-footer">vocAI · Powered by Groq &amp; LLaMA 3.3 · Call Intelligence Platform built by Mahitha Bhagavathi </div>', unsafe_allow_html=True)
