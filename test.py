import curses





def read_from_file(filename):
    processed_list = []
    with open(filename, "r") as file:
        for line in file.readlines():
            processed_list.append(line.replace("\n", ""))

    return processed_list
max_len = 0
max_cell_len = 0
max_elements = 0

lines = read_from_file("test.txt")
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


# start line ├ ┤

def read_from_file(filename, divisor="", separator=0):
    processed_list = []
    max_elements = 0
    with open(filename, "r") as file:
        for line in file.readlines():
            if len(line.replace("\n", "").rstrip(";").split(";")) > max_elements:
                max_elements = len(line.replace("\n", "").rstrip(";").split(";"))


            if len(line.replace("\n", "").rstrip(";").split(";")) < max_elements:
                processed_list.append(line.replace("\n", "")+" ;")
            else:
                processed_list.append(line.replace("\n", ""))
    new_processed_list = []
    if divisor != "":

        for line in processed_list:
            cell_list = []
            if separator != 0:
                for cell in line.rstrip(";").split(";"):
                    cell_list.append(cell.ljust(separator))
                new_processed_list.append("│".join(cell_list))
            else:
                new_processed_list.append(line.replace(";", divisor))
        return new_processed_list
    else:
        return processed_list

my_list = read_from_file("test.txt")

test_list = ["cat1;cat2;cat3;cat4;cat5;", "1;2;3;4;5;", "test1;test2;test3;test4;"]

test_string = "provaprova"
print(test_string[0:40])





