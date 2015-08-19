import time

from sudoku import Sudoku
from solver import Solver
from testdata import data

if __name__ == "__main__":

    start = time.time()

    """
        sudokus = [
            "379502000500089603006004925490350000068090537005820091600275300057003086920600750",
            "165900040000458062480070503026580400501004086008209701853010900070305018600042370"
            #"306800000500600008000070036000093800428005300060020010000904003030006150059000004",
            #"002000005008001070000003010000020400690080000700040900000600003000400809867500000"
        ]
    """
    for sudoku in data:
        solver = Solver(Sudoku(sudoku))
        solver.solve()

    end = time.time()

    print("It took", end - start, "ms to run", len(data), "Sudokus")
