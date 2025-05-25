from .Window import Window


def test_editor(window, window_controller):

    rows, cols = window.getmaxyx()
    editor = Window((1, 3), rows-2, cols)


    window.clear()
    my_file = "editor_test.txt"

    window_controller.write_line(my_file+"│", 0, 0, "custom")
    window_controller.write_line("─"*len(my_file)+"┘", 0, 1, "custom")
    window.refresh()


    editor.initialize_display_values(filename=my_file, text=[])

    editor.advanced_display(text=[], filename=my_file, parent_window=window)

