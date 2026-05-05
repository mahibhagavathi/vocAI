import streamlit as st
import os
from groq import Groq
import json
import time

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="vocAI – Call Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Imports ──────────────────────────────────────────────────────────────────
from styles import inject_styles
from sample_calls import SAMPLE_CALLS
from analyzer import analyze_transcript

# ─── Styles ───────────────────────────────────────────────────────────────────
inject_styles()

# ─── Session State ────────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "analysis" not in st.session_state:
    st.session_state.analysis = None

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="voc-header">
    <div class="voc-logo">
        <span class="voc-logo-voc">voc</span><span class="voc-logo-ai">AI</span>
    </div>
    <div class="voc-tagline">Customer Call Intelligence Platform</div>
    <div class="voc-divider"></div>
</div>
""", unsafe_allow_html=True)

# ─── API Key ──────────────────────────────────────────────────────────────────
groq_api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
if not groq_api_key:
    st.markdown("""
    <div class="voc-warning">
        ⚠️ &nbsp; Add your <strong>GROQ_API_KEY</strong> in Streamlit Secrets to enable AI analysis.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INPUT STAGE
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.stage == "input":

    st.markdown('<div class="section-label">ANALYZE A CALL</div>', unsafe_allow_html=True)

    # Input method tabs
    tab1, tab2, tab3 = st.tabs(["📝  Paste Transcript", "📁  Sample Calls", "🎙️  Upload Audio"])

    with tab1:
        st.markdown('<div class="tab-hint">Paste a raw call transcript below — agent and customer lines, any format.</div>', unsafe_allow_html=True)
        transcript_input = st.text_area(
            label="",
            placeholder="Agent: Thank you for calling Support, how can I help you today?\nCustomer: Hi, I've been charged twice for my subscription...\n...",
            height=280,
            key="transcript_paste"
        )
        if st.button("⚡  Analyze Transcript", key="btn_paste", use_container_width=True):
            if transcript_input.strip():
                st.session_state.transcript = transcript_input.strip()
                st.session_state.stage = "analyzing"
                st.rerun()
            else:
                st.error("Please paste a transcript first.")

    with tab2:
        st.markdown('<div class="tab-hint">Choose from pre-loaded demo calls to explore vocAI\'s capabilities.</div>', unsafe_allow_html=True)
        for idx, sample in enumerate(SAMPLE_CALLS):
            with st.container():
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="sample-card">
                        <div class="sample-title">{sample['title']}</div>
                        <div class="sample-meta">{sample['type']} &nbsp;·&nbsp; {sample['duration']} &nbsp;·&nbsp; {sample['outcome']}</div>
                        <div class="sample-preview">{sample['preview']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
                    if st.button("Analyze →", key=f"sample_{idx}"):
                        st.session_state.transcript = sample["transcript"]
                        st.session_state.stage = "analyzing"
                        st.rerun()

    with tab3:
        st.markdown('<div class="tab-hint">Upload an MP3 or WAV file — transcription powered by Groq Whisper.</div>', unsafe_allow_html=True)
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
    <div class="analyzing-screen">
        <div class="analyzing-orb"></div>
        <div class="analyzing-title">Analyzing your call...</div>
        <div class="analyzing-sub">Running 6-stage intelligence pipeline</div>
    </div>
    """, unsafe_allow_html=True)

    steps = [
        "📄 Extracting summary & issue classification...",
        "😊 Mapping emotional intelligence layer...",
        "🧑‍💼 Scoring agent performance...",
        "💬 Identifying conversation intelligence...",
        "💡 Generating AI coaching recommendations...",
        "📊 Building business strategy insights...",
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
            st.rerun()
        except Exception as e:
            st.error(f"Analysis failed: {e}")
            if st.button("← Go back"):
                st.session_state.stage = "input"
                st.rerun()
    else:
        for i, step in enumerate(steps):
            status_text.markdown(f'<div class="step-text">{step}</div>', unsafe_allow_html=True)
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
    a = st.session_state.analysis

    # ── Reset button ──
    col_r1, col_r2 = st.columns([5, 1])
    with col_r2:
        if st.button("← New Analysis"):
            st.session_state.stage = "input"
            st.session_state.analysis = None
            st.session_state.transcript = ""
            st.rerun()

    # ═══ STAGE 1: INSTANT SUMMARY ═══════════════════════════════════════════
    st.markdown('<div class="stage-header stage-1"><span class="stage-num">01</span> Instant Summary</div>', unsafe_allow_html=True)

    s1 = a.get("stage1", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ISSUE TYPE</div>
            <div class="metric-value">{s1.get('issue_type', 'N/A')}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">CUSTOMER INTENT</div>
            <div class="metric-value">{s1.get('intent', 'N/A')}</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        resolution = s1.get('resolution', 'Unknown')
        color_map = {"Resolved": "#00d68f", "Unresolved": "#ff4d6d", "Escalated": "#ffa94d"}
        color = color_map.get(resolution, "#aaa")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">RESOLUTION</div>
            <div class="metric-value" style="color:{color}">{resolution}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-label">CALL SUMMARY</div>
        <div class="summary-text">{s1.get('summary', 'No summary available.')}</div>
    </div>""", unsafe_allow_html=True)

    # ═══ STAGE 2: EMOTIONAL INTELLIGENCE ════════════════════════════════════
    with st.expander("😊  Stage 2 — Emotional Intelligence", expanded=False):
        s2 = a.get("stage2", {})
        st.markdown('<div class="exp-inner">', unsafe_allow_html=True)

        # Sentiment per stage
        phases = s2.get("sentiment_phases", {})
        cols = st.columns(3)
        emojis = {"Positive": "😊", "Negative": "😠", "Neutral": "😐", "Mixed": "😕"}
        phase_keys = [("beginning", "Beginning"), ("middle", "Middle"), ("end", "End")]
        for i, (key, label) in enumerate(phase_keys):
            val = phases.get(key, "N/A")
            with cols[i]:
                st.markdown(f"""
                <div class="phase-card">
                    <div class="phase-label">{label}</div>
                    <div class="phase-emoji">{emojis.get(val, '🔲')}</div>
                    <div class="phase-value">{val}</div>
                </div>""", unsafe_allow_html=True)

        # Emotion spikes
        spikes = s2.get("emotion_spikes", [])
        if spikes:
            st.markdown('<div class="subsection-label">⚡ Emotion Spikes Detected</div>', unsafe_allow_html=True)
            for spike in spikes:
                emotion_colors = {
                    "Anger": "#ff4d6d", "Frustration": "#ffa94d",
                    "Confusion": "#748ffc", "Satisfaction": "#00d68f"
                }
                ec = emotion_colors.get(spike.get("emotion", ""), "#aaa")
                st.markdown(f"""
                <div class="spike-item">
                    <span class="spike-badge" style="background:{ec}22; color:{ec}; border-color:{ec}44">{spike.get('emotion','')}</span>
                    <span class="spike-desc">{spike.get('description','')}</span>
                </div>""", unsafe_allow_html=True)

        # Critical moments
        critical = s2.get("critical_moments", [])
        if critical:
            st.markdown('<div class="subsection-label">⚠️ Critical Moments</div>', unsafe_allow_html=True)
            for moment in critical:
                st.markdown(f'<div class="critical-item">⚠️ {moment}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ STAGE 3: AGENT SCORECARD ════════════════════════════════════════════
    with st.expander("🧑‍💼  Stage 3 — Agent Performance Scorecard", expanded=False):
        s3 = a.get("stage3", {})
        st.markdown('<div class="exp-inner">', unsafe_allow_html=True)

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
            ("Communication Clarity", s3.get("communication_score", 0), "🗣️"),
            ("Problem-Solving", s3.get("problem_solving_score", 0), "🧠"),
            ("Empathy & Tone", s3.get("empathy_score", 0), "💙"),
            ("Response Speed", s3.get("response_speed_score", 0), "⏱️"),
        ]
        for label, score, icon in sub_scores:
            pct = score * 10
            bar_color = "#00d68f" if score >= 7 else "#ffa94d" if score >= 5 else "#ff4d6d"
            st.markdown(f"""
            <div class="score-bar-row">
                <div class="score-bar-label">{icon} {label}</div>
                <div class="score-bar-track">
                    <div class="score-bar-fill" style="width:{pct}%; background:{bar_color}"></div>
                </div>
                <div class="score-bar-num">{score}/10</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ STAGE 4: CONVERSATION INTELLIGENCE ══════════════════════════════════
    with st.expander("💬  Stage 4 — Conversation Intelligence", expanded=False):
        s4 = a.get("stage4", {})
        st.markdown('<div class="exp-inner">', unsafe_allow_html=True)

        key_sentences = s4.get("key_customer_sentences", [])
        if key_sentences:
            st.markdown('<div class="subsection-label">💬 Key Customer Statements</div>', unsafe_allow_html=True)
            for s in key_sentences:
                st.markdown(f'<div class="quote-block customer-quote">"{s}"</div>', unsafe_allow_html=True)

        best = s4.get("agent_best_reply", "")
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
            moment_icons = {"escalation_point": "🔺", "confusion_point": "❓", "resolution_moment": "✅"}
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

        st.markdown('</div>', unsafe_allow_html=True)

    # ═══ STAGE 5: AI COACHING ════════════════════════════════════════════════
    st.markdown('<div class="stage-header stage-5"><span class="stage-num">05</span> AI Coach Mode</div>', unsafe_allow_html=True)
    s5 = a.get("stage5", {})

    rewrites = s5.get("response_rewrites", [])
    if rewrites:
        st.markdown('<div class="subsection-label">💡 Suggested Response Rewrites</div>', unsafe_allow_html=True)
        for rw in rewrites:
            st.markdown(f"""
            <div class="rewrite-card">
                <div class="rewrite-original"><span class="rw-tag orig-tag">ORIGINAL</span>{rw.get('original','')}</div>
                <div class="rewrite-arrow">↓ Better</div>
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

    # ═══ STAGE 6: BUSINESS DASHBOARD ════════════════════════════════════════
    st.markdown('<div class="stage-header stage-6"><span class="stage-num">06</span> Business Dashboard</div>', unsafe_allow_html=True)
    s6 = a.get("stage6", {})

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
        st.markdown('<div class="biz-card recs-card full-width">', unsafe_allow_html=True)
        st.markdown('<div class="biz-card-title">🧠 AI Recommendations for Teams</div>', unsafe_allow_html=True)
        for rec in team_recs:
            st.markdown(f'<div class="biz-item rec-item">✦ {rec}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="voc-footer">
        vocAI · Powered by Groq &amp; LLaMA · Built for Customer Excellence
    </div>""", unsafe_allow_html=True)
