import random

import numpy as np

from game_finished_checker import check_if_game_finished, get_available_moves, make_move, COMPUTER


class Node:
    def __init__(self, _board, _parent, col, root=False):
        self.children = []
        self.board = _board
        self.parent = _parent
        self.value = 0
        self.no_visits = 0
        self.is_root = root
        # to add function chcecking legal moves from this state
        self.unexpanded_moves = get_available_moves(_board)
        self.column_val = col  # this node was produced by a move in this column

    def visits(self):
        return self.no_visits

    def uct(self):
        if self.visits() == 0:
            return np.infty
        return (self.value / self.no_visits) + (np.sqrt(2 * np.log(self.no_visits)) / self.no_visits)

    def expand(self, move, state):
        child = Node(col=move, _parent=self, _board=state, root=False)
        self.unexpanded_moves.remove(move)
        self.children.append(child)
        return child


class MCTS:
    def __init__(self):
        from time import time
        self.start_time = time()
        self.player_id = COMPUTER

    def check_time(self):
        from time import time
        return (time() - self.start_time) < 5000

    def monte_carlo_tree_search(self, root: Node):
        mcts_board = root.board
        while self.check_time():
            # selection + expansion
            leaf, mcts_board = self.traverse(root, mcts_board)
            # simulation
            simulation_result = self.rollout(mcts_board)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
        return self.best_child(root)

    def traverse(self, node: Node, mcts_board):
        while self.not_fully_expanded(node):
            # selection: select best child
            new_node = self.best_uct(node)
            if new_node is not None:
                mcts_board = make_move(mcts_board, new_node.column_val, self.player_id)
            else:
                break

        if node.unexpanded_moves != []:
            # then expansion: add one new child node
            m = node.unexpanded_moves[random.choice(range(len(node.unexpanded_moves)))]
            mcts_board = make_move(mcts_board, m, self.player_id)
            node = node.expand(move=m, state=mcts_board)
        return node, mcts_board

    def rollout(self, mcts_board):
        while self.non_terminal(mcts_board):
            available_moves = get_available_moves(mcts_board)
            mcts_board = make_move(mcts_board, available_moves[random.choice(range(len(available_moves)))],
                                   self.player_id)
        return self.result(mcts_board)

    def backpropagate(self, node: Node, result):
        if node.is_root:
            return
        node.stats = self.update_stats(node, result)
        self.backpropagate(node.parent, result)

    def best_child(self, node: Node):
        return max(node.children, key=node.visits)

    def pick_random(self, children):
        return children[random.choice(range(len(children)))]

    def best_uct(self, node: Node):
        print(node.children)
        if len(node.children) == 0:

            return None
        return max(node.children, key=Node.uct)

    def update_stats(self, node, result):
        node.value += result
        node.no_visits += 1

    def non_terminal(self, board):
        return not check_if_game_finished(board) and len(get_available_moves(board)) > 0

    def not_fully_expanded(self, node):
        if node.children == [] or node.unexpanded_moves != []:
            return True

    def result(self, board):
        from game_finished_checker import get_result
        return get_result(board)
