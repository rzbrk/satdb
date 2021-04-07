#!/usr/bin/env python3

import argparse
#import gzip
#import re
import xml.etree.ElementTree as et
#import mysql.connector
from datetime import datetime
import os

from satdb import Config, Dbase, NDMMetadata, NDMOrbelem, tools

NULL = "NULL"

#------------------------------------------------------------------------------
# Ingest metadata in database
def metadata2db(db, md):
    # Handle NULL decay_date
    if md.decay_date == NULL:
        md.decay_date = "0000-00-00 00:00:00"
    # Handle NULL launch_date
    if md.launch_date == NULL:
        md.launch_date = "0000-00-00 00:00:00"

    # Each object is unambiguously defined by the norad_cat_id.
    # The object metadata can change, especially for newly launched objects.
    # First, see if object with norad_cat_id is already in the database. If
    # so, perform an update. If not, perform insert.
    sql = 'select count(*),created from object_metadata where norad_cat_id=%s'
    res = db.fetchone(sql, (md.norad_cat_id,))
    n = res[0]
    # db_created is the creation/update time stamp from the object in the
    # database (python datetime object)
    db_created = res[1]
    # ndm_created is the time from the NDM. Create a python datetime object
    # from md.created (string)
    ndm_created = datetime.strptime(md.created, '%Y-%m-%dT%H:%M:%S')

    # Because norad_cat_id is unique, n from the above database query can only
    # be zero (no such onject in database) or 1 (object already in database)
    if n == 0:
        # No object with given norad_cat_id in database
        sql = 'insert into object_metadata (id, id_short, name, center_name, ref_frame, mean_element_theory, created, type, rcs_size, country_code, launch_date, site, decay_date, classification_type, norad_cat_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        db.write(sql, (md.obj_id, md.id_short, md.name, md.center_name, md.ref_frame, md.mean_element_theory, md.created, md.obj_type, md.rcs_size, md.country_code, md.launch_date, md.site, md.decay_date, md.classification_type, md.norad_cat_id))
    elif n == 1:
        # Object with given norad_cat_id already in database.
        # Perform an update if data from NDM is newer that the data in the
        # database. If not, do nothing.
        if ndm_created > db_created:
            sql = 'update object_metadata set id=%s, id_short=%s, name=%s, center_name=%s, ref_frame=%s, mean_element_theory=%s, created=%s, type=%s, rcs_size=%s, country_code=%s, launch_date=%s, site=%s, decay_date=%s, classification_type=%s where norad_cat_id=%s'
            db.write(sql, (md.obj_id, md.id_short, md.name, md.center_name, md.ref_frame, md.mean_element_theory, md.created, md.obj_type, md.rcs_size, md.country_code, md.launch_date, md.site, md.decay_date, md.classification_type, md.norad_cat_id))
    else:
        # Multiple objects with the same norad_cat_id?!?
        # Houston, we have a problem :/
        print("Database must not contain multiple objects with same NORAD Cat ID. Exiting")
        exit()

#------------------------------------------------------------------------------
# Ingest orbital elements in database
def orbelem2db(db, od):
    sql = 'insert ignore into orbelem (epoch, mean_motion, eccentricity, inclination, ra_of_asc_node, arg_of_pericenter, mean_anomaly, ephemeris_type, norad_cat_id, element_set_no, rev_at_epoch, bstar, mean_motion_dot, mean_motion_ddot, semimajor_axis, period, apoapsis, periapsis, ingested, originator, data_created, originator_comment) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    db.write(sql, (od.epoch, od.mean_motion, od.eccentricity, od.inclination, od.raan, od.arg_of_pericenter, od.mean_anomaly, od.ephemeris_type, od.norad_cat_id, od.element_set_no, od.rev_at_epoch, od.bstar, od.mean_motion_dot, od.mean_motion_ddot, od.semimajor_axis, od.period, od.apoapsis, od.periapsis, od.ingested, od.originator, od.data_created, od.originator_comment))

#------------------------------------------------------------------------------
# Main routine
def main(args):

    # Raed the config file
    config = Config(args.config)

    # Connect to the database
    dbc = Dbase(config)
    dbc.connect()

    # Open the NDM file
    fh = tools.open_file(args.ndmfile)
    root = et.fromstring(fh.read())

    # Now, loop over all segments, which are the space objects in the NDM file
    n_segment = len(root.findall(".//segment"))
    i = 1
    t_start = datetime.now()
    for segment in root.findall(".//segment"):

        # Extract all data needed for the database table "object_metadata"
        md = NDMMetadata(segment)

        # Extract all data needed for the database table "orbelem"
        od = NDMOrbelem(segment, root)

        eta = (datetime.now() - t_start)/i * (n_segment - i)
        print("[" + str(i) + "/" + str(n_segment) + "] Processing " + md.obj_id + " (" + md.name + "), ETA: " + str(eta))
        metadata2db(dbc, md)
        orbelem2db(dbc, od)
        i += 1

    # Disconnect database
    dbc.disconnect()

###############################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file")
    parser.add_argument("ndmfile", help="NDM file")
    args = parser.parse_args()
    main(args)
