import tkinter
import customtkinter

# Splitting each function into its own file creates circular dependency errors, so I put them all in this one file instead.

class RoundInProgressScreen(customtkinter.CTkFrame):
	def __init__(self, parent, controller, gs):
		customtkinter.CTkFrame.__init__(self, parent)

		l1 = customtkinter.CTkLabel(self, text="This is the round in progress screen where stuff happens.")
		b1 = customtkinter.CTkButton(self, text="go to RoundOver frame", command = lambda: controller.show_frame(RoundOverScreen))

		l1.grid(column=0, row=0)
		b1.grid(column=0, row=1)

class GameOverScreen(customtkinter.CTkFrame):
	def __init__(self, parent, controller, gs):
		customtkinter.CTkFrame.__init__(self, parent)

		l1 = customtkinter.CTkLabel(self, text="This is the game over screen where stuff happens.")
		b1 = customtkinter.CTkButton(self, text="go to MainMenuScreen frame", command = lambda: controller.show_frame(MainMenuScreen))

		l1.grid(column = 0, row=0)
		b1.grid(column=0, row=1)

class RoundOverScreen(customtkinter.CTkFrame):
	def __init__(self, parent, controller, gs):
		customtkinter.CTkFrame.__init__(self, parent)

		l1 = customtkinter.CTkLabel(self, text="This is the round over screen where stuff happens.")
		b1 = customtkinter.CTkButton(self, text="go to RoundInProgressScreen frame", command = lambda: controller.show_frame(RoundInProgressScreen))
		b2 = customtkinter.CTkButton(self, text="go to GameOverScreen frame", command = lambda: controller.show_frame(GameOverScreen))

		l1.grid(column=0, row=0)
		b1.grid(column=0, row=1)
		b2.grid(column=0, row=2)


class MainMenuScreen(customtkinter.CTkFrame):
	ip_addr_prefix = "Your IP address is: "
	toggle_flag = True

	def __init__(self, parent, controller, gs):
		def toggleRole():
			self.toggle_flag = not self.toggle_flag

			if self.toggle_flag:
				l2.configure(text='Current mode: Client')
				l3.configure(text='')
			else:
				l2.configure(text='Current mode: Host')
				l3.configure(text=self.ip_addr_prefix + '192.168.52.98')
		
		
		customtkinter.CTkFrame.__init__(self, parent)

		l1 = customtkinter.CTkLabel(self, text="This is the main menu screen where stuff happens.")
		l2 = customtkinter.CTkLabel(self, text='Client')
		l3 = customtkinter.CTkLabel(self, text='')
		l4 = customtkinter.CTkLabel(self, text='Enter the host\'s IP address:')
		# b1 = customtkinter.CTkButton(self, text="quit program", command=lambda: exit)
		b2 = customtkinter.CTkButton(self, text='go to RoundInProgressScreen frame', command=lambda: controller.show_frame(RoundInProgressScreen))
		b3 = customtkinter.CTkSwitch(self, text='Play as host?', command=lambda: toggleRole())
		tb1 = customtkinter.CTkTextbox(self, width=200, height=30)

		'''
		global dest_ip
		if tb1.enterKeyIsPressed():
			dest_ip = tb1.get(0)
		'''

		l1.grid(column=0, row=0)
		l2.grid(column=0, row=1)
		l3.grid(column=0, row=2)
		l4.grid(column=0, row=6)
		b2.grid(column=0, row=3)
		b3.grid(column=0, row=4)
		tb1.grid(column=0, row=7)
