import signal
import time
from multiprocessing import Process

from finyl import logger
from finyl.actions import action_do
from finyl.settings import EVENTS_PATH, ENV
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


def check_start_nfc() -> Process:
    """Run the nfc listen process if we are in a Pi environment"""
    if ENV != "DEV":
        from finyl.nfc import nfc_listen

        nfc_process = Process(target=nfc_listen, args=())
        nfc_process.start()
        return nfc_process


def start() -> None:
    nfc_process = check_start_nfc()
    action_process = None

    def handler(signum, frame):
        logger.info("shutting down player")
        try:
            if action_process:
                action_process.terminate()
            if nfc_process:
                nfc_process.terminate()
        except Exception as e:
            logger.ERROR(e)
        exit(1)

    signal.signal(signal.SIGINT, handler)
    initialize(PREFERENCES)

    logger.info("Listening to new events...")
    last_event = None
    while True:
        time.sleep(0.1)
        event = listen()
        if event and event != last_event:
            logger.info("New event found:")
            logger.info(event)
            if action_process:
                action_process.terminate()
            action_process = action_do(event)
            last_event = event
