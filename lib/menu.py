from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
from tkinter import PhotoImage
import customtkinter
import tkinter as tk
import mysql.connector

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

logout_button = customtkinter.CTkButton(label, text='Logout', width=10, fg_color=(framebg), command=confirm_logout)
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




# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        return connection
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL", error)
        return None

# Function to fetch total sales today from the database
def get_total_sales_today(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(total_price) FROM order_log WHERE DATE(timestamp) = CURDATE()")
    result = cursor.fetchone()[0]
    cursor.close()
    return result if result else 0

# Function to fetch overall sales from the database
def get_overall_sales(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT SUM(total_price) FROM order_log")
    result = cursor.fetchone()[0]
    cursor.close()
    return result if result else 0

# Function to fetch the most sold item from the database
def get_most_sold_item(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT product_name, COUNT(*) AS count FROM order_log GROUP BY product_name ORDER BY count DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    return result if result else ("N/A", 0)

# Function to update the labels with the fetched data
def update_labels():
    total_sales_today = get_total_sales_today(db_connection)
    overall_sales = get_overall_sales(db_connection)
    most_sold_item_name, most_sold_item_count = get_most_sold_item(db_connection)

    total_sales_today_label.configure(text="Total Sales Today: Php {:.2f}".format(total_sales_today))
    overall_sales_label.configure(text="Overall Sales: Php {:.2f}".format(overall_sales))
    most_sold_item_label.configure(text="Most Sold Item: {} ({} times)".format(most_sold_item_name, most_sold_item_count))

# Connect to the database
db_connection = connect_to_database()

# Create a frame
statsframe = customtkinter.CTkFrame(root, fg_color=(buttonsbg))
statsframe.pack(padx=0, pady=0, fill="x", anchor="center")

# Create labels
total_sales_today_label = customtkinter.CTkLabel(statsframe, text="Total Sales Today: Php 0.00", fg_color=('white', buttonsbg))
total_sales_today_label.grid(row=0, column=0, padx=10, pady=10)

overall_sales_label = customtkinter.CTkLabel(statsframe, text="Overall Sales: Php 0.00", fg_color=('white', buttonsbg))
overall_sales_label.grid(row=0, column=1, padx=10, pady=10)

most_sold_item_label = customtkinter.CTkLabel(statsframe, text="Most Sold Item: N/A", fg_color=('white', buttonsbg))
most_sold_item_label.grid(row=0, column=2, padx=10, pady=10)

# Center labels within statsframe
statsframe.grid_columnconfigure(0, weight=1)
statsframe.grid_columnconfigure(1, weight=1)
statsframe.grid_columnconfigure(2, weight=1)


# Update labels initially
update_labels()

# Update labels every 10 seconds (10000 milliseconds)
root.after(10000, update_labels)

# Run the main event loop
root.mainloop()


root.mainloop()