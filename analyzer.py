import json
import time
from groq import Groq

ANALYSIS_PROMPT = """You are vocAI, an expert customer service call analyzer. Analyze the given transcript and return a complete JSON analysis.

Return ONLY valid JSON — no markdown, no explanation, no backticks.

The JSON must follow this exact structure:
{
  "stage1": {
    "summary": "5-10 sentence summary of the full call",
    "issue_type": "one of: Billing / Technical / Cancellation / Complaint / Inquiry / Upgrade",
    "intent": "one of: Refund / Support / Upgrade / Complaint / Inquiry / Cancellation",
    "resolution": "one of: Resolved / Unresolved / Escalated"
  },
  "stage2": {
    "sentiment_phases": {
      "beginning": "one of: Positive / Neutral / Negative / Mixed",
      "middle": "one of: Positive / Neutral / Negative / Mixed",
      "end": "one of: Positive / Neutral / Negative / Mixed"
    },
    "emotion_spikes": [
      {"emotion": "Anger/Frustration/Confusion/Satisfaction", "description": "brief description of what triggered it"},
      {"emotion": "...", "description": "..."}
    ],
    "critical_moments": [
      "description of critical emotional moment 1",
      "description of critical emotional moment 2"
    ]
  },
  "stage3": {
    "overall_score": 7,
    "communication_score": 7,
    "problem_solving_score": 6,
    "empathy_score": 8,
    "response_speed_score": 7
  },
  "stage4": {
    "key_customer_sentences": [
      "most important thing the customer said",
      "second most important customer statement",
      "third key customer statement"
    ],
    "agent_best_reply": "the single best thing the agent said",
    "agent_worst_reply": "the weakest or most problematic thing the agent said",
    "critical_moments": {
      "escalation_point": "description of when/if escalation occurred",
      "confusion_point": "description of a moment of confusion or miscommunication",
      "resolution_moment": "description of when/if resolution occurred"
    }
  },
  "stage5": {
    "response_rewrites": [
      {
        "original": "something the agent actually said that could be improved",
        "improved": "a better way to say it"
      },
      {
        "original": "another agent statement to improve",
        "improved": "improved version"
      }
    ],
    "ideal_resolution_pathway": [
      "Step 1: ...",
      "Step 2: ...",
      "Step 3: ...",
      "Step 4: ...",
      "Step 5: ..."
    ],
    "mistake_summary": [
      "Key mistake 1 the agent made",
      "Key mistake 2",
      "Key mistake 3"
    ]
  },
  "stage6": {
    "ai_recommendations": [
      "Recommendation for the team",
      "Second recommendation",
      "Third recommendation"
    ],
    "coaching_tips": [
      "Coaching tip for agents",
      "Second tip",
      "Third tip"
    ],
    "escalation_suggestions": [
      "When to escalate earlier in future calls",
      "Second trigger",
      "Third trigger"
    ],
    "upsell_opportunities": [
      "Upsell/cross-sell opportunity detected",
      "Second opportunity if any"
    ],
    "strategic_insights": [
      "Pattern or strategic insight from this call",
      "Second insight",
      "Third insight"
    ]
  }
}

Be specific and insightful. All scores must be integers between 1 and 10.
Emotion spikes should have 2-4 items. Keep all text concise and actionable.
"""


def analyze_transcript(transcript: str, api_key: str, progress_bar, status_text, steps) -> dict:
    client = Groq(api_key=api_key)

    # Simulate staged progress while making single API call
    status_text.markdown(f'<div class="step-text">{steps[0]}</div>', unsafe_allow_html=True)
    progress_bar.progress(0.1)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": ANALYSIS_PROMPT},
            {"role": "user", "content": f"Analyze this call transcript:\n\n{transcript}"}
        ],
        temperature=0.3,
        max_tokens=4000,
    )

    raw = response.choices[0].message.content.strip()

    # Animate through steps
    for i, step in enumerate(steps[1:], 2):
        status_text.markdown(f'<div class="step-text">{step}</div>', unsafe_allow_html=True)
        progress_bar.progress(i / len(steps))
        time.sleep(0.35)

    # Clean and parse JSON
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            result = json.loads(raw[start:end])
        else:
            raise ValueError(f"Could not parse JSON from response: {raw[:200]}")

    progress_bar.progress(1.0)
    return result


# For local testing
if __name__ == "__main__":
    import os
    key = os.environ.get("GROQ_API_KEY", "")
    sample = """Agent: Thank you for calling. How can I help?
Customer: I was billed twice this month and I'm very upset.
Agent: I'm sorry. Let me look into that for you.
Customer: This has happened before. This is unacceptable.
Agent: I apologize. I'll file a ticket and get back to you in 3-5 days.
Customer: Fine. Goodbye."""

    class FakeProgress:
        def progress(self, v): pass

    class FakeStatus:
        def markdown(self, v, **kw): pass

    result = analyze_transcript(sample, key, FakeProgress(), FakeStatus(), ["s"]*6)
    print(json.dumps(result, indent=2))
