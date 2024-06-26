from tkinter import *
import subprocess 
from tkinter import ttk
import tkinter as tk
import pandas as pd
import mysql.connector
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog
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

################################################################

################################################################
    
def back():
    subprocess.Popen(['python', 'lib/product.py'])
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
    cursor.execute("SELECT registration, name, category, description, date, price, quantity, attributes, supplier FROM archive")

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
        treeview.insert('', tk.END, values=row)

################################################################
        
################################################################

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
        query = "SELECT * FROM archive WHERE LOWER(CONCAT(registration, name, category, description, date, price, quantity, attributes, supplier)) LIKE %s"
        cursor.execute(query, ("%" + text + "%",))

        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert matching rows into the Treeview
        for row in cursor.fetchall():
        # Extract specific columns from the row
            registration, name, category, description, date, price, quantity, attributes, supplier, image = row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],row[8], row[9]

        # Insert the extracted values into the Treeview
            treeview.insert("", "end", values=(registration, name, category, description, date, price, quantity, attributes, supplier))

    except mysql.connector.Error as e:
        print("Error:", e)
        messagebox.showerror('Error', 'Failed to search product.')

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

################################################################

def refresh_treeview():
    # Clear existing items from the treeview
    for item in treeview.get_children():
        treeview.delete(item)
    load_data()

################################################################

def unarchive():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a product to unarchive.")
        return

    registration = treeview.item(selected_item)['values'][0]
    
    # Connect to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LTS",
        port=3306
    )
    cursor = conn.cursor()

    # Fetch the product details from the archive table
    cursor.execute("SELECT * FROM archive WHERE registration=%s", (registration,))
    archived_product = cursor.fetchone()

    if not archived_product:
        messagebox.showerror("Error", "Selected product not found in archive.")
        return

    # Insert the archived product into the active table
    insert_query = "INSERT INTO products (registration, name, category, description, date, price, quantity, attributes, supplier, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(insert_query, archived_product[:10])
    conn.commit()

    # Delete the product from the archive table
    delete_query = "DELETE FROM archive WHERE registration=%s"
    cursor.execute(delete_query, (registration,))
    conn.commit()

    # Log the unarchive action
    log_changes("Unarchived", registration, archived_product[1])

    refresh_treeview()

    conn.close()
    messagebox.showinfo("Success", "Product has been unarchived successfully.")

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
                 
def on_enter(e):
    search_entry.delete(0, 'end')

def on_leave(e):
    name=search_entry.get()
    if name=='':
        search_entry.insert(0, 'Search')

################################################################
        
    
#### HEADER ####

# Label
label = Label(root, text='Archive', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

# Search button
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

# Back button
imageicon1 = PhotoImage(file='images/back_button.png')
back_button = Button(label, image=imageicon1, bg='#704214', border=0, command=back)
back_button.pack(side=LEFT, padx=10, pady=10, anchor="nw")

################################################################

###### TABLE #########

frame = customtkinter.CTkFrame(root, fg_color=(framebg))
frame.pack(side=TOP, fill="both", anchor="n", expand=True)

# Frame for Treeview
f = customtkinter.CTkFrame(frame, fg_color=(framebg))
f.pack(side=TOP, fill="both",pady=10,padx=10, anchor="nw", expand=True)

# Create vertical scrollbar
fscroll = customtkinter.CTkScrollbar(f, fg_color=(framebg))
fscroll.pack(side="right", fill="y")

cols = ("registration", "name", "category", "description", "date", "price", "quantity", "attributes", "supplier")

# Create Treeview widget
treeview = SortableTreeview(f, show="headings", columns=cols, height=12)
treeview.pack(side=TOP, fill="both", anchor="nw", expand=True)

# Add font size of 15
style = ttk.Style()
style.configure("Treeview", font=("TkDefaultFont", 13))

# Configure column width for each column
column_widths = {"registration": 70, "name": 70, "category": 70, "description": 70, "date": 70, "price": 70, "quantity": 70, "attributes": 70, "supplier": 70}
for col, width in column_widths.items():
    treeview.column(col, width=width)

# Set scrollbar commands
fscroll.configure(command=treeview.yview)

# Set headings using SortableTreeview's set_heading method
heading_map = {"registration": "#1", "name": "#2", "category": "#3", "description": "#4", "date": "#5", "price": "#6", "quantity": "#7", "attributes": "#8", "supplier": "#9"}
treeview.set_heading(heading_map)

for col, col_id in heading_map.items():
    treeview.heading(col_id, text=col.title(), anchor=CENTER, command=lambda c=col_id: treeview.sort_by_column(c, False))

load_data()

################################################################

footer = Label(root,  width=10, font='Helvetica 10 bold', height=3, bg=framebg, fg="white", anchor=CENTER)
footer.pack(side=BOTTOM, fill="x", anchor = "sw")

# Export buttons

unarchive_button = customtkinter.CTkButton(footer, text="Unarchive", fg_color=('#704214'), command=unarchive)#, width=15, height=2, font='Helvetica 10 bold', bg='#704214', fg='white', command=unarchive, border=0)
unarchive_button.pack(side=RIGHT, padx=5, pady=0, anchor="e")

###############################################################

root.mainloop()