import yaml
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

def load_models_from_config(file_path="config.yml"):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("models", [])

def select_model(models):
    selected_index = [0]  # Use list for mutability in nested scope

    style = Style.from_dict({
        "selected": "bg:#ffffa0 #000ff0",  # Yellow background, black text
        "default": ""
    })

    def get_text():
        lines = []
        for i, model in enumerate(models):
            if i == selected_index[0]:
                lines.append([("class:selected", f"> {model}\n")])
            else:
                lines.append([("class:default", f"  {model}\n")])
        return sum(lines, [])

    control = FormattedTextControl(get_text)
    window = Window(content=control, always_hide_cursor=True)
    root_container = HSplit([window])
    layout = Layout(root_container)

    kb = KeyBindings()

    @kb.add("up")
    def up(event):
        selected_index[0] = (selected_index[0] - 1) % len(models)
        event.app.invalidate()

    @kb.add("down")
    def down(event):
        selected_index[0] = (selected_index[0] + 1) % len(models)
        event.app.invalidate()

    @kb.add("enter")
    def enter(event):
        event.app.exit(result=models[selected_index[0]])

    application = Application(layout=layout, key_bindings=kb, full_screen=False, style=style)
    print("Select a model to use:\n")
    return application.run()
