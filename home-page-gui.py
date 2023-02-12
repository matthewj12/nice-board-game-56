#!/usr/bin/python3
import tkinter #you do need tkinter and customtkinter
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

#create CTk window like you do with the Tk window
app = customtkinter.CTk()  
app.geometry("1500x700")
app.title("Superset Me")
customtkinter.set_widget_scaling(1.1)

label = customtkinter.CTkLabel(master=app,
                               text= "Players Joined",
                               width=200,
                               height=70,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.38, rely=0.1, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= "1: ",
                               width=150,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.4, rely=0.35, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= "2:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.37, rely=0.6, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= "3:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.37, rely=0.6, anchor=tkinter.W)

label = customtkinter.CTkLabel(master=app,
                               text= "4:",
                               width=100,
                               height=25,
                               fg_color=("white", "gray"),
                               corner_radius=8,
                               font=('Times New Roman',25))

label.place(relx=0.37, rely=0.6, anchor=tkinter.W)
