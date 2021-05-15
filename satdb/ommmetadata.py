from datetime import datetime

NULL="NULL"

# Class for object metadata
class OMMMetadata:
    def __init__(self):
        self.norad = None

        # OMM standard metadata (celestrak & spacetrack)
        self.name = None
        self.obj_id = None
        self.id_short = None # derived from obj_id)
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
        self.created = None

    def from_omm(self, segment):
        self.norad = segment.find(".//tleParameters/NORAD_CAT_ID").text or NULL

        self.obj_id = segment.find(".//metadata/OBJECT_ID").text or NULL
        if self.obj_id != NULL:
            self.id_short = self.obj_id[2:4] + self.obj_id[5:]
        self.name = segment.find(".//metadata/OBJECT_NAME").text
        self.center_name = segment.find(".//metadata/CENTER_NAME").text
        self.ref_frame = segment.find(".//metadata/REF_FRAME").text
        self.mean_element_theory = segment.find(".//metadata/MEAN_ELEMENT_THEORY").text

        self.classification_type = segment.find(".//tleParameters/CLASSIFICATION_TYPE").text or NULL

        # OMM user defined parameters
        try:
            self.obj_type = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='OBJECT_TYPE']").text
        except:
            self.obj_type = NULL
        try:
            self.rcs_size = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='RCS_SIZE']").text
        except:
            self.rcs_size = NULL
        try:
            self.country_code = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='COUNTRY_CODE']").text
        except:
            self.country_code = NULL
        try:
            self.launch_date = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='LAUNCH_DATE']").text
        except:
            self.launch_date = "0000-00-00T00:00:00"
        try:
            self.site = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SITE']").text
        except:
            self.site = NULL
        try:
            self.decay_date = segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='DECAY_DATE']").text
        except:
            self.decay_date = "0000-00-00T00:00:00"

        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

