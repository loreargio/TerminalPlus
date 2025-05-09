import curses

def create_app():
    screen = curses.initscr()

    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    return screen

def line(scr, text: str, pos: tuple[int, int]):
    scr.addstr(pos[0], pos[1], text)
    curses.echo()
    text_out = scr.getstr()

    return text_out

def find_newline(window) -> int:
    newline = 0
    rows, cols = window.getmaxyx()
    for y in range(rows - 1):
        if len(window.instr(y, 0).decode("utf-8").strip()) == 0:
            newline = y
            break

    return newline

def message(window, text):
    window.addstr(find_newline(window), 0, text)