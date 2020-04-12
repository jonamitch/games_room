import datetime
from secrets import secrets
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class AppConfig:
    """ Config file used for the flask app and ad hoc utilities """
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets['app_secret_key']
    AI_TREE_DEPTH = 6