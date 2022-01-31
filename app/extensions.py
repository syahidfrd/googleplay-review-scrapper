"""
To avoid cyclic imports, instantiate extensions here.
Use this module to access them elsewhere in project,
instead using `__init__.py`
"""

# SQLAlchemy extension
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .models import * # noqa

# Scheduler extension
from flask_apscheduler import APScheduler # noqa
scheduler = APScheduler()

# get google service account credential
from google.oauth2 import service_account # noqa
SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
SERVICE_ACCOUNT_FILE = 'publisher.json'
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
