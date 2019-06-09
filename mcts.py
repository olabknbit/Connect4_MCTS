import random


class Node:
    def __init__(self, _board, _parent, col, root=False):
        self.children = []
        self.board = _board
        self.parent = _parent
        self.value = 0
        self.no_visits = 0
        self.is_root = root
        self.column_val = col

    def visits(self):
        return self.no_visits

    def uct(self):
        # todo: implement uct
        return self.value


class MCTS:

    def check_time(self):
        return True

    def monte_carlo_tree_search(self, root: Node):
        while self.check_time():
            leaf = self.traverse(root)
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
        return self.best_child(root)

    def traverse(self, node: Node):
        while self.fully_expanded(node):
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

    def fully_expanded(self, node):
        # todo: check if nodes present in constructed tree
        pass

    def result(self, node):
        # todo: check game result at this state (board)
        pass

    def pick_univisted(self, node, children):
        # todo: return either unvisited children or self - when?
        pass
