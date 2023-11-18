import os
import signal
import subprocess
import time
from finyl.settings import EVENTS_PATH


PLAYER_PID = None


def handler(signum, frame):
    print("shutting down player")
    try:
        if PLAYER_PID:
            os.kill(PLAYER_PID, signal.SIGKILL)
    except Exception as e:
        print(e)
    exit(1)


def listen():
    with open(EVENTS_PATH) as f:
        last_line = None
        for line in f:
            last_line = line
        return last_line


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    print("Listening to new events...")

    last_command = None
    while True:
        time.sleep(1)
        command = listen()
        if command and command != last_command:
            print("New event found!")
            if PLAYER_PID:
                os.kill(PLAYER_PID, signal.SIGKILL)
                PLAYER_PID = None
            if command == "stop":
                pass
            else:
                player_process = subprocess.Popen(
                    f"python3 finyl/play.py {command}", shell=True
                )
                PLAYER_PID = player_process.pid
            last_command = command
