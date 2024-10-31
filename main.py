from nicegui import ui
from problems import Problem, Fraction, ParsingError
from generate_problems import send_problems
from websockets.sync.client import connect
import subprocess
from subprocess import Popen
import pandas
import os
import time
import signal
import glob
import pathlib
import tomlkit

NB_PROBLEMS = 10

TABLET_IP = "192.168.1.24"

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
        self.websocket = connect(f"ws://{TABLET_IP}:8080")
        self.problem_id = problem_id
        self.p = Popen(["python", "gaze/main.py"])
        self.user_id = user_id
        self.correct = None
        self.current_problem = None
        self.answer = None
        self.waiting = False
        self.ok_image_path = None
        self.start_current_user()
        self.load_current_problem()
        with ui.column():
            ui.label().bind_text_from(self, "problem_id", backward= lambda id: f"{id+1}/{NB_PROBLEMS}")
            ui.image().bind_source_from(self, "ok_image_path")

        with ui.element("div").style("display: flex; align-items: center; justify-content: center; height: 100vh; width:100%;"):
            with ui.column().style("align-items: center;"):
                ui.html().bind_content_from(self, "current_problem", get_problem_statement)
                ui.input("Ta réponse : ").bind_value(self, "answer").on("keydown.enter", self.check_answer)
                ui.button('Valider', on_click=self.check_answer)
        ui.run(reload=False)
    
    def start_current_user(self):
        self.websocket.send(f"u{self.user_id}")

    def load_current_problem(self):
        self.current_problem = Problem.load(f"problem_set/problem{self.problem_id}.prob")
        self.websocket.send(f"n{self.problem_id}")
        print("waiting for answer...")
        self.websocket.recv(timeout=None)

    def check_answer(self):
        if self.answer is not None:
            try:
                self.correct = self.current_problem.is_solution(Fraction.from_string(self.answer))
            except ParsingError:
                self.correct = False
                return

            if self.correct:
                self.ok_image_path = "images/okay.jpg"
            else:
                self.ok_image_path = "images/notokay.png"

            self.answer = None
            self.next()
        
    def end_session(self):
        print("WELWELWEL")
        self.p.send_signal(signal.SIGINT)
        self.websocket.send("e")
        self.websocket.recv(timeout=None)
        self.grab_taps()
        self.p.wait()
        self.slice_eyes()
        

    def next(self):
        if self.problem_id < NB_PROBLEMS - 1:
            self.problem_id += 1
            self.load_current_problem()
        else:
            self.end_session()
    
    def grab_taps(self):
        subprocess.run(["scp", "-r", f"pi@{TABLET_IP}:/home/pi/haptic_rods_C/user{self.user_id}", "user_data/"])


    def slice_eyes(self):
        log_names = glob.glob("logs/*")
        latest_log_name = max(log_names, key=os.path.getctime)
        eye_tracking_df = pandas.read_csv(latest_log_name)
        for i in range(NB_PROBLEMS):
            times = []
            with open(f"user_data/user{self.user_id}/rods_u{self.user_id}p{i}.tap") as rods_file:
                for line in rods_file.readlines():
                    if line[0] == "t":
                        times.append(int(line[1:]))
                eye_tracking_df[(eye_tracking_df["Timestamp (ms)"]//1000).between(times[0], times[1])].to_csv(f"user_data/user{self.user_id}/eyes_u{self.user_id}p{i}.csv")
        
        # pathlib.Path.unlink(latest_log_name)

if __name__ in {"__main__", "__mp_main__"}:
    with open("meta.toml", "r+") as meta:
        doc = tomlkit.load(meta)
        meta.seek(0)
        doc["latest_user_id"] += 1
        tomlkit.dump(doc, meta)
        app = App(doc["latest_user_id"],0)
    print("hi")