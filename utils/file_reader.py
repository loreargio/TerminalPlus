def read_file(window_controller, filename: str, divisor: str="", separator: int=0) -> list:
    """
    Reads a csv-style file and processes it according to divisor
    and separator values
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
    except Exception:
        window_controller.write_line(f"Cannot find '{filename}'", line="new")

    new_processed_list = []
    if divisor != "":
        if separator > 0:
            for line_index in range(len(processed_list)):
                split_line = processed_list[line_index].rstrip(";").split(";")
                for i in range(len(split_line)):
                    split_line[i] += " "*(separator-len(split_line[i]))
                new_processed_list.append(divisor.join(split_line))

        return new_processed_list
    else:
        return processed_list