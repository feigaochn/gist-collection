# run in interactive mode!!

from tkinter import *
from tkinter import ttk

root = Tk()

# create a button in root
button = ttk.Button(root, text='hello', command='buttonpressed')

# put it on screen; otherwise nothing shows!
button.grid()

# check value of option:
print(button['text'])
# change value of option:
button['text'] = 'goodbye'

# get all info about the text option:
print(button.configure('text'))
# ('text', 'text', 'Text', '', 'goodbye')


# get info on all options for this widget:
print(button.configure())
# {'cursor': ('cursor', 'cursor', 'Cursor', '', ''), 'style': ('style', 'style', 'Style', '', ''),
# 'default': ('default', 'default', 'Default', <index object at 0x00DFFD10>, <index object at 0x00DFFD10>),
# 'text': ('text', 'text', 'Text', '', 'goodbye'), 'image': ('image', 'image', 'Image', '', ''),
# 'class': ('class', '', '', '', ''), 'padding': ('padding', 'padding', 'Pad', '', ''),
# 'width': ('width', 'width', 'Width', '', ''),
# 'state': ('state', 'state', 'State', <index object at 0x0167FA20>, <index object at 0x0167FA20>),
# 'command': ('command', 'command' , 'Command', '', 'buttonpressed'),
# 'textvariable': ('textvariable', 'textVariable', 'Variable', '', ''),
# 'compound': ('compound', 'compound', 'Compound', <index object at 0x0167FA08>, <index object at 0x0167FA08>),
# 'underline': ('underline', 'underline', 'Underline', -1, -1),
# 'takefocus': ('takefocus', 'takeFocus', 'TakeFocus', '', 'ttk::takefocus')}


root.mainloop()
