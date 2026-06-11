def theme_agent(ui_json):
    if "theme" not in ui_json:
        ui_json["theme"] = {}

    defaults = {
        "primary_color": "#0f5fb8",
        "secondary_color": "#2994ff",
        "background_color": "#f7f9fc",
        "header_font_size": "42px",
        "body_font_size": "16px",
        "card_radius": "16px"
    }

    for key, value in defaults.items():
        if key not in ui_json["theme"]:
            ui_json["theme"][key] = value

    return ui_json