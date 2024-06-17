import tkinter as tk
from tkinter import scrolledtext

window = tk.Tk()

text = tk.scrolledtext.ScrolledText(window)
text.pack(padx=10, pady=2)

window.mainloop()

