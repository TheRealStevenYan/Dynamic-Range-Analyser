import math

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
        elif abs(sample_integer) <= 1500 or abs(sample_integer) >= 31000:
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

