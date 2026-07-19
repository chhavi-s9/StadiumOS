"""
=========================================================
prompts.py

Prompt templates for StadiumOS AI.

Responsibilities
----------------
- Crowd analysis
- Incident analysis
- Operational recommendations
- Executive summaries

=========================================================
"""

# =========================================================
# CROWD ANALYSIS
# =========================================================

CROWD_ANALYSIS_PROMPT = """
You are an AI Crowd Operations Specialist for FIFA World Cup 2026.

Analyze the following stadium data.

Current Zone:
{zone}

Crowd Density:
{density}

Incidents:
{incidents}

Provide:

1. Risk Level
2. Explanation
3. Recommended Action

Return ONLY valid JSON.

Example:

{{
  "risk": "HIGH",
  "reason": "...",
  "recommendation": "..."
}}
"""


# =========================================================
# INCIDENT ANALYSIS
# =========================================================

INCIDENT_RESPONSE_PROMPT = """
You are an AI Emergency Operations Coordinator.

Incident Type:
{incident_type}

Severity:
{severity}

Location:
{location}

Recommend:

- Immediate response
- Staff deployment
- Fan communication

Return ONLY JSON.
"""


# =========================================================
# VOLUNTEER DISPATCH
# =========================================================

VOLUNTEER_PROMPT = """
You are managing FIFA stadium volunteers.

Task:
{task}

Available Volunteers:
{volunteers}

Recommend:

- Which volunteer should respond
- Priority
- Reason

Return ONLY JSON.
"""


# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

SUMMARY_PROMPT = """
Summarize the current stadium situation.

Data:

{state}

Provide:

- Overall status
- Highest priority issue
- Recommended next action

Maximum 120 words.
"""