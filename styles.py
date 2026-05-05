import streamlit as st
import os
from groq import Groq
import time
from analyzer import analyze_transcript
from sample_calls import SAMPLE_CALLS
from styles import inject_styles

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="vocAI – Call Intelligence",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_styles()

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "input"

if "active_section" not in st.session_state:
    st.session_state.active_section = 1

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# ─────────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION (BIRD’S EYE VIEW)
# ─────────────────────────────────────────────────────────────
st.sidebar.title("📊 Call Intelligence Flow")

st.sidebar.markdown("### Navigation")

sections = {
    1: "📄 Instant Summary",
    2: "😊 Emotional Intelligence",
    3: "🧑‍💼 Agent Performance",
    4: "💬 Conversation Insights",
    5: "✉️ Email Generator",
    6: "🧠 AI Coach"
}

status_map = {
    "not_started": "⚪",
    "active": "🟣",
    "completed": "🟢"
}

def get_status(i):
    if st.session_state.analysis is None:
        return "not_started"
    if st.session_state.active_section == i:
        return "active"
    if st.session_state.active_section > i:
        return "completed"
    return "not_started"

for i, label in sections.items():
    status = get_status(i)
    if st.sidebar.button(f"{status_map[status]} {label}", key=f"nav_{i}"):
        st.session_state.active_section = i


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:20px;">
    <h1 style="color:#7c3aed;">vocAI</h1>
    <p style="color:#666;">AI-Powered Customer Call Intelligence Dashboard</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# INPUT STAGE
# ─────────────────────────────────────────────────────────────
if st.session_state.stage == "input":

    st.subheader("📥 Input Call Data")

    tab1, tab2 = st.tabs(["Paste Transcript", "Sample Calls"])

    with tab1:
        transcript = st.text_area("Paste call transcript", height=250)

        if st.button("Analyze Call"):
            if transcript.strip():
                st.session_state.transcript = transcript
                st.session_state.stage = "analyzing"
                st.rerun()

    with tab2:
        for i, sample in enumerate(SAMPLE_CALLS):
            st.markdown(f"### {sample['title']}")
            if st.button(f"Use Sample {i+1}"):
                st.session_state.transcript = sample["transcript"]
                st.session_state.stage = "analyzing"
                st.rerun()


# ─────────────────────────────────────────────────────────────
# ANALYSIS STAGE
# ─────────────────────────────────────────────────────────────
elif st.session_state.stage == "analyzing":

    st.info("Analyzing call... please wait")

    progress = st.progress(0)

    steps = [
        "Summarizing call",
        "Detecting sentiment",
        "Scoring agent",
        "Extracting insights",
        "Generating recommendations",
        "Finalizing report"
    ]

    for i, s in enumerate(steps):
        progress.progress((i+1)/len(steps))
        time.sleep(0.4)

    result = analyze_transcript(st.session_state.transcript, os.getenv("GROQ_API_KEY"))
    st.session_state.analysis = result
    st.session_state.stage = "results"
    st.rerun()


# ─────────────────────────────────────────────────────────────
# RESULTS DASHBOARD
# ─────────────────────────────────────────────────────────────
elif st.session_state.stage == "results":

    a = st.session_state.analysis

    section = st.session_state.active_section


    # ───────────────────── STAGE 1 ─────────────────────
    if section == 1:
        st.header("📄 Instant Summary")

        st.markdown(f"""
        ### Issue Type
        {a['stage1']['issue_type']}

        ### Intent
        {a['stage1']['intent']}

        ### Resolution
        **{a['stage1']['resolution']}**

        ---

        ### Summary
        {a['stage1']['summary']}
        """)


    # ───────────────────── STAGE 2 ─────────────────────
    elif section == 2:
        st.header("😊 Emotional Intelligence")

        st.markdown("### Sentiment Journey")
        st.json(a["stage2"]["sentiment_phases"])

        st.markdown("### Emotion Spikes")
        st.json(a["stage2"]["emotion_spikes"])


    # ───────────────────── STAGE 3 ─────────────────────
    elif section == 3:
        st.header("🧑‍💼 Agent Performance")

        st.metric("Overall Score", a["stage3"]["overall_score"])

        st.write(a["stage3"])


    # ───────────────────── STAGE 4 ─────────────────────
    elif section == 4:
        st.header("💬 Conversation Insights")

        st.write("Key Moments")
        st.json(a["stage4"])


    # ───────────────────── STAGE 5 EMAIL GENERATOR ─────────────────────
    elif section == 5:
        st.header("✉️ Call-Based Email Generator")

        resolution = a["stage1"]["resolution"]

        customer_name = "Customer"
        ticket = "AUTO-Generated-001"

        if resolution == "Resolved":
            email = f"""
Subject: Your issue has been resolved – We’re here if you need anything else

Hi {customer_name},

We’re happy to inform you that your issue has been resolved successfully.

Summary:
{a['stage1']['summary']}

We truly appreciate your patience and thank you for contacting support.

If you have a moment, we’d love your feedback:
👉 [Feedback Link]

Best regards,  
Support Team
"""
        
        elif resolution == "Unresolved":
            email = f"""
Subject: Update on your support request – We're working on it

Hi {customer_name},

Thank you for reaching out. We’re actively working on your issue.

Current Status:
{a['stage1']['summary']}

Next Steps:
- Investigation in progress
- Team is reviewing your case
- Expected update within 24–48 hours

We appreciate your patience.

Best regards,  
Support Team
"""

        else:
            email = f"""
Subject: Your request has been escalated for faster resolution

Hi {customer_name},

Your issue has been escalated to our specialized team.

What’s happening:
{a['stage1']['summary']}

Handled by: Senior Support Team  
Expected response time: 24 hours

We assure you this is being prioritized.

Best regards,  
Support Team
"""

        st.code(email)


    # ───────────────────── STAGE 6 COACH ─────────────────────
    elif section == 6:
        st.header("🧠 AI Coach Insights")

        st.write(a["stage5"])


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("vocAI • AI Call Intelligence System")
