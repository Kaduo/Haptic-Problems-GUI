from enum import Enum
import random
from math import gcd, lcm
from tkinter import Tk, Label, StringVar, N, S, W, E, ttk
from math import sqrt
import os
from subprocess import Popen
from fabric import Connection

TABLET_IP = "192.168.1.9"
USER = "pi"
PASSWORD = "raspberry"


SIGINT = 2

NB_REGLETTES = 10
MIN_LENGTH = 1
MAX_LENGTH = 10

TABLET_WIDTH = 1000
TABLET_HEIGHT = 600

UNIT_ROD_WIDTH = 40

USER = "pi"
PASSWORD = "raspberry"


def send_key(c, k):
    c.run(f"DISPLAY=:0 xdotool getactivewindow key {k}")


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


class ParsingError(Exception):
    pass


class Fraction:
    def __init__(self, numerator, denominator, reduce=False):
        self.numerator = numerator
        self.denominator = denominator

        if reduce:
            reduced = self.reduced()
            self.numerator = reduced.numerator
            self.denominator = reduced.denominator

    def reduced(self):
        d = gcd(self.numerator, self.denominator)
        return Fraction(self.numerator // d, self.denominator // d)

    def __eq__(self, other):
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def from_string(s: str):
        current_part = []
        break_encountered = False
        break_character = None
        numerator = 0
        denominator = 0
        for char in s:
            if char.isnumeric():
                current_part.append(int(char))

            elif char in [".", ",", "/"]:
                if break_encountered:
                    raise ParsingError('Multiple "/" or "." symbols in answer.')
                break_encountered = True
                break_character = char
                current_part.reverse()
                for i, digit in enumerate(current_part):
                    numerator += digit * (10**i)
                current_part = []

            elif char.isspace():
                pass

            else:
                raise ParsingError(f"Unexpected character in answer: {char}")

        if break_character == "/":
            current_part.reverse()
            for i, digit in enumerate(current_part):
                denominator += digit * (10**i)

        else:
            denominator = 10 ** len(current_part) if break_encountered else 1
            numerator *= 10 ** len(current_part)
            current_part.reverse()
            for i, digit in enumerate(current_part):
                numerator += digit * (10**i)

        return Fraction(numerator, denominator)


def random_rod(min_length=MIN_LENGTH, max_length=MAX_LENGTH):
    return Rod(random.randrange(min_length, max_length + 1))


class RodSpec:
    def __init__(self, nb_rods_per_length=[0] * 10, d={}):
        # nb_rods_per_length is a list where the n-th element is the
        # number of rods of length n+1.
        # d is a dictionary where the element at key l is the number of
        # rods of length l.
        # If both are set, the numbers are added together.
        self.nb_rods_per_length = nb_rods_per_length
        for length in range(MIN_LENGTH, MAX_LENGTH + 1):
            if length in d.keys():
                self.nb_rods_per_length[length - 1] = d[length]

    def nb_of_length(self, length):
        return self.nb_rods_per_length[length - 1]

    def add_rods(self, length, number=1):
        self.nb_rods_per_length[length - 1] += number

    def nb_rods(self):
        return int(sum(self.nb_rods_per_length))

    def line_width(self):
        area = sum([self.nb_rods_per_length[i] * (i + 1) for i in range(NB_REGLETTES)])
        return sqrt(5 * area / 3) * UNIT_ROD_WIDTH  # 5/3 is the tablet's aspect ratio

    def pad(self, total_rods=20):
        if self.nb_rods() < total_rods:
            diff = total_rods - self.nb_rods()
            for _ in range(diff):
                self.nb_rods_per_length[
                    random.randint(MIN_LENGTH - 1, MAX_LENGTH - 1)
                ] += 1

    def save(
        self,
        filename="spec.rods",
        screen_width=TABLET_WIDTH,
        screen_height=TABLET_HEIGHT,
        unit_rod_width=UNIT_ROD_WIDTH,
    ):
        line_width = self.line_width()
        pad_y = 0

        rod_lengths = []
        for length in range(1, MAX_LENGTH + 1):
            rod_lengths += [length] * self.nb_rods_per_length[length - 1]

        random.shuffle(rod_lengths)
        rod_lines = [[]]

        with open(filename, "w") as f:
            x = 0
            f.write(f"{self.nb_rods()} ")
            for length in rod_lengths:
                if length + x > line_width:
                    pad_x = (screen_width - x) / len(rod_lines[-1])

                    for j, rod in enumerate(rod_lines[-1]):
                        rod[1] += (j + random.uniform(0.2, 0.8)) * pad_x  # pad x
                    x = 0
                    rod_lines.append([])

                rod_lines[-1].append([length, x])
                x += unit_rod_width * length

            # Pad the last line
            pad_x = (screen_width - x) / len(rod_lines[-1])

            for j, rod in enumerate(rod_lines[-1]):
                rod[1] += (j + random.uniform(0.2, 0.8)) * pad_x

            # Move the last line around
            rand_idx = random.randrange(0, len(rod_lines))
            rod_lines[-1], rod_lines[rand_idx] = rod_lines[rand_idx], rod_lines[-1]

            pad_y = (screen_height - (len(rod_lines) * unit_rod_width)) / len(rod_lines)

            for line_idx, line in enumerate(rod_lines):
                for [length, x] in line:
                    f.write(
                        f"{length} {x} {pad_y*(line_idx + random.uniform(0.2,0.8)) + line_idx*unit_rod_width} "
                    )

            f.close()


class Problem:
    def __init__(self, l1, r1, r2, padding=20):
        self.l1 = l1
        self.r1 = r1
        self.r2 = r2
        self.solution = Fraction((r2.length * l1), r1.length, reduce=True)

        lcm_r1_r2 = lcm(r1.length, r2.length)
        gcd_r1_r2 = gcd(r1.length, r2.length)
        self.necessary_rods = RodSpec(
            d={
                r1.length: lcm_r1_r2 // r1.length,
                r2.length: lcm_r1_r2 // r2.length,
                gcd_r1_r2: r2.length // gcd_r1_r2,
            }
        )

        self.necessary_rods.pad(padding)

    def random(padding= 20):
        # TODO : prevent second random rod to be the same as the first one
        return Problem(random.randrange(1, 11), random_rod(min_length=2), random_rod(), padding=padding)

    def __str__(self):
        return f"Si la réglette {self.r1.color} mesure {self.l1} cm, combien mesure la réglette {self.r2.color} ?"

    def is_solution(self, answer):
        return self.solution == answer

    def save(self, name="problem"):
        with open(name + ".prob", "w") as f:
            f.write(f"{self.l1} ")
            f.write(f"{self.r1.length} ")
            f.write(f"{self.r2.length}")
            f.close()
        self.necessary_rods.save(name + ".rods")

    def load(filename):
        with open(filename, "r") as f:
            args = f.read().split(" ")
            l1 = int(args[0])
            r1 = Rod(int(args[1]))
            r2 = Rod(int(args[2]))
            f.close()
            return Problem(l1, r1, r2)


def make_problems(n):
    pass


class App:
    def __init__(self):

        self.c = Connection(TABLET_IP, user=USER, connect_kwargs={"password": PASSWORD})

        self.problem_id = 0
        self.problem = Problem.load(f"problem_set/problem{self.problem_id}.prob")
        self.root = Tk()
        #self.root.attributes("-fullscreen", True)
        self.root.title("Haptic Rods")

        self.mainframe = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=1)

        self.problem_frame = ttk.Frame(self.mainframe)
        self.problem_frame.grid(column=1, row=1, sticky=S)
        self.answer = StringVar()
        self.answer_entry = ttk.Entry(self.mainframe, textvariable=self.answer)
        self.answer_entry.grid(column=1, row=2, sticky=N)
        self.answer_entry.focus()

        self.display_problem(self.problem)
        self.root.bind("<Return>", self.submit_answer)

    def submit_answer(self, *args):
        try:
            value = Fraction.from_string(self.answer.get())
            if self.problem.is_solution(value):
                self.root.configure(bg="green")
            else:
                self.root.configure(bg="red")
        except ParsingError:
            self.root.configure(bg="red")
        
        self.problem_id += 1
        self.problem = Problem.load(f"problem_set/problem{self.problem_id}.prob")
        self.display_problem(self.problem)

    def mainloop(self):
        self.root.mainloop()

    def display_problem(self, problem):
        for widget in self.problem_frame.winfo_children():
            widget.destroy()
        # self.answer_entry.delete("1.0", END)
        Label(self.problem_frame, text="Si la réglette ").grid(
            column=1, row=1, sticky=S
        )

        Label(
            self.problem_frame,
            text=f"{problem.r1.color} ",
            foreground=problem.r1.color.value,
        ).grid(column=2, row=1, sticky=(S, W))

        Label(
            self.problem_frame,
            text=f"mesure {problem.l1} cm, quelle est la longueur de la réglette ",
        ).grid(column=3, row=1, sticky=(S, W))

        Label(
            self.problem_frame,
            text=f"{problem.r2.color} ",
            foreground=problem.r2.color.value,
        ).grid(column=4, row=1, sticky=(S, W))

        Label(self.problem_frame, text="?").grid(column=5, row=1, sticky=(S, W))

        if self.problem_id == 0:
            self.c.run("DISPLAY=:0 cd ~/haptic_rods_C && make update_and_run", asynchronous=True)
        else:
            send_key(self.c, "N")

if __name__ == "__main__":
    # os.system(f"scp -r '/home/aflokkat/Bureau/HapticRods/Haptic-Problems-GUI/problem_set' pi@{TABLET_IP}:~/haptic_rods_C/problem_set")
    p = Popen(["python", "gaze/main.py"])

    app = App()
    app.mainloop()
    send_key(app.c, "Escape")
    # app.c.run("pkill haptic_rods")
    # print("hello...")

    p.send_signal(SIGINT)