import curses
import curses.panel
import time
import sys

def login():
	screen = curses.initscr()
	screen.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	dims = screen.getmaxyx()
	screen.nodelay(0)
	screen.clear()

	selection = -1
	option = 0
	optionData = 0
	userName = ""
	pword = ""
	dataBase = ""

	

	while selection < 0:
		graphics = [0]*4
		graphics[option] = curses.A_REVERSE
		screen.addstr((dims[0]/2)-1, dims[1]/3, 'Username', graphics[0])
		screen.addstr((dims[0]/2), dims[1]/3, 'Password', graphics[1])
		screen.addstr((dims[0]/2)+1, dims[1]/3, 'Database', graphics[2])
		screen.addstr((dims[0]/2)+2, dims[1]/3, 'Login', graphics[3])
		screen.refresh()
		action = screen.getch()
		if action == curses.KEY_UP:
			option = (option - 1) % 4
		elif action == curses.KEY_DOWN:
			option = (option + 1) % 4
		elif action == ord('\n'):
			selection = option

		if selection < 0:
			selection = -1

		elif selection == 0:
			screen.move(dims[0]/2-1, dims[1]/3+10)
			curses.curs_set(1)
			curses.echo(1)
			curses.nocbreak()
			userName = screen.getstr()
			selection = -1
			curses.curs_set(0)
			curses.cbreak()
			curses.echo(0)

		elif selection == 1:
			curses.curs_set(1)
			curses.nocbreak()
			screen.move(dims[0]/2, dims[1]/3+10)
			pword = screen.getstr()
			selection = -1
			curses.curs_set(0)
			curses.cbreak()

		elif selection == 2:
			dataList = ["MySQL", "GRSQL"]
			while 1:
				screen.addstr((dims[0]/2)+1, dims[1]/3+10, dataList[optionData])
				action = screen.getch()
				if action == curses.KEY_UP or action == curses.KEY_DOWN:
					optionData = (optionData + 1) % 2
				elif action == ord('\n'):
					dataBase = dataList[optionData]
					break
			selection = -1

		elif selection == 3:
			if checkInput(userName, pword, dataBase) != 0:
				screen.clear()
				curses.echo(1)
				curses.endwin()
				connectDatabase(userName, pword, dataBase)
				return
			selection = -1

def checkInput(userName, pword, dataBase):
	if userName == "" or pword == "" or dataBase == "":
		return 0

def connectDatabase(userName, pword, dataBase):
	print(userName, pword, dataBase)

login()