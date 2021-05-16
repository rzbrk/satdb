#! /usr/bin/env python3

import argparse
from spacetrack import SpaceTrackClient
from satdb import STConfig
from satdb.tools import ttprint
from datetime import datetime
import os.path
import gzip

def main(args):

    ttprint("Executing " + os.path.basename(__file__))

    # Current UTC date/time as string for the output filename
    nowstr = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # Read the config file
    ttprint("Reading config file " + args.config)
    config = STConfig(args.config)

    # Check if output folder exists
    if not args.outdir.endswith('/'):
        args.outdir = args.outdir + '/'
    if not os.path.isdir(args.outdir):
        ttprint("Output directory doesn't exist. Exiting.")
        exit()
    else:
        ttprint("Output directory " + args.outdir + " exists")

    # Login to space-track and download data
    try:
        st = SpaceTrackClient(config.user, config.password)
    except:
        ttprint("Error connecting to Space-Track. Exiting.")
        exit()
    else:
        ttprint("Downloading OMM from space-track.org")
        xml = st.gp(decay_date=None,
            orderby=['norad_cat_id', 'epoch desc'],
            format='xml')
        outfilename = args.outdir + nowstr + ".xml.gz"
        with gzip.open(outfilename, 'wt') as outfile:
            outfile.write(xml)
        outfile.close()
        ttprint("Downloaded file: " + outfilename)
        ttprint("Finished")

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("outdir", help="Output directory for OMM file")
    args = parser.parse_args()
    main(args)
