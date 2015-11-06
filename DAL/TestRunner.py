import DBFactory
from Credentials import Credentials

if __name__ == '__main__':

	username = "cs419user"
	password = "password"
	hostname = "db4free.net"
	dbname = "cs419mysqldb"
	dbtype = "MySql"
	# query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA'.'COLUMNS' WHERE 'TABLE_SCHEMA'= 'cs419mysqldb' AND 'TABLE_NAME' = 'users'"
	query = "SELECT * FROM users"
	#query = "INSERT INTO users(id, email,password,firstName, lastName) VALUES(null, 'test@test.com','Encrypted Password','John','Doe')"

	userCreds = Credentials(username, password, hostname, dbname)

	
	dbFactory = DBFactory.DBFactory()
	database = dbFactory.resolve(dbtype)
	dbconn = database.connect(userCreds)
	qr = database.query(dbconn, query)

	for row in qr:
		print (row)

	#print "Connection return %r" % dbconn
	#print "Query response %s \n" % queryresponse
	print "Username: %s " % userCreds.username
	print "Password: %s " % userCreds.password
	print "Host: %s " % userCreds.host
	print "Dbname: %s " % userCreds.dbname

