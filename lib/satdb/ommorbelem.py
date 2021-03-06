from datetime import datetime, timedelta
from tletools import TLE
from satdb import tools

#NULL="NULL"

# Some constants to compute orbital parameters
GM = 398600441800000.0      # gravitational const * mass Earth
GM13 = GM ** (1.0/3.0)
MRAD = 6378.137             # Earth's radius [km]
PI = 3.14159265358979
TPI86 = 2.0 * PI / 86400.0

# Class for orbital elements
class OMMOrbelem:
    def __init__(self):
        self.norad = None

        # Orbital mean elements (celestrak + space-track)
        self.epoch = None
        self.mean_motion = None
        self.eccentricity = None
        self.inclination = None
        self.raan = None
        self.arg_of_pericenter = None
        self.mean_anomaly = None

        # TLE parameters (celestrak + space-track)
        self.ephemeris_type = None
        classification_type = None
        # norad --> see above
        self.element_set_no = None
        self.rev_at_epoch = None
        self.bstar = None
        self.mean_motion_dot = None
        self.mean_motion_ddot = None

        # TLE/3LE (can be computed from the TLE parameters above)
        self.tle_line0 = None
        self.tle_line1 = None
        self.tle_line2 = None

        # User defined parameters (space-track only)
        # Can be computed from orbital mean elements
        self.semimajor_axis = None
        self.period = None
        self.apoapsis = None
        self.periapsis = None

        # Some additional info (space-track only)
        self.originator = None
        self.data_created = None
        self.originator_comment = None

        # Creation date/time of entry in database
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def from_omm(self, segment, root):
        self.norad = segment.find(".//tleParameters/NORAD_CAT_ID").text or None

        # Orbital mean elements (celestrak + space-track)
        self.epoch = segment.find(".//meanElements/EPOCH").text or None
        self.mean_motion = segment.find(".//meanElements/MEAN_MOTION").text or None
        self.eccentricity = segment.find(".//meanElements/ECCENTRICITY").text or None
        self.inclination = segment.find(".//meanElements/INCLINATION").text or None
        self.raan = segment.find(".//meanElements/RA_OF_ASC_NODE").text or None
        self.arg_of_pericenter = segment.find(".//meanElements/ARG_OF_PERICENTER").text or None
        self.mean_anomaly = segment.find(".//meanElements/MEAN_ANOMALY").text or None

        # TLE parameters (celestrak + space-track)
        self.ephemeris_type = segment.find(".//tleParameters/EPHEMERIS_TYPE").text or None
        self.classification_type = segment.find(".//tleParameters/CLASSIFICATION_TYPE").text
        self.element_set_no = segment.find(".//tleParameters/ELEMENT_SET_NO").text or None
        self.rev_at_epoch = segment.find(".//tleParameters/REV_AT_EPOCH").text or None
        self.bstar =  segment.find(".//tleParameters/BSTAR").text or None
        self.mean_motion_dot = segment.find(".//tleParameters/MEAN_MOTION_DOT").text or None
        self.mean_motion_ddot = segment.find(".//tleParameters/MEAN_MOTION_DDOT").text or None

        # TLE/3LE (can be computed from the TLE parameters above)
        self.tle_line0 = None
        self.tle_line1 = None
        self.tle_line2 = None

        # User defined parameters (space-track only)
        # Can be computed from orbital mean elements
        try:
            self.semimajor_axis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SEMIMAJOR_AXIS']").text
        except:
            #self.semimajor_axis = None
            self.semimajor_axis = GM13 / ((TPI86 * float(self.mean_motion)) ** (2.0 / 3.0)) / 1000.0
        try:
            self.period = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIOD']").text
        except:
            #self.period = None
            self.period = 2.0 * PI * (((float(self.semimajor_axis) * 1000.0) ** 3.0) / GM) ** (0.5) / 60.0
        try:
            self.apoapsis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='APOAPSIS']").text
        except:
            #self.apoapsis = None
            self.apoapsis = float(self.semimajor_axis) * (1.0 + float(self.eccentricity)) - MRAD
        try:
            self.periapsis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIAPSIS']").text
        except:
            #self.periapsis = None
            self.periapsis = float(self.semimajor_axis) * (1.0 - float(self.eccentricity)) - MRAD

        try:
            self.originator_comment = root.find(".//COMMENT").text
        except:
            #self.originator_comment = None
            pass
        self.data_created = root.find(".//CREATION_DATE").text or None
        self.originator = root.find(".//ORIGINATOR").text or None

        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def from_tle(self, tle_lines=None):

        if tle_lines is not None:
            if len(tle_lines) == 3:
                tle = TLE.from_lines(*tle_lines)

                self.norad = tle.norad
                self.epoch = tools.doy2datetime(tle.epoch_year, tle.epoch_day)
                #self.epoch = datetime(tle.epoch_year, 1, 1) + timedelta(days=(tle.epoch_day - 1))

        # Format of TLE dict for reference
        #(
        #name='ISS (ZARYA)',
        #norad='25544',
        #classification='U',
        #int_desig='98067A',
        #epoch_year=2019,
        #epoch_day=249.04864348,
        #dn_o2=1.909e-05,
        #ddn_o6=0.0,
        #bstar=4.0858e-05,
        #set_num=999,
        #inc=51.6464,
        #raan=320.1755,
        #ecc=0.0007999,
        #argp=10.9066,
        #M=53.2893,
        #n=15.50437522,
        #rev_num=18780
        #)

        # Orbital mean elements
        self.mean_motion = tle.n
        self.eccentricity = tle.ecc
        self.inclination = tle.inc
        self.raan = tle.raan
        self.arg_of_pericenter = tle.argp
        self.mean_anomaly = tle.M

        # TLE parameters
        self.ephemeris_type = 0
        self.classification_type = tle.classification
        self.element_set_no = tle.set_num
        self.rev_at_epoch = tle.rev_num
        self.bstar = tle.bstar
        self.mean_motion_dot = tle.dn_o2
        self.mean_motion_ddot = tle.ddn_o6

        # User defined parameters (space-track only)
        # Can be computed from orbital mean elements
        self.semimajor_axis = GM13 / ((TPI86 * float(self.mean_motion)) ** (2.0 / 3.0)) / 1000.0
        self.period = 2.0 * PI * (((float(self.semimajor_axis) * 1000.0) ** 3.0) / GM) ** (0.5) / 60.0
        self.apoapsis = float(self.semimajor_axis) * (1.0 + float(self.eccentricity)) - MRAD
        self.periapsis = float(self.semimajor_axis) * (1.0 - float(self.eccentricity)) - MRAD

        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def to_db(self, dbc):
        # Initialize lists for the db columns to write to and for the
        # corresponding values
        db_cols=[]
        db_vals=[]

        # Loop over all attributes and put the attributes which are not None
        # to the above lists
        for attr in self.__dict__:
            val = getattr(self, attr)
            if val is not None:
                db_cols.append(attr)
                db_vals.append(val)

        # Create the sql statement to insert the data to the db
        ps = ["%s"] * len(db_cols)
        sql = "insert ignore into orbelem ("
        sql += ", ".join(db_cols)
        sql += ") values ("
        sql += ", ".join(ps)
        sql += ")"

        # Execute the sql statement
        res = dbc.write(sql, tuple(db_vals))
