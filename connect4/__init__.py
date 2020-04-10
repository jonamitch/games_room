from connect4.game_classes import Board, Player
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


if __name__ == '__main__':

    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0]
    ]

    board, position = make_move(grid, 2, depth=6)
    print(board.create_grid_from_board())
