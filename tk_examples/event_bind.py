from tkinter import *
from tkinter import ttk

root = Tk()

lbl = ttk.Label(root, text="Starting...")
lbl.grid()

lbl.bind('<Enter>', lambda e: lbl.configure(text='Moved mouse inside'))
lbl.bind('<Leave>', lambda e: lbl.configure(text='Moved mouse outside'))
lbl.bind('<1>', lambda e: lbl.configure(text='Clicked left mouse button'))
lbl.bind('<Double-1>', lambda e: lbl.configure(text='Double clicked'))
lbl.bind('<B3-Motion>', lambda e: lbl.configure(text='right button drag to %d,%d' % (e.x, e.y)))

root.mainloop()


