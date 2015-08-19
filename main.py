import time

class Field:

	def __init__(self, x, y, value = None):
		self.x = x
		self.y = y
		self.possible = list(range(1,10))
		self.solved = False
		self.value = 0
		if value: self.setValue(value)

	def setValue(self, value):
		if self.value:
			raise ValueError("Already has a Value:", self)

		self.value = value

		if self.value != 0:
			self.possible = None
			self.solved = True

	def __str__(self):
		return str(self.value) + " "
		#return "[" + str(self.value) + "::" + str(self.possible) + "]"
		#return "[(" + str(self.x) + ":" + str(self.y) + ")->" + str(self.value) + "]"

	def __repr__(self):
		return self.__str__()

class Sudoku:

	# defines the filer-functions to determine the boxes
	# box order is left->right then top->bottom
	box_definition = [
		lambda fld: fld.x < 3 and fld.x >= 0 and fld.y < 3 and fld.y >= 0,
		lambda fld: fld.x < 6 and fld.x >= 3 and fld.y < 3 and fld.y >= 0,
		lambda fld: fld.x < 9 and fld.x >= 6 and fld.y < 3 and fld.y >= 0,
		lambda fld: fld.x < 3 and fld.x >= 0 and fld.y < 6 and fld.y >= 3,
		lambda fld: fld.x < 6 and fld.x >= 3 and fld.y < 6 and fld.y >= 3,
		lambda fld: fld.x < 9 and fld.x >= 6 and fld.y < 6 and fld.y >= 3,
		lambda fld: fld.x < 3 and fld.x >= 0 and fld.y < 9 and fld.y >= 6,
		lambda fld: fld.x < 6 and fld.x >= 3 and fld.y < 9 and fld.y >= 6,
		lambda fld: fld.x < 9 and fld.x >= 6 and fld.y < 9 and fld.y >= 6
	]





	def __init__(self, input_str):
		self.fields = []
		self.raw_data = [int(val) for val in input_str]
		if len(self.raw_data) != 81: raise ValueError("Sudoku raw data doesnt have ")
		self.parse_raw(self.raw_data)

		givens = list(filter(lambda x: x != 0, self.raw_data))

		print("Sudoku has", str(len(givens)), "Givens already" )


	def parse_raw(self, raw):
		for col_idx in range(9):
			for row_idx in range(9):

				val = raw[col_idx*9 + row_idx]
				fld = Field(row_idx, col_idx, val)

				self.fields.append(fld)


	def sort_wrapper(function):
		def function_wrapper(*args, **kwargs):
			return sorted(function(*args, **kwargs), key = lambda fld: fld.x + fld.y*9)
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
		for field in self.fields:
			if not field.value:
				return False
		return True

	def is_correct(self):
		groups = self.get_rows() + self.get_cols() + self.get_boxes()
		for group in groups:
			group_values = [field.value for field in group]
			for number in range(1,10):
				if group_values.count(number) != 1:
					return False
		return True


	def __repr__(self):
		return self.__str__()

	def __str__(self):
		string_representation = ""
		for row_idx in range(9):
			string_representation += "Row " + str(row_idx) + ": "
			for field in self.get_row(row_idx):
				string_representation += str(field)
			string_representation += "\n"
		return string_representation


class Solver:

	def __init__(self, sudoku):
		self.sudoku = sudoku


	def solve(self):
		print("Solving Sudoku now!")
		#print("Sudoku is:\n" + str(self.sudoku))

		found_new_value = True
		while found_new_value and not self.sudoku.is_solved():
			#found_new_value = False
			self.eliminate_possibilities()
			found_new_value = self.write_definite()

		print("Finished solving sudoku!")
		print("Solved:", self.sudoku.is_solved())
		print("Correct:", self.sudoku.is_correct())
		#print("Result:\n" + str(self.sudoku))
		print(20*"*")

	def eliminate_possibilities(self):

		def remove_possibility(group, number):
			for field in group:
				if not field.solved and number in field.possible:
					field.possible.remove(number)

		groups = self.sudoku.get_rows() + self.sudoku.get_cols() + self.sudoku.get_boxes()

		for group in groups:
			for field in group:
				if field.solved:
					#print("Removing", field.value, "from group", group)
					remove_possibility(group, field.value)



	def write_definite(self):
		found_definite = False
		for field in self.sudoku.fields:
			#if not field.solved: print(len(field.possible))
			if not field.solved and len(field.possible) <= 1:
				#print("Determined single value for", field.x, ":", field.y, "to be", field.possible[0])
				field.setValue(field.possible[0])
				found_definite = True
		return found_definite



if __name__ == "__main__":

	start = time.time()

	sudokus = [
		"379502000500089603006004925490350000068090537005820091600275300057003086920600750",
		"165900040000458062480070503026580400501004086008209701853010900070305018600042370",
		"306800000500600008000070036000093800428005300060020010000904003030006150059000004",
		"002000005008001070000003010000020400690080000700040900000600003000400809867500000"
	]

	for sudoku in sudokus:
		solver = Solver(Sudoku(sudoku))
		solver.solve()

	end = time.time()

	print("It took", end-start, "ms to run", len(sudokus), "Sudokus")