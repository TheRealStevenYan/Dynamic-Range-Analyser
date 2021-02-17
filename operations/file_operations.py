import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import operations.number_operations as op


# Opens a file, and creates + returns an AudioData object based on its data.
def open_file():
    file_path = tk.filedialog.askopenfilename()
    try:
        audio_segment = get_audio_segment(file_path)
        return calculate_data(audio_segment)
    except:
        return None


# Accepts a path to an input file, and then returns it as an AudioSegment.
# Throws exception if not found. Remember to catch this exception.
def get_audio_segment(input_path):
    file_ext = os.path.splitext(input_path)[1]
    file_ext = file_ext[1:len(file_ext)]
    audio_segment = AudioSegment.from_file(input_path, format=file_ext)
    return audio_segment


# Calculates the required data (dynamic range etc) from the given array of samples.
# Creates an AudioData object with the required data as attributes.
def calculate_data(audio_segment):
    sample_array = audio_segment.get_array_of_samples()
    data_max, data_min = op.get_max_and_min(sample_array)
    data_avg = op.average_value(sample_array)

    dynamic_range = op.dynamic_range(data_max, data_min)
    score = op.dynamic_range_score(data_max, data_avg)
    return AudioData(dynamic_range, score, audio_segment, sample_array)


# A class containing the data of the selected file. Used for saving / loading / printing operations.
class AudioData:
    def __init__(self, dr, dr_score, audio_segment, sample_array):
        self.dynamic_range = dr
        self.dynamic_range_score = dr_score
        self.audio_segment = audio_segment
        self.array_of_samples = sample_array
