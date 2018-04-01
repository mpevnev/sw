"""
Curses-based character name prompt.
"""


import sw.const.ui.curses.char_name_prompt as cnp
import sw.ui as ui
import sw.ui.curses as curses
import sw.event.char_name_prompt as event


class CharNamePrompt(ui.CharNamePrompt):
    """ Character name prompt. """

    def __init__(self, screen, uidata):
        super().__init__()
        self.screen = screen
        self.uidata = uidata
        _, w = self.screen.getmaxyx()
        textwidth = uidata[cnp.TEXTBOX_WIDTH]
        self.subwin = screen.derwin(1, textwidth,
                                    uidata[cnp.OFFSET] + 1, (w - textwidth) // 2)
        self.textbox = curses.Textbox(self.subwin)

    def draw(self):
        self.screen.erase()
        offset = self.uidata[cnp.OFFSET]
        curses.print_centered(self.screen, offset, self.uidata[cnp.HEADER])
        curses.print_centered(self.screen, offset + 2, self.uidata[cnp.SUBSCRIPT])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        curses.curs_set(1)
        # I dont know why this is needed, at least on my machine backspace
        # doesn't work as expected without this.
        validator = lambda key: 263 if key == 127 else key
        name = self.textbox.edit(validator)
        curses.curs_set(0)
        return (event.NAME_ENTERED, name)
