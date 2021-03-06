import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import operations.number_operations as op


# A class containing the data of the selected file. Used for saving / loading / printi
class AudioData:
    # Constructor. Initialises a blank AudioData class.
    def __init__(self):
        self.dynamic_range = 0
        self.dynamic_range_score = 0
        self.audio_segment = None
        self.array_of_samples = []
        self.file_path = ""

    # Opens a file, and initialises all the attributes in the AudioData class based on the file.
    def open_file(self):
        self.file_path = tk.filedialog.askopenfilename()
        try:
            self.__get_audio_segment()
            self.__calculate_data()
        except Exception as e:
            print(e)

    # Accepts a path to an input file, and then returns it as an AudioSegment.
    # Throws exception if not found. Remember to catch this exception.
    def __get_audio_segment(self):
        file_ext = os.path.splitext(self.file_path)[1]
        file_ext = file_ext[1:len(file_ext)]
        self.audio_segment = AudioSegment.from_file(self.file_path, format=file_ext)

    # Helper function.
    # Calculates the required data (dynamic range etc) from the given array of samples.
    # Creates an AudioData object with the required data as attributes.
    def __calculate_data(self):
        self.array_of_samples = self.audio_segment.get_array_of_samples()
        data_max, data_min = op.get_max_and_min(self.array_of_samples)
        data_avg = op.average_value(self.array_of_samples)

        self.dynamic_range = op.dynamic_range(data_max, data_min)
        self.dynamic_range_score = op.dynamic_range_score(data_max, data_avg)
