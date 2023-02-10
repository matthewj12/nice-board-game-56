#!/usr/bin/python3
import tkinter #you do need tkinter and customtkinter
import customtkinter
import os #this allows you to use the command line to change the date
import subprocess #this allows you to run and stop the program without using os
import datetime #this allows you to get the system date and time
import time #this allows you to use "after" to call the date_time method and update the date and time
import glob #for compressing the zip files to import into jupyter hub
import shutil
import webbrowser
from tkinter import messagebox

global have_numbers

#from the server
have_numbers = "1 2 5 6"
#array
grid = "0 0 0 0\n\n0 0 0 0\n\n0 0 0 0\n\n0 0 0 0"

customtkinter.set_appearance_mode("Light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#create CTk window like you do with the Tk window
app = customtkinter.CTk()  
app.geometry("1500x700")
app.title("Superset Me")
customtkinter.set_widget_scaling(1.1)

#change the display to be able to see better
def mode():
    if (mode_switch.get() == "on"):
        customtkinter.set_appearance_mode("Dark")
    else:
        customtkinter.set_appearance_mode("Light")

def button(button_press, number):
    print(number)
    buttons[button_press].configure(state=tkinter.DISABLED)


mode_switch = customtkinter.CTkSwitch(master=app, text="Dark Mode", command=mode, onvalue="on", offvalue="off")
mode_switch.pack(padx=20, pady=10)
mode_switch.place(relx=0.1, rely=.03, anchor=tkinter.CENTER)

label = customtkinter.CTkLabel(master=app,
                               text= "Your Set: "+have_numbers,
                               width=200,
                               height=70,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.38, rely=0.1, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= grid,
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.4, rely=0.35, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= "pick a number to guess",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.37, rely=0.6, anchor=tkinter.W)

buttons = []
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
x = 0.25
y = 0.7
for i in range(20):
    n = numbers[i]
    number_button = customtkinter.CTkButton(master=app, text=i+1, command=lambda button_press=i, number = n: button(button_press, number),font=('Times New Roman',30), width=50, height=50)
    number_button.place(relx=x, rely=y, anchor=tkinter.CENTER)
    number_button.configure(state=tkinter.NORMAL)
    buttons.append(number_button)
    x=x+0.05
    if i == 9:
        y=y+0.1
        x = 0.25


#disable the numbers they already have
split = have_numbers.split()
for check_n in numbers:
    for check_split in split:
        if check_n == check_split:
            print(int(check_n))
            buttons[int(check_n)-1].configure(state=tkinter.DISABLED)


#this is the start of the gui design where everything is layed out 
label = customtkinter.CTkLabel(master=app,
                               text="Turns:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.1, rely=0.1, anchor=tkinter.W)

    
label = customtkinter.CTkLabel(master=app,
                               text="Player 1:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25))

label.place(relx=0.1, rely=0.2, anchor=tkinter.W)

    
label = customtkinter.CTkLabel(master=app,
                               text="Player 2:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25))

label.place(relx=0.1, rely=0.3, anchor=tkinter.W)
    
label = customtkinter.CTkLabel(master=app,
                               text="Player 3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25))
                               
label.place(relx=0.1, rely=0.4, anchor=tkinter.W)


label = customtkinter.CTkLabel(master=app,
                               text="Player 4:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25))
                               
label.place(relx=0.1, rely=0.5, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text="Wins",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25)
                               )
                              
label.place(relx=0.8, rely=0.1, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text="Player 1:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25)
                               )
                               
label.place(relx=0.8, rely=0.2, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text="Player 2:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius= 5,
                               font=('Times New Roman',25)
                               )
                              
label.place(relx=0.8, rely=0.3, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text="Player 3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25)
                               )
                               
label.place(relx=0.8, rely=0.4, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text="Player 3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=5,
                               font=('Times New Roman',25)
                               )
                               
label.place(relx=0.8, rely=0.5, anchor=tkinter.W)

app.mainloop()