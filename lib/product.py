from tkinter import *
from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import mysql.connector
from subprocess import call
import subprocess
from tkinter import ttk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
from mysql.connector import Error
import io


background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"

root = Tk()
root.title("Light Track System")
root.geometry("800x600+0+0")
root.config(bg = background)
root.resizable(True,True)

style = ttk.Style()
style.theme_use("clam")  # Use the default theme
style.configure("Treeview", rowheight=25, background=framebg, foreground = "white")  # Set row height and background color
style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"),  background="#704214", foreground="white")  # Set heading font
style.map("Treeview", foreground=[('selected', 'black')], background=[('selected', 'white')])  # Set selected row color
style.configure("Treeview", fieldbackground=framebg)  # Set field background color
style.configure("Treeview.Treeitem", background=framebg, fieldbackground=framebg, foreground ="white")  # Set item background color

# Connect to MySQL database
mydb = mysql.connector.connect(
   host="localhost",
    user="root",
    password="",
    database="LTS",
    port=3306
)
mycursor = mydb.cursor()
 
def Exit():
    root.destroy()

def add():
    subprocess.Popen(['python', 'lib/addproduct.py'])
    root.destroy()

def archive():
    subprocess.Popen(['python', 'lib/archive.py'])
    root.destroy()

################################################################
    
def load_data():
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

    # Execute query to select data from the table
    cursor.execute("SELECT registration, name, price, quantity FROM products")

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Configure treeview headings with column names
    for col_name in cursor.column_names:
        treeview.heading(col_name, text=col_name)

    # Insert data into treeview
    for row in rows:
        treeview.insert('', END, values=row)

################################################################

def search():
    text = Search.get().lower()  # Convert search text to lowercase for case-insensitive search
    
    # Clear any previous selection in the Treeview
    treeview.selection_remove(treeview.selection())

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
        query = "SELECT * FROM products WHERE LOWER(CONCAT(registration, name, price, quantity)) LIKE %s"
        cursor.execute(query, ("%" + text + "%",))

        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert matching rows into the Treeview
        for row in cursor.fetchall():
        # Extract specific columns from the row
            registration, name, price, quantity = row[0], row[1], row[5],row[6]

        # Insert the extracted values into the Treeview
            treeview.insert("", "end", values=(registration, name, price,quantity))

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror('Error', 'Failed to search product.')

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

################################################################
    
def back():
    subprocess.Popen(['python', 'lib/menu.py'])
    root.destroy() 

################################################################

class SortableTreeview(ttk.Treeview):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.heading_clicked = False
        self.heading_map = {}  # Dictionary to map heading names to column IDs
        self.bind("<ButtonRelease-1>", self.on_click)

    def set_heading(self, heading_map):
        self.heading_map = heading_map

    def on_click(self, event):
        region = self.identify("region", event.x, event.y)
        if region == "heading":
            self.heading_clicked = True

    def sort_by_column(self, column, reverse=False):
        # Function to convert values to numerical type if possible
        def convert(value):
            try:
                return float(value)
            except ValueError:
                return value

        # Get all items and their values in the specified column
        items = [(convert(self.set(i, column)), i) for i in self.get_children("")]

        # Sort the items based on their numerical values
        items.sort(key=lambda x: x[0], reverse=reverse)

        # Reorder the items in the treeview
        for index, (_, i) in enumerate(items):
            self.move(i, "", index)

        # Toggle the sorting direction for the next click
        self.heading(column, command=lambda: self.sort_by_column(column, not reverse))

#################################################################

def on_enter(e):
    search_entry.delete(0, 'end')

def on_leave(e):
    name=search_entry.get()
    if name=='':
        search_entry.insert(0, 'Search')

#################################################################

def fetch_data(registration):
    query = "SELECT * FROM products WHERE registration = %s"
    mycursor.execute(query, (registration,))
    result = mycursor.fetchone()  # Fetch a single row
    return result

#################################################################

def clear_product_details():
    # Destroy the existing LabelFrame widget
    obj.destroy()

#################################################################

def display_image(obj, image_data):
    try:
        # Convert image data to PhotoImage
        img = Image.open(io.BytesIO(image_data))
        img = img.resize((200, 200))  # Resize the image
        img = ImageTk.PhotoImage(img)
        image_label = Label(obj, image=img)
        image_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        image_label.image = img  # Keep a reference to prevent image from being garbage collected
    
    except Exception as e:
        print("Error:", e)
        # Display a placeholder image or error message
        error_img = Image.open("images/error_image.jpg")  # Provide a path to a placeholder error image
        error_img = error_img.resize((200, 200))  # Resize the error image
        error_img = ImageTk.PhotoImage(error_img)
        image_label = Label(obj, image=error_img)
        image_label.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        image_label.image = error_img  # Keep a reference to prevent image from being garbage collected

#################################################################

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

#################################################################

def submit_order(product_data, registration_number, product_name):
    # Function to handle making an order for the selected product
    def submit_order():
        # Get the amount ordered from the Entry widget
        amount_ordered = amount_entry.get()

        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Update the quantity in the database
        cursor.execute("UPDATE products SET quantity = quantity - %s WHERE registration = %s", (amount_ordered, product_data[0]))

        # Commit the transaction
        conn.commit()

        # Close the database connection
        conn.close()

        # Log the changes
        log_changes("sold", registration_number, product_name)

        # Print a confirmation message
        print(f"Ordered {amount_ordered} of {product_data[1]}")

        # Close the order window
        order_window.destroy()

        # Refresh the TreeView
        refresh_treeview()
        refresh_label()

    # Create a new Toplevel window for the order
    order_window = Toplevel()
    order_window.title("Make Order")
    
    # Add labels and entry for amount
    Label(order_window, text="Amount Ordered:").grid(row=0, column=0, padx=5, pady=5)
    amount_entry = Entry(order_window)
    amount_entry.grid(row=0, column=1, padx=5, pady=5)

    # Add a button to submit the order
    submit_button = Button(order_window, text="Submit Order", command=submit_order)
    submit_button.grid(row=1, columnspan=2, padx=5, pady=5)

    # Make amount_entry accessible within the function
    submit_order.amount_entry = amount_entry  # Assigning to a function attribute

#################################################################

def select_product_for_order(data):
    # Assuming data contains product information
    registration_number = data[0]
    product_name = data[1]

    # Check if the Frame widget exists before destroying it
    if 'obj' in globals():
        clear_product_details()

    if data:
        # Create a new Frame widget to display product details
        global obj
        obj = Frame(root, bd=0, width=350, bg=framebg, relief=GROOVE)
        obj.pack(side=TOP, anchor="n", padx=10, pady=10, fill='x')

        # Labels for database fields
        labels = ['Product No:', 'Product Name:', 'Category:', 'Description:', 'Date:', 'Price:', 'Quantity:', 'Attributes:', 'Supplier:', "Image:"]

        # Display labels and corresponding data
        rows = 1
        for label_text, value in zip(labels, data):
            if label_text == 'Image:':
                display_image(obj, value)  # Call the display_image function
            else:
                Label(obj, text=label_text, font='Arial 10 bold', fg='white', bg=framebg).grid(row=rows, column=0, sticky="w", padx=(10, 0), pady=3)
                Label(obj, text=value, font='Arial 10', bg=framebg, fg='white').grid(row=rows, column=1, sticky="w", padx=0, pady=3)
            rows += 1

        # Button to select the product for making orders
        Button(obj, text="Select for Order", font='Arial 10 bold', bg='#704214', fg='white', command=lambda: submit_order(data, registration_number, product_name)).grid(row=rows, columnspan=2, pady=10)
    else:
        # If data is None, display a message indicating no data found
        Label(root, text="No data found for selected product", font='Arial 10 bold', fg='red').pack()

#################################################################

def on_item_select(event):
    # Get the selected item
    selected_item = treeview.focus()

    # Get the registration number from the selected item
    registration = treeview.item(selected_item, 'values')[0] 

    # Fetch data based on the selected item
    data = fetch_data(registration)

    # Display the fetched data
    select_product_for_order(data)

#################################################################

def refresh_treeview():
    # Clear existing nodes
    for child in treeview.get_children():
        treeview.delete(child)
    
    load_data()

def refresh_label():
    select_product_for_order()

#################################################################

#### HEADER ####

# top frames
label = Label(root, text='Product', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

imageicon4 = PhotoImage(file='images/add.png')
search_button = Button(label, image=imageicon4, bg='#704214', fg='white', font='Helvetica 13 bold', command=add, bd=0)
search_button.pack(side=RIGHT, padx=10, pady=10, anchor="e")

imageicon3 = PhotoImage(file='images/search.png')
search_button = Button(label, image=imageicon3, bg='#704214', fg='white', font='Helvetica 13 bold', command=search, bd=0)
search_button.pack(side=RIGHT, padx=0, pady=10, anchor="e")

# search box
Search = StringVar()
search_entry = Entry(label, textvariable=Search, font='Helvetica 15', bg=framebg, fg='white', bd=0, highlightthickness=1, highlightbackground=framebg)
search_entry.default_text = 'Search'
search_entry.insert(0, search_entry.default_text)
search_entry.bind("<FocusIn>", on_enter)
search_entry.bind("<FocusOut>", on_leave)
search_entry.pack(side=RIGHT, padx=0, pady=10, anchor="e")

# Back button
imageicon1 = PhotoImage(file='images/back_button.png')
back_button = Button(label, image=imageicon1, bg='#704214', border=0, command=back)
back_button.pack(side=LEFT, padx=10, pady=10, anchor="nw")

archive_button = Button(label, text='Archive', width=15, height=2, font='Helvetica 10 bold', bg=framebg, fg='white', command=archive, border=0)
archive_button.pack(side=LEFT, padx=5, pady=0, anchor="e")

#################################################################

###### TABLE #########

frame = Frame(root, bg="#c19a6b", bd=0)
frame.pack(side=LEFT, fill="both", anchor="n")

# Frame for Treeview
f = Frame(frame, bd=0, bg='#704214', relief=GROOVE)
f.pack(side=LEFT, fill="y", anchor="w", padx=(10,0), pady=10)

# Create vertical scrollbar
fscroll = ttk.Scrollbar(f, orient="vertical", style="Vertical.TScrollbar")
fscroll.pack(side="right", fill="y")

# Create horizontal scrollbar
hscroll = ttk.Scrollbar(f, orient="horizontal", style="Horizontal.TScrollbar")
hscroll.pack(side="bottom", fill="x")

cols = ("registration", "name", "price", "quantity")

# Create Treeview widget
treeview = SortableTreeview(f, show="headings", columns=cols, height=12)
treeview.pack(side=TOP, fill="both", anchor="nw", expand=True)

# Configure column width for each column
column_widths = {"registration": 100, "name": 100, "price": 100, "quantity": 100}
for col, width in column_widths.items():
    treeview.column(col, width=width)

# Set scrollbar commands
fscroll.config(command=treeview.yview)
hscroll.config(command=treeview.xview)

# Set headings using SortableTreeview's set_heading method
heading_map = {"registration": "#1", "name": "#2", "price": "#3", "quantity": "#4"}
treeview.set_heading(heading_map)

for col, col_id in heading_map.items():
    treeview.heading(col_id, text=col.title(), anchor=CENTER, command=lambda c=col_id: treeview.sort_by_column(c, False))

load_data()

treeview.bind("<<TreeviewSelect>>", on_item_select)

################################################################

obj = LabelFrame(root, text='Product Details:', font=15, bd=0, width=350, bg=framebg, fg='white', height=270, relief=GROOVE)
obj.pack(side=TOP, anchor="n", padx = 10, pady = 10, fill='x')

# Labels for database fields
labels = ['Product No:', 'Product Name:', 'Category:', 'Description:', 'Date:', 'Price:', 'Quantity:', 'Attributes:', 'Supplier:', 'Image:']

################################################################

 
root.mainloop()