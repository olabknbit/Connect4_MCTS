import random

from game_finished_checker import HEIGHT, WIDTH, is_valid_move
from mcts import Node, MCTS


class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        # last move is (row, col)
        self.last_move = None, None
        self.BLUE = -1
        self.RED = 1

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
        if not is_valid_move(self.board, col):
            print(self.get_player_name(player) + ": invalid move!")
        else:
            for row in range(HEIGHT):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    self.last_move = row, col
                    break
        self.print_board()
        return row, col

    def make_random_move(self, player):
        valid = False
        while not valid:
            col = random.choice(range(WIDTH))
            valid = is_valid_move(self.board, col)
        self._move(player, col)

    def make_mcts_move(self, player):
        root = Node(_board=self.board, _parent=None, col=-1, root=True)
        mcts = MCTS()
        decision = mcts.monte_carlo_tree_search(root)
        col = decision.column_val
        self._move(player, col)

    def check_if_game_finished(self, row_id, col_id):
        from game_finished_checker import check_diagonal_right, check_horizontal, check_diagonal_left, check_vertical
        player = self.board[row_id][col_id]

        return check_horizontal(self.board, player, row_id, col_id) \
               or check_vertical(self.board, player, row_id, col_id) \
               or check_diagonal_right(self.board, player, row_id, col_id) \
               or check_diagonal_left(self.board, player, row_id, col_id)

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
