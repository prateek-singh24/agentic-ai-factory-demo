import json
from agents.llm_client import ask_llm


def customization_agent(existing_ui_json, modification_request):
    prompt = f"""
You are a UI customization agent.

Existing UI JSON:
{json.dumps(existing_ui_json, indent=2)}

User modification request:
{modification_request}

Update the existing UI JSON.

Rules:
- Return ONLY valid JSON.
- Preserve the existing app unless the user asks to remove something.
- Apply all requested customizations.
- Only use supported layouts: tabs, sidebar.
- Only use supported components: text_input, text_area, selectbox, date_input, file_upload, button, service_cards, result_cards.
- Only use supported theme properties: primary_color, secondary_color, background_color, header_font_size, body_font_size, card_radius.
- If user asks for left navigation or sidebar, set "layout_type": "sidebar".
- If user asks for tabs, set "layout_type": "tabs".
- If user asks for dropdowns, add selectbox components.
- If user asks for inputs, add text_input or text_area components.
- If user asks for bigger/smaller font, update theme font sizes.
- Do not create hover interactions, animations, JavaScript behavior, React components, drag-drop, or unsupported layouts.
- Every key must be unique.
"""

    result = ask_llm(
        "You customize existing generated app JSON based on supported renderer instructions.",
        prompt
    )

    return json.loads(result)