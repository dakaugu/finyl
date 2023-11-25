import os
import signal
import subprocess
import time
from finyl.settings import EVENTS_PATH
from finyl.utils import initialize


PREFERENCES = {"vinyl_feel": 0}


def listen() -> str:
    """Listen to new events triggered by nfc reader activities or button presses
    A new line is added typically if the nfc tag is different from the last event
    or a button press is triggered
    """
    with open(EVENTS_PATH) as f:
        last_line = None
        for line in f:
            last_line = line
        return last_line


def start() -> None:
    player_pid = 0

    def handler(signum, frame):
        print("shutting down player")
        try:
            if player_pid:
                os.killpg(os.getpgid(player_pid), signal.SIGKILL)
        except Exception as e:
            print(e)
        exit(1)

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
            if player_pid:
                # TODO: or try catch here
                os.killpg(os.getpgid(player_pid), signal.SIGKILL)
                player_pid = 0
            if command == "stop":
                pass
            else:
                # TODO: try catch then dont modify pid
                player_process = subprocess.Popen(
                    f"python3 finyl/play.py {command}", shell=True, preexec_fn=os.setsid
                )
                player_pid = player_process.pid
            last_command = command
