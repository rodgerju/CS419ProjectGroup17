from AbstractDatabase import AbstractDatabase
from Results import Results
import Credentials
import re
import psycopg2
import sys

class PostgreSQL(AbstractDatabase):

	def connect(self, Credentials):
		try:
			db = None
			db = psycopg2.connect(database=Credentials.dbname,
			user = Credentials.username, 
			password= Credentials.password, 
			host=Credentials.host, 
			port = Credentials.port)
			return True
		except Exception as ex:
			raise ex	
		finally:
			if db:
				db.close()

	def query(self, Credentials, query):
		try:
			db = None
			db = psycopg2.connect(database=Credentials.dbname,
			user = Credentials.username, 
			password= Credentials.password, 
			host=Credentials.host, 
			port = Credentials.port)
			cursor = db.cursor()
			cursor.execute(query)
			
			command = self.parsecommand(query)
			result = Results()
			if (command != "select"):
				self.commitchanges(db)	
				result.rowsaffected(cursor)
			elif (command == "create"):
				result.populatenames(cursor)
			elif ("select table_name, table_type from information_schema.tables" in query):
				result.populatenames(cursor)
			else:
				result.populatetable(cursor)				
			return result	
		except Exception as ex:
			raise ex	
		finally:
			if db:
				db.close()

	def commitchanges(self, conn):
		try:
			conn.commit()				
		except Exception as ex:
			conn.rollback()
			raise ex
			
	def parsecommand(self, query):		
			return (query.split(' ', 1)[0]).lower()
