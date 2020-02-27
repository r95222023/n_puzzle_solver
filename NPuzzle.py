from iddfs import Iddfs
from bfs import Bfs


def gen_puzzle(n, steps=25):
    import random
    puzzle = list(range(1, n*n)) + [0]
    for steps in range(steps):
        puzzle = random.choice(get_children(puzzle))

    return puzzle


class NPuzzle:
    """Class for Iddfs"""
    def __init__(self):
        # It can take different history for parallel computation.
        # Ex: {'[1,0,2,3,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]','[3,1,2,0,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]'}
        # for two cores machine
        self.iddfs = Iddfs()
        self.bfs = Bfs({})
        self.gen_puzzle = self.iddfs.gen_puzzle

    # def engage(self, puzzle):
    #     if self.method == "Iddfs":
    #         Iddfs().engage(puzzle)
    #     if self.method == "Bfs":
    #         Bfs({}).engage(puzzle)

