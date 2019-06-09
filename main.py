from connect4 import Connect4
from game_finished_checker import COMPUTER


def read_input(team):
    col = None
    while col is None:
        try:
            i = int(input(team + ": Enter the number of column:"))
            if 0 <= i <= 6:
                col = i

        except KeyboardInterrupt:
            raise
        except:
            continue
    return col


def play_with_comptuter():
    c4.print_board()
    while True:
        col = read_input("HUMAN")
        c4.red_move(col)
        c4.make_random_move(COMPUTER)


def multiplayer():
    c4.print_board()
    while True:
        col = read_input("RED")
        c4.red_move(col)
        col = read_input("BLUE")
        c4.blue_move(col)


if __name__ == '__main__':
    c4 = Connect4()
    play_with_comptuter()
