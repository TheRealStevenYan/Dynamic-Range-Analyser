import os
import sqlite3

from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog
import math


# A class containing the data of the selected file. Used for saving / loading / printi
class AudioData:
    # Constructor. Initialises a blank AudioData class.
    def __init__(self):
        self.dynamic_range = 0
        self.dynamic_range_score = 0
        self.audio_segment = None
        self.array_of_samples = []
        self.file_path = ""
        self.file_name = ""

    # Opens a file, and initialises all the attributes in the AudioData class based on the file.
    def open_file(self):
        self.file_path = tk.filedialog.askopenfilename()
        self.file_name = os.path.basename(self.file_path)
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
        data_max, data_min = get_max_and_min(self.array_of_samples)
        data_avg = average_value(self.array_of_samples)

        self.dynamic_range = dynamic_range(data_max, data_min)
        self.dynamic_range_score = dynamic_range_score(data_max, data_avg)


# A class which utilises an SQLite database to keep track of previous entries.
class AudioDataLog:
    def __init__(self):
        self.db_conn = None
        self.db_connect()
        self.db_table_init()

    def db_connect(self):
        database_abs_path = os.path.abspath("database.db")
        print(database_abs_path)
        try:
            self.db_conn = sqlite3.connect(database_abs_path)
        except sqlite3.Error as e:
            print(e)

    def db_table_init(self):
        cur = self.db_conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS audio_log (
                       File_Name text,
                       Dynamic_Range integer,
                       Score integer
                    )""")
        self.db_conn.commit()

    def db_insert(self, audio_data):
        cur = self.db_conn.cursor()
        try:
            cur.execute("INSERT INTO audio_log VALUES ('{name}', {dr}, {score})"
                        .format(name=audio_data.file_name,
                                dr=audio_data.dynamic_range,
                                score=audio_data.dynamic_range_score))
            self.db_conn.commit()
        except sqlite3.Error as e:
            print(e)

    def db_close(self):
        self.db_conn.close()

    def db_query(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM audio_log")
        return cur.fetchall()




"""
dynamic range is the measure of the difference in loudness from the loudest parts of a song to the quietest
mp3s can be broken down into audio samples which are an integer representation of the sound.
dynamic range is calculated by using the formula 20 * log(high / low), where:
    high is the absolute highest sample,
    low is the closest value to 0 (but not 0)
https://en.wikipedia.org/wiki/Dynamic_range
"""


# Returns the absolute maximum, and the closest value to 0 (but not 0) from the sample array.
def get_max_and_min(sample_array):
    max_sample = 0
    min_sample = 100000
    for sample_integer in sample_array:
        if abs(sample_integer) > max_sample:
            max_sample = abs(sample_integer)
        if abs(sample_integer) < min_sample and sample_integer != 0:
            min_sample = abs(sample_integer)
    return max_sample, min_sample


# The average is calculated by total sum / number of samples, with some compensation to remove outliers as follows:
# All songs have lots of samples at 1 or 0. Since they drag down the average score by quite a lot, we discount them.
# Songs with extended periods of low volume may seem to have good dynamic range, but low volumes could occur
# during breaks / solos. As it could bring down our average, we weigh these values less.
# The highest volumes tend to occur briefly during peaks. As these are brief, we also weigh them less.
def average_value(sample_array):
    sum = 0
    small_values = 0
    for sample_integer in sample_array:
        if abs(sample_integer) <= 10:
            small_values += 1
            continue
        if abs(sample_integer) <= 1500 or abs(sample_integer) >= 31000:
            sum += abs(sample_integer / 2)
            small_values += .25
            continue
        sum += abs(sample_integer)
    return abs(sum / (len(sample_array) - small_values))


# Calculates dynamic range according to the the formula given at the top of this file. Rounded to 3 decimal places.
def dynamic_range(sample_max, sample_min):
    return round(20 * math.log((sample_max / sample_min), 10), 3)


# The dynamic range score is calculated by taking the ratio between the absolute maximum of the sample, and its average.
# There is a bit of compensation to bump up our scores a little bit.
def dynamic_range_score(sample_max, sample_avg):
    return round(1.35 * sample_max / sample_avg, 2)