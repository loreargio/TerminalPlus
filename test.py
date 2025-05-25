import curses

def main(screen):
    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    while True:
        key = scr.getch()
        if key == curses.KEY_MOUSE:
            _, mouse_x, mouse_y, _, state = curses.getmouse()
            start_y = 0
            if state == 2:
                start_x, start_y = mouse_x, mouse_y
                scr.addstr(2, 0, f"start y: {start_y}, start x:{start_x}")

            if state == 1:
                end_x, end_y = mouse_x, mouse_y
                scr.addstr(5, 0, f"end y:{end_y}, end x:{end_x}, start y:{start_y}")







curses.wrapper(main)