import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog

class HamburgerMenu(tk.Menu):
    def __init__(self, parent, treeview, **kwargs):
        super().__init__(parent, **kwargs)
        self.treeview = treeview
        self.add_command(label="Filter", command=self.filter_treeview)
    
    def filter_treeview(self):
        keyword = simpledialog.askstring("Filter", "Enter keyword to filter:")
        if keyword:
            self.treeview.delete(*self.treeview.get_children())
            for item in data:
                if keyword.lower() in item.lower():
                    self.treeview.insert("", "end", values=item)

data = ["Apple", "Banana", "Orange", "Pineapple", "Grapes", "Kiwi", "Watermelon"]

def main():
    root = tk.Tk()
    root.title("Hamburger Menu Example")
    root.geometry("400x300")

    treeview = ttk.Treeview(root, columns=("Values"), show="headings")
    treeview.heading("Values", text="Values")
    for item in data:
        treeview.insert("", "end", values=item)
    treeview.pack(fill="both", expand=True)

    menubar = tk.Menu(root)
    root.config(menu=menubar)
    file_menu = HamburgerMenu(menubar, treeview, tearoff=0)
    menubar.add_cascade(label="Menu", menu=file_menu)

    root.mainloop()

if __name__ == "__main__":
    main()
