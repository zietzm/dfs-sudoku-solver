import time

import numpy as np

import solver


board = np.array([
    [0,0,0,0,9,0,8,2,3],
    [0,8,0,0,3,2,0,7,5],
    [3,0,2,5,8,0,4,9,0],
    [0,2,7,0,0,0,0,0,4],
    [0,9,0,2,1,4,0,8,0],
    [4,0,0,0,0,0,2,0,0],
    [0,4,0,0,7,1,0,0,2],
    [2,0,0,9,4,0,0,5,0],
    [0,0,6,0,2,5,0,4,0]
])

b = solver.SudokuSolver(board)

t1 = time.time()

b.solve()

t2 = time.time() - t1

assert b.valid_board()

print(f"Time: {t2} seconds")
print(f"Steps: {b.num_steps}")
print(b.board)
