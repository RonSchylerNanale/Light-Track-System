from tkinter import *
import subprocess 
from tkinter import ttk
import tkinter as tk
import pandas as pd
import mysql.connector
from datetime import datetime
from tkinter import simpledialog
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

def Exit():
    root.destroy()

################################################################
    
def back():
    subprocess.Popen(['python', 'lib/menu.py'])
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
    cursor.execute("SELECT id, action, registration_number, product_name, timestamp FROM change_log")

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
        
def export():
    # Connect to MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )

        # Define SQL query to fetch data
        query = "SELECT * FROM change_log"

        # Execute the query and fetch data into a pandas DataFrame
        df = pd.read_sql(query, connection)

        # Prompt the user to select a file name and location
        default_file_name = "Change-Log-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_file_name, filetypes=[("Excel files", "*.xlsx")])

        if filename:
            # Write DataFrame to Excel file
            df.to_excel(filename, index=False)
            messagebox.showinfo("Export Successful", "Data exported to " + filename)

    except mysql.connector.Error as e:
        messagebox.showerror("Error", "Error connecting to MySQL: " + str(e))

    finally:
        if connection.is_connected():
            connection.close()
            
################################################################

def export_to_excel(treeview):
    # Get the data from the Treeview
    items = treeview.get_children("")
    data_list = []
    for item in items:
        item_data = []
        for value in treeview.item(item, "values"):
            item_data.append(value)
        data_list.append(tuple(item_data))

    # Convert data to a DataFrame
    df = pd.DataFrame(data_list, columns=["id", "action", "registration_number", "product_name", "timestamp"])

    # Define the default file name with the current timestamp
    default_file_name = "Current-Page-Log-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"

    # Ask user to choose filename and location
    filename = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=default_file_name, filetypes=[("Excel files", "*.xlsx")])
    if filename:
        # Export DataFrame to Excel
        df.to_excel(filename, index=False)
        print("Data exported to", filename)

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
        query = "SELECT * FROM change_log WHERE LOWER(CONCAT(id, action, registration_number, product_name, timestamp)) LIKE %s"
        cursor.execute(query, ("%" + text + "%",))

        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert matching rows into the Treeview
        for row in cursor.fetchall():
        # Extract specific columns from the row
            id, action, registration_number, product_name, timestamp = row[0], row[1], row[2], row[3], row[4]

        # Insert the extracted values into the Treeview
            treeview.insert("", "end", values=(id, action, registration_number, product_name, timestamp))

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

#### HEADER ####

# Label
label = Label(root, text='Logs', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
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
fscroll = customtkinter.CTkScrollbar(f)
fscroll.pack(side="right", fill="y")

cols = ("id", "action", "registration_number", "product_name", "timestamp")

# Create Treeview widget
treeview = SortableTreeview(f, show="headings", columns=cols, height=12)
treeview.pack(side=TOP, fill="both", anchor="nw", expand=True)

# Add font size of 15
style = ttk.Style()
style.configure("Treeview", font=("TkDefaultFont", 13))

# Configure column width for each column
column_widths = {"id": 70, "action": 70, "registration_number": 70, "product_name": 70, "timestamp": 70}
for col, width in column_widths.items():
    treeview.column(col, width=width)

# Set scrollbar commands
fscroll.configure(command=treeview.yview)

# Set headings using SortableTreeview's set_heading method
heading_map = {"id": "#1", "action": "#2", "registration_number": "#3", "product_name": "#4", "timestamp": "#5"}
treeview.set_heading(heading_map)

for col, col_id in heading_map.items():
    treeview.heading(col_id, text=col.title(), anchor=CENTER, command=lambda c=col_id: treeview.sort_by_column(c, False))

load_data()

################################################################

footer = Label(root,  width=10, font='Helvetica 10 bold', height=3, bg=framebg, fg="white", anchor=CENTER)
footer.pack(side=BOTTOM, fill="x", anchor = "sw")

export_db_button = customtkinter.CTkButton(footer, text='Export Database', fg_color=(buttonsbg), command=export)
export_db_button.pack(side=RIGHT, padx=5, pady=0, anchor="e")

export_page_button = customtkinter.CTkButton(footer, text='Export Current Page', fg_color=(buttonsbg), command=lambda: export_to_excel(treeview))
export_page_button.pack(side=RIGHT, padx=5, pady=0, anchor="e")

###############################################################

root.mainloop()