import curses
import curses.panel
import time
import sys
import DBFactory
from Credentials import Credentials

class displayQueries(object):

	def querySession(self, screen, credentials, database):
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
			if query != "": 
				result = database.query(credentials, query)
				num = result.getnumrows() - 1
				rc = 0				
				while num > 0:
					screen.addstr(rc, 0, str(result.getrow(num)))
					num -= 1				
			 		rc += 1