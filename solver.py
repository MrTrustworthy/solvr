__author__ = 'MrTrustworthy'



class Solver:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def solve(self):
        print("Solving Sudoku now!")
        # print("Sudoku is:\n" + str(self.sudoku))

        found_new_value = True
        while found_new_value and not self.sudoku.is_solved():
            # found_new_value = False
            self.eliminate_possibilities()
            found_new_value = self.write_definite()

        self.print_result()


    def eliminate_possibilities(self):

        def remove_possibility(group, number):
            for field in group:
                if not field.solved and number in field.possible:
                    field.possible.remove(number)

        groups = self.sudoku.get_rows() + self.sudoku.get_cols() + self.sudoku.get_boxes()

        for group in groups:
            for field in group:
                if field.solved:
                    # print("Removing", field.value, "from group", group)
                    remove_possibility(group, field.value)

    def write_definite(self):
        found_definite = False
        for field in self.sudoku.fields:
            # if not field.solved: print(len(field.possible))
            if not field.solved and len(field.possible) <= 1:
                # print("Determined single value for", field.x, ":", field.y, "to be", field.possible[0])
                field.set_value(field.possible[0])
                found_definite = True
        return found_definite

    def print_result(self):
        print("Finished solving sudoku!")
        print("Solved:", self.sudoku.is_solved())
        print("Correct:", self.sudoku.is_correct())
        print("Result:\n" + str(self.sudoku))
        print(20 * "*")
