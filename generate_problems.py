from main import Problem
import os
from net import tablet_ip

def generate_problems(n, prefix="problem_set/problem"):
    for i in range(n):
        p = Problem.random()
        p.save(prefix+str(i))

def send_problems():
    os.system(f"scp -r '/home/aflokkat/Bureau/HapticRods/Haptic-Problems-GUI/problem_set' pi@{tablet_ip}:~/haptic_rods_C/problem_set")

if __name__ == "__main__":
    generate_problems(20)
    send_problems()