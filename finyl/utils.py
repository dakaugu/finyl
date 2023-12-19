import os
import subprocess
from multiprocessing import Process
from threading import Thread
from sys import platform

import requests
from pydub import AudioSegment, playback

from finyl.settings import BASE_PATH, DOWNLOAD_PATH, EVENTS_PATH, ENV
from finyl.sounds import FINYL_START, VINYL_SOUND, WIFI_CONNECTED


def play_in_background(file_path: str) -> None:
    """Play a sound in background"""
    sound = AudioSegment.from_file(file_path, parameters=["-nostdin"])
    Thread(target=playback.play, args=(sound,)).start()


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
            print(f"{path} path does not exist. Creating it...")
            os.mkdir(path)
        else:
            print(f"{path} path exists")


def init_event_file() -> None:
    """Create event file that finyl listens to for activities"""
    if not os.path.exists(EVENTS_PATH):
        print("finyl event file does not exist. Creating it... ")
    else:
        print(f"{EVENTS_PATH} exists, clearing it!")

    with open(EVENTS_PATH, "w") as event_file:
        event_file.write("")


def connect_wifi(ssid: str, password: str) -> None:
    """Runs `nmcli` command to connect device to Wi-Fi.
    Raspberry Pi OS comes with `nmcli` out of the box. We will use it to
    connect to the targeted Wi-Fi network
    """
    if platform != "darwin":
        subprocess.Popen(f"nmcli d wifi connect {ssid} password {password}", shell=True)
    is_connected = check_internet_connectivity()
    if not is_connected:
        pass
    if is_connected == 1:
        play_in_background(WIFI_CONNECTED)


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
    print("Initializing...")
    init_dirs()
    init_event_file()
    if preferences.get("vinyl_feel") == 1:
        p = Process(target=play_vinyl_crackle)
        p.start()
    if ENV != "DEV":
        play_in_background(FINYL_START)
