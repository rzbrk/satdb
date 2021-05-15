#! /usr/bin/env python3

import argparse
from spacetrack import SpaceTrackClient
from satdb import STConfig
from datetime import datetime
import os.path
import gzip

def main(args):

    # Current UTC date/time as string for the output filename
    nowstr = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # Read the config file
    config = STConfig(args.config)

    # Check if output folder exists
    if not args.outdir.endswith('/'):
        args.outdir = args.outdir + '/'
    if not os.path.isdir(args.outdir):
        print("Output directory doesn't exist. Exiting.")
        exit()

    # Login to space-track and download data
    try:
        st = SpaceTrackClient(config.user, config.password)
    except:
        print("Error connecting to Space-Track. Exiting.")
        exit()
    else:
        xml = st.gp(decay_date=None,
            orderby=['norad_cat_id', 'epoch desc'],
            format='xml')
        with gzip.open(args.outdir + nowstr + '.xml.gz', 'wt') as outfile:
            outfile.write(xml)
        outfile.close()

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("outdir", help="Output directory for OMM file")
    args = parser.parse_args()
    main(args)
