import math as math
from NPuzzle import NPuzzle
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


def play(state):
    command = ""
    new_state = state
    while not command == "exit":
        os.system('cls' if os.name == 'nt' else 'clear')
        if command == 'new':
            new_state = npuzzle.gen_puzzle(4, 10)
        # print(draw(random_puzzle))
        if command == 'u':
            new_state = npuzzle.get_move(new_state, 'up')
        if command == 'd':
            new_state = npuzzle.get_move(new_state, 'down')
        if command == 'l':
            new_state = npuzzle.get_move(new_state, 'left')
        if command == 'r':
            new_state = npuzzle.get_move(new_state, 'right')

        print(render(new_state))

        if command == 'solve':
            npuzzle.engage(new_state)

        command = input("Enter 'u','d','l','r' to move 0 to the up, down, left right "
                        "correspondly, 'new' to create a new puzzle, 'solve' to get the solution, 'exit' to end the program.\n>>")


npuzzle = NPuzzle().iddfs
random_puzzle = npuzzle.gen_puzzle(4, 10)
play(random_puzzle)

