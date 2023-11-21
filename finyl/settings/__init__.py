import os
from .settings import *


ENV = os.environ.get("FINYL_ENV", "DEV")
if ENV in ["FINYL_PI", "TEST"]:
    from .pi import *
elif ENV == "DEV":
    from .dev import *
