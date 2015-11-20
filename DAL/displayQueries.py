import curses
import curses.panel
import time
import sys
import DBFactory
from Credentials import Credentials

class displayQueries(object):

	def querySession(self, screen, credentials, database):
		dims = screen.getmaxyx()
		num = 1
		query = ""
		screen.clear()

		data = ["Table 1", "Table 2", "Table 3", "Table 4", "Table 5", "Table 6", "Table 7", "Table 8", "Table 9", "Table 10"]
		twin = self.tableScreen(screen, data)		
		qwin = self.queryScreen(screen)
		dwin = self.displayScreen(screen)

		paneld = curses.panel.new_panel(dwin)
		panelq = curses.panel.new_panel(qwin)
		panelt = curses.panel.new_panel(twin)

		while query != "/quit":		

			curses.panel.update_panels()
			curses.doupdate()	
			screen.move((dims[0]+1)-(dims[0]//4), 3)
			curses.curs_set(1)
			curses.echo(1)
			query = screen.getstr()
			screen.clear()
			if query == "/quit":
				continue
			if query != "": 
				dwin.clear()	
				dwin.addstr(1, 1, "(Select \"Enter\" to expand window)", curses.A_UNDERLINE)
				result = database.query(credentials, query)
				if(result.getrowcount() > 0):
					self.printtable(result,dwin)
				else:
					dwin.addstr(2, 1, str(result.getrowsaffected()) + " row(s) affected.")				
			else:
				if num == 1:
					num+=1
					paneld.top()
				else:
					num=1
					panelt.top()
				continue

	def tableScreen(self, screen, newData):
		dims = screen.getmaxyx()
		begin = dims[1]-(dims[1]//4)
		tableWin = curses.newwin(dims[0], (dims[1]//4), 0, begin)
		tableWin.box()
		tableWin.addstr(1, 2, "DB-Tables:", curses.A_UNDERLINE)
		if newData:
			for i in range(len(newData)):
				tableWin.addstr(i+3, 2, newData[i])
		return tableWin

	def queryScreen(self, screen):
		dims = screen.getmaxyx()
		begin = dims[0]-(dims[0]//4)		
		queryWin = curses.newwin((dims[0]//4), dims[1]-(dims[1]//4)+1, begin, 0)
		queryWin.box()
		queryWin.addstr(1, 1, "$")
		queryWin.move(1,3)
		return queryWin

	def displayScreen(self, screen):
		dims = screen.getmaxyx()
		disWin = curses.newwin((dims[0]-(dims[0]//4)), dims[1], 0, 0)
		disWin.box()
		disWin.addstr(1, 1, "Display Queries:", curses.A_UNDERLINE)

		return disWin	

	def printtable(self, result, window):
		cols= {"id": 3, "name": 10, "firstName": 10, "lastName": 10, "email": 20, "date": 12, "phone": 14}

		dims = window.getmaxyx()
		window.box()
		table = result.gettable()
		rc = 2
		cc = 0
		colsize = []
		s = [] 
		defaultSize = 15

		for row in table:
			
			for column in row:
				if rc < 3:
					if cc == 0:
						if str(column) in cols:
							colsize.append(cols[str(column)])
						else:
							colsize.append(defaultSize)		
						window.addstr(rc, 2, str(column))	
						s.append(colsize[cc]+3)
					else:
						if str(column) in cols:
							colsize.append(colsize[cc-1] + cols[str(column)])
						else:
							colsize.append(colsize[cc-1] + defaultSize)
						window.addstr(rc, s[cc-1], str(column))
						s.append(colsize[cc]+1)
				else:
					if cc == 0:
						window.addstr(rc, 2, str(column))
					else:
  		 				window.addstr(rc, s[cc-1], str(column)) 	
				cc+=1
  		 	rc+=1
  		 	cc=0
