from agents.llm_client import ask_llm


def architect_agent(user_command, requirements, ba_output):
    prompt = f"""
User request:
{user_command}

Requirements:
{requirements}

Business Analysis:
{ba_output}

Create:
1. Solution architecture
2. UI modules
3. Backend modules
4. API design
5. Data model
6. Security considerations
7. Deployment considerations
"""

    return ask_llm(
        "You are a Solution Architect Agent.",
        prompt
    )