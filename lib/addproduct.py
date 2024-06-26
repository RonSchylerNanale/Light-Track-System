from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import io
from tkinter.ttk import Combobox
import mysql.connector
from subprocess import call
import subprocess
from PIL import Image, ImageTk
from tkinter import StringVar
from datetime import datetime
import tkinter.messagebox as messagebox
import customtkinter
import tkinter as tk



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


# Define a StringVar to hold the image data
image_data_var = StringVar()

def create_tables():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Create the products table if it doesn't exist
        create_products_table_query = """
            CREATE TABLE IF NOT EXISTS products (
                registration VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(255),
                description TEXT,
                date DATE,
                price DECIMAL(10, 2),
                quantity INT,
                attributes TEXT,
                supplier VARCHAR(255),
                image LONGBLOB
            )
        """
        cursor.execute(create_products_table_query)
        conn.commit()

        # Create the archive table if it doesn't exist
        create_archive_table_query = """
            CREATE TABLE IF NOT EXISTS archive (
                registration VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                category VARCHAR(255),
                description TEXT,
                date DATE,
                price DECIMAL(10, 2),
                quantity INT,
                attributes TEXT,
                supplier VARCHAR(255),
                image LONGBLOB
            )
        """
        cursor.execute(create_archive_table_query)
        conn.commit()

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror('Error', 'Failed to create tables.')

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Call create_tables function before executing any other code
create_tables()

def Exit():
    subprocess.Popen(['python', 'lib/product.py'])
    root.destroy()

################################################################
    
def product_no():
    # Establish connection to MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LTS",
        port = 3306
    )

    # Create cursor
    cursor = connection.cursor()

    # Query to get the maximum registration number
    query = "SELECT MAX(Registration) FROM products"

    # Execute query
    cursor.execute(query)

    # Fetch the result
    max_registration = cursor.fetchone()[0]

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Set the registration number accordingly
    if max_registration is not None:
        Registration.set(int(max_registration) + 1)  # Convert max_registration to int
    else:
        Registration.set("1")
     
################################################################

def clear():
    global img
    Name.set('')
    Category.set("Select Category")
    Description.set('')
    Price.set('')
    Quantity.set('')
    Attributes.set('')
    Supplier.set('')

    product_no()

    saveButton.configure(state = 'normal')

    try:
        # Load and display the default image
        img1 = PhotoImage(file='Images/upload_photo.png')
        lbl.config(image=img1)
        lbl.image = img1
    except TclError:
        print("Error loading default image")  # Handle any potential error

################################################################
        
def show_image():
    global filename, img_variable

    # Open the file dialog to select an image
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), 
                                          title='Select Image File',
                                          filetype=(("PNG File", "*.png"),
                                                    ("JPG File", "*.jpg"),
                                                    ("All Files", "*.*")))
    if filename:
        # Open and resize the image
        img = Image.open(filename)
        img = img.resize((250, 250))

        # Convert the image to PhotoImage format
        img_variable = ImageTk.PhotoImage(img)

        # Display the image in the label
        lbl.config(image=img_variable)
        lbl.image = img_variable
    else:
        img_variable = None

    return img_variable  # Return the PhotoImage object

################################################################

def convertToBinary(img_variable):
    with open(img_variable, 'rb') as file:
        binarydata=file.read()
    return binarydata

################################################################
    
def Save():
    try:
        R1 = Registration.get()
        N1 = Name.get()
        C1 = Category.get()
        D2 = Description.get()
        D1 = Date.get()
        P1 = Price.get()
        Q1 = Quantity.get()
        A1 = Attributes.get()
        S1 = Supplier.get()

        # Get the image data if available
        img_data = None
        if 'img_variable' in globals() and img_variable:
            img_data = convertToBinary(filename)  # pass filename

        # Check if any required data is missing
        if N1 == "" or C1 == "" or D2 == "" or D1 == "" or P1 == "" or Q1 == "" or A1 == "" or S1 == "":
            messagebox.showerror("Error", "Some data is missing!")
            return

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            registration INTEGER PRIMARY KEY,
            name VARCHAR(45) NOT NULL,
            category VARCHAR(45) NOT NULL,
            description VARCHAR(255) NOT NULL, 
            date DATE NOT NULL, 
            price INTEGER NOT NULL, 
            quantity INTEGER NOT NULL, 
            attributes VARCHAR(255) NOT NULL, 
            supplier VARCHAR(255) NOT NULL,
            image LONGBLOB 
        )
        """)

        # Check if the product already exists
        query = "SELECT * FROM products WHERE name = %s"
        cursor.execute(query, (N1,))
        existing_product = cursor.fetchone()

        # Insert data into the database
        if existing_product:
            messagebox.showerror('Error', 'Product already exists')
        else:
            insert_query = "INSERT INTO products (registration, name, category, description, date, price, quantity, attributes, supplier, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (R1, N1, C1, D2, D1, P1, Q1, A1, S1, img_data)
            cursor.execute(insert_query, data)
            conn.commit()

            log_changes("Added", R1, N1)

            messagebox.showinfo('Info', 'Product added successfully!')
            clear()  # Clear the entry fields
            product_no()  # Generate a new registration number

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror("Error", "Failed to add product! Product Number already exists!")

    except tk.TclError as tcl_err:
        print("TclError:", tcl_err)
        messagebox.showerror("Error", "Please enter only numbers for the Price and Quantity fields!") 

    finally:
        if conn.is_connected():
            cursor.close()

################################################################

def Update():
    R1 = Registration.get()
    N1 = Name.get()
    C1 = Category.get()
    D2 = Description.get()
    D1 = Date.get()
    P1 = Price.get()
    Q1 = Quantity.get()
    A1 = Attributes.get()
    S1 = Supplier.get()

    # Get the image data if available
    img_data = None
    if 'img_variable' in globals() and img_variable:
        img_data = convertToBinary(filename)  # pass filename

    # Check if any required data is missing
    if N1 == "" or C1 == "" or D2 == "" or D1 == "" or P1 == "" or Q1 == "" or A1 == "" or S1 == "":
        messagebox.showerror("Error", "Some data is missing!")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Check if the product exists
        query = "SELECT * FROM products WHERE registration = %s"
        cursor.execute(query, (R1,))
        existing_product = cursor.fetchone()

        # Update data in the database
        if existing_product:
            update_query = """
                UPDATE products
                SET name=%s, category=%s, description=%s, date=%s, price=%s, quantity=%s, attributes=%s, supplier=%s, image=%s
                WHERE registration=%s
            """
            data = (N1, C1, D2, D1, P1, Q1, A1, S1, img_data, R1)
            cursor.execute(update_query, data)
            conn.commit()

            log_changes("Updated", R1, N1)

            messagebox.showinfo('Info', 'Product updated successfully!')
            clear()  # Clear the entry fields

        else:
            messagebox.showerror('Error', 'Product does not exist')

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror("Error", "Failed to update product!")

    finally:
        if conn.is_connected():
            cursor.close()

################################################################

def search():
    text = Search.get()

    clear()
    saveButton.configure(state='disabled')

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Execute SQL query to search for the product
        query = "SELECT * FROM products WHERE name LIKE %s"
        cursor.execute(query, ("%" + text + "%",))
        result = cursor.fetchone()

        if result:
            # Populate the fields with the fetched data
            Registration.set(result[0])
            Name.set(result[1])
            Category.set(result[2])
            Description.set(result[3])
            Date.set(result[4])
            Price.set(result[5])
            Quantity.set(result[6])
            Attributes.set(result[7])
            Supplier.set(result[8])
            
            # Set the image data
            image_data = result[9]

            # Load and display the image
            try:
                img = Image.open(io.BytesIO(image_data))
                img = img.resize((200, 200))  # Resize the image
                img = ImageTk.PhotoImage(img)
                lbl.config(image=img)
                lbl.image = img  # Keep a reference to prevent image from being garbage collected
            except FileNotFoundError:
                messagebox.showinfo('Info', 'Product Image is not available')

        else:
            messagebox.showerror('Invalid', 'Invalid Product Name')

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror('Error', 'Failed to search product.')

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

################################################################
            
def on_enter(e):
    search_entry.delete(0, 'end')

def on_leave(e):
    name=search_entry.get()
    if name=='':
        search_entry.insert(0, 'Search')

################################################################
            
def log_changes(action, registration_number, product_name):
    
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Create change_log table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS change_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(50) NOT NULL,
            registration_number INT NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Get current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Insert log entry into the database
        insert_query = "INSERT INTO change_log (action, registration_number, product_name, timestamp) VALUES (%s, %s, %s, %s)"
        data = (action, registration_number, product_name, current_datetime)
        cursor.execute(insert_query, data)
        conn.commit()

    except mysql.connector.Error as e:
        print("Error:", e)

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

################################################################
 
#### HEADER ####

# top frames
label = Label(root, text='Add / Update Product', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

imageicon3 = PhotoImage(file='images/search.png')
search_button = Button(label, image=imageicon3, bg='#704214', fg='white', font='Helvetica 13 bold', command=search, bd=0)
search_button.pack(side=RIGHT, padx=0, pady=10, anchor="e")

# search box
Search = StringVar()
search_entry = customtkinter.CTkEntry(label, textvariable=Search, fg_color=(framebg))
search_entry.default_text = 'Search'
search_entry.insert(0, search_entry.default_text)
search_entry.bind("<FocusIn>", on_enter)
search_entry.bind("<FocusOut>", on_leave)
search_entry.pack(side="right", padx=10, pady=10)

#################################################################

frame = customtkinter.CTkFrame(root, fg_color=(framebg))
frame.pack(side=TOP, fill="both")

Label(frame, text='Product No: ', font='Helvetica 10 bold', fg='white', bg=framebg).grid(row=1, column=1, padx=(10, 0), pady=10, sticky="e")
Label(frame, text='Date: ', font='Helvetica 10 bold', fg='white', bg=framebg).grid(row=1, column=3, padx=(20, 0), pady=10, sticky="e")

Registration = IntVar()
Date = StringVar()

reg_entry = Entry(frame, textvariable=Registration, width=15, font='Helvetica 10', border=0)
reg_entry.grid(row=1, column=2, padx=10, pady=10, sticky="e")

product_no()

today = date.today()
d1 = today.strftime("%y/%m/%d")
date_entry = Entry(frame, textvariable=Date, width=15, font='Helvetica 10')
date_entry.grid(row=1, column=4, padx=10, pady=10, sticky="e")
Date.set(d1)   

##################################################################

obj = Label(root, font=15, bd=2, width=500, bg=framebg, fg='white', height=250, relief=GROOVE)
obj.pack(side=LEFT, fill="both")

Label(obj, text="Product Name:", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=0, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Category:", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=1, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Description:", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=2, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Price:", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=3, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Quantity: ", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=4, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Attributes: ", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=5, column=0, padx=10, pady=10, sticky="w")
Label(obj, text="Supplier: ", font='Helvetica 10 bold', bg=framebg, fg='white').grid(row=6, column=0, padx=10, pady=10, sticky="w")

Name = StringVar()
name_entry = Entry(obj, textvariable=Name, width=20, font='Helvetica 10 bold', bg='white')
name_entry.grid(row=0, column=2, padx=10, pady=10)

Category = Combobox(obj, values=['Candle', 'Scented Candle', 'Bundle'])
Category.grid(row=1, column=2, padx=10, pady=10)
Category.set('Select Category')

Description = StringVar()
description_entry = Entry(obj, textvariable=Description, width=20, font='Helvetica 10 bold', bg='white')
description_entry.grid(row=2, column=2, padx=10, pady=10)

Price = IntVar()
price_entry = Entry(obj, textvariable=Price, width=20, font='Helvetica 10 bold', bg='white')
price_entry.grid(row=3, column=2, padx=10, pady=10)

Quantity = IntVar()
quanti_entry = Entry(obj, textvariable=Quantity, width=20, font='Helvetica 10 bold', bg='white')
quanti_entry.grid(row=4, column=2, padx=10, pady=10)

Attributes = StringVar()
attribute_entry = Entry(obj, textvariable=Attributes, width=20, font='Helvetica 10 bold', bg='white')
attribute_entry.grid(row=5, column=2, padx=10, pady=10)

Supplier = StringVar()
supply_entry = Entry(obj, textvariable=Supplier, width=20, font='Helvetica 10 bold', bg='white')
supply_entry.grid(row=6, column=2, padx=10, pady=10)

updateButton = customtkinter.CTkButton(obj, text='Update', fg_color=(buttonsbg), command= Update)
updateButton.grid(row=8, column=0, padx=10, pady=10)

resetButton = customtkinter.CTkButton(obj, text='Clear', fg_color=(
    '#704214'), command=clear)
resetButton.grid(row=8, column=2, padx=10, pady=10)

################################################

imageFrame = customtkinter.CTkFrame(root, fg_color=('white', framebg), corner_radius=0)
imageFrame.pack(side=TOP, anchor="center")

customtkinter.CTkLabel(imageFrame, text="Product Image", fg_color=(framebg)).grid(row=0, column=1, padx=10, pady=10, sticky="we")

f = customtkinter.CTkFrame(imageFrame, fg_color=(buttonsbg))
f.grid(row=1, column=1, padx=20, pady=0, sticky='we')

lbl = Label(f, bg='#704214')
lbl.place(x=5, y=5)

uploadButton = customtkinter.CTkButton(imageFrame, text='Upload Photo', fg_color=(buttonsbg), command=show_image)
uploadButton.grid(row=3, column=1, padx=10, pady=10)

########################################################################

buttonFrame = customtkinter.CTkFrame(root,fg_color=(framebg), corner_radius=0)
buttonFrame.pack(side=BOTTOM, anchor="n")

saveButton = customtkinter.CTkButton(buttonFrame, text='Save', fg_color=('#704214'), command=Save)#, width=15, height=2, font='Helvetica 10 bold', bg='#704214', fg='white', command=Save, border=0)
saveButton.grid(row=1, column=2, padx=10, pady=10)

exitButton = customtkinter.CTkButton(buttonFrame, text='Done', fg_color=('#704214'), command=Exit)#, width=15, height=2, font='Helvetica 10 bold', bg='#704214', fg='white', command=Exit, border=0)
exitButton.grid(row=1, column=4, padx=10, pady=10)


root.mainloop()