"""
Message module.

Provides Message class.
"""


from itertools import chain


class Message():
    """ A game message, as displayed in a message box of a UI. """

    def __init__(self, text, channel):
        self.text = text
        self.channel = channel

    def lines(self, textbox_width):
        """
        Return a list of lines, each shorter than a given width.
        """
        res = self.text.splitlines()
        res = map(lambda s: chunks(s, textbox_width), res)
        res = chain.from_iterable(res)
        res = map(str.rstrip, res)
        return list(res)

    def num_lines(self, textbox_width):
        """
        Return the number of lines this message would occupy if placed into a
        box of given width (assuming monospace font).
        """
        i = 0
        res = 0
        for c in self.text:
            if c == "\n":
                if i != 0:
                    res += 1
                i = 0
                continue
            i += 1
            if i >= textbox_width:
                i = 0
                res += 1
        return res


#--------- helper things ---------#


def chunks(string, chunk_length):
    """ Return a generator of chunks of a given string of given length. """
    i = 0
    final = len(string)
    while i < final:
        yield string[i:i+chunk_length]
        i += chunk_length
