class ManhattanDistance:
    """
    Implementation of Manhattan distance heuristic
    """
    def __init__(self):
        return

    def compute(self, node):
        """
        Computes Manhattan distance of the given Node
        """
        score = 0
        size = node.get_size()
        size_square = size**2
        for value in range(1, size_square):
            goal_row = value // size
            goal_col = value % size
            actual_row, actual_col = node.get_coord_by_value(value)
            score += abs(goal_row - actual_row) + abs(goal_col - actual_col)
        # score += abs(size_square-1 - node.get_state().index(0))
        return score


class MisplacementTiles:
    """
    Implementation of Number of Misplacement tiles heuristic
    """

    def __init__(self):
        return

    def compute(self, node):
        """
        Computes Number of Misplacement tiles of the given Node
        """
        score = 0
        size = node.get_size()
        size_square = size**2
        for value in range(1, size_square):
            goal_row = value // size
            goal_col = value % size
            actual_row, actual_col = node.get_coord_by_value(value)
            if goal_col != actual_col or goal_row != actual_row:
                score += 1
        if (size_square - 1) != node.get_state().index(0):
            score += 1
        return score
