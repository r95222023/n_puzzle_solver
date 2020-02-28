import math as math
from NPuzzle import NPuzzle
npuzzle = NPuzzle().iddfs
random_puzzle = npuzzle.gen_puzzle(4, 30)

# print(random_puzzle)


def render(state):
    size = int(math.sqrt(len(state)))
    res_str = "    -------------\n    |"
    for i in range(0, len(state)):
        num = state[i]
        res_str = res_str + (" " if num < 10 else "") + str(num) + "|" + ("\n    -------------\n    |" if (i+1) % size == 0 else "")
    return res_str

# ['down', 'down', 'left', 'left', 'left', 'up', 'right', 'down', 'right', 'right']

def play(state):
    command = ""
    new_state = state
    while not command == "exit":
        # print(draw(random_puzzle))
        if command == 'u':
            new_state = npuzzle.get_move(new_state, 'up')
        if command == 'd':
            new_state = npuzzle.get_move(new_state, 'down')
        if command == 'l':
            new_state = npuzzle.get_move(new_state, 'left')
        if command == 'r':
            new_state = npuzzle.get_move(new_state, 'right')

        if command == 'solve':
            npuzzle.engage(random_puzzle)
        else:
            print(render(new_state))

        command = input("Enter 'u','d','l','r' to move blank space to the up, down, left right "
                        "correspondly or enter 'solve' to get the solution, 'exit' to end the program\n>>")


play(random_puzzle)

