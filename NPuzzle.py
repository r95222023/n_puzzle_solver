from Iddfs import Iddfs
from Bfs import Bfs
from AStar import AStar
from IdAstar import IdAStar
from Node import Node
import random


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
        last_move = None
        for step in range(steps):
            node = random.choice(node.get_children())

        return node.get_state()
    # def engage(self, puzzle):
    #     if self.method == "Iddfs":
    #         Iddfs().engage(puzzle)
    #     if self.method == "Bfs":
    #         Bfs({}).engage(puzzle)

