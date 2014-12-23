# Version: 0.4
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Author's email: ", \
# "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")

# http://code.activestate.com/recipes/578885-draggable-desktop-note-tkinter/
# Inspired by "A-Note": http://a-note.sourceforge.net/
# And based on these tricks:
# https://stackoverflow.com/questions/11544187/tkinter-resize-text-to-contents
# But here I am using my improved version of the automatic resized Text widget:
# https://code.activestate.com/recipes/578886-automatic-resized-text-widget-tkinter/?in=user-4189907
# https://stackoverflow.com/questions/6104991/transparent-colors-tkinter
# Features:
# The note is draggable
# You can minimize the note at the left side of the screen or maximize it
# You can hide the contents of the note
# Please, comment me whether you see some bug.

import tkinter as Tk


class DraggableWindow(object):

    def __init__(self, disable_draggingd=False, release_command=None):
        if not disable_draggingd:
            self.bind('<Button-1>', self.initiate_motion)
            self.bind('<ButtonRelease-1>', self.release_dragging)

        self.release_command = release_command

    def initiate_motion(self, event):
        mouse_x, mouse_y = self.winfo_pointerxy()

        self.deltaX = mouse_x - self.winfo_x()
        self.deltaY = mouse_y - self.winfo_y()

        self.bind('<Motion>', self.drag_window)

    def drag_window(self, event):
        mouse_x, mouse_y = self.winfo_pointerxy()

        new_x = mouse_x - self.deltaX
        new_y = mouse_y - self.deltaY

        if new_x < 0:
            new_x = 0

        if new_y < 0:
            new_y = 0

        self.wm_geometry("+%s+%s" % (new_x, new_y))

    def release_dragging(self, event):
        self.unbind('<Motion>')

        if self.release_command is not None:
            self.release_command()

    def disable_dragging(self):
        self.unbind('<Button-1>')
        self.unbind('<ButtonRelease-1>')
        self.unbind('<Motion>')

    def enable_dragging(self):
        self.bind('<Button-1>', self.initiate_motion)
        self.bind('<ButtonRelease-1>', self.release_dragging)


class AutoResizedText(Tk.Text):

    def __init__(self, *args, **kwargs):
        Tk.Text.__init__(self, *args, **kwargs)

        self.min_width = kwargs.get('width', 0)
        self.min_height = kwargs.get('height', 0)

        self.bindtags(('autoresizetext',)+self.bindtags())
        self.bind_class("autoresizetext", "<KeyPress>", self.update_textbox)

    def update_textbox(self, event):
        widget_width = self.min_width
        widget_height = max(float(self.index(Tk.END)), self.min_height)

        if event.keysym == 'BackSpace':
            self.delete("%s-1c" % Tk.INSERT)
            new_text = self.get("1.0", Tk.END)
        if event.keysym == 'Delete':
            self.delete("%s" % Tk.INSERT)
            new_text = self.get("1.0", Tk.END)
        # We check whether it is a punctuation or normal key
        elif len(event.char) == 1:
            if event.keysym == 'Return':
                new_char = '\n'
            else:
                new_char = event.char
            old_text = self.get("1.0", Tk.END)
            new_text = self.insert_character_into_message(
                old_text,
                self.index(
                    Tk.INSERT),
                new_char)
        else:
            # If it is a special key, we continue the binding chain
            return

        for line in new_text.split("\n"):
            if len(line) > widget_width:
                widget_width = len(line)+1

        self.config(width=widget_width, height=widget_height)
        self.update_idletasks()

        if event.keysym != 'BackSpace' and event.keysym != 'Delete':
            self.insert(Tk.INSERT, new_char)

        return "break"

    def insert_character_into_message(self, message, coordinate, char):
        target_row, target_column = list(map(int, coordinate.split('.')))

        this_row = 1
        this_column = 0
        index = 0

        for ch in message:
            if this_row == target_row and this_column == target_column:
                message = message[:index] + char + message[index:]
                return message

            index += 1

            if ch == '\n':
                this_row += 1
                this_column = 0
            else:
                this_column += 1


class DesktopNote(Tk.Toplevel, DraggableWindow):
    BG_NOTE = '#%02x%02x%02x' % (255, 255, 125)

    def __init__(
            self,
            parent,
            title='Without title',
            min_width=10,
            min_height=3):
        Tk.Toplevel.__init__(self, parent)
        DraggableWindow.__init__(self)

        self.overrideredirect(True)

        self.close_IMG = Tk.PhotoImage(
            data="R0lGODlhEAAQAPAAAAQEBAAAACH5BAEAAAEALAAAAAAQABAAAAImDI6ZFu3/DpxO0mlvBLFX7oEfJo5QZlZNaZTupp2shsY13So6VwAAOw==")
        self.minimize_IMG = Tk.PhotoImage(
            data="R0lGODlhEAAQAPAAAAQEBAAAACH5BAEAAAEALAAAAAAQABAAAAIiDI6ZFu3/DpxO0mlvBBrmbnBg83Wldl6ZgoljSsFYqNRcAQA7")
        self.restore_IMG = Tk.PhotoImage(
            data="R0lGODlhEAAQAPcAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAhFAP8FGEiwYEGB/xIqXLhwIMOHCh02NBgxAEODFhNKjNiwYsWDGQWGxIhQ48iJI09ynLhS48WUB1lCfLhxpkebHTHqtBgQADs=")
        self.minimizeAtRightSide_IMG = Tk.PhotoImage(
            data="R0lGODlhEAAQAPcAAAAAAAQEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAQABAAAAg+AP8FGEiwYEGB/xIqXLhwIMOHCh1CfChxosSKEC8GmJhQI0eBG0F+9MiRpMWQGCmiDPmxI8uWKUuCNEhzY0AAOw==")

        frameNote = Tk.Frame(
            self,
            bg=self.BG_NOTE,
            bd=1,
            highlightbackground='black',
            highlightcolor='black',
            highlightthickness=1)
        frameNote.pack()

        self.mimizedNote = Tk.Label(
            frameNote,
            text=title,
            bg=self.BG_NOTE,
            wraplength=1)
        self.mimizedNote.bind(
            '<Button-1>',
            lambda event: self.maximize_from_right_side())

        self.maximizedNote = Tk.Frame(frameNote)
        self.maximizedNote.pack()

        Header = Tk.Frame(self.maximizedNote, bg=self.BG_NOTE)
        Header.pack(fill=Tk.X)

        HR = Tk.Frame(self.maximizedNote, bg='black', height=1)
        HR.pack(padx=1, fill=Tk.X)

        titleLabel = Tk.Label(Header, text=title, bg=self.BG_NOTE)
        titleLabel.pack(side=Tk.LEFT)

        Tk.Button(
            Header,
            compound=Tk.TOP,
            image=self.close_IMG,
            bg=self.BG_NOTE,
            activebackground=self.BG_NOTE,
            command=self.destroy).pack(
            side=Tk.RIGHT)

        self.iconifyButton = Tk.Button(
            Header,
            image=self.minimize_IMG,
            command=self.minimize,
            bg=self.BG_NOTE,
            activebackground=self.BG_NOTE)
        self.iconifyButton.pack(side=Tk.RIGHT)

        Tk.Button(
            Header,
            compound=Tk.TOP,
            image=self.minimizeAtRightSide_IMG,
            bg=self.BG_NOTE,
            activebackground=self.BG_NOTE,
            command=self.minimize_at_right_side).pack(
            side=Tk.RIGHT)

        self.text_box = AutoResizedText(
            self.maximizedNote,
            bd=0,
            bg=self.BG_NOTE,
            width=min_width,
            height=min_height)
        self.text_box.pack(expand=Tk.YES, fill=Tk.BOTH)

    def minimize_at_right_side(self):
        self.disable_dragging()
        self.maximizedNote.pack_forget()
        self.mimizedNote.pack()

        self.x = self.winfo_x()
        self.y = self.winfo_y()

        self.wm_geometry('-0+%d' % self.y)

    def maximize_from_right_side(self):
        self.maximizedNote.pack()
        self.mimizedNote.pack_forget()
        self.wm_geometry('+%d+%d' % (self.x, self.y))
        self.enable_dragging()

    def minimize(self):
        self.text_box.pack_forget()
        self.iconifyButton['command'] = self.maximize
        self.iconifyButton['image'] = self.restore_IMG

    def maximize(self):
        self.text_box.pack(expand=Tk.YES, fill=Tk.BOTH)
        self.iconifyButton['command'] = self.minimize
        self.iconifyButton['image'] = self.minimize_IMG


class Test(Tk.Tk):

    def __init__(self):
        self.root = Tk.Tk()
        Tk.Label(self.root, text="Title:").pack(side=Tk.LEFT)

        self.title = Tk.StringVar()
        self.title.set('TITLE')

        entry_title = Tk.Entry(self.root, textvariable=self.title)
        entry_title.pack(side=Tk.LEFT)
        entry_title.bind('<Return>', lambda event: self.create_note())

        Tk.Button(
            self.root,
            text="Create another note",
            command=self.create_note).pack(
            side=Tk.LEFT)

        self.create_note()

    def create_note(self):
        New_note = DesktopNote(self.root, self.title.get())
        New_note.text_box.focus()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    Test().run()
