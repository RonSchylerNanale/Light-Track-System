from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
from openpyxl import Workbook
import pathlib
import mysql.connector
from subprocess import call
import subprocess

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"

root = Tk()
root.title("Light Track System")
root.geometry("800x600+0+0")
root.config(bg = background)
root.resizable(True,True)

################################################################

def open_product():
    subprocess.Popen(['python', 'lib/product.py'])
    root.destroy()
    
################################################################

def open_inventory():
    subprocess.Popen(['python', 'lib/inventory.py'])
    root.destroy()

################################################################

def open_history():
    subprocess.Popen(['python', 'lib/history.py'])
    root.destroy()

################################################################
    
def logout():
    subprocess.Popen(['python', 'lib/logindb.py'])
    root.destroy()
    messagebox.showinfo("Logout", "You have been logged out.")  

################################################################

label = Label(root, text='Main Menu', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

logout = Button(label, text='Logout', width=7, height=1, font='arial 10 bold', bg='#704214', fg='white', border=0, command=logout)
logout.pack(side=TOP, anchor='e', pady=10)

frame = Frame(root, bg="#c19a6b", bd=0)
frame.pack(side=TOP, fill="both", expand=True)

# Create a frame to hold the buttons
button_frame = Frame(frame, bg="#c19a6b")
button_frame.pack(expand=True)

imageicon5 = PhotoImage(file='images/product.png')
products = Button(button_frame, image=imageicon5, bg='#c19a6b', border=0, command=open_product)
products.grid(row=1, column=0)

imageicon6 = PhotoImage(file='images/inventory.png')
database = Button(button_frame, image=imageicon6, bg='#c19a6b', border=0, command=open_inventory)
database.grid(row=1, column=1)

imageicon7 = PhotoImage(file='images/history.png')
database = Button(button_frame, image=imageicon7, bg='#c19a6b', border=0, command=open_history)
database.grid(row=1, column=2)


clock_frame = Frame(label, bg="#c19a6b")
clock_frame.pack(expand=True)

lbl_clock=Label(clock_frame, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYY Time: HH-MM-SS", compound=LEFT, font=("Helvetica", 10, "bold"), bg="white", fg="black", anchor="w", padx=20)
lbl_clock.grid(row=0, column=2)



root.mainloop()