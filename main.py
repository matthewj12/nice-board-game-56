#from screens import *
from constants import *
from networking import *
from boardgamestuff import *
from tkinter_test import *
import tkinter
from tkinter import font as tkfont  # python 3

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

# class RootTkObj(tkinter.Tk):
# 	def __init__(self, *args, **kwargs):
# 		# calls the customtkinter.CTk object's constructor function
# 		tkinter.Tk.__init__(self, *args, **kwargs)
		
# 		#container.pack(side="top", fill="both", expand=True)
		
# 		# By passing this GameState object into every frame, we can have a unified backend state throughout every screen entire GUI. Python is pass-by-reference, so any changes made to gs within a frame class's conscructor will be refleted in this here object.
# 		gs = GameState()
# 		for x in range(PLAYER_COUNT) : # create a player object for each player give them unique numbers
# 			p = Player()
# 			p.initial_numbers = getUniqueRandNums()
# 			p.id_num = x
# 			gs.player_turn_order.insert(x,p)

		
# 		# the container is where we'll stack a bunch of frames
# 		# on top of each other, then the one we want visible
# 		# will be raised above the others

# 		container = tk.Frame(self)
# 		container.pack(side="top", fill="both", expand=True)
# 		container.grid_rowconfigure(0, weight=10)
# 		container.grid_columnconfigure(0, weight=10)

# 		self.frames = {}
# 		for F in (StartPage, HostPage, ClientPage, GameStartPage):
# 			page_name = F.__name__
# 			frame = F(parent=container, controller=self)
# 			self.frames[page_name] = frame

# 			# put all of the pages in the same location;
# 			# the one on the top of the stacking order
# 			# will be the one that is visible.
# 			frame.grid(row=0, column=0, sticky="nsew")

# 			self.show_frame("StartPage")

# 	def show_frame(self, page_name):
# 		'''Show a frame for the given page name'''
# 		frame = self.frames[page_name]
# 		frame.tkraise()

def main():
	app = SampleApp()
	app.title_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")
    #app.geometry("1500x700")

	#app.title('Superset Me!')
	#app.geometry('1280x720')

	app.mainloop()


if __name__ == '__main__':
	main()
