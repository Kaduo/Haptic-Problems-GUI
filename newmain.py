from nicegui import ui
from problems import Problem, Fraction
from generate_problems import send_problems
from websockets.sync.client import connect
from subprocess import Popen

NB_PROBLEMS = 4


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

    def __init__(self, user_id, problem_id):
        self.websocket = connect("ws://192.168.1.24:8080")
        self.problem_id = problem_id
        self.p = Popen(["python", "gaze/main.py"])
        self.user_id = user_id
        self.correct = None
        self.current_problem = None
        self.answer = None
        self.waiting = False
        self.start_current_user()
        self.load_current_problem()
        with ui.column():
            ui.label().bind_text_from(self, "problem_id", backward= lambda id: f"{id+1}/{NB_PROBLEMS}")
            ui.icon("Done").bind_visibility_from(self, "correct", value=True)

        with ui.element("div").style("display: flex; align-items: center; justify-content: center; height: 100vh; width:100%;"):
            with ui.column().style("align-items: center;"):
                ui.html().bind_content_from(self, "current_problem", get_problem_statement)
                ui.input("Ta réponse : ").bind_value(self, "answer")
                ui.button('Valider', on_click=lambda: self.check_answer())
        ui.run()
    
    def start_current_user(self):
        self.websocket.send(f"u{self.user_id}")

    def load_current_problem(self):
        self.current_problem = Problem.load(f"problem_set/problem{self.problem_id}.prob")
        self.websocket.send(f"n{self.problem_id}")
        self.websocket.recv(timeout=None)

    def check_answer(self):
        self.correct = self.current_problem.is_solution(Fraction.from_string(self.answer))
        self.answer = None
        self.next()

    def next(self):
        if self.problem_id < NB_PROBLEMS:
            self.problem_id += 1
            self.load_current_problem()
        else:
            
            self.problem_id = 0
            self.user_id += 1
            self.start_current_user()
            self.load_current_problem()

if __name__ in {"__main__", "__mp_main__"}:
    
    app = App(5,0)
    print("hi")