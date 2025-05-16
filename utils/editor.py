from .curses_app import find_newline, message
import curses
from .Window import Window



def test_editor(window):

    rows, cols = window.getmaxyx()
    editor_window = Window((1, 3), rows-2, cols)
    text_window = editor_window.get_window()

    window.clear()
    test_filename = "prova.txt"
    window.addstr(0, 0, test_filename+"│")
    window.addstr(1, 0,  "─"*len(test_filename)+"┘")
    window.refresh()

    file = []
    max_row_len = 0
    with open("editor_test.txt", "r") as f:
        for line in f.readlines():
            if line != "\n":
                file.append(line.replace("\n", ""))
            else:
                file.append(line)
            if len(line.replace("\n", "")) > max_row_len:
                max_row_len = len(line.replace("\n", ""))
    file_len = len(file)


    if file_len > editor_window.get_win_y():
        end_row = editor_window.get_win_y()
    else:
        end_row = file_len


    if max_row_len > editor_window.get_win_x():
        end_column = editor_window.get_win_x()
    else:
        end_column = max_row_len

    new_curs_y, new_curs_x = editor_window.get_mouse_pos()


    start_row = 0
    start_column = 0

    while True:

        editor_window.advanced_display(text=[],
                                        start_row=start_row,
                                        end_row=end_row,
                                        start_column=start_column,
                                        end_column=end_column,
                                        filename="editor_test.txt")



        editor_window.move_cursor(new_curs_x, new_curs_y)

        key = editor_window.get_input()

        # exit
        if key == 24:
            text_window.clear()
            text_window.touchwin()
            window.refresh()
            window.clear()
            return

        # pressed enter
        if key == 10:
            pass


        curs_y, curs_x = editor_window.get_mouse_pos()

        #move up
        if key == 259 and curs_y > 0:
            new_y, new_x = editor_window.move_up()
            if new_y-4 == 3 and start_row > 0:
                start_row -= 1
                end_row -= 1
                text_window.clear()
                continue
            new_curs_y = new_y
            new_curs_x = new_x


        #move down
        if key == 258 and curs_y+1 < editor_window.get_win_y():
            new_y, new_x = editor_window.move_down()
            if new_y+4 == editor_window.get_win_y() and end_row <= file_len:
                start_row += 1
                end_row += 1
                text_window.clear()
                continue
            new_curs_y = new_y
            new_curs_x = new_x


        #move left
        if key == 260 and curs_x > 0:
            new_y, new_x = editor_window.move_left()
            if new_x-4 == 0 and start_column > 0:
                start_column -= 1
                end_column -= 1
                text_window.clear()
                continue
            new_curs_y = new_y
            new_curs_x = new_x


        #move right
        if key == 261 and curs_x < editor_window.get_win_x()-1:
            new_y, new_x = editor_window.move_right()
            if new_x+4 == editor_window.get_win_x() and end_column <= max_row_len:
                start_column += 1
                end_column += 1
                text_window.clear()
                continue
            new_curs_y = new_y
            new_curs_x = new_x

