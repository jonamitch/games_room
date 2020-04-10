from .game_classes import Board, Player
from .ai_calc import calc_next_move


def make_player_move(grid, player_num, entry_col):
    board = Board(grid)
    player = Player(player_num)
    position = board.add_counter(entry_col, player)
    if position:
        return board, (position.x, position.y)
    else:
        return board, None


def make_ai_move(grid, player_num, depth):
    board = Board(grid)
    player = Player(player_num)
    tree, suggested_move = calc_next_move(board, player, depth)
    position = board.add_counter(suggested_move, player)
    if position:
        return board, (position.x, position.y)
    else:
        return board, None



