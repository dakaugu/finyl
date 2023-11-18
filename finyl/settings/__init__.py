import os
from .settings import *


ENV = os.environ.get("FINYL_ENV", "DEV")
if ENV == "FINYL_PI":
    from .pi import *
elif ENV == "DEV":
    from .dev import *
