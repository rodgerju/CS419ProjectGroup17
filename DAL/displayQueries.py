import curses
import curses.panel
import time
import sys
import DBFactory
from Credentials import Credentials

def connectDatabase(screen, userName, pword, dataBase, hostName, dbName):
	userCreds = Credentials(userName, pword, hostName, dbName)
	dbFactory = DBFactory.DBFactory()
	db = dbFactory.resolve(dataBase)	
	dbconn = db.connect(userCreds)
	dims = screen.getmaxyx()
	query = ""
	screen.clear()
	while query != "/quit":			
		screen.addstr(dims[0]-1, 0, '$')
		screen.move(dims[0]-1, 2)		
		curses.curs_set(1)
		curses.echo(1)
		query = screen.getstr()
		screen.clear()
		if query == "/quit":
			continue
		queryresponse = db.query(dbconn, query)
		rc = 0		
		for row in queryresponse:
			cc = 0			
			for col in row: 				
				screen.addstr(rc, cc*10, str(col))
				cc += 1
			rc += 1		
		#for row in range(0, len(queryresponse)+1):
		#	for col in range(0, len(row)+1):
		#		screen.addstr(row, col*10, queryresponse[row][col]) 
	return







































