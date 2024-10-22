from main import Problem
import os
from main import TABLET_IP

def generate_problems(n, prefix="problem_set/problem"):
    for i in range(n):
        p = Problem.random()
        p.save(prefix+str(i))

def send_problems():
    os.system(f"scp -r 'problem_set' pi@{TABLET_IP}:~/haptic_rods_C/")

if __name__ == "__main__":
    generate_problems(30)
    send_problems()