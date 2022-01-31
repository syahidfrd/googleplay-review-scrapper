import os
from dotenv import load_dotenv

load_dotenv()

# app
APP_NAME = "Google Play Review Scrapper"
DEBUG = True

# database
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# multichannel
QISMO_BASE_URL = os.environ.get("QISMO_BASE_URL")
QISMO_APP_ID = os.environ.get("QISMO_APP_ID")
CHANNEL_IDENTIFIER_KEY = os.environ.get("CHANNEL_IDENTIFIER_KEY")
ANDROID_PACKAGE_NAME = os.environ.get("ANDROID_PACKAGE_NAME")
JOB_INTERVAL = os.environ.get("JOB_INTERVAL")
