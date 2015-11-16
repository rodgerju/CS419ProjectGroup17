class Results:

	def __init__(self):		
		self.table = []
		self.numrows = 0		
		self.affected = 0	

	def populatetable(self, data):	
		self.table.append([i[0] for i in data.description])
		count = 0
		for row in data:
			self.table.append(row)
			count += 1		
		self.numrows = count	

	def rowsaffected(self, data):
		self.rowsaffected = data.rowcount

	def gettable(self):
		return self.table	

	def getrowcount(self):
		return self.numrows

	def getrowsaffected(self):
		return self.rowsaffected
	

