from .file_reader import read_file

def draw_table(window, window_controller , file):
    max_len = 0
    max_cell_len = 0
    max_elements = 0

    lines = read_file(window_controller, file)
    if not lines:
        return 0
    for line in lines:
        stripped_line = line.rstrip(";")
        line_len = len(stripped_line)

        if line_len > max_len:
            max_len = line_len

        if len(stripped_line.split(";")) > max_elements:
            max_elements = len(stripped_line.split(";"))

        for cell in stripped_line.split(";"):
            if len(cell) > max_cell_len:
                max_cell_len = len(cell) + 1


    def draw_first_line(window_controller, max_cell_len, max_elements):
        first_line = ("┌" + ((("─" * max_cell_len) + "┬") * max_elements) + "┐").rstrip("┬")
        window_controller.write_line(first_line, line="new")

    def draw_last_line(window_controller, max_cell_len, max_elements):
        last_line = ("└" + ((("─" * max_cell_len) + "┴")*max_elements) + "┘").rstrip("┴")
        window_controller.write_line(last_line, line="new")

    draw_first_line(window_controller, max_cell_len, max_elements)
    for index in range(len(lines)*2-1):
        if index % 2 == 0:
            new_lines = read_file(window, file, divisor="│", separator=max_cell_len)
            value_lines = "│" + new_lines[int(index / 2)] + "│"
            window_controller.write_line(value_lines, line="new")

        elif index % 2 == 1:
            middle_line = ("├" + ((("─" * max_cell_len) + "┼")*max_elements) + "┤").rstrip("┼")
            window_controller.write_line(middle_line, line="new")
    draw_last_line(window_controller, max_cell_len, max_elements)