from .caching import cache_score_of_board
from copy import copy, deepcopy


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return "[{},{}]".format(self.x, self.y)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x)

    def multiply(self, multiplier):
        return Position(self.x * multiplier, self.y * multiplier)

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def is_unit(self):
        return self.x in [-1, 0, 1] and self.y in [-1, 0, 1] and not self.is_zero()


class Vector:
    def __init__(self, coord, direction, multiple, self_index=0):
        assert(direction.is_unit())
        self.coords = set()
        for i in range(multiple):
            adj_multiple = i - self_index
            self.coords.add(coord + direction.multiply(adj_multiple))
        self.is_vertical = direction == Position(0, 1) or direction == Position(0, -1)

    def __repr__(self):
        return "[{}]".format(','.join([str(x) for x in self.coords]))

    def contains_coord(self, coord):
        return coord in self.coords


class Board:
    def __init__(self, grid):
        self.right_up_directions = [Position(0, 1), Position(1, 1), Position(1, 0), Position(1, -1)]
        self.height = len(grid)
        self.heights = range(self.height)
        self.width = len(grid[0])
        self.widths = range(self.width)
        self.fours = []
        self.calc_fours()
        self.four_dict = {}
        self.calc_four_dict()

        self.live_heights = {entry: 0 for entry in self.widths}
        self.live_heights = {}
        self.active_positions_1 = set()
        self.active_positions_2 = set()
        self.create_board_from_grid(grid)
        self.winner = None
        self.score_details = {}
        self.score = None

    def create_grid_from_board(self):
        grid = [[0 for _ in self.widths] for _ in self.heights]
        for position in self.active_positions_1:
            grid[self.height - position.y - 1][position.x] = 1
        for position in self.active_positions_2:
            grid[self.height - position.y - 1][position.x] = 2
        return grid

    def create_board_from_grid(self, grid):
        for grid_row_num, row in enumerate(grid):
            row_num = self.height - grid_row_num - 1
            for col_num, cell in enumerate(row):
                if cell == 0:
                    continue
                if col_num not in self.live_heights:
                    self.live_heights[col_num] = row_num + 1
                position = Position(col_num, row_num)
                if cell == 1:
                    self.active_positions_1.add(position)
                else:
                    self.active_positions_2.add(position)
        for col in self.widths:
            if col not in self.live_heights:
                self.live_heights[col] = 0

    def create_child_board(self):
        child_board = copy(self)
        child_board.active_positions_1 = copy(self.active_positions_1)
        child_board.active_positions_2 = copy(self.active_positions_2)
        child_board.live_heights = copy(self.live_heights)
        child_board.score_details = copy(self.score_details)
        child_board.winner = self.winner
        child_board.score = self.score
        return child_board

    def __repr__(self):
        row = 'Board: {} \r\n'.format(self.id())
        for y in self.heights[::-1]:
            for x in self.widths:
                if self.live_heights[x] <= y:
                    row += '-  '
                elif Position(x, y) in self.active_positions_1:
                    row += 'X  '
                else:
                    row += 'O  '
            row += '\r\n'
        for x in self.widths:
            row += '---'.format(x + 1)
        row += '\r\n'
        for x in self.widths:
            row += '{}  '.format(x+1)
        row += '\r\n'
        row += 'Score: {}'.format(self.score_details)
        return row

    def id(self):
        id = ''
        for x in self.widths:
            used_heights = range(self.live_heights[x])
            for y in used_heights:
                if Position(x, y) in self.active_positions_1:
                    id += '1'
                else:
                    id += '2'
            id += '0'
        return id

    def valid_moves(self):
        return [entry for entry in self.widths if self.live_heights[entry] < self.height]

    def is_on_board(self, coord):
        return (coord.x in self.widths) and (coord.y in self.heights)

    def calc_fours(self):
        for x in self.widths:
            for y in self.heights:
                coord = Position(x, y)
                for direction in self.right_up_directions:
                    end_coord = coord + direction.multiply(3)
                    if self.is_on_board(end_coord):
                        self.fours.append(Vector(coord, direction, 4))

    def calc_four_dict(self):
        for x in self.widths:
            for y in self.heights:
                coord = Position(x, y)
                self.four_dict[coord] = set()
                for vector in self.fours:
                    if vector.contains_coord(coord):
                        self.four_dict[coord].add(vector)
                # self.four_dict[coord] = [vector for vector in self.fours if vector.contains_coord(coord)]

    def get_all_fours_intersecting(self, set_of_coords):
        all_fours_intersecting = set()
        for coord in set_of_coords:
            all_fours_intersecting |= self.four_dict[coord]
        return all_fours_intersecting

    def get_all_live_positions(self):
        return self.active_positions_1 | self.active_positions_2

    @cache_score_of_board()
    def calc_score_of_board(self):
        score = {1: 0, 2: 0}
        for vector in self.get_all_fours_intersecting(self.get_all_live_positions()):
            vector_score = [0, 0, 0]
            for coord in vector.coords:
                if coord in self.active_positions_1:
                    vector_score[0] += 1
                elif coord in self.active_positions_2:
                    vector_score[1] += 1
                elif vector.is_vertical:
                    vector_score[2] += 1
                else:
                    vector_score[2] += coord.y - self.live_heights[coord.x] + 1
            if vector_score[0] == 0 and vector_score[1] == 0:
                pass
            elif vector_score[0] > 0 and vector_score[1] > 0:
                pass
            else:
                for player_num in [1, 2]:
                    if vector_score[player_num - 1] > 0:
                        if vector_score[2] == 0:
                            self.winner = Player(player_num).num
                        score[player_num] += 10 ** max(6 - vector_score[2], 0)
        score[0] = score[1] - score[2]
        self.score_details = score
        self.score = score[0]

    def play_move(self, entry, player):
        height = self.live_heights[entry]
        if height < self.height:
            new_entry = Position(entry, height)
            if player.num == 1:
                self.active_positions_1.add(new_entry)
            else:
                self.active_positions_2.add(new_entry)
            self.live_heights[entry] = height + 1
            self.calc_score_of_board()
            return new_entry
        else:
            return None


class Player:
    def __init__(self, player_num):
        self.num = player_num

    def next_player(self):
        return Player(3 - self.num)

    def max_min(self):
        if self.num == 1:
            return max
        else:
            return min
