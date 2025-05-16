import curses
from .curses_app import find_newline

class Window:
    def __init__(self, pos: tuple[int, int], rows: int, cols: int):
        self.__pos = pos
        self.__rows = rows
        self.__cols = cols

        self.__window = curses.newwin(self.__rows, self.__cols, self.__pos[1], self.__pos[0])

    def get_window(self):
        return self.__window

    def write_line(self, text: str, x: int=0, y: int=0, line: str="custom"):
        if line == "custom":
            self.__window.addstr(y, x, str(text))
        elif line == "new":
            self.__window.addstr(find_newline(self.__window), 0, str(text))



    def read_line(self, y: int) -> str:
        return self.__window.getstr(y, 0).decode("utf-8")

    def get_input(self) -> int:
        self.__window.keypad(True)
        curses.noecho()

        return self.__window.getch()

    def get_mouse_pos(self) -> tuple[int, int]:
        return self.__window.getyx()

    def move_down(self):
        y, x = self.get_mouse_pos()
        return y+1, x

    def move_up(self):
        y, x = self.get_mouse_pos()
        return y-1, x

    def move_left(self):
        y, x = self.get_mouse_pos()
        return y, x-1

    def move_right(self):
        y, x = self.get_mouse_pos()
        return y, x+1

    def get_win_x(self) -> int:
        _, x = self.__window.getmaxyx()
        return x

    def get_win_y(self) -> int:
        y, _ = self.__window.getmaxyx()
        return y

    def move_cursor(self, x: int, y: int):
        self.__window.move(y, x)

    def advanced_display(self, text: list[str]=[], start_row: int=0, end_row: int=0, start_column: int=0, end_column: int=0, filename: str=""):
        if text == [] and filename != "":
            input_text = []
            with open(filename, "r") as input_file:
                for line in input_file.readlines():
                    if line != "\n":
                        input_text.append(line.replace("\n", ""))
                    else:
                        input_text.append(line)
        else:
            input_text = text

        write_index = 0
        for index in range(start_row, end_row-1):
            if input_text[index] == "\n":
                self.write_line(" "*(self.get_win_x()-1), 0, write_index)
            else:
                self.write_line(input_text[index][start_column:end_column], 0, write_index)
            write_index += 1