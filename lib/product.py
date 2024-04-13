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
 
def Exit():
    root.destroy()

def add():
    subprocess.Popen(['python', 'lib/addproduct.py'])
    root.destroy()

def archive():
    subprocess.Popen(['python', 'lib/archive.py'])
    root.destroy()

def orderlogs():
    subprocess.Popen(['python', 'lib/orderlogs.py'])
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

def refresh_treeview():
    # Clear existing items from the treeview
    for item in treeview.get_children():
        treeview.delete(item)
    load_data()

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

        if text:
            # Execute SQL query to search for the product
            query = "SELECT * FROM products WHERE LOWER(CONCAT(registration, name, price, quantity)) LIKE %s"
            cursor.execute(query, ("%" + text + "%",))
        else:
            # If search text is empty, fetch all products
            cursor.execute("SELECT * FROM products")

        # Clear existing items in the Treeview
        treeview.delete(*treeview.get_children())

        # Insert matching rows into the Treeview
        for row in cursor.fetchall():
            # Extract specific columns from the row
            registration, name, price, quantity = row[0], row[1], row[5], row[6]

            # Insert the extracted values into the Treeview
            treeview.insert("", "end", values=(registration, name, price, quantity))

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

def order_log(registration_number, product_name, amount_ordered, price):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Create order_log table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS order_log (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            registration_number INT NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            amount_sold INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        conn.commit()

        amount_ordered = int(amount_ordered)
        price = float(price)    
        
        # Calculate total price
        total_price = amount_ordered * price

        # Insert log entry into the database
        insert_query = "INSERT INTO order_log (registration_number, product_name, amount_sold, price, total_price) VALUES (%s, %s, %s, %s, %s)"
        data = (registration_number, product_name, amount_ordered, price, total_price)
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
        # Get the amount ordered and price from the Entry widgets
        amount_ordered = amount_entry.get()
        price = int(float(price_entry.get()))
        
        # Add the product to the cart
        add_to_cart(product_data, registration_number, amount_ordered, price)

        log_changes("sold", registration_number, product_name)

        # Close the order window
        order_window.destroy()

    # Create a new Toplevel window for the order
    order_window = Toplevel()
    order_window.title("Make Order")
    order_window.config(bg = background)
    order_window.resizable(True,True)
    
    # Add labels and entry for product name, amount, and price
    Label(order_window, text="Product Name:", bg=framebg, fg='white').grid(row=0, column=0, padx=5, pady=5)
    Label(order_window, text=product_name, bg=framebg, fg='white').grid(row=0, column=1, padx=5, pady=5)

    Label(order_window, text="Amount Ordered:", bg=framebg, fg='white').grid(row=1, column=0, padx=5, pady=5)
    amount_entry = Entry(order_window)
    amount_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(order_window, text="Price:", bg=framebg, fg='white').grid(row=2, column=0, padx=5, pady=5)
    price_entry = Entry(order_window)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    # Add a button to submit the order
    submit_button = Button(order_window, text="Add to Cart", bg="#704214", fg='white', command=submit_order)
    submit_button.grid(row=3, columnspan=2, padx=0, pady=5)

    # Make amount_entry accessible within the function
    submit_order.amount_entry = amount_entry  # Assigning to a function attribute

    # Populate the price entry with the price of the selected item
    price_entry.insert(0, product_data[5])  # Assuming price is at index 5 in product_data

#################################################################

cart_items = []

def add_to_cart(product_data, registration_number, amount_ordered, price):
    # Add the selected product to the cart
    cart_items.append({
        "registration_number": registration_number,
        "product_name": product_data[1],
        "amount_ordered": amount_ordered,
        "price": price
    })
    messagebox.showinfo("Success", "Product added to cart.")

#################################################################

cursor = mydb.cursor()

def display_cart():
    # Create a new window for displaying the cart
    cart_window = Toplevel(root)
    cart_window.title("Cart")
    cart_window.geometry("300x500+600+40")
    cart_window.configure(bg=background)  # Set background color to white

     # Check if cart_items is empty
    if not cart_items:
        Label(cart_window, text="No items added", bg=background, fg="white").pack(padx=10, pady=10)

    # Define a function to handle checkout
    def checkout(registration_number, product_data, amount_ordered, price):

        # Extract product_name from product_data
        product_name = product_data['product_name']
        try:
            # Convert amount_ordered and price to float to ensure correct calculation
            amount_ordered = float(amount_ordered)
            price = float(price)

            # Calculate the total price
            total_price = amount_ordered * price

            # Update the quantity in the products table
            update_query = "UPDATE products SET quantity = quantity - %s WHERE name = %s"
            cursor.execute(update_query, (amount_ordered, product_name))
            mydb.commit()

            # Record the order in the orderlogs table
            insert_query = "INSERT INTO order_log (registration_number, product_name, amount_sold, price, total_price) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (registration_number, product_name, amount_ordered, price, total_price))
            mydb.commit()

            # Display a confirmation message
            confirmation_message = f"Transaction complete!\n\nProduct: {product_name}\nQuantity Ordered: {amount_ordered}\nTotal Price: {total_price}"
            messagebox.showinfo("Transaction Complete", confirmation_message)

            # Close the cart window after checkout
            cart_window.destroy()

        except mysql.connector.Error as error:
            print("Failed to update quantity in the products table or record the order:", error)

    def remove_item_from_cart(item):
        cart_items.remove(item)
        cart_window.destroy()  # Close the current cart window
        display_cart()  # Re-display the cart window with updated items

    # Display cart items with remove button for each item
    for idx, item in enumerate(cart_items):
        item_frame = Frame(cart_window, bg=background)
        item_frame.pack(padx=10, pady=5, fill="x")

        item_label = Label(item_frame, text=f"Item {idx+1}: {item['product_name']} - Quantity: {item['amount_ordered']} - Price: {item['price']}", bg=background)
        item_label.pack(side=LEFT)

        remove_button = Button(item_frame, text="Remove", font='Helvetica 10 bold', bg="RED", fg="White",command=lambda i=item: remove_item_from_cart(i))
        remove_button.pack(side=RIGHT)

    # Define a function to handle checkout for all items
    def checkout_all():
        if not cart_items:
            messagebox.showerror("Error", "No items on cart")
        else:
            for item in cart_items:
                checkout(item['registration_number'], item, item['amount_ordered'], item['price'])
            refresh_treeview()

    # Add a single Checkout button for all items
    submit_button = Button(cart_window, text="Checkout", font='Helvetica 10 bold', bg="green", fg="white", command=checkout_all, bd=0)
    submit_button.pack(side=BOTTOM, padx=10, pady=10)

#################################################################

def archive_product(data):
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = connection.cursor()

        # Move the product details to the archive table
        archive_query = "INSERT INTO archive SELECT * FROM products WHERE name = %s"
        cursor.execute(archive_query, (data[1],))
        connection.commit()

        # Delete the product from the products table
        delete_query = "DELETE FROM products WHERE name = %s"
        cursor.execute(delete_query, (data[1],))
        connection.commit()

        # Show confirmation message
        messagebox.showinfo("Archive Successful", f"{data[1]} has been archived.")

        log_changes("Archived", data[0], data[1])

        refresh_treeview()

    except mysql.connector.Error as error:
        print("Error archiving product:", error)
    finally:
        if 'connection' in locals():
            cursor.close()
            connection.close()

#################################################################

def update_product(data):
    # Create a new window to display the update form
    update_window = Toplevel(root)
    update_window.title("Update Product")
    update_window.configure(bg=background)

    # Labels for attributes that can be updated
    update_labels = ['Product Name:', 'Description:', 'Price:', 'Attributes:', 'Supplier:']
    # Corresponding indices for these attributes in the data
    attribute_indices = [1, 3, 5, 7, 8]

    # Display labels and entry fields for attributes that can be updated
    for i, label_text in enumerate(update_labels):
        Label(update_window, text=label_text, font='Arial 10 bold', bg=background, fg="white").grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = Entry(update_window, font='Arial 10')
        entry.insert(0, data[attribute_indices[i]])  # Fill entry with current value
        entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')

    # Function to handle the update process
    def confirm_update():
        updated_values = [entry.get() for entry in entry_fields]
        registration_number = data[0]  # Assuming registration number is the primary key
        attributes_to_update = ['name', 'description', 'price', 'attributes', 'supplier']
        values_dict = dict(zip(attributes_to_update, updated_values))

        # Establish connection to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = db_connection.cursor()

        # Construct the SQL update statement
        update_query = "UPDATE products SET "
        update_query += ", ".join([f"{attr} = %s" for attr in attributes_to_update])
        update_query += " WHERE registration = %s"

        # Execute the update statement
        cursor.execute(update_query, (*updated_values, registration_number))
        
        # Commit the transaction
        db_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        update_window.destroy()  # Close the update window

        log_changes("Updated", data[0], data[1])

        refresh_treeview()
        
        messagebox.showinfo("Update Successful", "Product updated successfully!")


    # Button to confirm the update
    confirm_button = Button(update_window, text="Update", font='Arial 10 bold', bg='#4287f5', fg='white', command=confirm_update)
    confirm_button.grid(row=len(update_labels), columnspan=2, pady=10)

    entry_fields = [entry for entry in update_window.children.values() if isinstance(entry, Entry)]

    # Main loop for the update window
    update_window.mainloop()

#################################################################

def delete_product_from_database(registration_number):
    try:
        # Establish connection to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = db_connection.cursor()

        # Construct the SQL delete statement
        delete_query = "DELETE FROM products WHERE registration = %s"

        # Execute the delete statement
        cursor.execute(delete_query, (registration_number,))

        # Commit the transaction
        db_connection.commit()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        return True
    except mysql.connector.Error as error:
        print("Error deleting product:", error)
        return False

#################################################################

def delete_product(data):
    registration_number = data[0]
    product_name = data[1]

    confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete '{product_name}'?")

    if confirmation:
        if delete_product_from_database(registration_number):
            messagebox.showinfo("Success", "Product deleted successfully!")
            refresh_treeview()
        else:
            messagebox.showerror("Error", "Failed to delete product!")

#################################################################

def select_product_for_order(data):
    # Assuming data contains product information
    registration_number = data[0]
    product_name = data[1]

    # Check if the Frame widget exists before destroying it
    if 'obj' in globals():
        clear_product_details()

    def fetch_product_from_database(registration_number):
        # Establish connection to the MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = db_connection.cursor()

        # Fetch product information from the database
        cursor.execute("SELECT * FROM products WHERE registration = %s", (registration_number,))
        product_data = cursor.fetchone()

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()

        return product_data

    data = fetch_product_from_database(registration_number)

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

        # Create a frame for buttons
        button_frame = Frame(obj, bg=framebg)
        button_frame.grid(row=rows, column=0, columnspan=3, padx=10, pady=10)

          # Button to select the product for making orders
        Button(button_frame, text="Add to Cart", font='Arial 10 bold', bg='#704214', fg='white', command=lambda: submit_order(data, registration_number, product_name), bd=0).pack(side=LEFT, padx=(0, 5))

        # Button to archive the selected product
        Button(button_frame, text="Archive", font='Arial 10 bold', bg='#FF5733', fg='white', command=lambda: archive_product(data), bd=0).pack(side=LEFT, padx=(0, 5))

        # Button to update the selected product
        Button(button_frame, text="Update", font='Arial 10 bold', bg='#4287f5', fg='white', command=lambda: update_product(data), bd=0).pack(side=LEFT, padx=(5, 0))

        # Button to restock the selected product
        Button(button_frame, text="Restock", font='Arial 10 bold', bg='#1E8449', fg='white', command=lambda: restock_product(data), bd=0).pack(side=LEFT, padx=(5, 0))

        # Button to delete the selected product
        Button(button_frame, text="Delete", font='Arial 10 bold', bg='#FF5733', fg='white', command=lambda: delete_product(data), bd=0).pack(side=LEFT, padx=(5, 0))

    else:
        # If data is None, display a message indicating no data found
        Label(root, text="No data found for selected product", font='Arial 10 bold', fg='red').pack()

#################################################################

def restock_product(data):
    # Function to handle restocking of the selected product
    quantity_to_add = simpledialog.askinteger("Restock Product", "Enter the quantity to restock:")
    if quantity_to_add is not None and quantity_to_add > 0:
        try:
            # Establish MySQL connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="LTS",
                port=3306
            )
            cursor = connection.cursor()

            # Update the quantity in the database
            update_query = "UPDATE products SET quantity = quantity + %s WHERE name = %s"
            cursor.execute(update_query, (quantity_to_add, data[1]))
            connection.commit()

            # Show confirmation message
            messagebox.showinfo("Restock Successful", f"{quantity_to_add} units added to {data[1]}.")
        
            refresh_treeview()

        except mysql.connector.Error as error:
            print("Error updating quantity:", error)
        finally:
            if 'connection' in locals():
                cursor.close()
                connection.close()

#################################################################
        
def on_item_select(event):
    # Get the selected item
    selected_item = treeview.focus()

    # Check if there's a selected item
    if selected_item:
        # Get the registration number from the selected item
        values = treeview.item(selected_item, 'values')
        if values:
            registration = values[0]
    
            # Fetch data based on the selected item
            data = fetch_data(registration)
    
            select_product_for_order(data)
        else:
            print("No values associated with the selected item")
    else:
        print("No item selected")

#################################################################
    
# Function to check product quantities and show restock button if necessary
def check_quantity():
    # Connect to MySQL database
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        # Query to get products with quantity <= 20
        cursor.execute("SELECT name FROM products WHERE quantity <= 20")
        products_to_restock = cursor.fetchall()

        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")

#################################################################

def show_restock_list():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LTS",
            port=3306
        )
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM products WHERE quantity <= 20")
        products_to_restock = cursor.fetchall()

        # Create Tkinter window
        window = Toplevel(root)
        window.title("Products to Restock")
        window.geometry("300x500+600+40")
        window.configure(bg=background)

        if not products_to_restock:
            restock_label = Label(window, text="No products need restocking.", bg=background, fg='white')
            restock_label.pack(padx=5, pady=5)
        else:
            restock_list = "\n".join([product[0] for product in products_to_restock])
            restock_label = Label(window, text=f"These products need to be restocked:\n{restock_list}")
            restock_label.pack(padx=5, pady=5)

        conn.close()

        # Run Tkinter event loop
        window.mainloop()

    except mysql.connector.Error as e:
        error_window = Tk()
        error_window.title("Error")
        error_label = Label(error_window, text=f"Error connecting to database: {e}")
        error_label.pack()
        error_window.mainloop()

# Check quantity when the window is loaded
check_quantity()

#################################################################

#### HEADER ####

# top frames
label = Label(root, text='Product', width=10, font='Helvetica 10 bold', height=3, bg="#704214", fg="white", anchor=CENTER)
label.pack(side=TOP, fill="x", anchor = "nw")

# Load the original images
imageicon1 = Image.open('images/back_button.png')
imageicon3 = Image.open('images/search.png')
imageicon4 = Image.open('images/add.png')
imageicon5 = Image.open('images/cart.png')
imageicon6 = Image.open('images/alert.png')

# Resize the images to 30x30 pixels
imageicon3 = imageicon3.resize((30, 30))
imageicon4 = imageicon4.resize((30, 30))
imageicon5 = imageicon5.resize((30, 30))
imageicon6 = imageicon6.resize((30, 30))

# Convert the images to PhotoImage objects
imageicon1 = ImageTk.PhotoImage(imageicon1)
imageicon3 = ImageTk.PhotoImage(imageicon3)
imageicon4 = ImageTk.PhotoImage(imageicon4)
imageicon5 = ImageTk.PhotoImage(imageicon5)
imageicon6 = ImageTk.PhotoImage(imageicon6)

# Now use these resized images in your buttons
back_button = Button(label, image=imageicon1, bg='#704214', border=0, command=back)
back_button.pack(side=LEFT, padx=10, pady=5, anchor="nw")

search_button = Button(label, image=imageicon3, bg='#704214', fg='white', font='Helvetica 13 bold', command=search, bd=0)
search_button.pack(side=LEFT, padx=0, pady=5, anchor="e")

add_button = Button(label, image=imageicon4, bg='#704214', fg='white', font='Helvetica 13 bold', command=add, bd=0)
add_button.pack(side=RIGHT, padx=10, pady=5, anchor="e")

view_cart_button = Button(label, image=imageicon5, command=display_cart, bg='#704214', fg='white', bd=0)
view_cart_button.pack(side=RIGHT, padx=0, pady=5, anchor="e")

restock_button = Button(label, image=imageicon6, bg='#704214', fg='white',command=show_restock_list, bd=0)
restock_button.pack(side=RIGHT, padx=10, pady=5, anchor="e")


# search box
Search = StringVar()
search_entry = Entry(label, textvariable=Search, font='Helvetica 15', bg=framebg, fg='white', bd=0, highlightthickness=1, highlightbackground=framebg)
search_entry.default_text = 'Search'
search_entry.insert(0, search_entry.default_text)
search_entry.bind("<FocusIn>", on_enter)
search_entry.bind("<FocusOut>", on_leave)
search_entry.pack(side=LEFT, padx=0, pady=10, anchor="e")

orderhistory_button = Button(label, text='Order History', width=10, height=1, font='Helvetica 10 bold', bg=framebg, fg='white', command=orderlogs, border=0)
orderhistory_button.pack(side=RIGHT, padx=5, pady=0, anchor="e")

archive_button = Button(label, text='Archive', width=10, height=1, font='Helvetica 10 bold', bg=framebg, fg='white', command=archive, border=0)
archive_button.pack(side=RIGHT, padx=5, pady=0, anchor="e")

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