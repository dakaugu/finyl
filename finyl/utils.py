import os
from multiprocessing import Process
from threading import Thread

import requests
from pydub import AudioSegment, playback

from finyl import logger
from finyl.settings import BASE_PATH, DOWNLOAD_PATH, EVENTS_PATH, ENV
from finyl.sounds import FINYL_START, VINYL_SOUND


def play_sound(file_path: str, background=False) -> None:
    """Play a sound in background"""
    sound = AudioSegment.from_file(file_path, parameters=["-nostdin"])
    if background:
        Thread(target=playback.play, args=(sound,)).start()
    else:
        playback.play(sound)


# TODO: move to preferences
def play_vinyl_crackle() -> None:
    """Play vinyl crackling in the background while playing records"""
    sound = AudioSegment.from_file(VINYL_SOUND)
    sound = sound - 27  # -27db play it quieter than main audio
    playback.play(sound)
    play_vinyl_crackle()


def init_dirs() -> None:
    """Create necessary directories for finyl software to run"""
    for path in [BASE_PATH, DOWNLOAD_PATH]:
        if not os.path.exists(path):
            logger.info(f"{path} path does not exist. Creating it...")
            os.mkdir(path)
        else:
            logger.info(f"{path} path exists")


def init_event_file() -> None:
    """Create event file that finyl listens to for activities"""
    if not os.path.exists(EVENTS_PATH):
        logger.info("finyl event file does not exist. Creating it... ")
    else:
        logger.info(f"{EVENTS_PATH} exists, clearing it!")

    with open(EVENTS_PATH, "w") as event_file:
        event_file.write("")


def check_internet_connectivity() -> int:
    """Check for if internet states
    - not connected: 0
    - Connected and working: 1
    - connected and not working: 2
    """
    try:
        requests.get("https://httpbin.org/ip")
    except requests.ConnectionError:
        return 0
    except requests.Timeout:
        return 2
    return 1


def initialize(preferences: dict) -> None:
    logger.info("Initializing...")
    init_dirs()
    init_event_file()
    if preferences.get("vinyl_feel") == 1:
        p = Process(target=play_vinyl_crackle)
        p.start()
    if ENV != "DEV":
        play_sound(FINYL_START, background=True)
