import json
from agents.llm_client import ask_llm


def output_formatting_agent(raw_output, action_label="", app_context=None):
    prompt = f"""
You are an Output Formatting Agent.

Your job is to convert raw backend/action output into clean UI-safe output.

Action label:
{action_label}

Raw output:
{raw_output}

App context:
{app_context}

Return ONLY valid JSON in this format:

{{
  "display_type": "success_message | markdown | table | cards | warning",
  "title": "Short display title",
  "message": "Clean message to show to the user",
  "columns": [],
  "rows": [],
  "cards": [
    {{
      "title": "Card title",
      "description": "Card description",
      "value": "Optional value"
    }}
  ]
}}

Rules:
- Never show raw JSON to the user.
- If the raw output is backend-style JSON, summarize it into a clean success message.
- If the action is Add Task, Create Task, Save, Submit, or Update, use display_type = success_message.
- If there are multiple findings, use cards or table.
- If something is missing or blocked, use warning.
- Keep output user-friendly.
"""

    result = ask_llm(
        "You format raw execution output into clean UI display JSON.",
        prompt
    )

    return json.loads(result)