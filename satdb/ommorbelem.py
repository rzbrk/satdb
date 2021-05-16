from datetime import datetime

NULL="NULL"

# Some constants to compute orbital parameters
GM = 398600441800000.0      # gravitational const * mass Earth
GM13 = GM ** (1.0/3.0)
MRAD = 6378.137             # Earth's radius [km]
PI = 3.14159265358979
TPI86 = 2.0 * PI / 86400.0

# Class for orbital elements
class OMMOrbelem:
    def __init__(self):
        #self.segment = segment
        #self.root = root

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
        # classification type --> metadata
        self.norad = None
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

        self.ingested = None # Date/time, when data was ingested to db

        # Some additional info (space-track only)
        self.originator = None
        self.data_created = None
        self.originator_comment = None

        #self.read_data()

    def from_omm(self, segment, root):
        # Orbital mean elements (celestrak + space-track)
        self.epoch = segment.find(".//meanElements/EPOCH").text or NULL
        self.mean_motion = segment.find(".//meanElements/MEAN_MOTION").text or NULL
        self.eccentricity = segment.find(".//meanElements/ECCENTRICITY").text or NULL
        self.inclination = segment.find(".//meanElements/INCLINATION").text or NULL
        self.raan = segment.find(".//meanElements/RA_OF_ASC_NODE").text or NULL
        self.arg_of_pericenter = segment.find(".//meanElements/ARG_OF_PERICENTER").text or NULL
        self.mean_anomaly = segment.find(".//meanElements/MEAN_ANOMALY").text or NULL

        # TLE parameters (celestrak + space-track)
        self.ephemeris_type = segment.find(".//tleParameters/EPHEMERIS_TYPE").text or NULL
        self.norad = segment.find(".//tleParameters/NORAD_CAT_ID").text or NULL
        self.element_set_no = segment.find(".//tleParameters/ELEMENT_SET_NO").text or NULL
        self.rev_at_epoch = segment.find(".//tleParameters/REV_AT_EPOCH").text or NULL
        self.bstar =  segment.find(".//tleParameters/BSTAR").text or NULL
        self.mean_motion_dot = segment.find(".//tleParameters/MEAN_MOTION_DOT").text or NULL
        self.mean_motion_ddot = segment.find(".//tleParameters/MEAN_MOTION_DDOT").text or NULL

        # TLE/3LE (can be computed from the TLE parameters above)
        self.tle_line0 = NULL
        self.tle_line1 = NULL
        self.tle_line2 = NULL

        # User defined parameters (space-track only)
        # Can be computed from orbital mean elements
        try:
            self.semimajor_axis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SEMIMAJOR_AXIS']").text
        except:
            #self.semimajor_axis = NULL
            self.semimajor_axis = GM13 / ((TPI86 * float(self.mean_motion)) ** (2.0 / 3.0)) / 1000.0
        try:
            self.period = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIOD']").text
        except:
            #self.period = NULL
            self.period = 2.0 * PI * (((float(self.semimajor_axis) * 1000.0) ** 3.0) / GM) ** (0.5) / 60.0
        try:
            self.apoapsis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='APOAPSIS']").text
        except:
            #self.apoapsis = NULL
            self.apoapsis = float(self.semimajor_axis) * (1.0 + float(self.eccentricity)) - MRAD
        try:
            self.periapsis = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIAPSIS']").text
        except:
            #self.periapsis = NULL
            self.periapsis = float(self.semimajor_axis) * (1.0 - float(self.eccentricity)) - MRAD

        self.ingested = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        try:
            self.originator_comment = root.find(".//COMMENT").text
        except:
            self.originator_comment = NULL
        self.date_created = root.find(".//CREATION_DATE").text or NULL
        self.originator = root.find(".//ORIGINATOR").text or NULL

