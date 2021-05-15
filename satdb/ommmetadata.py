from datetime import datetime

NULL="NULL"

# Class for object metadata
class OMMMetadata:
    def __init__(self, segment):
        self.segment = segment
        self.obj_id = NULL
        self.id_short = NULL
        self.name = None
        self.center_name = None
        self.ref_frame = None
        self.mean_element_theory = None
        # self.description = None
        # self.image = None
        self.created = None
        self.obj_type = None
        self.rcs_size = None
        self.country_code = None
        self.launch_date = None
        self.site = None
        self.decay_date = None
        self.classification_type = None
        self.norad_cat_id = None
        self.name = None
        self.read_data()

    def read_data(self):
        self.obj_id = self.segment.find(".//metadata/OBJECT_ID").text or NULL
        if self.obj_id != NULL:
            self.id_short = self.obj_id[2:4] + self.obj_id[5:]
        self.name = self.segment.find(".//metadata/OBJECT_NAME").text
        self.center_name = self.segment.find(".//metadata/CENTER_NAME").text
        self.ref_frame = self.segment.find(".//metadata/REF_FRAME").text
        self.mean_element_theory = self.segment.find(".//metadata/MEAN_ELEMENT_THEORY").text
        # description
        # image
        self.created = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        try:
            self.obj_type = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='OBJECT_TYPE']").text
        except:
            self.obj_type = NULL
        try:
            self.rcs_size = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='RCS_SIZE']").text
        except:
            self.rcs_size = NULL
        try:
            self.country_code = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='COUNTRY_CODE']").text
        except:
            self.country_code = NULL
        try:
            self.launch_date = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='LAUNCH_DATE']").text
        except:
            self.launch_date = NULL
        try:
            self.site = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='SITE']").text
        except:
            self.site = NULL
        try:
            self.decay_date = self.segment.find(".//userDefinedParameters/USER_DEFINED[@parameter='DECAY_DATE']").text
        except:
            self.decay_date = NULL

        self.classification_type = self.segment.find(".//tleParameters/CLASSIFICATION_TYPE").text or NULL
        self.norad_cat_id = self.segment.find(".//tleParameters/NORAD_CAT_ID").text or NULL
        self.name = self.segment.find(".//metadata/OBJECT_NAME").text or NULL

