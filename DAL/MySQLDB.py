from AbstractDatabase import AbstractDatabase
from Results import Results
import Credentials
import MySQLdb
import MySQLdb.cursors as cursors
import re

class MySQLDB(AbstractDatabase):

	def connect(self, Credentials):		
		try:
			db = MySQLdb.connect(host=Credentials.host, 
			port = Credentials.port,
			user = Credentials.username, 
			passwd= Credentials.password, 
			db = Credentials.dbname, cursorclass=cursors.SSCursor)
			db.close()
			return True
		except:
			return False		

	def query(self, credentials, query):
		try:
			conn = MySQLdb.connect(host=credentials.host, 
			port = credentials.port,
			user = credentials.username, 
			passwd= credentials.password, 
			db = credentials.dbname, cursorclass=cursors.SSCursor)
			cursor = conn.cursor()
			cursor.execute(query)
			
			command = self.parsecommand(query)
			result = Results()
			if (command != "select"):
				self.commitchanges(conn)	
				result.rowsaffected(cursor)
			elif (command == "create"):
				result.populatenames(cursor)
			elif ("select table_name from information_schema.tables" in query):
				result.populatenames(cursor)
			else:
				result.populatetable(cursor)			
			cursor.close()
			return result	
		except Exception as ex:
			raise ex	

	def commitchanges(self, conn):
		try:
			conn.commit()				
		except Exception as ex:
			conn.rollback()
			raise ex
			
	def parsecommand(self, query):		
			return (query.split(' ', 1)[0]).lower()
