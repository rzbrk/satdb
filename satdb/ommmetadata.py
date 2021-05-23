from datetime import datetime
import re

#NULL="NULL"

# Class for object metadata
class OMMMetadata:
    def __init__(self):
        self.norad = None

        # We "borrow the epoch from the mean orbital elements also for the
        # metadata
        self.epoch = None

        # OMM standard metadata (celestrak & spacetrack)
        self.obj_id = None
        self.id_short = None # derived from obj_id)
        self.name = None
        self.center_name = None
        self.ref_frame = None
        self.mean_element_theory = None
        self.classification_type = None # from tle parameters

        # OMM user defined metadata parameters (spacetrack only)
        self.obj_type = None
        self.rcs_size = None
        self.country_code = None
        self.launch_date = None
        self.site = None
        self.decay_date = None

        # Creation date/time of entry in database
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def set(self, **kwargs):
        # Loop over the kwargs dictionary
        for key, value in kwargs.items():
            # If object/instance has attribute, change it to the given value
            if hasattr(self, key):
                setattr(self, key, value)
        # Always update/overwrite the attribute created
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    def from_omm(self, segment):
        self.norad = segment.find(".//tleParameters/NORAD_CAT_ID").text

        self.epoch = segment.find(".//meanElements/EPOCH").text or None

        self.obj_id = segment.find(".//metadata/OBJECT_ID").text
        if self.obj_id is not None:
            if re.match('^[\d]{4}-[\d]{3}[A-Z]{0,3}$', self.obj_id):
                self.id_short = self.obj_id[2:4] + self.obj_id[5:]
        self.name = segment.find(".//metadata/OBJECT_NAME").text
        self.center_name = segment.find(".//metadata/CENTER_NAME").text
        self.ref_frame = segment.find(".//metadata/REF_FRAME").text
        self.mean_element_theory = segment.find(".//metadata/MEAN_ELEMENT_THEORY").text

        self.classification_type = segment.find(".//tleParameters/CLASSIFICATION_TYPE").text

        # OMM user defined parameters
        try:
            self.obj_type = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='OBJECT_TYPE']").text
        except:
            #self.obj_type = NULL
            pass
        try:
            self.rcs_size = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='RCS_SIZE']").text
        except:
            #self.rcs_size = NULL
            pass
        try:
            self.country_code = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='COUNTRY_CODE']").text
        except:
            #self.country_code = NULL
            pass
        try:
            self.launch_date = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='LAUNCH_DATE']").text
        except:
            #self.launch_date = "0000-00-00T00:00:00"
            pass
        try:
            self.site = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SITE']").text
        except:
            #self.site = NULL
            pass
        try:
            self.decay_date = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='DECAY_DATE']").text
        except:
            #self.decay_date = "0000-00-00T00:00:00"
            pass

        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

        #self.__empty2null()

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
        sql = "insert ignore into metadata ("
        sql += ", ".join(db_cols)
        sql += ") values ("
        sql += ", ".join(ps)
        sql += ")"

        # Execute the sql statement
        res = dbc.write(sql, tuple(db_vals))

