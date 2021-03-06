import tkinter as tk

from pip._vendor.colorama import Fore, Style
from operations.file_operations import AudioData


class MainGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("800x600")
        self.audio_data = AudioData()
        self.__audio_data_record = []
        self.output = tk.Text(self.window)

        self.__update_window()
        self.make_open_file_button()
        self.window.mainloop()

    # Makes a button which, when pressed, opens a window to select an audio file.
    # When an audio file is selected, it then parses the audio file and prints out its data.
    def make_open_file_button(self):
        open_button = tk.Button(self.window, text="Open File", command=lambda: self.__open_button_helper())
        open_button.pack()

    # A helper function which handles what happens when the 'open file' button is pressed.
    def __open_button_helper(self):
        if self.audio_data.audio_segment is not None:
            self.__audio_data_record.append(self.audio_data)
            print(self.__audio_data_record)
        self.audio_data.open_file()
        self.__update_window()

    # Updates the text on the window. Bunch of tkinter stuff going on here.
    def __update_window(self):
        self.output.configure(state="normal")
        self.output.delete('1.0', tk.END)
        self.output.tag_configure("center", justify='center')
        self.__print_scores()
        self.output.tag_add("center", "1.0", "end")
        self.output.configure(state="disabled")
        self.output.pack()

    def __print_scores(self):
        self.output.insert(tk.INSERT, interpret_dr(self.audio_data.dynamic_range))
        self.output.insert(tk.INSERT, interpret_score(self.audio_data.dynamic_range_score))


# Returns a string which interprets the dynamic range it is given.
def interpret_dr(dynamic_range):
    return_string = "The dynamic range of this file is {dr} dB.\n" \
                    "This is {quality}.\n".format(dr=dynamic_range, quality=__dr_assessment(dynamic_range))
    return return_string


def interpret_score(score):
    return_string = "The dynamic range score of this file is {s}. \n" \
                    "This file has {quality} dynamic range.\n".format(s=score, quality=__score_assessment(score))
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


# Returns a string which describes the quality of the audio file based on its dynamic range.
# Coloured text described here. https://ozzmaker.com/add-colour-to-text-in-python/
def __dr_assessment(dynamic_range):
    if 100 <= dynamic_range <= 144:
        return "Hi-Resolution Audio (24-bit)"
    elif 80 <= dynamic_range < 100:
        return "CD Quality (16-bit)"
    elif 60 <= dynamic_range < 80:
        return "Vinyl LP Quality"
    else:
        return "Unknown"
