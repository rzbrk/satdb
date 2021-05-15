#!/usr/bin/env python3

import argparse
#import gzip
#import re
import xml.etree.ElementTree as et
#import mysql.connector
from datetime import datetime
import os

from satdb import DBConfig, Dbase, OMMMetadata, OMMOrbelem, tools

NULL = "NULL"

#------------------------------------------------------------------------------
# Ingest metadata in database
def metadata2db(db, md):

    # Check, if the exact metadata set is already in database
    sql = ('select count(*) from metadata ' +
            'where norad=%s ' +
            'and name=%s ' +
            'and id=%s'  +
            'and id_short=%s ' +
            'and center_name=%s ' +
            'and ref_frame=%s ' +
            'and mean_element_theory=%s ' +
            'and classification_type=%s ' +
            'and type=%s ' +
            'and rcs_size=%s ' +
            'and country_code=%s ' +
            'and launch_date=%s ' +
            'and site=%s ' +
            'and decay_date=%s')
    res = db.fetchone(sql, (md.norad,
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
        md.decay_date,)
        )
    n = res[0]

    # Only if n = 0 the metadata not yet exist in db and will be inserted.
    # If n > 0, simply do nothing, because data is already in database.
    if n == 0:
        sql = ('insert into metadata (' +
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
            'norad_cat_id,' +
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
        od.norad_cat_id,
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

    # Raed the config file
    config = DBConfig(args.config)

    # Connect to the database
    dbc = Dbase(config)
    dbc.connect()

    # Open the OMM file
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
        od = OMMOrbelem(segment, root)

        eta = (datetime.now() - t_start)/i * (n_segment - i)
        print("[" + str(i) + "/" + str(n_segment) + "] Processing "
                + md.obj_id + " (" + md.name + "), ETA: " + str(eta))
        metadata2db(dbc, md)
        orbelem2db(dbc, od)
        i += 1

    # Disconnect database
    dbc.disconnect()

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("ommfile", help="OMM file")
    args = parser.parse_args()
    main(args)
