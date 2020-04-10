from game_classes import Board

if __name__ == '__main__':

    stop = None
    while stop is None:
        print('#############################')
        print('Starting game of Connect4!')

        board_height = 7
        board_width = 7
        board = Board(board_width, board_height)
        print(board)
        player = 1
        # Loops through goes
        while not board.winner:
            column = None
            while column is None:
                text = input("Player {}: Enter the column to put a counter in (1-7): ".format(player))
                if text in ['1', '2', '3', '4', '5', '6', '7']:
                    column = int(text) - 1
                    column = board.add_counter(column, player)
                    if column is None:
                        print('Please enter a column with space')
                else:
                    print('Please enter a number between 1 and 7')
            print(board)
            player = 3 - player
        print('Player {} wins!'.format(board.winner))
        print('#############################')
        stop_text = input("Input 'Y' to play again:")
        if stop_text != 'Y' and stop_text != 'y':
            stop = True
    print('Thanks for playing!')
