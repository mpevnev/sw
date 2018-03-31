"""
Curses-based character name prompt.
"""


import sw.const as const
import sw.const.ui.char_name_prompt as cnp
import sw.ui as ui
import sw.ui.curses as curses
import sw.event.char_name_prompt as event


class CharNamePrompt(ui.CharNamePrompt):
    """ Character name prompt. """

    def __init__(self, screen, data, default_name):
        super().__init__()
        self.screen = screen
        _, w = self.screen.getmaxyx()
        self.subwin = screen.derwin(1, cnp.TEXTPAD_WIDTH,
                                    cnp.TEXTPAD_AT, (w - cnp.TEXTPAD_WIDTH) // 2)
        self.textbox = curses.Textbox(self.subwin)
        self.data = data
        self.name = default_name

    def draw(self):
        self.screen.erase()
        strings = self.data.strings[const.CHAR_NAME_PROMPT]
        curses.print_centered(self.screen, cnp.TEXTPAD_AT - 1, strings[cnp.PROMPT])
        curses.print_centered(self.screen, cnp.TEXTPAD_AT + 1, strings[cnp.LEAVE_EMPTY])
        self.screen.refresh()
        curses.doupdate()

    def get_event(self):
        self.textbox.edit()
        self.name = self.textbox.gather()
        return (event.NAME_ENTERED, self.name)
