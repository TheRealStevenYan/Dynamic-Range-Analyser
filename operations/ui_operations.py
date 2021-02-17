import tkinter as tk
from operations.file_operations import open_file


audio_data = None


def make_ui():
    window = tk.Tk()
    make_open_file_button(window)
    window.mainloop()


# Makes a button which, when pressed, opens a window to select an audio file.
# When an audio file is selected, it then parses the audio file and prints out its data.
def make_open_file_button(window):
    open_button = tk.Button(window, text="Open File", command=lambda: print_data(open_file()))
    open_button.pack()


def print_data(data):
    global audio_data
    audio_data = data
    if audio_data is not None:
        print(interpret_dr(audio_data.dynamic_range))
        print(interpret_score(audio_data.dynamic_range_score))


# Returns a string which interprets the dynamic range it is given.
def interpret_dr(dynamic_range):
    return_string = "The dynamic range of this file is {dr} dB.\n" \
                    "This is {quality}.".format(dr=dynamic_range, quality=__dr_assessment(dynamic_range))
    return return_string


def interpret_score(score):
    return_string = "The dynamic range score of this file is {s}. \n" \
                    "This file has {quality} dynamic range.".format(s=score, quality=__score_assessment(score))
    return return_string


def __score_assessment(score):
    if score <= 5.5:
        return "poor"
    elif 5.5 < score <= 7:
        return "mediocre"
    elif 7 < score <= 8:
        return "average"
    elif 8 < score <= 9:
        return "good"
    else:
        return "excellent"


# Private helper. Returns a string which describes the quality of the audio file based on its dynamic range.
def __dr_assessment(dynamic_range):
    if 100 <= dynamic_range <= 144:
        return "Hi-Resolution Audio (24-bit)"
    elif 80 <= dynamic_range < 100:
        return "CD Quality (16-bit)"
    elif 60 <= dynamic_range < 80:
        return "Vinyl LP Quality"
