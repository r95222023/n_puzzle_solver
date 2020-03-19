from Node import Node, NodePool
from HeuristicFunction import ManhattanDistance
import math


class IdAStar:
    """
    Python implementation of Iterative deepening A* algorithm
    """

    def __init__(self, heuristic=ManhattanDistance()):
        self._node_expanded = 0
        self._heuristic = heuristic

    def search(self, path, bound):
        node = path[-1]
        self._node_expanded = self._node_expanded + 1
        f = node.get_f_score()
        if f > bound:
            return f
        # Solution found!
        if node.get_h_score() == 0:
            return {'path': path, 'bound': bound}
        min_t = math.inf
        # g = g + cost for each children (see Node.py line 135)
        children = node.get_children()
        for child_node in children:
            path.append(child_node)
            t = self.search(path, bound)
            if type(t) == dict:
                return t
            if t < min_t:
                min_t = t
            path.pop()
        return min_t

    def solve(self, puzzle):
        """
        Solve the given starting puzzle and
        return the {path, bound}.
        Return None if no solution has been found.
        """
        # init node, g = 0
        node = Node(puzzle, heuristic=self._heuristic, g_score=0)
        path = [node]
        bound = node.get_h_score()
        # Create the initial Node from the given position.
        # Add the initial node to the pool.
        while True:
            # Pop best node from priority queue
            self._node_expanded = 0
            t = self.search(path, bound)
            if type(t) == dict:
                # Solution found!
                node_pool = NodePool(t['path'])
                # Convert nodes to states
                route = node_pool.trace_back(t['path'][-1])
                # Make steps human readable form
                return {'steps': node_pool.read_move(route), 'route': route, 'nodes': self._node_expanded}
            if t == math.inf:
                return
            bound = t
