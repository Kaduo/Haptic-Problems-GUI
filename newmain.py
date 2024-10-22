from nicegui import ui
from problems import Problem, Rod, Color, Fraction
from generate_problems import send_problems
from websockets.sync.client import connect

NB_PROBLEMS = 20

def colored_label(text_parts, colors):
    # Create HTML code with colored parts
    html_content = "".join(
        f'<span style="color: {color};">{text}</span>' 
        for text, color in zip(text_parts, colors)
    )
    return html_content

def get_problem_statement(problem):
    text_parts = ["Si la réglette ", f"{problem.r1.color}", f" mesure {problem.l1} cm, combien mesure la réglette ",f"{problem.r2.color}"," ?"]
    colors = ["black", problem.r1.color.value, "black", problem.r2.color.value, "black"]
    return colored_label(text_parts, colors)


class App:

    def __init__(self):
        self.websocket = connect("ws://192.168.1.9:8080")
        self.problem_id = 0
        self.statement = ui.html()
        self.input = ui.input("Ta réponse : ")
        self.load_next_problem()
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
            self.statement
            self.input
            ui.button('Valider', on_click=lambda: self.check_answer(self.input.value))
        ui.run()


    def load_next_problem(self):
        self.current_problem = Problem.load(f"problem_set/problem{self.problem_id}.prob")
        self.statement.set_content(get_problem_statement(self.current_problem))
        self.problem_id += 1

    def check_answer(self, answer):
        if self.current_problem.is_solution(Fraction.from_string(answer)):
            print("YAY")
        else:
            print("NOOO")

        self.load_next_problem()
        self.websocket.send(f"n{self.problem_id}")


if __name__ in {"__main__", "__mp_main__"}:
    app = App()