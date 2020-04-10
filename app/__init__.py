"""
IG Markets API Flask application for Python - sets up the config, db, login manager and connects to the IG services
2019 Jonamitch
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from config import AppConfig

app = Flask(__name__)
app.config.from_object(AppConfig)
bootstrap = Bootstrap(app)

from app import routes
