# Version: 0.9
# Author: Miguel Martinez Lopez
# Uncomment the next line to see my email
# print "Author's email: ",
# "61706c69636163696f6e616d656469646140676d61696c2e636f6d".decode("hex")


import tkinter as Tk
import tkinter.font


class AutoResizedText(Tk.Frame):

    def __init__(
            self,
            master,
            width=0,
            height=0,
            family=None,
            size=None,
            *args,
            **kwargs):

        Tk.Frame.__init__(self, master, width=width, height=height)
        self.pack_propagate(False)

        self.min_width = width
        self.min_height = height

        self.Text_widget = Tk.Text(self, *args, **kwargs)
        self.Text_widget.pack(expand=True, fill='both')

        if family is not None and size is not None:
            self.font = tkinter.font.Font(family=family, size=size)
        else:
            self.font = tkinter.font.Font(family=self.Text_widget.cget("font"))

        self.Text_widget.config(font=self.font)

        # I want to insert a tag just in front of the class tag
        # It's not necesseary to guive to this tag extra priority including it at the beginning
        # For this reason I am making this search
        list_of_bind_tags = list(self.Text_widget.bindtags())
        list_of_bind_tags.insert(
            list_of_bind_tags.index('Text'),
            'autoresizetext')

        self.Text_widget.bindtags(tuple(list_of_bind_tags))
        self.Text_widget.bind_class(
            "autoresizetext",
            "<KeyPress>",
            self.update_textbox)

    def update_textbox(self, event):

        if event.keysym == 'BackSpace':
            self.Text_widget.delete("%s-1c" % Tk.INSERT)
            new_text = self.Text_widget.get("1.0", Tk.END)
        elif event.keysym == 'Delete':
            self.Text_widget.delete("%s" % Tk.INSERT)
            new_text = self.Text_widget.get("1.0", Tk.END)
            # We check whether it is a punctuation or normal key
        elif len(event.char) == 1:
            if event.keysym == 'Return':
                # In this situation ord(event.char)=13, which is the CARRIAGE RETURN character
                # We want instead the new line character with ASCII code 10
                new_char = '\n'
            else:
                new_char = event.char

            old_text = self.Text_widget.get("1.0", Tk.END)
            new_text = self.insert_character_into_message(
                old_text,
                self.Text_widget.index(
                    Tk.INSERT),
                new_char)

        else:
            # If it is a special key, we continue the binding chain
            return

        # Tk Text widget always adds a newline at the end of a line
        # This last character is also important for the Text coordinate system
        new_text = new_text[:-1]

        number_of_lines = 0
        widget_width = 0

        for line in new_text.split("\n"):
            widget_width = max(widget_width, self.font.measure(line))
            number_of_lines += 1

        # We need to add this extra space to calculate the correct width
        widget_width += 2 * \
            self.Text_widget['bd'] + 2*self.Text_widget['padx'] + self.Text_widget['insertwidth']

        if widget_width < self.min_width:
            widget_width = self.min_width

        self.Text_widget.configure(height=number_of_lines)
        widget_height = max(
            self.Text_widget.winfo_reqheight(),
            self.min_height)

        self.config(width=widget_width, height=widget_height)

        # If we don't update_idletasks(), the window won't be resized before
        # the insertion
        self.update_idletasks()

        # Finally we insert the new character
        if event.keysym != 'BackSpace' and event.keysym != 'Delete':
            self.Text_widget.insert(Tk.INSERT, new_char)

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

    def focus(self):
        self.Text_widget.focus()

if __name__ == '__main__':
    root = Tk.Tk()
    auto_text = AutoResizedText(
        root,
        family="Arial",
        size=15,
        width=100,
        height=50)
    auto_text.pack()
    auto_text.Text_widget.focus()
    root.mainloop()
