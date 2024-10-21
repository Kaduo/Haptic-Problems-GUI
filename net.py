from fabric import Connection

TABLET_IP = "192.168.1.9"
USER = "pi"
PASSWORD = "raspberry"

# if __name__ == "__main__":

#     c = Connection(TABLET_IP, user=user, connect_kwargs={"password": password})

#     try:
#         c.run("cd ~/haptic_rods_C/ && make update_and_run")
#     finally:
#         print("hi")
#         c.run("DISPLAY=:0 xdotool getactivewindow key Escape")
#         c.close()