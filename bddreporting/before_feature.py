import os
import json
import codecs
import sys
from datetime import datetime
from .utils import extract_multiline_string, applyJinja2Template, get_current_date_time
from .config import Config

def before_feature(func):
    def wrapper(*args, **kwargs):
        feature = args[1]
        feature.feature_file_abspath = os.path.dirname ( os.path.abspath( feature.filename ) )
        current_date, current_time = get_current_date_time()

        report_tag = Config.get("report_tag", "report")

        if not ( not report_tag or report_tag in feature.tags):
            return

        if not Config.get("export_scenario", False):

            header = ""
            if Config.get("feature_header", False ):
                header = Config.get("feature_header", "")
            else:
                header = extract_multiline_string( feature.description )

            feature_parameter = { "date": current_date, "time": current_time }
            header = applyJinja2Template( header, feature_parameter )  

            if header and len( header ) > 0:
                feature.log = header + "\n" * 2  
        result = func(*args, **kwargs)
        return result
    return wrapper