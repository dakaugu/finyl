import os
from multiprocessing import Process
from pydub import AudioSegment, playback
from finyl.settings import BASE_PATH, DOWNLOAD_PATH, EVENTS_PATH


# TODO: move to preferences
def play_vinyl_crackle() -> None:
    """Play vinyl crackling in the background while playing records"""
    sound = AudioSegment.from_file(
        os.path.dirname(__file__) + "/sounds/vinyl_crackle.mp3"
    )
    sound = sound - 27  # -27db play it quieter than main audio
    playback.play(sound)
    play_vinyl_crackle()


def init_dirs() -> None:
    """Create necessary directories for finyl software to run"""
    for path in [BASE_PATH, DOWNLOAD_PATH]:
        if not os.path.exists(path):
            print(f"{path} path does not exist. Creating it...")
            os.mkdir(path)
        else:
            print(f"{path} path exists")


def init_event_file() -> None:
    """Create event file that finyl listens to for activities"""
    if not os.path.exists(EVENTS_PATH):
        print("finyl event file does not exist. Creating it... ")
        with open(EVENTS_PATH, "w") as event_file:
            event_file.write("")
    else:
        print(f"{EVENTS_PATH} exists")


def initialize(preferences: dict) -> None:
    print("Initializing...")
    init_dirs()
    init_event_file()
    if preferences.get("vinyl_feel") == 1:
        p = Process(target=play_vinyl_crackle)
        p.start()
