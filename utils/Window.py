import curses
from .curses_app import find_newline
from .file_reader import write_file


class Window:
    def __init__(self, pos: tuple[int, int], rows: int, cols: int):
        self.__pos = pos
        self.__rows = rows
        self.__cols = cols

        self.__window = curses.newwin(self.__rows, self.__cols, self.__pos[1], self.__pos[0])
        #display values
        self.__start_row = 0
        self.__start_column = 0
        self.__end_row = 0
        self.__end_column = 0
        self.__max_row_len = 0
        self.__file_len = 0
        self.__new_curs_x = 0
        self.__new_curs_y = 0

        #mouse selection
        self.__sel_start_y = 0
        self.__sel_end_y = 0
        self.__sel_start_x = 0
        self.__sel_end_x = 0
        self.__sel_begin = 0


    def get_window(self):
        return self.__window

    def write_line(self, text: str, x: int=0, y: int=0, line: str="custom"):
        if line == "custom":
            self.__window.addstr(y, x, str(text))
        elif line == "new":
            self.__window.addstr(find_newline(self.__window), 0, str(text))



    def read_str_input(self, y: int) -> str:
        return self.__window.getstr(y, 0).decode("utf-8")

    def read_line(self, y: int) -> str:
        return self.__window.instr(y, 0).decode("utf-8")

    def get_input_ch(self) -> int:
        self.__window.keypad(True)
        curses.noecho()

        return self.__window.getch()

    def get_input_from_cursor(self, x: int=0, y: int=0, length: int=1):
        curr_y, curr_x = self.get_mouse_pos()
        character = self.__window.instr(curr_y+y, curr_x+x, length)

        return character.decode("utf-8")

    def get_input_str(self, input_text: str):
        self.write_line(input_text, line="new")
        curses.echo()
        text_out = self.__window.getstr()

        return text_out

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


    def initialize_display_values(self, filename: str, text: list[str]=[]):
        self.__max_row_len = 0
        if text == [] and filename != "":
            input_file = []
            with open(filename, "r") as file:
                for line in file.readlines():
                    input_file.append(line.replace("\n", ""))
        else:
            input_file = text
        for line in input_file:
            if len(line.replace("\n", "")) > self.__max_row_len:
                self.__max_row_len = len(line.replace("\n", ""))

        self.__file_len = len(input_file)-1

        if self.__file_len > self.get_win_y():
            self.__end_row = self.get_win_y()
        else:
            self.__end_row = self.__file_len

        if self.__max_row_len > self.get_win_x():
            self.__end_column = self.get_win_x()
        else:
            self.__end_column = self.__max_row_len

        self.__new_curs_y, self.__new_curs_x = self.get_mouse_pos()

    def advanced_display(self, parent_window: curses.window, text: list[str]=[], filename: str=""):
        while True:
            if text == [] and filename != "":
                input_text = []
                with open(filename, "r") as input_file:
                    for line in input_file.readlines():
                        input_text.append(line.replace("\n", ""))
            else:
                input_text = text

            #write text lines
            write_index = 0
            for index, line in enumerate(input_text):
                if index < self.__start_row:
                    continue
                elif index == self.__end_row:
                    break
                else:
                    self.write_line(input_text[index][self.__start_column:self.__end_column], 0, write_index)
                    write_index += 1


            if self.__sel_begin == 1:
                if self.__sel_start_y == self.__sel_end_y:
                    self.__window.chgat(self.__sel_start_y, self.__sel_start_x, self.__sel_end_x - self.__sel_start_x, curses.A_REVERSE)
                else:
                    self.__window.chgat(self.__sel_start_y, self.__sel_start_x, curses.A_REVERSE)
                    for i in range(1, self.__sel_end_y-self.__sel_start_y):
                        self.__window.chgat(self.__sel_start_y+i, 0, curses.A_REVERSE)
                    self.__window.chgat(self.__sel_end_y, 0, self.__sel_end_x, curses.A_REVERSE)
                self.__sel_begin = 0

            self.move_cursor(self.__new_curs_x, self.__new_curs_y)

            input_key = self.get_input_ch()

            arrow_up = 259
            arrow_down = 258
            arrow_left = 260
            arrow_right = 261
            ctrl_x = 24
            enter = 10
            backspace = 263

            curr_y, curr_x = self.get_mouse_pos()

            # exit
            if input_key == ctrl_x:
                self.__window.clear()
                self.__window.touchwin()
                parent_window.refresh()
                parent_window.clear()
                return

            char_pool = list(range(33, 168))
            char_pool.append(176)
            #pressed character
            if input_key in char_pool:
                row_index = self.__start_row + curr_y
                curr_line_index = self.__start_column + curr_x

                if curr_x == len(input_text[row_index]):
                    input_text[row_index] += chr(input_key)
                else:
                    new_line = list(input_text[row_index])
                    new_line.insert(curr_line_index, chr(input_key))
                    input_text[row_index] = "".join(new_line)
                write_file(filename, input_text)
                self.__new_curs_x += 1
                self.__window.clear()


            # pressed enter
            if input_key == enter:
                new_line = self.get_input_from_cursor(length=self.get_win_x() - curr_x).strip(" ")
                file_index = self.__start_row + curr_y
                if new_line == "":
                    input_text.insert(file_index+1, "\n")
                else:
                    input_text.insert(file_index+1, new_line)
                    prev_line = input_text[file_index].split(new_line)

                    input_text.pop(file_index)
                    input_text.insert(file_index, "".join(prev_line))
                write_file(filename, input_text)
                self.__new_curs_y += 1
                self.__window.clear()


            #backspace
            if input_key == backspace:
                row_index = self.__start_row+curr_y
                curr_line_index = self.__start_column+curr_x

                if curr_line_index == 0:
                    if curr_y - 1 > -1:
                        if len(input_text[row_index]) > 0:
                            if input_text[row_index-1] == "":
                                input_text[row_index-1] = input_text[row_index]
                                input_text.pop(row_index)
                            else:
                                input_text[row_index-1] += input_text[row_index]
                                input_text.pop(row_index)
                        else:
                            input_text.pop(row_index)
                else:
                    curr_line = list(input_text[row_index])
                    curr_line.pop(curr_line_index-1)
                    input_text[row_index] = "".join(curr_line)

                write_file(filename, input_text)
                self.__new_curs_x -= 1
                self.__window.clear()


            #mouse click
            if input_key == curses.KEY_MOUSE:
                _, m_x, m_y, _, state = curses.getmouse()
                if state == 4:
                    self.__new_curs_x = m_x-1
                    self.__new_curs_y = m_y - 3

                    self.__sel_start_x = 0
                    self.__sel_start_y = 0
                    self.__sel_end_x = 0
                    self.__sel_end_y = 0
                    self.__window.clear()

                elif state == 2:
                    start_x, start_y = m_x, m_y-3
                    self.__sel_start_x = start_x-1
                    self.__sel_start_y = start_y

                if state == 1:
                    end_x = m_x
                    end_y = m_y-3

                    self.__sel_end_x = end_x
                    self.__sel_end_y = end_y
                    self.__sel_begin = 1


            # move up
            if input_key == arrow_up and curr_y > 0:
                new_y, new_x = self.move_up()
                if new_y - 4 == 3 and self.__start_row > 0:
                    self.__start_row -= 1
                    self.__end_row -= 1
                    self.__window.clear()
                    continue
                self.__new_curs_y = new_y

                if self.read_line(new_y).strip(" ") == "":
                    self.__new_curs_x = 0
                else:
                    self.__new_curs_x = new_x

            # move down
            if input_key == arrow_down and curr_y + 1 < self.get_win_y():
                new_y, new_x = self.move_down()
                if new_y + 4 == self.get_win_y() and self.__end_row <= self.__file_len:
                    self.__start_row += 1
                    self.__end_row += 1
                    self.__window.clear()
                    continue
                self.__new_curs_y = new_y

                if self.read_line(new_y).strip(" ") == "":
                    self.__new_curs_x = 0
                else:
                    self.__new_curs_x = new_x


            # move left
            if input_key == arrow_left and curr_x > 0:
                new_y, new_x = self.move_left()
                if new_x - 4 == 0 and self.__start_column > 0:
                    self.__start_column -= 1
                    self.__end_column -= 1
                    self.__window.clear()
                    continue
                self.__new_curs_y = new_y
                self.__new_curs_x = new_x

            # move right
            if input_key == arrow_right and curr_x < self.get_win_x() - 1:
                new_y, new_x = self.move_right()
                if new_x + 4 == self.get_win_x() and self.__end_column < self.__max_row_len + 1:
                    self.__start_column += 1
                    self.__end_column += 1
                    self.__window.clear()
                    continue
                self.__new_curs_y = new_y
                self.__new_curs_x = new_x



            curr_y, curr_x = self.get_mouse_pos()
            line_len = len(input_text[self.__start_row + curr_y])
            if self.__new_curs_x > line_len:
                self.__new_curs_x = line_len

            if len(input_text[self.__start_row + self.__new_curs_y]) < self.get_win_x():
                if self.__start_column > 0:
                    self.__end_column -= self.__start_column
                    self.__start_column = 0




