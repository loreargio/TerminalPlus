def find_man(command_name):
    manual = []
    with open("mandb.txt", "r") as man:
        while True:
            line = man.readline()
            if len(line) == 0:
                break
            if line.rstrip(":\n") == command_name:
                continue
            if line.rstrip("\n") == "end!":
                break
            manual.append(line)
    return manual
