"""
Message module.

Provides Message class.
"""


from itertools import chain


class Message():
    """ A game message, as displayed in a message box of a UI. """

    def __init__(self, text, channel):
        """
        Initialize a game message.

        :param str text: the text of the message.
        :param channel: a channel in which the message should be displayed.
        :type channel: sw.const.message.Channel
        """
        self.text = text
        self.channel = channel

    def lines(self, textbox_width):
        """
        Split the message into lines that would fit into a text box of given
        width.

        :param int textbox_width: the width of the assumed text box.

        :return: a list of lines.
        :rtype: list[str]
        """
        res = self.text.splitlines()
        res = map(lambda s: chunks(s, textbox_width), res)
        res = chain.from_iterable(res)
        res = map(str.rstrip, res)
        return list(res)

    def num_lines(self, textbox_width):
        """
        Calculate the number of lines this message would occupy if placed into
        a box of given width (assuming monospace font).

        :param int textbox_width: the width of the assumed text box.

        :return: number of lines.
        :rtype: int
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
    """
    Split the string into chunks of given or lesser length.

    :param str string: the string to be split.
    :param int chunk_length: maximum length of a chunk.
    """
    i = 0
    final = len(string)
    while i < final:
        yield string[i:i+chunk_length]
        i += chunk_length
