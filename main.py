from curses.textpad import rectangle
import subprocess
import pathvalidate
from utils.curses_app import *
from utils.table_drawer import *
from utils.mandb import *
from utils.editor import *
from utils.Window import Window


def main(screen):
    command_list = ["edit", "whoami", "close", "table", "clear", "man"]
    screen = create_app()
    rows, cols = screen.getmaxyx()
    main_window = Window((1, 1), rows-2, cols-3)
    window = main_window.get_window()
    rectangle(screen, 0, 0, rows-1, cols-2)
    screen.refresh()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    while True:
        test_line = main_window.get_input_str("Test>")

        in_line = test_line.decode("utf-8").split(" ")
        match in_line[0]:
            case "close":
                break
            case "whoami":
                main_window.write_line(subprocess.getoutput("whoami"), line="new")

            case "table":
                if len(in_line) == 1:
                    main_window.write_line("At least 1 argument required", line="new")
                    continue
                if len(in_line) > 2:
                    main_window.write_line("Cannot use more than 1 argument", line="new")
                    continue

                if pathvalidate.is_valid_filename(in_line[1]):
                    draw_table(window, main_window, in_line[1])
                else:
                    main_window.write_line("Insert a correct text file", line="new")
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
                    main_window.write_line("Please insert the name of a command", line="new")
                    continue
                if len(in_line) > 2:
                    main_window.write_line("Cannot use more than 1 argument", line="new")
                    continue
                if in_line[1] not in command_list:
                    main_window.write_line("Please use a correct command name", line="new")
                    continue

                man = find_man(in_line[1])
                for l in man:
                    main_window.write_line(l, line="new")

            case "edit":
                test_editor(window, main_window)

            case "clear":
                window.clear()


curses.wrapper(main)