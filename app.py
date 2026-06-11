import streamlit as st

from agents.orchestrator_agent import orchestrator_agent
from agents.customization_agent import customization_agent
from agents.validation_agent import validation_agent
from agents.theme_agent import theme_agent
from agents.capability_agent import capability_agent
from agents.output_formatting_agent import output_formatting_agent
from engines.generic_executor import generic_executor

st.set_page_config(
    page_title="Agentic AI Software Factory",
    layout="wide"
)

BASE_CSS = """
<style>
.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.hero h1 {
    margin-bottom: 8px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #e8edf5;
    margin-bottom: 18px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 1px solid #e8edf5;
}

.metric-title {
    font-size: 14px;
    color: #607089;
}

.metric-value {
    font-size: 24px;
    font-weight: 800;
    color: #052b5f;
}

.service-card {
    background: #e8f2ff;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
    color: #004b9b;
    font-weight: 500;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
    color: #14213d;
}

.stButton > button {
    border-radius: 10px;
    height: 45px;
    font-weight: 600;
}
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)

if "agent_outputs" not in st.session_state:
    st.session_state.agent_outputs = None

if "customization_history" not in st.session_state:
    st.session_state.customization_history = []


st.title("Agentic AI Software Factory")

user_command = st.text_area(
    "What do you want to build?",
    placeholder=(
        "Example: Create a day-to-day office activity organizer with task planning, "
        "meeting tracking, reminders, priority dashboard, and daily summary."
    ),
    height=120
)

if st.button("Generate App", use_container_width=True):
    with st.spinner(
        "10-agent workflow running: Clarification → Requirements → BA → Architecture → UI → Theme → Validation"
    ):
        try:
            st.session_state.agent_outputs = orchestrator_agent(user_command)
            st.session_state.customization_history = []
            st.success("App generated successfully.")
        except Exception as e:
            st.error("Generation failed.")
            st.write(e)


def apply_dynamic_theme(app):
    theme = app.get("theme", {})

    primary = theme.get("primary_color", "#0f5fb8")
    secondary = theme.get("secondary_color", "#2994ff")
    background = theme.get("background_color", "#f7f9fc")
    header_font_size = theme.get("header_font_size", "42px")
    body_font_size = theme.get("body_font_size", "16px")
    card_radius = theme.get("card_radius", "16px")

    st.markdown(f"""
    <style>
    .main {{
        background-color: {background};
    }}

    .hero {{
        background: linear-gradient(135deg, {primary}, {secondary});
    }}

    .hero h1 {{
        font-size: {header_font_size};
    }}

    body, p, label, div {{
        font-size: {body_font_size};
    }}

    .card {{
        border-radius: {card_radius};
    }}

    .metric-card {{
        border-radius: {card_radius};
    }}
    </style>
    """, unsafe_allow_html=True)


def render_formatted_output(formatted_output):
    display_type = formatted_output.get("display_type", "markdown")
    title = formatted_output.get("title", "")
    message = formatted_output.get("message", "")

    if display_type == "success_message":
        st.success(message or title or "Action completed successfully.")

    elif display_type == "warning":
        st.warning(message or title or "Action could not be completed.")

    elif display_type == "table":
        rows = formatted_output.get("rows", [])
        if title:
            st.subheader(title)
        if message:
            st.write(message)
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No table records available.")

    elif display_type == "cards":
        if title:
            st.subheader(title)
        if message:
            st.write(message)

        cards = formatted_output.get("cards", [])
        if not cards:
            st.info("No cards available.")
            return

        for card in cards:
            st.markdown(f"""
            <div class="card">
                <h4>{card.get("title", "")}</h4>
                <p>{card.get("description", "")}</p>
                <b>{card.get("value", "")}</b>
            </div>
            """, unsafe_allow_html=True)

    else:
        if title:
            st.subheader(title)
        st.markdown(message or "Action completed.")


def collect_runtime_inputs():
    inputs = {}
    uploaded_files = {}

    for session_key, value in st.session_state.items():
        if hasattr(value, "name"):
            uploaded_files[session_key] = value
        elif isinstance(value, (str, int, float, bool)):
            inputs[session_key] = value

    return inputs, uploaded_files


def render_component(component, index):
    ctype = component.get("type")
    label = component.get("label", "")
    key = component.get("key", f"component_{index}")

    if ctype == "text_input":
        st.text_input(
            label,
            placeholder=component.get("placeholder", ""),
            key=key
        )

    elif ctype == "text_area":
        st.text_area(
            label,
            placeholder=component.get("placeholder", ""),
            key=key
        )

    elif ctype == "selectbox":
        st.selectbox(
            label,
            component.get("options", ["Option 1", "Option 2"]),
            key=key
        )

    elif ctype == "date_input":
        st.date_input(label, key=key)

    elif ctype == "file_upload":
        st.file_uploader(label, key=key)

    elif ctype == "button":
        if st.button(label, key=key, use_container_width=True):
            with st.spinner("Running action..."):
                inputs, uploaded_files = collect_runtime_inputs()

                raw_output = generic_executor(
                    action=component.get("action", label),
                    inputs=inputs,
                    uploaded_files=uploaded_files,
                    app_context=st.session_state.agent_outputs
                )

                formatted_output = output_formatting_agent(
                    raw_output=raw_output,
                    action_label=label,
                    app_context=st.session_state.agent_outputs
                )

                render_formatted_output(formatted_output)

    elif ctype == "service_cards":
        for item in component.get("items", []):
            st.markdown(
                f"<div class='service-card'>{item}</div>",
                unsafe_allow_html=True
            )

    elif ctype == "result_cards":
        for item in component.get("items", []):
            st.markdown(f"""
            <div class="card">
                <h4>{item.get("title", "")}</h4>
                <p>{item.get("description", "")}</p>
                <b>{item.get("value", "")}</b>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning(f"Unsupported component type: {ctype}")


def render_page(page):
    st.markdown(
        f"<div class='section-title'>{page.get('page_title', 'Page')}</div>",
        unsafe_allow_html=True
    )

    components = page.get("components", [])
    left, right = st.columns([1.3, 1])

    for i, component in enumerate(components):
        target = left if i % 2 == 0 else right
        with target:
            render_component(component, i)


def render_dynamic_app(app):
    apply_dynamic_theme(app)

    st.divider()

    st.markdown(f"""
    <div class="hero">
        <h1>{app.get("hero_icon", "✨")} {app.get("app_title", "Generated App")}</h1>
        <p>{app.get("subtitle", "")}</p>
    </div>
    """, unsafe_allow_html=True)

    metrics = app.get("metrics", [])
    if metrics:
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{metric.get("label", "")}</div>
                    <div class="metric-value">{metric.get("value", "")}</div>
                </div>
                """, unsafe_allow_html=True)

    pages = app.get("pages", [])

    if not pages:
        st.warning("No pages were generated.")
        return

    layout_type = app.get("layout_type", "tabs")

    if layout_type == "sidebar":
        with st.sidebar:
            st.markdown("## Navigation")
            selected_page_name = st.radio(
                "Go to",
                [p.get("page_title", "Page") for p in pages],
                label_visibility="collapsed"
            )

        selected_page = next(
            p for p in pages
            if p.get("page_title", "Page") == selected_page_name
        )

        render_page(selected_page)

    elif layout_type == "tabs":
        tabs = st.tabs([p.get("page_title", "Page") for p in pages])

        for tab, page in zip(tabs, pages):
            with tab:
                render_page(page)

    else:
        st.warning(
            f"Layout '{layout_type}' is not supported by the current renderer. "
            "Supported layouts are: tabs and sidebar."
        )


if st.session_state.agent_outputs:
    outputs = st.session_state.agent_outputs

    st.subheader("Customize Existing App")

    modification_request = st.text_area(
        "Tell the builder what to change",
        placeholder=(
            "Example: Make the theme green, add 5 dropdowns, move navigation to sidebar, "
            "make the header bigger and body text smaller."
        ),
        height=100
    )

    if st.button("Apply Customization", use_container_width=True):
        with st.spinner("Checking whether this customization is supported..."):
            try:
                capability_result = capability_agent(modification_request)

                if not capability_result.get("supported", False):
                    st.warning("This customization is not supported by the current UI renderer.")

                    st.write("Reason:")
                    st.write(capability_result.get("reason", ""))

                    st.write("Safe alternative:")
                    st.write(capability_result.get("safe_alternative", ""))

                    st.write("Renderer change needed:")
                    st.write(capability_result.get("required_renderer_change", ""))

                else:
                    updated_ui = customization_agent(
                        st.session_state.agent_outputs["ui_json"],
                        modification_request
                    )

                    updated_ui = theme_agent(updated_ui)
                    updated_ui = validation_agent(updated_ui)

                    st.session_state.agent_outputs["ui_json"] = updated_ui
                    st.session_state.customization_history.append(modification_request)

                    st.success("Customization applied.")

            except Exception as e:
                st.error("Customization failed.")
                st.write(e)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Generated App",
        "Clarification",
        "Requirements",
        "Business Analysis",
        "Architecture",
        "Customization History"
    ])

    with tab1:
        render_dynamic_app(outputs["ui_json"])

    with tab2:
        st.markdown(outputs["clarification"])

    with tab3:
        st.markdown(outputs["requirements"])

    with tab4:
        st.markdown(outputs["business_analysis"])

    with tab5:
        st.markdown(outputs["architecture"])

    with tab6:
        if st.session_state.customization_history:
            for i, item in enumerate(st.session_state.customization_history, start=1):
                st.write(f"{i}. {item}")
        else:
            st.write("No customizations applied yet.")