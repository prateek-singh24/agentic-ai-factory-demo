from agents.llm_client import ask_llm
from engines.file_processor import read_uploaded_file


def generic_executor(action, inputs, uploaded_files, app_context=None):
    processed_files = {}

    for key, uploaded_file in uploaded_files.items():
        processed_files[key] = {
            "file_name": uploaded_file.name if uploaded_file else None,
            "content": read_uploaded_file(uploaded_file)
        }

    prompt = f"""
You are a Generic AI Application Execution Engine.

The generated app has this context:
{app_context}

The user clicked this action:
{action}

User inputs:
{inputs}

Uploaded files extracted content:
{processed_files}

Perform the requested action using the available inputs and uploaded file contents.

Rules:
- Do not say this is a mock result if actual uploaded content is available.
- If required files are missing, clearly say which files are missing.
- If extraction is incomplete, say what could not be read.
- Give practical, structured output.
- For comparison/reconciliation tasks, show discrepancies in a table-like format.
- For document analysis, show source evidence where possible.
- For classification, show categories and confidence.
- For dashboard tasks, summarize key metrics and findings.
"""

    return ask_llm(
        "You execute dynamic app actions using uploaded files and user inputs.",
        prompt
    )