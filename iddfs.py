import math as math
import time
import resource
history = {}
# history record every explored state with key equal to state id and value equal to the previous state id of that state.
# It is used for both hashing and rebuilding entire solunjtion.


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


# def compare(arr1, arr2):
#     res = True
#     if not arr1 or not arr2:
#         res = False
#
#     for i in range(0, len(arr1)):
#         if arr1[i] != arr2[i]:
#             res = False
#     return res


def is_solvable(state):
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


def get_children(state):
    """Create all possible unexplored node from current state"""
    children = []
    side_size = int(math.sqrt(len(state)))
    pos = state.index(0)
    row = pos // side_size
    col = pos % side_size
    moves = get_moves(side_size, col, row)
    for direction in moves:
        if moves[direction]['is_movable']:
            new_state = move(state, pos, moves[direction]['rel_pos'])
            children.append(new_state)

    return children


def get_move(state, direction):
    """Get new state from current state by moving empty space in a direction"""
    side_size = int(math.sqrt(len(state)))
    pos = state.index(0)
    row = pos // side_size
    col = pos % side_size
    moves = get_moves(side_size, col, row)
    new_state = state
    if direction in moves:
        if moves[direction]['is_movable']:
            new_state = move(state, pos, moves[direction]['rel_pos'])
    return new_state


def read_move(steps):
    """Convert steps to human readable moves"""
    res = []
    size = len(steps[0])
    side_size = int(math.sqrt(size))
    for i in range(0, len(steps)-1):
        state = steps[i]
        next_state = steps[i+1]
        next_pos = next_state.index(0)
        pos = state.index(0)
        rel = next_pos-pos
        direction = 'up'
        if rel == 1:
            direction = 'right'
        if rel == -1:
            direction = 'left'
        if rel == side_size:
            direction = 'down'
        res.append(direction)
    return res


def gen_puzzle(n, steps=25):
    import random
    puzzle = list(range(1, n*n)) + [0]
    for steps in range(steps):
        puzzle = random.choice(get_children(puzzle))

    return puzzle


# start_time = time.time()
# print("Solution: %s" % read_move(id_dfs([1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15])))
# print("Time taken: %s seconds " % (time.time() - start_time))
# print("Total Memory used: %s bytes " % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
#
# start_time = time.time()
# print("Solution: %s" % read_move(id_dfs([2,3,4,8,1,5,7,0,9,6,10,12,13,14,11,15])))
# print("Time taken: %s seconds " % (time.time() - start_time))
# print("Total Memory used: %s bytes " % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
#
#
# random_puzzle = gen_puzzle(4, 70)
# print("Random Puzzle: %s" % random_puzzle)
# print("Solution: %s" % read_move(id_dfs(random_puzzle)))
# print("Time taken: %s seconds " % (time.time() - start_time))
# print("Total Memory used: %s bytes " % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

class Iddfs:
    """Class for Iddfs"""
    def __init__(self, **kargs):
        # It can take different history for parallel computation.
        # Ex: {'[1,0,2,3,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]','[3,1,2,0,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]'}
        # for two cores machine
        # self.show_nodes = True if ("show_nodes" in kargs) else False
        self.get_children = get_children
        self.nodes = 0
        self.get_move = get_move
        self.gen_puzzle = gen_puzzle

    def id_dfs(self, puzzle):
        import itertools
        goal = [i for i in range(1, len(puzzle))] + [0]

        for depth in itertools.count():
            route = self.dfs([puzzle], goal, depth)
            if route:
                return route

    def dfs(self, route, goal, depth):
        self.nodes = self.nodes + 1
        if depth == 0:
            return
        if route[-1] == goal:
            # print('Memory Usage: {} bytes'.format(sys.getsizeof(
            #     route)))  # https://www.pluralsight.com/blog/tutorials/how-to-profile-memory-usage-in-python
            return route
        for child_node in get_children(route[-1]):
            if child_node not in route:
                next_route = self.dfs(route + [child_node], goal, depth - 1)
                if next_route:
                    return next_route

    def engage(self, puzzle):
        print("Puzzle: %s" % puzzle)
        self.nodes = 0
        start_time = time.time()
        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        route = self.id_dfs(puzzle)
        end_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print("Solution: %s" % read_move(route))
        print("Number of Nodes expanded: %s" % self.nodes)
        print("Time taken: %s seconds " % (time.time() - start_time))
        print("Total Memory used: %s bytes " % (end_mem - start_mem))


