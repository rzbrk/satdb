#!/usr/bin/env python3

import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, AutoDateFormatter
import re

from satdb import Config, Dbase, tools

def main(args):
    # Read the config file
    config = Config(args.config)

    # Connect to database
    dbc = Dbase(config)
    dbc.connect()

    print(args.ids)

    # Initialize plot
    fig = plt.figure()
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111)
    ax.set_xlabel("Time")
    ax.tick_params(axis='x', labelrotation=45)
    ax.set_ylabel("Altitude [km]")
    ax.ticklabel_format(axis="y", useOffset=False)
    #ax.set_title("")

    # Loop over all objects
    i = 1
    for norad in args.ids:
        norad = int(norad)

        # Get name of object
        query = "select name from object_metadata where norad_cat_id = %s"
        name = dbc.fetchone(query, (norad,))[0]

        print(" ", str(i)+"/"+str(len(args.ids)), "Retrieving data for", name, "(NORAD Cat ID: " + str(norad) + ") ...")

        # Retrieve data (epoch, semimajor axis) for object
        query = "select epoch, semimajor_axis from orbelem where norad_cat_id = %s"
        data = dbc.fetchall(query, (norad,))
        # Create empty arrays
        t = []
        sma = []
        for d in data:
            t.append(d[0])
            # Substract Earth radius from semimajor axis
            sma.append(d[1] - tools.re)

        # Apply moving median filter
        if (args.movmedian):
            sma = tools.movmedian(sma, args.movmedian)

        ax.plot(t, sma, "-", label = name+" ("+str(norad)+")")

        i += 1

    ax.legend()
    if (args.ymin is not None and args.ymax is not None and args.ymin < args.ymax):
        plt.ylim([args.ymin, args.ymax])

    # Save plot to file
    if (args.filename == ""):
        imgfile = "output/" + args.lid + ".png"
    else:
        imgfile = args.filename
    plt.savefig(imgfile, format="png")
    print("")
    print("Image saved to", imgfile)

    dbc.disconnect()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("ids", type=str, nargs="+", help="Object IDs to plot")
    parser.add_argument("--movmedian",
            type=int,
            default=0,
            help="Apply moving median filter. Specify box halfwidth.",
            )
    parser.add_argument("--filename",
            type=str,
            default="",
            help="Specify filename for image",
            )
    parser.add_argument("--ymin",
            type=int,
            help="Minimum value for vertical axis")
    parser.add_argument("--ymax",
            type=int,
            help="Maximum value for vertical axis")
    args = parser.parse_args()
    main(args)
