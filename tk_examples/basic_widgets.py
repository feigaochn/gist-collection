from tkinter import *
from tkinter import ttk

# to use jpg image
from PIL import Image, ImageTk

root = Tk()

# Frame
frame = ttk.Frame(root)
frame.grid()
frame['padding'] = (5,10)
frame['borderwidth'] = 2
frame['relief'] = 'raised' # 'sunken'

# Label
label = ttk.Label(frame, text="full name:")
label.grid()
resultsContents = StringVar()
label['textvariable'] = resultsContents
resultsContents.set('New value to display')
gif = PhotoImage(file='image.gif')
label['image'] = gif
jpg_image = Image.open("small.jpg")
jpg_photo = ImageTk.PhotoImage(jpg_image)
label['image'] = jpg_photo
label.image = jpg_photo



# mainloop
root.mainloop()

