import tkinter as tk
from tkinter import ttk

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"

root = tk.Tk()
root.title("Light Track System")
root.geometry("640x640")
root.config(bg = background)
root.resizable(False,False)

style = ttk.Style(root)

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.Labelframe(frame, text="Insert Row")
widgets_frame.place(x=5, y=5)

product_name = ttk.Entry(widgets_frame)
product_name.insert(0, "Product Name")
product_name.bind("<FocusIn>", lambda e: product_name.delete('0', 'end'))
product_name.grid(row=0, column=0, sticky="ew")

root.mainloop()