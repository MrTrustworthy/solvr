
class Field:

	x = None
	y = None
	value = None
	possible = range(9)

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def setValue(self, value):
		pass

class Sudoku:

	raw_data = None
	fields = []

	def __init__(self, raw):
		self.raw_data = raw
		self.parse_raw(self.raw_data)
		print(self.fields)

	def parse_raw(self, raw):
		for row_idx in range(9):
			for col_idx in range(9):
				fld = Field(row_idx, col_idx)
				val = raw[row_idx + col_idx*9]
				fld.setValue(val)
				self.fields.append(fld)


	def get_row(self, index):
		pass

	def get_col(self, index):
		pass

if __name__ == "__main__":
	raw = [
		1, None, None, None, None, None, None, None, None,
		2, 1, None, None, None, None, None, None, None,
		None, 2, 1, None, None, None, None, None, None,
		None, None, 2, 1, None, None, None, None, None,
		None, None, None, 2, 1, None, None, None, None,
		None, None, None, None, 2, 1, None, None, None,
		None, None, None, None, None, 2, 1, None, None,
		None, None, None, None, None, None, 2, 1, None,
		None, None, None, None, None, None, None, 2, 1
	]
	a = Sudoku(raw)

