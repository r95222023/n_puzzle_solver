import math as math
import time
from NPuzzle import NPuzzle
from Node import Node
from Heuristic_function import ManhattanDistance, MisplacementTiles
import os

# print(random_puzzle)


def render(state):
    size = int(math.sqrt(len(state)))
    top_line ="\n    "
    bottom_line="\n    "
    for i in range(0, size):
        top_line += "-----"
        bottom_line += "-----"
    top_line += "-\n    |"
    bottom_line += "-\n"
    res_str = top_line
    for i in range(0, len(state)):
        num = state[i]
        res_str = res_str + ("  " if num < 10 else " ") + str(num) \
                  + " |" + (top_line if (i + 1) % size == 0 and (i != len(state)-1) else "")
    res_str = res_str + bottom_line
    return res_str

# ['down', 'down', 'left', 'left', 'left', 'up', 'right', 'down', 'right', 'right']


def play(size):
    command = ""
    subcommand =""
    _size = size
    _heuristic = ManhattanDistance()
    npuzzle = NPuzzle()
    new_state = npuzzle.gen_puzzle(_size, 30)

    while not command == "exit":
        node = Node(new_state, None, 0)
        os.system('cls' if os.name == 'nt' else 'clear')
        if command == 'new':
            new_state = npuzzle.gen_puzzle(_size, 30)
        if command == 'size':
            while not (type(subcommand) == int and subcommand > 0):
                subcommand = input("Size=?")
                subcommand = int(subcommand)
                _size = subcommand
                new_state = npuzzle.gen_puzzle(_size, 30)

        if command == 'heuristic':
            while not (type(subcommand) == int and subcommand > 0):
                subcommand = input("Choose heuristic function. 1) Manhattan Distance, 2) Misplacement Tiles >>")
                subcommand = int(subcommand)
                if subcommand == 1:
                    _heuristic = ManhattanDistance()
                if subcommand == 2:
                    _heuristic = MisplacementTiles()

        # print(draw(random_puzzle))
        if command == 'u':
            new_state = node.get_move('up').get_state()
        if command == 'd':
            new_state = node.get_move('down').get_state()
        if command == 'l':
            new_state = node.get_move('left').get_state()
        if command == 'r':
            new_state = node.get_move('right').get_state()

        print(render(new_state))

        if command == 'solve':
            start_time = time.time()
            solution = npuzzle.AStar(_heuristic).solve(new_state)
            print('Solution:', solution['steps'])
            print('Number of nodes expanded: ', solution['nodes'])
            print('Time taken: ', time.time() - start_time, ' seconds')
        if Node(new_state, _heuristic, 0).get_h_score() == 0:
            print("Congratulation! You solved the puzzle!")
        subcommand = ""
        command = input("Enter 'u','d','l','r' to move 0 to the up, down, left right "
                        "correspondingly, 'new' to create a new puzzle, 'solve' to get the solution, "
                        "'size' to change size, 'heuristic' to select heuristic function, 'exit' to end the program.\n>>")


class CLInterface:
    """Command line interface for n puzzle solver"""

    def __init__(self):
        self.play = play
        self.render = render

