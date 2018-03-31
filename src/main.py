#!/usr/bin/python

"""
Main module, contanining game's driver.
"""


import mofloc


import sw.stage.startup as startup
import sw.ui as ui


def main():
    """ Main processing loop. """
    flow = startup.Startup()
    mofloc.execute(flow, startup.ENTRY_POINT, ui.CURSES)


if __name__ == "__main__":
    main()
