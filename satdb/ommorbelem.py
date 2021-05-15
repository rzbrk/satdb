from datetime import datetime

NULL="NULL"

# Class for orbital elements
class OMMOrbelem:
    def __init__(self, segment, root):
        self.segment = segment
        self.root = root
        self.epoch = None
        self.mean_motion = None
        self.eccentricity = None
        self.inclination = None
        self.raan = None
        self.arg_of_pericenter = None
        self.mean_anomaly = None
        self.ephemeris_type = None
        self.norad_cat_id = None
        self.element_set_no = None
        self.rev_at_epoch = None
        self.bstar = None
        self.mean_motion_dot = None
        self.mean_motion_ddot = None
        self.tle_line0 = None
        self.tle_line1 = None
        self.tle_line2 = None
        self.semimajor_axis = None
        self.period = None
        self.apoapsis = None
        self.periapsis = None
        self.ingested = None
        self.originator = None
        self.data_created = None
        self.originator_comment = None
        self.read_data()

    def read_data(self):
        self.epoch = self.segment.find(".//meanElements/EPOCH").text or NULL
        self.mean_motion = self.segment.find(".//meanElements/MEAN_MOTION").text or NULL
        self.eccentricity = self.segment.find(".//meanElements/ECCENTRICITY").text or NULL
        self.inclination = self.segment.find(".//meanElements/INCLINATION").text or NULL
        self.raan = self.segment.find(".//meanElements/RA_OF_ASC_NODE").text or NULL
        self.arg_of_pericenter = self.segment.find(".//meanElements/ARG_OF_PERICENTER").text or NULL
        self.mean_anomaly = self.segment.find(".//meanElements/MEAN_ANOMALY").text or NULL
        self.ephemeris_type = self.segment.find(".//tleParameters/EPHEMERIS_TYPE").text or NULL
        self.norad_cat_id = self.segment.find(".//tleParameters/NORAD_CAT_ID").text or NULL
        self.element_set_no = self.segment.find(".//tleParameters/ELEMENT_SET_NO").text or NULL
        self.rev_at_epoch = self.segment.find(".//tleParameters/REV_AT_EPOCH").text or NULL
        self.bstar =  self.segment.find(".//tleParameters/BSTAR").text or NULL
        self.mean_motion_dot = self.segment.find(".//tleParameters/MEAN_MOTION_DOT").text or NULL
        self.mean_motion_ddot = self.segment.find(".//tleParameters/MEAN_MOTION_DDOT").text or NULL
        self.tle_line0 = NULL
        self.tle_line1 = NULL
        self.tle_line2 = NULL
        try:
            self.semimajor_axis = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SEMIMAJOR_AXIS']").text
        except:
            self.semimajor_axis = NULL
        try:
            self.period = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIOD']").text
        except:
            self.perio = NULL
        try:
            self.apoapsis = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='APOAPSIS']").text
        except:
            self.apoapsis = NULL
        try:
            self.periapsis = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='PERIAPSIS']").text
        except:
            self.periapsis = NULL
        self.ingested = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            self.originator_comment = self.root.find(".//COMMENT").text
        except:
            self.originator_comment = NULL
        self.date_created = self.root.find(".//CREATION_DATE").text or NULL
        self.originator = self.root.find(".//ORIGINATOR").text or NULL

