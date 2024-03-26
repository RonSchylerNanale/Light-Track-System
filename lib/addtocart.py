import tkinter as tk

class ShoppingCartApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Shopping Cart")
        
        self.items = []
        
        self.item_label = tk.Label(master, text="Items in Cart:")
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

def main():
    root = tk.Tk()
    app = ShoppingCartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
