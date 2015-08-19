__author__ = 'MrTrustworthy'


class Field:
    """
    Represents a Field inside the Sudoku. A Field has:
     Value [Integer]
     X and Y Positions [Integer]
     possibles [Array] containing the possible values for a field
     solved [Boolean] Indicating whether it already has a fixed value
    """

    def __init__(self, x, y, value=0):
        """
        Initializes Field object and sets value if one is given
        :param x: X-Position of the field, starting left
        :param y: Y-Position of the field, starting top
        :param value: Value (if given field) or 0 (if not given field)) for the field
        :return: self
        """
        self.x = x
        self.y = y
        self.possible = list(range(1, 10))
        self.solved = False
        self.value = 0
        if value:
            self.set_value(value)

    def set_value(self, value):
        """
        Sets the value of a field.
        :param value: Set the fields value to this. If Value is not 0, the field will be marked as solved
        :return:
        """
        if self.value:
            raise ValueError("Already has a Value:", self)

        self.value = value

        if self.value != 0:
            self.possible = None
            self.solved = True

    def __str__(self):
        """
        Returns string representation of self
        :return: String
        """
        return str(self.value) + " "
        # return "[" + str(self.value) + "::" + str(self.possible) + "]"
        #return "[(" + str(self.x) + ":" + str(self.y) + ")->" + str(self.value) + "]"

    def __repr__(self):
        """
        Calls self.__str__ to help with debugging
        :return:
        """
        return self.__str__()

