import re

from PiicoDev_RFID import PiicoDev_RFID
from PiicoDev_Unified import sleep_ms

from finyl import logger
from finyl.settings import EVENTS_PATH


def nfc_listen() -> None:
    """Listen to nfc events and log them in events.txt"""
    rfid = PiicoDev_RFID()  # Initialise the RFID module

    logger.info("NFC module is listening...")
    last_text = None
    while True:
        if rfid.tagPresent():  # if an RFID tag is present
            raw_text = rfid.readText()  # get the id
            if last_text == raw_text:
                continue
            # Some characters are being appended at the start and end of the text
            # adding `finyl/text/finyl/` to the string tag to get only necessary text
            rtext = re.search("finyl/(.*)/finyl/", raw_text)
            if rtext:
                final_text = rtext.group(1)
                if final_text:
                    with open(EVENTS_PATH, "w") as event_file:
                        event_file.write(final_text)
            last_text = raw_text
        sleep_ms(300)
