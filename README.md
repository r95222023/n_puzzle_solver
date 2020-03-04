# n-puzzle solver
Use different search algorithm to solve the n-puzzle (8-, 15-puzzle etc...) games.

- **Source code:** https://github.com/r95222023/n_puzzle_solver

It provides:

- Breadth-first search
- Iterative deepening depth-first search
- A* search with Manhattan Distance and Misplacement Tiles heuristic functions 
- Command line interface that allows user to play the n puzzle game and solve the 
  puzzle with different search algorithm


Usage:
Import the NPuzzle class and use solve method. For example, 

    from NPuzzle import NPuzzle
    from HeuristicFunction import ManhattanDistance, MisplacementTiles

    puzzle = [1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15]
    n_puzzle = NPuzzle()
    
    # for A* Search
    bfs = n_puzzle.AStar(ManhattanDistance())
    bfs.solve(puzzle)
    
    # for Iterative Deepening Depth-First Search
    iddfs = n_puzzle.Iddfs()
    iddfs.solve(puzzle)
    
    # for Breadth-First Search
    bfs = n_puzzle.Bfs()
    bfs.solve(puzzle)
    
To play the n-puzzle game, simply run

    python play.py
    
Tests can be run with:

    python run.py