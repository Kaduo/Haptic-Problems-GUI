import fabric
from fabric import Connection

tablet_ip = "192.168.1.7"
user = "pi"
password = "raspberry"

def send_key(c, k):
    c.run(f"DISPLAY=:0 xdotool getactive window key {k}")

c = Connection(tablet_ip, user=user, connect_kwargs={"password": password})

try:
    c.run("cd ~/haptic_rods_C/ && make update_and_run")
finally:
    print("hi")
    c.run("DISPLAY=:0 xdotool getactivewindow key Escape")
    c.close()