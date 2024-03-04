from dotenv import load_dotenv

load_dotenv(override=True)
from .settings import *

APP_ENV = "local"
DEBUG = True

# Django debug toolbar configuration
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]

# Email configuration
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
