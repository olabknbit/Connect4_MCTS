import random


class Connect4:
    def __init__(self):
        # board has 6 rows and 7 cols
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        # last move is (row, col)
        self.last_move = None, None
        self.BLUE = -1
        self.RED = 1

    def is_valid_move(self, col):
        if col < 0 or col > 6:
            return False
        return self.board[5][-1] == 0

    def get_player_name(self, player):
        if player == self.BLUE:
            return "BLUE"
        else:
            return "RED"

    def _move(self, player, col):
        if not self.is_valid_move(col):
            print(self.get_player_name(player) + ": invalid move!")
        else:
            for row in range(6):
                if self.board[row][col] == 0:
                    self.board[row][col] = player
                    self.last_move = row, col
                    break
        self.print_board()
        return row, col

    def make_random_move(self, player):
        valid = False

        while not valid:
            col = random.choice(range(7))
            valid = self.is_valid_move(col)
        self._move(player, col)

    def check_if_game_finished(self, row, col):
        # TODO impl
        return False

    def blue_move(self, col):
        row, col = self._move(self.BLUE, col)
        self.check_if_game_finished(row, col)

    def red_move(self, col):
        row, col = self._move(self.RED, col)
        self.check_if_game_finished(row, col)

    def print_board(self):
        for i in range(len(self.board)):
            row = self.board[-1 - i]
            row_str = ""
            for el in row:
                if el == -1:
                    row_str += 'o'
                elif el == 1:
                    row_str += 'x'
                else:
                    row_str += "."
            print(row_str)
        print()
