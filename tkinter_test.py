from boardgamestuff import *
from networking import *
from main import *

try:
	import tkinter as tk                # python 3
	from tkinter import font as tkfont  # python 3
except ImportError:
	import tKinter as tk     # python 2
	import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		global ip_address
		global client_enter_ip
		global player_four
		global player_three
		global player_two
		global player_one
		global buttons
		global numbers
		global have_numbers
		global grid
		global grid_fill
		#from the server
		have_numbers = " ".join([str(i) for i in getUniqueRandNums()])
		#array
		grid_fill = []
		#make the grid read in areas of four, like n%4 to know which x belongs to which person
		grid = ["X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X", "X"]

		buttons = []
		numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
		ip_address = getIPaddr()
		client_enter_ip = ""
		player_one = ""
		player_two = ""
		player_three = ""
		
		player_four = ""

		# By passing this GameState object into every frame, we can have a unified backend state throughout every screen entire GUI. Python is pass-by-reference, so any changes made to gs within a frame class's conscructor will be refleted in this here object.
		gs = GameState()
		for x in range(PLAYER_COUNT) : # create a player object for each player give them unique numbers
			p = Player()
			p.initial_numbers = getUniqueRandNums()
			p.id_num = x
			gs.player_turn_order.insert(x,p)

		# the container is where we'll stack a bunch of frames
		# on top of each other, then the one we want visible
		# will be raised above the others
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=10)
		container.grid_columnconfigure(0, weight=10)

		self.frames = {}
		for F in (StartPage, HostPage, ClientPage, GameStartPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame

			# put all of the pages in the same location;
			# the one on the top of the stacking order
			# will be the one that is visible.
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

	def show_frame(self, page_name):
		'''Show a frame for the given page name'''
		frame = self.frames[page_name]
		frame.tkraise()


class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.controller = controller
		label = tk.Label(self, text="Are you the Host or Client?", font=('Times New Roman',50))
		label.pack(side="top", fill="x", pady=10)

		button1 = tk.Button(self, text="Host", height = 3, width = 20, font=('Times New Roman',30),
							command=lambda: controller.show_frame("HostPage"))
		button2 = tk.Button(self, text="Client", height = 3, width = 20, font=('Times New Roman',30),
							command=lambda: controller.show_frame("ClientPage"))
		button1.pack()
		button2.pack()


class HostPage(tk.Frame):

	def __init__(self, parent, controller):
		global player_four
		global player_three
		global player_two
		global player_one
        
		tk.Frame.__init__(self, parent)

		self.controller = controller
        
		label = tk.Label(self, text="This is Your IP: "+getIPaddr(), font=('Times New Roman',50))
		label.pack(side="top", fill="x", pady=10)
		label_announce = tk.Label(self,
							text= "The game will begin when there are 4 connected players \nPlayers Joined:",
							width=40,
							height=2,
							font=('Times New Roman',25))

		label_player_one = tk.Label(self,
							text= "1: "+player_one,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_two = tk.Label(self,
							text= "2: "+player_two,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_three = tk.Label(self,
							text= "3: "+player_three,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_four = tk.Label(self,
							text= "4: "+player_four,
							width=10,
							height=2,
							font=('Times New Roman',25))
		
		button_restart = tk.Button(self, text="Restart",
							width=10,
							height=2,
							font=('Times New Roman',25),
							command=lambda: controller.show_frame("StartPage"))
		
		button_Ready= tk.Button(self, text="Ready",
							width=10,
							height=2,
							font=('Times New Roman',25),
							command=hosting)
		
		label.grid(row=0, column=3)
		label_announce.grid(row = 1, column = 3)
		label_player_one.grid(row = 2, column = 2)
		label_player_two.grid(row = 3, column = 2)
		label_player_three.grid(row = 4, column = 2)
		label_player_four.grid(row = 5, column = 2)
		button_restart.grid(row = 6, column = 2)
		button_Ready.grid(row = 6, column = 4)

def hosting():
	hostServerInitConnect()

class ClientPage(tk.Frame):

	def __init__(self, parent, controller):
	   
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="Enter your Ip: ", font=('Times New Roman',50))
		label.pack(side="top", fill="x", pady=10)
		entry_ip = tk.Entry(self, font=('Times New Roman',25))

		label_announce = tk.Label(self,
							text= "The game will begin when there are 4 connected players \nPlayers Joined:",
							width=40,
							height=2,
							font=('Times New Roman',25))

		label_player_one = tk.Label(self,
							text= "1: "+player_one,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_two = tk.Label(self,
							text= "2: "+player_two,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_three = tk.Label(self,
							text= "3: "+player_three,
							width=10,
							height=2,
							font=('Times New Roman',25))

		label_player_four = tk.Label(self,
							text= "4: "+player_four,
							width=10,
							height=2,
							font=('Times New Roman',25))
		
		button_restart = tk.Button(self, text="Restart",
							width=10,
							height=2,
							font=('Times New Roman',25),
							command=lambda: controller.show_frame("StartPage"))
		button_IP = tk.Button(self, text="Connect",
							width=10,
							height=2,
							font=('Times New Roman',25),
							command=lambda: loadIP(str(entry_ip.get())) )
		button_ready = tk.Button(self, text="Ready",
							width=10,
							height=2,
							font=('Times New Roman',25),
							#have a connector to server here, not sure but its giving me an error
							
							command=lambda: controller.show_frame("GameStartPage"))
		
		label.grid(row=0, column=3)
		entry_ip.grid(row=0, column=4)
		label_announce.grid(row = 1, column = 4)
		label_player_one.grid(row = 2, column = 2)
		label_player_two.grid(row = 3, column = 2)
		label_player_three.grid(row = 4, column = 2)
		label_player_four.grid(row = 5, column = 2)
		button_restart.grid(row = 6, column = 3)
		button_IP.grid(row = 6, column = 5)
		button_ready.grid(row = 6, column = 4)
class loadIP:
    def __init__(self, dest_ip):
        clientServerInitConnect(dest_ip)

class GameStartPage(tk.Frame):

	def __init__(self, parent, controller):
		print(client_enter_ip)
		Connection(client_enter_ip, 6100, getIPaddr())
		tk.Frame.__init__(self, parent)
		self.controller = controller
		def button(button_press, number):
			#getGuessFromPlayer(number)
			print(number)
			global have_numbers

		    #sendGameState(client_enter_ip, 6100, 99999, )
			buttons[button_press]["state"] = tk.DISABLED
			have_numbers_add = have_numbers+" "+str(number)
			have_numbers = have_numbers_add
			label_have_numbers["text"] = "Your Set: "+ have_numbers

		label_have_numbers = tk.Label(self,
							   text= "Your Set: "+have_numbers,
							   width=30,
							   height=2,
							   font=('Times New Roman',25))

		label_have_numbers.grid(row=0, column=12)

		#creating the grid
		col = 2
		rowi = 1
		for i in range(16):
			n = grid[i]
			label_grid = tk.Label(self, text=".", font=('Times New Roman',30), width=2, height=1, state = tk.NORMAL)
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
		col = 0
		rowi = 6
		for i in range(20):
			n = numbers[i]
			number_button = tk.Button(self, text=i+1, command=lambda button_press=i, number = n: button(button_press, number),font=('Times New Roman',30), width=2, height=1, state = tk.NORMAL)
			number_button.grid(row = rowi, column = col)
			buttons.append(number_button)
			col=col+1
			if i == 9:
				rowi=rowi+1
				col = 0

		#disable the button numbers they already have
		split = have_numbers.split()
		for check_n in numbers:
			for check_split in split:
				if check_n == check_split:
					buttons[int(check_n)-1]["state"]=tk.DISABLED

		button_restart = tk.Button(self, text="Restart",
							width=5,
							height=2,
							font=('Times New Roman',25),
							command=lambda: controller.show_frame("StartPage"))

		button_restart.grid(row = 8, column = 9)

		label_scores = tk.Label(self,
							   text="Scores:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25))

		label_scores.grid(row = 0, column = 0)

		label_scores_one = tk.Label(self,
							   text="Player 1:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25))

		label_scores_one.grid(row = 1, column= 0)

	
		label_scores_two = tk.Label(self,
							   text="Player 2:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25))

		label_scores_two.grid(row = 2, column=0)
	
		label_scores_three = tk.Label(self,
							   text="Player 3:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25))
							   
		label_scores_three.grid(row=3, column=0)


		label_scores_four = tk.Label(self,
							   text="Player 4:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25))
							   
		label_scores_four.grid(row=4, column=0)

		label_wins = tk.Label(self,
							   text="Wins:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25)
							   )
							  
		label_wins.grid(row=0, column=6)

		label_wins_one = tk.Label(self,
							   text="Player 1:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25)
							   )
							   
		label_wins_one.grid(row=1, column=6)

		label_wins_two = tk.Label(self,
							   text="Player 2:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25)
							   )
							  
		label_wins_two.grid(row=2, column=6)

		label_wins_three = tk.Label(self,
							   text="Player 3:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25)
							   )
							   
		label_wins_three.grid(row=3, column=6)

		label_wins_four = tk.Label(self,
							   text="Player 3:",
							   width=6,
							   height=2,
							   font=('Times New Roman',25)
							   )
							   
		label_wins_four.grid(row=4, column=6)

if __name__ == "__main__":
	app = SampleApp()
	app.mainloop()