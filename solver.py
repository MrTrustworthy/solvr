__author__ = 'MrTrustworthy'



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

            found_exclusive = False

            for tuple_length in range(2,6): #2-5
                new_exclusive = self.eliminate_exclusives(tuple_length)
                found_exclusive = found_exclusive or new_exclusive

            found_new_value = self.write_definite()

            # determine whether we made progress
            go_on = found_exclusive or found_new_value or found_possibility
            #print(found_exclusive, found_new_value, found_possibility)

        self.print_result()


    def get_groups(self):
        """
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


    def write_definite(self):
        """
        Write a value if it's the only possibility in the field
        :return:
        """
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
