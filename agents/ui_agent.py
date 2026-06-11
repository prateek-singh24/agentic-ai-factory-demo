import json
from agents.llm_client import ask_llm


def ui_agent(user_command, clarification, requirements, ba_output, architecture):
    prompt = f"""
You are an expert UI/UX product designer.

User request:
{user_command}

Clarification:
{clarification}

Requirements:
{requirements}

Business Analysis:
{ba_output}

Architecture:
{architecture}

Return ONLY valid JSON.

Use this exact JSON structure:

{{
  "app_title": "App title",
  "subtitle": "Short subtitle",
  "hero_icon": "emoji",
  "theme": {{
    "primary_color": "#0f5fb8",
    "secondary_color": "#2994ff",
    "background_color": "#f7f9fc",
    "header_font_size": "42px",
    "body_font_size": "16px",
    "card_radius": "16px"
  }},
  "metrics": [
    {{"label": "Metric name", "value": "Metric value"}}
  ],
  "pages": [
    {{
      "page_title": "Page title",
      "components": [
        {{
          "type": "text_input",
          "label": "Input label",
          "key": "unique_key",
          "placeholder": "placeholder text"
        }},
        {{
          "type": "text_area",
          "label": "Textarea label",
          "key": "unique_key",
          "placeholder": "placeholder text"
        }},
        {{
          "type": "selectbox",
          "label": "Select label",
          "key": "unique_key",
          "options": ["Option 1", "Option 2"]
        }},
        {{
          "type": "date_input",
          "label": "Date label",
          "key": "unique_key"
        }},
        {{
          "type": "file_upload",
          "label": "Upload file",
          "key": "unique_key"
        }},
        {{
          "type": "button",
          "label": "Button label",
          "key": "unique_key",
          "action": "Describe what this button should do"
        }},
        {{
          "type": "service_cards",
          "items": ["Service 1", "Service 2"]
        }},
        {{
          "type": "result_cards",
          "items": [
            {{"title": "Card title", "description": "Card description", "value": "Important value"}}
          ]
        }}
      ]
    }}
  ]
}}

Rules:
- Create a polished website-like UI.
- Create 3 to 5 pages/tabs.
- Use realistic fields, dropdowns, cards, buttons, and sample data.
- Every key must be unique.
- If user asks for colors, fonts, extra dropdowns, inputs, or layout changes, include them.
- Return JSON only.
"""

    result = ask_llm(
        "You generate polished JSON UI definitions for dynamic apps.",
        prompt
    )

    return json.loads(result)