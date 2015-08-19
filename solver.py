__author__ = 'MrTrustworthy'

import pdb

class Solver:
    """
    The solver takes a sudoku and tries to solve it
    """

    def __init__(self, sudoku):
        """
        Basic constructor
        :param sudoku: a "Sudoku" Object
        :return: self
        """
        self.sudoku = sudoku


    def solve(self):
        """
        Tries to solve a sudoku
        :return: None
        """
        print("Solving Sudoku now!")
        print("Sudoku is:\n" + str(self.sudoku))

        # we want to find out when a run went through without changing something
        go_on = True

        while go_on and not self.sudoku.is_solved():

            go_on = False

            found_possibility = self.eliminate_possibilities()

            found_unique = self.write_uniques()

            found_exclusive = False
            for set_length in range(2,9): #2-8
                new_exclusive = self.eliminate_exclusives(set_length)
                found_exclusive = found_exclusive or new_exclusive


            found_new_value = self.write_definite()

            # determine whether we made progress
            go_on = found_exclusive or found_new_value or found_possibility or found_unique


        if self.sudoku.is_solved() and self.sudoku.is_correct():
            self.print_result()
        else:
            self.print_error()


    def get_groups(self):
        """
        Utility function to avoid code duplication
        :return: All Rows, Cols and Boxes in an array
        """
        return self.sudoku.get_rows() + self.sudoku.get_cols() + self.sudoku.get_boxes()


    def eliminate_possibilities(self):
        """
        Eliminates possible values for all groups based on the already solved fields in that group
        :return:
        """

        removed_possibility = False
        def remove_possibility(group, number):
            """
            Utility function to remove a possibility from all fields in a group
            :param group:
            :param number:
            :return:
            """
            for field in group:
                if not field.solved and number in field.possible:
                    field.possible.remove(number)
                    #if len(field.possible) == 0: pdb.set_trace()
                    global removed_possibility
                    removed_possibility = True

        groups = self.get_groups()

        for group in groups:
            for field in group:
                if field.solved:
                    # print("Removing", field.value, "from group", group)
                    remove_possibility(group, field.value)

        return removed_possibility

    def eliminate_exclusives(self, set_length=2):
        """
        Eliminates tuples as possibility in a group if they are "held" by 2 other fields in the group.
        :param set_length: Length of the set we want to search for
        :return: True if the function has found and deleted a tuple
        """

        found_tuple = False
        def remove_from_group(group, possibilities, fields_to_keep):
            """
            Utility function to remove a set of possibilities from one group
            :param group: group whose fields we want to modify
            :param possibilities: possibilities we want to remove from the fields
            :param fields_to_keep: fields we don't want to change because they are the originals
            :return:
            """

            # find out which fields we need to change
            fields_to_change = [field for field in group if not field.solved and field not in fields_to_keep]

             # remove possibilities from fields
            for field in fields_to_change:
                for number in possibilities:
                    if number in field.possible:
                        field.possible.remove(number)
                        global found_tuple
                        found_tuple = True

        groups = self.get_groups()

        for group in groups:
            # find all fields that can have useful possibilities
            relevant_fields = [field for field in group if not field.solved and len(field.possible) == set_length]

            for field in relevant_fields:
                # found a tuple possibility
                possibles = field.possible[:]
                # check for other field with the same (set_length) possibilities
                matching_fields = list(filter(lambda fld: fld.possible == possibles, group))

                if len(matching_fields) == set_length:
                    remove_from_group(group, possibles, matching_fields)
                    #print("Found fields with tuples:", len(matching_fields))

        return found_tuple

    def write_uniques(self):
        """
        if a value only appears once in a group as possibility, write it
        :return:
        """
        #return False
        wrote_unique = False

        for group in self.get_groups():

            possible_numbers = list(range(1,10))
            for field in group:
                if field.solved:
                    possible_numbers.remove(field.value)

            for number in possible_numbers:
                # all fields that have this number as possibility
                fields = list(filter(lambda fld: not fld.solved and number in fld.possible, group))

                # if there is only one, fill it!
                if len(fields) == 1:
                    fields[0].set_value(number)
                    self.eliminate_possibilities()
                    self.eliminate_exclusives()
                    wrote_unique = True

        return wrote_unique

    def write_definite(self):
        """
        Write a value if it's the only possibility in the field
        :return:
        """
        found_definite = False
        for field in self.sudoku.fields:

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

    def print_error(self):
        print("Couldn't solve sudoku!")
        print("Correct so far:", self.sudoku.is_correct())
        print(str(self.sudoku))