#!/usr/bin/python3
import tkinter #you do need tkinter and customtkinter
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#create CTk window like you do with the Tk window
app = customtkinter.CTk()  
app.geometry("1500x700")
app.title("Superset Me Home")
customtkinter.set_widget_scaling(1.1)

def button_press_server():
    #create CTk window like you do with the Tk window
    app.destroy()
    waiting_server = customtkinter.CTk()  
    waiting_server.geometry("1500x700")
    waiting_server.title("Superset Me Home")
    customtkinter.set_widget_scaling(1.1)

    label = customtkinter.CTkLabel(master=waiting_server,
                               text= "Your IP is:",
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label.place(relx=0.3, rely=0.1, anchor=tkinter.W)
    
    label = customtkinter.CTkLabel(master=waiting_server,
                               text= "The game will begin when there are 4 connected players \nPlayers Joined:",
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label.place(relx=0.3, rely=0.2, anchor=tkinter.W)

    label_player_one = customtkinter.CTkLabel(master=waiting_server,
                               text= "1: ",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_one.place(relx=0.4, rely=0.3, anchor=tkinter.W)

    label_player_two = customtkinter.CTkLabel(master=waiting_server,
                               text= "2:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_two.place(relx=0.4, rely=0.4, anchor=tkinter.W)

    label_player_three = customtkinter.CTkLabel(master=waiting_server,
                               text= "3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_three.place(relx=0.4, rely=0.5, anchor=tkinter.W)

    label_player_four = customtkinter.CTkLabel(master=waiting_server,
                               text= "4:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_four.place(relx=0.4, rely=0.6, anchor=tkinter.W)
    waiting_server.mainloop()

def button_press_client():
    #create CTk window like you do with the Tk window
    app.destroy()
    waiting_client = customtkinter.CTk()  
    waiting_client.geometry("1500x700")
    waiting_client.title("Superset Me Home")
    customtkinter.set_widget_scaling(1.1)
    label = customtkinter.CTkLabel(master=waiting_client,
                               text= "The game will begin when there are 4 connected players \nPlayers Joined:",
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label.place(relx=0.3, rely=0.1, anchor=tkinter.W)

    label = customtkinter.CTkLabel(master=waiting_client,
                               text= "The game will begin when there are 4 connected players \nPlayers Joined:",
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label.place(relx=0.3, rely=0.1, anchor=tkinter.W)

    label_player_one = customtkinter.CTkLabel(master=waiting_client,
                               text= "1: ",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_one.place(relx=0.4, rely=0.2, anchor=tkinter.W)

    label_player_two = customtkinter.CTkLabel(master=waiting_client,
                               text= "2:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_two.place(relx=0.4, rely=0.3, anchor=tkinter.W)

    label_player_three = customtkinter.CTkLabel(master=waiting_client,
                               text= "3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_three.place(relx=0.4, rely=0.4, anchor=tkinter.W)

    label_player_four = customtkinter.CTkLabel(master=waiting_client,
                               text= "4:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

    label_player_four.place(relx=0.4, rely=0.5, anchor=tkinter.W)
    waiting_client.mainloop()

label_player_four = customtkinter.CTkLabel(master=app,
                               text= "Are you the client or server?",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label_player_four.place(relx=0.4, rely=0.2, anchor=tkinter.W)

button = customtkinter.CTkButton(master=app, text="Client", command=button_press_client, font=('Times New Roman',30), width=50, height=50)
button.place(relx=0.45, rely=0.3, anchor=tkinter.CENTER)
button.configure(state=tkinter.NORMAL)

button = customtkinter.CTkButton(master=app, text="Server", command=button_press_server, font=('Times New Roman',30), width=50, height=50)
button.place(relx=0.55, rely=0.3, anchor=tkinter.CENTER)
button.configure(state=tkinter.NORMAL)

app.mainloop()
