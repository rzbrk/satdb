#!/usr/bin/env python3

import numpy as np

# Returns the index numbers of outliers in array data
# Adapted from https://www.askpython.com/python/examples/detection-removal-outliers-in-python
def outliers(data, report=False):
    q25,q75 = np.percentile(data, [25, 75])
    iqr = q75 - q25

    dmax = q75 + (1.5 * iqr)
    dmin = q25 - (1.5 * iqr)

    n_outliers = 0
    for i in range(0,len(data)-1):
        if (data[i] < dmin or data[i] > dmax):
            data[i] = np.nan
            n_outliers += 1

    if (report):
        print("  # Elements:", len(data))
        print("  # Outliers:", n_outliers)

    return data
