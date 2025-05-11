from .curses_app import find_newline, message
import curses

def test_editor(window):

    rows, cols = window.getmaxyx()
    text_window = curses.newwin(rows-2, cols, 3, 1)
    window.clear()
    test_filename = "prova.txt"
    window.addstr(0, 0, test_filename+"│")
    window.addstr(1, 0,  "─"*len(test_filename)+"┘")

    file = []
    max_row_len = 0
    with open("editor_test.txt", "r") as f:
        for line in f.readlines():
            file.append(line.replace("\n", ""))
            if len(line.replace("\n", "")) > max_row_len:
                max_row_len = len(line.replace("\n", ""))


    start_index = 0
    start_col = 0
    text_win_rows, text_win_cols = text_window.getmaxyx()

    if len(file) > text_win_rows:
        rows_to_show = text_win_rows
    else:
        rows_to_show = len(file)

    if max_row_len > text_win_cols:
        cols_to_show = text_win_cols
    else:
        cols_to_show = max_row_len

    new_curs_y, new_curs_x = text_window.getyx()

    while True:
        # """
        text_window.clear()
        start = 0
        for i in range(start_index, rows_to_show-1):

            if file[i] == "\n":
                text_window.addstr(start, 0, " "*cols)
                start += 1
            else:
                text_window.addstr(start, 0, file[i][start_col:cols_to_show])
                start += 1

        # """



        text_window.move(new_curs_y, new_curs_x)
        text_window.keypad(True)
        curses.noecho()

        key = text_window.getch()

        if key == 24:
            text_window.clear()
            text_window.touchwin()
            window.refresh()
            window.clear()

            return

        curs_y, curs_x = text_window.getyx()

        #move up
        if key == 259 and curs_y > 0:
            text_window.move(curs_y-1, curs_x)

            if(curs_y-1) - 4 == 3:
                if start_index > 0:
                    start_index -= 1
                    rows_to_show -= 1
                    continue

            new_curs_y = curs_y-1
            new_curs_x = curs_x

        #move down
        if key == 258 and curs_y+1 < text_win_rows:
            text_window.move(curs_y+1, curs_x)

            if (curs_y+1) + 4 == text_win_rows:
                if rows_to_show <= len(file):
                    start_index += 1
                    rows_to_show += 1
                    continue

            new_curs_y = curs_y+1
            new_curs_x = curs_x

        #move left
        if key == 260 and curs_x > 0:
            text_window.move(curs_y, curs_x-1)
            if (curs_x-1)-4 == 0:
                if start_col > 0:
                    start_col -= 1
                    cols_to_show -= 1
                    continue
            new_curs_y = curs_y
            new_curs_x = curs_x-1

        #move right
        if key == 261 and curs_x < text_win_cols-1:
            text_window.move(curs_y, curs_x+1)
            if (curs_x+1)+4 == text_win_cols:
                if cols_to_show <= max_row_len:
                    start_col += 1
                    cols_to_show += 1
                    continue
            new_curs_y = curs_y
            new_curs_x = curs_x+1



