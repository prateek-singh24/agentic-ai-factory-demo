from agents.llm_client import ask_llm


def business_analyst_agent(user_command, requirements):
    prompt = f"""
User request:
{user_command}

Requirements:
{requirements}

Create:
1. User stories
2. Acceptance criteria
3. Main workflows
4. Business rules
5. Sample user journeys
"""

    return ask_llm(
        "You are a Business Analyst Agent.",
        prompt
    )