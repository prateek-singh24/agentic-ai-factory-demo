def validation_agent(ui_json):
    if not isinstance(ui_json, dict):
        ui_json = {}

    ui_json.setdefault("app_title", "Generated App")
    ui_json.setdefault("subtitle", "")
    ui_json.setdefault("hero_icon", "✨")
    ui_json.setdefault("metrics", [])
    ui_json.setdefault("pages", [])
    ui_json.setdefault("theme", {})

    used_keys = set()

    for page_index, page in enumerate(ui_json["pages"]):
        page.setdefault("page_title", f"Page {page_index + 1}")
        page.setdefault("components", [])

        for comp_index, comp in enumerate(page["components"]):
            if "type" not in comp:
                comp["type"] = "text_input"

            if "label" not in comp:
                comp["label"] = comp["type"].replace("_", " ").title()

            if "key" not in comp:
                comp["key"] = f"page_{page_index}_component_{comp_index}"

            original_key = comp["key"]
            counter = 1

            while comp["key"] in used_keys:
                comp["key"] = f"{original_key}_{counter}"
                counter += 1

            used_keys.add(comp["key"])

    return ui_json