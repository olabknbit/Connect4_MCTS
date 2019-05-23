from connect4 import Connect4


def read_input():
    col = None
    while col is None:
        i = int(input("Enter the number of column:"))
        if 0 < i < 6:
            col = i
    return col


if __name__ == '__main__':
    c4 = Connect4()

    while True:
        col = read_input()
        c4.red_move(col)
        c4.make_random_move(c4.BLUE)
