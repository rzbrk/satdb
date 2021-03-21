#!/usr/bin/env python3

import mysql.connector
from getpass import getpass
from datetime import datetime
import matplotlib.pyplot as plt
import re
from satdb import config, dbase

# Earth radius [km]
r_earth = 6378.0

def dbconn():
    pwd = getpass("Enter password: ")
    dbc = mysql.connector.connect(
            host = "h2916865.stratoserver.net",
            user = "orbdata",
            database = "orbdata01",
            password = pwd,
            )

    return dbc

def main():
    now = datetime.now().strftime("%Y-%m-%d")

    # Connect to database
    dbc = dbconn()

    # Return array with year and launch no (YYYY-NNN) for all launches with
    # starlink satellites
    c = dbc.cursor()
    query = "select distinct(substr(id, 1, 8)), launch_date from object_metadata where id is not null and name like 'STARLINK%' and launch_date <> '0000-00-00'"
    c.execute(query)
    dates = c.fetchall()

    # Ask the user to select one launch event
    not_selected = True
    while (not_selected):
        print("")
        print("Select launch event:")
        i = 1
        for d in dates:
            lid = d[0]
            launch_date = d[1]
            print("  ", i, lid, launch_date)
            i += 1

        print("")
        l = input("Select: ")
        l = int(l)

        if (l >= 1 and l <= len(dates)):
            not_selected = False

    # Fetch all starlink and falcon 9 objects from selected launch. Exclude
    # the rideshare payloads other than starlink
    lid = dates[l - 1][0]
    ldate = dates[l - 1][1]

    c = dbc.cursor()
    query = "select norad_cat_id, name from object_metadata where id like %s and (name like 'STARLINK%' or name like 'FALCON 9%')"
    c.execute(query, (lid+"%",))
    res = c.fetchall()

    # Loop over all objects
    for r in res:
        norad = r[0]
        name = r[1]
        print("\t", norad, name)

        # Retrieve data (epoch, semimajor axis) for object
        c = dbc.cursor()
        query = "select epoch, semimajor_axis from orbelem where norad_cat_id = %s"
        c.execute(query, (norad,))
        data = c.fetchall()
        # Create empty arrays
        t = []
        sma = []
        for d in data:
            # Days after launch
            dt = d[0] - ldate
            t.append(dt.days)
            # Substract Earth radius from semimajor axis
            sma.append(d[1] - r_earth)

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
    plt.savefig(lid+".png", format="png")

    dbc.close()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
