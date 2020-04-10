"""
Connect4 AI Flask application for Python - defines the routes and associated methods
2020 Jonamitch
"""
from flask import render_template, jsonify
from app import app
import logging

logger = logging.getLogger(__name__)


@app.route('/connect4')
def connect4():
    """Connect4 endpoint to play connect4"""
    return render_template('connect4.html', title='Connect4')


@app.route('/connect4/<col_entry>')
def connect4_col_entry(col_entry):
    """Connect4 endpoint to play connect4"""
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0]
    ]

    return jsonify([{'grid': grid}])
