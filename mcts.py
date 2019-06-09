import random

import numpy as np


class Node:
    def __init__(self, _board, _parent, col, root=False):
        self.children = []
        self.board = _board
        self.parent = _parent
        self.value = 0
        self.no_visits = 0
        self.is_root = root
        # to add function chcecking legal moves from yhis state
        self.unexpanded_moves = []
        self.column_val = col  # this node was produced by a move in this column

    def visits(self):
        return self.no_visits

    def uct(self):
        return (self.value / self.no_visits) + (np.sqrt(2 * np.log(self.visits) / self.visits))

    def expand(self, move, state):
        child = Node(col=move, _parent=self, _board=state, root=False)
        self.unexpanded_moves.remove(move)
        self.children.append(child)
        return child


class MCTS:
    def __init__(self):
        from time import time
        self.start_time = time()

    def check_time(self):
        from time import time
        return (time() - self.start_time) < 5

    def monte_carlo_tree_search(self, root: Node):
        while self.check_time():
            # selection
            leaf = self.traverse(root)
            # expansion
            simulation_result = self.rollout(leaf)
            # backpropagation
            self.backpropagate(leaf, simulation_result)
        return self.best_child(root)

    def traverse(self, node: Node):
        while self.not_fully_expanded(node):
            node = self.best_uct(node)
        return self.pick_univisted(node, node.children)

    def rollout(self, node: Node):
        while self.non_terminal(node):
            node = self.rollout_policy(node)
        return self.result(node)

    def rollout_policy(self, node: Node):
        return self.pick_random(node.children)

    def backpropagate(self, node: Node, result):
        if node.is_root:
            return
        node.stats = self.update_stats(node, result)
        self.backpropagate(node.parent)

    def best_child(self, node: Node):
        return max(node.children, key=node.visits)

    def pick_random(self, children):
        return children[random.choice(range(len(children)))]

    def best_uct(self, node: Node):
        return max(node.children, key=node.uct)

    def update_stats(self, node, result):
        node.value += result

    def non_terminal(self, node):
        from game_finished_checker import check_if_game_finished, get_available_moves
        return not check_if_game_finished(node.board) and len(get_available_moves(node.board)) > 0

    def not_fully_expanded(self, node):
        if node.children == [] or node.unexpanded_moves != []:
            return True

    def result(self, board):
        from game_finished_checker import get_result
        return get_result(board)

    def pick_univisted(self, node, children):
        # todo: return either unvisited children or self - when?
        pass
