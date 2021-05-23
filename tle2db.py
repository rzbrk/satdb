#!/usr/bin/env python3

import argparse
from tletools import TLE
from datetime import datetime, timedelta
import os

from satdb import DBConfig, Dbase, OMMMetadata, OMMOrbelem, tools
from satdb.tools import ttprint

def main(args):

    ttprint("Executing " + os.path.basename(__file__))

    # Read the config file
    ttprint("Reading config file " + args.config)
    config = DBConfig(args.config)

    # Connect to the database
    ttprint("Connecting to database")
    dbc = Dbase(config)
    dbc.connect()

    # Open the TLE file
    fh = tools.open_file(args.tlefile)
    all_lines = fh.readlines()
    fh.close

    # Total number of TLEs in file
    n_tle = int(len(all_lines)/3)

    # Read three consecutive lines and process as TLE
    i = 1
    t_start = datetime.now()
    tle_lines = []
    for line in all_lines:
        tle_lines.append(line.rstrip())

        if len(tle_lines) == 3:
            # Metadata
            md = OMMMetadata()
            md.from_tle(tle_lines)
            md.to_db(dbc)

            if args.verbose:
                eta = (datetime.now() - t_start).seconds * (n_tle - i)/i
                if eta > 60:
                    eta = round(eta/60., 1)
                    eta_units = " min"
                else:
                    eta = int(eta)
                    eta_units = " sec"
                ttprint("[" + str(i) + "/" + str(n_tle) + "] Processing "
                        + md.obj_id + " (" + md.name + "), ETA: " + str(eta)
                        + eta_units)

            # Mean orbital elements
            od = OMMOrbelem()
            od.from_tle(tle_lines)
            od.to_db(dbc)

            # Empty tle_lines
            tle_lines = []

            i += 1

    # Disconnect database
    ttprint("Disconnecting from database")
    dbc.disconnect()

    ttprint("Finished")

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("tlefile", help="TLE file")
    parser.add_argument("--verbose", help="increase output verbosity",
            action="store_true")
    args = parser.parse_args()
    main(args)
