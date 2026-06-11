from agents.llm_client import ask_llm


def clarification_agent(user_command):
    prompt = f"""
User request:
{user_command}

Analyze whether the request is clear enough to build a dynamic app.

Return:
1. Interpreted intent
2. App type
3. Key features requested
4. Missing information, if any
5. Assumptions to proceed
"""

    return ask_llm(
        "You are a Clarification Agent. You interpret vague user requests and make practical assumptions.",
        prompt
    )