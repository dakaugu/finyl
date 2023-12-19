import signal
import time
from multiprocessing import Process

from finyl.audio_player import Player
from finyl.settings import EVENTS_PATH, ENV
from finyl.sounds import NFC_CONFIRMED
from finyl.utils import initialize, play_in_background
from finyl.yt_album import Album

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


def check_start_nfc() -> Process:
    """Run the nfc listen process if we are in a Pi environment"""
    if ENV != "DEV":
        from finyl.nfc import nfc_listen

        nfc_process = Process(target=nfc_listen, args=())
        nfc_process.start()
        return nfc_process


def start() -> None:
    nfc_process = check_start_nfc()
    player_process = None

    def handler(signum, frame):
        print("shutting down player")
        try:
            if player_process:
                player_process.terminate()
            if nfc_process:
                nfc_process.terminate()
        except Exception as e:
            print(e)
        exit(1)

    signal.signal(signal.SIGINT, handler)
    initialize(PREFERENCES)
    print("Listening to new events...")

    last_event = None
    while True:
        time.sleep(1)
        event = listen()
        command_args = event.split(",") if event else []
        if event and event != last_event:
            print("New event found:")
            print(event)
            if player_process:
                player_process.terminate()
            play_in_background(NFC_CONFIRMED)
            if command_args[0] == "stop":
                pass
            else:
                album = Album(command_args[0])
                Process(target=album.download, args=()).start()
                player = Player(album)
                player_process = Process(
                    target=player.play_album,
                    args=(
                        int(command_args[1]),  # track
                        int(command_args[2]),  # offset (start in seconds)
                    ),
                )
                player_process.start()
            last_event = event
