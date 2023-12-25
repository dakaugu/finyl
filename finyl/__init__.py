import logging

from finyl.settings import ENV, PI_ENV

LOG_FILE = "/var/log/finyl.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if ENV == PI_ENV:
    handler = logging.FileHandler(LOG_FILE)
else:
    handler = logging.StreamHandler()

formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
