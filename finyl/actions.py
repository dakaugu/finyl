from ast import literal_eval
from multiprocessing import set_start_method, Process
from subprocess import Popen
from sys import platform
from typing import Optional

from finyl import logger
from finyl.audio_player import Player
from finyl.sounds import NFC_CONFIRMED, WIFI_CONNECTED
from finyl.utils import play_sound, check_internet_connectivity
from finyl.yt_album import Album

# This is added because of a pickling error with multiprocessing and globals()
# with @action decorator
# see: https://medium.com/devopss-hole/python-multiprocessing-pickle-issue-e2d35ccf96a9
set_start_method("fork")


def finyl_eval(v: str):
    try:
        return literal_eval(v)
    except (ValueError, SyntaxError):
        return v


def action(func):
    """Base interactions with valid finyl/*/finyl/ nfc payload"""

    def caller(*args):
        play_sound(NFC_CONFIRMED, background=True)
        func(*args)

    return caller


def action_do(command: str) -> Optional[Process]:
    """Run action based on command string and return a separate process
    A typical command looks like:
    - pre nfc:
    `finyl/action_name/argument_1, argument_2, argument_3/finyl/`
    - post nfc:
    `action_name/argument_1, argument_2, argument_3`
    """
    try:
        command, args = command.split("/")
        args = tuple([finyl_eval(v) for v in args.split(",")])
    except ValueError:
        logger.error(f"Invalid command: {command}. action or arguments not provided!")
        # play_sound(NFC_ERROR)  # TODO: need to revisit weird bug behind this
        return None
    try:
        action_process = Process(target=globals()[command], args=args)
        action_process.start()
        return action_process
    except (KeyError, TypeError) as e:
        match e:
            case KeyError():
                logger.error(f"This action:{command} has not been implemented yet")
            case TypeError():
                logger.error(f"Invalid arguments for action:{command}, args:{args}")
        # play_sound(NFC_ERROR)  # TODO: need to revisit weird bug behind this
        logger.error(e)
        traceback = e.__traceback__
        while traceback:
            logger.error(
                f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}"
            )
            traceback = traceback.tb_next


@action
def stop(*args) -> None:
    """forces last action process to stop, stopping playback"""
    return None


@action
def play(id: str, track: int, offset: int, *args) -> None:
    """
    play/<id>,<track>,<offset>
    Play album action
    """
    album = Album(id)
    player = Player(album)
    Process(target=album.download, args=()).start()
    player.play_album(track, offset)


@action
def connect_wifi(ssid: str, password: str, *args) -> None:
    """
    connect_wifi/<ssid>,<password>
    Runs `nmcli` command to connect device to Wi-Fi.
    Raspberry Pi OS comes with `nmcli` out of the box. We will use it to
    connect to the targeted Wi-Fi network
    """
    if platform != "darwin":
        Popen(f"nmcli d wifi connect {ssid} password {password}", shell=True)
    is_connected = check_internet_connectivity()
    if not is_connected:
        pass
    if is_connected == 1:
        play_sound(WIFI_CONNECTED, background=True)
