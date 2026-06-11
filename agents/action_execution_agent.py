from agents.llm_client import ask_llm


def action_execution_agent(action, app_context=None):
    prompt = f"""
The user clicked this button/action inside the generated app:

Action:
{action}

App context:
{app_context}

Generate a practical, structured output.
"""

    return ask_llm(
        "You are an Action Execution Agent inside a generated app.",
        prompt
    )