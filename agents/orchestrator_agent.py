from agents.clarification_agent import clarification_agent
from agents.requirement_agent import requirement_agent
from agents.business_analyst_agent import business_analyst_agent
from agents.architect_agent import architect_agent
from agents.ui_agent import ui_agent
from agents.theme_agent import theme_agent
from agents.validation_agent import validation_agent


def orchestrator_agent(user_command):
    clarification = clarification_agent(user_command)

    requirements = requirement_agent(
        user_command,
        clarification
    )

    ba_output = business_analyst_agent(
        user_command,
        requirements
    )

    architecture = architect_agent(
        user_command,
        requirements,
        ba_output
    )

    ui_json = ui_agent(
        user_command,
        clarification,
        requirements,
        ba_output,
        architecture
    )

    ui_json = theme_agent(ui_json)
    ui_json = validation_agent(ui_json)

    return {
        "clarification": clarification,
        "requirements": requirements,
        "business_analysis": ba_output,
        "architecture": architecture,
        "ui_json": ui_json
    }