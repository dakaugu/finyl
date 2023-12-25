import os

from .settings import *

ENV = os.environ.get("FINYL_ENV", "DEV")

PI_ENV = "FINYL_PI"
DEV_ENV = "DEV"
TEST_ENV = "TEST"

if ENV in [PI_ENV, TEST_ENV]:
    from .pi import *
elif ENV == DEV_ENV:
    from .dev import *
