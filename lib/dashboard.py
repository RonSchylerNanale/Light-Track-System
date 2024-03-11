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
    
def logout():
    subprocess.Popen(['python', 'lib/logindb.py'])
    root.destroy()
    messagebox.showinfo("Logout", "You have been logged out.")  

################################################################

label = Label(root, text='Dashboard', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

logout = Button(label, text='Logout', width=7, height=1, font='arial 10 bold', bg='#704214', fg='white', border=0, command=logout)
logout.pack(side=TOP, anchor='e', pady=10)

frame = Frame(root, bg="#c19a6b", bd=0)
frame.pack(side=TOP, fill="both", expand=True)


root.mainloop()