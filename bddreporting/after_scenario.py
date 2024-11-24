from .utils import extract_multiline_string, applyJinja2Template
import sys
from .config import Config
from .utils import write_text, get_current_date_time

def after_scenario(func):
    def wrapper(*args, **kwargs):
        context = args[0]
        scenario = args[1]

        report_tag = Config.get("report_tag", "report")

        if not ( not report_tag or report_tag in scenario.tags):
            return 

        # Create a directory based on the feature name
        scenario_name = scenario.name

        if Config.get("scenario_header", False ):
            header = Config.get("scenario_header", "")
        else:
            header = extract_multiline_string( scenario.description )

        current_date, current_time = get_current_date_time()

        outline_parameter = { "scenario": scenario.name , "feature": scenario.feature.name, "date": current_date, "time": current_time }
        if context.active_outline:
            row = context.active_outline
            outline_parameter = outline_parameter | dict(zip(row.headings, row.cells))
            scenario_name = scenario_name.format(**outline_parameter)
        try:
            header = applyJinja2Template( header, outline_parameter )    
        except:
            pass

        text = ""
        if header and len( header ) > 0:
            text = header + "\n" * 2

        # Ensure the log is set up in the context (you could accumulate log messages in context.log during the steps)
        if hasattr(context, "log"): 
            text += context.log
            
        if len( text ) > 0:
            if Config.get("export_scenario", True):
                write_text( text, context.feature.filename, context.feature.name, scenario.name, scenario.tags )
            elif hasattr(context.feature, "log"):
                pass
                context.feature.log += text

        if Config.get("halt_execution_on_failure", False) and context.failed:
            sys.exit("Exiting the behave test runner.")
        result = func(*args, **kwargs)
        return result
    return wrapper
