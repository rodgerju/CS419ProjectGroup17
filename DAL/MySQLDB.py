from AbstractDatabase import AbstractDatabase
import Credentials
import MySQLdb
import MySQLdb.cursors as cursors

class MySQLDB(AbstractDatabase):


	def connect(self, Credentials):		
			db = MySQLdb.connect(host=Credentials.host, 
				user = Credentials.username, 
				passwd= Credentials.password, 
				db = Credentials.dbname, cursorclass=cursors.SSCursor)
			return db

	def query(self, conn, query):
		cursor = conn.cursor()
		cursor.execute(query)
		for row in cursor:
			print (row)