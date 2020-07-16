import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

DEBUG = True
Testing = True
SECRET_KEY = "SECRET_KEY!"  # same key will be used for csrf protection

import logging

LOG_FILE = "/tmp/challengegroover.log"
LOG_SIZE = 1024 * 1024
LOG_LEVEL = logging.DEBUG
