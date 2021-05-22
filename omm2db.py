#!/usr/bin/env python3

import argparse
import xml.etree.ElementTree as et
from datetime import datetime
import os

from satdb import DBConfig, Dbase, OMMMetadata, OMMOrbelem, tools
from satdb.tools import ttprint

#------------------------------------------------------------------------------
# Ingest metadata in database
def metadata2db(db, md):

    # All columns in table metadata - except created - form the primary key.
    # Therefore, the combination of all column in the primary key will be
    # unique. This will be ensured by the database itself. :)
    # Therefore, we can perform an "insert ignore" for the metadata. If the
    # database sees, the metadata already exists, the sql request will be
    # ignored. This way, we save to perform a select request to see, if the
    # metadata is already in the database. This improves the speed of the
    # script.
    sql = ('insert ignore into metadata (' +
        'norad,' +
        'name,' +
        'id,' +
        'id_short,' +
        'center_name,' +
        'ref_frame,' +
        'mean_element_theory,' +
        'classification_type,' +
        'type,' +
        'rcs_size,' +
        'country_code,' +
        'launch_date,' +
        'site,' +
        'decay_date,' +
        'created) ' +
        'values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    res = db.write(sql, (md.norad,
        md.name,
        md.obj_id,
        md.id_short,
        md.center_name,
        md.ref_frame,
        md.mean_element_theory,
        md.classification_type,
        md.obj_type,
        md.rcs_size,
        md.country_code,
        md.launch_date,
        md.site,
        md.decay_date,
        md.created,)
        )

#------------------------------------------------------------------------------
# Ingest orbital elements in database
def orbelem2db(db, od):
    sql = ('insert ignore into orbelem (epoch,' +
            'mean_motion,' +
            'eccentricity,' +
            'inclination,' +
            'ra_of_asc_node,' +
            'arg_of_pericenter,' +
            'mean_anomaly,' +
            'ephemeris_type,' +
            'norad,' +
            'element_set_no,' +
            'rev_at_epoch,' +
            'bstar,' +
            'mean_motion_dot,' +
            'mean_motion_ddot,' +
            'semimajor_axis,' +
            'period,' +
            'apoapsis,' +
            'periapsis,' +
            'ingested,' +
            'originator,' +
            'data_created,' +
            'originator_comment) values (%s, %s, %s, %s, %s, %s, %s, %s,' +
            '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
    db.write(sql, (od.epoch,
        od.mean_motion,
        od.eccentricity,
        od.inclination,
        od.raan,
        od.arg_of_pericenter,
        od.mean_anomaly,
        od.ephemeris_type,
        od.norad,
        od.element_set_no,
        od.rev_at_epoch,
        od.bstar,
        od.mean_motion_dot,
        od.mean_motion_ddot,
        od.semimajor_axis,
        od.period,
        od.apoapsis,
        od.periapsis,
        od.ingested,
        od.originator,
        od.data_created,
        od.originator_comment))

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
        metadata2db(dbc, md)
        orbelem2db(dbc, od)
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
    args = parser.parse_args()
    main(args)
