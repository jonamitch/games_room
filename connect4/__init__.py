from .game_classes import Board, Player
from ai_alpha_beta.ai_alpha_beta import calc_next_move


def make_move(grid, player_num, entry_col=None, depth=1):
    board = Board(grid)
    player = Player(player_num)
    if entry_col is None:
        tree, entry_col = calc_next_move(board, player, depth)
    position = board.play_move(entry_col, player)
    if position:
        return board, (position.x, position.y)
    else:
        return board, None
