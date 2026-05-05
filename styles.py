import streamlit as st

def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #080c12 !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #080c12 !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* ── Header ───────────────────────────────────────────────── */
.voc-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}

.voc-logo {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1;
}

.voc-logo-voc {
    color: #e8eaf0;
}

.voc-logo-ai {
    color: #4af0b0;
    background: linear-gradient(135deg, #4af0b0, #00b4d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.voc-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    font-weight: 300;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #5a6275;
    margin-top: 0.4rem;
}

.voc-divider {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, #4af0b0, #00b4d8);
    margin: 1.4rem auto 0;
    border-radius: 2px;
}

/* ── Warning ──────────────────────────────────────────────── */
.voc-warning {
    background: #1a1200;
    border: 1px solid #ffa94d44;
    border-left: 3px solid #ffa94d;
    color: #ffa94d;
    padding: 0.75rem 1.2rem;
    border-radius: 6px;
    font-size: 0.88rem;
    margin-bottom: 1.5rem;
}

/* ── Section Label ────────────────────────────────────────── */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4af0b0;
    margin-bottom: 1rem;
    margin-top: 0.5rem;
}

/* ── Tabs ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e2533 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: #5a6275 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.2rem !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    background: #1a2236 !important;
    color: #4af0b0 !important;
}

.stTabs [data-baseweb="tab-panel"] {
    padding-top: 1.2rem !important;
}

.tab-hint {
    font-size: 0.86rem;
    color: #4a5568;
    margin-bottom: 1rem;
    font-style: italic;
}

/* ── Text Area ────────────────────────────────────────────── */
.stTextArea textarea {
    background: #0d1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    color: #c9d1d9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 1rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextArea textarea:focus {
    border-color: #4af0b044 !important;
    box-shadow: 0 0 0 3px #4af0b011 !important;
}

/* ── Buttons ──────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #0d2a1f, #112233) !important;
    border: 1px solid #4af0b033 !important;
    color: #4af0b0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    border-radius: 8px !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #162f24, #162540) !important;
    border-color: #4af0b066 !important;
    box-shadow: 0 4px 20px #4af0b022 !important;
    transform: translateY(-1px) !important;
}

/* ── Sample Cards ─────────────────────────────────────────── */
.sample-card {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.2s ease;
}

.sample-card:hover {
    border-color: #4af0b033;
}

.sample-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    color: #e8eaf0;
    margin-bottom: 0.25rem;
}

.sample-meta {
    font-size: 0.78rem;
    color: #4af0b0;
    letter-spacing: 0.05em;
    margin-bottom: 0.35rem;
}

.sample-preview {
    font-size: 0.83rem;
    color: #5a6275;
    font-style: italic;
    line-height: 1.5;
}

/* ── Analyzing Screen ─────────────────────────────────────── */
.analyzing-screen {
    text-align: center;
    padding: 4rem 0 2rem;
}

.analyzing-orb {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background: radial-gradient(circle at 40% 40%, #4af0b0, #00b4d8, #0d1117);
    margin: 0 auto 1.5rem;
    animation: pulse-orb 1.8s ease-in-out infinite;
    box-shadow: 0 0 40px #4af0b055;
}

@keyframes pulse-orb {
    0%, 100% { transform: scale(1); box-shadow: 0 0 40px #4af0b055; }
    50% { transform: scale(1.08); box-shadow: 0 0 60px #4af0b088; }
}

.analyzing-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #e8eaf0;
    margin-bottom: 0.4rem;
}

.analyzing-sub {
    font-size: 0.85rem;
    color: #5a6275;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.step-text {
    font-size: 0.88rem;
    color: #4af0b0;
    text-align: center;
    margin-top: 0.75rem;
    font-family: 'DM Sans', sans-serif;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #4af0b0, #00b4d8) !important;
    border-radius: 4px !important;
}

.stProgress > div > div > div {
    background: #1e2533 !important;
    border-radius: 4px !important;
}

/* ── Stage Headers ────────────────────────────────────────── */
.stage-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e8eaf0;
    padding: 0.9rem 1.2rem;
    border-radius: 10px;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    letter-spacing: -0.02em;
}

.stage-1 { background: linear-gradient(135deg, #0d1f18, #0a1a20); border-left: 3px solid #4af0b0; }
.stage-5 { background: linear-gradient(135deg, #1a1020, #0d1020); border-left: 3px solid #a78bfa; }
.stage-6 { background: linear-gradient(135deg, #1a1200, #141020); border-left: 3px solid #ffa94d; }

.stage-num {
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    background: #1e2533;
    color: #5a6275;
    padding: 0.2rem 0.45rem;
    border-radius: 4px;
}

/* ── Metric Cards ─────────────────────────────────────────── */
.metric-card {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1.2rem 1rem;
    text-align: center;
    height: 100%;
}

.metric-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5a6275;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #4af0b0;
}

/* ── Summary Box ──────────────────────────────────────────── */
.summary-box {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.8rem;
    line-height: 1.75;
}

.summary-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5a6275;
    margin-bottom: 0.75rem;
}

.summary-text {
    font-size: 0.92rem;
    color: #c9d1d9;
    line-height: 1.8;
}

/* ── Expanders ────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: #0d1117 !important;
    border: 1px solid #1e2533 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    color: #c9d1d9 !important;
    padding: 0.9rem 1.2rem !important;
    margin-bottom: 0.3rem !important;
}

.streamlit-expanderContent {
    background: #080c12 !important;
    border: 1px solid #1e2533 !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

.exp-inner {
    padding: 0.5rem 0;
}

/* ── Subsection Labels ────────────────────────────────────── */
.subsection-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a6275;
    margin: 1.2rem 0 0.6rem;
    border-bottom: 1px solid #1e2533;
    padding-bottom: 0.4rem;
}

/* ── Phase Cards (Sentiment) ──────────────────────────────── */
.phase-card {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1.2rem 1rem;
    text-align: center;
}

.phase-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5a6275;
    margin-bottom: 0.6rem;
}

.phase-emoji {
    font-size: 1.8rem;
    line-height: 1;
    margin-bottom: 0.4rem;
}

.phase-value {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    color: #c9d1d9;
}

/* ── Spike Items ──────────────────────────────────────────── */
.spike-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    border-bottom: 1px solid #1e2533;
    font-size: 0.88rem;
}

.spike-badge {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    border: 1px solid;
    white-space: nowrap;
}

.spike-desc {
    color: #8892a4;
    line-height: 1.5;
}

/* ── Critical Items ───────────────────────────────────────── */
.critical-item {
    background: #1a0d0d;
    border: 1px solid #ff4d6d22;
    border-left: 3px solid #ff4d6d;
    color: #ff9aab;
    padding: 0.7rem 1rem;
    border-radius: 6px;
    font-size: 0.88rem;
    margin: 0.4rem 0;
}

/* ── Score Hero ───────────────────────────────────────────── */
.score-hero {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1.5rem 0 1rem;
}

.score-ring {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(
        #4af0b0 calc(var(--score) * 36deg),
        #1e2533 0deg
    );
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.75rem;
    box-shadow: 0 0 30px #4af0b022;
}

.score-inner {
    width: 76px;
    height: 76px;
    border-radius: 50%;
    background: #080c12;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #4af0b0;
    line-height: 1;
}

.score-label {
    font-size: 0.72rem;
    color: #5a6275;
}

.score-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

/* ── Score Bars ───────────────────────────────────────────── */
.score-bar-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.6rem 0;
}

.score-bar-label {
    font-size: 0.85rem;
    color: #8892a4;
    width: 180px;
    flex-shrink: 0;
}

.score-bar-track {
    flex: 1;
    height: 6px;
    background: #1e2533;
    border-radius: 3px;
    overflow: hidden;
}

.score-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.8s ease;
}

.score-bar-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 700;
    color: #c9d1d9;
    width: 40px;
    text-align: right;
    flex-shrink: 0;
}

/* ── Quotes ───────────────────────────────────────────────── */
.quote-block {
    padding: 0.9rem 1.2rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-style: italic;
    line-height: 1.6;
    margin: 0.4rem 0;
}

.customer-quote {
    background: #0d1520;
    border-left: 3px solid #00b4d8;
    color: #a0b0c8;
}

.best-quote {
    background: #0a1f0e;
    border-left: 3px solid #00d68f;
    color: #80c898;
}

.worst-quote {
    background: #1a0d0d;
    border-left: 3px solid #ff4d6d;
    color: #ff9aab;
}

/* ── Moments ──────────────────────────────────────────────── */
.moment-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.8rem 0;
    border-bottom: 1px solid #1e2533;
}

.moment-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
    margin-top: 0.1rem;
}

.moment-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5a6275;
    margin-bottom: 0.25rem;
}

.moment-desc {
    font-size: 0.9rem;
    color: #8892a4;
    line-height: 1.5;
}

/* ── Rewrite Cards ────────────────────────────────────────── */
.rewrite-card {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

.rewrite-original, .rewrite-better {
    font-size: 0.88rem;
    line-height: 1.6;
    color: #8892a4;
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
}

.rewrite-better {
    color: #80c898;
}

.rewrite-arrow {
    text-align: center;
    color: #4af0b0;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.4rem 0;
    opacity: 0.6;
}

.rw-tag {
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    padding: 0.15rem 0.5rem;
    border-radius: 3px;
    flex-shrink: 0;
    margin-top: 0.1rem;
}

.orig-tag {
    background: #1e2533;
    color: #5a6275;
}

.better-tag {
    background: #0a2515;
    color: #4af0b0;
}

/* ── Pathway Steps ────────────────────────────────────────── */
.pathway-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.8rem 0;
    border-bottom: 1px solid #1e2533;
}

.pathway-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4af0b0, #00b4d8);
    color: #080c12;
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 0.05rem;
}

.pathway-text {
    font-size: 0.9rem;
    color: #8892a4;
    line-height: 1.6;
}

/* ── Mistake Items ────────────────────────────────────────── */
.mistake-item {
    background: #130f0a;
    border: 1px solid #ffa94d22;
    color: #ffc980;
    padding: 0.65rem 1rem;
    border-radius: 6px;
    font-size: 0.88rem;
    margin: 0.35rem 0;
    border-left: 3px solid #ffa94d;
}

/* ── Business Cards ───────────────────────────────────────── */
.biz-card {
    background: #0d1117;
    border: 1px solid #1e2533;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.8rem;
}

.escalation-card {
    border-left: 3px solid #ff4d6d;
}

.upsell-card {
    border-left: 3px solid #ffa94d;
}

.recs-card {
    border-left: 3px solid #4af0b0;
    margin-top: 0.5rem;
}

.biz-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    color: #c9d1d9;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2533;
}

.biz-item {
    font-size: 0.88rem;
    color: #8892a4;
    line-height: 1.6;
    padding: 0.3rem 0;
}

.rec-item {
    color: #a0b8c8;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1e253388;
}

.rec-item:last-child {
    border-bottom: none;
}

/* ── Footer ───────────────────────────────────────────────── */
.voc-footer {
    text-align: center;
    font-size: 0.78rem;
    color: #2a3242;
    padding: 3rem 0 1rem;
    letter-spacing: 0.05em;
}

/* ── File Uploader ────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: #0d1117 !important;
    border: 1px dashed #1e2533 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

[data-testid="stFileUploader"]:hover {
    border-color: #4af0b044 !important;
}

/* ── Spinner ──────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #4af0b0 !important;
}

/* ── Responsive ───────────────────────────────────────────── */
@media (max-width: 768px) {
    .block-container {
        padding: 1rem 1.2rem 3rem !important;
    }
    .score-bar-label {
        width: 130px;
    }
}
</style>
""", unsafe_allow_html=True)
