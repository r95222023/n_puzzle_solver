import copy
import math
import time


def move(state, pos, rel_pos):
    """Move zero to a new position with rel_pos relative to current position"""
    new_state = state.copy()
    return swap(new_state, pos, pos + rel_pos)


def swap(state, from_pos, to_pos):
    """Swap zero from current position to a new position"""
    cache = state[from_pos]
    state[from_pos] = state[to_pos]
    state[to_pos] = cache
    return state


def get_moves(side_size, col, row):
    """Create dict for moves that has the has the information such as
       relative position for zero to swap and is that move possible for each move"""
    return {
        'up': {
            'rel_pos': -1*side_size,
            'is_movable': row > 0
        },
        'left': {
            'rel_pos': -1,
            'is_movable': col > 0
        },
        'down': {
            'rel_pos': side_size,
            'is_movable': row < (side_size-1)
        },
        'right': {
            'rel_pos': 1,
            'is_movable': col < (side_size-1)
        },
    }


class Node:
    """
    A node is a position (immutable) in the puzzle
    It also contains the gScore, hScore, fScore and
    the list of moves which bring us to this position
    """

    def __init__(self, state, heuristic, g_score=0):
        """
        Builds a new node
        """
        self._state = state
        self._size =  int(math.sqrt(len(state)))
        self._heuristic = heuristic
        self._h_score = None
        self._g_score = g_score

    def get_size(self):
        return self._size

    def get_state(self):
        """
        Get position of the Node (nested list of integers)
        """
        return copy.deepcopy(self._state)

    def get_g_score(self):
        """
        Get gScore of the Node
        """
        return self._g_score

    def get_h_score(self):
        """
        Get hScore of this Node. Heuristic passed in
        the constructor will be used for computation
        """
        if self._h_score is None:
            self._h_score = self._heuristic.compute(self)
        return self._h_score

    def get_f_score(self):
        """
        Get fScore of the Node
        fScore = gScore + hScore
        """
        return self.get_g_score() + self.get_h_score()

    def get_heuristic(self):
        """
        Return heuristic used to compute hScore for this node
        """
        return self._heuristic

    def get_coord_by_value(self, value):
        """
        Get i and j coord of the given value
        """
        pos = self._state.index(value)+1
        row = pos // self._size
        col = pos % self._size
        return [row, col]

    def get_state_id(self):
        return str(self._state)

    def get_move(self, direction):
        """Get new state from current state by moving empty space in a direction"""
        pos = self._state.index(0)
        row = pos // self._size
        col = pos % self._size
        moves = get_moves(self._size, col, row)
        new_state = self._state
        if direction in moves:
            if moves[direction]['is_movable']:
                new_state = move(self._state, pos, moves[direction]['rel_pos'])
        return Node(new_state, self._heuristic, self._g_score+1)

    def get_children(self):
        """Create all possible unexplored node from current state"""
        children = []
        side_size = int(math.sqrt(len(self._state)))
        pos = self._state.index(0)
        row = pos // side_size
        col = pos % side_size
        moves = get_moves(side_size, col, row)
        for direction in moves:
            if moves[direction]['is_movable']:
                new_state = move(self._state, pos, moves[direction]['rel_pos'])
                children.append(Node(new_state, self._heuristic, self._g_score+1))

        return children


class NodePool:
    """
    Contains list of Nodes used by A* algorithm.

    This is an enhanced implementation of a priority queue
    designed especially to solve 15-puzzle problems
    """

    def __init__(self):
        self._pool = []
        self._history = {}

    def get_history(self):
        return self._history

    def add(self, node, prev_node):
        """
        Add new Node to the pool
        Nodes previously added will not be added again
        """
        state_id = node.get_state_id()
        if state_id in self._history:
            # duplicate entry
            return

        if node != prev_node:
            self._history[state_id] = prev_node.get_state_id()
        else:
            self._history[state_id] = False
        self._insort(node)

    def pop(self):
        """
        Pop the node with best score (first in the pool)
        """
        return self._pool.pop(0)

    def is_empty(self):
        """
        Return true if the priority queue does not contain any node
        """
        return len(self._pool) == 0

    def _insort(self, node):
        """
        Insert the node in the pool while keeping the list ordered
        """
        lo = 0
        hi = len(self._pool)
        f_score = node.get_f_score()
        while lo < hi:
            mid = (lo+hi)//2
            if f_score < self._pool[mid].get_f_score(): hi = mid
            else: lo = mid + 1
        self._pool.insert(lo, node)

    def trace_back(self, node):
        """Find previous state recursively to rebuild the solution"""
        state_id = node.get_state_id()
        steps = [eval(state_id)]
        if state_id in self._history:
            previous = self._history[state_id]
        else:
            previous = False
        while previous:
            steps.append(eval(previous))
            if previous in self._history:
                previous = self._history[previous]
            else:
                previous = False
        return steps[::-1]

    def read_move(self, steps):
        """Convert steps to human readable moves"""
        res = []
        size = len(steps[0])
        side_size = int(math.sqrt(size))
        for i in range(0, len(steps) - 1):
            state = steps[i]
            next_state = steps[i + 1]
            next_pos = next_state.index(0)
            pos = state.index(0)
            rel = next_pos - pos
            direction = 'up'
            if rel == 1:
                direction = 'right'
            if rel == -1:
                direction = 'left'
            if rel == side_size:
                direction = 'down'
            res.append(direction)
        return res