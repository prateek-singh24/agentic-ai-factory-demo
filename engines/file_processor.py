import json
import pandas as pd
from pypdf import PdfReader


def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    try:
        if file_name.endswith(".json"):
            data = json.load(uploaded_file)
            return json.dumps(data, indent=2)

        elif file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            return df.head(100).to_string(index=False)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            return df.head(100).to_string(index=False)

        elif file_name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")

        elif file_name.endswith(".pdf"):
            reader = PdfReader(uploaded_file)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text[:15000]

        else:
            return f"Unsupported file type: {uploaded_file.name}"

    except Exception as e:
        return f"Error reading file {uploaded_file.name}: {str(e)}"