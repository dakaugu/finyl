import signal
import time
from multiprocessing import Process
from finyl.settings import EVENTS_PATH
from finyl.utils import initialize, nfc_listen
from finyl.yt_album import Album
from finyl.audio_player import Player


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
    nfc_process = Process(target=nfc_listen, args=())
    nfc_process.start()
    player_process = None

    def handler(signum, frame):
        print("shutting down player")
        try:
            if player_process:
                player_process.terminate()
            nfc_process.terminate()
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
        command_args = command.split(",")
        if command and command != last_command:
            print("New event found:")
            print(command)
            if player_process:
                player_process.terminate()
            if command_args[0] == "stop":
                pass
            else:
                album = Album(command_args[0])
                Process(target=album.download, args=()).start()
                player = Player()
                player_process = Process(
                    target=player.play_album,
                    args=(
                        album,
                        int(command_args[1]),  # track
                        int(command_args[2]),  # offset (start in seconds)
                    ),
                )
                player_process.start()
            last_command = command
