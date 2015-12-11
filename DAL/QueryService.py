import curses
import curses.panel
import curses.textpad
import time
import sys
import DBFactory
from Credentials import Credentials

class QueryService(object):

	def querySession(self, screen, credentials, database):
		dims = screen.getmaxyx()
		num = 1
		query = ""
		screen.clear()

		twin = self.tableScreen(screen)		
		qwin = self.queryScreen(screen)
		dwin = self.displayScreen(screen)
		self.printnames(twin, credentials, database)

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
			if query == "/quit":
				continue
			if query != "":
				if query[len(query) - 1] == ';': 
					screen.clear()					
					dwin.clear()	
					dwin.addstr(1, 1, "(Select \"Enter\" to expand window)", curses.A_UNDERLINE)
					try:
						query = query.lower()						
						curses.panel.update_panels()
						curses.doupdate()
						result = database.query(credentials, query)
						if("create" in query):
							twin.clear()
							twin.box()
							dwin.box()
							self.printnames(twin, credentials, database)
						elif("drop" in query):
							twin.clear()
							twin.box()
							dwin.box()
							self.printnames(twin, credentials, database)
						if(result.getrowcount() > 0):
							self.printtable(result,dwin,0)
						else:
							dwin.addstr(2, 1, str(result.getrowsaffected()) + " row(s) affected.")				
					except Exception as ex:
						dwin.addstr(2, 1, str(ex))
					query = ""
					qwin.addstr(queryLine + 1, 1, " ")
					queryLine = 0
					qwin.addstr(queryLine + 1, 1, "$")
					curses.panel.update_panels()
					curses.doupdate()	
					screen.move((dims[0]+1)-(dims[0]//4), 3)
					curses.curs_set(1)
					curses.echo(1)
				else:
					while query[len(query) - 1] == ' ':
						query = query[:-1]
					query += " "										
					qwin.addstr(queryLine + 1, 1, " ")					
					queryLine += 1
					if queryLine > (dims[0]/4 - 3):
						screen.clear()
						queryLine = 0					
					qwin.addstr(queryLine + 1, 1, "$")
					curses.panel.update_panels()						
					screen.move((dims[0]+1)-(dims[0]//4) + queryLine, 3)

			else:
				screen.clear()
				if result != "":					
					dwin.clear()
					dwin.addstr(1, 1, "(Press \"Tab\" to query)", curses.A_UNDERLINE)
					self.printtable(result,dwin,0)
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

	def printnames(self, win, credentials, database):
		i = 0		
		win.addstr(1, 2, "DB-Tables:", curses.A_UNDERLINE)
		if credentials.dbtype == "MySql":
			tblquery = "select table_name from information_schema.tables where table_schema = \"" + credentials.dbname + "\";"
			newData = database.query(credentials, tblquery)
			names = newData.getnames()
			if names:
				for row in names:
					tbl =  str(i+1) + "." + " " + str(row).strip("',()") 
					win.addstr(i+3, 2, tbl)
					i+=1
		else:
			tblquery = "select table_name, table_type from information_schema.tables where table_schema =\'public\';"
			newData = database.query(credentials, tblquery)
			names = newData.getnames()
			if names:
				for row in names:
					for col in row[:1]:
						tbl =  str(i+1) + "." + " " + str(col).strip("',()") 
						win.addstr(i+3, 2, tbl)
					i+=1	

	def tableScreen(self, screen):
		dims = screen.getmaxyx()
		i = 0
		begin = dims[1]-(dims[1]//4)
		tableWin = curses.newwin((dims[0]-(dims[0]//4)), (dims[1]//4), 0, begin)
		tableWin.box()
		return tableWin

	def pagination(self, screen, dwin, result):
		displayRows = 2		
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
				self.printtable(result,dwin, pageNum)
				selection = -1
			elif selection == 0:
				pageNum += 1
				if pageNum * displayRows >= result.getrowcount():
					pageNum -= 1				
				dwin.clear()	
				dwin.addstr(1, 1, "(Press \"Tab\" to query)", curses.A_UNDERLINE)
				self.printtable(result,dwin, pageNum)
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
		queryWin = curses.newwin((dims[0]//4), dims[1], begin, 0)
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
			
	def getColSizes(self, win, obj):
		dims = win.getmaxyx()		
		rownum = 1
		aveCol = 0
		setMax = 0
		total = 0
		maxSize = 0
		sizes = []
		numcols = 0
		for row in obj:
			i = 0
			for col in row:
				total += len(str(col))				
				if rownum == 1:
					sizes.append(len(str(col)))
				if rownum > 1:
					if sizes[i] < len(str(col)):
						sizes[i] = len(str(col))
				i += 1
			numcols = i
			rownum += 1			
			if (total+(numcols+1)) > dims[1]:
				setMax = 1			
			total = 0
		if setMax == 1:
			aveCol = ((dims[1]-(numcols+1))/numcols)
		return sizes, setMax, aveCol

	def printtable(self, result, window, startRow):
		dims = window.getmaxyx()
		window.box()
		header = 0
		table = 0
		header = list(result.getheader())
		table = list(result.gettable())
		rc = 2
		cc = 0
		count = 3 
		colsize = []
		displayRows = 2
		if result.getrowcount() < (startRow * displayRows) + displayRows:
			printRange = result.getrowcount()
		else:
			printRange = (startRow * displayRows) + displayRows
		for i in range((startRow * displayRows), printRange):
			header.append(list(table[i]))
		maxWidth, setCol, colAve = self.getColSizes(window, header)
		for row in header:
			for column in row:
				if setCol == 1:
					if rc < 3:
						if cc == 0:
							if len(str(column)) > colAve:
								tmp = str(column)
								abr = tmp[:colAve-3] + "..."	
								window.addstr(rc*2, 2, abr)
							else:
								window.addstr(rc*2, 2, str(column))	
							colsize.append(colAve+2)
							curses.textpad.rectangle(window, count, 1, count+2, colsize[cc])
						else:
							colsize.append(colsize[cc-1] + colAve + 1)
							if len(str(column)) > colAve:
								tmp = str(column)
								abr = tmp[:colAve-3] + "..."	
								window.addstr(rc*2, colsize[cc-1]+1, abr)
							else:
								window.addstr(rc*2, colsize[cc-1]+1, str(column))
							curses.textpad.rectangle(window, count, colsize[cc-1], count+2, colsize[cc])
					else:
						if cc == 0:
							if len(str(column)) > colAve:
								tmp = str(column)
								abr = tmp[:colAve-3] + "..."	
								window.addstr(rc*2, 2, abr)
							else:
								window.addstr(rc*2, 2, str(column))
							curses.textpad.rectangle(window, count, 1, count+2, colsize[cc])
						else:
							if len(str(column)) > colAve:
								tmp = str(column)
								abr = tmp[:colAve-3] + "..."
								window.addstr(rc*2, colsize[cc-1]+1, abr)
							else:
	  		 					window.addstr(rc*2, colsize[cc-1]+1, str(column)) 	
							curses.textpad.rectangle(window, count, colsize[cc-1], count+2, colsize[cc])
				else:
					if rc < 3:
						if cc == 0:
							window.addstr(rc*2, 2, str(column))	
							colsize.append(maxWidth[cc]+2)
							curses.textpad.rectangle(window, count, 1, count+2, colsize[cc])
						else:
							colsize.append(colsize[cc-1] + maxWidth[cc] + 1)
							window.addstr(rc*2, colsize[cc-1]+1, str(column))
							curses.textpad.rectangle(window, count, colsize[cc-1], count+2, colsize[cc])
					else:
						if cc == 0:
							window.addstr(rc*2, 2, str(column))
							curses.textpad.rectangle(window, count, 1, count+2, colsize[cc])
						else:
							window.addstr(rc*2, colsize[cc-1]+1, str(column)) 	
							curses.textpad.rectangle(window, count, colsize[cc-1], count+2, colsize[cc])
				cc+=1
  		 	rc+=1
  		 	cc=0
			count+=2
