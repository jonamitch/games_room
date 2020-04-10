import config
from game_classes import Board, Player
import ai_calc
import next_move_calculator

if __name__ == '__main__':

    stop = None
    while stop is None:
        print('#############################')
        print('Starting game of Connect4!')

        # Initialise board and player 1
        board = Board(config.board_width, config.board_height)
        print(board)
        player = Player(1)
        tree = None

        # Set-up any player 1 move sequences
        if len(config.player_1_initial_moves) > 0 and config.use_player_1_initial_moves:
            player_one_preset_moves = config.player_1_initial_moves
        else:
            player_one_preset_moves = []

        # Set-up board for any initial moves
        if len(config.board_initial_moves) > 0 and config.use_board_initial_moves and len(player_one_preset_moves) == 0:
            print('Performing configured initial moves')
            for move in config.board_initial_moves:
                player = Player(move[1])
                board.add_counter(move[0], player)
            player = player.next_player()
            print(board)

        # Loops through goes
        while not board.winner:
            if player.num == 1:
                column = None
                while column is None:
                    if len(player_one_preset_moves) > 0:
                        text = player_one_preset_moves.pop(0)
                    else:
                        text = input("Player {}: Enter the column to put a counter in (1-7): ".format(player.num))
                    if text in ['1', '2', '3', '4', '5', '6', '7']:
                        column = int(text) - 1
                        column = board.add_counter(column, player)
                        if column is None:
                            print('Please enter a column with space')
                    else:
                        print('Please enter a number between 1 and 7')
            if player.num == 2:
                # suggested_move = next_move_calculator.calc_next_move(board, player, config.depth)
                tree, suggested_move = ai_calc.calc_next_move(board, player, config.depth, tree)
                column = board.add_counter(suggested_move, player)
                print('Player {} played into column: {}'.format(player.num, suggested_move + 1))
            print(board)
            player = player.next_player()
        print('Player {} wins!'.format(board.winner))
        print('#############################')
        stop_text = input("Input 'Y' to play again:")
        if stop_text != 'Y' and stop_text != 'y':
            stop = True
    print('Thanks for playing!')
