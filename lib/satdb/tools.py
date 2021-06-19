#!/usr/bin/env python3

import numpy as np
import re as regexp
import gzip
from datetime import datetime, timedelta
from math import floor, log10
import re

# Earth radius in km
#re = 6378.

def movmedian(data, boxhw):
    data_filtered = []

    for i in range(0,len(data)):
        # Lower boundary
        lb = i - boxhw if i >= boxhw else 0
        # Upper boundary
        ub = i + boxhw if i + boxhw < len(data) else len(data)-1
        # Calculate median from array slice (sliding window)
        data_filtered.append(np.median(data[lb:ub+1]))
        #print(i, lb, ub, data[lb:ub+1], np.median(data[lb:ub+1]))

    return data_filtered

# Open a file for reading. Unzip first, if gzipped
def open_file(filename):
    if regexp.match('.*.gz$', filename):
        fh = gzip.open(filename, 'rt')
    else:
        fh = open(filename, 'r')

    return fh

# Time tagged print function
def ttprint(message):
    nowstr = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S:")
    print(nowstr, message)

# Convert given number to string with exponent notation used in TLEs
# Examples:
# -0.99     => '-99000-0'
#  0.0      => ' 00000-0'
#  0.01     => ' 10000-1'
#  0.099    => ' 99000-1'
#  0.123    => ' 12300-1'
#  0.1      => ' 10000-0'
#  0.12     => ' 12000-0'
#  0.99     => ' 99000-0'
#  1.0      => ' 10000+1'
#
def conv_exp_notation(number):

    sign = "-" if number < 0. else " "

    exp = int(floor(log10(abs(number)))) + 1 if number != 0 else 0

    mant = abs(number)/10**exp

    formatted_number_str = (
        sign +
        ('%5.5f' % mant).replace('0.', '')
        )

    if exp < 0:
        formatted_number_str += '%2d' % exp
    elif exp == 0:
        formatted_number_str += '-0'
    else:
        formatted_number_str += '+' + '%1d' % exp

    return formatted_number_str

# Computes the checksum for a TLE line.
# See: https://celestrak.com/NORAD/documentation/tle-fmt.php
# If the line contains bad/forbidden characters, this function returns 0
def tle_checksum(line=None):
    checksum = None
    bad_char = None

    if line is not None:
        checksum = 0
        for i in range(0, len(line)):
            if re.match('[ a-zA-Z.+]', line[i]):
                checksum += 0
            elif line[i] == '-':
                checksum += 1
            elif re.match('[0-9]', line[i]):
                checksum += int(line[i])
            else:
                print("Forbidden character!")
                bad_char = True
                break

            if (bad_char):
                break

        # Perform modulo 10
        if not bad_char:
            checksum = checksum % 10
        else:
            checksum = None

    return checksum

# Calculate a datetime object from the year YYYY and the decimal day of
# year (doy)
def doy2datetime(year, doy):
    # The day of year starts with 1 at January, 1st 00:00:00! See e.g.
    # the example in the German Wikipedia article for TLE:
    # https://de.wikipedia.org/wiki/Satellitenbahnelement#Erl%C3%A4uterung_der_Zahlengruppen
    # Therefore, the doy must be greater-equal 1
    return datetime(year, 1, 1) + timedelta(days=(doy - 1))

# Calculate the decimal day of year from a given datetime object
def datetime2doy(epoch):
    # January, 1st 00:00:00 is already doy 1! Therefore, the below line
    # contains a constant 1
    t0 = datetime(epoch.year, 1, 1)

    return 1. + (epoch - t0).days + (epoch - t0).seconds / 86400.

