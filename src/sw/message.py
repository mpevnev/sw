"""
Message module.

Provides Message class.
"""


class Message():
    """ A game message, as displayed in a message box of a UI. """

    def __init__(self, text, channel):
        self.text = text
        self.channel = channel

    def num_lines(self, textbox_width):
        i = 0
        res = 0
        for c in self.text:
            if c == "\n":
                i = 0
                res += 1
                continue
            i += 1
            if i >= textbox_width:
                i = 0
                res += 1
        return res
