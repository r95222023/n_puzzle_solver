from Iddfs import Iddfs
from Bfs import Bfs
from AStar import AStar
from IdAStar import IdAStar
from Node import Node
import random
import math


class NPuzzle:
    """Wrapper for all n-puzzle solver algorithm"""
    def __init__(self):
        # It can take different history for parallel computation.
        # Ex: {'[1,0,2,3,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]','[3,1,2,0,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]'}
        # for two cores machine
        self.AStar = AStar
        self.Bfs = Bfs
        self.Iddfs = Iddfs
        self.IdAStar = IdAStar

    def gen_puzzle(self, n, steps=25):
        puzzle = list(range(1, n * n)) + [0]
        node = Node(puzzle, None, 0)
        for step in range(steps):
            node = random.choice(node.get_children())

        return node.get_state()
    # def engage(self, puzzle):
    #     if self.method == "Iddfs":
    #         Iddfs().engage(puzzle)
    #     if self.method == "Bfs":
    #         Bfs({}).engage(puzzle)

    def is_solvable(self, state):
        """Check if the puzzle is solvable."""
        # count the number of inversions
        # refer to https://github.com/gliderkite/puzzle15/blob/master/puzzle15.py
        inversions = 0
        for i, v in [(i, v) for i, v in enumerate(state) if v != len(state)]:
            j = i + 1
            while j < len(state):
                if state[j] < v:
                    inversions += 1
                j += 1
        # check if the puzzle is solvable
        size = int(math.sqrt(len(state)))
        # grid width is odd and number of inversion even -> solvable
        if size % 2 != 0 and inversions % 2 == 0:
            return True
        # grid width is even
        if size % 2 == 0:
            emptyrow = size - state.index(0) // size
            return (emptyrow % 2 != 0) == (inversions % 2 == 0)
        return False

