#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as et
from datetime import datetime
import os

from satdb import DBConfig, Dbase, OMMMetadata, OMMOrbelem, tools
from satdb.tools import ttprint

#------------------------------------------------------------------------------
# Main routine
def main(args):

    ttprint("Executing " + os.path.basename(__file__))

    # Read the config file
    ttprint("Reading config file " + args.config)
    config = DBConfig(args.config)

    # Connect to the database
    ttprint("Connecting to database")
    dbc = Dbase(config)
    dbc.connect()

    # Open the OMM file
    ttprint("Reading OMM file " + args.ommfile)
    fh = tools.open_file(args.ommfile)
    root = et.fromstring(fh.read())

    # Now, loop over all segments, which are the space objects in the OMM file
    n_segment = len(root.findall(".//segment"))
    i = 1
    t_start = datetime.now()
    for segment in root.findall(".//segment"):

        # Extract all data needed for the database table "metadata"
        md = OMMMetadata()
        md.from_omm(segment)

        # Extract all data needed for the database table "orbelem"
        od = OMMOrbelem()
        od.from_omm(segment, root)

        if args.verbose:
            eta = (datetime.now() - t_start).seconds * (n_segment - i)/i
            if eta > 60:
                eta = round(eta/60., 1)
                eta_units = " min"
            else:
                eta = int(eta)
                eta_units = " sec"
            ttprint("[" + str(i) + "/" + str(n_segment) + "] Processing "
                    + md.obj_id + " (" + md.name + "), ETA: " + str(eta)
                    + eta_units)

        # Write metadata and orbital elements to database
        md.to_db(dbc)
        od.to_db(dbc)

        i += 1

    # Disconnect database
    ttprint("Disconnecting from database")
    dbc.disconnect()

    ttprint("Finished")

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("ommfile", help="OMM file")
    parser.add_argument("--verbose", help="increase output verbosity",
            action="store_true")
    args = parser.parse_args()
    main(args)
