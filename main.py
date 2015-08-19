import time
from sudoku import Sudoku
from solver import Solver
from testdata import data

if __name__ == "__main__":

    start = time.time()

    for sudoku in data:
        solver = Solver(Sudoku(sudoku))
        solver.solve()

    end = time.time()

    print("It took", end - start, "ms to run", len(data), "Sudokus")
