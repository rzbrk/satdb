#!/usr/bin/env python3

import numpy as np

# Returns the index numbers of outliers in array data
# Adapted from: https://stackoverflow.com/a/61308669
def outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    data_range = np.arange(len(data))
    idx_list = data_range[s>=m]

    return idx_list
