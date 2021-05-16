#!/usr/bin/env python3

import numpy as np
import re as regexp
import gzip
from datetime import datetime

# Earth radius in km
re = 6378.

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
