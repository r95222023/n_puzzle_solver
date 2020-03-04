import sys
import math as math
import time

history = {}
# history record every explored state with key equal to state id and value equal to the previous state id of that state.
# It is used for both hashing and rebuilding entire solution.


def get_state_id(state):
    """Create a unique id for hashing"""
    return str(state)


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

def compare(state):
    """Compare current state to the final solution"""
    res = True
    for i in range(0, len(state)-1):
        if state[i] != i+1:
            res = False
    return res


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
            state_id = get_state_id(state)
            new_state_id = get_state_id(new_state)
            if not (new_state_id in history):
                history[new_state_id] = state_id
                children.append(new_state)

    return children


def trace_back(state):
    """Find previous state recursively to rebuild the solution"""
    state_id = get_state_id(state)
    steps = [state_id]
    if state_id in history:
        previous = history[state_id]
    else:
        previous = False
    i = 0
    while previous:
        i = i + 1
        steps.append(previous)
        if previous in history:
            previous = history[previous]
        else:
            previous = False
    return steps[::-1]


def read_move(steps):
    """Convert steps to human readable moves"""
    res = []
    size = len(steps[0])
    side_size = int(math.sqrt(size))
    for i in range(0, len(steps)-1):
        state = [int(j) for j in list(steps[i].replace('[', '').replace(']', '').split(', '))]
        next_state = [int(k) for k in list(steps[i+1].replace('[', '').replace(']', '').split(', '))]
        next_pos = next_state.index(0)
        pos = state.index(0)
        rel = next_pos-pos
        direction = 'down'
        if rel == 1:
            direction = 'right'
        if rel == -1:
            direction = 'left'
        if rel == side_size:
            direction = 'up'
        res.append(direction)
    return res


def breadth_search(states):
    """Breadth depth first search"""
    cost = 0
    res = []
    children = []
    for state in states:
        cost = cost + 1
        if compare(state):
            print('Bingo!!')
            # found solution!
            steps = trace_back(state)
            # rebuild the solution
            print('Memory Usage: {} bytes'.format(sys.getsizeof(children))) #https://www.pluralsight.com/blog/tutorials/how-to-profile-memory-usage-in-python
            # check memory usage for the nodes
            res = {'Depth': len(steps)-1, 'Number of Nodes expanded': cost, 'Moves:': read_move(steps), 'Steps': trace_back(state)}
            # final result
            break
            # stop searching once find the solution
        else:
            for child in get_children(state):
                children.append(child)

    return res if ('Steps' in res) else children


def solve(state):
    """engage the computation with 'state' as the initial state"""
    start_time = time.time()
    history[get_state_id(state)] = False
    search = breadth_search([state])
    if is_solvable(state) or True:
        while not ('Steps' in search):
            search = breadth_search(search)
        print(search)
        # print('Depth: {}'.format(len(search['moves'])))
        # print('Number of Nodes expanded: {}'.format(search['cost']))
        # print('Moves: {}'.format(search['Moves']))
        # print('Steps: {}'.format(search['steps']))
    else:
        print('Warning: the given state is not solvable')
    print("Time taken: %s seconds " % (time.time() - start_time))
    return


class Bfs:
    """Class for Bfs"""
    def __init__(self, init_history):
        # It can take different history for parallel computation.
        # Ex: {'[1,0,2,3,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]','[3,1,2,0,4,5,6,7,8]':'[0,1,2,3,4,5,6,7,8]'}
        # for two cores machine
        self.history = init_history or {}
        self.is_solvable = is_solvable
        self.get_children = get_children
        self.breadth_search = breadth_search
        self.solve = solve


