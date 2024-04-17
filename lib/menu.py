from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
from tkinter import PhotoImage
import customtkinter

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"
buttonsbg = "#704214"

root = customtkinter.CTk()
root.title("Light Track System")
root.geometry("800x600+0+0")
root.config(bg = background)
root.resizable(True,True)
#root.wm_state('zoomed')

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
    
def confirm_logout():
    confirmed = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
    if confirmed:
        logout_action()

def logout_action():
    subprocess.Popen(['python', 'lib/logindb.py'])
    root.destroy()
    messagebox.showinfo("Logout", "You have been logged out.")

################################################################

label = Label(root, text='Main Menu', width=10, font='Helvetica 15 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

logout_button = customtkinter.CTkButton(label, text='Logout', width=10, fg_color=('white', framebg), command=confirm_logout)
logout_button.pack(side=TOP, anchor='e', pady=10, padx=10)

frame = customtkinter.CTkFrame(root, fg_color=(framebg), corner_radius=5)
frame.pack(side=TOP, fill="both", expand=True)

# Create a frame to hold the buttons
button_frame = customtkinter.CTkFrame(frame,fg_color=(framebg))
button_frame.pack(expand=True)

# Load the original images
imageicon5 = Image.open('images/product.png')
imageicon6 = Image.open('images/inventory.png')
imageicon7 = Image.open('images/history.png')

# Resize the images to 20x20 pixels
imageicon5 = imageicon5.resize((250, 250))
imageicon6 = imageicon6.resize((250, 250))
imageicon7 = imageicon7.resize((250, 250))

# Convert the images to PhotoImage objects
imageicon5 = ImageTk.PhotoImage(imageicon5)
imageicon6 = ImageTk.PhotoImage(imageicon6)
imageicon7 = ImageTk.PhotoImage(imageicon7)

# Now use these resized images in your buttons
products = Button(button_frame, image=imageicon5, bg='#c19a6b', border=0, command=open_product)
products.grid(row=1, column=1)

database = Button(button_frame, image=imageicon6, bg='#c19a6b', border=0, command=open_inventory)
database.grid(row=1, column=2)

database = Button(button_frame, image=imageicon7, bg='#c19a6b', border=0, command=open_history)
database.grid(row=1, column=3)

root.mainloop()