import curses
import curses.panel
import curses.textpad
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

		curses.panel.update_panels()
		curses.doupdate()	
		screen.move((dims[0]+1)-(dims[0]//4), 3)
		curses.curs_set(1)
		curses.echo(1)
		result = ""
		queryLine = 0
		while query != "/quit":		
			
			query += screen.getstr()
			screen.clear()
			if query == "/quit":
				continue
			if query != "":
				if query[len(query) - 1] == ';': 
					dwin.clear()	
					dwin.addstr(1, 1, "(Select \"Enter\" to expand window)", curses.A_UNDERLINE)
					try:
						curses.panel.update_panels()
						curses.doupdate()					
						result = database.query(credentials, query)
						if(result.getrowcount() > 0):
							self.printtable2(result,dwin,0)
						else:
							dwin.addstr(2, 1, str(result.getrowsaffected()) + " row(s) affected.")				
					except Exception as ex:
						dwin.addstr(2, 1, str(ex))
					query = ""
					curses.panel.update_panels()
					curses.doupdate()	
					screen.move((dims[0]+1)-(dims[0]//4), 3)
					curses.curs_set(1)
					curses.echo(1)
					queryLine = 0
				else:
					if query[len(query) - 1] != ' ':
						query += ' '					
					queryLine += 1					
					curses.panel.update_panels()
					curses.doupdate()	
					screen.move((dims[0]+1)-(dims[0]//4) + queryLine, 3)
					curses.curs_set(1)
					curses.echo(1)

			else:

				if result != "":
					dwin.clear()
					dwin.addstr(1, 1, "(Press \"Tab\" to query)", curses.A_UNDERLINE)
					self.printtable2(result,dwin,0)
					curses.panel.update_panels()
					curses.doupdate()
					paneld.top()
					curses.panel.update_panels()
					curses.doupdate()	
					self.pagination(screen, dwin, result)
				panelt.top()
				query = ""
				curses.panel.update_panels()
				curses.doupdate()	
				screen.move((dims[0]+1)-(dims[0]//4), 3)
				curses.curs_set(1)
				curses.echo(1)

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

	def pagination(self, screen, dwin, result):
		dims = screen.getmaxyx()	
		selection = -1		
		option = 0
		pageNum = 0
		curses.noecho()
		curses.curs_set(0)
		screen.keypad(1)
		while selection < 0:	
			self.printOptions(screen, dwin, option)
			curses.panel.update_panels()
			curses.doupdate()
			curses.curs_set(0)
			curses.echo(0)
			action = screen.getch()
			if action == curses.KEY_RIGHT:
				option = (option - 1) % 2
			elif action == curses.KEY_LEFT:
				option = (option + 1) % 2
			elif action == ord('\t'):
				return
			elif action == ord('\n'):
				selection = option
			
			if selection == 1:
				pageNum -= 1
				if pageNum < 0:
					pageNum = 0
				dwin.clear()	
				dwin.addstr(1, 1, "(Press \"Tab\" to query)", curses.A_UNDERLINE)
				self.printtable2(result,dwin, pageNum)
				selection = -1
			elif selection == 0:
				pageNum += 1
				if pageNum * 3 >= result.getrowcount():
					pageNum -= 1				
				dwin.clear()	
				dwin.addstr(1, 1, "(Press \"Tab\" to query)", curses.A_UNDERLINE)
				self.printtable2(result,dwin, pageNum)
				selection = -1

	def printOptions(self, screen, paneld, option):
		dims = screen.getmaxyx()		
		graphics = [0] * 2
		graphics[option] = curses.A_REVERSE
		pageDwn = "PgDwn"
		pageUp = "PgUp"
		paneld.addstr(dims[0] -(dims[0]//4) - 2, dims[1] - (len(pageUp) + len(pageDwn) + 2), pageDwn, graphics[0])
		paneld.addstr(dims[0] -(dims[0]//4) - 2, dims[1] - (len(pageUp) + 1), pageUp, graphics[1])
		screen.refresh()
	
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

	def printtable2(self, result, win, startRow):
		dims = win.getmaxyx()
		win.box()
		displayRows = 3
		header = 0
		table = 0
		header = list(result.getheader())
		table = list(result.gettable())	
		rc = 2
		cc = 0
		count = 1
		colsize = []
		defaultSize = 15
		if result.getrowcount() < (startRow * displayRows) + displayRows:
			printRange = result.getrowcount()
		else:
			printRange = (startRow * displayRows) + displayRows
		for i in range((startRow * displayRows), printRange):
			header.append(list(table[i]))
		for row in header:
			for column in row:			
				if rc < 3:
					if cc == 0:
						colsize.append(defaultSize+1)
						if len(str(column)) > 14:
							tmp = str(column)
							abr = tmp[:11] + "..."
							win.addstr(rc*2+1, 2, abr)
						else:
							win.addstr(rc*2+1, 2, str(column))
						win.addstr(rc*2, 1, "+-------------+")
						win.addstr(rc*2+1, 1, "|")
						#win.addstr(rc*2+1, 2, str(column))
						win.addstr(rc*2+1, colsize[cc]-1, "|")
						win.addstr(rc*2+2, colsize[cc]-1, "+-------------+")
					else:
						colsize.append(colsize[cc-1]+defaultSize)
						win.addstr(rc*2, colsize[cc-1], "--------------+")
						if len(str(column)) > 14:
							tmp = str(column)
							abr = tmp[:11] + "..."
							win.addstr(rc*2+1, colsize[cc-1], abr)
						else:
							win.addstr(rc*2+1, colsize[cc-1], str(column))	
						win.addstr(rc*2+1, colsize[cc]-1, "|")
						win.addstr(rc*2+2, colsize[cc-1], "--------------+")
				else:
					if cc == 0:
						win.addstr(rc*2, 1, "+-------------+")
						win.addstr(rc*2+1, 1, "|")
						if len(str(column)) > 14:
							tmp = str(column)
							abr = tmp[:11] + "..."
							win.addstr(rc*2+1, 2, abr)
						else:
							win.addstr(rc*2+1, 2, str(column))
						win.addstr(rc*2+1, colsize[cc]-1, "|")
						win.addstr(rc*2+2, 1, "+-------------+")
		
					else:
						win.addstr(rc*2, colsize[cc-1], "--------------+")
						if len(str(column)) > 14:
							tmp = str(column)
							abr = tmp[:11] + "..."
							win.addstr(rc*2+1, colsize[cc-1], abr)
						else:
							win.addstr(rc*2+1, colsize[cc-1], str(column))
						win.addstr(rc*2+1, colsize[cc]-1, "|")
						win.addstr(rc*2+2, colsize[cc-1], "--------------+")

							
				cc+=1
			rc+=1
			cc=0	
			count+=2
