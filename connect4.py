import random

from game_finished_checker import HEIGHT, WIDTH, COMPUTER, HUMAN, is_valid_move, _print_board
from mcts import Node, MCTS


class Connect4:
    def __init__(self):
        self.board = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
        # last move is (row, col)
        self.last_move = None, None

    def get_player_name(self, player):
        if player == COMPUTER:
            return "COMPUTER(x)"
        else:
            return "HUMAN(o)"

    def _move(self, player, col):
        if not is_valid_move(self.board, col):
            print(self.get_player_name(player) + ": invalid move!")
        else:
            for row in range(HEIGHT):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    self.last_move = row, col
                    break
        _print_board(self.board)
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
        row, col = self._move(COMPUTER, col)
        if self.check_if_game_finished(row, col):
            print("COMPUTER won")
            exit(0)

    def red_move(self, col):
        row, col = self._move(HUMAN, col)
        if self.check_if_game_finished(row, col):
            print("HUMAN won")
            exit(0)

    def print_board(self):
        _print_board(self.board)