__author__ = 'MrTrustworthy'

from field import Field

class Sudoku:
    """
    Represents a Sudoku with rows, cols and boxes
    """


    # defines the filer-functions to determine the boxes
    # box order is left->right then top->bottom
    box_definition = [
        lambda fld: 0 <= fld.x < 3 and 0 <= fld.y < 3,
        lambda fld: 3 <= fld.x < 6 and 0 <= fld.y < 3,
        lambda fld: 6 <= fld.x < 9 and 0 <= fld.y < 3,
        lambda fld: 0 <= fld.x < 3 and 3 <= fld.y < 6,
        lambda fld: 3 <= fld.x < 6 and 3 <= fld.y < 6,
        lambda fld: 6 <= fld.x < 9 and 3 <= fld.y < 6,
        lambda fld: 0 <= fld.x < 3 and 6 <= fld.y < 9,
        lambda fld: 3 <= fld.x < 6 and 6 <= fld.y < 9,
        lambda fld: 6 <= fld.x < 9 and 6 <= fld.y < 9
    ]

    def __init__(self, raw_data):
        """
        Creates a sudoku object based on the given raw data
        :param raw_data: String in the form of "0040012006...." which represents a sudoku left->right->top->bottom
        :return: self
        """

        self.fields = []
        self.amount_given = 0
        self.raw_data = raw_data

        if len(self.raw_data) != 81:
            raise ValueError("Sudoku raw data doesnt have 81 fields!")

        self.parse_raw()


    def parse_raw(self):
        """
        Calculates and generates the Fields of the sudoku based on the given raw data
        :return:
        """

        raw = [int(val) for val in self.raw_data]

        givens = list(filter(lambda x: x != 0, raw))
        self.amount_given = str(len(givens))
        print("Sudoku has", self.amount_given, "Givens already")

        for col_idx in range(9):
            for row_idx in range(9):
                val = raw[col_idx * 9 + row_idx]
                fld = Field(row_idx, col_idx, val)

                self.fields.append(fld)


    def sort_wrapper(function):
        """
        Utility wrapper function to sort the returns of get_row/col/box
        :param function: any of self.get_row/col/box
        :return: sorted output of the given function
        """
        def function_wrapper(*args, **kwargs):
            return sorted(function(*args, **kwargs), key=lambda fld: fld.x + fld.y * 9)
        return function_wrapper


    @sort_wrapper
    def get_row(self, index):
        return filter(lambda fld: fld.y == index, self.fields)

    def get_rows(self):
        return [self.get_row(i) for i in range(9)]

    @sort_wrapper
    def get_col(self, index):
        return filter(lambda fld: fld.x == index, self.fields)

    def get_cols(self):
        return [self.get_col(i) for i in range(9)]

    @sort_wrapper
    def get_box(self, index):
        return filter(self.box_definition[index], self.fields)

    def get_boxes(self):
        return [self.get_box(i) for i in range(9)]

    def is_solved(self):
        """
        Checks if a sudoku has all fields filled out.
        Does NOT contain information about whether those numbers are correct.
        :return: Boolean
        """
        for field in self.fields:
            if not field.value:
                return False
        return True

    def is_correct(self):
        """
        Calculates whether the Sudoku is correct so far, based on the rule that no number
        can occur twice in a row, col or box
        :return: True if sudoku has no conflicting numbers, else False
        """
        groups = self.get_rows() + self.get_cols() + self.get_boxes()
        for group in groups:
            group_values = [field.value for field in group]
            for number in range(1, 10):
                if group_values.count(number) != 1:
                    return False
        return True

    def __repr__(self):
        """
        Calls self.__str__ to ease debugging
        :return:
        """
        return self.__str__()

    def __str__(self):
        """
        Creates a string representation of the sudoku with all Rows and their current values
        :return: String containing the representation
        """
        string_representation = ""
        for row_idx in range(9):
            string_representation += "Row " + str(row_idx) + ": "
            for field in self.get_row(row_idx):
                string_representation += str(field)
            string_representation += "\n"
        return string_representation
