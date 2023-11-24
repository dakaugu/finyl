import os
import signal
import subprocess
import time
from finyl.settings import EVENTS_PATH
from finyl.utils import initialize


PLAYER_PID = None
PREFERENCES = {"vinyl_feel": 0}


def handler(signum, frame):
    print("shutting down player")
    try:
        if PLAYER_PID:
            os.killpg(os.getpgid(PLAYER_PID), signal.SIGTERM)
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
    initialize(PREFERENCES)
    print("Listening to new events...")

    last_command = None
    while True:
        time.sleep(1)
        command = listen()
        if command and command != last_command:
            print("New event found:")
            print(command)
            if PLAYER_PID:
                os.kill(PLAYER_PID, signal.SIGKILL)
                PLAYER_PID = None
            if command == "stop":
                pass
            else:
                player_process = subprocess.Popen(
                    f"python3 finyl/play.py {command}", shell=True, preexec_fn=os.setsid
                )
                PLAYER_PID = player_process.pid
            last_command = command
