# board has 6 rows and 7 cols
WIDTH = 7
HEIGHT = 6


def check_horizontal(board, player, row_id, col_id):
    row = board[row_id]

    for i in range(-3, 3):
        if row[col_id + i:col_id + i + 4] == ([player] * 4):
            return True
    return False


def check_vertical(board, player, row_id, col_id):
    column = [row[col_id] for row in board[row_id - 3:row_id + 1]]
    return row_id >= 3 and column == ([player] * 4)


def check_diagonal_right(board, player, row_id, col_id):
    for i in range(-3, 3):
        diag = [row[col_id + j + i] if col_id + j + i < WIDTH else 0 for j, row in
                enumerate(board[row_id + i:row_id + i + 4])]
        if diag == ([player] * 4):
            return True
    return False


def check_diagonal_left(board, player, row_id, col_id):
    for i in range(-3, 3):
        diag = [row[col_id - j - i] if col_id - j - i < WIDTH else 0 for j, row in
                enumerate(board[row_id + i:row_id + i + 4])]
        if diag == ([player] * 4):
            return True
    return False


def check_if_game_finished(board):
    for row_id in range(HEIGHT):
        for col_id in range(WIDTH):

            player = board[row_id][col_id]
            if check_horizontal(board, player, row_id, col_id) \
                    or check_vertical(board, player, row_id, col_id) \
                    or check_diagonal_right(board, player, row_id, col_id) \
                    or check_diagonal_left(board, player, row_id, col_id):
                return True

    return False
