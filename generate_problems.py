from problems import random_problem
import os
from problems import TABLET_IP

def generate_problems(n, prefix="problem_set/problem"):
    for i in range(n):
        print(f"proble{i}")
        p = random_problem()
        p.save(prefix+str(i))

def send_problems():
    os.system(f"scp -r 'problem_set' pi@{TABLET_IP}:~/haptic_rods_C/")

if __name__ == "__main__":
    generate_problems(30)
    send_problems()