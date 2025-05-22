def read_file(window_controller, filename: str, divisor: str="", separator: int=0) -> list:
    """
    Reads a csv-style file and processes it according to divisor
    and separator values
    :param window_controller: The controller of the window
    :param filename: The name of the file
    :param divisor: The divisor between the single-line values
    :param separator: The space that the single-line values has to occupy
    :return: A processed list
    """
    processed_list = []
    max_elements = 0
    try:
        with open(filename, "r") as file:
            for line in file.readlines():
                stripped_line = line.replace("\n", "").rstrip(";")

                if len(stripped_line.split(";")) > max_elements:
                    max_elements = len(stripped_line.split(";"))

                if len(stripped_line.split(";")) < max_elements:
                    processed_list.append(line.replace("\n", "")+" ;")
                else:
                    processed_list.append(line.replace("\n", ""))
    except FileNotFoundError:
        window_controller.write_line(f"Cannot find '{filename}'", line="new")

    new_processed_list = []
    if divisor != "":
        for line_index in range(len(processed_list)):
            split_line = processed_list[line_index].rstrip(";").split(";")
            for i in range(len(split_line)):
                split_line[i] += " "*(separator-len(split_line[i]))
            new_processed_list.append(divisor.join(split_line))

        return new_processed_list
    else:
        return processed_list

def write_file(filename, file_input):
    new_file = []
    for line in file_input:
        if line[-2:] != "\n":
            new_file.append(line+"\n")
        else:
            new_file.append(line)

    with open(filename, "w") as file:
        file.writelines(new_file)

