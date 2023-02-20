# from screens import *
from constants import *
from networking import *
from boardgamestuff import *
# from tkinter_test import *
import tkinter
# from tkinter import font as tkfont  # python 3


dest_ip = None
dest_port = None
p_id = None
gs = None


def showFrame(frame_class, parent, controller):
	frame = frame_class(parent=parent, controller=controller)
	frame.grid(row=0, column=0, sticky='nsew')
	frame.tkraise()


class RoundInProgressScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		global p_id, gs
		tkinter.Frame.__init__(self, parent)

		# l1 = tkinter.Label(self, text="This is the round in progress screen where stuff happens.")
		# b1 = tkinter.Button(self, text="go to RoundOver frame", command = lambda: controller.show_frame(RoundOverScreen))

		# l1.grid(column=0, row=0)
		# b1.grid(column=0, row=1)


		buttons = []
		grid_fill = []
		grid = ['X'] * 16

		tkinter.Frame.__init__(self, parent)

		def button(button_press, number):
			#getGuessFromPlayer(number)
			#sendGameState(client_enter_ip, 6100, 99999, )
			buttons[button_press]["state"] = tkinter.DISABLED

		label_have_numbers = tkinter.Label(self, text="Your Set: ", width=30, height=2)
		if p_id != None:
			nums = ''.join([str(n)+', ' for n in gs.players[p_id].initial_numbers])[:-2]
			print('nums = ' + nums)
			label_have_numbers.configure(text='Your Set: ' + nums)
		label_have_numbers.grid(row=0, column=12)

		#creating the grid
		col = 2
		rowi = 1
		for i in range(16):
			n = grid[i]
			label_grid = tkinter.Label(self, text=".", width=2, height=1, state = tkinter.NORMAL)
			label_grid.grid(row = rowi, column = col)
			if rowi == col-1:
				label_grid["bg"] = "green"
			grid_fill.append(label_grid)
			col=col+1
			#color the grid

			if i == 3:
				rowi=rowi+1
				col = 2
			elif i == 7:
				rowi=rowi+1
				col = 2
			elif i == 11:
				rowi=rowi+1
				col = 2

		#creating the buttons
		for i in range(MAX_NUM):
			number_button = tkinter.Button(self, text=str(i+1), command=lambda button_press=i, number = i+1: button(button_press, number), width=1, height=1, state = tkinter.NORMAL)
			number_button.grid(row = i//10+6, column = i%10)
			buttons.append(number_button)

		#disable the button numbers they already have
		
		if p_id != None:
			for check_n in range(1, MAX_NUM+1):
				if check_n in gs.players[p_id].initial_numbers:
					buttons[int(check_n)-1]["state"]=tkinter.DISABLED

		button_restart = tkinter.Button(self, text="Restart", width=5, height=2, command=lambda: showFrame(MainMenuScreen, parent, controller))

		button_restart.grid(row = 8, column = 9)

		label_scores = tkinter.Label(self, text="Scores:", width=6, height=2)
		label_scores.grid(row = 0, column = 0)
		label_scores_one = tkinter.Label(self, text="Player 1:", width=6, height=2)
		label_scores_one.grid(row = 1, column= 0)

		label_scores_two = tkinter.Label(self, text="Player 2:", width=6, height=2)
		label_scores_two.grid(row = 2, column=0)
		label_scores_three = tkinter.Label(self, text="Player 3:", width=6, height=2)
		label_scores_three.grid(row=3, column=0)

		label_scores_four = tkinter.Label(self, text="Player 4:", width=6, height=2)
		label_scores_four.grid(row=4, column=0)
		label_wins = tkinter.Label(self, text="Wins:", width=6, height=2 )
		label_wins.grid(row=0, column=6)

		label_wins_one = tkinter.Label(self, text="Player 1:", width=6, height=2 )
		label_wins_one.grid(row=1, column=6)
		label_wins_two = tkinter.Label(self, text="Player 2:", width=6, height=2 )
		label_wins_two.grid(row=2, column=6)

		label_wins_three = tkinter.Label(self, text="Player 3:", width=6, height=2 )
		label_wins_three.grid(row=3, column=6)
		label_wins_four = tkinter.Label(self, text="Player 3:", width=6, height=2 )
		label_wins_four.grid(row=4, column=6)

class GameOverScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		global gs
		tkinter.Frame.__init__(self, parent)

		l1 = tkinter.Label(self, text="This is the game over screen where stuff happens.")
		b1 = tkinter.Button(self, text="go to MainMenuScreen frame", command = lambda: controller.show_frame('MainMenuScreen'))

		l1.grid(column = 0, row=0)
		b1.grid(column=0, row=1)

class RoundOverScreen(tkinter.Frame):
	def __init__(self, parent, controller):
		global gs
		tkinter.Frame.__init__(self, parent)

		l1 = tkinter.Label(self, text="This is the round over screen where stuff happens.")
		b1 = tkinter.Button(self, text="go to RoundInProgressScreen frame", command = lambda: controller.show_frame('RoundInProgressScreen'))
		b2 = tkinter.Button(self, text="go to GameOverScreen frame", command = lambda: controller.show_frame('GameOverScreen'))

		l1.grid(column=0, row=0)
		b1.grid(column=0, row=1)
		b2.grid(column=0, row=2)

class MainMenuScreen(tkinter.Frame):
	ip_addr_prefix = "Your IP address is: "
	toggle_flag = True

	def __init__(self, parent, controller):
		def connectToHost():
			global p_id, gs
			nonlocal l7
			global dest_ip
			dest_ip = tb1.get()
			p_id = clientServerInitConnect(dest_ip)
			print('set pid to ' + p_id)
			gs = recvGameState(dest_ip, SERVER_PORT, PACKET_SIZE)

			l7 = tkinter.Label(self, text="Waiting for host to start game...")
			l7.grid(column=0, row=10)

			gs = recvGameState(dest_ip, SERVER_PORT, PACKET_SIZE)
			if gs.game_started:
				showFrame(RoundInProgressScreen, parent, controller)
				self.destroy()


		def connectToClient():
			global gs, p_id
			nonlocal b5, conn_statuses
			p_id = '0'
			gs.players['0'] = Player()
			gs.players['0'].initial_numbers = getUniqueRandNums()
			connected = 1

			while connected < PLAYER_COUNT:
				gs = hostServerInitConnect(gs, connected)
				
				gs.players[str(connected)].initial_numbers = getUniqueRandNums()
				sendGameState(gs.players[str(connected)].ip_addr, SERVER_PORT, PACKET_SIZE, gs)
				connected += 1

				conn_statuses[connected-1].configure(text=f"Player {connected+1}: Connected")

			b5 = tkinter.Button(self, text="Start Game", command=lambda: startGame())
			b5.grid(column=0, row=10)


		
		def toggleRole():
			nonlocal l4, tb1, l3, l2, conn_statuses
			self.toggle_flag = not self.toggle_flag

			if self.toggle_flag:
				l2.configure(text='Current mode: Client')
				l3.configure(text='')
				l4 = tkinter.Label(self, text='Enter the host\'s IP address:')
				l4.grid(column=0, row=6)
				tb1 = tkinter.Entry(self)
				tb1.grid(column=0, row=7)
				l5.destroy()
				l6.destroy()

			else:
				l4.destroy()
				tb1.destroy()

				for i in range(PLAYER_COUNT):
					if i == 0:
						l = tkinter.Label(self, text="Player 1: Connected")
					else:
						l = tkinter.Label(self, text=f"Player {i+1}: Not Connected")

					l.grid(row=i+6, column=0)
					conn_statuses[i] = l

				l2.configure(text='Current mode: Host')
				l3.configure(text=self.ip_addr_prefix + getIPaddr())

				connectToClient()


		def startGame():
			global gs
			gs.game_started = True
			for i in range(1, PLAYER_COUNT):
				p = gs.players[str(i)]
				sendGameState(p.ip_addr, SERVER_PORT, PACKET_SIZE, gs)

			showFrame(RoundInProgressScreen, parent, controller)
			self.destroy()
		
		
		tkinter.Frame.__init__(self, parent)

		l1 = tkinter.Label(self, text="This is the main menu screen where stuff happens.")
		l2 = tkinter.Label(self, text='Current Mode: Client')
		l3 = tkinter.Label(self, text='')
		l4 = tkinter.Label(self, text='Enter the host\'s IP address:')
		# b1 = tkinter.Button(self, text="quit program", command=lambda: exit)
		# b2 = tkinter.Button(self, text='go to RoundInProgressScreen frame', command=lambda: controller.show_frame(RoundInProgressScreen))
		b3 = tkinter.Button(self, text='Toggle host/client', command=lambda: toggleRole())
		b4 = tkinter.Button(self, text='Connect', command=lambda: connectToHost())
		tb1 = tkinter.Entry(self)

		b5 = l7 = None

		conn_statuses = []
		for i in range(PLAYER_COUNT):
			conn_statuses.append(None)


		'''
		global dest_ip
		if tb1.enterKeyIsPressed():
			dest_ip = tb1.get(0)
		'''

		l1.grid(column=0, row=0)
		l2.grid(column=0, row=1)
		l3.grid(column=0, row=2)
		# b2.grid(column=0, row=3)
		b3.grid(column=0, row=4)
		b4.grid(column=0, row=5)
		l4.grid(column=0, row=6)
		tb1.grid(column=0, row=7)



class RootTkObj(tkinter.Tk):
	def __init__(self, *args, **kwargs):
		global gs
		gs = GameState()
		gs.players = {}
		gs.game_started = False
		# calls the customtkinter.CTk object's constructor function
		tkinter.Tk.__init__(self, *args, **kwargs)
		
		#container.pack(side="top", fill="both", expand=True)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others

		container = tkinter.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=10)
		container.grid_columnconfigure(0, weight=10)

		showFrame(MainMenuScreen, container, self)

	# 	self.frames = {}
	# 	for F in (MainMenuScreen, RoundInProgressScreen, RoundOverScreen, GameOverScreen):
	# 		page_name = F.__name__
	# 		frame = F(parent=self.container, controller=self)
	# 		self.frames[page_name] = frame

	# 		# put all of the pages in the same location;
	# 		# the one on the top of the stacking order
	# 		# will be the one that is visible.
	# 		frame.grid(row=0, column=0, sticky="nsew")

	# 	self.show_frame("MainMenuScreen")

	# def show_frame(self, page_name):
	# 	'''Show a frame for the given page name'''
	# 	frame = self.frames[page_name]
	# 	if page_name == 'RoundInProgressScreen':
	# 		frame = RoundInProgressScreen(parent=self.container, controller=self)
	# 	frame.tkraise()

def main():
	app = RootTkObj()
	app.title('superset me')
	app.geometry('600x600')
	app.mainloop()
	
	# app = SampleApp()
	# app.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")

	# app.title('Superset Me!')
	# app.geometry('1500x800')

	# app.mainloop()


if __name__ == '__main__':
	main()
