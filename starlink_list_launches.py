#!/usr/bin/env python3

import argparse
from datetime import datetime

from satdb import Config, Dbase, tools

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

    print("\nStarlink launches in database\n")
    print("      # | Launch ID |       Date | # Total | # Ridesh | # Decayed")
    print(" ", "-" * 64)
    i = 1
    for d in dates:
        lid = d[0]
        ldate = d[1].strftime("%Y-%m-%d")

        # For each launch retrieve some additional information
        # Active objects in orbit
        query = "select count(*) from object_metadata where id like %s and decay_date = '0000-00-00'"
        n_active = dbc.fetchone(query, (lid+'%',))[0]

        # Rideshare objects (no starlink or falcon objects
        query = "select count(*) from object_metadata where id like %s and (name not like 'STARLINK%' and name not like 'FALCON%')"
        n_rideshare = dbc.fetchone(query, (lid+'%',))[0]
        # Decayed/reentered objects
        query = "select count(*) from object_metadata where id like %s and decay_date <> '0000-00-00'"
        n_decayed = dbc.fetchone(query, (lid+'%',))[0]


        print("   %4d |  %8s | %10s |     %3d |      %3d |       %3d" %
                (i, lid, ldate, n_active, n_rideshare, n_decayed))

        i += 1

    print()
    dbc.disconnect()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    args = parser.parse_args()
    main(args)
