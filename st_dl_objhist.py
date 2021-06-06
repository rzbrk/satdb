#! /usr/bin/env python3

import argparse

#from spacetrack import SpaceTrackClient
import spacetrack.operators as op
from spacetrack.aio import AsyncSpaceTrackClient
import asyncio

from satdb import STConfig
from satdb.tools import ttprint

from datetime import datetime
import os.path
import gzip

async def st_download(config, norad, epoch_range):
    st = AsyncSpaceTrackClient(
        config.user,
        config.password
        )

    async with st:
        data = await st.gp_history(
            iter_lines=True,
            #ordinal=1,
            norad_cat_id=norad,
            epoch='2017-07-14--2020-12-31',
            #mean_motion=op.inclusive_range(0.99, 1.01),
            #eccentricity=op.less_than(0.01),
            format='xml',
            )

        with open('test.xml', 'w') as fp:
            async for line in data:
                #fp.write(line + '\n')
                fp.write(line)

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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(st_download(config, args.norad, None))

    ttprint("Finished")

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("outdir", help="Output directory for OMM file")
    parser.add_argument("norad", help="NORAD Catalogue ID of object", type=int)
    args = parser.parse_args()
    main(args)
