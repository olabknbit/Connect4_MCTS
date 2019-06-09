import random

from . import Node, MCTS

class Connect4:
    def __init__(self):
        # board has 6 rows and 7 cols
        self.width = 7
        self.height = 6
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        # last move is (row, col)
        self.last_move = None, None
        self.BLUE = -1
        self.RED = 1

    def is_valid_move(self, col):
        if col < 0 or col > self.height:
            return False
        return self.board[self.height - 1][-1] == 0

    def get_player_name(self, player):
        if player == self.BLUE:
            return "BLUE(x)"
        else:
            return "RED(o)"

    def get_player_symbol(self, player):
        if player == self.BLUE:
            return "x"
        elif player == self.RED:
            return "o"
        else:
            return "."

    def _move(self, player, col):
        if not self.is_valid_move(col):
            print(self.get_player_name(player) + ": invalid move!")
        else:
            for row in range(self.height):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    self.last_move = row, col
                    break
        self.print_board()
        return row, col

    def make_random_move(self, player):
        valid = False
        while not valid:
            col = random.choice(range(self.width))
            valid = self.is_valid_move(col)
        self._move(player, col)

    def make_mcts_move(self, player):
        root = Node(_board=self.board, _parent=None, col=-1, root=True)
        decision = MCTS.monte_carlo_tree_search(root)
        col = decision.column_val
        self._move(player, col)

    def check_if_game_finished(self, row_id, col_id):
        player = self.board[row_id][col_id]

        def check_horizontal(row_id, col_id):
            row = self.board[row_id]

            for i in range(-3, 3):
                if row[col_id + i:col_id + i + 4] == ([player] * 4):
                    return True
            return False

        def check_vertical(row_id, col_id):
            column = [row[col_id] for row in self.board[row_id - 3:row_id + 1]]
            return row_id >= 3 and column == ([player] * 4)

        def check_diagonal_right(row_id, col_id):
            for i in range(-3, 3):
                diag = [row[col_id + j + i] if col_id + j + i < self.width else 0 for j, row in
                        enumerate(self.board[row_id + i:row_id + i + 4])]
                if diag == ([player] * 4):
                    return True
            return False

        def check_diagonal_left(row_id, col_id):
            for i in range(-3, 3):
                diag = [row[col_id - j - i] if col_id - j - i < self.width else 0 for j, row in
                        enumerate(self.board[row_id + i:row_id + i + 4])]
                if diag == ([player] * 4):
                    return True
            return False

        return check_horizontal(row_id, col_id) \
               or check_vertical(row_id, col_id) \
               or check_diagonal_right(row_id, col_id) \
               or check_diagonal_left(row_id, col_id)

    def blue_move(self, col):
        row, col = self._move(self.BLUE, col)
        if self.check_if_game_finished(row, col):
            print("BLUE won")
            exit(0)

    def red_move(self, col):
        row, col = self._move(self.RED, col)
        if self.check_if_game_finished(row, col):
            print("RED won")
            exit(0)

    def print_board(self):
        for i in range(len(self.board)):
            row = self.board[-1 - i]
            row_str = ""
            for el in row:
                row_str += self.get_player_symbol(el) + " "
            print(row_str)
        print()


