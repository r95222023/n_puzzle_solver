# n-puzzle solver
Use Breadth-first search algorithm or Iterative deepening depth-first search to find the solution of an n-puzzle games.

- **Source code:** https://github.com/r95222023/n_puzzle_solver

It provides:

- a brute force Breadth-first search algorithm for n-puzzle games (8-puzzle, 15-puzzle etc)
- Iterative deepening depth-first search which saves memory
- solvable check


Usage:
For Python, simply import from the file and initialize the class with a history or an empty dict.
Then run engage method to compute.

    from NPuzzle import NPuzzle
    fifteen_puzzle = NPuzzle().iddfs # for Breadth-first serch use NPuzzle().bfs
    fifteen_puzzle.engage([1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15])
    
tests can then be run after installation of Python with:

    python run.py