from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import mysql.connector
from subprocess import call
import subprocess

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"

root = Tk()
root.title("Light Track System")
root.geometry("360x640")
root.config(bg = background)
root.resizable(True,True)


    
def Exit():
    root.destroy()

################################################################
    
def showimage():
    global filename
    global img
    filename=filedialog.askopenfilename(initialdir=os.getcwd(), 
                                        title='Select Image File', filetype=(("JPG File", "*.jpg"),
                                                                             ("PNG File", "*.png"),
                                                                             ("All Files", "*.txt")))
    img = (Image.open(filename))
    resized_image = img.resize((100,100))
    photo2 = ImageTk.PhotoImage(resized_image)
    lbl.config(image=photo2)
    lbl.image=photo2

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
        Registration.set(max_registration + 1)
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

    saveButton.config(state = 'normal')

    img1=PhotoImage(file='Images/upload_photo.png')
    lbl.config(image=img1)
    lbl.image=img1

    img=""


################################################################
# top frames
Label(root, text='PRODUCT DETAILS', width=10, font='arial 10 bold', height=3,bg = "#704214", fg="white", anchor=CENTER).pack(side=TOP, fill=X)


#################################################################

Label(root,text='Product No: ', font='arial 10 bold', fg='white', bg=framebg).place(x=10,y=70)
Label(root,text='Last Updated: ', font='arial 10 bold', fg='white', bg=framebg).place(x=155,y=70)

Registration=IntVar()
Date = StringVar()

reg_entry = Label(root, textvariable=Registration, font='arial 10', border=0, bg=framebg, fg='white')
reg_entry.place(x=90, y=72)

product_no()

##################################################################

today = date.today()
d1 = today.strftime("%y/%m/%d")
date_entry = Label(root, textvariable=Date, font='arial 10', border=0, bg=framebg, fg='white')
date_entry.place(x=270, y=72)
Date.set(d1)

##################################################################

obj=LabelFrame(root, text='Product Details:', font=15, bd=2, width=350, bg=framebg, fg='white', height=270, relief=GROOVE)
obj.place(x=5, y=320)

Label(obj, text="Product Name:", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=5)
Label(obj, text="Category:", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=35)
Label(obj, text="Description:", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=65)

Label(obj, text="Price:", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=95)
Label(obj, text="Quantity: ", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=125)
Label(obj, text="Attributes: ", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=155)

Label(obj, text="Supplier: ", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=185)
Label(obj, text="Product Images: ", font='arial 10 bold', bg=framebg, fg='white').place(x=5,y=215)

Name=StringVar()
name_entry = Entry(obj, textvariable=Name, width=20, font='arial 10 bold', bg='white')
name_entry.place(x=160, y=5)

Category=Combobox(obj, values=['Candle', 'Scented Candle', 'Bundle'])
Category.place(x=160, y=35)
Category.set('Select Category')

Description=StringVar()
description_entry = Entry(obj, textvariable=Description, width=20, font='arial 10 bold', bg='white')
description_entry.place(x=160, y=65)

Price=IntVar()
price_entry = Entry(obj, textvariable=Price, width=20, font='arial 10 bold', bg='white')
price_entry.place(x=160, y=95)

Quantity=StringVar()
quanti_entry = Entry(obj, textvariable=Quantity, width=20, font='arial 10 bold', bg='white')
quanti_entry.place(x=160, y=125)

Attributes=StringVar()
attribute_entry = Entry(obj, textvariable=Attributes, width=20, font='arial 10 bold', bg='white')
attribute_entry.place(x=160, y=155)

Supplier=StringVar()
supply_entry = Entry(obj, textvariable=Supplier, width=20, font='arial 10 bold', bg='white')
supply_entry.place(x=160, y=185)

f=Frame(root, bd=3, bg='#704214', width=200, height=200,relief=GROOVE, border=0)
f.place(x=80, y=110)
 
########################################################################

exitButton=Button(root, text='Back', width=15, height=2, font='arial 10 bold', bg='#704214', fg='white', command=Exit,  border=0)
exitButton.place(x=228,y=595)



root.mainloop()