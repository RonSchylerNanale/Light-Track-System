from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import openpyxl, xlrd
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
root.geometry("800x600")
root.config(bg = background)
root.resizable(True,True)

################################################################

def open_product():
    subprocess.Popen(['python', 'lib/product.py'])
    root.destroy()
    
################################################################

def open_database():
    subprocess.Popen(['python', 'lib/database.py'])
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

imageicon5 = PhotoImage(file='images/inventory.png')
products = Button(button_frame, image=imageicon5, bg='#c19a6b', border=0, command=open_product)
products.pack(side=RIGHT, pady=10, padx=50)

imageicon6 = PhotoImage(file='images/sales.png')
database = Button(button_frame, image=imageicon6, bg='#c19a6b', border=0, command=open_database)
database.pack(side=LEFT, pady=10, padx=50)





root.mainloop()