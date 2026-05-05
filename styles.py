import streamlit as st

def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --bg-base:      #f7f5ff;
    --bg-surface:   #ffffff;
    --bg-subtle:    #f0ecff;
    --bg-hover:     #ede8ff;
    --purple-50:    #f5f0ff;
    --purple-100:   #ede8ff;
    --purple-200:   #d9d0ff;
    --purple-300:   #bfb2ff;
    --purple-400:   #a08bff;
    --purple-500:   #7c5cfc;
    --purple-600:   #6741f5;
    --purple-700:   #5330d4;
    --purple-800:   #3d228f;
    --lavender:     #c4b5fd;
    --text-primary: #1e1535;
    --text-secondary:#4a3f6b;
    --text-muted:   #8b7fb5;
    --text-faint:   #b8aed4;
    --green:        #10b981;
    --green-soft:   #ecfdf5;
    --amber:        #f59e0b;
    --amber-soft:   #fffbeb;
    --red:          #ef4444;
    --red-soft:     #fef2f2;
    --blue:         #3b82f6;
    --blue-soft:    #eff6ff;
    --border:       #e8e2f8;
    --shadow-sm:    0 1px 4px rgba(124,92,252,0.08);
    --shadow-md:    0 4px 16px rgba(124,92,252,0.10);
    --shadow-lg:    0 10px 40px rgba(124,92,252,0.13);
    --r-sm: 6px; --r-md: 10px; --r-lg: 16px; --r-xl: 24px;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.main .block-container {
    background: var(--bg-base) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer { display: none !important; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 920px !important; }

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1.5px solid var(--border) !important;
    min-width: 255px !important; max-width: 255px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] .block-container { padding: 0 !important; max-width: 100% !important; }

.sb-logo { padding: 1.5rem 1.3rem 1.1rem; border-bottom: 1px solid var(--border); }
.sb-logo-text { font-family: 'Instrument Serif', serif; font-size: 1.6rem; letter-spacing: -0.03em; line-height: 1; }
.sb-logo-voc  { color: var(--text-primary); }
.sb-logo-ai   { color: var(--purple-500); font-style: italic; }
.sb-tagline   { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint); margin-top: 0.3rem; }

.sb-section-lbl { font-size: 0.62rem; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase; color: var(--text-faint); padding: 1rem 1.3rem 0.3rem; }

.sb-nav-item {
    display: flex; align-items: center; gap: 0.65rem;
    padding: 0.6rem 1.3rem; cursor: pointer;
    position: relative; transition: background 0.15s ease;
}
.sb-nav-item:hover { background: var(--purple-50); }
.sb-nav-item.active { background: var(--purple-100); }
.sb-nav-item.active::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px; background: var(--purple-500); border-radius: 0 2px 2px 0;
}

.sb-nav-icon {
    width: 28px; height: 28px; border-radius: var(--r-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; flex-shrink: 0;
}
.sb-nav-icon-1 { background: #dcfce7; }
.sb-nav-icon-2 { background: #fef9c3; }
.sb-nav-icon-3 { background: #dbeafe; }
.sb-nav-icon-4 { background: #fdf4ff; }
.sb-nav-icon-5 { background: #fff7ed; }
.sb-nav-icon-6 { background: var(--purple-100); }

.sb-nav-title { font-size: 0.81rem; font-weight: 600; color: var(--text-secondary); }
.sb-nav-item.active .sb-nav-title { color: var(--purple-600); }

.sb-status {
    font-size: 0.61rem; font-weight: 800; letter-spacing: 0.05em;
    padding: 0.15rem 0.5rem; border-radius: 20px; margin-left: auto; flex-shrink: 0;
}
.sb-done    { background: #dcfce7; color: #15803d; }
.sb-active  { background: var(--purple-100); color: var(--purple-600); }
.sb-pending { background: #f1f5f9; color: #94a3b8; }

.sb-divider { height: 1px; background: var(--border); margin: 0.6rem 1.3rem; }

.sb-call-info {
    margin: 0.5rem 0.8rem;
    background: var(--purple-50); border: 1px solid var(--purple-200);
    border-radius: var(--r-md); padding: 0.85rem 1rem;
}
.sci-lbl { font-size: 0.62rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.45rem; }
.sci-badge {
    display: inline-flex; align-items: center; gap: 0.3rem;
    font-size: 0.74rem; font-weight: 700; color: var(--purple-700);
    background: var(--purple-200); padding: 0.22rem 0.6rem;
    border-radius: 20px; margin-bottom: 0.25rem;
}

.sb-footer { padding: 1rem 1.3rem; border-top: 1px solid var(--border); margin-top: auto; font-size: 0.7rem; color: var(--text-faint); text-align: center; }

/* ── Page Header ─────────────────────────────────────── */
.page-eyebrow { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase; color: var(--purple-400); margin-bottom: 0.35rem; }
.page-title   { font-family: 'Instrument Serif', serif; font-size: 2rem; color: var(--text-primary); letter-spacing: -0.03em; line-height: 1.2; margin-bottom: 0.35rem; }
.page-subtitle{ font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.8rem; }

/* ── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-subtle) !important; border-radius: var(--r-lg) !important;
    padding: 5px !important; gap: 3px !important;
    border: 1.5px solid var(--border) !important; width: fit-content !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: var(--r-md) !important;
    color: var(--text-muted) !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.82rem !important; font-weight: 600 !important;
    padding: 0.48rem 1.1rem !important; border: none !important; transition: all 0.18s ease !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-surface) !important; color: var(--purple-600) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.3rem !important; background: transparent !important; }

.input-hint { font-size: 0.84rem; color: var(--text-muted); margin-bottom: 0.9rem; }

/* ── Textarea ────────────────────────────────────────── */
.stTextArea textarea {
    background: var(--bg-surface) !important; border: 1.5px solid var(--border) !important;
    border-radius: var(--r-lg) !important; color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.87rem !important;
    line-height: 1.7 !important; padding: 1rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: var(--purple-400) !important;
    box-shadow: 0 0 0 4px rgba(160,139,255,0.13) !important;
}

/* ── Buttons ─────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--purple-500), var(--purple-700)) !important;
    border: none !important; color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.86rem !important;
    font-weight: 700 !important; letter-spacing: 0.02em !important;
    border-radius: var(--r-md) !important; padding: 0.62rem 1.6rem !important;
    box-shadow: 0 2px 10px rgba(124,92,252,0.32) !important; transition: all 0.18s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--purple-600), var(--purple-800)) !important;
    box-shadow: 0 4px 18px rgba(124,92,252,0.42) !important; transform: translateY(-1px) !important;
}

/* ── Warning ─────────────────────────────────────────── */
.voc-warning {
    background: var(--amber-soft); border: 1px solid #fde68a; border-left: 3px solid var(--amber);
    color: #92400e; padding: 0.75rem 1.1rem; border-radius: var(--r-md);
    font-size: 0.85rem; font-weight: 500; margin-bottom: 1.5rem;
}

/* ── Analyzing ───────────────────────────────────────── */
.analyzing-screen { text-align: center; padding: 5rem 2rem 3rem; }
.analyzing-orb {
    width: 78px; height: 78px; border-radius: 50%; margin: 0 auto 1.8rem;
    background: conic-gradient(var(--purple-400) 0%, var(--lavender) 35%, var(--purple-600) 70%, var(--purple-400) 100%);
    animation: orb-spin 1.8s linear infinite;
    box-shadow: 0 0 50px rgba(124,92,252,0.28);
    position: relative;
}
.analyzing-orb::after {
    content: ''; position: absolute; inset: 10px;
    border-radius: 50%; background: var(--bg-base);
}
@keyframes orb-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.analyzing-title { font-family: 'Instrument Serif', serif; font-size: 1.75rem; color: var(--text-primary); margin-bottom: 0.4rem; }
.analyzing-sub   { font-size: 0.82rem; color: var(--text-muted); letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 2.5rem; }
.step-text { font-size: 0.87rem; color: var(--purple-500); font-weight: 600; text-align: center; margin-top: 0.75rem; }

.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--purple-400), var(--purple-600)) !important; border-radius: 4px !important; }
.stProgress > div > div > div       { background: var(--purple-100) !important; border-radius: 4px !important; }

/* ── Stage Headers ───────────────────────────────────── */
.stage-hdr {
    display: flex; align-items: center; gap: 0.75rem;
    margin-bottom: 1.2rem; padding-bottom: 0.85rem;
    border-bottom: 2px solid var(--border);
}
.stage-badge {
    width: 34px; height: 34px; border-radius: var(--r-sm);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.7rem; font-weight: 800; letter-spacing: 0.05em; flex-shrink: 0;
}
.sb1 { background: #dcfce7; color: #15803d; }
.sb2 { background: #fef9c3; color: #854d0e; }
.sb3 { background: #dbeafe; color: #1e40af; }
.sb4 { background: #fdf4ff; color: #7e22ce; }
.sb5 { background: #fff7ed; color: #c2410c; }
.sb6 { background: var(--purple-100); color: var(--purple-700); }

.stage-title { font-family: 'Instrument Serif', serif; font-size: 1.3rem; color: var(--text-primary); letter-spacing: -0.02em; }
.stage-sub   { font-size: 0.76rem; color: var(--text-muted); margin-top: 0.1rem; }

/* ── KPI Cards ───────────────────────────────────────── */
.kpi-card {
    background: var(--bg-surface); border: 1.5px solid var(--border);
    border-radius: var(--r-lg); padding: 1.1rem 1rem 1rem;
    transition: all 0.18s ease;
}
.kpi-card:hover { border-color: var(--purple-200); box-shadow: var(--shadow-md); }
.kpi-icon  { font-size: 1.3rem; margin-bottom: 0.5rem; }
.kpi-lbl   { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint); margin-bottom: 0.3rem; }
.kpi-val   { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
.kpi-green { color: var(--green); }
.kpi-red   { color: var(--red); }
.kpi-amber { color: var(--amber); }
.kpi-purple{ color: var(--purple-500); }

/* ── Summary Box ─────────────────────────────────────── */
.summary-box {
    background: linear-gradient(135deg, var(--bg-surface), var(--purple-50));
    border: 1.5px solid var(--purple-200); border-radius: var(--r-lg); padding: 1.3rem 1.5rem;
}
.summary-eyebrow { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--purple-400); margin-bottom: 0.6rem; }
.summary-text    { font-size: 0.92rem; color: var(--text-secondary); line-height: 1.85; }

/* ── Phase Grid ──────────────────────────────────────── */
.phase-card {
    background: var(--bg-surface); border: 1.5px solid var(--border);
    border-radius: var(--r-lg); padding: 1rem 0.8rem; text-align: center;
}
.phase-lbl   { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint); margin-bottom: 0.65rem; }
.phase-emoji { font-size: 1.85rem; margin-bottom: 0.4rem; }
.phase-val   { font-size: 0.82rem; font-weight: 700; color: var(--text-secondary); }

/* ── Emotion Tags ────────────────────────────────────── */
.emotion-row {
    display: flex; align-items: flex-start; gap: 0.75rem;
    padding: 0.75rem 0; border-bottom: 1px solid var(--border);
}
.emotion-row:last-child { border-bottom: none; }
.emotion-tag { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.06em; padding: 0.2rem 0.6rem; border-radius: 20px; white-space: nowrap; flex-shrink: 0; }
.tag-anger        { background: #fee2e2; color: #b91c1c; }
.tag-frustration  { background: #ffedd5; color: #c2410c; }
.tag-confusion    { background: #ede9fe; color: #5b21b6; }
.tag-satisfaction { background: #d1fae5; color: #065f46; }
.tag-default      { background: #f1f5f9; color: #475569; }
.emotion-desc { font-size: 0.86rem; color: var(--text-muted); line-height: 1.55; }

.critical-pill {
    display: flex; align-items: flex-start; gap: 0.65rem;
    background: #fff1f2; border: 1px solid #fecdd3; border-radius: var(--r-md);
    padding: 0.7rem 0.95rem; margin-bottom: 0.45rem;
    font-size: 0.85rem; color: #9f1239;
}

/* ── Score Hero ──────────────────────────────────────── */
.score-hero {
    background: linear-gradient(135deg, var(--purple-600), var(--purple-800));
    border-radius: var(--r-xl); padding: 1.8rem 2rem;
    display: flex; align-items: center; gap: 1.8rem; margin-bottom: 1.2rem;
    box-shadow: 0 8px 32px rgba(83,48,212,0.3);
}
.score-ring-wrap { position: relative; width: 92px; height: 92px; flex-shrink: 0; }
.score-ring-svg  { width: 92px; height: 92px; transform: rotate(-90deg); }
.score-ring-bg   { fill: none; stroke: rgba(255,255,255,0.15); stroke-width: 8; }
.score-ring-fill { fill: none; stroke: var(--lavender); stroke-width: 8; stroke-linecap: round; }
.score-ring-center { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.score-big   { font-size: 1.75rem; font-weight: 800; color: #fff; line-height: 1; }
.score-denom { font-size: 0.7rem; color: rgba(255,255,255,0.55); }
.score-hero-right { color: #fff; }
.score-hero-title { font-family: 'Instrument Serif', serif; font-size: 1.3rem; margin-bottom: 0.25rem; }
.score-hero-sub   { font-size: 0.8rem; color: rgba(255,255,255,0.6); }

.sub-score-row { display: flex; align-items: center; gap: 0.85rem; padding: 0.62rem 0; border-bottom: 1px solid var(--border); }
.sub-score-row:last-child { border-bottom: none; }
.sub-score-lbl  { font-size: 0.83rem; font-weight: 600; color: var(--text-secondary); width: 185px; flex-shrink: 0; }
.sub-score-track{ flex: 1; height: 6px; background: var(--bg-subtle); border-radius: 3px; overflow: hidden; }
.sub-score-fill { height: 100%; border-radius: 3px; }
.fill-high   { background: linear-gradient(90deg, #6ee7b7, #10b981); }
.fill-medium { background: linear-gradient(90deg, #fcd34d, #f59e0b); }
.fill-low    { background: linear-gradient(90deg, #fca5a5, #ef4444); }
.sub-score-num { font-size: 0.83rem; font-weight: 800; color: var(--text-primary); width: 38px; text-align: right; flex-shrink: 0; }

/* ── Quotes ──────────────────────────────────────────── */
.quote-block { padding: 0.85rem 1.1rem; border-radius: var(--r-md); font-size: 0.88rem; font-style: italic; line-height: 1.7; margin: 0.4rem 0; }
.q-customer  { background: var(--blue-soft); border-left: 3px solid var(--blue); color: #1e3a5f; }
.q-best      { background: var(--green-soft); border-left: 3px solid var(--green); color: #064e3b; }
.q-worst     { background: var(--red-soft); border-left: 3px solid var(--red); color: #7f1d1d; }

/* ── Moments ─────────────────────────────────────────── */
.moment-card {
    display: flex; align-items: flex-start; gap: 0.85rem;
    background: var(--bg-surface); border: 1.5px solid var(--border);
    border-radius: var(--r-md); padding: 0.85rem 1rem; margin-bottom: 0.55rem;
}
.moment-icon { width: 32px; height: 32px; border-radius: var(--r-sm); display: flex; align-items: center; justify-content: center; font-size: 0.95rem; flex-shrink: 0; }
.mi-esc { background: #fee2e2; }
.mi-con { background: #ede9fe; }
.mi-res { background: #dcfce7; }
.moment-lbl  { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-faint); margin-bottom: 0.2rem; }
.moment-desc { font-size: 0.87rem; color: var(--text-secondary); line-height: 1.55; }

/* ── Rewrite Cards ───────────────────────────────────── */
.rewrite-card { background: var(--bg-surface); border: 1.5px solid var(--border); border-radius: var(--r-lg); overflow: hidden; margin-bottom: 0.75rem; }
.rw-orig {
    padding: 0.85rem 1.1rem; background: #fff8f8; border-bottom: 1px solid #ffe4e6;
    font-size: 0.86rem; color: #7f1d1d; line-height: 1.65;
    display: flex; gap: 0.6rem; align-items: flex-start;
}
.rw-impr {
    padding: 0.85rem 1.1rem; background: var(--green-soft);
    font-size: 0.86rem; color: #064e3b; line-height: 1.65;
    display: flex; gap: 0.6rem; align-items: flex-start;
}
.rw-pill { font-size: 0.6rem; font-weight: 800; letter-spacing: 0.1em; padding: 0.15rem 0.48rem; border-radius: 20px; flex-shrink: 0; margin-top: 0.12rem; }
.rw-pill-o { background: #fee2e2; color: #991b1b; }
.rw-pill-n { background: #d1fae5; color: #065f46; }

/* ── Pathway ─────────────────────────────────────────── */
.pathway-row { display: flex; align-items: flex-start; gap: 0.9rem; padding: 0.75rem 0; border-bottom: 1px dashed var(--border); }
.pathway-row:last-child { border-bottom: none; }
.pathway-num {
    width: 28px; height: 28px; border-radius: 50%;
    background: linear-gradient(135deg, var(--purple-400), var(--purple-600));
    color: #fff; font-size: 0.76rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(124,92,252,0.3);
}
.pathway-text { font-size: 0.88rem; color: var(--text-secondary); line-height: 1.6; padding-top: 0.1rem; }

/* ── Mistake ─────────────────────────────────────────── */
.mistake-item { display: flex; align-items: flex-start; gap: 0.6rem; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.87rem; color: var(--text-secondary); }
.mistake-item:last-child { border-bottom: none; }
.mistake-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--amber); flex-shrink: 0; margin-top: 0.48rem; }

/* ── Business Cards ──────────────────────────────────── */
.biz-card {
    background: var(--bg-surface); border: 1.5px solid var(--border);
    border-radius: var(--r-lg); padding: 1.1rem 1.3rem; margin-bottom: 0.7rem;
    transition: all 0.18s ease; height: 100%;
}
.biz-card:hover { border-color: var(--purple-200); box-shadow: var(--shadow-sm); }
.biz-card-hdr { display: flex; align-items: center; gap: 0.55rem; margin-bottom: 0.8rem; padding-bottom: 0.65rem; border-bottom: 1px solid var(--border); }
.biz-icon { width: 28px; height: 28px; border-radius: var(--r-sm); display: flex; align-items: center; justify-content: center; font-size: 0.88rem; }
.biz-title { font-size: 0.83rem; font-weight: 700; color: var(--text-primary); }
.biz-item { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; padding: 0.3rem 0; border-bottom: 1px solid var(--border); display: flex; align-items: flex-start; gap: 0.5rem; }
.biz-item:last-child { border-bottom: none; }
.biz-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; margin-top: 0.58rem; }

.recs-card {
    background: linear-gradient(135deg, var(--purple-50), var(--bg-surface));
    border: 1.5px solid var(--purple-200); border-radius: var(--r-lg);
    padding: 1.2rem 1.4rem; margin-top: 0.75rem;
}
.recs-item { display: flex; align-items: flex-start; gap: 0.65rem; padding: 0.45rem 0; border-bottom: 1px solid var(--purple-100); font-size: 0.87rem; color: var(--text-secondary); line-height: 1.6; }
.recs-item:last-child { border-bottom: none; }
.recs-icon { color: var(--purple-400); font-size: 0.82rem; flex-shrink: 0; margin-top: 0.18rem; }

/* ── Email Generator ─────────────────────────────────── */
.email-type-banner {
    background: linear-gradient(135deg, var(--purple-50), #fff);
    border: 1.5px solid var(--purple-200); border-radius: var(--r-lg);
    padding: 1rem 1.3rem; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 0.8rem;
}
.email-type-icon { font-size: 1.5rem; }
.email-type-lbl  { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; color: var(--purple-400); margin-bottom: 0.15rem; }
.email-type-desc { font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); }

.email-card { background: var(--bg-surface); border: 1.5px solid var(--border); border-radius: var(--r-lg); overflow: hidden; }
.email-toolbar { display: flex; align-items: center; justify-content: space-between; padding: 0.65rem 1.1rem; background: var(--bg-subtle); border-bottom: 1px solid var(--border); }
.email-toolbar-lbl { font-size: 0.7rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); }
.email-subject-row { display: flex; align-items: baseline; gap: 0.6rem; padding: 0.85rem 1.2rem 0.5rem; border-bottom: 1px solid var(--border); }
.email-subj-lbl    { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-faint); flex-shrink: 0; }
.email-subj-text   { font-size: 0.9rem; font-weight: 700; color: var(--text-primary); }
.email-body        { padding: 1rem 1.2rem 1.3rem; font-size: 0.87rem; color: var(--text-secondary); line-height: 1.9; white-space: pre-wrap; }

/* ── Sample Cards ────────────────────────────────────── */
.sample-card {
    background: var(--bg-surface); border: 1.5px solid var(--border);
    border-radius: var(--r-lg); padding: 1.05rem 1.2rem; margin-bottom: 0.65rem;
    transition: all 0.18s ease;
}
.sample-card:hover { border-color: var(--purple-300); box-shadow: var(--shadow-md); transform: translateY(-1px); }
.sample-title  { font-size: 0.91rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.3rem; }
.sample-meta   { display: flex; gap: 0.45rem; flex-wrap: wrap; margin-bottom: 0.35rem; }
.sbadge { font-size: 0.66rem; font-weight: 700; letter-spacing: 0.04em; padding: 0.18rem 0.52rem; border-radius: 20px; }
.sbadge-billing   { background: #fef3c7; color: #92400e; }
.sbadge-cancel    { background: #fce7f3; color: #9d174d; }
.sbadge-technical { background: var(--blue-soft); color: #1d4ed8; }
.sbadge-resolved  { background: var(--green-soft); color: #065f46; }
.sbadge-unresolved{ background: var(--red-soft); color: #991b1b; }
.sbadge-escalated { background: #fff7ed; color: #92400e; }
.sample-preview   { font-size: 0.81rem; color: var(--text-muted); font-style: italic; line-height: 1.5; }

/* ── Sub-labels ──────────────────────────────────────── */
.sub-lbl { font-size: 0.7rem; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-faint); margin: 1.05rem 0 0.5rem; display: flex; align-items: center; gap: 0.4rem; }
.sub-lbl::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ── Section Divider ─────────────────────────────────── */
.section-div { height: 2px; background: linear-gradient(90deg, var(--purple-200), transparent); border-radius: 2px; margin: 2.2rem 0; }

/* ── File Upload ─────────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--bg-surface) !important; border: 1.5px dashed var(--purple-200) !important;
    border-radius: var(--r-lg) !important; padding: 1.2rem !important; transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover { border-color: var(--purple-400) !important; background: var(--purple-50) !important; }

/* ── Column fix ──────────────────────────────────────── */
[data-testid="column"] { padding: 0 0.38rem !important; }

/* ── Back btn ────────────────────────────────────────── */
.back-btn > button {
    background: var(--bg-subtle) !important; border: 1.5px solid var(--border) !important;
    color: var(--text-secondary) !important; font-size: 0.82rem !important;
    font-weight: 600 !important; box-shadow: none !important; padding: 0.5rem 1rem !important;
}
.back-btn > button:hover { background: var(--purple-50) !important; border-color: var(--purple-200) !important; box-shadow: none !important; transform: none !important; }

/* ── Footer ──────────────────────────────────────────── */
.voc-footer { text-align: center; font-size: 0.72rem; color: var(--text-faint); padding: 3rem 0 1rem; letter-spacing: 0.05em; }

/* ── Expanders ───────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-surface) !important; border: 1.5px solid var(--border) !important;
    border-radius: var(--r-lg) !important; margin-bottom: 0.6rem !important;
    box-shadow: none !important; overflow: hidden !important; transition: border-color 0.18s !important;
}
[data-testid="stExpander"]:hover { border-color: var(--purple-200) !important; }
[data-testid="stExpander"] summary { padding: 0.85rem 1.1rem !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 700 !important; font-size: 0.89rem !important; color: var(--text-primary) !important; background: transparent !important; border: none !important; }
[data-testid="stExpander"] [data-testid="stExpanderDetails"] { padding: 0.2rem 1.1rem 1.1rem !important; }
</style>
""", unsafe_allow_html=True)
