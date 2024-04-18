import ast
from tkinter import *
from tkinter import messagebox
import mysql.connector
from subprocess import call
import subprocess
from PIL import Image, ImageTk
import customtkinter



window = customtkinter.CTk()
window.title("Sign Up")
window.geometry('800x600+0+0')

window.resizable(True,True)

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"
buttonsbg = "#704214"

window.configure(fg_color=framebg)


def open_signin():
    subprocess.Popen(['python', 'lib/logindb.py'])
    window.destroy() 

    # Establish a connection to the MySQL database

################################################################

def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LTS",
        port = 3306
    )
    return conn

################################################################

def clear():
    user.set('')
    code.set('')

################################################################
    
# Function to sign up a user
def change():
    U1 = user.get()
    C1 = code.get()

    # Establish connection to MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LTS",
        port=3306
    )

    # Create cursor
    cursor = connection.cursor()

    select_query = "SELECT username FROM users WHERE username = %s"
    cursor.execute(select_query, (U1,))
    result = cursor.fetchone()

    if result:
        # Update query
        update_query = """UPDATE users
                          SET password=%s WHERE username=%s"""

        # Data tuple for query parameters
        data = (U1, C1)

        # Execute the update query
        cursor.execute(update_query, data)

        # Commit changes
        connection.commit()

        # Show success message
        messagebox.showinfo("Update", "Password Changed!")

    else:
        # Show error message
        messagebox.showerror("Error", "User not found!")

    # Close cursor and connection
    cursor.close()
    connection.close()

    clear()
################################################################

image_frame = customtkinter.CTkFrame(window, fg_color=(framebg))
image_frame.pack(side=LEFT, padx=0, pady=0)

img1 = Image.open('images/Tanglaw231.png')

img1 = img1.resize((670, 800))

img1 = ImageTk.PhotoImage(img1)

# Create a frame for the main content
frame = customtkinter.CTkFrame(window, fg_color=(framebg))
frame.pack(side=LEFT, padx=10)

# Create an image label
image_label = Label(image_frame, image=img1, bg="#c19a6b")
image_label.grid(row=0, column=0, pady=0)

# Create an image label
img = PhotoImage(file="images/login_logo.png")
image_label = Label(frame, image=img, bg="#c19a6b")
image_label.grid(row=0, column=0, pady=5)

# Create a frame for the heading
heading_frame = customtkinter.CTkFrame(frame, fg_color=(framebg))
heading_frame.grid(row=2, column=0, pady=5)

# Create a label for the heading
heading = Label(heading_frame, text='Reset Password', fg='white', bg='#c19a6b', font=("Microsoft YaHei UI Light", 23, 'bold'))
heading.pack()

divider = Frame(frame, width=295, height=2, bg='white')
divider.grid(row=3, column=0, pady=(10,50))

################################################################

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Username')

################################################################

user = Entry(frame, width=15, fg='white', bg="#c19a6b", border=0, font=("Microsoft YaHei UI Light", 12))
user.default_text = 'Username'
user.insert(0, user.default_text)
user.bind("<FocusIn>", on_enter)
user.bind("<FocusOut>", on_leave)
user.grid(row=4, column=0, columnspan=2, pady=5)

namepad = Frame(frame, width=150, height=2, bg='white')
namepad.grid(row=5, column=0, pady=5)

################################################################

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0, 'New Password')

################################################################
        
code = Entry(frame, width=15, fg='white', bg="#c19a6b", border=0, font=("Microsoft YaHei UI Light", 12))
code.default_text = 'New Password'
code.insert(0, code.default_text)
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)
code.grid(row=6, column=0, columnspan=2, pady=5)

passpad = Frame(frame, width=150, height=2, bg='white')
passpad.grid(row=7, column=0, pady=5)

################################################################

def on_enter(e):
    confirm_code.delete(0, 'end')

def on_leave(e):
    name=confirm_code.get()
    if name=='':
        confirm_code.insert(0, 'Confirm Password')

################################################################
        
confirm_code = Entry(frame, width=15, fg='white', bg="#c19a6b", border=0, font=("Microsoft YaHei UI Light", 12))
confirm_code.default_text = 'Confirm Password'
confirm_code.insert(0, confirm_code.default_text)
confirm_code.bind("<FocusIn>", on_enter)
confirm_code.bind("<FocusOut>", on_leave)
confirm_code.grid(row=8, column=0, columnspan=2, pady=5)

confirmpad = Frame(frame, width=150, height=2, bg='white')
confirmpad.grid(row=9, column=0, pady=5)

#################################################################

customtkinter.CTkButton(frame, text='Sign up', fg_color=(buttonsbg), command=change).grid(row=10, column=0, columnspan=2, pady=5)

customtkinter.CTkButton(frame, text=' Back to Login', fg_color=(framebg), command=open_signin).grid(row=11, column=0, columnspan=2, pady=5)


window.mainloop()