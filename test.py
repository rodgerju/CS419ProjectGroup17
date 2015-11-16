import MySQLdb
import MySQLdb.cursors as cursors

conn = MySQLdb.connect("localhost","cs","password","testing")
cursor = conn.cursor()
cursor.execute("Select * from users")
for row in cursor:
	print row

