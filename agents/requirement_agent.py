from agents.llm_client import ask_llm


def requirement_agent(user_command, clarification):
    prompt = f"""
User request:
{user_command}

Clarification:
{clarification}

Create requirements for this app.

Return:
1. Business objective
2. Functional requirements
3. Non-functional requirements
4. User roles
5. Main modules
6. Customization requirements
"""

    return ask_llm(
        "You are a Requirement Analysis Agent.",
        prompt
    )