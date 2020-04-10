"""
Games Room AI Flask application for Python - defines the routes and associated methods
2020 Jonamitch
"""
from flask import render_template, send_from_directory
from app import app
import os
import logging

logger = logging.getLogger(__name__)


@app.route('/')
@app.route('/index')
def index():
    """Home endpoint to create home page"""
    return render_template('index.html', title='Home')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
