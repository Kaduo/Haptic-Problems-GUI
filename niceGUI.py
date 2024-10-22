#Si la réglette {self.r1.color} mesure {self.l1} cm, combien mesure la réglette {self.r2.color} ?
from enum import Enum
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

class Color(Enum):
    WHITE = "#c8c8c8"
    RED = "#e62937"
    GREEN = "#00e430"
    PURPLE = "#c87aff"
    YELLOW = "#fdf900"
    DARK_GREEN = "#00752c"
    BLACK = "#000000"
    BROWN = "#7f6a4f"
    BLUE = "#0079f1"
    ORANGE = "#ffa100"

    def __str__(self):
        match self:
            case Color.WHITE:
                return "blanche"
            case Color.RED:
                return "rouge"
            case Color.GREEN:
                return "verte"
            case Color.PURPLE:
                return "mauve"
            case Color.YELLOW:
                return "jaune"
            case Color.DARK_GREEN:
                return "vert foncé"
            case Color.BLACK:
                return "noire"
            case Color.BROWN:
                return "marron"
            case Color.BLUE:
                return "bleue"
            case Color.ORANGE:
                return "orange"


class Rod:
    def __init__(self, length):
        self.length = length
        self.color = list(Color)[self.length - 1]



# def show(event: ValueChangeEventArguments):
#     name = type(event.sender).__name__
#     ui.notify(f'{name}: {event.value}')

rod1 = Rod(1)
rod2 = Rod(2)



def colored_label(text_parts, colors):
    # Create HTML code with colored parts
    html_content = "".join(
        f'<span style="color: {color};">{text}</span>' 
        for text, color in zip(text_parts, colors)
    )
    return html_content


text_parts = ["Si la réglette ", f"{rod1.color}", f" mesure {rod1.length} cm, combien mesure la réglette ",f"{rod2.color}"," ?"]
colors = ["black", rod1.color.value, "black", rod2.color.value, "black"]

ui.add_body_html("""
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
    </style>
""")

with ui.column().style("align-items: center;"):
    problem_statement = ui.html(colored_label(text_parts, colors))
    ui.input('Ta réponse : ')
    ui.button('Valider', on_click=lambda: problem_statement.set_content("hello"))
ui.run()