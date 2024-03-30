from tkinter import *
import tkinter as tk

background = "#c19a6b"
framebg = "#c19a6b"
framefg = "#c19a6b"

class ShoppingCartApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shopping Cart")
        
        self.items = []
        
        self.item_label = tk.Label(master, text="Items in Cart:", bg=background)
        self.item_label.pack()
        
        self.item_listbox = tk.Listbox(master, height=10)
        self.item_listbox.pack()
        
        self.add_to_cart_button = tk.Button(master, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.pack()
        
        self.show_cart_button = tk.Button(master, text="Show Cart", command=self.show_cart)
        self.show_cart_button.pack()
        
        self.clear_cart_button = tk.Button(master, text="Clear Cart", command=self.clear_cart)
        self.clear_cart_button.pack()
        
    def add_to_cart(self):
        item = "Item" + str(len(self.items) + 1)  # Just a placeholder item name
        self.items.append(item)
        self.item_listbox.insert(tk.END, item)
        
    def show_cart(self):
        cart_window = tk.Toplevel(self.master)
        cart_window.title("Cart Contents")
        
        cart_label = tk.Label(cart_window, text="Items in Cart:")
        cart_label.pack()
        
        cart_listbox = tk.Listbox(cart_window, height=10)
        cart_listbox.pack()
        
        for item in self.items:
            cart_listbox.insert(tk.END, item)
        
    def clear_cart(self):
        self.items.clear()
        self.item_listbox.delete(0, tk.END)

root = Tk()
root.title("Light Track System")
root.geometry("800x600+0+0")
root.config(bg=background)
root.resizable(True,True)

app = ShoppingCartApp(root)
root.mainloop()
