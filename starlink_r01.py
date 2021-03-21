#!/usr/bin/env python3

import argparse
from getpass import getpass
from datetime import datetime
import matplotlib.pyplot as plt
import re

from satdb import Config, Dbase, tools

# Earth radius [km]
r_earth = 6378.0

def main(args):
    now = datetime.now().strftime("%Y-%m-%d")

    # Read the config file
    config = Config(args.config)

    # Connect to database
    dbc = Dbase(config)
    dbc.connect()

    # Return array with year and launch no (YYYY-NNN) for all launches with
    # starlink satellites
    query = "select distinct(substr(id, 1, 8)), launch_date from object_metadata where id is not null and name like 'STARLINK%' and launch_date <> '0000-00-00'"
    dates = dbc.fetchall(query)

    # Ask the user to select one launch event
    not_selected = True
    while (not_selected):
        print("")
        print("Please select a launch event (choose by row number):")
        i = 1
        for d in dates:
            lid = d[0]
            ldate = d[1].strftime("%Y-%m-%d")
            print("  ", i, lid, "(" + ldate + ")")
            i += 1

        print("")
        l = input("Select: ")
        try:
            l = int(l)
        except:
            # Choose a non-valid integer instead
            l = 0

        # Check if l is in the right range
        if (l >= 1 and l <= len(dates)):
            not_selected = False

    print("")
    # Fetch all starlink and falcon 9 objects from selected launch. Exclude
    # the rideshare payloads other than starlink
    lid = dates[l - 1][0]
    ldate = dates[l - 1][1]

    query = "select norad_cat_id, name from object_metadata where id like %s and (name like 'STARLINK%' or name like 'FALCON 9%')"
    res = dbc.fetchall(query, (lid + "%",))

    # Loop over all objects
    for r in res:
        norad = r[0]
        name = r[1]
        print("  Retrieving data for", name, "(NORAD Cat ID: " + str(norad) + ") ...")

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
            sma.append(d[1] - r_earth)

        # Set outlier to nan
        if (args.skip_outliers):
            sma = tools.outliers(sma, report=True)

        # Starlinks: blue line color
        # Falcon 9 R/B or debris: red line color
        if (re.match("STARLINK-.*", name)):
            linestyle = "-"
        else:
            linestyle = "r--"

        plt.plot(t, sma, linestyle, label = name)
        plt.xlabel("Days from launch")
        plt.ylabel("Altitude [km]")
        plt.title("Starlink Launch " + lid + " (" + ldate.strftime("%Y-%m-%d") + ")")

    # Save plot to file
    imgfile = "output/" + lid + ".png"
    plt.savefig(imgfile, format="png")
    print("")
    print("Image saved to", imgfile)

    dbc.disconnect()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("--skip-outliers", action = "store_true",
            help="Skip outliers")
    args = parser.parse_args()
    main(args)
