import json
from agents.llm_client import ask_llm


SUPPORTED_CAPABILITIES = {
    "layouts": ["tabs", "sidebar"],
    "components": [
        "text_input",
        "text_area",
        "selectbox",
        "date_input",
        "file_upload",
        "button",
        "service_cards",
        "result_cards"
    ],
    "themes": [
        "primary_color",
        "secondary_color",
        "background_color",
        "header_font_size",
        "body_font_size",
        "card_radius"
    ],
    "unsupported": [
        "hover sidebar",
        "drag and drop builder",
        "animated menus",
        "custom JavaScript",
        "custom React components",
        "floating panels",
        "canvas drawing",
        "real-time multiplayer",
        "advanced charts"
    ]
}


def capability_agent(modification_request):
    prompt = f"""
You are a Capability Check Agent.

User customization request:
{modification_request}

Current renderer capabilities:
{json.dumps(SUPPORTED_CAPABILITIES, indent=2)}

Return ONLY valid JSON:

{{
  "supported": true,
  "reason": "short reason",
  "safe_alternative": "safe alternative if unsupported",
  "required_renderer_change": "code/rendering change needed if unsupported"
}}
"""

    result = ask_llm(
        "You check whether a UI customization is supported by the current Streamlit renderer.",
        prompt
    )

    return json.loads(result)