class Results:

	def __init__(self):
		self.columns = ""
		self.rows = []
		self.numrows = 0	
		self.numcols = 0

	def addrow(self, row):
		self.rows.append(row)	
		self.numrows += 1	

	def setnumcolumns(self, num):
		self.numcols = num

	def setcolumns(self, columns):
		self.columns = columns

	def getcolumns(self):
		return self.columns

	def getnumrows(self):
		return self.numrows

	def getrow(self, num):
		return self.rows[num]
