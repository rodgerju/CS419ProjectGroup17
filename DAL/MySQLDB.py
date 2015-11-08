from AbstractDatabase import AbstractDatabase
from Results import Results
import Credentials
import MySQLdb
import MySQLdb.cursors as cursors

class MySQLDB(AbstractDatabase):

	def connect(self, Credentials):		
		try:
			db = MySQLdb.connect(host=Credentials.host, 
			user = Credentials.username, 
			passwd= Credentials.password, 
			db = Credentials.dbname, cursorclass=cursors.SSCursor)
			db.close()
			return True
		except:
			return False		

	def query(self, Credentials, query):
		conn = MySQLdb.connect(host=Credentials.host, 
			user = Credentials.username, 
			passwd= Credentials.password, 
			db = Credentials.dbname, cursorclass=cursors.SSCursor)
		cursor = conn.cursor()
		cursor.execute(query)
		
		command = (query.split(' ', 1)[0]).lower()
		result = Results()
		if (command == "insert") or (command == "delete"):
			try:
				conn.commit()				
			except:
				conn.rollback()
		else:
			for row in cursor:
				result.addrow(row)
		cursor.close()
		return result

