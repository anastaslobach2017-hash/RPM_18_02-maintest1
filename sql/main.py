import tkinter as tk
from app import App

root = tk.Tk()

try:

    root.iconbitmap("icon.ico.ico")
except Exception:

    pass

app = App(root)

root.mainloop()