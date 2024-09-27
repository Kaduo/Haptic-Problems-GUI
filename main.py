from enum import Enum
import random
from math import gcd, lcm
from tkinter import *
from tkinter import ttk
from tkinter import font
from math import sqrt

NB_REGLETTES = 10
MIN_LENGTH = 1
MAX_LENGTH = 10

TABLET_WIDTH = 1600
TABLET_HEIGHT = 600

UNIT_ROD_WIDTH = 40


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
        for l in range(MIN_LENGTH, MAX_LENGTH + 1):
            if l in d.keys():
                self.nb_rods_per_length[l - 1] = d[l]

    def nb_of_length(self, l):
        return self.nb_rods_per_length[l - 1]

    def add_rods(self, length, number=1):
        self.nb_rods_per_length[length - 1] += number

    def nb_rods(self):
        return int(sum(self.nb_rods_per_length))

    def line_width(self):
        area = sum([self.nb_rods_per_length[i] * (i + 1) for i in range(NB_REGLETTES)])
        return sqrt(8 * area / 3) * UNIT_ROD_WIDTH  # 8/3 is the tablet's aspect ratio

    def pad(self, total_rods=20):
        if self.nb_rods() < total_rods:
            print(total_rods)
            print(self.nb_rods())
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
        pad_xs = []
        pad_y = 0

        rod_lengths = []
        for l in range(1, MAX_LENGTH+1):
            rod_lengths += [l]*self.nb_rods_per_length[l-1]

        random.shuffle(rod_lengths)
        rod_lines = [[]]

        with open(filename, "w") as f:
            x = 0
            f.write(f"{self.nb_rods()} ")
            for l in rod_lengths:
                if l + x > line_width:
                    pad_x = (screen_width - x)/len(rod_lines[-1])

                    for j, rod in enumerate(rod_lines[-1]):
                        rod[1] += (j+random.uniform(0.2,0.8))*pad_x # pad x


                    x = 0
                    rod_lines.append([])


                rod_lines[-1].append([l, x])
                x += unit_rod_width * l

            #Pad the last line
            pad_x = (screen_width - x)/len(rod_lines[-1])

            for j, rod in enumerate(rod_lines[-1]):
                rod[1] += (j+random.uniform(0.2,0.8))*pad_x

            #Move the last line around
            rand_idx = random.randrange(0, len(rod_lines))
            rod_lines[-1], rod_lines[rand_idx] = rod_lines[rand_idx], rod_lines[-1]


            pad_y = (screen_height - (len(rod_lines)*unit_rod_width))/len(rod_lines)
            
            for line_idx, line in enumerate(rod_lines):
                for [l, x] in line:
                    f.write(f"{l} {x} {pad_y*(line_idx + random.uniform(0.2,0.8)) + line_idx*unit_rod_width} ")

            f.close()

class Problem:

    def __init__(self, l1, r1, r2):
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

    def random():
        # TODO : prevent second random rod to be the same as the first one
        return Problem(random.randrange(1, 11), random_rod(min_length=2), random_rod())

    def __str__(self):
        return f"Si la réglette {self.r1.color} mesure {self.l1} cm, combien mesure la réglette {self.r2.color} ?"

    def is_solution(self, answer):
        return self.solution == answer


if __name__ == "__main__":

    def submit_answer(*args):

        try:
            value = Fraction.from_string(answer.get())
            print(problem.is_solution(value))

        except ParsingError:
            pass

    problem = Problem.random()
    problem.necessary_rods.pad(30)
    problem.necessary_rods.save()

    root = Tk()
    root.title("Haptic Rods")

    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe.columnconfigure(1, weight=1)
    mainframe.rowconfigure(1, weight=1)
    mainframe.rowconfigure(2, weight=1)

    # problem_statement = Text(mainframe, height=1)
    # problem_statement.insert("end", "hello")
    # problem_statement.insert("end", " world")
    # problem_statement.configure(state="disabled")
    # problem_statement.grid(column=4, row=4)

    # problem_font = font.nametofont("TkDefaultFont")
    # problem_font["size"] = 50

    problem_frame = ttk.Frame(mainframe)
    problem_frame.grid(column=1, row=1, sticky=S)
    Label(problem_frame, text=f"Si la réglette ").grid(column=1, row=1, sticky=S)
    Label(
        problem_frame, text=f"{problem.r1.color} ", foreground=problem.r1.color.value
    ).grid(column=2, row=1, sticky=(S, W))
    Label(
        problem_frame,
        text=f"mesure {problem.l1} cm, quelle est la longueur de la réglette ",
    ).grid(column=3, row=1, sticky=(S, W))
    Label(
        problem_frame, text=f"{problem.r2.color} ", foreground=problem.r2.color.value
    ).grid(column=4, row=1, sticky=(S, W))
    Label(problem_frame, text=f"?").grid(column=5, row=1, sticky=(S, W))

    # ttk.Label(mainframe, text=str(problem)).grid(column=1, row=1, sticky=(S, E))

    answer = StringVar()
    answer_entry = ttk.Entry(mainframe, textvariable=answer)
    answer_entry.grid(column=1, row=2, sticky=N)
    answer_entry.focus()

    # ttk.Label(mainframe, text="cm").grid(column = 2, row = 2, sticky = E)

    root.bind("<Return>", submit_answer)

    root.mainloop()