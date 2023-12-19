from finyl.sounds import NFC_CONFIRMED
from finyl.utils import play_in_background


def action(func):
    """Base interactions with valid finyl/*/finyl/ nfc payload"""

    def caller():
        play_in_background(NFC_CONFIRMED)
        func()

    return caller
