#from screens import *
from constants import *
from networking import *
from boardgamestuff import *
from tkinter_test import *
import tkinter

'''
To make this code work with regular tkinter instead of customtkinter (which is pretty much just a wrapper around tkinter providing some custom made, pre-themed widgets), make the following replacements:

tkinter.SampleObj -> customtkinter.SampleObj

Replacements for SampleObj:
	Frame -> CTkFrame
	Button -> CTkButton
	Label -> CTkLabel
	etc.
'''

dest_ip = None
dest_port = None

class RootCtkObj(tkinter.Tk):
	def __init__(self, *args, **kwargs):
		# calls the customtkinter.CTk object's constructor function
		super().__init__()
		
		#container.pack(side="top", fill="both", expand=True)
		
		# By passing this GameState object into every frame, we can have a unified backend state throughout every screen entire GUI. Python is pass-by-reference, so any changes made to gs within a frame class's conscructor will be refleted in this here object.
		gs = GameState()
		for x in range(PLAYER_COUNT) : # create a player object for each player give them unique numbers
			p = Player()
			p.initial_numbers = getUniqueRandNums()
			p.id_num = x
			gs.player_turn_order.insert(x,p)

		# TODO: initialize gs.players with their secret numbers, use functions in networking.py to assign them their ids, accept usernames, define turn order, etc.
		# This is where the code that's currently in the "playGame" function in "board-game-cli.py" (This file no longer exists in the repository. Refer to previous committs to see it) needs to go.
		# We will use functions from boardgamestuff.py to implement this, but the actual top-level of the game lives here.
		# The constructors (__init__ functions) of each class in screens.py is where the other half of the game logic will occurr. When players press keys and hit enter or click buttons, the game state object gs must be updated accordingly.
		container = tk.Frame(self)
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
		# select the frame from the list of all frames.
		frame = self.frames[page_name]
		# Create the frame and make it visible.
		frame.tkraise()


def main():
	app = RootCtkObj()

	app.title('Superset Me!')
	app.geometry('1280x720')

	app.mainloop()


if __name__ == '__main__':
	main()
