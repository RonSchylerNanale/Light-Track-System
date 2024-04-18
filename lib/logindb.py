from tkinter import *
from tkinter import messagebox
import ast
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

#########################################################################

MAX_ATTEMPTS = 5
attempts = 0  # Moved attempts variable outside the signin function

def signin():
    global attempts  # Declare attempts as global to access and modify it
    username = user.get()
    password = code.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result and result[0] == password:
            global logged_in_username
            logged_in_username = username
            subprocess.Popen(['python', 'lib/menu.py'])
            window.destroy()
        else:
            attempts += 1
            if attempts >= MAX_ATTEMPTS:
                show_forgot_password_button()
            else:
                messagebox.showerror('Invalid', 'Invalid Username or Password')

    except mysql.connector.Error as e:
        print("Error connecting to MySQL:", e)
        messagebox.showerror('Error', 'Error connecting to database')

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def show_forgot_password_button():
    forgot_password_button = Button(frame, text="Forgot Password?", border=0, bg="#c19a6b", cursor='hand2', fg='white', command=forgot_pass)
    forgot_password_button.grid(row=10, column=0, columnspan=2, pady=5)
            
#########################################################################

def get_logged_in_username():
    return logged_in_username if 'logged_in_username' in globals() else None

#########################################################################

def open_signup():
    subprocess.Popen(['python', 'lib/signup.py'])
    window.destroy()

#########################################################################

def forgot_pass():
    subprocess.Popen(['python', 'lib/forgot.py'])
    window.destroy()

#########################################################################
    
def toggle_password_visibility():
    if code.cget('show') == '*':
        code.config(show='')
    else:
        code.config(show='*')

#########################################################################

def on_enter(e):
    if e.widget.get() == "Username" or e.widget.get() == "Password":
        e.widget.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0, 'Username')

#########################################################################
    
image_frame = customtkinter.CTkFrame(window, fg_color=(framebg))
image_frame.pack(side=LEFT, padx=0, pady=0, fill='x')

img1 = Image.open('images/Tanglaw231.png')

img1 = img1.resize((670, 800))

img1 = ImageTk.PhotoImage(img1)

frame = customtkinter.CTkFrame(window, fg_color=(framebg))
frame.pack(side= LEFT, padx = 10, anchor='center')

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
heading = Label(heading_frame, text='Log in', fg='white', bg='#c19a6b', font=("Microsoft YaHei UI Light", 23, 'bold'))
heading.pack()

divider = Frame(frame, width=295, height=2, bg='white')
divider.grid(row=3, column=0, pady=(10,50))


################################################################
        
# Entry for username
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
        code.insert(0, 'Password')

################################################################

# Entry for password
code = Entry(frame, width=15, fg='white', bg="#c19a6b", border=0, font=("Microsoft YaHei UI Light", 12), show='*')
code.default_text = 'Password'
code.insert(0, code.default_text)
code.bind("<FocusIn>", on_enter)
code.bind("<FocusOut>", on_leave)
code.grid(row=6, column=0, columnspan=2, pady=5)

#show/hide password
toggle_password_button = Button(frame, text="Show", bg=framebg, fg='white', command=toggle_password_visibility, border=0, font=("Microsoft YaHei UI Light", 10)).grid(row=6, column=0, padx=(0,80), sticky='e')

passpad = Frame(frame, width=150, height=2, bg='white')
passpad.grid(row=7, column=0, pady=5)

# Button for Sign in
customtkinter.CTkButton(frame, text='Sign in', fg_color=(buttonsbg), command=signin).grid(row=8, column=0, columnspan=2, pady=5)

# Buttons for Create Account and Forgot Password
customtkinter.CTkButton(frame, text='Create Account', fg_color=(framebg), command=open_signup).grid(row=9, column=0, columnspan=2, pady=5)


window.mainloop()