#! /usr/bin/env python3

import argparse

#from spacetrack import SpaceTrackClient
import spacetrack.operators as op
from spacetrack.aio import AsyncSpaceTrackClient
import asyncio

from satdb import STConfig
from satdb.tools import ttprint

from datetime import date, datetime
import os.path
import gzip

VERBOSE = False

async def st_download(config, filename, norad, epoch_from, epoch_to):
    # Login to space-track and download data
    try:
        st = AsyncSpaceTrackClient(
            config.user,
            config.password
            )
    except:
        ttprint("Error connecting to Space-Track. Exiting.")
        exit()
    else:
        # Read chunks of 100kB, see:
        # https://spacetrack.readthedocs.io/en/latest/usage.html#streaming-downloads
        ttprint("Downloading OMM from space-track.org")
        async with st:
            data = await st.gp_history(
                iter_content=True,
                norad_cat_id=norad,
                epoch=op.inclusive_range(epoch_from, epoch_to),
                #epoch='2017-07-14--2020-12-31',
                format='xml',
                )

            with gzip.open(filename, 'wt') as fp:
                nlines=1
                async for line in data:
                    fp.write(line)
                    if VERBOSE:
                        ttprint("  Write chunk " + str(nlines) + " ...")
                    nlines += 1
        ttprint("Downloaded file: " + filename)

def main(args):

    ttprint("Executing " + os.path.basename(__file__))

    # Current UTC date/time as string for the output filename
    nowstr = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    # Update global variable VERBOSE, if necessary
    if args.verbose:
        global VERBOSE
        VERBOSE = True

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

    # Try to convert the command line arguments from and to to valid dates
    try:
        epoch_from = date.fromisoformat(args.epoch_from)
    except:
        ttprint("Cannot convert \"" + args.epoch_from + "\" to date object. Exiting")
        exit()
    else:
        pass

    try:
        epoch_to = date.fromisoformat(args.epoch_to)
    except:
        ttprint("Cannot convert \"" + args.epoch_to + "\" to date object. Exiting")
        exit()
    else:
        pass

    # epoch_from shall be lower than epoch_to
    if not epoch_to > epoch_from:
        ttprint("Empty or negative epoch range. Exiting")
        exit()

    filename = (
        args.outdir +
        nowstr +
        "_" +
        str(args.norad) +
        ".xml.gz"
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(st_download(config,
        filename,
        args.norad,
        epoch_from,
        epoch_to,
        ))

    ttprint("Finished")

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("outdir", help="Output directory for OMM file")
    parser.add_argument("norad", help="NORAD Catalogue ID of object", type=int)
    parser.add_argument("--from", "-f", dest="epoch_from",
        help="Lower boundary for epoch range (YYYY-MM-DD)",
        type=str)
    parser.add_argument("--to", "-to", dest="epoch_to",
        help="Upper boundary for epoch range (YYYY-MM-DD",
        type=str)
    parser.add_argument("--verbose", help="increase output verbosity",
            action="store_true")
    args = parser.parse_args()
    main(args)
