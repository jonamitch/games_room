"""
Connect4 AI Flask application for Python - defines the routes and associated methods
2020 Jonamitch
"""
from flask import render_template, jsonify, request
from app import app
from connect4 import make_player_move, make_ai_move
import json
import logging

logger = logging.getLogger(__name__)


@app.route('/connect4')
def connect4():
    """Connect4 endpoint to play connect4"""
    return render_template('connect4.html', title='Connect4')


@app.route('/connect4/entryCol', methods=['POST'])
def connect4_col_entry():
    """Connect4 endpoint to play connect4"""
    if request.method == 'POST':
        if 'entryCol' in request.form:
            entry_col = json.loads(request.form['entryCol'])
        else:
            entry_col = None
        grid = json.loads(request.form['grid'])
        player = json.loads(request.form['player'])
    else:
        raise Exception('GET method not allowed')

    if entry_col is not None:
        new_board, position = make_player_move(grid, player, entry_col)
    else:
        new_board, position = make_ai_move(grid, player, app.config['AI_TREE_DEPTH'])

    return jsonify([{'grid': new_board.create_grid_from_board(), 'winner': new_board.winner, 'position': position}])

