from Node import Node, NodePool


class AStar:
    """
    Python implementation of A* algorithm
    """

    def __init__(self, heuristic):
        self._node_pool = NodePool()
        self._heuristic = heuristic

    def solve(self, puzzle):
        """
        Solve the given starting puzzle and
        return the {route, steps, nodes}.
        Return None if no solution has been found.
        """
        node = Node(puzzle, self._heuristic, 0)
        self._node_pool.add(node, False)
        # Create the initial Node from the given position.
        # Add the initial node to the pool.
        while not self._node_pool.is_empty():
            # Pop best node from priority queue
            current_node = self._node_pool.pop()
            if current_node.get_h_score() == 0:
                # Solution found!
                route = self._node_pool.trace_back(current_node)
                return {'route': route, 'steps': self._node_pool.read_move(route), 'nodes': len(self._node_pool.get_history())}
            # Compute child nodes and add them to the queue
            children = current_node.get_children()
            for child in children:
                self._node_pool.add(child, current_node)
        # No solution has been found
        return None
