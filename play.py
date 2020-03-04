import math as math
from NPuzzle import NPuzzle
from Node import Node
from Heuristic_function import ManhattanDistance, MisplacementTiles
import os

# print(random_puzzle)


def render(state):
    size = int(math.sqrt(len(state)))
    res_str = "\n    ---------------------\n    |"
    for i in range(0, len(state)):
        num = state[i]
        res_str = res_str + ("  " if num < 10 else " ") + str(num) \
                  + " |" + ("\n    ---------------------\n    |" if (i + 1) % size == 0 and (i != len(state)-1) else "")
    res_str = res_str + "\n    ---------------------\n"
    return res_str

# ['down', 'down', 'left', 'left', 'left', 'up', 'right', 'down', 'right', 'right']


def play(heuristic):
    command = ""
    npuzzle = NPuzzle()
    new_state = npuzzle.gen_puzzle(4, 30)

    while not command == "exit":
        node = Node(new_state, None, 0)
        os.system('cls' if os.name == 'nt' else 'clear')
        if command == 'new':
            new_state = npuzzle.gen_puzzle(4, 30)
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
            print(npuzzle.AStar(heuristic).solve(new_state))

        command = input("Enter 'u','d','l','r' to move 0 to the up, down, left right "
                        "correspondly, 'new' to create a new puzzle, 'solve' to get the solution, 'exit' to end the program.\n>>")



play(ManhattanDistance())

