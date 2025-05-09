import curses
import curses.textpad
from curses.textpad import rectangle
import subprocess
import pathvalidate
from utils.curses_app import *
from utils.file_reader import *
from utils.table_drawer import *
from utils.mandb import *


def main(screen):
    command_list = ["whoami", "close", "table", "clear", "man"]
    screen = create_app()
    rows, cols = screen.getmaxyx()
    window = curses.newwin(rows-2, cols-3, 1, 1)
    rectangle(screen, 0, 0, rows-1, cols-2)
    screen.refresh()

    start_x = 0
    while True:

        test_line = line(window, "Test> ", (find_newline(window), start_x))

        in_line = test_line.decode("utf-8").split(" ")
        match in_line[0]:
            case "close":
                break
            case "whoami":
                window.addstr(find_newline(window), 0, subprocess.getoutput("whoami"))
            case "table":
                if len(in_line) == 1:
                    message(window, "At least 1 argument required")
                    continue
                if len(in_line) > 2:
                    message(window, "Cannot use more than 1 argument")
                    continue

                if pathvalidate.is_valid_filename(in_line[1]):
                    draw_table(window, in_line[1])
                else:
                    message(window, "Insert a correct text file")
                    continue
            case "table-chars":
                window.addch(curses.ACS_HLINE)
                window.addch(curses.ACS_VLINE)
                window.addch("/")
                window.addch(curses.ACS_TTEE)
                window.addch(curses.ACS_BTEE)
                window.addch(curses.ACS_LTEE)
                window.addch(curses.ACS_RTEE)
                window.addch("/")
                window.addch(curses.ACS_PLUS)
                window.addch("/")
                window.addch(curses.ACS_LLCORNER)
                window.addch(curses.ACS_LRCORNER)
                window.addch(curses.ACS_ULCORNER)
                window.addch(curses.ACS_URCORNER)
            case "man":
                if len(in_line) == 1:
                    message(window, "Please insert the name of a command")
                    continue
                if len(in_line) > 2:
                    message(window, "Cannot use more than 1 argument")
                    continue
                if in_line[1] not in command_list:
                    message(window, "Please use a correct command name")
                    continue
                man = find_man(in_line[1])
                for l in man:
                    message(window, l)
            case "clear":
                window.clear()


curses.wrapper(main)