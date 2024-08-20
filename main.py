from enum import Enum
import random
from math import gcd
from tkinter import *
from tkinter import ttk

NB_REGLETTES = 10
MIN_LENGTH = 1
MAX_LENGTH = 10

class Color(Enum):
    WHITE = 0xc8c8c8
    RED = 0xe62937
    GREEN = 0x00e430
    PURPLE = 0xc87aff
    YELLOW = 0xfdf900
    DARK_GREEN = 0x00752c
    BLACK = 0x000000
    BROWN = 0x7f6a4f
    BLUE = 0x0079f1
    ORANGE = 0xffa100

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

class Rod():

    def __init__(self, length):
        self.length = length
        self.color = list(Color)[self.length - 1]

class ParsingError(Exception):
    pass

class Fraction():

    def __init__(self, numerator, denominator, reduce = False):
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
        return self.numerator*other.denominator == other.numerator * self.denominator

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
                    raise ParsingError("Multiple \"/\" or \".\" symbols in answer.")
                break_encountered = True
                break_character = char
                current_part.reverse()
                for i, digit in enumerate(current_part):
                    numerator += digit*(10**i)
                current_part = []
            
            elif char.isspace():
                pass

            else:
                raise ParsingError(f"Unexpected character in answer: {char}")
        
        if break_character == "/":
            current_part.reverse()
            for i, digit in enumerate(current_part):
                denominator += digit*(10**i)
        
        else:
            denominator = 10**len(current_part) if break_encountered else 1
            numerator *= 10**len(current_part)
            current_part.reverse()
            for i, digit in enumerate(current_part):
                numerator += digit*(10**i)

        return Fraction(numerator, denominator)


def random_rod(min_length = MIN_LENGTH, max_length = MAX_LENGTH):
    return Rod(random.randrange(min_length, max_length + 1))

class Problem():

    def __init__(self, l, r1, r2):
        self.l = l
        self.r1 = r1
        self.r2 = r2
        self.solution = Fraction((r2.length * l), r1.length, reduce = True)
    
    def random():
        # TODO : prevent second random rod to be the same as the first one
        return Problem(random.randrange(1, 11), random_rod(min_length=2), random_rod())

    def __str__(self):
        return f"Si la réglette {self.r1.color} mesure {self.l} cm, combien mesure la réglette {self.r2.color} ?"
    
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

    root = Tk()
    root.title("Haptic Rods")

    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text=str(problem)).grid(column=1, row=1, sticky=(S, E))

    answer = StringVar()
    answer_entry = ttk.Entry(mainframe, textvariable=answer)
    answer_entry.grid(column = 1, row = 2, sticky=(W, E))
    answer_entry.focus()

    ttk.Label(mainframe, text="cm").grid(column = 2, row = 2, sticky = E)

    root.bind("<Return>", submit_answer)

    root.mainloop()