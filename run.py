from NPuzzle import NPuzzle
from HeuristicFunction import ManhattanDistance, MisplacementTiles
from CLInterface import CLInterface
import time

puzzle = [1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15]
n_puzzle = NPuzzle()

# for A* Search
a_star = n_puzzle.AStar(ManhattanDistance())

# example
print("Example:")
start_time = time.time()
solution = a_star.solve(puzzle)
print('Solution:', solution['steps'])
print('Number of nodes expanded: ', solution['nodes'])
print('Time taken: ', time.time() - start_time, ' seconds\n')

command = input("Do you want to play a game (y/n)? ")

if command == "y":
    CLInterface().play(4)
