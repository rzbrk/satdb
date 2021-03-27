#!/usr/bin/env python3

import argparse
from datetime import datetime
import matplotlib.pyplot as plt
import re

from satdb import Config, Dbase, tools

def valid_lid(lid):
    # Valid launch ID is of type YYYY-NNN
    if (not re.match("^\d{4}-\d{3}$", lid)):
        print("Launch ID", lid, "not of type YYYY-NNN")
        quit()
    else:
        return True

def main(args):
    # Check if the provided lid is valid
    valid_lid(args.lid)

    # Read the config file
    config = Config(args.config)

    # Connect to database
    dbc = Dbase(config)
    dbc.connect()

    # If launch ID is not starlink launch, then exit
    query = "select count(*), launch_date from object_metadata where id like %s and (name like 'STARLINK%' or name like 'FALCON 9%')"
    res = dbc.fetchone(query, (args.lid + "%",))
    n_obj = res[0]
    ldate = res[1]

    if (n_obj == 0):
        print("No Starlink objects for launch event", args.lid, "found. Exiting.")
        quit()

    # Retrieve all objects for this launch event from database
    query = "select norad_cat_id, name from object_metadata where id like %s and (name like 'STARLINK%' or name like 'FALCON 9%')"
    res = dbc.fetchall(query, (args.lid + "%",))

    # Loop over all objects
    i = 1
    for r in res:
        norad = r[0]
        name = r[1]
        print(" ", str(i)+"/"+str(n_obj), "Retrieving data for", name, "(NORAD Cat ID: " + str(norad) + ") ...")

        # Retrieve data (epoch, semimajor axis) for object
        query = "select epoch, semimajor_axis from orbelem where norad_cat_id = %s"
        data = dbc.fetchall(query, (norad,))
        # Create empty arrays
        t = []
        sma = []
        for d in data:
            # Days after launch
            dt = d[0] - ldate
            t.append(dt.days)
            # Substract Earth radius from semimajor axis
            sma.append(d[1] - tools.re)

        # Apply moving median filter
        if (args.movmedian):
            sma = tools.movmedian(sma, args.movmedian)

        # Starlinks: blue line color
        # Falcon 9 R/B or debris: red line color
        if (re.match("STARLINK-.*", name)):
            linestyle = "-"
        else:
            linestyle = "r--"

        plt.plot(t, sma, linestyle, label = name)
        plt.xlabel("Days from launch")
        plt.ylabel("Altitude [km]")
        plt.title("Starlink Launch " + args.lid + " (" + ldate.strftime("%Y-%m-%d") + ")")

        i += 1

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
    parser.add_argument("lid", help="Launch ID")
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
    args = parser.parse_args()
    main(args)
