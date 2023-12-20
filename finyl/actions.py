from ast import literal_eval
from multiprocessing import set_start_method, Process
from typing import Optional

from finyl.audio_player import Player
from finyl.sounds import NFC_CONFIRMED
from finyl.utils import play_in_background
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
        play_in_background(NFC_CONFIRMED)
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
        print(f"Invalid command: {command}. action or arguments not provided!")
        return None
    try:
        action_process = Process(target=globals()[command], args=args)
        action_process.start()
        return action_process
    except (KeyError, TypeError) as e:
        match e:
            case KeyError():
                print(f"This action:{command} has not been implemented yet")
            case TypeError():
                print(f"Invalid arguments for action:{command}, args:{args}")
        print(e)
        traceback = e.__traceback__
        while traceback:
            print(f"{traceback.tb_frame.f_code.co_filename}: {traceback.tb_lineno}")
            traceback = traceback.tb_next


@action
def stop(*args):
    """forces last action process to stop, stopping playback"""
    return None


@action
def play(id: str, track: int, offset: int, *args):
    """Play album action"""
    album = Album(id)
    player = Player(album)
    Process(target=album.download, args=()).start()
    player.play_album(track, offset)
