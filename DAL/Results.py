class Results:

	def __init__(self):
		self.rows = []
		self.numrows = 0	

	def addrow(self, row):
		self.rows.append(row)	
		self.numrows += 1	

	def getnumrows(self):
		return self.numrows

	def getrow(self, num):
		return self.rows[num]