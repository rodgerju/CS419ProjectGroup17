from AbstractDatabase import AbstractDatabase

class PostgreSQL(AbstractDatabase):


	def connect(self, Credentials):
		return False

	def query(self, db, query):
		return "PostgreSQL: I am a query response!" 